"""Codex hook·CLI 입력과 session 선택을 공통 runtime에 연결한다."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

from ...workspace_contract import HarnessError, expect_nonempty_string, fail
from ..host_adapter import MaintainHostAdapter
from ..runtime.state import _HOOK_EVENTS
from .events import _hook_output


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
            "activate",
            "deactivate",
            "status",
            "session-start",
            "user-prompt",
            "response-end",
            "session-end",
            "drain",
        ),
    )
    parser.add_argument(
        "control_value",
        nargs="?",
        help="Workspace id for positional 'activate WORKSPACE_ID'",
    )
    parser.add_argument("--project-root")
    parser.add_argument("--runtime-root")
    parser.add_argument("--config-path")
    parser.add_argument("--session-key")
    parser.add_argument("--session-id")
    parser.add_argument("--workspace-id")
    return parser


def _stdin_payload() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"Codex hook stdin is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        fail("Codex hook stdin must contain a JSON object")
    return value


def _control_session_id(explicit_session_id: str | None) -> str:
    candidate = (
        explicit_session_id
        if explicit_session_id is not None
        else os.environ.get("CODEX_SESSION_ID")
    )
    if candidate is None:
        fail("Maintain control command requires --session-id or " "CODEX_SESSION_ID")
    return expect_nonempty_string(candidate, "Codex session id")


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        payload: dict[str, Any] | None = None
        is_hook_command = arguments.command in _HOOK_EVENTS
        if arguments.project_root:
            project_root = Path(arguments.project_root)
        elif arguments.command == "drain":
            fail("drain requires --project-root")
        elif is_hook_command:
            payload = _stdin_payload()
            project_root = _discover_project_root(
                Path(str(payload.get("cwd", Path.cwd())))
            )
        else:
            project_root = _discover_project_root(Path.cwd())
        adapter = MaintainHostAdapter(
            project_root,
            config_path=Path(arguments.config_path) if arguments.config_path else None,
            runtime_root=(
                Path(arguments.runtime_root) if arguments.runtime_root else None
            ),
        )
        if arguments.command == "drain":
            if not arguments.session_key:
                fail("drain requires --session-key")
            if (
                arguments.control_value
                or arguments.session_id
                or arguments.workspace_id
            ):
                fail("drain does not accept session or Workspace control options")
            output = adapter.drain(arguments.session_key)
        elif arguments.command == "activate":
            if arguments.session_key:
                fail("--session-key is only valid for drain")
            if (
                arguments.workspace_id
                and arguments.control_value
                and arguments.workspace_id != arguments.control_value
            ):
                fail("activate received two different Workspace ids")
            workspace_id = arguments.workspace_id or arguments.control_value
            if not workspace_id:
                fail("activate requires WORKSPACE_ID or --workspace-id")
            output = adapter.activate(
                _control_session_id(arguments.session_id),
                workspace_id,
            )
        elif arguments.command == "deactivate":
            if (
                arguments.control_value
                or arguments.session_key
                or arguments.workspace_id
            ):
                fail("deactivate accepts only session selection options")
            output = adapter.deactivate(_control_session_id(arguments.session_id))
        elif arguments.command == "status":
            if (
                arguments.control_value
                or arguments.session_key
                or arguments.workspace_id
            ):
                fail("status accepts only session selection options")
            output = adapter.status(_control_session_id(arguments.session_id))
        else:
            if arguments.session_key:
                fail("--session-key is only valid for drain")
            if (
                arguments.control_value
                or arguments.session_id
                or arguments.workspace_id
            ):
                fail("hook commands do not accept session control options")
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
        if arguments.command in {"drain", "activate", "deactivate", "status"}:
            print(f"Maintain {arguments.command} failed: {exc}", file=sys.stderr)
            return 2
        event_name = _HOOK_EVENTS[arguments.command]
        message = (
            f"Workspace Maintain {arguments.command} failed: {exc}. "
            "No success, freshness, or completion is claimed."
        )
        # 한국어: 해당 Workspace Maintain 명령에 실패했다: {exc}.
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
            )
        )
        return 0
