"""Claude Code hook의 prompt·응답을 공통 Maintain runtime에 연결한다.

Claude 입력에는 두 hook이 공유하는 turn id가 없어 전용 runtime에 최소 연결
상태를 보존한다. Workspace 연결과 파일 반영 규칙은 공통 runtime을 따른다."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
from typing import Any, Mapping, TextIO
import uuid

from ...workspace_contract import HarnessError, expect_nonempty_string, fail
from ..runtime.engine import MaintainRuntime
from ..runtime.storage_io import (
    _atomic_write_json,
    _read_json_object as _read_host_json_object,
)
from .codex_session import CodexMaintainSession
from .events import _hook_output

_HOOK_EVENTS = {
    "session-start": "SessionStart",
    "user-prompt": "UserPromptSubmit",
    "response-end": "Stop",
    "session-end": "SessionEnd",
}
_CONTROL_COMMANDS = {"activate", "deactivate", "status"}
_CLAUDE_SESSION_ENV = "MAINTAIN_CLAUDE_SESSION_ID"
_TURN_STATE_SCHEMA_VERSION = 1


class ClaudeHookAdapter:
    """Workspace를 추론하지 않고 Claude Code hook을 공통 이벤트로 변환한다."""

    def __init__(
        self,
        project_root: Path,
        *,
        adapter: MaintainRuntime | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.runtime_root = (
            adapter.runtime_root
            if adapter is not None
            else self.project_root / ".claude" / "maintain-runtime"
        )
        self.adapter = adapter or MaintainRuntime(
            self.project_root,
            runtime_root=self.runtime_root,
            config_path=self.project_root / ".claude" / "maintain.json",
            worker_module="context.work.harness.maintain.adapters.claude",
            session_type=CodexMaintainSession,
        )
        self.environ = dict(os.environ if environ is None else environ)

    @staticmethod
    def _session_key(session_id: str) -> str:
        return hashlib.sha256(session_id.encode("utf-8")).hexdigest()

    def _turn_state_path(self, session_id: str) -> Path:
        return (
            self.runtime_root
            / self._session_key(session_id)
            / "claude-hook-turn-state.json"
        )

    def _turn_state_session_directory(self, session_id: str) -> Path:
        """런타임이 검증한 동일한 세션 디렉터리를 사용한다."""
        return self.adapter.store._session_directory(session_id)

    @staticmethod
    def _payload_string(payload: Mapping[str, Any], key: str) -> str:
        if not isinstance(payload, dict):
            fail("Claude hook input must be a JSON object")
        return expect_nonempty_string(payload.get(key), f"Claude hook {key}")

    @staticmethod
    def _is_subagent_payload(payload: Mapping[str, Any]) -> bool:
        """Claude subagent 이벤트에 Main session의 연결을 적용하지 않는다."""
        if not isinstance(payload, dict):
            fail("Claude hook input must be a JSON object")
        agent_id = payload.get("agent_id")
        return isinstance(agent_id, str) and bool(agent_id.strip())

    def _base_payload(self, payload: Mapping[str, Any], command: str) -> dict[str, Any]:
        actual = payload.get("hook_event_name")
        expected = _HOOK_EVENTS[command]
        if actual != expected:
            fail(
                f"{command} received hook_event_name {actual!r}; expected {expected!r}"
            )
        return {
            "hook_event_name": expected,
            "session_id": self._payload_string(payload, "session_id"),
            "cwd": str(payload.get("cwd") or self.project_root),
        }

    def _write_session_environment(self, session_id: str) -> None:
        environment_file = self.environ.get("CLAUDE_ENV_FILE")
        if not environment_file:
            return
        path = Path(environment_file)
        try:
            with path.open("a", encoding="utf-8") as stream:
                stream.write(
                    f"export {_CLAUDE_SESSION_ENV}={shlex.quote(session_id)}\n"
                )
        except OSError as exc:
            raise HarnessError(
                f"Claude SessionStart could not persist session selector: {exc}"
            ) from exc

    def _read_turn_state(self, session_id: str) -> dict[str, Any] | None:
        path = self._turn_state_path(session_id)
        if not path.exists():
            return None
        value = _read_host_json_object(path, "Claude Maintain turn state")
        if value.get("schema_version") != _TURN_STATE_SCHEMA_VERSION:
            fail("Claude Maintain turn state has an unsupported schema version")
        pending = value.get("pending")
        last_stop = value.get("last_stop")
        for label, candidate in (("pending", pending), ("last_stop", last_stop)):
            if candidate is not None and not isinstance(candidate, dict):
                fail(f"Claude Maintain turn state {label} must be an object or null")
        return value

    def _write_turn_state(self, session_id: str, value: Mapping[str, Any]) -> None:
        session_directory = self._turn_state_session_directory(session_id)
        path = self._turn_state_path(session_id)
        try:
            # 공통 런타임의 경로 검증·잠금·원자적 쓰기를 함께 적용한다.
            # Claude의 보조 상태에도 동일한 파일 쓰기 경계를 유지한다.
            with self.adapter.store._state_lock(session_directory):
                _atomic_write_json(path, value)
        except OSError as exc:
            raise HarnessError(
                f"Claude Maintain turn state could not be saved: {exc}"
            ) from exc

    def session_start(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        if self._is_subagent_payload(payload):
            return _hook_output("SessionStart")
        normalized = self._base_payload(payload, "session-start")
        self._write_session_environment(normalized["session_id"])
        return self.adapter.session_start(normalized)

    def user_prompt(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        if self._is_subagent_payload(payload):
            return _hook_output("UserPromptSubmit")
        normalized = self._base_payload(payload, "user-prompt")
        session_id = normalized["session_id"]
        normalized["prompt"] = self._payload_string(payload, "prompt")
        if self.adapter.status(session_id)["status"] != "active":
            return _hook_output("UserPromptSubmit")

        state = self._read_turn_state(session_id)
        pending = state.get("pending") if state else None
        if pending and pending.get("prompt") == normalized["prompt"]:
            turn_id = expect_nonempty_string(
                pending.get("turn_id"), "Claude Maintain pending turn id"
            )
        else:
            turn_id = str(uuid.uuid4())
        normalized["turn_id"] = turn_id
        output = self.adapter.user_prompt(normalized)
        self._write_turn_state(
            session_id,
            {
                "schema_version": _TURN_STATE_SCHEMA_VERSION,
                "pending": {"turn_id": turn_id, "prompt": normalized["prompt"]},
                "last_stop": None,
            },
        )
        return output

    def response_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        if self._is_subagent_payload(payload):
            return _hook_output("Stop")
        if payload.get("stop_hook_active"):
            return _hook_output("Stop")
        normalized = self._base_payload(payload, "response-end")
        session_id = normalized["session_id"]
        normalized["last_assistant_message"] = self._payload_string(
            payload, "last_assistant_message"
        )
        normalized["stop_hook_active"] = bool(payload.get("stop_hook_active", False))
        # 이미 접수된 turn은 연결 해제 이후에도 원래 binding을 유지한다.

        state = self._read_turn_state(session_id)
        pending = state.get("pending") if state else None
        last_stop = state.get("last_stop") if state else None
        if pending is not None:
            turn_id = expect_nonempty_string(
                pending.get("turn_id"), "Claude Maintain pending turn id"
            )
        elif (
            last_stop is not None
            and last_stop.get("last_assistant_message")
            == normalized["last_assistant_message"]
        ):
            turn_id = expect_nonempty_string(
                last_stop.get("turn_id"), "Claude Maintain stopped turn id"
            )
        else:
            # prompt가 미연결 상태였으면 turn 중간의 activation을 늦은 응답에 소급하지 않는다.
            return _hook_output("Stop")

        normalized["turn_id"] = turn_id
        output = self.adapter.response_end(normalized)
        self._write_turn_state(
            session_id,
            {
                "schema_version": _TURN_STATE_SCHEMA_VERSION,
                "pending": None,
                "last_stop": {
                    "turn_id": turn_id,
                    "last_assistant_message": normalized["last_assistant_message"],
                },
            },
        )
        return output

    def session_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        if self._is_subagent_payload(payload):
            return _hook_output("SessionEnd")
        return self.adapter.session_end(self._base_payload(payload, "session-end"))

    def control(
        self, command: str, *, workspace_id: str | None, session_id: str | None
    ) -> dict[str, Any]:
        if command not in _CONTROL_COMMANDS:
            fail(f"unsupported Claude Maintain control command: {command}")
        selected_session_id = (
            session_id
            if session_id is not None
            else self.environ.get(_CLAUDE_SESSION_ENV)
        )
        selected_session_id = expect_nonempty_string(
            selected_session_id, f"{_CLAUDE_SESSION_ENV} or --session-id"
        )
        if command == "activate":
            if not workspace_id:
                fail("activate requires a Workspace id")
            return self.adapter.activate(selected_session_id, workspace_id)
        if workspace_id:
            fail(f"{command} does not accept a Workspace id")
        if command == "deactivate":
            return self.adapter.deactivate(selected_session_id)
        return self.adapter.status(selected_session_id)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Claude Maintain adapter")
    parser.add_argument(
        "command",
        choices=(*_HOOK_EVENTS, *_CONTROL_COMMANDS, "drain"),
    )
    parser.add_argument("workspace_id", nargs="?")
    parser.add_argument("--session-id")
    parser.add_argument("--project-root")
    parser.add_argument("--runtime-root")
    parser.add_argument("--config-path")
    parser.add_argument("--session-key")
    return parser


def main(
    argv: list[str] | None = None,
    *,
    project_root: Path | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    environ: Mapping[str, str] | None = None,
) -> int:
    arguments = _parser().parse_args(argv)
    output_stream = stdout or sys.stdout
    root = project_root or (
        Path(arguments.project_root)
        if arguments.project_root
        else Path(__file__).resolve().parents[5]
    )
    try:
        if arguments.command == "drain":
            if (
                not arguments.session_key
                or not arguments.runtime_root
                or not arguments.config_path
            ):
                fail("drain requires --session-key, --runtime-root and --config-path")
            if arguments.workspace_id or arguments.session_id:
                fail("drain does not accept session or Workspace control options")
            runtime = MaintainRuntime(
                root,
                runtime_root=Path(arguments.runtime_root),
                config_path=Path(arguments.config_path),
                worker_module="context.work.harness.maintain.adapters.claude",
                session_type=CodexMaintainSession,
            )
            print(
                json.dumps(runtime.drain(arguments.session_key), ensure_ascii=False),
                file=output_stream,
            )
            return 0
        if arguments.runtime_root or arguments.config_path or arguments.session_key:
            fail("runtime options are only valid for drain")
        adapter = ClaudeHookAdapter(root, environ=environ)
        if arguments.command in _CONTROL_COMMANDS:
            output = adapter.control(
                arguments.command,
                workspace_id=arguments.workspace_id,
                session_id=arguments.session_id,
            )
        else:
            if arguments.workspace_id or arguments.session_id:
                fail("hook commands do not accept session control options")
            try:
                payload = json.load(stdin or sys.stdin)
            except json.JSONDecodeError as exc:
                raise HarnessError(
                    f"Claude hook stdin is not valid JSON: {exc}"
                ) from exc
            handlers = {
                "session-start": adapter.session_start,
                "user-prompt": adapter.user_prompt,
                "response-end": adapter.response_end,
                "session-end": adapter.session_end,
            }
            output = handlers[arguments.command](payload)
        print(
            json.dumps(output, ensure_ascii=False, sort_keys=True), file=output_stream
        )
        return 0
    except (HarnessError, OSError, ValueError) as exc:
        if arguments.command in {*_CONTROL_COMMANDS, "drain"}:
            print(f"Claude Maintain {arguments.command} failed: {exc}", file=sys.stderr)
            return 2
        event_name = _HOOK_EVENTS[arguments.command]
        message = (
            f"Claude Workspace Maintain {arguments.command} failed: {exc}. "
            "No success, freshness, or completion is claimed."
        )
        # 한국어: 해당 Claude Workspace Maintain 명령에 실패했다: {exc}.
        # 성공·최신성·완료를 주장하지 않는다.
        print(
            json.dumps(
                _hook_output(
                    event_name,
                    additional_context=message,
                    system_message=message,
                ),
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=output_stream,
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
