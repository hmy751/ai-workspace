#!/usr/bin/env python3
"""Hook, status, and drain command line entrypoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from context_maintainer.config import RuntimeConfig
from context_maintainer.protocol import (
    ProtocolError,
    validate_session_start,
    validate_stop,
    validate_user_prompt,
)
from context_maintainer.store import RuntimeStore, git_fingerprint


def _repo_root(explicit: Optional[str]) -> Path:
    return Path(explicit).resolve() if explicit else Path(__file__).resolve().parents[2]


def _hook_output(*, warning: Optional[str] = None) -> Dict[str, Any]:
    output: Dict[str, Any] = {"continue": True}
    if warning:
        output["systemMessage"] = warning
    return output


def handle_hook(
    event_name: str,
    payload: Any,
    store: RuntimeStore,
    *,
    drain_after: bool = False,
) -> Dict[str, Any]:
    if os.environ.get("CODEX_CONTEXT_MAINTAINER_CHILD"):
        return _hook_output()
    try:
        if event_name == "SessionStart":
            store.accept_session_start(validate_session_start(payload))
        elif event_name == "UserPromptSubmit":
            normalized = validate_user_prompt(payload)
            store.accept_user_prompt(normalized, git_fingerprint(store.repo_root))
        elif event_name == "Stop":
            normalized = validate_stop(payload)
            store.accept_stop(normalized, git_fingerprint(store.repo_root))
            if drain_after:
                store.drain()
        else:
            raise ProtocolError(f"unsupported hook event: {event_name}")
    except ProtocolError as exc:
        store.record_malformed(event_name, payload, str(exc))
        return _hook_output(
            warning="Context maintainer ignored a malformed hook payload; inspect status."
        )
    except Exception as exc:  # Hook boundary must remain fail-open.
        try:
            store.record_failure(f"{event_name}:{type(exc).__name__}")
        except Exception:
            pass
        return _hook_output(
            warning="Context maintainer observe hook failed; inspect status."
        )
    return _hook_output()


def render_status(status: Dict[str, Any]) -> str:
    last_enqueued = status["last_enqueued"]
    last_enqueued_value = (
        last_enqueued["sequence"] if isinstance(last_enqueued, dict) else "none"
    )
    gap = status["gap"]
    return "\n".join(
        [
            f"mode: {status['mode']}",
            f"workspace: {status['workspace']['id']}",
            f"last enqueued: {last_enqueued_value}",
            f"last drained: {status['last_drained']['sequence']}",
            (
                "queue: "
                f"{status['queue']['count']} "
                f"(oldest age: {status['queue']['oldest_age_seconds']})"
            ),
            (
                "missing pairs: "
                f"{status['missing_pair']['count']} "
                f"(waiting stop: {status['missing_pair']['waiting_stop']}, "
                f"stop before user: {status['missing_pair']['stop_before_user']})"
            ),
            (
                f"gap: expected {gap['expected_sequence']}"
                if gap["present"]
                else "gap: none"
            ),
            f"malformed: {status['malformed']['total']} (current: {status['malformed']['current']})",
            f"duplicates: {status['duplicate']['total']}",
            f"conflicts: {status['conflict']['total']} (current: {status['conflict']['current']})",
            f"failures: {status['failure']['total']}",
            (
                f"queue scope: {status['proof_ceiling']['queue_scope']}; "
                "cross-session gap isolation: "
                f"{str(status['proof_ceiling']['cross_session_gap_isolation']).lower()}; "
                "manual gap recovery: "
                f"{str(status['proof_ceiling']['manual_gap_recovery']).lower()}"
            ),
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="context-maintainer")
    parser.add_argument("--repo-root", help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    hook = subparsers.add_parser("hook")
    hook.add_argument("event", choices=("SessionStart", "UserPromptSubmit", "Stop"))
    hook.add_argument("--drain", action="store_true")

    status = subparsers.add_parser("status")
    status.add_argument("--json", action="store_true")

    drain = subparsers.add_parser("drain")
    drain.add_argument("--once", action="store_true")
    drain.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = _repo_root(args.repo_root)
    try:
        store = RuntimeStore(repo_root, RuntimeConfig.for_repo(repo_root))
    except Exception:
        if args.command == "hook":
            print(json.dumps(_hook_output()))
            return 0
        raise

    if args.command == "hook":
        try:
            payload = json.loads(sys.stdin.read())
        except json.JSONDecodeError as exc:
            store.record_malformed(args.event, None, f"invalid_json:{exc.msg}")
            print(
                json.dumps(
                    _hook_output(
                        warning="Context maintainer ignored malformed hook JSON; inspect status."
                    )
                )
            )
            return 0
        print(json.dumps(handle_hook(args.event, payload, store, drain_after=args.drain)))
        return 0

    if args.command == "status":
        status_value = store.status()
        print(
            json.dumps(status_value, ensure_ascii=False, sort_keys=True)
            if args.json
            else render_status(status_value)
        )
        return 0

    result = store.drain(once=args.once)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"processed: {result['processed']}; "
            f"last drained: {result['last_drained']}; "
            f"blocked: {result['blocked'] or 'none'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
