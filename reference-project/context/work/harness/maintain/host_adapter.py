"""기존 Codex 호출 경로를 보존하는 연결. 공통 구현은 runtime이 소유한다."""

from pathlib import Path
from typing import Any

from .runtime.engine import MaintainRuntime
from .adapters.codex_session import CodexMaintainSession
from .semantic.session import SemanticSessionFactory


class MaintainHostAdapter(MaintainRuntime):
    """기존 Codex 기본값을 사용하는 호환 진입점."""

    def __init__(
        self,
        project_root: Path,
        *,
        runtime_root: Path | None = None,
        config_path: Path | None = None,
        session_type: SemanticSessionFactory | None = None,
        **options: Any,
    ) -> None:
        root = Path(project_root).absolute()
        super().__init__(
            project_root,
            runtime_root=(
                runtime_root
                if runtime_root is not None
                else root / ".codex" / "maintain-runtime"
            ),
            config_path=(
                config_path
                if config_path is not None
                else root / ".codex" / "maintain.json"
            ),
            worker_module="context.work.harness.maintain.host_adapter",
            session_type=session_type or CodexMaintainSession,
            **options,
        )


def main(argv: list[str] | None = None) -> int:
    from .adapters.codex import main as run

    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
