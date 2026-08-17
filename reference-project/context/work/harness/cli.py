"""Command-line routing for Workspace recovery and evidence recording."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .recover import build_recovery_packet, render_recovery_packet
from .verify import record_evidence
from .workspace_contract import HarnessError, read_json_without_symlinks


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recover a selected Workspace or record bounded verification evidence"
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
        "verify", help="record evidence produced by an existing verification"
    )
    verify_parser.add_argument("workspace_id", nargs="?")
    verify_parser.add_argument(
        "--input-json",
        required=True,
        metavar="PATH|-",
        help="read an evidence payload from a Project-root-relative file or stdin",
    )
    return parser


def _read_stdin_json() -> dict[str, object]:
    try:
        raw = sys.stdin.read()
    except OSError as exc:
        raise HarnessError(f"Verify evidence stdin is not readable: {exc}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"Verify evidence stdin is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise HarnessError("Verify evidence stdin must contain a JSON object")
    return value


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

        payload = (
            _read_stdin_json()
            if arguments.input_json == "-"
            else read_json_without_symlinks(
                project_root,
                arguments.input_json,
                "Verify evidence input",
            )
        )
        summary = record_evidence(
            work_root, payload, arguments.workspace_id
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except HarnessError as exc:
        print(f"workspace harness error: {exc}", file=sys.stderr)
        return 2
