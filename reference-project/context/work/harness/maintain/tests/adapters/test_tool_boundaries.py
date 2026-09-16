"""도구별 설정 격리와 실제 CLI·worker 프로세스 진입을 검증한다."""

from __future__ import annotations

from contextlib import redirect_stderr
import hashlib
import io
import json
import subprocess
import sys

from context.work.harness.maintain.adapters.claude import ClaudeHookAdapter, main
from context.work.harness.maintain.host_adapter import MaintainHostAdapter
from context.work.harness.maintain.runtime.engine import MaintainRuntime
from context.work.harness.testing import WorkspaceFixture

from ..support.semantic import FakeSemanticSession, RecordingPopen


class ToolBoundaryTests(WorkspaceFixture):
    include_verification_scenarios = False

    def setUp(self) -> None:
        super().setUp()
        self.session_type = type("ToolScenario", (FakeSemanticSession,), {})
        self.session_type.reset()
        for tool in ("codex", "claude"):
            directory = self.project_root / f".{tool}"
            directory.mkdir()
            (directory / "maintain.json").write_text(
                json.dumps({"schema_version": 2, "mode": "explicit"}),
                encoding="utf-8",
            )

    def claude_runtime(self) -> MaintainRuntime:
        return MaintainRuntime(
            self.project_root,
            runtime_root=self.project_root / ".claude" / "maintain-runtime",
            config_path=self.project_root / ".claude" / "maintain.json",
            worker_module="context.work.harness.maintain.adapters.claude",
            session_type=self.session_type,
            runner=lambda *args, **kwargs: None,
            popen=RecordingPopen(),
        )

    @staticmethod
    def payload(event: str, **extra: object) -> dict[str, object]:
        return {"hook_event_name": event, "session_id": "same-id", **extra}

    def test_tool_bindings_with_same_session_id_remain_isolated(self) -> None:
        codex = MaintainHostAdapter(
            self.project_root,
            session_type=self.session_type,
            runner=lambda *args, **kwargs: None,
            popen=RecordingPopen(),
        )
        claude = self.claude_runtime()
        codex.activate("same-id", "001-example")
        self.assertEqual(claude.status("same-id")["status"], "unbound")
        claude.activate("same-id", "001-example")
        codex.deactivate("same-id")
        self.assertEqual(claude.status("same-id")["status"], "active")
        self.assertNotEqual(codex.runtime_root, claude.runtime_root)

    def test_claude_default_adapter_does_not_require_codex_host_config(self) -> None:
        (self.project_root / ".codex" / "maintain.json").unlink()
        hook = ClaudeHookAdapter(self.project_root, environ={})
        self.assertEqual(
            hook.control("status", workspace_id=None, session_id="same-id")["status"],
            "unbound",
        )
        self.assertFalse(hook.runtime_root.exists())

    def test_recursive_stop_preserves_pending_turn_for_real_response(self) -> None:
        runtime = self.claude_runtime()
        runtime.activate("same-id", "001-example")
        hook = ClaudeHookAdapter(self.project_root, adapter=runtime, environ={})
        hook.user_prompt(self.payload("UserPromptSubmit", prompt="기록할 내용"))
        state_path = hook._turn_state_path("same-id")
        pending = state_path.read_bytes()
        self.assertEqual(
            hook.response_end(self.payload("Stop", stop_hook_active=True)),
            {"continue": True},
        )
        self.assertEqual(state_path.read_bytes(), pending)
        hook.response_end(self.payload("Stop", last_assistant_message="확인했습니다"))
        key = hashlib.sha256(b"same-id").hexdigest()
        self.assertEqual(runtime.drain(key)["processed"], 1)
        self.assertEqual(self.session_type.deltas[0]["user_prompt"], "기록할 내용")

    def test_malformed_hook_input_returns_failure_notice_without_runtime(self) -> None:
        for value in (None, [], "invalid"):
            with self.subTest(value=value):
                output = io.StringIO()
                result = main(
                    ["user-prompt"],
                    project_root=self.project_root,
                    stdin=io.StringIO(json.dumps(value)),
                    stdout=output,
                    environ={},
                )
                self.assertEqual(result, 0)
                self.assertIn("failed", json.loads(output.getvalue())["systemMessage"])
                self.assertFalse(
                    (self.project_root / ".claude" / "maintain-runtime").exists()
                )

    def test_detached_claude_worker_uses_claude_config_in_new_process(self) -> None:
        runtime = self.claude_runtime()
        runtime.activate("same-id", "001-example")
        key = hashlib.sha256(b"same-id").hexdigest()
        runtime.worker._start_detached_drain(key)
        command, _ = runtime.context.popen.calls[0]
        (self.project_root / ".codex" / "maintain.json").write_text(
            "invalid", encoding="utf-8"
        )
        completed = subprocess.run(
            command,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["processed"], 0)

    def test_codex_legacy_module_cli_is_executable(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "context.work.harness.maintain.host_adapter",
                "status",
                "--project-root",
                str(self.project_root),
                "--session-id",
                "same-id",
            ],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "unbound")

    def test_claude_drain_rejects_missing_runtime_selection(self) -> None:
        with redirect_stderr(io.StringIO()):
            self.assertEqual(main(["drain"], project_root=self.project_root), 2)

    def test_invalid_claude_config_cannot_change_codex_binding(self) -> None:
        codex = MaintainHostAdapter(self.project_root, session_type=self.session_type)
        codex.activate("same-id", "001-example")
        (self.project_root / ".claude" / "maintain.json").write_text(
            "invalid", encoding="utf-8"
        )
        with redirect_stderr(io.StringIO()):
            self.assertEqual(
                main(
                    ["status", "--session-id", "same-id"],
                    project_root=self.project_root,
                ),
                2,
            )
        self.assertEqual(codex.status("same-id")["status"], "active")
