"""Crash-tolerant, session-scoped event storage for Maintain.

This module deliberately stops at the runtime boundary.  It does not install
hooks, start background work, choose a reporting channel, inspect Git, or make
semantic Context decisions.  A caller supplies the runtime root, Workspace id,
session id, and the processor callable.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import shlex
import stat
import time
from typing import Any
import uuid


SESSION_START_SOURCES = frozenset({"startup", "resume", "clear", "compact"})
COMMITTABLE_OUTCOMES = frozenset(
    {"no_change", "updated_quiet", "updated_report", "needs_decision"}
)
CHECKPOINT_OUTCOMES = COMMITTABLE_OUTCOMES | {"gap_abandoned"}
PROCESS_LOCK_WAIT_SECONDS = 95.0
MAX_REPORT_RECIPIENTS = 32
MAX_REPORT_RESOLUTION_BATCH = 128

_PROVENANCE_CODE = re.compile(r"^[a-z0-9][a-z0-9_.:@/-]{0,127}$")


class RuntimeProtocolError(ValueError):
    """An input or stored object does not satisfy the runtime protocol."""


class ProcessingDeferredError(RuntimeError):
    """Defer this event without consuming its processor retry budget."""


FaultInjector = Callable[[str], None]
Processor = Callable[[dict[str, Any]], object]


_TOOL_NAME = re.compile(r"^[A-Za-z0-9_.:/-]{1,128}$")
_TOOL_ID = re.compile(r"^[^\x00-\x1f\x7f]{1,256}$")
_PATCH_HEADER = re.compile(
    r"^\*\*\* (Add|Update|Delete) File: (.+)$", re.MULTILINE
)
_PATH_FIELDS = frozenset(
    {
        "path",
        "file",
        "cwd",
        "workdir",
        "file_path",
        "filepath",
        "working_directory",
    }
)
_SHELL_TOOL_NAMES = frozenset(
    {"bash", "exec", "exec_command", "shell", "shell_command"}
)
_SAFE_RESULT_STATUS = frozenset(
    {
        "success",
        "succeeded",
        "completed",
        "ok",
        "passed",
        "fail",
        "failed",
        "error",
        "timeout",
        "timed_out",
        "cancelled",
        "canceled",
    }
)
_TOOL_HASH_MAX_NODES = 8_192
_TOOL_HASH_MAX_TEXT_CHARS = 1_048_576
_TOOL_HASH_MAX_DEPTH = 32


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _fsync_directory(path: Path) -> None:
    """Make a directory-entry publication durable on the POSIX runtime."""
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        if not stat.S_ISDIR(os.fstat(descriptor).st_mode):
            raise RuntimeProtocolError("publication parent must be a directory")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _bounded_tool_digest(value: object) -> str:
    """Hash the complete accepted JSON value or reject it before serialization.

    The bounds keep synchronous PostToolUse capture predictable.  Oversized or
    deeply nested values are not represented by a prefix/summary hash because
    that would make distinct replays appear identical.
    """
    nodes = 0
    text_chars = 0

    def visit(candidate: object, depth: int) -> None:
        nonlocal nodes, text_chars
        nodes += 1
        if nodes > _TOOL_HASH_MAX_NODES or depth > _TOOL_HASH_MAX_DEPTH:
            raise RuntimeProtocolError(
                "tool payload exceeds the evidence capture bound"
            )
        if isinstance(candidate, str):
            text_chars += len(candidate)
            if text_chars > _TOOL_HASH_MAX_TEXT_CHARS:
                raise RuntimeProtocolError(
                    "tool payload exceeds the evidence capture bound"
                )
        elif candidate is None or isinstance(candidate, (bool, int, float)):
            return
        elif isinstance(candidate, Mapping):
            for key, child in candidate.items():
                if isinstance(key, str):
                    text_chars += len(key)
                    if text_chars > _TOOL_HASH_MAX_TEXT_CHARS:
                        raise RuntimeProtocolError(
                            "tool payload exceeds the evidence capture bound"
                        )
                visit(child, depth + 1)
        elif isinstance(candidate, (list, tuple)):
            for child in candidate:
                visit(child, depth + 1)
        else:
            raise RuntimeProtocolError(
                "tool input and tool response must be JSON-compatible"
            )
    visit(value, 0)
    try:
        return _digest(value)
    except (TypeError, ValueError, RecursionError) as error:
        raise RuntimeProtocolError(
            "tool input and tool response must be JSON-compatible"
        ) from error


def _opaque_key(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:32]


def _event_key(session_id: str, turn_id: str) -> str:
    return _opaque_key(session_id + "\0" + turn_id)


def _require_object(payload: object) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise RuntimeProtocolError("payload must be an object")
    return payload


def _require_string(
    payload: Mapping[str, Any], field: str, *, nonempty: bool = True
) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or (nonempty and not value):
        qualification = "non-empty " if nonempty else ""
        raise RuntimeProtocolError(f"{field} must be a {qualification}string")
    return value


class MaintainRuntime:
    """Store and process response-end events independently per main session."""

    _METRIC_NAMES = (
        "session_starts",
        "prompts",
        "stops",
        "tool_evidence",
        "tool_evidence_duplicates",
        "tool_evidence_conflicts",
        "duplicates",
        "conflicts",
        "malformed",
        "processor_failures",
        "processed",
        "no_change",
        "updated_quiet",
        "updated_report",
        "needs_decision",
        "reports_acknowledged",
        "agent_state_quarantined",
        "gap_repairs",
    )

    def __init__(
        self,
        *,
        runtime_root: Path,
        workspace_id: str,
        fault_injector: FaultInjector | None = None,
    ) -> None:
        if not isinstance(workspace_id, str) or not workspace_id:
            raise ValueError("workspace_id must be a non-empty string")
        self.runtime_root = Path(runtime_root).resolve()
        self.workspace_id = workspace_id
        self.workspace_key = _opaque_key(workspace_id)
        # A namespaced subtree intentionally ignores any repository-global v1
        # queue, cursor, ledger, or control files at runtime_root.
        self.root = self.runtime_root / "workspaces" / self.workspace_key
        self.sessions_root = self.root / "sessions"
        self._fault_injector = fault_injector

    def session_start(self, payload: object) -> dict[str, Any]:
        value = _require_object(payload)
        self._require_event_name(value, "SessionStart")
        session_id = _require_string(value, "session_id")
        source = _require_string(value, "source")
        if source not in SESSION_START_SOURCES:
            raise RuntimeProtocolError(
                "source must be startup, resume, clear, or compact"
            )

        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            metadata = self._load_metadata(session_root, session_id)
            now = _utc_now()
            metadata["first_seen_at"] = metadata.get("first_seen_at") or now
            metadata["last_seen_at"] = now
            metadata["latest_source"] = source
            metadata["start_count"] += 1
            if source == "compact":
                metadata["compact_count"] += 1
            # A compact marker never resets a cursor, queue, or agent session.
            metadata["markers"].append({"source": source, "at": now})
            metadata["markers"] = metadata["markers"][-32:]
            self._atomic_write(session_root / "session.json", metadata)
            self._increment_metrics(session_root, "session_starts")
        return {
            "recorded": True,
            "session_key": _opaque_key(session_id),
            "source": source,
        }

    def user_prompt(self, payload: object) -> dict[str, Any]:
        value = _require_object(payload)
        self._require_event_name(value, "UserPromptSubmit")
        session_id = _require_string(value, "session_id")
        turn_id = _require_string(value, "turn_id")
        prompt = value.get("prompt")
        if not isinstance(prompt, str):
            raise RuntimeProtocolError("prompt must be a string")

        session_root = self._session_root(session_id)
        key = _event_key(session_id, turn_id)
        prompt_hash = _digest(prompt)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
            self._reconcile_capture(session_root, session_id)
            ledger_path = self._ledger_path(session_root, key)
            ledger = self._read_json_object(ledger_path)
            if ledger is not None:
                original_hash = ledger.get("prompt_sha256")
                if original_hash == prompt_hash:
                    # A replay can restore a missing partial whose digest ledger
                    # survived but whose raw allocation did not.
                    if ledger.get("status") == "waiting_stop":
                        sequence = self._positive_int(ledger.get("sequence"))
                        if sequence is not None:
                            partial_path = self._partial_path(
                                session_root, sequence, key
                            )
                            if not partial_path.exists():
                                self._atomic_write(
                                    partial_path,
                                    self._partial(
                                        sequence,
                                        key,
                                        session_id,
                                        turn_id,
                                        prompt,
                                    ),
                                )
                    self._increment_metrics(session_root, "duplicates")
                    self._reconcile_capture(session_root, session_id)
                    refreshed = self._read_json_object(ledger_path) or ledger
                    return {
                        "event_id": key,
                        "sequence": refreshed.get("sequence"),
                        "duplicate": True,
                        "paired": refreshed.get("status") == "queued",
                    }
                self._record_conflict(
                    session_root,
                    ledger_path,
                    ledger,
                    kind="prompt",
                    observed_hash=prompt_hash,
                )
                return {
                    "event_id": key,
                    "sequence": ledger.get("sequence"),
                    "conflict": True,
                }

            sequence = self._allocate_sequence(session_root)
            partial = self._partial(
                sequence, key, session_id, turn_id, prompt
            )
            partial_path = self._partial_path(session_root, sequence, key)
            self._atomic_write(partial_path, partial)
            self._fault("after_prompt_publish")
            ledger = {
                "schema": "context-maintain.digest-ledger.v2",
                "event_id": key,
                "sequence": sequence,
                "status": "waiting_stop",
                "prompt_sha256": prompt_hash,
                "assistant_sha256": None,
                "content_sha256": None,
                "first_seen_at": partial["received_at"],
                "updated_at": _utc_now(),
            }
            self._atomic_write(ledger_path, ledger)
            self._fault("after_prompt_ledger")
            self._write_control(session_root, sequence + 1)
            self._increment_metrics(session_root, "prompts")
            self._reconcile_capture(session_root, session_id)
            refreshed = self._read_json_object(ledger_path) or ledger
            return {
                "event_id": key,
                "sequence": sequence,
                "paired": refreshed.get("status") == "queued",
            }

    def stop(self, payload: object) -> dict[str, Any]:
        value = _require_object(payload)
        self._require_event_name(value, "Stop")
        session_id = _require_string(value, "session_id")
        turn_id = _require_string(value, "turn_id")
        assistant = value.get("last_assistant_message")
        if assistant is not None and not isinstance(assistant, str):
            raise RuntimeProtocolError(
                "last_assistant_message must be a string or null"
            )

        session_root = self._session_root(session_id)
        key = _event_key(session_id, turn_id)
        assistant_hash = _digest(assistant)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
            self._reconcile_capture(session_root, session_id)
            ledger_path = self._ledger_path(session_root, key)
            ledger = self._read_json_object(ledger_path)
            if ledger is None:
                orphan_path = self._orphan_path(session_root, key)
                orphan = self._read_json_object(orphan_path)
                if orphan is not None:
                    original_hash = orphan.get("assistant_sha256")
                    if original_hash == assistant_hash:
                        self._increment_metrics(session_root, "duplicates")
                        return {
                            "event_id": key,
                            "duplicate": True,
                            "paired": False,
                        }
                    orphan["conflict"] = {
                        "kind": "assistant",
                        "observed_sha256": assistant_hash,
                        "detected_at": _utc_now(),
                    }
                    self._atomic_write(orphan_path, orphan)
                    self._increment_metrics(session_root, "conflicts")
                    return {"event_id": key, "conflict": True, "paired": False}
                self._atomic_write(
                    orphan_path,
                    {
                        "schema": "context-maintain.stop-orphan.v2",
                        "event_id": key,
                        "identity": {
                            "session_id": session_id,
                            "turn_id": turn_id,
                        },
                        "assistant": assistant,
                        "assistant_sha256": assistant_hash,
                        "received_at": _utc_now(),
                    },
                )
                self._increment_metrics(session_root, "stops")
                return {"event_id": key, "waiting_user": True, "paired": False}

            status = ledger.get("status")
            if ledger.get("conflict") is not None:
                # Once an observed conflict is recorded, the immutable original
                # remains replayable as a benign duplicate.  Only the differing
                # replay stays conflicting.
                if (
                    status in {"queued", "completed"}
                    and ledger.get("assistant_sha256") == assistant_hash
                ):
                    self._increment_metrics(session_root, "duplicates")
                    return {
                        "event_id": key,
                        "sequence": ledger.get("sequence"),
                        "duplicate": True,
                    }
                return {
                    "event_id": key,
                    "sequence": ledger.get("sequence"),
                    "conflict": True,
                }
            if status in {"queued", "completed"}:
                if ledger.get("assistant_sha256") == assistant_hash:
                    self._increment_metrics(session_root, "duplicates")
                    return {
                        "event_id": key,
                        "sequence": ledger.get("sequence"),
                        "duplicate": True,
                    }
                self._record_conflict(
                    session_root,
                    ledger_path,
                    ledger,
                    kind="assistant",
                    observed_hash=assistant_hash,
                )
                return {
                    "event_id": key,
                    "sequence": ledger.get("sequence"),
                    "conflict": True,
                }

            sequence = self._positive_int(ledger.get("sequence"))
            if sequence is None:
                self._increment_metrics(session_root, "malformed")
                return {"event_id": key, "malformed": True}
            partial_path = self._partial_path(session_root, sequence, key)
            partial = self._validate_partial(
                self._read_json_object(partial_path),
                expected_session_id=session_id,
            )
            if partial is None:
                self._increment_metrics(session_root, "malformed")
                return {
                    "event_id": key,
                    "sequence": sequence,
                    "malformed": True,
                }

            result = self._publish_pair(
                session_root,
                partial,
                assistant,
                assistant_hash,
                ledger_path,
            )
            self._increment_metrics(session_root, "stops")
            return result

    def post_tool_use(self, payload: object) -> dict[str, Any]:
        """Capture only a bounded, sanitized tool-use summary for one turn.

        The full tool input and response are never persisted. Their canonical
        hashes make an exact replay distinguishable from a conflicting replay
        without retaining patches, command arguments, output, or secrets.
        """

        value = _require_object(payload)
        self._require_event_name(value, "PostToolUse")
        session_id = _require_string(value, "session_id")
        turn_id = _require_string(value, "turn_id")
        tool_name = _require_string(value, "tool_name")
        tool_use_id = _require_string(value, "tool_use_id")
        if _TOOL_NAME.fullmatch(tool_name) is None:
            raise RuntimeProtocolError("tool_name has an invalid format")
        if _TOOL_ID.fullmatch(tool_use_id) is None:
            raise RuntimeProtocolError("tool_use_id has an invalid format")
        if "tool_input" not in value or "tool_response" not in value:
            raise RuntimeProtocolError(
                "PostToolUse requires tool_input and tool_response"
            )

        tool_input = value["tool_input"]
        tool_response = value["tool_response"]
        input_hash = _bounded_tool_digest(tool_input)
        response_hash = _bounded_tool_digest(tool_response)

        key = _event_key(session_id, turn_id)
        facts = _sanitize_tool_facts(tool_name, tool_input, tool_response)
        stable = {
            "event_id": key,
            "identity": {"session_id": session_id, "turn_id": turn_id},
            "tool_name": tool_name,
            "tool_use_id": tool_use_id,
            "input_sha256": input_hash,
            "response_sha256": response_hash,
            "facts": facts,
        }
        evidence_hash = _digest(stable)
        record = {
            "schema": "context-maintain.tool-evidence.v1",
            **stable,
            "evidence_sha256": evidence_hash,
            "captured_at": _utc_now(),
        }

        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
            self._reconcile_capture(session_root, session_id)
            evidence_path = self._tool_evidence_path(
                session_root, key, tool_use_id
            )
            if evidence_path.is_symlink():
                self._increment_metrics(session_root, "malformed")
                return {"event_id": key, "malformed": True}
            existing = self._validate_tool_evidence(
                self._read_json_object(evidence_path),
                expected_session_id=session_id,
                expected_turn_id=turn_id,
            )
            if evidence_path.exists() and existing is None:
                self._increment_metrics(session_root, "malformed")
                return {"event_id": key, "malformed": True}
            if existing is not None:
                if existing["evidence_sha256"] == evidence_hash:
                    self._increment_metrics(
                        session_root, "tool_evidence_duplicates"
                    )
                    return {
                        "event_id": key,
                        "tool_use_id": tool_use_id,
                        "duplicate": True,
                    }
                if existing.get("conflict") is None:
                    existing["conflict"] = {
                        "observed_sha256": evidence_hash,
                        "detected_at": _utc_now(),
                    }
                    self._atomic_write(evidence_path, existing)
                    self._increment_metrics(
                        session_root, "tool_evidence_conflicts"
                    )
                return {
                    "event_id": key,
                    "tool_use_id": tool_use_id,
                    "conflict": True,
                }

            ledger_path = self._ledger_path(session_root, key)
            ledger = self._read_json_object(ledger_path)
            if isinstance(ledger, dict) and ledger.get("status") in {
                "queued",
                "completed",
            }:
                digests = ledger.get("tool_evidence_digests")
                digest_key = _opaque_key(tool_use_id)
                if (
                    isinstance(digests, dict)
                    and digests.get(digest_key) == evidence_hash
                ):
                    self._increment_metrics(
                        session_root, "tool_evidence_duplicates"
                    )
                    return {
                        "event_id": key,
                        "tool_use_id": tool_use_id,
                        "duplicate": True,
                    }
                self._record_conflict(
                    session_root,
                    ledger_path,
                    ledger,
                    kind="tool_evidence",
                    observed_hash=evidence_hash,
                )
                self._increment_metrics(
                    session_root, "tool_evidence_conflicts"
                )
                return {
                    "event_id": key,
                    "tool_use_id": tool_use_id,
                    "conflict": True,
                    "late": True,
                }

            created = self._publish_immutable(evidence_path, record)
            if not created:
                # The session lock makes this possible only after external
                # mutation. Never replace the durable first observation.
                self._increment_metrics(session_root, "malformed")
                return {"event_id": key, "malformed": True}
            self._increment_metrics(session_root, "tool_evidence")
            return {
                "event_id": key,
                "tool_use_id": tool_use_id,
                "recorded": True,
            }

    def work_generation(self, session_id: str) -> dict[str, Any]:
        """Return a content-free generation derived from durable queued work.

        The generation is not an in-memory notification counter.  It is a
        digest of immutable queue identities, so it survives process death and
        lets a worker compare its terminal observation after releasing the
        process lock.
        """
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
            return {
                "schema": "context-maintain.work-generation.v1",
                "session_key": _opaque_key(session_id),
                "generation": self._work_generation_locked(session_root),
                "queued": sum(
                    1 for _ in (session_root / "queue").glob("*.json")
                ),
            }

    def process_next(
        self,
        session_id: str,
        processor: Processor,
        *,
        process_lock_wait_seconds: float = PROCESS_LOCK_WAIT_SECONDS,
    ) -> dict[str, Any]:
        """Process at most one event without losing a concurrent wake-up.

        A terminal observation (idle or blocked) is made while the process lock
        is held.  After releasing that lock, the durable queue generation is
        read again.  If capture published work in the narrow unlock window, the
        same caller retries instead of exiting while a concurrently spawned
        worker reports ``busy``.  Once this method has released the process
        lock and observed an unchanged generation, any later capture can start
        a new worker normally.
        """
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        if not callable(processor):
            raise TypeError("processor must be callable")
        if (
            not isinstance(process_lock_wait_seconds, (int, float))
            or isinstance(process_lock_wait_seconds, bool)
            or not 0 <= process_lock_wait_seconds <= 120
        ):
            raise ValueError(
                "process_lock_wait_seconds must be between 0 and 120"
            )
        session_root = self._session_root(session_id)

        while True:
            with self._process_locked(
                session_root,
                wait_seconds=float(process_lock_wait_seconds),
            ) as acquired:
                if not acquired:
                    generation = self.work_generation(session_id)
                    return {
                        "status": "busy",
                        "session_key": _opaque_key(session_id),
                        "work_generation": generation["generation"],
                    }
                result = self._process_next_acquired(
                    session_id,
                    session_root,
                    processor,
                )
                if result.get("status") not in {"idle", "blocked"}:
                    return result
                observed_generation = result["work_generation"]
                self._fault("after_terminal_observation_before_process_unlock")

            current = self.work_generation(session_id)
            if current["generation"] == observed_generation:
                return result
            # Capture published a durable queue entry while this processor was
            # still the process-lock owner.  Retry the terminal observation;
            # process at most the newly available single event in this call.

    def _process_next_acquired(
        self,
        session_id: str,
        session_root: Path,
        processor: Processor,
    ) -> dict[str, Any]:
        """One process-lock owner's work; caller owns the process lock."""

        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
            self._reconcile_capture(session_root, session_id)
            checkpoint, checkpoint_valid = self._load_checkpoint(session_root)
            if not checkpoint_valid:
                return {
                    "status": "blocked",
                    "reason": "malformed_checkpoint",
                    "work_generation": self._work_generation_locked(
                        session_root
                    ),
                }
            self._reconcile_checkpoint_covered_residue(
                session_root,
                checkpoint,
            )
            if checkpoint["last_processed_sequence"] > 0:
                self._clear_processing_lease(
                    session_root,
                    expected_sequence=checkpoint[
                        "last_processed_sequence"
                    ],
                )
            expected = checkpoint["last_processed_sequence"] + 1
            candidates = sorted(
                (session_root / "queue").glob(f"{expected:020d}-*.json")
            )
            if len(candidates) > 1:
                self._increment_metrics(session_root, "malformed")
                return {
                    "status": "blocked",
                    "reason": "queue_conflict",
                    "work_generation": self._work_generation_locked(
                        session_root
                    ),
                }
            if not candidates:
                assigned = self._max_assigned_sequence(session_root)
                if assigned >= expected:
                    gap = self._missing_stop_gap(
                        session_root,
                        processed_sequence=checkpoint[
                            "last_processed_sequence"
                        ],
                        assigned_sequence=assigned,
                    )
                    return {
                        "status": "blocked",
                        "reason": (
                            "missing_stop_gap"
                            if gap is not None
                            else "waiting_pair"
                        ),
                        "expected_sequence": expected,
                        "work_generation": self._work_generation_locked(
                            session_root
                        ),
                    }
                return {
                    "status": "idle",
                    "last_processed_sequence": checkpoint[
                        "last_processed_sequence"
                    ],
                    "work_generation": self._work_generation_locked(
                        session_root
                    ),
                }
            queue_path = candidates[0]
            event = self._validate_event(
                self._read_json_object(queue_path),
                expected_session_id=session_id,
                expected_sequence=expected,
            )
            if event is None:
                self._increment_metrics(session_root, "malformed")
                return {
                    "status": "blocked",
                    "reason": "malformed_event",
                    "work_generation": self._work_generation_locked(
                        session_root
                    ),
                }
            ledger_problem = self._queue_ledger_problem(
                session_root,
                queue_path,
                event,
            )
            if ledger_problem is not None:
                return {
                    "status": "blocked",
                    "reason": ledger_problem,
                    "sequence": expected,
                    "work_generation": self._work_generation_locked(
                        session_root
                    ),
                }
            self._write_processing_lease(session_root, event)

        try:
            processor_result = processor(dict(event))
            outcome, report = self._normalize_processor_result(
                processor_result
            )
        except ProcessingDeferredError:
            with self._session_locked(session_root):
                self._clear_processing_lease(
                    session_root,
                    expected_sequence=expected,
                )
                generation = self._work_generation_locked(session_root)
            return {
                "status": "deferred",
                "reason": "prior_session_pending",
                "sequence": expected,
                "work_generation": generation,
            }
        except Exception:
            with self._session_locked(session_root):
                current, valid = self._load_checkpoint(session_root)
                if valid and current["last_processed_sequence"] < expected:
                    current["failure"] = {
                        "code": "processor_error",
                        "sequence": expected,
                        "attempts": self._failure_attempts(current, expected) + 1,
                        "last_failed_at": _utc_now(),
                    }
                    self._atomic_write(
                        session_root / "checkpoint.json", current
                    )
                    self._increment_metrics(
                        session_root, "processor_failures"
                    )
                self._clear_processing_lease(
                    session_root,
                    expected_sequence=expected,
                )
            return {
                "status": "retry",
                "reason": "processor_error",
                "sequence": expected,
            }

        with self._session_locked(session_root):
            current, valid = self._load_checkpoint(session_root)
            if not valid:
                self._clear_processing_lease(
                    session_root,
                    expected_sequence=expected,
                )
                return {
                    "status": "blocked",
                    "reason": "malformed_checkpoint",
                }
            if current["last_processed_sequence"] >= expected:
                self._reconcile_checkpoint_covered_residue(
                    session_root,
                    current,
                )
                self._clear_processing_lease(
                    session_root,
                    expected_sequence=expected,
                )
                return {
                    "status": "already_processed",
                    "sequence": expected,
                }
            current_event = self._validate_event(
                self._read_json_object(queue_path),
                expected_session_id=session_id,
                expected_sequence=expected,
            )
            if (
                current_event is None
                or current_event["content_sha256"]
                != event["content_sha256"]
            ):
                current["failure"] = {
                    "code": "event_changed_during_processing",
                    "sequence": expected,
                    "attempts": self._failure_attempts(current, expected) + 1,
                    "last_failed_at": _utc_now(),
                }
                self._atomic_write(session_root / "checkpoint.json", current)
                self._increment_metrics(session_root, "processor_failures")
                self._clear_processing_lease(
                    session_root,
                    expected_sequence=expected,
                )
                return {
                    "status": "retry",
                    "reason": "event_changed_during_processing",
                    "sequence": expected,
                }

            ledger_problem = self._queue_ledger_problem(
                session_root,
                queue_path,
                current_event,
            )
            if ledger_problem is not None:
                self._clear_processing_lease(
                    session_root,
                    expected_sequence=expected,
                )
                return {
                    "status": "blocked",
                    "reason": ledger_problem,
                    "sequence": expected,
                    "work_generation": self._work_generation_locked(
                        session_root
                    ),
                }

            now = _utc_now()
            pending = current["pending_reports"]
            if outcome in {"updated_report", "needs_decision"}:
                report_record: dict[str, Any] = {
                    "report_id": _digest(
                        {
                            "event": event["content_sha256"],
                            "outcome": outcome,
                        }
                    )[:32],
                    "kind": outcome,
                    "event_id": event["event_id"],
                    "sequence": expected,
                    "created_at": now,
                    "delivered_to": [],
                }
                if report is not None:
                    report_record["payload"] = report
                pending.append(report_record)
            current["last_processed_sequence"] = expected
            current["last_processed_event"] = event["event_id"]
            current["last_processed_content_sha256"] = event[
                "content_sha256"
            ]
            current["last_processed_at"] = now
            current["last_outcome"] = outcome
            current["failure"] = None
            # Cursor advancement and a needs-decision report are one atomic
            # checkpoint replacement, so neither can exist without the other.
            self._atomic_write(session_root / "checkpoint.json", current)
            self._fault("after_checkpoint_before_cleanup")
            self._complete_event(session_root, event, outcome, queue_path)
            self._clear_processing_lease(
                session_root,
                expected_sequence=expected,
            )
            self._increment_metrics(session_root, "processed")
            self._increment_metrics(session_root, outcome)
            remaining_queue = sum(
                1 for _ in (session_root / "queue").glob("*.json")
            )
            return {
                "status": "processed",
                "outcome": outcome,
                "sequence": expected,
                "pending_report": outcome
                in {"updated_report", "needs_decision"},
                "work_remaining": remaining_queue > 0,
                "work_generation": self._work_generation_locked(session_root),
            }

    def pending_reports(self, session_id: str) -> list[dict[str, Any]]:
        """Return this recipient's not-yet-delivered semantic reports."""
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        recipient_key = _opaque_key(session_id)
        session_root = self._session_root(session_id)
        if (
            not self._valid_session_metadata(
                self._read_json_object(session_root / "session.json"),
                expected_session_hash=_digest(session_id),
            )
            or not self._session_layout_readable(session_root)
        ):
            return []
        with self._session_read_locked(session_root):
            checkpoint, valid = self._load_checkpoint(
                session_root, reconcile_repairs=False
            )
            if not valid:
                return []
            return [
                json.loads(json.dumps(record))
                for record in checkpoint["pending_reports"]
                if recipient_key not in record["delivered_to"]
            ]

    def workspace_pending_reports(
        self, *, exclude_session_id: str
    ) -> list[dict[str, Any]]:
        """Return exact prior semantic reports with only an opaque origin key.

        This never returns session ids, queued prompts, assistant messages, or
        tool evidence.  ``payload`` is the already-persisted semantic report
        intended for user delivery.  The origin key exists solely so the host
        can acknowledge that exact report after a successful stdout flush.
        """
        if not isinstance(exclude_session_id, str) or not exclude_session_id:
            raise ValueError("exclude_session_id must be a non-empty string")
        excluded_key = _opaque_key(exclude_session_id)
        recipient_key = excluded_key
        if not self.sessions_root.exists():
            return []
        reports: list[dict[str, Any]] = []
        for session_root in self._ordered_session_roots(
            exclude_session_id, include_current=False
        ):
            if not self._session_layout_readable(session_root):
                continue
            with self._session_read_locked(session_root):
                checkpoint, valid = self._load_checkpoint(
                    session_root, reconcile_repairs=False
                )
                if not valid:
                    continue
                for record in checkpoint["pending_reports"]:
                    if recipient_key in record["delivered_to"]:
                        continue
                    copy = json.loads(json.dumps(record))
                    copy["origin_session_key"] = session_root.name
                    reports.append(copy)
        reports.sort(
            key=lambda item: (
                str(item.get("created_at", "")),
                str(item["origin_session_key"]),
                int(item.get("sequence", 0)),
                str(item.get("report_id", "")),
            )
        )
        return reports

    def next_runnable_session_id(self) -> str | None:
        """Return one earliest safely recoverable session, or fail closed.

        The raw id is recovered only from the next valid queued response event
        and must match both the established metadata hash and opaque session
        directory.  Fresh sessions, report-only sessions, and an incomplete
        pre-response capture tail do not prevent a later queue from running.
        Any earlier malformed, conflicted, gapped, actively processed, or
        otherwise non-runnable session prevents bypassing it.
        """
        entries = self._established_session_entries_for_recovery()
        if entries is None:
            return None

        for session_root, session_hash in entries:
            status = self._session_status_by_root(session_root, session_hash)
            freshness = status["freshness"]
            pending = status["pending"]
            failure = status["failure"]
            gap = status["gap"]
            integrity = status["integrity"]

            if (
                freshness["state"] == "unknown"
                or bool(gap["detected"])
                or int(integrity["malformed"]) > 0
                or int(integrity["conflicts"]) > 0
                or bool(pending["processor_active"])
            ):
                return None

            queued = int(pending["queued"])
            stale_lease = failure["code"] == "stale_process_lease"
            retry_pending = bool(failure["retry_pending"])
            retry_exhausted = (
                retry_pending
                and isinstance(failure["attempts"], int)
                and not isinstance(failure["attempts"], bool)
                and failure["attempts"] >= 3
            )
            if retry_exhausted:
                return None
            if int(pending["cleanup_residue"]) > 0:
                return self._checkpoint_cleanup_session_id(
                    session_root,
                    expected_session_hash=session_hash,
                )
            if queued > 0 or stale_lease or retry_pending:
                return self._runnable_session_id_from_queue(
                    session_root,
                    expected_session_hash=session_hash,
                )

            if freshness["state"] in {"fresh", "report_pending"}:
                continue
            if self._is_incomplete_capture_tail(status):
                continue
            return None
        return None

    def acknowledge_workspace_report(
        self,
        origin_session_key: str,
        report_id: str,
        recipient_session_id: str,
    ) -> bool:
        """Acknowledge delivery to one recipient without resolving ambiguity."""
        if (
            not isinstance(origin_session_key, str)
            or re.fullmatch(r"[0-9a-f]{32}", origin_session_key) is None
        ):
            raise ValueError("origin_session_key must be a 32-character hex key")
        if not isinstance(report_id, str) or not report_id:
            raise ValueError("report_id must be a non-empty string")
        if not isinstance(recipient_session_id, str) or not recipient_session_id:
            raise ValueError("recipient_session_id must be a non-empty string")
        session_root = self.sessions_root / origin_session_key
        if (
            session_root.is_symlink()
            or not session_root.is_dir()
            or not self._valid_session_metadata(
                self._read_json_object(session_root / "session.json")
            )
            or not self._session_layout_readable(session_root)
        ):
            return False
        with self._session_locked(session_root):
            checkpoint, valid = self._load_checkpoint(session_root)
            if not valid:
                return False
            return self._acknowledge_report_locked(
                session_root,
                checkpoint,
                report_id,
                recipient_key=_opaque_key(recipient_session_id),
            )

    def acknowledge_report(self, session_id: str, report_id: str) -> bool:
        """Acknowledge delivery to the report's current session recipient."""
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        if not isinstance(report_id, str) or not report_id:
            raise ValueError("report_id must be a non-empty string")
        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            checkpoint, valid = self._load_checkpoint(session_root)
            if not valid:
                return False
            return self._acknowledge_report_locked(
                session_root,
                checkpoint,
                report_id,
                recipient_key=_opaque_key(session_id),
            )

    def workspace_unresolved_decisions(
        self, *, for_session_id: str
    ) -> list[dict[str, str]]:
        """Return bounded current/prior decisions, never later-session ones."""
        if not isinstance(for_session_id, str) or not for_session_id:
            raise ValueError("for_session_id must be a non-empty string")
        decisions: list[dict[str, str]] = []
        for session_root in self._ordered_session_roots(
            for_session_id, include_current=True
        ):
            if not self._session_layout_readable(session_root):
                continue
            with self._session_read_locked(session_root):
                checkpoint, valid = self._load_checkpoint(
                    session_root, reconcile_repairs=False
                )
                if not valid:
                    continue
                for record in checkpoint["pending_reports"]:
                    if record["kind"] != "needs_decision":
                        continue
                    payload = record.get("payload")
                    question = (
                        payload.get("question", "")
                        if isinstance(payload, Mapping)
                        else ""
                    )
                    summary = (
                        payload.get("summary", "")
                        if isinstance(payload, Mapping)
                        else ""
                    )
                    decisions.append(
                        {
                            "origin_session_key": session_root.name,
                            "report_id": record["report_id"],
                            "question": question[:500]
                            if isinstance(question, str)
                            else "",
                            "summary": summary[:800]
                            if isinstance(summary, str)
                            else "",
                        }
                    )
        decisions.sort(
            key=lambda item: (
                item["origin_session_key"],
                item["report_id"],
            )
        )
        return decisions[:MAX_REPORT_RESOLUTION_BATCH]

    def resolve_workspace_reports(
        self, report_ids: list[str] | tuple[str, ...]
    ) -> dict[str, list[str]]:
        """Idempotently remove exact resolved needs-decision reports."""
        if not isinstance(report_ids, (list, tuple)):
            raise ValueError("report_ids must be a list or tuple")
        if len(report_ids) > MAX_REPORT_RESOLUTION_BATCH:
            raise ValueError("too many report_ids in one resolution batch")
        if any(
            not isinstance(report_id, str)
            or re.fullmatch(r"[0-9a-f]{32}", report_id) is None
            for report_id in report_ids
        ):
            raise ValueError("report_ids must contain 32-character hex ids")
        requested = sorted(set(report_ids))
        requested_set = set(requested)
        resolved: set[str] = set()
        if requested_set and self.sessions_root.exists():
            for session_root in sorted(self.sessions_root.iterdir()):
                if (
                    session_root.is_symlink()
                    or not session_root.is_dir()
                    or re.fullmatch(r"[0-9a-f]{32}", session_root.name) is None
                    or not self._valid_session_metadata(
                        self._read_json_object(session_root / "session.json")
                    )
                    or not self._session_layout_readable(session_root)
                ):
                    continue
                with self._session_locked(session_root):
                    checkpoint, valid = self._load_checkpoint(session_root)
                    if not valid:
                        continue
                    kept: list[dict[str, Any]] = []
                    changed = False
                    for record in checkpoint["pending_reports"]:
                        if (
                            record["kind"] == "needs_decision"
                            and record["report_id"] in requested_set
                        ):
                            resolved.add(record["report_id"])
                            changed = True
                            continue
                        kept.append(record)
                    if changed:
                        checkpoint["pending_reports"] = kept
                        self._atomic_write(
                            session_root / "checkpoint.json", checkpoint
                        )
        return {
            "requested_report_ids": requested,
            "resolved_report_ids": sorted(resolved),
        }

    def _acknowledge_report_locked(
        self,
        session_root: Path,
        checkpoint: dict[str, Any],
        report_id: str,
        *,
        recipient_key: str,
    ) -> bool:
        for index, record in enumerate(checkpoint["pending_reports"]):
            if record["report_id"] != report_id:
                continue
            if record["kind"] == "updated_report":
                del checkpoint["pending_reports"][index]
            else:
                delivered_to = record["delivered_to"]
                if recipient_key in delivered_to:
                    return False
                # Resolution normally happens long before this bound. Keeping
                # the most recent recipients prevents unbounded checkpoint
                # growth while preserving duplicate suppression for active
                # sessions.
                record["delivered_to"] = (
                    delivered_to + [recipient_key]
                )[-MAX_REPORT_RECIPIENTS:]
            self._atomic_write(session_root / "checkpoint.json", checkpoint)
            self._increment_metrics(session_root, "reports_acknowledged")
            return True
        return False

    def repair_missing_stop_gap(
        self,
        session_id: str,
        expected_sequence: int,
        *,
        approved_by: str,
        reason: str,
    ) -> dict[str, Any]:
        """Abandon exactly one proven missing Stop after explicit approval.

        ``approved_by`` and ``reason`` are deliberately bounded provenance
        codes, not free-form conversation text.  The approved ledger record is
        durable before cursor advancement; if the process dies between those
        publications, checkpoint loading finishes that already-approved repair
        without inventing a new abandonment.
        """
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        if self._positive_int(expected_sequence) is None:
            raise ValueError("expected_sequence must be a positive integer")
        for field, value in (("approved_by", approved_by), ("reason", reason)):
            if not isinstance(value, str) or _PROVENANCE_CODE.fullmatch(value) is None:
                raise ValueError(
                    f"{field} must be a bounded lowercase provenance code"
                )

        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
            self._reconcile_capture(session_root, session_id)
            checkpoint, valid = self._load_checkpoint(session_root)
            if not valid:
                raise RuntimeProtocolError(
                    "cannot repair a gap with a malformed checkpoint"
                )

            existing = self._gap_repair_for_sequence(
                session_root, expected_sequence
            )
            if existing is not None:
                repair = existing["repair"]
                if (
                    repair["approved_by"] == approved_by
                    and repair["reason"] == reason
                ):
                    return {
                        "repaired": True,
                        "duplicate": True,
                        "sequence": expected_sequence,
                        "repair_sha256": repair["repair_sha256"],
                    }
                raise RuntimeProtocolError(
                    "the sequence already has different repair provenance"
                )

            if checkpoint["last_processed_sequence"] + 1 != expected_sequence:
                raise RuntimeProtocolError(
                    "repair must target the exact next expected sequence"
                )
            assigned = self._max_assigned_sequence(session_root)
            gap = self._missing_stop_gap(
                session_root,
                processed_sequence=checkpoint["last_processed_sequence"],
                assigned_sequence=assigned,
            )
            if gap is None or gap["expected_sequence"] != expected_sequence:
                raise RuntimeProtocolError(
                    "repair requires a higher-sequence-proven missing Stop"
                )

            matches: list[tuple[Path, dict[str, Any]]] = []
            for path in (session_root / "ledger").glob("*.json"):
                ledger = self._read_json_object(path)
                if (
                    isinstance(ledger, dict)
                    and self._positive_int(ledger.get("sequence"))
                    == expected_sequence
                ):
                    matches.append((path, ledger))
            if len(matches) != 1:
                raise RuntimeProtocolError(
                    "repair requires exactly one digest ledger for the gap"
                )
            ledger_path, ledger = matches[0]
            if (
                ledger.get("schema") != "context-maintain.digest-ledger.v2"
                or ledger.get("status") != "waiting_stop"
                or not isinstance(ledger.get("event_id"), str)
                or not ledger["event_id"]
                or not _is_sha256(ledger.get("prompt_sha256"))
                or ledger.get("conflict") is not None
            ):
                raise RuntimeProtocolError(
                    "the expected digest ledger is not safely repairable"
                )

            approved_at = _utc_now()
            repair_stable = {
                "schema": "context-maintain.gap-repair.v1",
                "action": "abandon_missing_stop",
                "sequence": expected_sequence,
                "event_id": ledger["event_id"],
                "prompt_sha256": ledger["prompt_sha256"],
                "approved_by": approved_by,
                "reason": reason,
            }
            repair_sha256 = _digest(repair_stable)
            repair = {
                **repair_stable,
                "repair_sha256": repair_sha256,
                "approved_at": approved_at,
            }
            ledger.update(
                {
                    "status": "abandoned",
                    "assistant_sha256": None,
                    "content_sha256": repair_sha256,
                    "outcome": "gap_abandoned",
                    "repair": repair,
                    "completed_at": approved_at,
                    "updated_at": approved_at,
                }
            )
            self._atomic_write(ledger_path, ledger)
            self._fault("after_gap_repair_ledger")
            self._apply_gap_repair_to_checkpoint(
                session_root, checkpoint, ledger
            )
            self._fault("after_gap_repair_checkpoint")
            self._cleanup_repaired_gap(session_root, ledger)
            self._increment_metrics(session_root, "gap_repairs")
            return {
                "repaired": True,
                "duplicate": False,
                "sequence": expected_sequence,
                "repair_sha256": repair_sha256,
            }

    def workspace_runtime_root(self) -> Path:
        """Return the validated Workspace-wide namespace, not a session root."""
        self._ensure_workspace_metadata()
        return self.root

    def session_runtime_root(self, session_id: str) -> Path:
        """Return the validated opaque session namespace for sibling adapters."""
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
        return session_root

    def load_agent_state(self, session_id: str) -> dict[str, Any]:
        """Load the small warm-agent checkpoint without conversation content."""
        session_root = self.session_runtime_root(session_id)
        with self._session_locked(session_root):
            path = session_root / "agent-state.json"
            if path.is_symlink():
                raise RuntimeProtocolError("stored agent state is malformed")
            if not path.exists():
                return self._agent_state_default()
            value = self._read_json_object(path)
            if not self._valid_agent_state(value):
                raise RuntimeProtocolError("stored agent state is malformed")
            return dict(value)

    def quarantine_agent_state(
        self, session_id: str, reason_code: str = "malformed"
    ) -> dict[str, Any]:
        """Quarantine malformed warm-agent state and install a clean default.

        The caller receives no bytes, path derived from content, or parse error
        detail from the rejected file.  A valid state is left untouched so an
        overly broad recovery handler cannot silently discard a warm thread.
        """
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        if (
            not isinstance(reason_code, str)
            or re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", reason_code) is None
        ):
            raise ValueError("reason_code must be a bounded lowercase code")

        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            self._ensure_workspace_metadata()
            self._ensure_session_metadata(session_root, session_id)
            path = session_root / "agent-state.json"
            value = self._read_json_object(path)
            if (
                path.exists()
                and not path.is_symlink()
                and self._valid_agent_state(value)
            ):
                return dict(value)

            if path.exists() or path.is_symlink():
                quarantine_root = session_root / "quarantine"
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                quarantine_path = quarantine_root / (
                    f"agent-state-{reason_code}-{stamp}-{uuid.uuid4().hex}.json"
                )
                os.replace(path, quarantine_path)
                self._increment_metrics(
                    session_root, "agent_state_quarantined"
                )

            default = self._agent_state_default()
            self._atomic_write(path, default)
            return dict(default)

    def last_committed_event(self, session_id: str) -> dict[str, Any] | None:
        """Return only the validated identity of the last durable checkpoint."""
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        session_root = self._session_root(session_id)
        with self._session_locked(session_root):
            checkpoint, valid = self._load_checkpoint(session_root)
            if not valid or checkpoint["last_processed_sequence"] == 0:
                return None
            return {
                "sequence": checkpoint["last_processed_sequence"],
                "event_id": checkpoint["last_processed_event"],
                "content_sha256": checkpoint[
                    "last_processed_content_sha256"
                ],
            }

    def save_agent_state(
        self, session_id: str, state: Mapping[str, Any]
    ) -> dict[str, Any]:
        """Persist a validated thread id and bounded grounding description.

        `updated_at` is runtime-owned so callers cannot make stale state appear
        newer.  The summary is semantic controller output, not a transcript.
        """
        if not isinstance(state, Mapping):
            raise RuntimeProtocolError("agent state must be an object")
        expected_fields = {
            "thread_id",
            "grounded",
            "workspace_bound",
            "summary",
        }
        if set(state) != expected_fields:
            raise RuntimeProtocolError(
                "agent state fields must be thread_id, grounded, "
                "workspace_bound, and summary"
            )
        thread_id = state.get("thread_id")
        grounded = state.get("grounded")
        workspace_bound = state.get("workspace_bound")
        summary = state.get("summary")
        if thread_id is not None and (
            not isinstance(thread_id, str) or not thread_id.strip()
        ):
            raise RuntimeProtocolError(
                "agent state thread_id must be null or a non-blank string"
            )
        if not isinstance(grounded, bool):
            raise RuntimeProtocolError("agent state grounded must be a boolean")
        if not isinstance(workspace_bound, bool):
            raise RuntimeProtocolError(
                "agent state workspace_bound must be a boolean"
            )
        if not isinstance(summary, str):
            raise RuntimeProtocolError("agent state summary must be a string")
        value = {
            "schema": "context-maintain.agent-state.v2",
            "thread_id": thread_id,
            "grounded": grounded,
            "workspace_bound": workspace_bound,
            "summary": summary,
            "updated_at": _utc_now(),
        }
        session_root = self.session_runtime_root(session_id)
        with self._session_locked(session_root):
            self._atomic_write(session_root / "agent-state.json", value)
        return dict(value)

    def status(self, session_id: str | None = None) -> dict[str, Any]:
        """Return content-free freshness and recovery state."""
        if session_id is not None:
            if not isinstance(session_id, str) or not session_id:
                raise ValueError("session_id must be a non-empty string")
            return self._session_status(session_id)

        if not self.sessions_root.exists():
            return {
                "schema": "context-maintain.runtime-status.v2",
                "workspace_id": self.workspace_id,
                "sessions": [],
                "counts": {"sessions": 0, "fresh": 0, "attention": 0},
            }
        sessions: list[dict[str, Any]] = []
        for path in sorted(self.sessions_root.iterdir()):
            if (
                path.is_symlink()
                or not path.is_dir()
                or re.fullmatch(r"[0-9a-f]{32}", path.name) is None
            ):
                continue
            metadata_path = path / "session.json"
            if not metadata_path.exists() and not metadata_path.is_symlink():
                # Old read-created directories have no established session.
                # Omitting them prevents a ghost from claiming freshness.
                continue
            metadata = self._read_json_object(metadata_path)
            if not self._valid_session_metadata(metadata):
                sessions.append(
                    self._unknown_session_status(
                        _digest(path.name), "malformed_session_metadata"
                    )
                )
                continue
            session_hash = str(metadata["session_id_sha256"])
            if not self._session_layout_readable(path):
                sessions.append(
                    self._unknown_session_status(
                        session_hash, "malformed_session_layout"
                    )
                )
                continue
            sessions.append(self._session_status_by_root(path, session_hash))
        return {
            "schema": "context-maintain.runtime-status.v2",
            "workspace_id": self.workspace_id,
            "sessions": sessions,
            "counts": {
                "sessions": len(sessions),
                "fresh": sum(
                    item["freshness"]["state"] == "fresh" for item in sessions
                ),
                "attention": sum(
                    item["freshness"]["state"] != "fresh" for item in sessions
                ),
            },
        }

    def workspace_freshness_summary(
        self, *, exclude_session_id: str | None = None
    ) -> dict[str, Any]:
        """Summarize prior-session readiness without conversation content.

        ``freshness_ready`` treats an otherwise-current session with a pending
        report as semantically caught up. ``ready_for_writes`` is stricter so a
        new session can surface important prior reports before writing.  The
        controller should compute this live at SessionStart; persisting a copy
        in agent state would become stale as prior workers finish.
        """
        if exclude_session_id is not None and (
            not isinstance(exclude_session_id, str) or not exclude_session_id
        ):
            raise ValueError("exclude_session_id must be a non-empty string")
        workspace_status = self.status()
        if exclude_session_id is None:
            sessions = list(workspace_status["sessions"])
        else:
            prior_hashes: set[str] = set()
            for path in self._ordered_session_roots(
                exclude_session_id, include_current=False
            ):
                metadata = self._read_json_object(path / "session.json")
                if self._valid_session_metadata(metadata):
                    assert isinstance(metadata, dict)
                    prior_hashes.add(str(metadata["session_id_sha256"]))
            sessions = [
                item
                for item in workspace_status["sessions"]
                if item.get("session_id_sha256") in prior_hashes
                or item.get("failure", {}).get("code")
                == "malformed_session_metadata"
            ]
        state_counts: dict[str, int] = {}
        report_kinds = {"updated_report": 0, "needs_decision": 0}
        report_count = 0
        trustworthy = True
        freshness_ready = True
        incomplete_capture_tail_sessions = 0
        warning_required = False
        for item in sessions:
            freshness = item["freshness"]
            state = str(freshness["state"])
            state_counts[state] = state_counts.get(state, 0) + 1
            trustworthy = trustworthy and bool(freshness["trustworthy"])
            pending = item["pending"]
            failure = item["failure"]
            gap = item["gap"]
            integrity = item["integrity"]
            incomplete_capture_tail = self._is_incomplete_capture_tail(item)
            incomplete_capture_tail_sessions += int(
                incomplete_capture_tail
            )
            freshness_ready = freshness_ready and (
                state in {"fresh", "report_pending"}
                or incomplete_capture_tail
            )
            report_count += int(pending["reports"])
            retry_warning = (
                bool(failure["retry_pending"])
                and isinstance(failure["attempts"], int)
                and not isinstance(failure["attempts"], bool)
                and failure["attempts"] >= 3
            )
            warning_required = warning_required or (
                state == "unknown"
                or bool(gap["detected"])
                or int(integrity["malformed"]) > 0
                or int(integrity["conflicts"]) > 0
                or retry_warning
                or (
                    incomplete_capture_tail
                    and not self._is_single_user_prompt_tail(item)
                )
            )
            kinds = pending.get("report_kinds", {})
            for kind in report_kinds:
                count = kinds.get(kind, 0) if isinstance(kinds, dict) else 0
                if isinstance(count, int) and not isinstance(count, bool):
                    report_kinds[kind] += max(0, count)
        freshness_ready = freshness_ready and trustworthy
        return {
            "schema": "context-maintain.workspace-freshness.v1",
            "workspace_id": self.workspace_id,
            "sessions_considered": len(sessions),
            "excluded_current_session": exclude_session_id is not None,
            "trustworthy": trustworthy,
            "freshness_ready": freshness_ready,
            "ready_for_writes": freshness_ready and report_count == 0,
            "warning_required": warning_required,
            "states": state_counts,
            "incomplete_capture_tail_sessions": (
                incomplete_capture_tail_sessions
            ),
            # Compatibility alias for the earlier UserPrompt-only contract.
            "unpaired_tail_sessions": incomplete_capture_tail_sessions,
            "pending_reports": {
                "count": report_count,
                "kinds": report_kinds,
            },
        }

    @staticmethod
    def _is_incomplete_capture_tail(status: Mapping[str, Any]) -> bool:
        """Whether a session has only pre-response capture residue.

        Sequence one may be an unmatched UserPrompt.  Any later assigned
        sequence proves this is no longer one isolated incomplete tail.
        """
        freshness = status["freshness"]
        pending = status["pending"]
        failure = status["failure"]
        gap = status["gap"]
        integrity = status["integrity"]
        residue_count = (
            int(pending["waiting_stop"])
            + int(pending["stop_before_user"])
            + int(pending["tool_evidence"])
        )
        return (
            freshness["state"] == "behind"
            and bool(freshness["trustworthy"])
            and freshness["processed_sequence"] == 0
            and int(freshness["captured_sequence"]) <= 1
            and int(pending["queued"]) == 0
            and int(pending["reports"]) == 0
            and residue_count > 0
            and not bool(pending["processor_active"])
            and not bool(failure["retry_pending"])
            and failure["code"] is None
            and not bool(gap["detected"])
            and int(integrity["malformed"]) == 0
            and int(integrity["conflicts"]) == 0
        )

    @classmethod
    def _is_single_user_prompt_tail(cls, status: Mapping[str, Any]) -> bool:
        """Whether the residue is exactly one prompt awaiting its own Stop."""
        if not cls._is_incomplete_capture_tail(status):
            return False
        freshness = status["freshness"]
        pending = status["pending"]
        return (
            int(freshness["captured_sequence"]) == 1
            and int(pending["waiting_stop"]) == 1
            and int(pending["stop_before_user"]) == 0
            and int(pending["tool_evidence"]) == 0
        )

    def _session_status(self, session_id: str) -> dict[str, Any]:
        session_hash = _digest(session_id)
        session_root = self._session_root(session_id)
        if session_root.is_symlink() or not session_root.is_dir():
            return self._unknown_session_status(
                session_hash, "session_not_established"
            )
        metadata = self._read_json_object(session_root / "session.json")
        if not self._valid_session_metadata(
            metadata, expected_session_hash=session_hash
        ):
            return self._unknown_session_status(
                session_hash, "malformed_session_metadata"
            )
        if not self._session_layout_readable(session_root):
            return self._unknown_session_status(
                session_hash, "malformed_session_layout"
            )
        return self._session_status_by_root(session_root, session_hash)

    def _session_status_by_root(
        self, session_root: Path, session_hash: str
    ) -> dict[str, Any]:
        with self._session_read_locked(session_root):
            checkpoint, checkpoint_valid = self._load_checkpoint(
                session_root, reconcile_repairs=False
            )

            queue_count, malformed_queue, max_queue = self._queue_summary(
                session_root
            )
            waiting_stop, conflicts, ledger_malformed, max_ledger = (
                self._ledger_summary(session_root)
            )
            orphan_count, residue_malformed = self._capture_residue_summary(
                session_root
            )
            (
                tool_evidence_count,
                tool_evidence_conflicts,
                tool_evidence_malformed,
            ) = self._tool_evidence_summary(session_root)
            assigned = max(
                self._max_assigned_sequence(session_root),
                max_queue,
                max_ledger,
            )
            processed = (
                checkpoint["last_processed_sequence"]
                if checkpoint_valid
                else None
            )
            pending_reports = (
                len(checkpoint["pending_reports"])
                if checkpoint_valid
                else 0
            )
            (
                cleanup_residue_count,
                cleanup_residue_malformed,
                _cleanup_session_ids,
            ) = (
                self._checkpoint_cleanup_residue_details(
                    session_root,
                    checkpoint,
                )
                if checkpoint_valid
                else (0, 0, set())
            )
            report_kinds = {"updated_report": 0, "needs_decision": 0}
            if checkpoint_valid:
                for report in checkpoint["pending_reports"]:
                    kind = report.get("kind")
                    if kind in report_kinds:
                        report_kinds[kind] += 1
            failure = checkpoint.get("failure") if checkpoint_valid else None
            gap = (
                self._missing_stop_gap(
                    session_root,
                    processed_sequence=processed,
                    assigned_sequence=assigned,
                )
                if processed is not None
                else None
            )
            processing = self._processing_summary(
                session_root,
                checkpoint if checkpoint_valid else None,
            )
            malformed = (
                malformed_queue
                + ledger_malformed
                + residue_malformed
                + tool_evidence_malformed
                + cleanup_residue_malformed
                + int(processing["malformed"])
            )
            conflicts += tool_evidence_conflicts
            gap_repairs = self._gap_repair_summary(session_root)
            trustworthy = (
                checkpoint_valid
                and malformed == 0
                and conflicts == 0
                and gap is None
                and not processing["stale"]
            )
            if not checkpoint_valid:
                state = "unknown"
            elif failure is not None:
                state = "retry_pending"
            elif conflicts or malformed or gap is not None or processing["stale"]:
                state = "attention_required"
            elif pending_reports:
                state = "report_pending"
            elif processing["active"]:
                state = "processing"
            elif (
                assigned > processed
                or queue_count
                or waiting_stop
                or orphan_count
                or tool_evidence_count
                or cleanup_residue_count
            ):
                state = "behind"
            else:
                state = "fresh"

            metrics = self._load_metrics(session_root)
            return {
                "schema": "context-maintain.session-status.v2",
                "workspace_id": self.workspace_id,
                "session_id_sha256": session_hash,
                "freshness": {
                    "state": state,
                    "trustworthy": trustworthy,
                    "captured_sequence": assigned,
                    "processed_sequence": processed,
                    "lag": None
                    if processed is None
                    else max(0, assigned - processed),
                },
                "pending": {
                    "waiting_stop": waiting_stop,
                    "stop_before_user": orphan_count,
                    "tool_evidence": tool_evidence_count,
                    "queued": queue_count,
                    "cleanup_residue": cleanup_residue_count,
                    "reports": pending_reports,
                    "report_kinds": report_kinds,
                    "processor_active": processing["active"],
                },
                "gap": {
                    "detected": gap is not None,
                    "code": gap["code"] if gap is not None else None,
                    "expected_sequence": (
                        gap["expected_sequence"] if gap is not None else None
                    ),
                    "higher_sequence": (
                        gap["higher_sequence"] if gap is not None else None
                    ),
                },
                "failure": {
                    "retry_pending": failure is not None,
                    "code": (
                        failure.get("code")
                        if isinstance(failure, dict)
                        else (
                            "malformed_checkpoint"
                            if not checkpoint_valid
                            else (
                                gap["code"]
                                if gap is not None
                                else processing["code"]
                            )
                        )
                    ),
                    "attempts": failure.get("attempts", 0)
                    if isinstance(failure, dict)
                    else 0,
                },
                "integrity": {
                    "malformed": malformed,
                    "conflicts": conflicts,
                },
                "repairs": {"gap_abandoned": gap_repairs},
                "counts": metrics,
            }

    def _unknown_session_status(
        self, session_hash: str, code: str
    ) -> dict[str, Any]:
        return {
            "schema": "context-maintain.session-status.v2",
            "workspace_id": self.workspace_id,
            "session_id_sha256": session_hash,
            "freshness": {
                "state": "unknown",
                "trustworthy": False,
                "captured_sequence": 0,
                "processed_sequence": None,
                "lag": None,
            },
            "pending": {
                "waiting_stop": 0,
                "stop_before_user": 0,
                "tool_evidence": 0,
                "queued": 0,
                "cleanup_residue": 0,
                "reports": 0,
                "report_kinds": {
                    "updated_report": 0,
                    "needs_decision": 0,
                },
                "processor_active": False,
            },
            "gap": {
                "detected": False,
                "code": None,
                "expected_sequence": None,
                "higher_sequence": None,
            },
            "failure": {
                "retry_pending": False,
                "code": code,
                "attempts": 0,
            },
            "integrity": {
                "malformed": int(code.startswith("malformed_")),
                "conflicts": 0,
            },
            "repairs": {
                "gap_abandoned": {
                    "count": 0,
                    "latest_sequence": None,
                    "latest_approved_by": None,
                    "latest_reason": None,
                }
            },
            "counts": {name: 0 for name in self._METRIC_NAMES},
        }

    @staticmethod
    def _require_event_name(payload: Mapping[str, Any], expected: str) -> None:
        actual = _require_string(payload, "hook_event_name")
        if actual != expected:
            raise RuntimeProtocolError(
                f"hook_event_name must be {expected!r}, received {actual!r}"
            )

    def _session_root(self, session_id: str) -> Path:
        return self.sessions_root / _opaque_key(session_id)

    @contextmanager
    def _session_locked(self, session_root: Path) -> Iterator[None]:
        self._ensure_session_layout(session_root)
        with self._runtime_lock_handle(session_root / ".lock") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @contextmanager
    def _session_read_locked(self, session_root: Path) -> Iterator[None]:
        """Lock an established session without creating or repairing it."""
        with self._runtime_lock_handle(
            session_root / ".lock", create=False
        ) as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @contextmanager
    def _process_locked(
        self, session_root: Path, *, wait_seconds: float = 0.0
    ) -> Iterator[bool]:
        self._ensure_session_layout(session_root)
        with self._runtime_lock_handle(
            session_root / ".process.lock"
        ) as handle:
            deadline = time.monotonic() + wait_seconds
            while True:
                try:
                    fcntl.flock(
                        handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB
                    )
                    break
                except BlockingIOError:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        yield False
                        return
                    time.sleep(min(0.05, remaining))
            try:
                yield True
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @classmethod
    def _process_lock_active(cls, session_root: Path) -> bool:
        """Report a live local processor from its OS lock, never a PID guess."""
        lock_path = session_root / ".process.lock"
        if not lock_path.exists() and not lock_path.is_symlink():
            return False
        with cls._runtime_lock_handle(
            lock_path, create=False
        ) as handle:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            return False

    @staticmethod
    @contextmanager
    def _runtime_lock_handle(
        path: Path, *, create: bool = True
    ) -> Iterator[Any]:
        """Open one regular lock inode without following a symlink."""
        flags = os.O_RDWR | (os.O_CREAT if create else 0)
        nofollow = getattr(os, "O_NOFOLLOW", 0)
        flags |= nofollow
        descriptor: int | None = None
        try:
            if path.is_symlink():
                raise RuntimeProtocolError(
                    "runtime lock path must not be a symlink"
                )
            try:
                descriptor = os.open(path, flags, 0o600)
            except OSError as error:
                raise RuntimeProtocolError(
                    "runtime lock path could not be opened safely"
                ) from error
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise RuntimeProtocolError(
                    "runtime lock path must be a regular file"
                )
            with os.fdopen(descriptor, "r+b") as handle:
                descriptor = None
                yield handle
        finally:
            if descriptor is not None:
                os.close(descriptor)

    def _write_processing_lease(
        self, session_root: Path, event: Mapping[str, Any]
    ) -> None:
        self._atomic_write(
            session_root / "processing.json",
            {
                "schema": "context-maintain.processing.v1",
                "sequence": event["sequence"],
                "event_id": event["event_id"],
                "content_sha256": event["content_sha256"],
                "started_at": _utc_now(),
            },
        )

    def _clear_processing_lease(
        self, session_root: Path, *, expected_sequence: int
    ) -> None:
        path = session_root / "processing.json"
        value = self._read_json_object(path)
        if self._valid_processing_lease(value) and (
            value["sequence"] == expected_sequence
        ):
            self._durable_unlink(path)

    def _processing_summary(
        self,
        session_root: Path,
        checkpoint: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        """Return content-free live/stale processor state.

        A file alone is never proof of a live worker.  The OS process lock is
        authoritative; a leftover lease without that lock is either reconciled
        from a matching committed checkpoint or reported as stale.
        """
        path = session_root / "processing.json"
        active = self._process_lock_active(session_root)
        if not path.exists() and not path.is_symlink():
            return {
                "active": active,
                "stale": False,
                "malformed": False,
                "code": None,
            }

        if path.is_symlink():
            return {
                "active": active,
                "stale": not active,
                "malformed": True,
                "code": "malformed_process_lease",
            }
        value = self._read_json_object(path)
        if not self._valid_processing_lease(value):
            return {
                "active": active,
                "stale": not active,
                "malformed": True,
                "code": "malformed_process_lease",
            }

        if not active and checkpoint is not None:
            committed = self._nonnegative_int(
                checkpoint.get("last_processed_sequence")
            )
            lease_sequence = value["sequence"]
            identity_matches = (
                committed == lease_sequence
                and checkpoint.get("last_processed_event")
                == value["event_id"]
                and checkpoint.get("last_processed_content_sha256")
                == value["content_sha256"]
            )
            if committed is not None and (
                committed > lease_sequence or identity_matches
            ):
                return {
                    "active": False,
                    "stale": False,
                    "malformed": False,
                    "code": None,
                }

        return {
            "active": active,
            "stale": not active,
            "malformed": False,
            "code": None if active else "stale_process_lease",
        }

    def _valid_processing_lease(self, value: object) -> bool:
        if not isinstance(value, dict) or set(value) != {
            "schema",
            "sequence",
            "event_id",
            "content_sha256",
            "started_at",
        }:
            return False
        return (
            value.get("schema") == "context-maintain.processing.v1"
            and self._positive_int(value.get("sequence")) is not None
            and isinstance(value.get("event_id"), str)
            and bool(value["event_id"])
            and isinstance(value.get("content_sha256"), str)
            and len(value["content_sha256"]) == 64
            and isinstance(value.get("started_at"), str)
            and bool(value["started_at"])
        )

    def _ensure_session_layout(self, session_root: Path) -> None:
        self._ensure_workspace_layout()
        for path in (
            session_root,
            session_root / "partials",
            session_root / "orphans",
            session_root / "queue",
            session_root / "ledger",
            session_root / "tool-evidence",
            session_root / "quarantine",
        ):
            if path.is_symlink():
                raise RuntimeProtocolError(
                    "runtime layout must not contain symlink directories"
                )
            if path.exists() and not path.is_dir():
                raise RuntimeProtocolError(
                    "runtime layout entries must be directories"
                )
            path.mkdir(parents=True, exist_ok=True)

    def _ensure_workspace_layout(self) -> None:
        for path in (
            self.runtime_root / "workspaces",
            self.root,
            self.sessions_root,
        ):
            if path.is_symlink():
                raise RuntimeProtocolError(
                    "Workspace runtime namespace must not contain symlinks"
                )
            if path.exists() and not path.is_dir():
                raise RuntimeProtocolError(
                    "Workspace runtime namespace must be a directory"
                )
            path.mkdir(parents=True, exist_ok=True)

    def _ensure_workspace_metadata(self) -> None:
        self._ensure_workspace_layout()
        path = self.root / "workspace.json"
        if path.is_symlink():
            raise RuntimeProtocolError(
                "Workspace runtime metadata must not be a symlink"
            )
        if not path.exists():
            self._publish_immutable(
                path,
                {
                    "schema": "context-maintain.workspace.v2",
                    "workspace_id": self.workspace_id,
                    "workspace_id_sha256": _digest(self.workspace_id),
                },
            )
            return
        value = self._read_json_object(path)
        if value != {
            "schema": "context-maintain.workspace.v2",
            "workspace_id": self.workspace_id,
            "workspace_id_sha256": _digest(self.workspace_id),
        }:
            raise RuntimeProtocolError("Workspace runtime metadata is malformed")

    def _ensure_session_metadata(
        self, session_root: Path, session_id: str
    ) -> None:
        path = session_root / "session.json"
        if path.exists():
            return
        metadata = self._metadata_default(session_id)
        now = _utc_now()
        metadata["first_seen_at"] = now
        metadata["last_seen_at"] = now
        self._atomic_write(path, metadata)

    def _load_metadata(
        self, session_root: Path, session_id: str
    ) -> dict[str, Any]:
        existing = self._read_json_object(session_root / "session.json")
        if not self._valid_session_metadata(
            existing, expected_session_hash=_digest(session_id)
        ):
            return self._metadata_default(session_id)
        assert isinstance(existing, dict)
        return existing

    def _valid_session_metadata(
        self,
        value: object,
        *,
        expected_session_hash: str | None = None,
    ) -> bool:
        if not isinstance(value, dict):
            return False
        session_hash = value.get("session_id_sha256")
        first_seen = value.get("first_seen_at")
        last_seen = value.get("last_seen_at")
        latest_source = value.get("latest_source")
        markers = value.get("markers")
        return (
            value.get("schema") == "context-maintain.session.v2"
            and isinstance(session_hash, str)
            and re.fullmatch(r"[0-9a-f]{64}", session_hash) is not None
            and (
                expected_session_hash is None
                or session_hash == expected_session_hash
            )
            and (
                first_seen is None
                or (isinstance(first_seen, str) and bool(first_seen))
            )
            and (
                last_seen is None
                or (isinstance(last_seen, str) and bool(last_seen))
            )
            and (latest_source is None or latest_source in SESSION_START_SOURCES)
            and self._nonnegative_int(value.get("start_count")) is not None
            and self._nonnegative_int(value.get("compact_count")) is not None
            and isinstance(markers, list)
            and len(markers) <= 32
            and all(
                isinstance(marker, dict)
                and marker.get("source") in SESSION_START_SOURCES
                and isinstance(marker.get("at"), str)
                and bool(marker["at"])
                for marker in markers
            )
        )

    @staticmethod
    def _session_layout_readable(session_root: Path) -> bool:
        required_directories = (
            session_root,
            session_root / "partials",
            session_root / "orphans",
            session_root / "queue",
            session_root / "ledger",
            session_root / "tool-evidence",
            session_root / "quarantine",
        )
        if any(
            path.is_symlink() or not path.is_dir()
            for path in required_directories
        ):
            return False
        lock_path = session_root / ".lock"
        process_lock = session_root / ".process.lock"
        return (
            not lock_path.is_symlink()
            and lock_path.is_file()
            and not process_lock.is_symlink()
            and (not process_lock.exists() or process_lock.is_file())
            and not (session_root / "session.json").is_symlink()
            and (session_root / "session.json").is_file()
        )

    def _ordered_session_roots(
        self, session_id: str, *, include_current: bool
    ) -> list[Path]:
        """Return established current/prior roots in stable session order."""
        current_root = self._session_root(session_id)
        current_metadata = self._read_json_object(current_root / "session.json")
        current_order: tuple[str, str] | None = None
        if self._valid_session_metadata(
            current_metadata, expected_session_hash=_digest(session_id)
        ):
            assert isinstance(current_metadata, dict)
            current_order = (
                str(current_metadata.get("first_seen_at") or ""),
                current_root.name,
            )

        if not self.sessions_root.exists():
            return []
        selected: list[tuple[tuple[str, str], Path]] = []
        for path in self.sessions_root.iterdir():
            if (
                path.is_symlink()
                or not path.is_dir()
                or re.fullmatch(r"[0-9a-f]{32}", path.name) is None
            ):
                continue
            metadata = self._read_json_object(path / "session.json")
            if not self._valid_session_metadata(metadata):
                continue
            assert isinstance(metadata, dict)
            order = (str(metadata.get("first_seen_at") or ""), path.name)
            if path == current_root:
                if include_current:
                    selected.append((order, path))
                continue
            if current_order is None or order < current_order:
                selected.append((order, path))
        selected.sort(key=lambda item: item[0])
        return [path for _, path in selected]

    def _established_session_entries_for_recovery(
        self,
    ) -> list[tuple[Path, str]] | None:
        """Read established session order, or fail closed on unsafe state."""
        if not self.sessions_root.exists():
            return []
        if self.sessions_root.is_symlink() or not self.sessions_root.is_dir():
            return None

        entries: list[tuple[tuple[str, str], Path, str]] = []
        for session_root in self.sessions_root.iterdir():
            if re.fullmatch(r"[0-9a-f]{32}", session_root.name) is None:
                continue
            if session_root.is_symlink() or not session_root.is_dir():
                return None
            metadata_path = session_root / "session.json"
            if not metadata_path.exists() and not metadata_path.is_symlink():
                # A legacy read-created ghost never became an established
                # session and cannot contain a valid recovery identity.
                continue
            if not self._session_layout_readable(session_root):
                return None
            with self._session_read_locked(session_root):
                metadata = self._read_json_object(metadata_path)
                if not self._valid_session_metadata(metadata):
                    return None
                assert isinstance(metadata, dict)
                session_hash = str(metadata["session_id_sha256"])
                order = (
                    str(metadata.get("first_seen_at") or ""),
                    session_root.name,
                )
                entries.append((order, session_root, session_hash))

        entries.sort(key=lambda item: item[0])
        return [
            (session_root, session_hash)
            for _, session_root, session_hash in entries
        ]

    def _runnable_session_id_from_queue(
        self,
        session_root: Path,
        *,
        expected_session_hash: str,
    ) -> str | None:
        """Recover one raw id from the exact next queue event under read lock."""
        with self._session_read_locked(session_root):
            metadata = self._read_json_object(session_root / "session.json")
            if not self._valid_session_metadata(
                metadata,
                expected_session_hash=expected_session_hash,
            ):
                return None
            checkpoint, checkpoint_valid = self._load_checkpoint(
                session_root,
                reconcile_repairs=False,
            )
            if not checkpoint_valid:
                return None

            processing = self._processing_summary(session_root, checkpoint)
            if processing["active"] or processing["malformed"]:
                return None

            queue_count, malformed_queue, max_queue = self._queue_summary(
                session_root
            )
            _waiting_stop, conflicts, ledger_malformed, max_ledger = (
                self._ledger_summary(session_root)
            )
            _orphan_count, residue_malformed = self._capture_residue_summary(
                session_root
            )
            (
                _tool_evidence_count,
                tool_evidence_conflicts,
                tool_evidence_malformed,
            ) = self._tool_evidence_summary(session_root)
            if (
                queue_count <= 0
                or malformed_queue
                or ledger_malformed
                or residue_malformed
                or tool_evidence_malformed
                or conflicts
                or tool_evidence_conflicts
            ):
                return None

            processed = checkpoint["last_processed_sequence"]
            assigned = max(
                self._max_assigned_sequence(session_root),
                max_queue,
                max_ledger,
            )
            if self._missing_stop_gap(
                session_root,
                processed_sequence=processed,
                assigned_sequence=assigned,
            ) is not None:
                return None

            expected = processed + 1
            candidates = sorted(
                (session_root / "queue").glob(f"{expected:020d}-*.json")
            )
            if len(candidates) != 1:
                return None
            event = self._validate_event(
                self._read_json_object(candidates[0]),
                expected_sequence=expected,
            )
            if event is None:
                return None
            identity = event["identity"]
            session_id = identity["session_id"]
            if (
                _digest(session_id) != expected_session_hash
                or _opaque_key(session_id) != session_root.name
                or candidates[0]
                != self._queue_path(session_root, expected, event["event_id"])
            ):
                return None
            return session_id

    def _checkpoint_cleanup_session_id(
        self,
        session_root: Path,
        *,
        expected_session_hash: str,
    ) -> str | None:
        """Recover one raw id whose checkpoint-covered residue needs sweep."""
        with self._session_read_locked(session_root):
            metadata = self._read_json_object(session_root / "session.json")
            if not self._valid_session_metadata(
                metadata,
                expected_session_hash=expected_session_hash,
            ):
                return None
            checkpoint, valid = self._load_checkpoint(
                session_root,
                reconcile_repairs=False,
            )
            if not valid:
                return None
            count, malformed, session_ids = (
                self._checkpoint_cleanup_residue_details(
                    session_root,
                    checkpoint,
                )
            )
            if count <= 0 or malformed or len(session_ids) != 1:
                return None
            session_id = next(iter(session_ids))
            if (
                _digest(session_id) != expected_session_hash
                or _opaque_key(session_id) != session_root.name
            ):
                return None
            return session_id

    @staticmethod
    def _metadata_default(session_id: str) -> dict[str, Any]:
        return {
            "schema": "context-maintain.session.v2",
            "session_id_sha256": _digest(session_id),
            "first_seen_at": None,
            "last_seen_at": None,
            "latest_source": None,
            "start_count": 0,
            "compact_count": 0,
            "markers": [],
        }

    def _allocate_sequence(self, session_root: Path) -> int:
        maximum = self._max_assigned_sequence(session_root)
        control = self._read_json_object(session_root / "control.json")
        candidate = (
            self._positive_int(control.get("next_sequence"))
            if isinstance(control, dict)
            else None
        )
        expected = maximum + 1
        if candidate != expected:
            if control is not None:
                self._increment_metrics(session_root, "malformed")
            self._write_control(session_root, expected)
        return expected

    def _write_control(self, session_root: Path, next_sequence: int) -> None:
        self._atomic_write(
            session_root / "control.json",
            {
                "schema": "context-maintain.control.v2",
                "next_sequence": next_sequence,
                "updated_at": _utc_now(),
            },
        )

    def _reconcile_capture(
        self, session_root: Path, session_id: str | None
    ) -> None:
        maximum = self._max_assigned_sequence(session_root)
        control = self._read_json_object(session_root / "control.json")
        control_next = (
            self._positive_int(control.get("next_sequence"))
            if isinstance(control, dict)
            else None
        )
        if control_next != maximum + 1:
            if control is not None:
                self._increment_metrics(session_root, "malformed")
            self._write_control(session_root, maximum + 1)

        for partial_path in sorted((session_root / "partials").glob("*.json")):
            partial = self._validate_partial(
                self._read_json_object(partial_path),
                expected_session_id=session_id,
            )
            if partial is None:
                continue
            key = partial["event_id"]
            sequence = partial["sequence"]
            ledger_path = self._ledger_path(session_root, key)
            ledger = self._read_json_object(ledger_path)
            prompt_hash = _digest(partial["prompt"])
            if ledger is None:
                if ledger_path.exists() or ledger_path.is_symlink():
                    continue
                ledger = {
                    "schema": "context-maintain.digest-ledger.v2",
                    "event_id": key,
                    "sequence": sequence,
                    "status": "waiting_stop",
                    "prompt_sha256": prompt_hash,
                    "assistant_sha256": None,
                    "content_sha256": None,
                    "first_seen_at": partial["received_at"],
                    "updated_at": _utc_now(),
                    "recovered": True,
                }
                self._atomic_write(ledger_path, ledger)
            elif (
                ledger.get("sequence") != sequence
                or ledger.get("prompt_sha256") != prompt_hash
            ):
                self._record_conflict(
                    session_root,
                    ledger_path,
                    ledger,
                    kind="prompt",
                    observed_hash=prompt_hash,
                )
                continue

            queue_path = self._queue_path(session_root, sequence, key)
            queued = self._validate_event(
                self._read_json_object(queue_path),
                expected_session_id=session_id,
                expected_sequence=sequence,
            )
            if queued is not None:
                if queued["prompt_sha256"] != prompt_hash:
                    self._record_conflict(
                        session_root,
                        ledger_path,
                        ledger,
                        kind="prompt",
                        observed_hash=queued["prompt_sha256"],
                    )
                continue

            orphan_path = self._orphan_path(session_root, key)
            orphan = self._validate_orphan(
                self._read_json_object(orphan_path),
                expected_session_id=session_id,
            )
            if orphan is None:
                continue
            if orphan.get("conflict") is not None:
                observed = orphan["conflict"].get("observed_sha256")
                if isinstance(observed, str):
                    self._record_conflict(
                        session_root,
                        ledger_path,
                        ledger,
                        kind="assistant",
                        observed_hash=observed,
                    )
                continue
            self._publish_pair(
                session_root,
                partial,
                orphan["assistant"],
                orphan["assistant_sha256"],
                ledger_path,
            )

        # A queue published before its digest-ledger update is authoritative:
        # it is immutable and carries its own stable content digest.
        for queue_path in sorted((session_root / "queue").glob("*.json")):
            event = self._validate_event(
                self._read_json_object(queue_path),
                expected_session_id=session_id,
            )
            if event is None:
                continue
            ledger_path = self._ledger_path(session_root, event["event_id"])
            ledger = self._read_json_object(ledger_path)
            if ledger is None:
                if ledger_path.exists() or ledger_path.is_symlink():
                    continue
                ledger = {
                    "schema": "context-maintain.digest-ledger.v2",
                    "event_id": event["event_id"],
                    "sequence": event["sequence"],
                    "status": "waiting_stop",
                    "prompt_sha256": event["prompt_sha256"],
                    "assistant_sha256": None,
                    "content_sha256": None,
                    "first_seen_at": event["captured_at"],
                    "updated_at": _utc_now(),
                    "recovered": True,
                }
            if (
                ledger.get("sequence") != event["sequence"]
                or ledger.get("prompt_sha256") != event["prompt_sha256"]
            ):
                self._record_conflict(
                    session_root,
                    ledger_path,
                    ledger,
                    kind="queue",
                    observed_hash=event["content_sha256"],
                )
                continue
            status = ledger.get("status")
            if ledger.get("conflict") is not None:
                continue
            if status == "waiting_stop":
                self._mark_ledger_queued(ledger_path, ledger, event)
            elif status == "queued":
                if (
                    self._queue_ledger_problem(
                        session_root,
                        queue_path,
                        event,
                    )
                    is not None
                ):
                    continue
            else:
                # Completed/abandoned provenance is never normalized back to
                # queued. Checkpoint-covered raw is swept separately.
                continue
            self._partial_path(
                session_root, event["sequence"], event["event_id"]
            ).unlink(missing_ok=True)
            self._orphan_path(session_root, event["event_id"]).unlink(
                missing_ok=True
            )

        maximum = self._max_assigned_sequence(session_root)
        self._write_control(session_root, maximum + 1)

    def _publish_pair(
        self,
        session_root: Path,
        partial: dict[str, Any],
        assistant: str | None,
        assistant_hash: str,
        ledger_path: Path,
    ) -> dict[str, Any]:
        evidence, malformed, conflicts = self._collect_tool_evidence(
            session_root,
            session_id=partial["identity"]["session_id"],
            turn_id=partial["identity"]["turn_id"],
        )
        if malformed:
            self._increment_metrics(session_root, "malformed")
            return {
                "event_id": partial["event_id"],
                "sequence": partial["sequence"],
                "malformed": True,
            }
        if conflicts:
            return {
                "event_id": partial["event_id"],
                "sequence": partial["sequence"],
                "conflict": True,
            }
        event = self._event(partial, assistant, assistant_hash, evidence)
        queue_path = self._queue_path(
            session_root, partial["sequence"], partial["event_id"]
        )
        created = self._publish_immutable(queue_path, event)
        if not created:
            existing = self._validate_event(
                self._read_json_object(queue_path),
                expected_session_id=partial["identity"]["session_id"],
                expected_sequence=partial["sequence"],
            )
            if existing is None:
                self._increment_metrics(session_root, "malformed")
                return {
                    "event_id": partial["event_id"],
                    "sequence": partial["sequence"],
                    "malformed": True,
                }
            if existing["content_sha256"] != event["content_sha256"]:
                ledger = self._read_json_object(ledger_path) or {}
                self._record_conflict(
                    session_root,
                    ledger_path,
                    ledger,
                    kind="assistant",
                    observed_hash=assistant_hash,
                )
                return {
                    "event_id": partial["event_id"],
                    "sequence": partial["sequence"],
                    "conflict": True,
                }
        self._fault("after_queue_publish_before_ledger")
        ledger = self._read_json_object(ledger_path)
        if ledger is None:
            self._increment_metrics(session_root, "malformed")
            return {
                "event_id": partial["event_id"],
                "sequence": partial["sequence"],
                "malformed": True,
            }
        self._mark_ledger_queued(ledger_path, ledger, event)
        self._partial_path(
            session_root, partial["sequence"], partial["event_id"]
        ).unlink(missing_ok=True)
        self._orphan_path(session_root, partial["event_id"]).unlink(
            missing_ok=True
        )
        return {
            "event_id": partial["event_id"],
            "sequence": partial["sequence"],
            "paired": True,
            "duplicate": not created,
        }

    @staticmethod
    def _partial(
        sequence: int,
        key: str,
        session_id: str,
        turn_id: str,
        prompt: str,
    ) -> dict[str, Any]:
        return {
            "schema": "context-maintain.partial.v2",
            "sequence": sequence,
            "event_id": key,
            "identity": {"session_id": session_id, "turn_id": turn_id},
            "prompt": prompt,
            "prompt_sha256": _digest(prompt),
            "received_at": _utc_now(),
        }

    def _event(
        self,
        partial: dict[str, Any],
        assistant: str | None,
        assistant_hash: str,
        tool_evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        stable = {
            "workspace_id": self.workspace_id,
            "sequence": partial["sequence"],
            "event_id": partial["event_id"],
            "identity": partial["identity"],
            "prompt": partial["prompt"],
            "assistant": assistant,
            "tool_evidence": tool_evidence,
        }
        return {
            "schema": "context-maintain.response-end.v2",
            **stable,
            "prompt_sha256": partial["prompt_sha256"],
            "assistant_sha256": assistant_hash,
            "content_sha256": _digest(stable),
            "captured_at": _utc_now(),
        }

    def _validate_partial(
        self,
        value: dict[str, Any] | None,
        *,
        expected_session_id: str | None,
    ) -> dict[str, Any] | None:
        if not isinstance(value, dict):
            return None
        sequence = self._positive_int(value.get("sequence"))
        identity = value.get("identity")
        if (
            value.get("schema") != "context-maintain.partial.v2"
            or sequence is None
            or not isinstance(identity, dict)
            or not isinstance(identity.get("session_id"), str)
            or not identity["session_id"]
            or not isinstance(identity.get("turn_id"), str)
            or not identity["turn_id"]
            or not isinstance(value.get("prompt"), str)
            or not isinstance(value.get("received_at"), str)
        ):
            return None
        if (
            expected_session_id is not None
            and identity["session_id"] != expected_session_id
        ):
            return None
        if value.get("event_id") != _event_key(
            identity["session_id"], identity["turn_id"]
        ):
            return None
        if value.get("prompt_sha256") != _digest(value["prompt"]):
            return None
        return value

    def _validate_orphan(
        self,
        value: dict[str, Any] | None,
        *,
        expected_session_id: str | None,
    ) -> dict[str, Any] | None:
        if not isinstance(value, dict):
            return None
        identity = value.get("identity")
        assistant = value.get("assistant")
        if (
            value.get("schema") != "context-maintain.stop-orphan.v2"
            or not isinstance(identity, dict)
            or not isinstance(identity.get("session_id"), str)
            or not isinstance(identity.get("turn_id"), str)
            or (assistant is not None and not isinstance(assistant, str))
            or not isinstance(value.get("received_at"), str)
        ):
            return None
        if (
            expected_session_id is not None
            and identity["session_id"] != expected_session_id
        ):
            return None
        if value.get("event_id") != _event_key(
            identity["session_id"], identity["turn_id"]
        ):
            return None
        if value.get("assistant_sha256") != _digest(assistant):
            return None
        return value

    def _validate_event(
        self,
        value: dict[str, Any] | None,
        *,
        expected_session_id: str | None = None,
        expected_sequence: int | None = None,
    ) -> dict[str, Any] | None:
        if not isinstance(value, dict):
            return None
        sequence = self._positive_int(value.get("sequence"))
        identity = value.get("identity")
        assistant = value.get("assistant")
        tool_evidence = value.get("tool_evidence", [])
        if (
            value.get("schema") != "context-maintain.response-end.v2"
            or value.get("workspace_id") != self.workspace_id
            or sequence is None
            or not isinstance(identity, dict)
            or not isinstance(identity.get("session_id"), str)
            or not identity["session_id"]
            or not isinstance(identity.get("turn_id"), str)
            or not identity["turn_id"]
            or not isinstance(value.get("prompt"), str)
            or (assistant is not None and not isinstance(assistant, str))
            or not self._valid_event_tool_evidence(tool_evidence, identity)
            or not isinstance(value.get("captured_at"), str)
        ):
            return None
        if expected_sequence is not None and sequence != expected_sequence:
            return None
        if (
            expected_session_id is not None
            and identity["session_id"] != expected_session_id
        ):
            return None
        key = _event_key(identity["session_id"], identity["turn_id"])
        if value.get("event_id") != key:
            return None
        prompt_hash = _digest(value["prompt"])
        assistant_hash = _digest(assistant)
        if (
            value.get("prompt_sha256") != prompt_hash
            or value.get("assistant_sha256") != assistant_hash
        ):
            return None
        stable = {
            "workspace_id": self.workspace_id,
            "sequence": sequence,
            "event_id": key,
            "identity": identity,
            "prompt": value["prompt"],
            "assistant": assistant,
        }
        if "tool_evidence" in value:
            stable["tool_evidence"] = tool_evidence
        if value.get("content_sha256") != _digest(stable):
            return None
        value["tool_evidence"] = tool_evidence
        return value

    def _validate_tool_evidence(
        self,
        value: dict[str, Any] | None,
        *,
        expected_session_id: str | None,
        expected_turn_id: str | None,
    ) -> dict[str, Any] | None:
        if not isinstance(value, dict):
            return None
        identity = value.get("identity")
        tool_name = value.get("tool_name")
        tool_use_id = value.get("tool_use_id")
        facts = value.get("facts")
        conflict = value.get("conflict")
        if (
            value.get("schema") != "context-maintain.tool-evidence.v1"
            or not isinstance(identity, dict)
            or not isinstance(identity.get("session_id"), str)
            or not identity["session_id"]
            or not isinstance(identity.get("turn_id"), str)
            or not identity["turn_id"]
            or not isinstance(tool_name, str)
            or _TOOL_NAME.fullmatch(tool_name) is None
            or not isinstance(tool_use_id, str)
            or _TOOL_ID.fullmatch(tool_use_id) is None
            or not _is_sha256(value.get("input_sha256"))
            or not _is_sha256(value.get("response_sha256"))
            or not _valid_tool_facts(facts)
            or not isinstance(value.get("captured_at"), str)
            or (
                conflict is not None
                and (
                    not isinstance(conflict, dict)
                    or not _is_sha256(conflict.get("observed_sha256"))
                    or not isinstance(conflict.get("detected_at"), str)
                )
            )
        ):
            return None
        if (
            expected_session_id is not None
            and identity["session_id"] != expected_session_id
        ):
            return None
        if (
            expected_turn_id is not None
            and identity["turn_id"] != expected_turn_id
        ):
            return None
        event_id = _event_key(identity["session_id"], identity["turn_id"])
        if value.get("event_id") != event_id:
            return None
        stable = {
            "event_id": event_id,
            "identity": identity,
            "tool_name": tool_name,
            "tool_use_id": tool_use_id,
            "input_sha256": value["input_sha256"],
            "response_sha256": value["response_sha256"],
            "facts": facts,
        }
        if value.get("evidence_sha256") != _digest(stable):
            return None
        return value

    @staticmethod
    def _valid_event_tool_evidence(
        value: object, identity: Mapping[str, Any]
    ) -> bool:
        if not isinstance(value, list) or len(value) > 128:
            return False
        event_id = _event_key(identity["session_id"], identity["turn_id"])
        seen: set[str] = set()
        for item in value:
            if not isinstance(item, dict) or set(item) != {
                "tool_name",
                "tool_use_id",
                "input_sha256",
                "response_sha256",
                "evidence_sha256",
                "facts",
            }:
                return False
            name = item.get("tool_name")
            use_id = item.get("tool_use_id")
            if (
                not isinstance(name, str)
                or _TOOL_NAME.fullmatch(name) is None
                or not isinstance(use_id, str)
                or _TOOL_ID.fullmatch(use_id) is None
                or use_id in seen
                or not _is_sha256(item.get("input_sha256"))
                or not _is_sha256(item.get("response_sha256"))
                or not _is_sha256(item.get("evidence_sha256"))
                or not _valid_tool_facts(item.get("facts"))
            ):
                return False
            stable = {
                "event_id": event_id,
                "identity": identity,
                "tool_name": name,
                "tool_use_id": use_id,
                "input_sha256": item["input_sha256"],
                "response_sha256": item["response_sha256"],
                "facts": item["facts"],
            }
            if item["evidence_sha256"] != _digest(stable):
                return False
            seen.add(use_id)
        return True

    def _collect_tool_evidence(
        self,
        session_root: Path,
        *,
        session_id: str,
        turn_id: str,
    ) -> tuple[list[dict[str, Any]], int, int]:
        key = _event_key(session_id, turn_id)
        turn_root = self._tool_evidence_turn_root(session_root, key)
        if turn_root.is_symlink():
            return [], 1, 0
        if not turn_root.exists():
            return [], 0, 0
        if not turn_root.is_dir():
            return [], 1, 0
        evidence: list[dict[str, Any]] = []
        malformed = conflicts = 0
        for path in sorted(turn_root.iterdir()):
            if path.is_symlink() or not path.is_file() or path.suffix != ".json":
                malformed += 1
                continue
            record = self._validate_tool_evidence(
                self._read_json_object(path),
                expected_session_id=session_id,
                expected_turn_id=turn_id,
            )
            if record is None:
                malformed += 1
                continue
            conflicts += record.get("conflict") is not None
            evidence.append(
                {
                    "tool_name": record["tool_name"],
                    "tool_use_id": record["tool_use_id"],
                    "input_sha256": record["input_sha256"],
                    "response_sha256": record["response_sha256"],
                    "evidence_sha256": record["evidence_sha256"],
                    "facts": record["facts"],
                }
            )
        evidence.sort(key=lambda item: (item["tool_name"], item["tool_use_id"]))
        if len(evidence) > 128:
            malformed += len(evidence) - 128
            evidence = evidence[:128]
        return evidence, malformed, conflicts

    def _mark_ledger_queued(
        self,
        path: Path,
        ledger: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        ledger.update(
            {
                "schema": "context-maintain.digest-ledger.v2",
                "event_id": event["event_id"],
                "sequence": event["sequence"],
                "status": "queued",
                "prompt_sha256": event["prompt_sha256"],
                "assistant_sha256": event["assistant_sha256"],
                "content_sha256": event["content_sha256"],
                "tool_evidence_sha256": _digest(event["tool_evidence"]),
                "tool_evidence_count": len(event["tool_evidence"]),
                "tool_evidence_digests": {
                    _opaque_key(item["tool_use_id"]): item["evidence_sha256"]
                    for item in event["tool_evidence"]
                },
                "updated_at": _utc_now(),
            }
        )
        self._atomic_write(path, ledger)

    def _complete_event(
        self,
        session_root: Path,
        event: dict[str, Any],
        outcome: str,
        queue_path: Path,
    ) -> None:
        ledger_path = self._ledger_path(session_root, event["event_id"])
        ledger = self._read_json_object(ledger_path) or {}
        ledger.update(
            {
                "schema": "context-maintain.digest-ledger.v2",
                "event_id": event["event_id"],
                "sequence": event["sequence"],
                "status": "completed",
                "prompt_sha256": event["prompt_sha256"],
                "assistant_sha256": event["assistant_sha256"],
                "content_sha256": event["content_sha256"],
                "tool_evidence_sha256": _digest(event["tool_evidence"]),
                "tool_evidence_count": len(event["tool_evidence"]),
                "tool_evidence_digests": {
                    _opaque_key(item["tool_use_id"]): item["evidence_sha256"]
                    for item in event["tool_evidence"]
                },
                "outcome": outcome,
                "completed_at": _utc_now(),
                "updated_at": _utc_now(),
            }
        )
        # The digest ledger is durable before raw conversation removal.
        self._atomic_write(ledger_path, ledger)
        self._fault("after_completed_ledger_before_raw_cleanup")
        self._cleanup_tool_evidence(
            session_root,
            event["identity"]["session_id"],
            event["identity"]["turn_id"],
        )
        self._durable_unlink(queue_path)

    def _reconcile_completed(
        self, session_root: Path, checkpoint: dict[str, Any]
    ) -> None:
        cursor = checkpoint["last_processed_sequence"]
        for queue_path in sorted((session_root / "queue").glob("*.json")):
            event = self._validate_event(self._read_json_object(queue_path))
            if event is None or event["sequence"] > cursor:
                continue
            problem = self._queue_ledger_problem(
                session_root,
                queue_path,
                event,
                allowed_statuses=frozenset({"queued", "completed"}),
            )
            if problem is not None:
                continue
            ledger = self._read_json_object(
                self._ledger_path(session_root, event["event_id"])
            )
            outcome = (
                ledger.get("outcome")
                if isinstance(ledger, dict)
                and ledger.get("status") == "completed"
                else (
                    checkpoint.get("last_outcome")
                    if event["sequence"] == cursor
                    else "processed"
                )
            )
            self._complete_event(session_root, event, str(outcome), queue_path)

    def _reconcile_checkpoint_covered_residue(
        self,
        session_root: Path,
        checkpoint: dict[str, Any],
    ) -> None:
        """Idempotently sweep only exact raw already covered by checkpoint."""
        self._reconcile_completed(session_root, checkpoint)
        cursor = checkpoint["last_processed_sequence"]
        for path in (session_root / "ledger").glob("*.json"):
            ledger = self._read_json_object(path)
            if (
                not self._valid_gap_repair_ledger(ledger)
                or int(ledger["sequence"]) > cursor
            ):
                continue
            found, _session_id, valid = self._repair_residue_identity(
                session_root,
                ledger,
            )
            if found and valid:
                self._cleanup_repaired_gap(session_root, ledger)

    def _load_checkpoint(
        self,
        session_root: Path,
        *,
        reconcile_repairs: bool = True,
    ) -> tuple[dict[str, Any], bool]:
        path = session_root / "checkpoint.json"
        if not path.exists():
            value = self._checkpoint_default()
            if reconcile_repairs:
                value = self._reconcile_approved_gap_repairs(
                    session_root, value
                )
            return value, self._checkpoint_consistent(session_root, value)
        value = self._read_json_object(path)
        if not isinstance(value, dict):
            return self._checkpoint_default(), False
        last = self._nonnegative_int(value.get("last_processed_sequence"))
        reports = value.get("pending_reports")
        failure = value.get("failure")
        last_event = value.get("last_processed_event")
        last_content_hash = value.get("last_processed_content_sha256")
        last_processed_at = value.get("last_processed_at")
        last_outcome = value.get("last_outcome")
        if (
            value.get("schema") != "context-maintain.checkpoint.v2"
            or last is None
            or not isinstance(reports, list)
            or any(not self._valid_pending_report(item) for item in reports)
            or (failure is not None and not isinstance(failure, dict))
        ):
            return self._checkpoint_default(), False
        if last == 0:
            if any(
                item is not None
                for item in (
                    last_event,
                    last_content_hash,
                    last_processed_at,
                    last_outcome,
                )
            ):
                return self._checkpoint_default(), False
        elif (
            not isinstance(last_event, str)
            or not last_event
            or not isinstance(last_content_hash, str)
            or len(last_content_hash) != 64
            or not isinstance(last_processed_at, str)
            or not last_processed_at
            or last_outcome not in CHECKPOINT_OUTCOMES
        ):
            return self._checkpoint_default(), False
        if isinstance(failure, dict) and (
            not isinstance(failure.get("code"), str)
            or not failure["code"]
            or self._positive_int(failure.get("sequence")) is None
            or self._positive_int(failure.get("attempts")) is None
            or not isinstance(failure.get("last_failed_at"), str)
        ):
            return self._checkpoint_default(), False
        if any(
            self._positive_int(item.get("sequence")) is None
            or item["sequence"] > last
            for item in reports
        ):
            return self._checkpoint_default(), False
        if len({item["report_id"] for item in reports}) != len(reports):
            return self._checkpoint_default(), False
        if reconcile_repairs:
            value = self._reconcile_approved_gap_repairs(session_root, value)
        return value, self._checkpoint_consistent(session_root, value)

    def _valid_pending_report(self, value: object) -> bool:
        if not isinstance(value, dict):
            return False
        report_id = value.get("report_id")
        event_id = value.get("event_id")
        delivered_to = value.get("delivered_to")
        return (
            isinstance(report_id, str)
            and re.fullmatch(r"[0-9a-f]{32}", report_id) is not None
            and value.get("kind") in {"updated_report", "needs_decision"}
            and isinstance(event_id, str)
            and re.fullmatch(r"[0-9a-f]{32}", event_id) is not None
            and self._positive_int(value.get("sequence")) is not None
            and isinstance(value.get("created_at"), str)
            and bool(value["created_at"])
            and isinstance(delivered_to, list)
            and len(delivered_to) <= MAX_REPORT_RECIPIENTS
            and all(
                isinstance(recipient, str)
                and re.fullmatch(r"[0-9a-f]{32}", recipient) is not None
                for recipient in delivered_to
            )
            and len(set(delivered_to)) == len(delivered_to)
        )

    def _checkpoint_consistent(
        self, session_root: Path, checkpoint: dict[str, Any]
    ) -> bool:
        """Reject a typed but impossible cursor instead of claiming freshness."""
        cursor = checkpoint["last_processed_sequence"]
        ledgers_by_sequence: dict[int, dict[str, Any]] = {}
        for path in (session_root / "ledger").glob("*.json"):
            ledger = self._read_json_object(path)
            if not isinstance(ledger, dict):
                continue
            sequence = self._positive_int(ledger.get("sequence"))
            if sequence is None:
                continue
            if sequence in ledgers_by_sequence:
                return False
            ledgers_by_sequence[sequence] = ledger

        if any(
            sequence > cursor
            and ledger.get("status") in {"completed", "abandoned"}
            for sequence, ledger in ledgers_by_sequence.items()
        ):
            return False
        if cursor == 0:
            return not any(
                ledger.get("status") in {"completed", "abandoned"}
                for ledger in ledgers_by_sequence.values()
            )

        for sequence in range(1, cursor + 1):
            ledger = ledgers_by_sequence.get(sequence)
            if ledger is None:
                return False
            if ledger.get("status") in {"completed", "abandoned"}:
                if (
                    ledger.get("status") == "abandoned"
                    and not self._valid_gap_repair_ledger(ledger)
                ):
                    return False
                continue
            # The only accepted incomplete digest ledger is the latest event
            # immediately after the checkpoint commit and before raw cleanup.
            if sequence != cursor or ledger.get("status") != "queued":
                return False
            queue_path = self._queue_path(
                session_root, sequence, str(ledger.get("event_id"))
            )
            event = self._validate_event(
                self._read_json_object(queue_path), expected_sequence=sequence
            )
            if event is None:
                return False
            if event["content_sha256"] != checkpoint[
                "last_processed_content_sha256"
            ]:
                return False

        latest = ledgers_by_sequence[cursor]
        return (
            latest.get("event_id") == checkpoint["last_processed_event"]
            and latest.get("content_sha256")
            == checkpoint["last_processed_content_sha256"]
        )

    @staticmethod
    def _checkpoint_default() -> dict[str, Any]:
        return {
            "schema": "context-maintain.checkpoint.v2",
            "last_processed_sequence": 0,
            "last_processed_event": None,
            "last_processed_content_sha256": None,
            "last_processed_at": None,
            "last_outcome": None,
            "failure": None,
            "pending_reports": [],
        }

    @staticmethod
    def _agent_state_default() -> dict[str, Any]:
        return {
            "schema": "context-maintain.agent-state.v2",
            "thread_id": None,
            "grounded": False,
            "workspace_bound": False,
            "summary": "",
            "updated_at": None,
        }

    @staticmethod
    def _valid_agent_state(value: object) -> bool:
        if not isinstance(value, dict):
            return False
        if set(value) != {
            "schema",
            "thread_id",
            "grounded",
            "workspace_bound",
            "summary",
            "updated_at",
        }:
            return False
        thread_id = value.get("thread_id")
        updated_at = value.get("updated_at")
        return (
            value.get("schema") == "context-maintain.agent-state.v2"
            and (
                thread_id is None
                or (isinstance(thread_id, str) and bool(thread_id.strip()))
            )
            and isinstance(value.get("grounded"), bool)
            and isinstance(value.get("workspace_bound"), bool)
            and isinstance(value.get("summary"), str)
            and (
                updated_at is None
                or (isinstance(updated_at, str) and bool(updated_at))
            )
        )

    @staticmethod
    def _failure_attempts(checkpoint: dict[str, Any], sequence: int) -> int:
        failure = checkpoint.get("failure")
        if (
            isinstance(failure, dict)
            and failure.get("sequence") == sequence
            and isinstance(failure.get("attempts"), int)
            and not isinstance(failure.get("attempts"), bool)
        ):
            return max(0, failure["attempts"])
        return 0

    def _normalize_processor_result(
        self, result: object
    ) -> tuple[str, object | None]:
        report: object | None = None
        if isinstance(result, str):
            outcome = result
        elif isinstance(result, Mapping):
            outcome = result.get("outcome")
            report = result.get("report", result)
        else:
            outcome = getattr(result, "outcome", None)
            to_dict = getattr(result, "to_dict", None)
            if callable(to_dict):
                report = to_dict()
        if not isinstance(outcome, str) or outcome not in COMMITTABLE_OUTCOMES:
            raise RuntimeProtocolError("processor returned a non-committable outcome")
        if report is not None:
            try:
                json.dumps(report, ensure_ascii=False)
            except (TypeError, ValueError) as error:
                raise RuntimeProtocolError(
                    "processor report must be JSON serializable"
                ) from error
        return outcome, report

    def _record_conflict(
        self,
        session_root: Path,
        ledger_path: Path,
        ledger: dict[str, Any],
        *,
        kind: str,
        observed_hash: str,
    ) -> None:
        ledger["conflict"] = {
            "kind": kind,
            "observed_sha256": observed_hash,
            "detected_at": _utc_now(),
        }
        ledger["updated_at"] = _utc_now()
        self._atomic_write(ledger_path, ledger)
        self._increment_metrics(session_root, "conflicts")

    def _queue_summary(self, session_root: Path) -> tuple[int, int, int]:
        count = malformed = maximum = 0
        for path in (session_root / "queue").glob("*.json"):
            count += 1
            event = self._validate_event(self._read_json_object(path))
            if event is None:
                malformed += 1
            else:
                maximum = max(maximum, event["sequence"])
        return count, malformed, maximum

    def _work_generation_locked(self, session_root: Path) -> str:
        """Project durable queue state to a raw-free wake-up generation."""
        identities: list[dict[str, object]] = []
        for path in sorted((session_root / "queue").glob("*.json")):
            event = self._validate_event(self._read_json_object(path))
            if event is None:
                identities.append({"name": path.name, "malformed": True})
                continue
            identities.append(
                {
                    "name": path.name,
                    "sequence": event["sequence"],
                    "event_id": event["event_id"],
                    "content_sha256": event["content_sha256"],
                }
            )
        return _digest(
            {
                "schema": "context-maintain.work-generation.v1",
                "queue": identities,
            }
        )

    def _queue_ledger_problem(
        self,
        session_root: Path,
        queue_path: Path,
        event: Mapping[str, Any],
        *,
        allowed_statuses: frozenset[str] = frozenset({"queued"}),
    ) -> str | None:
        """Return why one queued event lacks exact conflict-free provenance."""
        canonical_queue_path = self._queue_path(
            session_root,
            int(event["sequence"]),
            str(event["event_id"]),
        )
        if (
            queue_path != canonical_queue_path
            or queue_path.is_symlink()
            or not queue_path.is_file()
        ):
            return "malformed_queue_ledger"

        ledger_path = self._ledger_path(
            session_root,
            str(event["event_id"]),
        )
        if ledger_path.is_symlink() or not ledger_path.is_file():
            return "malformed_queue_ledger"
        ledger = self._read_json_object(ledger_path)
        if not isinstance(ledger, dict):
            return "malformed_queue_ledger"
        if ledger.get("conflict") is not None:
            return "ledger_conflict"

        tool_evidence = event["tool_evidence"]
        expected_tool_digests = {
            _opaque_key(str(item["tool_use_id"])): item["evidence_sha256"]
            for item in tool_evidence
        }
        exact = (
            ledger.get("schema") == "context-maintain.digest-ledger.v2"
            and ledger.get("status") in allowed_statuses
            and ledger.get("event_id") == event["event_id"]
            and ledger.get("sequence") == event["sequence"]
            and ledger.get("prompt_sha256") == event["prompt_sha256"]
            and ledger.get("assistant_sha256")
            == event["assistant_sha256"]
            and ledger.get("content_sha256") == event["content_sha256"]
            and ledger.get("tool_evidence_sha256")
            == _digest(tool_evidence)
            and ledger.get("tool_evidence_count") == len(tool_evidence)
            and ledger.get("tool_evidence_digests")
            == expected_tool_digests
        )
        return None if exact else "malformed_queue_ledger"

    def _session_identity_matches_root(
        self,
        session_root: Path,
        session_id: str,
    ) -> bool:
        metadata = self._read_json_object(session_root / "session.json")
        return (
            self._valid_session_metadata(
                metadata,
                expected_session_hash=_digest(session_id),
            )
            and _opaque_key(session_id) == session_root.name
        )

    def _repair_residue_identity(
        self,
        session_root: Path,
        ledger: Mapping[str, Any],
    ) -> tuple[bool, str | None, bool]:
        """Return presence, raw session id, and validity for repair residue."""
        sequence = int(ledger["sequence"])
        event_id = str(ledger["event_id"])
        partial_path = self._partial_path(session_root, sequence, event_id)
        orphan_path = self._orphan_path(session_root, event_id)
        evidence_root = self._tool_evidence_turn_root(
            session_root,
            event_id,
        )
        residue_found = any(
            path.exists() or path.is_symlink()
            for path in (partial_path, orphan_path, evidence_root)
        )
        if not residue_found:
            return False, None, True

        session_ids: set[str] = set()
        malformed = False
        if partial_path.exists() or partial_path.is_symlink():
            partial = (
                None
                if partial_path.is_symlink()
                else self._validate_partial(
                    self._read_json_object(partial_path),
                    expected_session_id=None,
                )
            )
            if (
                partial is None
                or partial.get("sequence") != sequence
                or partial.get("event_id") != event_id
                or partial.get("prompt_sha256")
                != ledger.get("prompt_sha256")
            ):
                malformed = True
            else:
                session_ids.add(partial["identity"]["session_id"])

        if orphan_path.exists() or orphan_path.is_symlink():
            orphan = (
                None
                if orphan_path.is_symlink()
                else self._validate_orphan(
                    self._read_json_object(orphan_path),
                    expected_session_id=None,
                )
            )
            if (
                orphan is None
                or orphan.get("event_id") != event_id
                or orphan.get("conflict") is not None
            ):
                malformed = True
            else:
                session_ids.add(orphan["identity"]["session_id"])

        if evidence_root.exists() or evidence_root.is_symlink():
            if evidence_root.is_symlink() or not evidence_root.is_dir():
                malformed = True
            else:
                for path in evidence_root.iterdir():
                    evidence = (
                        None
                        if path.is_symlink() or not path.is_file()
                        else self._validate_tool_evidence(
                            self._read_json_object(path),
                            expected_session_id=None,
                            expected_turn_id=None,
                        )
                    )
                    if (
                        evidence is None
                        or evidence.get("event_id") != event_id
                        or evidence.get("conflict") is not None
                    ):
                        malformed = True
                        continue
                    session_ids.add(evidence["identity"]["session_id"])

        if malformed or len(session_ids) != 1:
            return True, None, False
        session_id = next(iter(session_ids))
        if not self._session_identity_matches_root(session_root, session_id):
            return True, None, False
        return True, session_id, True

    def _checkpoint_cleanup_residue_details(
        self,
        session_root: Path,
        checkpoint: Mapping[str, Any],
    ) -> tuple[int, int, set[str]]:
        """Describe exact raw residue already covered by the checkpoint."""
        cursor = int(checkpoint["last_processed_sequence"])
        count = malformed = 0
        session_ids: set[str] = set()

        for queue_path in sorted((session_root / "queue").glob("*.json")):
            event = self._validate_event(self._read_json_object(queue_path))
            if event is None or int(event["sequence"]) > cursor:
                continue
            problem = self._queue_ledger_problem(
                session_root,
                queue_path,
                event,
                allowed_statuses=frozenset({"queued", "completed"}),
            )
            if problem == "ledger_conflict":
                continue
            if problem is not None or not self._session_identity_matches_root(
                session_root,
                event["identity"]["session_id"],
            ):
                malformed += 1
                continue
            count += 1
            session_ids.add(event["identity"]["session_id"])

        for path in (session_root / "ledger").glob("*.json"):
            ledger = self._read_json_object(path)
            if (
                not self._valid_gap_repair_ledger(ledger)
                or int(ledger["sequence"]) > cursor
            ):
                continue
            found, session_id, valid = self._repair_residue_identity(
                session_root,
                ledger,
            )
            if not found:
                continue
            if not valid or session_id is None:
                malformed += 1
                continue
            count += 1
            session_ids.add(session_id)

        return count, malformed, session_ids

    def _ledger_summary(
        self, session_root: Path
    ) -> tuple[int, int, int, int]:
        waiting = conflicts = malformed = maximum = 0
        for path in (session_root / "ledger").glob("*.json"):
            value = self._read_json_object(path)
            if not isinstance(value, dict):
                malformed += 1
                continue
            sequence = self._positive_int(value.get("sequence"))
            evidence_digests = value.get("tool_evidence_digests")
            if (
                value.get("schema") != "context-maintain.digest-ledger.v2"
                or sequence is None
                or not isinstance(value.get("event_id"), str)
                or not isinstance(value.get("prompt_sha256"), str)
                or (
                    evidence_digests is not None
                    and not _valid_evidence_digest_map(evidence_digests)
                )
            ):
                malformed += 1
                continue
            maximum = max(maximum, sequence)
            waiting += value.get("status") == "waiting_stop"
            conflicts += value.get("conflict") is not None
            if value.get("status") == "queued":
                queue_path = self._queue_path(
                    session_root,
                    sequence,
                    str(value.get("event_id")),
                )
                event = self._validate_event(
                    self._read_json_object(queue_path),
                    expected_sequence=sequence,
                )
                if event is None:
                    malformed += 1
                else:
                    problem = self._queue_ledger_problem(
                        session_root,
                        queue_path,
                        event,
                    )
                    if problem == "malformed_queue_ledger":
                        malformed += 1
            if value.get("status") == "abandoned" and not self._valid_gap_repair_ledger(
                value
            ):
                malformed += 1
        return waiting, conflicts, malformed, maximum

    def _gap_repair_for_sequence(
        self, session_root: Path, sequence: int
    ) -> dict[str, Any] | None:
        matches: list[dict[str, Any]] = []
        for path in (session_root / "ledger").glob("*.json"):
            value = self._read_json_object(path)
            if (
                isinstance(value, dict)
                and value.get("status") == "abandoned"
                and self._positive_int(value.get("sequence")) == sequence
                and self._valid_gap_repair_ledger(value)
            ):
                matches.append(value)
        return matches[0] if len(matches) == 1 else None

    def _valid_gap_repair_ledger(self, ledger: object) -> bool:
        if not isinstance(ledger, dict):
            return False
        repair = ledger.get("repair")
        if not isinstance(repair, dict) or set(repair) != {
            "schema",
            "action",
            "sequence",
            "event_id",
            "prompt_sha256",
            "approved_by",
            "reason",
            "repair_sha256",
            "approved_at",
        }:
            return False
        stable = {
            key: repair[key]
            for key in (
                "schema",
                "action",
                "sequence",
                "event_id",
                "prompt_sha256",
                "approved_by",
                "reason",
            )
        }
        return (
            ledger.get("schema") == "context-maintain.digest-ledger.v2"
            and ledger.get("status") == "abandoned"
            and ledger.get("outcome") == "gap_abandoned"
            and ledger.get("assistant_sha256") is None
            and self._positive_int(ledger.get("sequence"))
            == self._positive_int(repair.get("sequence"))
            and ledger.get("event_id") == repair.get("event_id")
            and ledger.get("prompt_sha256") == repair.get("prompt_sha256")
            and ledger.get("content_sha256") == repair.get("repair_sha256")
            and repair.get("schema") == "context-maintain.gap-repair.v1"
            and repair.get("action") == "abandon_missing_stop"
            and isinstance(repair.get("event_id"), str)
            and bool(repair["event_id"])
            and _is_sha256(repair.get("prompt_sha256"))
            and isinstance(repair.get("approved_by"), str)
            and _PROVENANCE_CODE.fullmatch(repair["approved_by"]) is not None
            and isinstance(repair.get("reason"), str)
            and _PROVENANCE_CODE.fullmatch(repair["reason"]) is not None
            and isinstance(repair.get("approved_at"), str)
            and bool(repair["approved_at"])
            and _is_sha256(repair.get("repair_sha256"))
            and repair["repair_sha256"] == _digest(stable)
        )

    def _apply_gap_repair_to_checkpoint(
        self,
        session_root: Path,
        checkpoint: dict[str, Any],
        ledger: dict[str, Any],
    ) -> dict[str, Any]:
        sequence = int(ledger["sequence"])
        if checkpoint["last_processed_sequence"] >= sequence:
            return checkpoint
        if checkpoint["last_processed_sequence"] + 1 != sequence:
            raise RuntimeProtocolError(
                "approved gap repair is not the next checkpoint sequence"
            )
        repair = ledger["repair"]
        checkpoint.update(
            {
                "last_processed_sequence": sequence,
                "last_processed_event": ledger["event_id"],
                "last_processed_content_sha256": ledger["content_sha256"],
                "last_processed_at": repair["approved_at"],
                "last_outcome": "gap_abandoned",
                "failure": None,
            }
        )
        self._atomic_write(session_root / "checkpoint.json", checkpoint)
        return checkpoint

    def _reconcile_approved_gap_repairs(
        self, session_root: Path, checkpoint: dict[str, Any]
    ) -> dict[str, Any]:
        """Finish only repairs whose explicit approval ledger is durable."""
        while True:
            sequence = checkpoint["last_processed_sequence"] + 1
            ledger = self._gap_repair_for_sequence(session_root, sequence)
            if ledger is None:
                return checkpoint
            checkpoint = self._apply_gap_repair_to_checkpoint(
                session_root, checkpoint, ledger
            )
            self._cleanup_repaired_gap(session_root, ledger)

    def _cleanup_repaired_gap(
        self, session_root: Path, ledger: dict[str, Any]
    ) -> None:
        sequence = int(ledger["sequence"])
        event_id = str(ledger["event_id"])
        partial_path = self._partial_path(session_root, sequence, event_id)
        self._cleanup_tool_evidence_by_key(session_root, event_id)
        self._durable_unlink(partial_path)
        self._durable_unlink(self._orphan_path(session_root, event_id))

    def _gap_repair_summary(self, session_root: Path) -> dict[str, Any]:
        records: list[dict[str, Any]] = []
        for path in (session_root / "ledger").glob("*.json"):
            ledger = self._read_json_object(path)
            if self._valid_gap_repair_ledger(ledger):
                records.append(ledger)
        records.sort(key=lambda item: int(item["sequence"]))
        latest = records[-1]["repair"] if records else None
        return {
            "count": len(records),
            "latest_sequence": (
                int(records[-1]["sequence"]) if records else None
            ),
            "latest_approved_by": (
                latest["approved_by"] if latest is not None else None
            ),
            "latest_reason": latest["reason"] if latest is not None else None,
        }

    def _missing_stop_gap(
        self,
        session_root: Path,
        *,
        processed_sequence: int,
        assigned_sequence: int,
    ) -> dict[str, Any] | None:
        """Detect a FIFO hole only after a later sequence proves the gap.

        One current prompt waiting for its own Stop is ordinary in-flight
        capture.  It becomes an unrecoverable-by-retry gap only when a higher
        sequence has already been allocated while the next expected ledger is
        still waiting for Stop.
        """
        expected = processed_sequence + 1
        if assigned_sequence <= expected:
            return None
        for path in (session_root / "ledger").glob("*.json"):
            value = self._read_json_object(path)
            if not isinstance(value, dict):
                continue
            if (
                value.get("schema") == "context-maintain.digest-ledger.v2"
                and self._positive_int(value.get("sequence")) == expected
                and value.get("status") == "waiting_stop"
            ):
                return {
                    "code": "missing_stop_gap",
                    "expected_sequence": expected,
                    "higher_sequence": assigned_sequence,
                }
        return None

    def _capture_residue_summary(self, session_root: Path) -> tuple[int, int]:
        orphan_count = malformed = 0
        for path in (session_root / "partials").glob("*.json"):
            if self._validate_partial(
                self._read_json_object(path), expected_session_id=None
            ) is None:
                malformed += 1
        for path in (session_root / "orphans").glob("*.json"):
            orphan_count += 1
            if self._validate_orphan(
                self._read_json_object(path), expected_session_id=None
            ) is None:
                malformed += 1
        return orphan_count, malformed

    def _tool_evidence_summary(
        self, session_root: Path
    ) -> tuple[int, int, int]:
        root = session_root / "tool-evidence"
        if root.is_symlink() or (root.exists() and not root.is_dir()):
            return 0, 0, 1
        if not root.exists():
            return 0, 0, 0
        count = conflicts = malformed = 0
        for turn_root in root.iterdir():
            if turn_root.is_symlink() or not turn_root.is_dir():
                malformed += 1
                continue
            for path in turn_root.iterdir():
                if path.is_symlink() or not path.is_file() or path.suffix != ".json":
                    malformed += 1
                    continue
                record = self._validate_tool_evidence(
                    self._read_json_object(path),
                    expected_session_id=None,
                    expected_turn_id=None,
                )
                if record is None:
                    malformed += 1
                    continue
                count += 1
                conflicts += record.get("conflict") is not None
        return count, conflicts, malformed

    def _cleanup_tool_evidence(
        self, session_root: Path, session_id: str, turn_id: str
    ) -> None:
        self._cleanup_tool_evidence_by_key(
            session_root,
            _event_key(session_id, turn_id),
        )

    def _cleanup_tool_evidence_by_key(
        self,
        session_root: Path,
        event_id: str,
    ) -> None:
        turn_root = self._tool_evidence_turn_root(session_root, event_id)
        if turn_root.is_symlink():
            turn_root.unlink(missing_ok=True)
            return
        if not turn_root.exists():
            return
        if not turn_root.is_dir():
            turn_root.unlink(missing_ok=True)
            return
        for path in turn_root.iterdir():
            if path.is_symlink() or path.is_file():
                path.unlink(missing_ok=True)
        try:
            turn_root.rmdir()
        except OSError:
            # An unexpected nested directory is never traversed or deleted.
            # Status will expose the remaining malformed runtime residue.
            pass

    def _max_assigned_sequence(self, session_root: Path) -> int:
        maximum = 0
        for directory in ("partials", "queue", "ledger"):
            for path in (session_root / directory).glob("*.json"):
                value = self._read_json_object(path)
                if isinstance(value, dict):
                    sequence = self._positive_int(value.get("sequence"))
                    if sequence is not None:
                        maximum = max(maximum, sequence)
        return maximum

    def _load_metrics(self, session_root: Path) -> dict[str, int]:
        value = self._read_json_object(session_root / "metrics.json")
        if not isinstance(value, dict) or value.get("schema") != "context-maintain.metrics.v2":
            return {name: 0 for name in self._METRIC_NAMES}
        counts = value.get("counts")
        if not isinstance(counts, dict):
            return {name: 0 for name in self._METRIC_NAMES}
        result: dict[str, int] = {}
        for name in self._METRIC_NAMES:
            candidate = self._nonnegative_int(counts.get(name))
            result[name] = candidate if candidate is not None else 0
        return result

    def _increment_metrics(self, session_root: Path, name: str) -> None:
        if name not in self._METRIC_NAMES:
            return
        counts = self._load_metrics(session_root)
        counts[name] += 1
        self._atomic_write(
            session_root / "metrics.json",
            {"schema": "context-maintain.metrics.v2", "counts": counts},
        )

    @staticmethod
    def _read_json_object(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    @staticmethod
    def _atomic_write(path: Path, value: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.parent / (
            f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
        )
        encoded = _canonical_bytes(value) + b"\n"
        try:
            with temporary.open("xb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            _fsync_directory(path.parent)
        finally:
            if temporary.exists() or temporary.is_symlink():
                temporary.unlink(missing_ok=True)
                _fsync_directory(path.parent)

    @staticmethod
    def _publish_immutable(path: Path, value: Mapping[str, Any]) -> bool:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.parent / (
            f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
        )
        encoded = _canonical_bytes(value) + b"\n"
        try:
            with temporary.open("xb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(temporary, path)
            except FileExistsError:
                return False
            _fsync_directory(path.parent)
            return True
        finally:
            if temporary.exists() or temporary.is_symlink():
                temporary.unlink(missing_ok=True)
                _fsync_directory(path.parent)

    @staticmethod
    def _durable_unlink(path: Path) -> None:
        if not path.exists() and not path.is_symlink():
            return
        path.unlink(missing_ok=True)
        _fsync_directory(path.parent)

    def _fault(self, point: str) -> None:
        if self._fault_injector is not None:
            self._fault_injector(point)

    @staticmethod
    def _positive_int(value: object) -> int | None:
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            return value
        return None

    @staticmethod
    def _nonnegative_int(value: object) -> int | None:
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            return value
        return None

    @staticmethod
    def _raw_name(sequence: int, key: str) -> str:
        return f"{sequence:020d}-{key}.json"

    def _partial_path(self, session_root: Path, sequence: int, key: str) -> Path:
        return session_root / "partials" / self._raw_name(sequence, key)

    @staticmethod
    def _orphan_path(session_root: Path, key: str) -> Path:
        return session_root / "orphans" / f"{key}.json"

    def _queue_path(self, session_root: Path, sequence: int, key: str) -> Path:
        return session_root / "queue" / self._raw_name(sequence, key)

    @staticmethod
    def _ledger_path(session_root: Path, key: str) -> Path:
        return session_root / "ledger" / f"{key}.json"

    @staticmethod
    def _tool_evidence_turn_root(session_root: Path, key: str) -> Path:
        return session_root / "tool-evidence" / key

    def _tool_evidence_path(
        self, session_root: Path, key: str, tool_use_id: str
    ) -> Path:
        turn_root = self._tool_evidence_turn_root(session_root, key)
        if turn_root.is_symlink():
            raise RuntimeProtocolError(
                "tool evidence turn directory must not be a symlink"
            )
        turn_root.mkdir(parents=True, exist_ok=True)
        return turn_root / f"{_opaque_key(tool_use_id)}.json"


def _sanitize_tool_facts(
    tool_name: str, tool_input: object, tool_response: object
) -> dict[str, Any]:
    """Extract a deliberately small allowlist; everything else stays hashed."""

    facts: dict[str, Any] = {}
    base_name = re.split(r"[.:/]", tool_name.lower())[-1]

    if base_name == "apply_patch":
        patch = _patch_text(tool_input)
        if patch is not None:
            changes: list[dict[str, str]] = []
            seen: set[tuple[str, str]] = set()
            # One MiB and 64 headers bound synchronous capture work and the
            # resulting semantic prompt without retaining patch bodies.
            for match in _PATCH_HEADER.finditer(patch[:1_048_576]):
                path = _safe_path(match.group(2))
                if path is None:
                    continue
                item = (match.group(1).lower(), path)
                if item in seen:
                    continue
                seen.add(item)
                changes.append({"operation": item[0], "path": item[1]})
                if len(changes) == 64:
                    break
            if changes:
                facts["patch_paths"] = changes

    path_values = _explicit_path_values(tool_input)
    if path_values:
        facts["paths"] = path_values

    if base_name in _SHELL_TOOL_NAMES:
        summary = _safe_command_summary(tool_input)
        if summary is not None:
            facts["command"] = summary

    result = _small_result(tool_response)
    if result:
        facts["result"] = result
    return facts


def _patch_text(tool_input: object) -> str | None:
    if isinstance(tool_input, str):
        return tool_input
    if not isinstance(tool_input, Mapping):
        return None
    for key in ("patch", "input", "text", "content"):
        candidate = tool_input.get(key)
        if isinstance(candidate, str):
            return candidate
    return None


def _explicit_path_values(tool_input: object) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    visited = 0

    def visit(value: object, depth: int) -> None:
        nonlocal visited
        if depth > 4 or visited >= 256:
            return
        visited += 1
        if isinstance(value, Mapping):
            for raw_key, candidate in list(value.items())[:64]:
                if not isinstance(raw_key, str):
                    continue
                key = raw_key.strip().lower().replace("-", "_")
                if key in _PATH_FIELDS and isinstance(candidate, str):
                    path = _safe_path(candidate)
                    pair = (key, path) if path is not None else None
                    if pair is not None and pair not in seen:
                        seen.add(pair)
                        found.append({"field": key, "value": path})
                        if len(found) == 64:
                            return
                elif isinstance(candidate, (Mapping, list, tuple)):
                    visit(candidate, depth + 1)
        elif isinstance(value, (list, tuple)):
            for candidate in value[:32]:
                if isinstance(candidate, (Mapping, list, tuple)):
                    visit(candidate, depth + 1)

    visit(tool_input, 0)
    found.sort(key=lambda item: (item["field"], item["value"]))
    return found


def _safe_path(value: str) -> str | None:
    path = value.strip()
    if (
        not path
        or len(path) > 1024
        or any(ord(character) < 32 or ord(character) == 127 for character in path)
    ):
        return None
    normalized = path.replace("\\", "/")
    candidate = PurePosixPath(normalized)
    if (
        normalized.startswith("/")
        or re.match(r"^[A-Za-z]:/", normalized) is not None
        or (bool(candidate.parts) and candidate.parts[0].startswith("~"))
        or (bool(candidate.parts) and candidate.parts[0].endswith(":"))
        or "://" in normalized
    ):
        return None
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    result = candidate.as_posix()
    if result in {"", "."} or result.startswith("../"):
        return None
    return result


def _safe_command_summary(tool_input: object) -> dict[str, str] | None:
    if not isinstance(tool_input, Mapping):
        return None
    command = tool_input.get("cmd", tool_input.get("command"))
    if not isinstance(command, str) or not command or len(command) > 4096:
        return None
    # A fixed classification is emitted, never command arguments. Reject
    # chaining, expansion, assignment, and redirection before tokenization.
    if re.search(r"[;&|<>`$\n\r]", command):
        return None
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None
    if not tokens or len(tokens) > 128 or any("=" in token for token in tokens):
        return None
    executable = Path(tokens[0]).name.lower()

    if executable == "git" and len(tokens) >= 2:
        subcommand = tokens[1].lower()
        if re.fullmatch(r"[a-z][a-z-]{0,31}", subcommand):
            return {"kind": "git", "summary": f"git {subcommand}"}

    summary: str | None = None
    if executable in {"pytest", "py.test", "vitest", "jest", "mocha"}:
        summary = executable
    elif executable in {"python", "python3"} and len(tokens) >= 3:
        if tokens[1:3] == ["-m", "pytest"]:
            summary = "python -m pytest"
        elif tokens[1:3] == ["-m", "unittest"]:
            summary = "python -m unittest"
    elif executable in {"npm", "pnpm", "yarn", "bun"} and len(tokens) >= 2:
        second = tokens[1].lower()
        if second == "test":
            summary = f"{executable} test"
        elif second == "run" and len(tokens) >= 3 and tokens[2].lower().startswith(
            "test"
        ):
            summary = f"{executable} run {tokens[2].lower()[:64]}"
        elif (
            executable == "pnpm"
            and second == "exec"
            and len(tokens) >= 3
            and Path(tokens[2]).name.lower() in {"pytest", "vitest", "jest", "mocha"}
        ):
            summary = f"pnpm exec {Path(tokens[2]).name.lower()}"
    elif executable in {"cargo", "go", "dotnet"} and len(tokens) >= 2:
        if tokens[1].lower() == "test":
            summary = f"{executable} test"
    elif executable in {"make", "mvn", "gradle", "gradlew"} and len(tokens) >= 2:
        if tokens[1].lower() == "test":
            summary = f"{executable} test"

    return {"kind": "test", "summary": summary} if summary else None


def _small_result(tool_response: object) -> dict[str, Any]:
    if not isinstance(tool_response, Mapping):
        return {}
    result: dict[str, Any] = {}
    exit_code = tool_response.get("exit_code")
    if (
        isinstance(exit_code, int)
        and not isinstance(exit_code, bool)
        and -255 <= exit_code <= 255
    ):
        result["exit_code"] = exit_code
    status = tool_response.get("status")
    if isinstance(status, str) and status.strip().lower() in _SAFE_RESULT_STATUS:
        result["status"] = status.strip().lower()
    return result


def _valid_tool_facts(value: object) -> bool:
    if not isinstance(value, dict) or not set(value).issubset(
        {"patch_paths", "paths", "command", "result"}
    ):
        return False
    try:
        if len(_canonical_bytes(value)) > 32768:
            return False
    except (TypeError, ValueError, RecursionError):
        return False
    patch_paths = value.get("patch_paths", [])
    paths = value.get("paths", [])
    command = value.get("command")
    result = value.get("result")
    if not isinstance(patch_paths, list) or len(patch_paths) > 64:
        return False
    if any(
        not isinstance(item, dict)
        or set(item) != {"operation", "path"}
        or item.get("operation") not in {"add", "update", "delete"}
        or not isinstance(item.get("path"), str)
        or _safe_path(item["path"]) != item["path"]
        for item in patch_paths
    ):
        return False
    if not isinstance(paths, list) or len(paths) > 64:
        return False
    if any(
        not isinstance(item, dict)
        or set(item) != {"field", "value"}
        or item.get("field") not in _PATH_FIELDS
        or not isinstance(item.get("value"), str)
        or _safe_path(item["value"]) != item["value"]
        for item in paths
    ):
        return False
    if command is not None and (
        not isinstance(command, dict)
        or set(command) != {"kind", "summary"}
        or command.get("kind") not in {"git", "test"}
        or not isinstance(command.get("summary"), str)
        or not 0 < len(command["summary"]) <= 160
    ):
        return False
    if result is not None:
        if not isinstance(result, dict) or not result or not set(result).issubset(
            {"exit_code", "status"}
        ):
            return False
        exit_code = result.get("exit_code")
        if exit_code is not None and (
            not isinstance(exit_code, int)
            or isinstance(exit_code, bool)
            or not -255 <= exit_code <= 255
        ):
            return False
        status = result.get("status")
        if status is not None and status not in _SAFE_RESULT_STATUS:
            return False
    return True


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _valid_evidence_digest_map(value: object) -> bool:
    return (
        isinstance(value, dict)
        and len(value) <= 128
        and all(
            isinstance(key, str)
            and re.fullmatch(r"[0-9a-f]{32}", key) is not None
            and _is_sha256(digest)
            for key, digest in value.items()
        )
    )


__all__ = [
    "COMMITTABLE_OUTCOMES",
    "MaintainRuntime",
    "PROCESS_LOCK_WAIT_SECONDS",
    "ProcessingDeferredError",
    "RuntimeProtocolError",
    "SESSION_START_SOURCES",
]
