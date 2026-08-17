"""Run one replaceable Codex warm-session adapter for Maintain.

This module is an execution bridge, not persistent truth. Workspace files own
durable context, and callers own event acknowledgement and replay. Replacing or
removing this adapter must not change the meaning of Maintain or a Workspace.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any


CHILD_ENVIRONMENT_VARIABLE = "CODEX_CONTEXT_MAINTAINER_CHILD"
DECISION_OUTCOMES = frozenset(
    {
        "no_change",
        "updated_quiet",
        "updated_report",
        "needs_decision",
        "freshness_failed",
    }
)
DEFAULT_DECISION_SCHEMA = Path(__file__).with_name("decision.schema.json")
# The synchronous SessionStart hook has a 120-second host deadline. Keep one
# model call comfortably inside it, and never chain a second call after this
# timeout; later hooks own retry.
DEFAULT_PROCESS_TIMEOUT_SECONDS = 90.0


class MaintainerRunnerError(RuntimeError):
    """Base error for an unaccepted Maintain turn."""


class CodexProcessError(MaintainerRunnerError):
    """The Codex process exited unsuccessfully."""

    def __init__(self, returncode: int, stderr: str) -> None:
        detail = stderr.strip() or "no stderr"
        super().__init__(f"Codex exited with status {returncode}: {detail}")
        self.returncode = returncode
        self.stderr = stderr


class CodexTimeoutError(MaintainerRunnerError):
    """The Codex process did not finish within the adapter's finite wait."""

    def __init__(self, timeout_seconds: float) -> None:
        super().__init__(
            f"Codex did not finish within {timeout_seconds:g} seconds"
        )
        self.timeout_seconds = timeout_seconds


class CodexProtocolError(MaintainerRunnerError):
    """The Codex JSONL stream did not satisfy the adapter protocol."""


class CodexTurnError(MaintainerRunnerError):
    """Codex explicitly reported a failed turn or error event."""


@dataclass(frozen=True)
class ProposedWrite:
    """One guarded Workspace Markdown replacement proposed by the agent."""

    path: str
    expected_sha256: str | None
    content: str

    @classmethod
    def from_object(cls, value: object, index: int) -> ProposedWrite:
        if not isinstance(value, dict):
            raise CodexProtocolError(f"writes[{index}] must be an object")
        if set(value) != {"path", "expected_sha256", "content"}:
            raise CodexProtocolError(
                f"writes[{index}] must contain only path, expected_sha256, content"
            )
        path = value["path"]
        content = value["content"]
        expected = value["expected_sha256"]
        if not isinstance(path, str) or not path.strip():
            raise CodexProtocolError(f"writes[{index}].path must not be blank")
        if not isinstance(content, str):
            raise CodexProtocolError(f"writes[{index}].content must be a string")
        if expected is not None and (
            not isinstance(expected, str)
            or len(expected) != 64
            or any(character not in "0123456789abcdef" for character in expected)
        ):
            raise CodexProtocolError(
                f"writes[{index}].expected_sha256 must be a lowercase SHA-256 or null"
            )
        return cls(path=path, expected_sha256=expected, content=content)


@dataclass(frozen=True)
class MaintainerDecision:
    """The minimal semantic outcome returned by the Maintainer agent."""

    outcome: str
    workspace_id: str
    event_id: str
    summary: str
    changed_paths: tuple[str, ...]
    writes: tuple[ProposedWrite, ...]
    question: str | None
    evidence_paths: tuple[str, ...]
    resolved_report_ids: tuple[str, ...]

    @classmethod
    def from_object(cls, value: object) -> MaintainerDecision:
        if not isinstance(value, dict):
            raise CodexProtocolError(
                "The final agent_message must contain a JSON object"
            )

        required = {
            "outcome",
            "workspace_id",
            "event_id",
            "summary",
            "changed_paths",
            "writes",
            "question",
            "evidence_paths",
            "resolved_report_ids",
        }
        actual = set(value)
        missing = sorted(required - actual)
        extra = sorted(actual - required)
        if missing or extra:
            details: list[str] = []
            if missing:
                details.append(f"missing fields: {', '.join(missing)}")
            if extra:
                details.append(f"unexpected fields: {', '.join(extra)}")
            raise CodexProtocolError(
                "Invalid Maintainer decision object (" + "; ".join(details) + ")"
            )

        outcome = _required_string(value, "outcome")
        if outcome not in DECISION_OUTCOMES:
            raise CodexProtocolError(
                f"Invalid Maintainer decision outcome: {outcome!r}"
            )
        summary = _string(value, "summary")

        question_value = value["question"]
        if question_value is not None and not isinstance(question_value, str):
            raise CodexProtocolError(
                "Maintainer decision field 'question' must be a string or null"
            )

        writes_value = value["writes"]
        if not isinstance(writes_value, list):
            raise CodexProtocolError("Maintainer decision field 'writes' must be an array")
        writes = tuple(
            ProposedWrite.from_object(item, index)
            for index, item in enumerate(writes_value)
        )
        paths = _string_tuple(value, "changed_paths")
        write_paths = tuple(write.path for write in writes)
        if len(set(write_paths)) != len(write_paths):
            raise CodexProtocolError("Maintainer decision contains duplicate write paths")
        if tuple(sorted(paths)) != tuple(sorted(write_paths)):
            raise CodexProtocolError(
                "Maintainer decision changed_paths must match writes paths"
            )
        if outcome.startswith("updated_") and not writes:
            raise CodexProtocolError(
                "An updated Maintainer decision must contain at least one write"
            )
        if not outcome.startswith("updated_") and writes:
            raise CodexProtocolError(
                "Only an updated Maintainer decision may contain writes"
            )
        if outcome == "needs_decision" and (
            question_value is None or not question_value.strip()
        ):
            raise CodexProtocolError(
                "A needs_decision outcome must contain a non-blank question"
            )
        if outcome == "needs_decision" and not summary.strip():
            raise CodexProtocolError(
                "A needs_decision outcome must contain a non-blank handoff summary"
            )
        if outcome != "needs_decision" and question_value is not None:
            raise CodexProtocolError(
                "Only a needs_decision outcome may contain a question"
            )

        resolved_report_ids = _string_tuple(value, "resolved_report_ids")
        if any(
            re.fullmatch(r"[0-9a-f]{32}", report_id) is None
            for report_id in resolved_report_ids
        ):
            raise CodexProtocolError(
                "resolved_report_ids must contain 32-character lowercase hex ids"
            )
        if len(resolved_report_ids) > 32:
            raise CodexProtocolError(
                "resolved_report_ids must contain at most 32 ids"
            )

        return cls(
            outcome=outcome,
            workspace_id=_required_string(value, "workspace_id"),
            event_id=_required_string(value, "event_id"),
            summary=summary,
            changed_paths=paths,
            writes=writes,
            question=question_value,
            evidence_paths=_string_tuple(value, "evidence_paths"),
            resolved_report_ids=resolved_report_ids,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "outcome": self.outcome,
            "workspace_id": self.workspace_id,
            "event_id": self.event_id,
            "summary": self.summary,
            "changed_paths": list(self.changed_paths),
            "writes": [
                {
                    "path": write.path,
                    "expected_sha256": write.expected_sha256,
                    "content": write.content,
                }
                for write in self.writes
            ],
            "question": self.question,
            "evidence_paths": list(self.evidence_paths),
            "resolved_report_ids": list(self.resolved_report_ids),
        }


@dataclass(frozen=True)
class MaintainerTurn:
    """One successfully completed Codex turn."""

    thread_id: str
    decision: MaintainerDecision


ProcessRunner = Callable[..., subprocess.CompletedProcess[str]]


class CodexWarmSessionRunner:
    """Keep a Codex thread id in memory while the calling task remains alive.

    The thread id is committed only after a complete, successful JSONL turn.
    Failed calls leave the previous id intact so the caller can replay the
    unacknowledged prompt. This object does not persist a cursor or acknowledge
    events on the caller's behalf.
    """

    def __init__(
        self,
        *,
        project_root: Path,
        sandbox: str = "read-only",
        decision_schema: Path = DEFAULT_DECISION_SCHEMA,
        codex_executable: str = "codex",
        process_runner: ProcessRunner = subprocess.run,
        initial_thread_id: str | None = None,
        process_timeout_seconds: float = DEFAULT_PROCESS_TIMEOUT_SECONDS,
    ) -> None:
        if not sandbox.strip():
            raise ValueError("sandbox must not be blank")
        if not codex_executable.strip():
            raise ValueError("codex_executable must not be blank")
        if process_timeout_seconds <= 0:
            raise ValueError("process_timeout_seconds must be positive")

        self.project_root = project_root.resolve()
        self.sandbox = sandbox
        self.decision_schema = decision_schema.resolve()
        self.codex_executable = codex_executable
        self.process_timeout_seconds = process_timeout_seconds
        self._process_runner = process_runner
        if initial_thread_id is not None and not initial_thread_id.strip():
            raise ValueError("initial_thread_id must not be blank")
        self._thread_id = initial_thread_id

    @property
    def thread_id(self) -> str | None:
        return self._thread_id

    def command_for(self, prompt: str) -> list[str]:
        """Build the bootstrap or resume argv without executing it."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-blank string")

        if self._thread_id is None:
            return [
                self.codex_executable,
                "exec",
                "-C",
                str(self.project_root),
                "-s",
                self.sandbox,
                "--json",
                "--output-schema",
                str(self.decision_schema),
                "-",
            ]
        return [
            self.codex_executable,
            "exec",
            "resume",
            self._thread_id,
            "--json",
            "--output-schema",
            str(self.decision_schema),
            "-",
        ]

    def run(self, prompt: str) -> MaintainerTurn:
        """Execute one turn and accept it only after strict stream validation."""
        command = self.command_for(prompt)
        previous_thread_id = self._thread_id
        environment = os.environ.copy()
        environment[CHILD_ENVIRONMENT_VARIABLE] = "1"
        try:
            completed = self._process_runner(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
                env=environment,
                input=prompt,
                timeout=self.process_timeout_seconds,
            )
        except subprocess.TimeoutExpired as error:
            raise CodexTimeoutError(self.process_timeout_seconds) from error

        if completed.returncode != 0:
            raise CodexProcessError(completed.returncode, completed.stderr)

        turn = parse_codex_jsonl(completed.stdout)
        if (
            previous_thread_id is not None
            and turn.thread_id != previous_thread_id
        ):
            raise CodexProtocolError(
                "Resumed Codex turn returned a different thread id: "
                f"expected {previous_thread_id!r}, got {turn.thread_id!r}"
            )

        self._thread_id = turn.thread_id
        return turn


def parse_codex_jsonl(output: str) -> MaintainerTurn:
    """Parse one Codex `exec --json` stream without accepting partial output."""
    thread_id: str | None = None
    last_agent_message: str | None = None
    terminal_event: str | None = None

    lines = output.splitlines()
    if not lines:
        raise CodexProtocolError("Codex returned an empty JSONL stream")

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise CodexProtocolError(
                f"Codex JSONL line {line_number} is blank"
            )
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise CodexProtocolError(
                f"Codex JSONL line {line_number} is not valid JSON: {error.msg}"
            ) from error
        if not isinstance(event, dict):
            raise CodexProtocolError(
                f"Codex JSONL line {line_number} must be an object"
            )

        event_type = event.get("type")
        if not isinstance(event_type, str) or not event_type:
            raise CodexProtocolError(
                f"Codex JSONL line {line_number} has no valid event type"
            )
        if terminal_event is not None:
            raise CodexProtocolError(
                "Codex JSONL stream contains an event after its terminal event"
            )

        if event_type == "thread.started":
            candidate = event.get("thread_id")
            if not isinstance(candidate, str) or not candidate.strip():
                raise CodexProtocolError(
                    "thread.started must contain a non-blank thread_id"
                )
            if thread_id is not None:
                raise CodexProtocolError(
                    "Codex JSONL stream contains multiple thread.started events"
                )
            thread_id = candidate
        elif event_type == "item.completed":
            item = event.get("item")
            if not isinstance(item, dict):
                raise CodexProtocolError(
                    "item.completed must contain an item object"
                )
            item_type = item.get("type")
            if not isinstance(item_type, str) or not item_type:
                raise CodexProtocolError(
                    "item.completed item must contain a valid type"
                )
            if item_type == "agent_message":
                text = item.get("text")
                if not isinstance(text, str):
                    raise CodexProtocolError(
                        "Completed agent_message must contain text"
                    )
                last_agent_message = text
        elif event_type in {"turn.completed", "turn.failed", "error"}:
            terminal_event = event_type
            if event_type != "turn.completed":
                raise CodexTurnError(_event_error_message(event_type, event))

    if thread_id is None:
        raise CodexProtocolError(
            "Codex JSONL stream has no thread.started thread_id"
        )
    if terminal_event is None:
        raise CodexProtocolError(
            "Codex JSONL stream has no terminal turn event"
        )
    if last_agent_message is None:
        raise CodexProtocolError(
            "Completed Codex turn has no completed agent_message"
        )

    try:
        decision_object = json.loads(last_agent_message)
    except json.JSONDecodeError as error:
        raise CodexProtocolError(
            "The final completed agent_message is not valid JSON: "
            f"{error.msg}"
        ) from error

    return MaintainerTurn(
        thread_id=thread_id,
        decision=MaintainerDecision.from_object(decision_object),
    )


def _event_error_message(event_type: str, event: Mapping[str, Any]) -> str:
    error = event.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if isinstance(message, str) and message.strip():
            return f"Codex reported {event_type}: {message}"
    message = event.get("message")
    if isinstance(message, str) and message.strip():
        return f"Codex reported {event_type}: {message}"
    return f"Codex reported {event_type}"


def _string(value: Mapping[str, Any], field: str) -> str:
    candidate = value[field]
    if not isinstance(candidate, str):
        raise CodexProtocolError(
            f"Maintainer decision field {field!r} must be a string"
        )
    return candidate


def _required_string(value: Mapping[str, Any], field: str) -> str:
    candidate = _string(value, field)
    if not candidate.strip():
        raise CodexProtocolError(
            f"Maintainer decision field {field!r} must not be blank"
        )
    return candidate


def _string_tuple(value: Mapping[str, Any], field: str) -> tuple[str, ...]:
    candidate = value[field]
    if not isinstance(candidate, list):
        raise CodexProtocolError(
            f"Maintainer decision field {field!r} must be an array"
        )
    if any(not isinstance(item, str) or not item.strip() for item in candidate):
        raise CodexProtocolError(
            f"Maintainer decision field {field!r} must contain non-blank strings"
        )
    if len(candidate) != len(set(candidate)):
        raise CodexProtocolError(
            f"Maintainer decision field {field!r} must not contain duplicates"
        )
    return tuple(candidate)
