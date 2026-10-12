"""세 Harness 책임의 CLI 입력을 해석하고 해당 공개 동작으로 연결한다."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .maintain import apply_maintain_decision, bootstrap_workspace
from .recover import build_recovery_packet, render_recovery_packet
from .verify import verify_workspace
from .workspace.validation import HarnessError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Recover a Workspace, guard a Maintain decision, or record "
            "bounded verification evidence"
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    recover_parser = subparsers.add_parser(
        "recover", help="print an explicit or active-default recovery packet"
    )
    recover_parser.add_argument("workspace_id", nargs="?")
    recover_parser.add_argument(
        "--json", action="store_true", dest="as_json", help="emit JSON"
    )

    maintain_parser = subparsers.add_parser(
        "maintain",
        help="build semantic-agent grounding or guard a proposed decision",
    )
    maintain_actions = maintain_parser.add_subparsers(
        dest="maintain_action", required=True
    )
    bootstrap_parser = maintain_actions.add_parser(
        "bootstrap", help="build one explicit bounded grounding packet"
    )
    bootstrap_parser.add_argument("workspace_id")
    bootstrap_parser.add_argument(
        "--json", action="store_true", dest="as_json", help="emit JSON"
    )
    apply_parser = maintain_actions.add_parser(
        "apply", help="validate and apply one structured Maintain decision"
    )
    apply_parser.add_argument("workspace_id")
    apply_parser.add_argument(
        "decision",
        help="JSON decision file, or '-' to read the decision from stdin",
    )

    verify_parser = subparsers.add_parser(
        "verify", help="record evidence for the Workspace's fixed claim and argv"
    )
    verify_parser.add_argument("workspace_id", nargs="?")
    return parser


def _print_packet(packet: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
    else:
        print(render_recovery_packet(packet), end="")


def _read_maintain_decision(source: str) -> Any:
    """CLI가 받은 파일 또는 stdin만 읽고, 적용 가능성은 Maintain에 맡긴다."""

    if source == "-":
        raw_decision = sys.stdin.read()
        label = "stdin Maintain decision"
    else:
        path = Path(source)
        label = f"Maintain decision {path}"
        try:
            raw_decision = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise HarnessError(f"{label} is not readable UTF-8 JSON: {exc}") from exc
    try:
        return json.loads(raw_decision)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"{label} is not valid JSON: {exc}") from exc


def _run_maintain(
    arguments: argparse.Namespace, project_root: Path, work_root: Path
) -> int:
    if arguments.maintain_action == "bootstrap":
        packet = bootstrap_workspace(project_root, work_root, arguments.workspace_id)
        _print_packet(packet, as_json=arguments.as_json)
    else:
        decision = _read_maintain_decision(arguments.decision)
        result = apply_maintain_decision(
            project_root, work_root, arguments.workspace_id, decision
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = _build_parser().parse_args(argv)
    work_root = Path(__file__).resolve().parent.parent
    project_root = work_root.parent.parent

    try:
        if arguments.command == "recover":
            packet = build_recovery_packet(
                project_root, work_root, arguments.workspace_id
            )
            _print_packet(packet, as_json=arguments.as_json)
            return 0

        if arguments.command == "maintain":
            return _run_maintain(arguments, project_root, work_root)

        exit_code, summary = verify_workspace(
            project_root, work_root, arguments.workspace_id
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return exit_code
    except HarnessError as exc:
        print(f"workspace harness error: {exc}", file=sys.stderr)
        return 2
