"""Durable semantic decision intent between judgment and runtime checkpoint.

The event runtime acknowledges a response only after its processor returns.
Workspace writes, however, can finish before that checkpoint replacement.  A
small per-session intent journal bridges that crash window: it preserves the
already-validated semantic decision and the exact processor result so replay
can finish the guarded write without asking the semantic agent a second time.

This journal is temporary runtime state, not a Context Owner.  It is removed
only after the runtime confirms that the same event id and content digest are
the committed checkpoint.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any

from .runner import MaintainerDecision


INTENT_SCHEMA = "context-maintain.decision-intent.v1"
INTENT_FILENAME = "maintain-decision-intent.json"
INTENT_LOCK_FILENAME = "maintain-decision-intent.lock"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class DecisionIntentError(RuntimeError):
    """A pending semantic decision cannot be trusted or safely replaced."""


class DecisionIntentConflictError(DecisionIntentError):
    """Another uncommitted event already owns the one-session journal."""


@dataclass(frozen=True)
class DecisionIntent:
    """One exact validated semantic result waiting for event acknowledgement."""

    key: str
    workspace_id: str
    event_id: str
    content_sha256: str
    thread_id: str
    decision: MaintainerDecision
    processor_result: str | dict[str, Any]
    agent_state: dict[str, Any]

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        event_id: str,
        content_sha256: str,
        thread_id: str,
        decision: MaintainerDecision,
        processor_result: str | Mapping[str, Any],
        agent_state: Mapping[str, Any],
    ) -> DecisionIntent:
        key = _intent_key(event_id, content_sha256)
        value = {
            "schema": INTENT_SCHEMA,
            "key": key,
            "workspace_id": workspace_id,
            "event_id": event_id,
            "content_sha256": content_sha256,
            "thread_id": thread_id,
            "decision": decision.to_dict(),
            # Proposals are duplicated deliberately.  This makes the
            # judgment-to-write boundary explicit and detects a journal whose
            # decision and write material were edited independently.
            "proposals": decision.to_dict()["writes"],
            "processor_result": processor_result,
            "agent_state": dict(agent_state),
        }
        return cls.from_object(value, expected_workspace_id=workspace_id)

    @classmethod
    def from_object(
        cls, value: object, *, expected_workspace_id: str
    ) -> DecisionIntent:
        if not isinstance(value, dict):
            raise DecisionIntentError("decision intent must be a JSON object")
        required = {
            "schema",
            "key",
            "workspace_id",
            "event_id",
            "content_sha256",
            "thread_id",
            "decision",
            "proposals",
            "processor_result",
            "agent_state",
        }
        if set(value) != required:
            raise DecisionIntentError(
                "decision intent has missing or unexpected fields"
            )
        if value.get("schema") != INTENT_SCHEMA:
            raise DecisionIntentError("decision intent schema is unsupported")

        workspace_id = _nonblank_string(value.get("workspace_id"), "workspace_id")
        if workspace_id != expected_workspace_id:
            raise DecisionIntentError(
                "decision intent belongs to another Workspace"
            )
        event_id = _nonblank_string(value.get("event_id"), "event_id")
        content_sha256 = _digest_string(
            value.get("content_sha256"), "content_sha256"
        )
        key = _digest_string(value.get("key"), "key")
        if key != _intent_key(event_id, content_sha256):
            raise DecisionIntentError("decision intent key does not match its event")
        thread_id = _nonblank_string(value.get("thread_id"), "thread_id")

        try:
            decision = MaintainerDecision.from_object(value.get("decision"))
        except Exception as error:
            raise DecisionIntentError(
                "decision intent contains an invalid semantic decision"
            ) from error
        if decision.workspace_id != workspace_id or decision.event_id != event_id:
            raise DecisionIntentError(
                "decision intent semantic identity does not match its event"
            )
        if value.get("proposals") != decision.to_dict()["writes"]:
            raise DecisionIntentError(
                "decision intent proposals differ from the semantic decision"
            )

        processor_result = _processor_result(
            value.get("processor_result"), decision
        )
        agent_state = _agent_state(value.get("agent_state"), thread_id)
        return cls(
            key=key,
            workspace_id=workspace_id,
            event_id=event_id,
            content_sha256=content_sha256,
            thread_id=thread_id,
            decision=decision,
            processor_result=processor_result,
            agent_state=agent_state,
        )

    def to_object(self) -> dict[str, Any]:
        decision = self.decision.to_dict()
        return {
            "schema": INTENT_SCHEMA,
            "key": self.key,
            "workspace_id": self.workspace_id,
            "event_id": self.event_id,
            "content_sha256": self.content_sha256,
            "thread_id": self.thread_id,
            "decision": decision,
            "proposals": decision["writes"],
            "processor_result": self.processor_result,
            "agent_state": self.agent_state,
        }


class DecisionIntentStore:
    """Atomic, single-pending-intent storage inside one runtime session."""

    def __init__(self, runtime_session_root: Path, workspace_id: str) -> None:
        root = Path(runtime_session_root)
        if root.is_symlink():
            raise DecisionIntentError("runtime session root must not be a symlink")
        try:
            self.root = root.resolve(strict=True)
        except FileNotFoundError as error:
            raise DecisionIntentError("runtime session root does not exist") from error
        if not self.root.is_dir():
            raise DecisionIntentError("runtime session root must be a directory")
        self.workspace_id = _nonblank_string(workspace_id, "workspace_id")
        self.path = self.root / INTENT_FILENAME
        self.lock_path = self.root / INTENT_LOCK_FILENAME

    def load(self) -> DecisionIntent | None:
        with self._locked():
            return self._load_locked()

    def persist(self, intent: DecisionIntent) -> DecisionIntent:
        if intent.workspace_id != self.workspace_id:
            raise DecisionIntentError("cannot store another Workspace intent")
        with self._locked():
            existing = self._load_locked()
            if existing is not None:
                if existing.to_object() == intent.to_object():
                    return existing
                raise DecisionIntentConflictError(
                    "another decision intent is still awaiting checkpoint commit"
                )
            self._atomic_write(intent.to_object())
            return intent

    def clear_if(self, *, event_id: str, content_sha256: str) -> bool:
        """Remove only the exact intent named by a committed checkpoint."""

        with self._locked():
            existing = self._load_locked()
            if existing is None:
                return False
            if (
                existing.event_id != event_id
                or existing.content_sha256 != content_sha256
            ):
                return False
            self.path.unlink()
            _fsync_directory(self.root)
            return True

    def _load_locked(self) -> DecisionIntent | None:
        if self.path.is_symlink():
            raise DecisionIntentError("decision intent must not be a symlink")
        if not self.path.exists():
            return None
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise DecisionIntentError(
                "stored decision intent is not valid UTF-8 JSON"
            ) from error
        return DecisionIntent.from_object(
            value, expected_workspace_id=self.workspace_id
        )

    def _atomic_write(self, value: object) -> None:
        payload = (
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".maintain-decision-intent-", suffix=".tmp", dir=self.root
        )
        temporary_path = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb") as handle:
                descriptor = -1
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            if self.path.exists() or self.path.is_symlink():
                raise DecisionIntentConflictError(
                    "decision intent appeared during atomic publication"
                )
            os.replace(temporary_path, self.path)
            _fsync_directory(self.root)
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            if temporary_path.exists():
                temporary_path.unlink()

    @contextmanager
    def _locked(self) -> Iterator[None]:
        flags = os.O_RDWR | os.O_CREAT
        flags |= getattr(os, "O_NOFOLLOW", 0)
        descriptor: int | None = None
        try:
            if self.lock_path.is_symlink():
                raise DecisionIntentError(
                    "decision intent lock must not be a symlink"
                )
            try:
                descriptor = os.open(self.lock_path, flags, 0o600)
            except OSError as error:
                raise DecisionIntentError(
                    "decision intent lock could not be opened safely"
                ) from error
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise DecisionIntentError(
                    "decision intent lock must be a regular file"
                )
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            if descriptor is not None:
                try:
                    fcntl.flock(descriptor, fcntl.LOCK_UN)
                finally:
                    os.close(descriptor)


def _intent_key(event_id: str, content_sha256: str) -> str:
    event = _nonblank_string(event_id, "event_id")
    digest = _digest_string(content_sha256, "content_sha256")
    return hashlib.sha256((event + "\0" + digest).encode("utf-8")).hexdigest()


def _processor_result(
    value: object, decision: MaintainerDecision
) -> str | dict[str, Any]:
    if decision.outcome in {"no_change", "updated_quiet"}:
        if value != decision.outcome:
            raise DecisionIntentError(
                "decision intent processor result does not match its outcome"
            )
        return decision.outcome
    if not isinstance(value, dict) or set(value) != {"outcome", "report"}:
        raise DecisionIntentError("decision intent processor report is malformed")
    if value.get("outcome") != decision.outcome:
        raise DecisionIntentError(
            "decision intent processor report outcome does not match"
        )
    report = value.get("report")
    if not isinstance(report, dict):
        raise DecisionIntentError("decision intent report must be an object")
    expected_fields = {"summary", "changed_paths"}
    if decision.outcome == "needs_decision":
        expected_fields.add("question")
    if set(report) != expected_fields:
        raise DecisionIntentError("decision intent report fields are malformed")
    summary = report.get("summary")
    paths = report.get("changed_paths")
    if not isinstance(summary, str) or not isinstance(paths, list) or any(
        not isinstance(path, str) for path in paths
    ):
        raise DecisionIntentError("decision intent report values are malformed")
    if tuple(paths) != decision.changed_paths:
        raise DecisionIntentError(
            "decision intent report paths differ from the semantic decision"
        )
    if decision.outcome == "needs_decision":
        question = report.get("question")
        if not isinstance(question, str) or not question.strip():
            raise DecisionIntentError(
                "decision intent needs-decision report lacks a question"
            )
    # JSON round-trip makes the returned mapping independent of caller state.
    return json.loads(json.dumps(value, ensure_ascii=False))


def _agent_state(value: object, thread_id: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "thread_id",
        "grounded",
        "workspace_bound",
        "summary",
    }:
        raise DecisionIntentError("decision intent agent state is malformed")
    if value.get("thread_id") != thread_id or value.get("grounded") is not True:
        raise DecisionIntentError("decision intent agent state identity is invalid")
    if not isinstance(value.get("workspace_bound"), bool):
        raise DecisionIntentError(
            "decision intent agent state workspace_bound must be a boolean"
        )
    if not isinstance(value.get("summary"), str):
        raise DecisionIntentError(
            "decision intent agent state summary must be a string"
        )
    return dict(value)


def _nonblank_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise DecisionIntentError(f"{label} must be a non-blank string")
    return value


def _digest_string(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise DecisionIntentError(f"{label} must be a lowercase SHA-256")
    return value


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


__all__ = [
    "DecisionIntent",
    "DecisionIntentConflictError",
    "DecisionIntentError",
    "DecisionIntentStore",
    "INTENT_FILENAME",
    "INTENT_LOCK_FILENAME",
]
