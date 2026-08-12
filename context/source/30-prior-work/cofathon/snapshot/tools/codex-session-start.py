#!/usr/bin/env python3
"""Inject the appropriate Cofathon re-entry contract into Codex context."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
INSTRUCTIONS_FILE = ROOT / "CLAUDE.md"
START_HEADING_PREFIX = "## 매 세션 시작 시"
AUDIT_FILE = ROOT / "logs" / "codex" / "session-start-hooks.jsonl"
REENTRY_FILES = (
    ROOT / "context" / "current.md",
    ROOT / "context" / "goal.md",
    ROOT / "context" / "core" / "README.md",
)

MAIN_HEADER = """[COFATHON_SESSION_START_V2]
아래 내용은 Codex SessionStart 훅이 다시 전달한 CLAUDE.md의 세션 시작 지시다.
문단의 지시를 그대로 수행하라."""

COMPACT_CONTEXT = """[COFATHON_CONTEXT_REFRESH_V2]
자동 context compact 뒤의 기준 복원이다. 진행 중인 사용자 요청을 보존하고 계속하라.
실질 작업을 잇기 전에 아래 세 문서를 최신 상태로 다시 확인하라.
- context/current.md
- context/goal.md
- context/core/README.md
시작 복기를 새 final 응답으로 반복하거나 사용자 재확인을 요구하며 멈추지 않는다.
지도와 실제 상태가 어긋나면 차이를 밝히고 실제 상태를 확인한 뒤 지도를 고친다."""


def read_hook_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"codex-session-start: invalid hook input: {exc}", file=sys.stderr)
        return {}
    if not isinstance(payload, dict):
        print("codex-session-start: hook input is not an object", file=sys.stderr)
        return {}
    return payload


def read_start_section() -> str:
    lines = INSTRUCTIONS_FILE.read_text(encoding="utf-8").splitlines()
    start = next(
        index
        for index, line in enumerate(lines)
        if line.startswith(START_HEADING_PREFIX)
    )
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    return "\n".join(lines[start:end]).strip()


def file_snapshot(path: Path) -> dict:
    relative_path = str(path.relative_to(ROOT))
    try:
        data = path.read_bytes()
    except OSError as exc:
        return {"path": relative_path, "error": str(exc)}
    return {
        "path": relative_path,
        "bytes": len(data),
        "sha256": sha256(data).hexdigest(),
    }


def append_audit(
    payload: dict,
    source: str,
    mode: str,
    section: str,
    additional_context: str,
) -> None:
    session_id = payload.get("session_id") or payload.get("sessionId")
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id if isinstance(session_id, str) else None,
        "source": source,
        "mode": mode,
        "cwd": payload.get("cwd") if isinstance(payload.get("cwd"), str) else None,
        "reentry_section_sha256": sha256(section.encode("utf-8")).hexdigest(),
        "additional_context_sha256": sha256(
            additional_context.encode("utf-8")
        ).hexdigest(),
        "targets": [file_snapshot(path) for path in REENTRY_FILES],
    }
    try:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT_FILE.open("a", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
    except OSError as exc:
        print(f"codex-session-start: audit write failed: {exc}", file=sys.stderr)


def main() -> int:
    payload = read_hook_input()
    raw_source = payload.get("source")
    source = raw_source if isinstance(raw_source, str) and raw_source else "startup"

    try:
        section = read_start_section()
    except (OSError, StopIteration) as exc:
        print(f"codex-session-start: {exc}", file=sys.stderr)
        section = "[CLAUDE.md의 세션 시작 문단 로드 실패]"

    if source == "compact":
        mode = "compact_refresh"
        additional_context = COMPACT_CONTEXT
    else:
        mode = "main_reentry"
        additional_context = (
            f"{MAIN_HEADER}\n\n"
            "--- CLAUDE.md / 매 세션 시작 시 ---\n"
            f"{section}"
        )

    append_audit(payload, source, mode, section, additional_context)
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": additional_context,
            }
        },
        sys.stdout,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
