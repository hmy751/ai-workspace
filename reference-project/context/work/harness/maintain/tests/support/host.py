"""Maintain host 시나리오의 경로·입력·runtime 준비."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

from context.work.harness.maintain.host_adapter import MaintainHostAdapter
from context.work.harness.maintain.operation import (
    apply_maintain_decision,
    bootstrap_workspace,
)
from context.work.harness.testing import WorkspaceFixture

from .semantic import FakeSemanticSession, RecordingPopen, IncrementingClock


class MaintainHostAdapterFixture(WorkspaceFixture):

    def setUp(self) -> None:
        super().setUp()
        self.semantic_session_type = type("ScenarioSession", (FakeSemanticSession,), {})
        self.semantic_session_type.reset()
        codex_directory = self.project_root / ".codex"
        codex_directory.mkdir()
        (codex_directory / "maintain.json").write_text(
            json.dumps({"schema_version": 2, "mode": "explicit"}) + "\n",
            encoding="utf-8",
        )
        self.runtime_root = codex_directory / "test-maintain-runtime"
        self.popen = RecordingPopen()
        self.clock = IncrementingClock()
        self.bootstrap_calls = 0
        self.apply_calls: list[dict[str, object]] = []

        def counted_bootstrap(
            project_root: Path, work_root: Path, workspace_id: str
        ) -> dict[str, Any]:
            self.bootstrap_calls += 1
            return bootstrap_workspace(project_root, work_root, workspace_id)

        def recording_apply(
            project_root: Path,
            work_root: Path,
            workspace_id: str,
            decision: Any,
        ) -> dict[str, Any]:
            self.apply_calls.append(decision)
            return apply_maintain_decision(
                project_root, work_root, workspace_id, decision
            )

        self.adapter = MaintainHostAdapter(
            self.project_root,
            runtime_root=self.runtime_root,
            session_type=self.semantic_session_type,
            runner=lambda *args, **kwargs: None,
            popen=self.popen,
            clock=self.clock,
            python_executable="fixture-python",
            bootstrap=counted_bootstrap,
            apply_decision=recording_apply,
        )

    @staticmethod
    def session_start_payload(session_id: str) -> dict[str, object]:
        return {
            "hook_event_name": "SessionStart",
            "session_id": session_id,
            "cwd": "/unused/by-direct-test",
            "source": "startup",
        }

    @staticmethod
    def prompt_payload(session_id: str, turn_id: str, prompt: str) -> dict[str, object]:
        return {
            "hook_event_name": "UserPromptSubmit",
            "session_id": session_id,
            "turn_id": turn_id,
            "prompt": prompt,
        }

    @staticmethod
    def stop_payload(session_id: str, turn_id: str, response: str) -> dict[str, object]:
        return {
            "hook_event_name": "Stop",
            "session_id": session_id,
            "turn_id": turn_id,
            "last_assistant_message": response,
            "stop_hook_active": False,
        }

    @staticmethod
    def session_key(session_id: str) -> str:
        return hashlib.sha256(session_id.encode("utf-8")).hexdigest()

    def activate_session(
        self,
        session_id: str,
        workspace_id: str = "001-example",
    ) -> dict[str, Any]:
        return self.adapter.activate(session_id, workspace_id)

    def start_bound_session(
        self,
        session_id: str,
        workspace_id: str = "001-example",
    ) -> dict[str, Any]:
        self.activate_session(session_id, workspace_id)
        return self.adapter.session_start(self.session_start_payload(session_id))

    def add_workspace(self, workspace_id: str) -> None:
        source = self.work_root / "workspaces" / "001-example"
        target = self.work_root / "workspaces" / workspace_id
        shutil.copytree(source, target)
        for relative_path in (
            "workspace.json",
            "recover.json",
            "verify.json",
            "current/state/status.json",
        ):
            path = target / relative_path
            value = json.loads(path.read_text(encoding="utf-8"))
            value["workspace_id"] = workspace_id
            path.write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    def workspace_bytes(self, workspace_id: str = "001-example") -> dict[str, bytes]:
        workspace = self.work_root / "workspaces" / workspace_id
        return {
            path.relative_to(workspace).as_posix(): path.read_bytes()
            for path in sorted(workspace.rglob("*"))
            if path.is_file()
        }
