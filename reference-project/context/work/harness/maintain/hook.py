"""Codex hook and detached worker entrypoint for Reference Maintain."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Protocol

if __package__ in {None, ""}:
    # Direct execution is supported for a thin Project hook command. The
    # reusable package still remains under the target Project root.
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from context.work.harness.maintain.config import (
    MaintainConfig,
    load_config,
)
from context.work.harness.maintain.controller import MaintainController
from context.work.harness.maintain.runner import CHILD_ENVIRONMENT_VARIABLE


HOOK_EVENTS = frozenset(
    {"SessionStart", "UserPromptSubmit", "PostToolUse", "Stop"}
)


class ControllerLike(Protocol):
    def session_start(self, payload: object) -> object: ...

    def capture_user_prompt(self, payload: object) -> dict[str, Any]: ...

    def capture_stop(self, payload: object) -> dict[str, Any]: ...

    def capture_post_tool_use(self, payload: object) -> dict[str, Any]: ...

    def take_pending_notice(self, session_id: str) -> object: ...

    def acknowledge_notice(
        self, session_id: str, report_ids: tuple[str, ...]
    ) -> tuple[str, ...]: ...

    def acknowledge_workspace_notice(
        self,
        recipient_session_id: str,
        report_acks: tuple[tuple[str, str], ...],
    ) -> tuple[tuple[str, str], ...]: ...

    def process_session(self, session_id: str) -> dict[str, Any]: ...

    def next_runnable_session_id(self) -> str | None: ...

    def repair_missing_stop_gap(
        self,
        session_id: str,
        expected_sequence: int,
        *,
        approved_by: str,
        reason: str,
    ) -> dict[str, Any]: ...

    def status(self, session_id: str | None = None) -> dict[str, Any]: ...


Spawner = Callable[[Path, str], None]


@dataclass(frozen=True)
class HookExecution:
    """Official hook output plus internal post-flush acknowledgement data."""

    output: dict[str, Any]
    session_id: str | None = None
    report_ids: tuple[str, ...] = ()
    workspace_report_acks: tuple[tuple[str, str], ...] = ()


def hook_output(
    event_name: str,
    *,
    additional_context: str | None = None,
    system_message: str | None = None,
) -> dict[str, Any]:
    """Return only official common fields and hook-specific context."""

    output: dict[str, Any] = {"continue": True}
    if system_message:
        output["systemMessage"] = system_message
    if additional_context:
        output["hookSpecificOutput"] = {
            "hookEventName": event_name,
            "additionalContext": additional_context,
        }
    return output


def handle_hook(
    event_name: str,
    payload: object,
    controller: ControllerLike,
    *,
    config_path: Path,
    spawner: Spawner,
    environment: Mapping[str, str] | None = None,
) -> HookExecution:
    """Capture quickly, inject pending notices, and fail open at the boundary."""

    environment = os.environ if environment is None else environment
    if environment.get(CHILD_ENVIRONMENT_VARIABLE):
        return HookExecution(hook_output(event_name))
    if event_name not in HOOK_EVENTS:
        return HookExecution(
            hook_output(
                event_name,
                system_message="Maintain이 지원하지 않는 hook event를 무시했습니다.",
            )
        )

    try:
        if event_name == "SessionStart":
            session_id = _session_id(payload)
            result = controller.session_start(payload)
            recovery_session_id = controller.next_runnable_session_id()
            if recovery_session_id is not None:
                spawner(config_path, recovery_session_id)
            notice = getattr(result, "notice", None)
            start_context = None
            if bool(getattr(result, "grounded_now", False)):
                summary = getattr(result, "summary", None)
                if isinstance(summary, str) and summary:
                    status = (
                        "초기 동기화가 끝났습니다"
                        if bool(getattr(result, "freshness_ready", True))
                        else "초기 방향은 읽었지만 이전 세션 처리가 남아 있습니다"
                    )
                    start_context = (
                        f"Maintain {status}. Main의 첫 commentary에서 다음 "
                        f"시작 상태를 한 문장으로 보여주세요: {summary}"
                    )
            return HookExecution(
                hook_output(
                    event_name,
                    additional_context=_join_contexts(
                        start_context,
                        getattr(notice, "additional_context", None),
                    ),
                    system_message=getattr(notice, "system_message", None),
                ),
                session_id=session_id,
                workspace_report_acks=tuple(
                    getattr(notice, "workspace_report_acks", ())
                ),
            )

        session_id = _session_id(payload)
        if event_name == "PostToolUse":
            capture = controller.capture_post_tool_use(payload)
            # This hook is a synchronous bounded capture only. The semantic
            # worker starts at a response boundary, never after each tool.
            return HookExecution(
                hook_output(
                    event_name,
                    system_message=_capture_warning(capture),
                )
            )
        if event_name == "UserPromptSubmit":
            capture = controller.capture_user_prompt(payload)
            notice = controller.take_pending_notice(session_id)
            spawner(config_path, session_id)
            warning = _capture_warning(capture)
            notice_system = getattr(notice, "system_message", None)
            return HookExecution(
                hook_output(
                    event_name,
                    additional_context=getattr(
                        notice, "additional_context", None
                    ),
                    system_message=_join_messages(notice_system, warning),
                ),
                session_id=session_id,
                report_ids=tuple(getattr(notice, "report_ids", ())),
                workspace_report_acks=tuple(
                    getattr(notice, "workspace_report_acks", ())
                ),
            )

        capture = controller.capture_stop(payload)
        spawner(config_path, session_id)
        return HookExecution(
            hook_output(
                event_name,
                system_message=_capture_warning(capture),
            )
        )
    except Exception:
        # Raw payloads and exception strings can contain conversation content;
        # neither is returned or written by this fail-open adapter.
        if event_name == "SessionStart":
            message = (
                "Maintain 초기 동기화를 완료하지 못했습니다. Main이 선택한 "
                "Workspace current를 직접 확인해 시작 상태를 맞추세요."
            )
        else:
            message = (
                "Maintain hook이 처리되지 않았습니다. Main 작업은 계속하며 "
                "status에서 freshness를 확인할 수 있습니다."
            )
        return HookExecution(
            hook_output(
                event_name,
                system_message=message,
                additional_context=_manual_grounding_context()
                if event_name == "SessionStart"
                else None,
            )
        )


def spawn_worker(
    config_path: Path,
    session_id: str,
    *,
    popen: Callable[..., subprocess.Popen[Any]] = subprocess.Popen,
) -> None:
    """Start a content-silent worker without waiting for semantic completion."""

    environment = os.environ.copy()
    environment[CHILD_ENVIRONMENT_VARIABLE] = "1"
    project_root = _target_project_root(config_path)
    popen(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--config",
            str(config_path),
            "worker",
            "--session-id",
            session_id,
        ],
        cwd=project_root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
        env=environment,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="context-maintain")
    parser.add_argument("--config", required=True)
    commands = parser.add_subparsers(dest="command", required=True)

    hook = commands.add_parser("hook")
    hook.add_argument("event", choices=sorted(HOOK_EVENTS))

    worker = commands.add_parser("worker")
    worker.add_argument("--session-id", required=True)

    status = commands.add_parser("status")
    status.add_argument("--session-id")

    repair = commands.add_parser("repair-gap")
    repair.add_argument("--session-id", required=True)
    repair.add_argument("--expected-sequence", required=True, type=int)
    repair.add_argument("--approved-by", required=True)
    repair.add_argument("--reason", required=True)
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    controller_factory: Callable[[MaintainConfig], ControllerLike] = MaintainController,
    spawner: Spawner = spawn_worker,
) -> int:
    args = build_parser().parse_args(argv)

    if (
        args.command == "hook"
        and os.environ.get(CHILD_ENVIRONMENT_VARIABLE)
    ):
        print(json.dumps(hook_output(args.event), sort_keys=True))
        return 0

    if args.command == "hook":
        try:
            payload = json.loads(sys.stdin.read())
        except (UnicodeError, json.JSONDecodeError):
            print(
                json.dumps(
                    hook_output(
                        args.event,
                        system_message="Maintain이 잘못된 hook JSON을 무시했습니다.",
                    ),
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 0
        try:
            config = load_config(args.config)
            controller = controller_factory(config)
            execution = handle_hook(
                args.event,
                payload,
                controller,
                config_path=config.config_path,
                spawner=spawner,
            )
        except Exception:
            if args.event == "SessionStart":
                message = (
                    "Maintain 설정 또는 초기 동기화에 실패했습니다. Main이 "
                    "선택한 Workspace current를 직접 확인해 시작 상태를 맞추세요."
                )
            else:
                message = (
                    "Maintain 설정 또는 hook 초기화에 실패했습니다. "
                    "Main 작업은 계속합니다."
                )
            execution = HookExecution(
                hook_output(
                    args.event,
                    system_message=message,
                    additional_context=_manual_grounding_context()
                    if args.event == "SessionStart"
                    else None,
                )
            )
        print(
            json.dumps(execution.output, ensure_ascii=False, sort_keys=True),
            flush=True,
        )
        if execution.session_id is not None and execution.report_ids:
            try:
                controller.acknowledge_notice(
                    execution.session_id, execution.report_ids
                )
            except Exception:
                # Delivery already succeeded. Leaving a report pending causes a
                # bounded duplicate later, which is safer than premature loss.
                pass
        if execution.workspace_report_acks:
            try:
                controller.acknowledge_workspace_notice(
                    execution.session_id or "",
                    execution.workspace_report_acks,
                )
            except Exception:
                # The prior-session report remains available for a bounded
                # duplicate at the next safe delivery point.
                pass
        return 0

    try:
        config = load_config(args.config)
        controller = controller_factory(config)
    except Exception:
        print(json.dumps({"error": "invalid_maintain_config"}, sort_keys=True))
        return 2

    if args.command == "worker":
        try:
            result = controller.process_session(args.session_id)
        except Exception:
            return 1
        try:
            next_session_id = controller.next_runnable_session_id()
            if next_session_id is None and result.get("successor_required") is True:
                next_session_id = args.session_id
            if next_session_id is not None:
                spawner(config.config_path, next_session_id)
        except Exception:
            return 1
        # A detached caller may not inspect stderr, but the process exit still
        # must not describe retryable or structurally blocked work as success.
        return (
            0
            if result.get("status")
            in {"idle", "busy", "already_processed", "processed"}
            else 1
        )

    if args.command == "repair-gap":
        try:
            repaired = controller.repair_missing_stop_gap(
                args.session_id,
                args.expected_sequence,
                approved_by=args.approved_by,
                reason=args.reason,
            )
        except Exception:
            print(json.dumps({"error": "gap_repair_rejected"}, sort_keys=True))
            return 2
        print(json.dumps(repaired, ensure_ascii=False, sort_keys=True))
        return 0

    print(
        json.dumps(
            controller.status(args.session_id),
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


def _session_id(payload: object) -> str:
    if not isinstance(payload, Mapping):
        raise ValueError("hook payload must be an object")
    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("session_id must be a non-empty string")
    return session_id


def _capture_warning(capture: Mapping[str, Any]) -> str | None:
    if capture.get("conflict"):
        return "Maintain 전달 증거가 기존 event와 충돌해 반영하지 않았습니다."
    if capture.get("malformed"):
        return "Maintain 전달 증거가 손상되어 반영하지 않았습니다."
    return None


def _manual_grounding_context() -> str:
    return (
        "Maintain 초기 동기화가 실패했습니다. Main은 첫 작업 전에 선택한 "
        "Workspace의 README와 current index, index가 고른 current 문서, "
        "output/index.md를 좁게 읽고 목표, 현재 상태, 다음 행동을 맞추세요."
    )


def _join_messages(*messages: object) -> str | None:
    values = [
        message.strip()
        for message in messages
        if isinstance(message, str) and message.strip()
    ]
    return " ".join(values) or None


def _join_contexts(*messages: object) -> str | None:
    values = [
        message.strip()
        for message in messages
        if isinstance(message, str) and message.strip()
    ]
    return "\n\n".join(values) or None


def _target_project_root(config_path: Path) -> Path:
    resolved = config_path.resolve(strict=False)
    codex_directory = next(
        (parent for parent in resolved.parents if parent.name == ".codex"),
        None,
    )
    if codex_directory is None:
        raise ValueError("config path is not below a .codex directory")
    return codex_directory.parent


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "HOOK_EVENTS",
    "HookExecution",
    "build_parser",
    "handle_hook",
    "hook_output",
    "main",
    "spawn_worker",
]
