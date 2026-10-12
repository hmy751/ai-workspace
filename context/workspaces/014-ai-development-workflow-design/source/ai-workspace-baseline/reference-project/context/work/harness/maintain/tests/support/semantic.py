"""외부 모델·프로세스 없이 호출과 실패를 재현하는 test double."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from context.work.harness.workspace_contract import HarnessError


def no_change(workspace_id: str = "001-example") -> dict[str, object]:
    return {
        "schema_version": 1,
        "workspace_id": workspace_id,
        "outcome": "no_change",
        "importance": "none",
        "summary": "No durable Workspace Context change.",
        "changes": [],
        "evidence": ["This response only restated existing context."],
        "unresolved": [],
        "question": None,
    }


class FakeSemanticSession:
    starts: list[dict[str, Any]] = []
    restores: list[str] = []
    restore_bindings: list[tuple[str, str]] = []
    deltas: list[dict[str, Any]] = []
    decisions: list[dict[str, object]] = []
    resume_errors: list[Exception] = []

    @classmethod
    def reset(cls) -> None:
        cls.starts = []
        cls.restores = []
        cls.restore_bindings = []
        cls.deltas = []
        cls.decisions = []
        cls.resume_errors = []

    def __init__(
        self,
        project_root: Path,
        workspace_id: str,
        *,
        runner: object,
    ) -> None:
        self.project_root = project_root
        self.workspace_id = workspace_id
        self.runner = runner
        self.thread_id: str | None = None

    @classmethod
    def restore(
        cls,
        project_root: Path,
        workspace_id: str,
        *,
        thread_id: str,
        runner: object,
    ) -> "FakeSemanticSession":
        session = cls(project_root, workspace_id, runner=runner)
        session.thread_id = thread_id
        cls.restores.append(thread_id)
        cls.restore_bindings.append((workspace_id, thread_id))
        return session

    def start(self, bounded_bootstrap: dict[str, Any]) -> dict[str, object]:
        type(self).starts.append(bounded_bootstrap)
        self.thread_id = f"maintain-thread-{len(type(self).starts)}"
        return {
            "schema_version": 1,
            "workspace_id": self.workspace_id,
            "status": "grounded",
            "starting_state": "bounded fixture state",
            "unresolved": [],
            "question": None,
        }

    def resume(self, delta: dict[str, Any]) -> dict[str, object]:
        type(self).deltas.append(delta)
        if type(self).resume_errors:
            raise type(self).resume_errors.pop(0)
        if type(self).decisions:
            return type(self).decisions.pop(0)
        return no_change(self.workspace_id)


class FailingStartSession(FakeSemanticSession):
    def start(self, bounded_bootstrap: dict[str, Any]) -> dict[str, object]:
        raise HarnessError("grounding unavailable")


class FailingSecondWorkspaceSession(FakeSemanticSession):
    def start(self, bounded_bootstrap: dict[str, Any]) -> dict[str, object]:
        if self.workspace_id == "002-other":
            raise HarnessError("successor grounding unavailable")
        return super().start(bounded_bootstrap)


class AmbiguousStartSession(FakeSemanticSession):
    def start(self, bounded_bootstrap: dict[str, Any]) -> dict[str, object]:
        type(self).starts.append(bounded_bootstrap)
        self.thread_id = "uncommitted-ambiguous-thread"
        return {
            "schema_version": 1,
            "workspace_id": self.workspace_id,
            "status": "needs_user_decision",
            "starting_state": "The source authority is ambiguous.",
            "unresolved": ["source authority"],
            "question": "Which source is authoritative?",
        }


class RecordingPopen:
    def __init__(self) -> None:
        self.calls: list[tuple[list[str], dict[str, object]]] = []

    def __call__(self, command: list[str], **options: object) -> object:
        self.calls.append((command, options))
        return object()


class FailingPopen(RecordingPopen):
    def __call__(self, command: list[str], **options: object) -> object:
        self.calls.append((command, options))
        raise OSError("detached worker launch failed")


class IncrementingClock:
    def __init__(self) -> None:
        self.value = 1000.0

    def __call__(self) -> float:
        self.value += 1.0
        return self.value
