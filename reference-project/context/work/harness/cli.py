"""Command-line routing for the recover and verify responsibilities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .recover import build_recovery_packet, render_recovery_packet
from .verify import verify_workspace
from .workspace_contract import HarnessError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recover or verify a bounded Project Workspace"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    recover_parser = subparsers.add_parser(
        "recover", help="print the active Workspace recovery packet"
    )
    recover_parser.add_argument("workspace_id", nargs="?")
    recover_parser.add_argument(
        "--json", action="store_true", dest="as_json", help="emit JSON"
    )

    verify_parser = subparsers.add_parser(
        "verify", help="run the Workspace's fixed verification argv"
    )
    verify_parser.add_argument("workspace_id", nargs="?")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _build_parser().parse_args(argv)
    harness_root = Path(__file__).resolve().parent
    work_root = harness_root.parent
    project_root = work_root.parent.parent
    try:
        if arguments.command == "recover":
            packet = build_recovery_packet(
                project_root, work_root, arguments.workspace_id
            )
            if arguments.as_json:
                print(json.dumps(packet, ensure_ascii=False, indent=2))
            else:
                print(render_recovery_packet(packet), end="")
            return 0

        exit_code, summary = verify_workspace(
            project_root, work_root, arguments.workspace_id
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return exit_code
    except HarnessError as exc:
        print(f"workspace harness error: {exc}", file=sys.stderr)
        return 2
