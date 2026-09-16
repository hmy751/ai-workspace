"""파일 반영 테스트의 결정 생성과 Workspace 관찰 도우미."""

from __future__ import annotations

import hashlib
from pathlib import Path

from context.work.harness.maintain import apply_maintain_decision
from context.work.harness.testing import WorkspaceFixture


class MaintainApplyFixture(WorkspaceFixture):
    include_verification_scenarios = False

    def decision(
        self,
        outcome: str,
        *,
        importance: str | None = None,
        changes: list[dict[str, object]] | None = None,
        question: str | None = None,
    ) -> dict[str, object]:
        if importance is None:
            importance = {
                "no_change": "none",
                "update": "quiet",
                "needs_user_decision": "important",
            }[outcome]
        return {
            "schema_version": 1,
            "workspace_id": "001-example",
            "outcome": outcome,
            "importance": importance,
            "summary": f"{outcome} fixture decision",
            "changes": changes or [],
            "evidence": ["fixture evidence"],
            "unresolved": [],
            "question": question,
        }

    def relative(self, relative_path: str) -> Path:
        return (
            self.work_root / "workspaces" / "001-example" / relative_path
        )

    def digest(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def workspace_bytes(self) -> dict[str, bytes]:
        workspace = self.work_root / "workspaces" / "001-example"
        return {
            path.relative_to(workspace).as_posix(): path.read_bytes()
            for path in workspace.rglob("*")
            if path.is_file() and not path.is_symlink()
        }

    def apply(self, decision: dict[str, object]) -> dict[str, object]:
        return apply_maintain_decision(
            self.project_root,
            self.work_root,
            "001-example",
            decision,
        )
