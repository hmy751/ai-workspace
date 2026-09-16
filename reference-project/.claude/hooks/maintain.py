"""Claude Code의 프로젝트별 Maintain 진입점."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from context.work.harness.maintain.claude_hook import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(project_root=PROJECT_ROOT))
