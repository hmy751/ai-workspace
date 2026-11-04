"""Recover·Verify의 CLI 입력을 해석하고 해당 공개 동작으로 연결한다."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .recover import build_recovery_packet, render_recovery_packet
from .verify import verify_workspace
from .workspace.validation import HarnessError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=("Recover a Workspace or record " "bounded verification evidence")
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    recover_parser = subparsers.add_parser(
        "recover", help="print an explicit or active-default recovery packet"
    )
    recover_parser.add_argument("workspace_id", nargs="?")
    recover_parser.add_argument(
        "--json", action="store_true", dest="as_json", help="emit JSON"
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

        exit_code, summary = verify_workspace(
            project_root, work_root, arguments.workspace_id
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return exit_code
    except HarnessError as exc:
        print(f"workspace harness error: {exc}", file=sys.stderr)
        return 2
