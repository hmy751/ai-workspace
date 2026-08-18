"""Codex command-hook lifecycle adapter for Workspace Maintain.

The adapter owns only removable host/session state.  Workspace meaning stays in
the existing Context owners, semantic judgement stays in the persisted Codex
thread, and all Context writes go through :mod:`operation`.  Its process locks
use POSIX ``fcntl``; portability to a non-POSIX Codex host is deliberately not
claimed by this Reference adapter.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterator

from .operation import apply_maintain_decision, bootstrap_workspace
from ..workspace_contract import (
    HarnessError,
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
    validate_workspace_id,
)


MAINTAIN_HOST_CONFIG_SCHEMA_VERSION = 1
MAINTAIN_HOST_STATE_SCHEMA_VERSION = 1
_CONFIG_KEYS = {"schema_version", "workspace_id"}
_SESSION_KEYS = {
    "schema_version",
    "workspace_id",
    "thread_id",
    "grounded_at",
}
_HEX_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_HOOK_EVENTS = {
    "session-start": "SessionStart",
    "user-prompt": "UserPromptSubmit",
    "response-end": "Stop",
    "session-end": "SessionEnd",
}


def _hash_identifier(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _reject_existing_symlink_components(path: Path, label: str) -> None:
    if not path.is_absolute():
        fail(f"{label} must be an absolute path")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            fail(f"{label} must not use symlink components")


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    _reject_existing_symlink_components(path, "Maintain runtime write path")
    path.parent.mkdir(parents=True, exist_ok=True)
    _reject_existing_symlink_components(path, "Maintain runtime write path")
    descriptor, raw_temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(raw_temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            descriptor = -1
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)
        raise


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    _reject_existing_symlink_components(path, label)
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise HarnessError(f"{label} is not readable UTF-8 JSON: {exc}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        fail(f"{label} must contain a JSON object")
    return value


def _hook_output(
    hook_event_name: str,
    *,
    additional_context: str | None = None,
    system_message: str | None = None,
) -> dict[str, Any]:
    output: dict[str, Any] = {"continue": True}
    if system_message:
        output["systemMessage"] = system_message
    if additional_context:
        output["hookSpecificOutput"] = {
            "hookEventName": hook_event_name,
            "additionalContext": additional_context,
        }
    return output


class MaintainHostAdapter:
    """Bind stable Codex hook fields to one isolated Maintainer session."""

    def __init__(
        self,
        project_root: Path,
        *,
        runtime_root: Path | None = None,
        session_type: type[Any] | None = None,
        runner: Callable[..., Any] = subprocess.run,
        popen: Callable[..., Any] = subprocess.Popen,
        clock: Callable[[], float] = time.time,
        python_executable: str = sys.executable,
        bootstrap: Callable[[Path, Path, str], dict[str, Any]] = (
            bootstrap_workspace
        ),
        apply_decision: Callable[
            [Path, Path, str, Any], dict[str, Any]
        ] = apply_maintain_decision,
    ) -> None:
        lexical_project_root = Path(project_root)
        if not lexical_project_root.is_absolute():
            lexical_project_root = Path.cwd() / lexical_project_root
        try:
            self.project_root = lexical_project_root.resolve(strict=True)
        except OSError as exc:
            raise HarnessError(f"Project root is unavailable: {exc}") from exc
        if not self.project_root.is_dir():
            fail("Project root must be a directory")
        self.work_root = self.project_root / "context" / "work"
        runtime_candidate = (
            Path(runtime_root)
            if runtime_root is not None
            else self.project_root / ".codex" / "maintain-runtime"
        )
        if not runtime_candidate.is_absolute():
            fail("Maintain runtime root must be an absolute path")
        if ".." in runtime_candidate.parts:
            fail("Maintain runtime root must not contain ancestor traversal")
        relative_runtime: Path | None = None
        for project_form in (lexical_project_root, self.project_root):
            try:
                relative_runtime = runtime_candidate.relative_to(project_form)
                break
            except ValueError:
                continue
        if relative_runtime is None:
            fail("Maintain runtime root must be inside the Project root")
        if not relative_runtime.parts:
            fail("Maintain runtime root must be below the Project root")
        # Preserve the runtime's lexical relative path while anchoring it to
        # the already-resolved Project root. This handles platform aliases
        # such as macOS /var -> /private/var without resolving runtime symlinks.
        self.runtime_root = self.project_root / relative_runtime
        self._validate_runtime_path(self.runtime_root, "Maintain runtime root")
        self._session_type_override = session_type
        self._runner = runner
        self._popen = popen
        self._clock = clock
        self._python_executable = expect_nonempty_string(
            python_executable, "Python executable"
        )
        self._bootstrap = bootstrap
        self._apply_decision = apply_decision

    def _session_type(self) -> type[Any]:
        if self._session_type_override is not None:
            return self._session_type_override
        from .codex_session import CodexMaintainSession

        return CodexMaintainSession

    def _binding(self) -> str:
        path = self.project_root / ".codex" / "maintain.json"
        value = _read_json_object(path, "Maintain host configuration")
        expect_exact_keys(value, _CONFIG_KEYS, "Maintain host configuration")
        expect_schema_version(
            value["schema_version"],
            MAINTAIN_HOST_CONFIG_SCHEMA_VERSION,
            "Maintain host configuration",
        )
        return validate_workspace_id(value["workspace_id"])

    @staticmethod
    def _payload_string(payload: Mapping[str, Any], key: str) -> str:
        if not isinstance(payload, Mapping):
            fail("Codex hook input must be a JSON object")
        return expect_nonempty_string(payload.get(key), f"Codex hook {key}")

    @staticmethod
    def _check_event(payload: Mapping[str, Any], command: str) -> None:
        actual = payload.get("hook_event_name")
        if actual is not None and actual != _HOOK_EVENTS[command]:
            fail(
                f"{command} received hook_event_name {actual!r}; expected "
                f"{_HOOK_EVENTS[command]!r}"
            )

    def _session_directory(self, session_id: str) -> Path:
        path = self.runtime_root / _hash_identifier(session_id)
        self._validate_runtime_path(path, "Maintain runtime session directory")
        return path

    def _directory_from_key(self, session_key: str) -> Path:
        if not _HEX_DIGEST.fullmatch(session_key):
            fail("Maintain runtime session key must be a SHA-256 digest")
        path = self.runtime_root / session_key
        self._validate_runtime_path(path, "Maintain runtime session directory")
        return path

    def _validate_runtime_path(self, path: Path, label: str) -> None:
        if not path.is_absolute() or ".." in path.parts:
            fail(f"{label} must be an absolute lexical descendant of the Project")
        try:
            relative = path.relative_to(self.project_root)
        except ValueError as exc:
            raise HarnessError(f"{label} must stay inside the Project root") from exc
        if not relative.parts:
            fail(f"{label} must be below the Project root")
        current = self.project_root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                fail(f"{label} must not use symlink components")
            if current.exists() and not current.is_dir():
                fail(f"{label} components must be directories")

    def _prepare_session_directory(self, session_directory: Path) -> None:
        self._validate_runtime_path(self.runtime_root, "Maintain runtime root")
        self._validate_runtime_path(
            session_directory, "Maintain runtime session directory"
        )
        try:
            session_directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise HarnessError(
                f"Maintain runtime session directory is unavailable: {exc}"
            ) from exc
        self._validate_runtime_path(self.runtime_root, "Maintain runtime root")
        self._validate_runtime_path(
            session_directory, "Maintain runtime session directory"
        )

    @contextmanager
    def _state_lock(self, session_directory: Path) -> Iterator[None]:
        self._prepare_session_directory(session_directory)
        lock_path = session_directory / ".state.lock"
        _reject_existing_symlink_components(lock_path, "Maintain state lock")
        descriptor = os.open(
            lock_path,
            os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    @contextmanager
    def _drain_lock(self, session_directory: Path) -> Iterator[None]:
        self._prepare_session_directory(session_directory)
        lock_path = session_directory / ".drain.lock"
        _reject_existing_symlink_components(lock_path, "Maintain drain lock")
        descriptor = os.open(
            lock_path,
            os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        try:
            # Drain runs only in a detached worker.  Blocking here closes the
            # snapshot race where a later worker could otherwise observe
            # ``busy``, exit, and leave an event added after the first worker's
            # snapshot permanently pending.
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def _read_session_state(self, session_directory: Path) -> dict[str, Any]:
        path = session_directory / "session.json"
        value = _read_json_object(path, "Maintain runtime session state")
        expect_exact_keys(value, _SESSION_KEYS, "Maintain runtime session state")
        expect_schema_version(
            value["schema_version"],
            MAINTAIN_HOST_STATE_SCHEMA_VERSION,
            "Maintain runtime session state",
        )
        value["workspace_id"] = validate_workspace_id(value["workspace_id"])
        value["thread_id"] = expect_nonempty_string(
            value["thread_id"], "Maintain runtime thread_id"
        )
        grounded_at = value["grounded_at"]
        if not isinstance(grounded_at, (int, float)) or isinstance(
            grounded_at, bool
        ):
            fail("Maintain runtime grounded_at must be a number")
        return value

    def _require_grounded(
        self, session_directory: Path, workspace_id: str
    ) -> dict[str, Any]:
        state = self._read_session_state(session_directory)
        if state["workspace_id"] != workspace_id:
            fail("Maintain runtime Workspace binding does not match configuration")
        return state

    def _next_sequence(self, session_directory: Path) -> int:
        path = session_directory / "next-sequence.json"
        if path.exists():
            value = _read_json_object(path, "Maintain runtime sequence state")
            expect_exact_keys(value, {"next"}, "Maintain runtime sequence state")
            next_value = value["next"]
            if type(next_value) is not int or next_value < 1:
                fail("Maintain runtime next sequence must be a positive integer")
        else:
            next_value = 1
        _atomic_write_json(path, {"next": next_value + 1})
        return next_value

    @staticmethod
    def _turn_path(session_directory: Path, turn_key: str) -> Path:
        return session_directory / "turns" / f"{turn_key}.json"

    @staticmethod
    def _event_path(session_directory: Path, turn_key: str) -> Path:
        return session_directory / "events" / f"{turn_key}.json"

    @staticmethod
    def _effect_path(session_directory: Path, turn_key: str) -> Path:
        return session_directory / "effects" / f"{turn_key}.json"

    def session_start(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "session-start")
        session_id = self._payload_string(payload, "session_id")
        workspace_id = self._binding()
        session_directory = self._session_directory(session_id)

        with self._state_lock(session_directory):
            state_path = session_directory / "session.json"
            if state_path.exists():
                state = self._require_grounded(session_directory, workspace_id)
                return _hook_output(
                    "SessionStart",
                    additional_context=(
                        "Workspace Maintain is reusing the already-grounded "
                        f"session for explicit Workspace `{workspace_id}`. "
                        "No new Context update or freshness claim was made."
                    ),
                )

            try:
                bounded_bootstrap = self._bootstrap(
                    self.project_root, self.work_root, workspace_id
                )
                session_type = self._session_type()
                semantic_session = session_type(
                    self.project_root,
                    workspace_id,
                    runner=self._runner,
                )
                grounding = semantic_session.start(bounded_bootstrap)
                thread_id = expect_nonempty_string(
                    semantic_session.thread_id,
                    "grounded Maintain thread_id",
                )
            except Exception as exc:
                message = (
                    f"Maintain grounding failed for Workspace `{workspace_id}`: "
                    f"{exc}. This session is not grounded or current."
                )
                self._write_notice(
                    session_directory,
                    "grounding",
                    kind="failure",
                    message=message,
                )
                return _hook_output(
                    "SessionStart",
                    additional_context=message,
                    system_message=message,
                )

            if grounding.get("status") != "grounded":
                question = grounding.get("question")
                if not isinstance(question, str) or not question.strip():
                    question = "Maintainer grounding requires a user decision."
                message = (
                    f"Maintain could not ground Workspace `{workspace_id}` "
                    f"without a user decision: {question} No grounded session, "
                    "Context write, freshness, or completion is claimed."
                )
                self._write_notice(
                    session_directory,
                    "grounding-needs-user-decision",
                    kind="ambiguity",
                    message=message,
                )
                return _hook_output(
                    "SessionStart",
                    additional_context=message,
                    system_message=message,
                )

            _atomic_write_json(
                state_path,
                {
                    "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                    "workspace_id": workspace_id,
                    "thread_id": thread_id,
                    "grounded_at": self._clock(),
                },
            )

        starting_state = grounding.get("starting_state")
        if not isinstance(starting_state, str) or not starting_state.strip():
            starting_state = json.dumps(
                grounding, ensure_ascii=False, sort_keys=True
            )
        context = (
            f"Workspace Maintain grounded explicit Workspace `{workspace_id}` "
            "once for this session. Grounding does not claim that Context is "
            f"fresh, verified, accepted, or complete. Starting state: {starting_state}"
        )
        return _hook_output(
            "SessionStart",
            additional_context=context,
            system_message=(
                f"Maintain grounded Workspace `{workspace_id}`; no Context "
                "update or completion was claimed."
            ),
        )

    def user_prompt(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "user-prompt")
        session_id = self._payload_string(payload, "session_id")
        turn_id = self._payload_string(payload, "turn_id")
        prompt = self._payload_string(payload, "prompt")
        workspace_id = self._binding()
        session_directory = self._session_directory(session_id)
        turn_key = _hash_identifier(turn_id)

        with self._state_lock(session_directory):
            self._require_grounded(session_directory, workspace_id)
            self._fail_orphan_prompts(
                session_directory, exclude_turn_key=turn_key
            )
            turn_path = self._turn_path(session_directory, turn_key)
            event_path = self._event_path(session_directory, turn_key)
            if turn_path.exists():
                existing = _read_json_object(
                    turn_path, "Maintain runtime user-prompt event"
                )
                if (
                    existing.get("turn_id") != turn_id
                    or existing.get("prompt") != prompt
                ):
                    fail("duplicate Maintain turn_id has different prompt content")
            else:
                sequence = (
                    _read_json_object(
                        event_path, "Maintain runtime response-end event"
                    ).get("sequence")
                    if event_path.exists()
                    else self._next_sequence(session_directory)
                )
                if type(sequence) is not int or sequence < 1:
                    fail("Maintain runtime event sequence is invalid")
                _atomic_write_json(
                    turn_path,
                    {
                        "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                        "sequence": sequence,
                        "turn_id": turn_id,
                        "prompt": prompt,
                        "received_at": self._clock(),
                    },
                )
                if event_path.exists():
                    event = _read_json_object(
                        event_path, "Maintain runtime response-end event"
                    )
                    if event.get("turn_id") != turn_id:
                        fail("Maintain runtime response-end turn binding changed")
                    event["user_prompt"] = prompt
                    _atomic_write_json(event_path, event)
            notices = self._take_notices(session_directory)
            unresolved = self._unresolved_event_keys(session_directory)
            blocking_failures = self._blocking_failure_keys(session_directory)

        # A previous detached worker may have crashed or lost a launch race.
        # Re-kicking is safe because the per-session drain lock serializes the
        # workers and the effect file makes resolved boundaries effect-once.
        if unresolved and not blocking_failures:
            self._start_detached_drain(session_directory.name)

        if not notices and not unresolved and not blocking_failures:
            return _hook_output("UserPromptSubmit")
        messages = [str(notice["message"]) for notice in notices]
        if unresolved:
            if blocking_failures:
                messages.append(
                    f"{len(unresolved)} later Workspace Maintain response-end "
                    "boundary/boundaries remain pending behind a failed "
                    "semantic or apply boundary. They were not applied, do not "
                    "establish fresh or current Context, and will not be "
                    "retried in this Main session. A new Main session must "
                    "ground from the canonical Workspace."
                )
            else:
                messages.append(
                    f"{len(unresolved)} previously accepted Workspace Maintain "
                    "response-end boundary/boundaries are still pending. They "
                    "are not completed and do not establish fresh or current "
                    "Context; a detached worker was started again."
                )
        elif blocking_failures:
            messages.append(
                "Automatic Workspace Maintain is paused for this Main session "
                "after a failed semantic or apply boundary. No later Context "
                "freshness is claimed; a new Main session must ground from the "
                "canonical Workspace."
            )
        context = "Previous Workspace Maintain results requiring attention:\n- " + (
            "\n- ".join(messages)
        )
        return _hook_output(
            "UserPromptSubmit",
            additional_context=context,
            system_message=(
                "Workspace Maintain has a previous result or pending boundary "
                "requiring attention."
            ),
        )

    def response_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "response-end")
        session_id = self._payload_string(payload, "session_id")
        turn_id = self._payload_string(payload, "turn_id")
        main_response = self._payload_string(
            payload, "last_assistant_message"
        )
        workspace_id = self._binding()
        session_directory = self._session_directory(session_id)
        session_key = session_directory.name
        turn_key = _hash_identifier(turn_id)

        with self._state_lock(session_directory):
            self._require_grounded(session_directory, workspace_id)
            turn_path = self._turn_path(session_directory, turn_key)
            if turn_path.exists():
                turn = _read_json_object(
                    turn_path, "Maintain runtime user-prompt event"
                )
                if turn.get("turn_id") != turn_id:
                    fail("Maintain runtime prompt turn binding changed")
                sequence = turn.get("sequence")
                user_prompt = turn.get("prompt")
            else:
                sequence = self._next_sequence(session_directory)
                user_prompt = None
            if type(sequence) is not int or sequence < 1:
                fail("Maintain runtime turn sequence is invalid")
            event_path = self._event_path(session_directory, turn_key)
            event = {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "sequence": sequence,
                "turn_id": turn_id,
                "user_prompt": user_prompt,
                "main_response": main_response,
                "accepted_at": self._clock(),
            }
            if event_path.exists():
                existing = _read_json_object(
                    event_path, "Maintain runtime response-end event"
                )
                stable_existing = {
                    key: existing.get(key)
                    for key in (
                        "schema_version",
                        "sequence",
                        "turn_id",
                        "user_prompt",
                        "main_response",
                    )
                }
                stable_event = {
                    key: event[key]
                    for key in (
                        "schema_version",
                        "sequence",
                        "turn_id",
                        "user_prompt",
                        "main_response",
                    )
                }
                if stable_existing != stable_event:
                    fail("duplicate Maintain response-end has different content")
            else:
                _atomic_write_json(event_path, event)
            blocking_failures = self._blocking_failure_keys(session_directory)

        if not blocking_failures:
            self._start_detached_drain(session_key)
        return _hook_output("Stop")

    def session_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "session-end")
        session_id = self._payload_string(payload, "session_id")
        workspace_id = self._binding()
        session_directory = self._session_directory(session_id)
        session_key = session_directory.name

        with self._state_lock(session_directory):
            self._require_grounded(session_directory, workspace_id)
            orphaned = self._fail_orphan_prompts(session_directory)
            unresolved = self._unresolved_event_keys(session_directory)
            failed = self._failed_effect_keys(session_directory)
            blocking_failures = self._blocking_failure_keys(session_directory)
            notices = self._take_notices(session_directory)
            _atomic_write_json(
                session_directory / "session-end.json",
                {
                    "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                    "ended_at": self._clock(),
                    "blocking_failure_keys": blocking_failures,
                    "failed_effect_keys": failed,
                    "orphan_prompt_keys": orphaned,
                    "surfaced_notice_count": len(notices),
                    "unresolved_event_keys": unresolved,
                },
            )
        if unresolved and not blocking_failures:
            self._start_detached_drain(session_key)
        if unresolved or orphaned or failed or notices:
            status_message = (
                f"Maintain session ended with {len(orphaned)} prompt(s) missing "
                f"a response-end and {len(unresolved)} accepted response-end "
                f"event(s) not yet resolved; {len(failed)} effect(s) are "
                "failed, not completed. Completion or freshness is not claimed."
            )
            if unresolved and not blocking_failures:
                status_message += (
                    " A best-effort worker was started for accepted "
                    "response-end events."
                )
            elif unresolved:
                status_message += (
                    " Later events remain pending behind a failed semantic or "
                    "apply boundary and were not retried in this Main session."
                )
            notice_messages = [str(notice["message"]) for notice in notices]
            message = "\n".join([status_message, *notice_messages])
            return _hook_output(
                "SessionEnd",
                additional_context=message,
                system_message=message,
            )
        return _hook_output("SessionEnd")

    def _fail_orphan_prompts(
        self,
        session_directory: Path,
        *,
        exclude_turn_key: str | None = None,
    ) -> list[str]:
        """Expose prompts superseded or ended without a matching Stop event."""

        turns_directory = session_directory / "turns"
        if not turns_directory.exists():
            return []
        orphaned: list[str] = []
        for turn_path in sorted(turns_directory.glob("*.json")):
            turn_key = turn_path.stem
            if turn_key == exclude_turn_key:
                continue
            if not _HEX_DIGEST.fullmatch(turn_key):
                fail("Maintain runtime contains an invalid prompt filename")
            if self._event_path(session_directory, turn_key).exists():
                continue
            effect_path = self._effect_path(session_directory, turn_key)
            if effect_path.exists():
                continue
            turn = _read_json_object(
                turn_path, "Maintain runtime user-prompt event"
            )
            turn_id = turn.get("turn_id")
            message = (
                f"Maintain received prompt turn `{turn_id}` without a matching "
                "response-end before the session advanced. That boundary is "
                "failed and no completion or freshness is claimed."
            )
            self._write_notice(
                session_directory,
                turn_key,
                kind="failure",
                message=message,
            )
            _atomic_write_json(
                effect_path,
                {
                    "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                    "blocks_later_events": False,
                    "status": "failed",
                    "finished_at": self._clock(),
                    "error": "prompt_without_response_end",
                },
            )
            orphaned.append(turn_key)
        return orphaned

    def _start_detached_drain(self, session_key: str) -> None:
        command = [
            self._python_executable,
            "-m",
            "context.work.harness.maintain.host_adapter",
            "drain",
            "--project-root",
            str(self.project_root),
            "--runtime-root",
            str(self.runtime_root),
            "--session-key",
            session_key,
        ]
        try:
            self._popen(
                command,
                cwd=self.project_root,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            session_directory = self._directory_from_key(session_key)
            self._write_notice(
                session_directory,
                f"spawn-{int(self._clock() * 1_000_000)}",
                kind="failure",
                message=(
                    "Maintain accepted a response-end but could not start its "
                    f"background worker: {exc}. Completion is not claimed."
                ),
            )

    def _events(self, session_directory: Path) -> list[tuple[str, dict[str, Any]]]:
        events_directory = session_directory / "events"
        if not events_directory.exists():
            return []
        events: list[tuple[str, dict[str, Any]]] = []
        for path in events_directory.glob("*.json"):
            turn_key = path.stem
            if not _HEX_DIGEST.fullmatch(turn_key):
                fail("Maintain runtime contains an invalid event filename")
            event = _read_json_object(path, "Maintain runtime response-end event")
            sequence = event.get("sequence")
            if type(sequence) is not int or sequence < 1:
                fail("Maintain runtime event sequence is invalid")
            events.append((turn_key, event))
        events.sort(key=lambda item: (item[1]["sequence"], item[0]))
        return events

    def _unresolved_event_keys(self, session_directory: Path) -> list[str]:
        return [
            turn_key
            for turn_key, _ in self._events(session_directory)
            if not self._effect_path(session_directory, turn_key).exists()
        ]

    def _failed_effect_keys(self, session_directory: Path) -> list[str]:
        effects_directory = session_directory / "effects"
        if not effects_directory.exists():
            return []
        failed: list[str] = []
        for path in sorted(effects_directory.glob("*.json")):
            if not _HEX_DIGEST.fullmatch(path.stem):
                fail("Maintain runtime contains an invalid effect filename")
            effect = _read_json_object(path, "Maintain runtime effect")
            if effect.get("status") == "failed":
                failed.append(path.stem)
        return failed

    @staticmethod
    def _effect_blocks_later_events(effect: Mapping[str, Any]) -> bool:
        if "blocks_later_events" not in effect:
            # schema v1 effects written before failure ordering was added did
            # not distinguish pairing failures from semantic/apply failures.
            # Treat an old failed effect as blocking rather than risk applying
            # a later event against an uncertain thread/Context relationship.
            return effect.get("status") == "failed"
        blocks_later = effect.get("blocks_later_events")
        if type(blocks_later) is not bool:
            fail("Maintain runtime effect blocking flag must be boolean")
        return blocks_later

    def _blocking_failure_keys(self, session_directory: Path) -> list[str]:
        blocking: list[str] = []
        for turn_key, _ in self._events(session_directory):
            effect_path = self._effect_path(session_directory, turn_key)
            if not effect_path.exists():
                continue
            effect = _read_json_object(
                effect_path, "Maintain runtime effect"
            )
            if (
                effect.get("status") == "failed"
                and self._effect_blocks_later_events(effect)
            ):
                blocking.append(turn_key)
        return blocking

    def _write_notice(
        self,
        session_directory: Path,
        notice_key: str,
        *,
        kind: str,
        message: str,
    ) -> None:
        if kind not in {"important", "ambiguity", "failure"}:
            fail("Maintain notifications are limited to important results and failures")
        safe_key = _hash_identifier(notice_key)
        path = session_directory / "notices" / f"{safe_key}.json"
        _atomic_write_json(
            path,
            {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "kind": kind,
                "message": expect_nonempty_string(message, "Maintain notice"),
                "created_at": self._clock(),
            },
        )

    def _take_notices(self, session_directory: Path) -> list[dict[str, Any]]:
        notices_directory = session_directory / "notices"
        if not notices_directory.exists():
            return []
        surfaced_directory = session_directory / "surfaced-notices"
        surfaced_directory.mkdir(parents=True, exist_ok=True)
        notices: list[tuple[Path, dict[str, Any]]] = []
        for path in notices_directory.glob("*.json"):
            notice = _read_json_object(path, "Maintain runtime notification")
            if notice.get("kind") not in {"important", "ambiguity", "failure"}:
                fail("Maintain runtime notification kind is invalid")
            if not isinstance(notice.get("created_at"), (int, float)):
                fail("Maintain runtime notification timestamp is invalid")
            expect_nonempty_string(
                notice.get("message"), "Maintain runtime notification message"
            )
            notices.append((path, notice))
        notices.sort(key=lambda item: (item[1]["created_at"], item[0].name))
        for path, _ in notices:
            os.replace(path, surfaced_directory / path.name)
        return [notice for _, notice in notices]

    def _notification_for_result(
        self,
        session_directory: Path,
        turn_key: str,
        result: Mapping[str, Any],
    ) -> None:
        context_status = result.get("context_status")
        importance = result.get("importance")
        workspace_id = result.get("workspace_id")
        summary = result.get("summary")
        if context_status == "needs_user_decision":
            question = result.get("question")
            self._write_notice(
                session_directory,
                turn_key,
                kind="ambiguity",
                message=(
                    f"Maintain needs a decision for Workspace `{workspace_id}`: "
                    f"{question} No related Context write was made."
                ),
            )
        elif context_status == "updated" and importance == "important":
            changed = result.get("changed")
            paths = []
            if isinstance(changed, list):
                paths = [
                    str(item.get("path"))
                    for item in changed
                    if isinstance(item, Mapping) and item.get("path")
                ]
            path_text = f" Changed: {', '.join(paths)}." if paths else ""
            self._write_notice(
                session_directory,
                turn_key,
                kind="important",
                message=(
                    f"Maintain updated Workspace `{workspace_id}`: {summary}."
                    f"{path_text}"
                ),
            )

    def drain(self, session_key: str) -> dict[str, Any]:
        session_directory = self._directory_from_key(session_key)
        workspace_id = self._binding()
        summary = {
            "session_key": session_key,
            "processed": 0,
            "failed": 0,
            "already_resolved": 0,
            "blocked": 0,
            "busy": False,
        }
        with self._drain_lock(session_directory):
            state = self._require_grounded(session_directory, workspace_id)
            for turn_key, event in self._events(session_directory):
                effect_path = self._effect_path(session_directory, turn_key)
                if effect_path.exists():
                    summary["already_resolved"] += 1
                    effect = _read_json_object(
                        effect_path, "Maintain runtime effect"
                    )
                    if (
                        effect.get("status") == "failed"
                        and self._effect_blocks_later_events(effect)
                    ):
                        summary["blocked"] = len(
                            self._unresolved_event_keys(session_directory)
                        )
                        break
                    continue
                user_prompt = event.get("user_prompt")
                turn_id = event.get("turn_id")
                main_response = event.get("main_response")
                if not all(
                    isinstance(value, str) and value.strip()
                    for value in (user_prompt, turn_id, main_response)
                ):
                    message = (
                        "Maintain could not pair a response-end with its stable "
                        "user prompt and turn_id. No completion or freshness is "
                        "claimed."
                    )
                    self._write_notice(
                        session_directory,
                        turn_key,
                        kind="failure",
                        message=message,
                    )
                    _atomic_write_json(
                        effect_path,
                        {
                            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                            "blocks_later_events": False,
                            "status": "failed",
                            "finished_at": self._clock(),
                            "error": message,
                        },
                    )
                    summary["failed"] += 1
                    continue
                try:
                    session_type = self._session_type()
                    semantic_session = session_type.restore(
                        self.project_root,
                        workspace_id,
                        thread_id=state["thread_id"],
                        runner=self._runner,
                    )
                    decision = semantic_session.resume(
                        {
                            "workspace_id": workspace_id,
                            "turn_id": turn_id,
                            "user_prompt": user_prompt,
                            "main_response": main_response,
                        }
                    )
                    result = self._apply_decision(
                        self.project_root,
                        self.work_root,
                        workspace_id,
                        decision,
                    )
                    self._notification_for_result(
                        session_directory, turn_key, result
                    )
                    _atomic_write_json(
                        effect_path,
                        {
                            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                            "status": "resolved",
                            "finished_at": self._clock(),
                            "context_status": result.get("context_status"),
                            "importance": result.get("importance"),
                        },
                    )
                    summary["processed"] += 1
                except Exception as exc:
                    message = (
                        f"Maintain failed while processing Workspace "
                        f"`{workspace_id}` response-end: {exc}. The event is "
                        "failed, not completed; inspect actual Context before "
                        "retrying."
                    )
                    self._write_notice(
                        session_directory,
                        turn_key,
                        kind="failure",
                        message=message,
                    )
                    _atomic_write_json(
                        effect_path,
                        {
                            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                            "blocks_later_events": True,
                            "status": "failed",
                            "finished_at": self._clock(),
                            "error": str(exc),
                        },
                    )
                    summary["failed"] += 1
                    summary["blocked"] = len(
                        self._unresolved_event_keys(session_directory)
                    )
                    break
        return summary


def _discover_project_root(start: Path) -> Path:
    try:
        candidate = start.resolve(strict=True)
    except OSError as exc:
        raise HarnessError(f"Codex hook cwd is unavailable: {exc}") from exc
    if candidate.is_file():
        candidate = candidate.parent
    for directory in (candidate, *candidate.parents):
        if (directory / ".codex" / "maintain.json").is_file():
            return directory
    fail("could not find project .codex/maintain.json from Codex hook cwd")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Codex Maintain host adapter")
    parser.add_argument(
        "command",
        choices=(
            "session-start",
            "user-prompt",
            "response-end",
            "session-end",
            "drain",
        ),
    )
    parser.add_argument("--project-root")
    parser.add_argument("--runtime-root")
    parser.add_argument("--session-key")
    return parser


def _stdin_payload() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"Codex hook stdin is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        fail("Codex hook stdin must contain a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        payload: dict[str, Any] | None = None
        if arguments.project_root:
            project_root = Path(arguments.project_root)
        elif arguments.command == "drain":
            fail("drain requires --project-root")
        else:
            payload = _stdin_payload()
            project_root = _discover_project_root(
                Path(str(payload.get("cwd", Path.cwd())))
            )
        adapter = MaintainHostAdapter(
            project_root,
            runtime_root=(
                Path(arguments.runtime_root) if arguments.runtime_root else None
            ),
        )
        if arguments.command == "drain":
            if not arguments.session_key:
                fail("drain requires --session-key")
            output = adapter.drain(arguments.session_key)
        else:
            if arguments.session_key:
                fail("--session-key is only valid for drain")
            if payload is None:
                payload = _stdin_payload()
            handlers = {
                "session-start": adapter.session_start,
                "user-prompt": adapter.user_prompt,
                "response-end": adapter.response_end,
                "session-end": adapter.session_end,
            }
            output = handlers[arguments.command](payload)
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (HarnessError, OSError, ValueError) as exc:
        if arguments.command == "drain":
            print(f"Maintain drain failed: {exc}", file=sys.stderr)
            return 2
        event_name = _HOOK_EVENTS[arguments.command]
        message = (
            f"Workspace Maintain {arguments.command} failed: {exc}. "
            "No success, freshness, or completion is claimed."
        )
        print(
            json.dumps(
                _hook_output(
                    event_name,
                    additional_context=message,
                    system_message=message,
                ),
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
