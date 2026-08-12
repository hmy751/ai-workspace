#!/usr/bin/env python3
"""Re-inject CLAUDE.md's session-start instructions into Codex context."""

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent.parent
INSTRUCTIONS_FILE = ROOT / "CLAUDE.md"
START_HEADING_PREFIX = "## 매 세션 시작 시"

HEADER = """[MYREALTRIP_SESSION_START_V3]
아래 내용은 Codex SessionStart 훅이 다시 전달한 CLAUDE.md의 세션 시작 지시다.
문단의 지시를 그대로 수행하라."""


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


def main() -> int:
    try:
        section = read_start_section()
    except (OSError, StopIteration) as exc:
        print(f"codex-session-start: {exc}", file=sys.stderr)
        section = "[CLAUDE.md의 세션 시작 문단 로드 실패]"

    additional_context = (
        f"{HEADER}\n\n"
        "--- CLAUDE.md / 매 세션 시작 시 ---\n"
        f"{section}"
    )
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
