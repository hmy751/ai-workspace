"""Maintain의 구성과 공개 동작. 하위 서비스가 각 책임을 소유한다."""

from __future__ import annotations

from pathlib import Path
from collections.abc import Callable, Mapping
from typing import Any
import subprocess
import sys
import time

from ...workspace_contract import HarnessError, fail, expect_nonempty_string
from ..bootstrap import bootstrap_workspace
from ..apply.service import apply_maintain_decision
from ..semantic.session import SemanticSessionFactory
from .context import RuntimeContext
from .storage import RuntimeStore
from .notices import NoticeService
from .binding import BindingService
from .status import StatusReader
from .events import EventIntake
from .worker import DrainWorker


class MaintainRuntime:
    """도구별 연결에서 전달한 의존성으로 공통 Maintain 흐름을 구성한다."""

    def __init__(
        self,
        project_root: Path,
        *,
        runtime_root: Path,
        config_path: Path,
        worker_module: str,
        session_type: SemanticSessionFactory,
        runner: Callable[..., Any] = subprocess.run,
        popen: Callable[..., Any] = subprocess.Popen,
        clock: Callable[[], float] = time.time,
        python_executable: str = sys.executable,
        bootstrap: Callable[..., Any] = bootstrap_workspace,
        apply_decision: Callable[..., Any] = apply_maintain_decision,
    ) -> None:
        lexical_project_root = Path(project_root)
        if not lexical_project_root.is_absolute():
            lexical_project_root = Path.cwd() / lexical_project_root
        try:
            self.project_root = lexical_project_root.resolve(strict=True)
        except OSError as exc:
            raise HarnessError(f"Project root is unavailable: {exc}") from exc
        if not self.project_root.is_dir():
            fail("Project root must be a directory")
        self.work_root = self.project_root / "context" / "work"
        runtime_candidate = Path(runtime_root)
        if not runtime_candidate.is_absolute():
            fail("Maintain runtime root must be an absolute path")
        if ".." in runtime_candidate.parts:
            fail("Maintain runtime root must not contain ancestor traversal")
        relative_runtime: Path | None = None
        for project_form in (lexical_project_root, self.project_root):
            try:
                relative_runtime = runtime_candidate.relative_to(project_form)
                break
            except ValueError:
                continue
        if relative_runtime is None:
            fail("Maintain runtime root must be inside the Project root")
        if not relative_runtime.parts:
            fail("Maintain runtime root must be below the Project root")
        # Project의 OS 별칭만 해석하고 하위 runtime의 symlink 검사는 유지한다.
        self.runtime_root = self.project_root / relative_runtime
        config_candidate = Path(config_path)
        for project_form in (lexical_project_root, self.project_root):
            try:
                relative_config = config_candidate.relative_to(project_form)
                break
            except ValueError:
                continue
        else:
            fail("Maintain configuration must stay inside the Project root")
        if ".." in relative_config.parts or not relative_config.parts:
            fail("Maintain configuration must be a lexical Project descendant")
        config_path = self.project_root / relative_config

        self.context = RuntimeContext(
            project_root=self.project_root,
            work_root=self.work_root,
            runtime_root=self.runtime_root,
            config_path=config_path,
            worker_module=worker_module,
            session_type=session_type,
            runner=runner,
            popen=popen,
            clock=clock,
            python_executable=expect_nonempty_string(
                python_executable, "Python executable"
            ),
            bootstrap=bootstrap,
            apply_decision=apply_decision,
        )
        self.store = RuntimeStore(self.context)
        self.store._validate_runtime_path(self.runtime_root, "Maintain runtime root")
        self.notices = NoticeService(self.context)
        self.bindings = BindingService(self.context, self.notices, self.store)
        self.status_reader = StatusReader(self.context, self.store)
        self.worker = DrainWorker(self.context, self.notices, self.store)
        self.events = EventIntake(self.context, self.notices, self.store, self.worker)

    def activate(self, session_id: str, workspace_id: str) -> dict[str, Any]:
        return self.bindings.activate(session_id, workspace_id)

    def deactivate(self, session_id: str) -> dict[str, Any]:
        return self.bindings.deactivate(session_id)

    def status(self, session_id: str) -> dict[str, Any]:
        return self.status_reader.status(session_id)

    def session_start(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return self.events.session_start(payload)

    def user_prompt(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return self.events.user_prompt(payload)

    def response_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return self.events.response_end(payload)

    def session_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return self.events.session_end(payload)

    def drain(self, session_key: str) -> dict[str, Any]:
        return self.worker.drain(session_key)
