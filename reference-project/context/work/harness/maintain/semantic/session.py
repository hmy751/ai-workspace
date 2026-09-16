"""판단 세션에 필요한 최소 동작. 실행 도구의 명령 형식은 노출하지 않는다."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Protocol


class SemanticSession(Protocol):
    """한 Workspace에 초기 맥락을 구성하고 같은 이해로 후속 판단을 수행한다."""

    @property
    def thread_id(self) -> str | None: ...

    def start(self, bounded_bootstrap: Mapping[str, Any]) -> dict[str, Any]: ...

    def resume(self, bounded_response_delta: Mapping[str, Any]) -> dict[str, Any]: ...


class SemanticSessionFactory(Protocol):
    """새 세션 생성과 저장된 세션 복원에 필요한 의존성."""

    def __call__(
        self, project_root: Path, workspace_id: str, *, runner: Callable[..., Any]
    ) -> SemanticSession: ...

    def restore(
        self,
        project_root: Path,
        workspace_id: str,
        *,
        thread_id: str,
        runner: Callable[..., Any],
    ) -> SemanticSession: ...
