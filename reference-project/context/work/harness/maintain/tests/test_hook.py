from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from context.work.harness.maintain.controller import (
    PendingNotice,
    SessionStartResult,
)
from context.work.harness.maintain.hook import (
    handle_hook,
    hook_output,
    main,
    spawn_worker,
)
from context.work.harness.maintain.runner import CHILD_ENVIRONMENT_VARIABLE


def payload(event: str) -> dict[str, object]:
    value: dict[str, object] = {
        "hook_event_name": event,
        "session_id": "main-session",
    }
    if event == "SessionStart":
        value["source"] = "startup"
    else:
        value["turn_id"] = "turn-1"
    if event == "UserPromptSubmit":
        value["prompt"] = "private prompt"
    if event == "Stop":
        value["last_assistant_message"] = "private answer"
    if event == "PostToolUse":
        value.update(
            {
                "tool_name": "apply_patch",
                "tool_use_id": "tool-use-1",
                "tool_input": "*** Update File: current/state.md\nSECRET",
                "tool_response": {"status": "completed"},
            }
        )
    return value


class FakeController:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []
        self.start_result = SessionStartResult(False, None)
        self.notice = PendingNotice(None, None, ())
        self.capture_result: dict[str, object] = {"paired": True}
        self.process_calls = 0
        self.process_result: dict[str, object] = {
            "status": "idle",
            "processed": 0,
            "successor_required": False,
        }
        self.next_runnable: str | None = None
        self.acknowledgements: list[tuple[str, tuple[str, ...]]] = []
        self.workspace_acknowledgements: list[
            tuple[str, tuple[tuple[str, str], ...]]
        ] = []
        self.repairs: list[tuple[str, int, str, str]] = []
        self.trace: list[str] = []
        self.start_error: Exception | None = None

    def session_start(self, value: object) -> SessionStartResult:
        self.calls.append(("session_start", value))
        if self.start_error is not None:
            raise self.start_error
        return self.start_result

    def capture_user_prompt(self, value: object) -> dict[str, object]:
        self.calls.append(("user", value))
        return self.capture_result

    def capture_stop(self, value: object) -> dict[str, object]:
        self.calls.append(("stop", value))
        return self.capture_result

    def capture_post_tool_use(self, value: object) -> dict[str, object]:
        self.calls.append(("post_tool", value))
        return self.capture_result

    def take_pending_notice(self, session_id: str) -> PendingNotice:
        self.calls.append(("pending", session_id))
        return self.notice

    def acknowledge_notice(
        self, session_id: str, report_ids: tuple[str, ...]
    ) -> tuple[str, ...]:
        self.trace.append("ack")
        self.acknowledgements.append((session_id, report_ids))
        return report_ids

    def acknowledge_workspace_notice(
        self,
        recipient_session_id: str,
        report_acks: tuple[tuple[str, str], ...],
    ) -> tuple[tuple[str, str], ...]:
        self.trace.append("workspace_ack")
        self.workspace_acknowledgements.append(
            (recipient_session_id, report_acks)
        )
        return report_acks

    def process_session(self, session_id: str) -> dict[str, object]:
        self.process_calls += 1
        return dict(self.process_result)

    def next_runnable_session_id(self) -> str | None:
        return self.next_runnable

    def repair_missing_stop_gap(
        self,
        session_id: str,
        expected_sequence: int,
        *,
        approved_by: str,
        reason: str,
    ) -> dict[str, object]:
        self.repairs.append(
            (session_id, expected_sequence, approved_by, reason)
        )
        return {"repaired": True, "sequence": expected_sequence}

    def status(self, session_id: str | None = None) -> dict[str, object]:
        return {"session": session_id, "freshness": {"state": "fresh"}}


class HookBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config_path = Path("/target/.codex/context-maintain.json")

    def test_session_start_requests_one_short_first_commentary(self) -> None:
        controller = FakeController()
        controller.start_result = SessionStartResult(True, "목표, 상태, 다음 행동")

        result = handle_hook(
            "SessionStart",
            payload("SessionStart"),
            controller,
            config_path=self.config_path,
            spawner=lambda *_args: self.fail("SessionStart must not spawn"),
            environment={},
        )

        self.assertEqual(result.output["continue"], True)
        specific = result.output["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "SessionStart")
        self.assertIn("첫 commentary", specific["additionalContext"])
        self.assertIn("목표, 상태, 다음 행동", specific["additionalContext"])

    def test_session_start_restarts_one_prior_runnable_worker(self) -> None:
        controller = FakeController()
        controller.start_result = SessionStartResult(True, "시작 상태")
        controller.next_runnable = "prior-session"
        spawned: list[tuple[Path, str]] = []

        result = handle_hook(
            "SessionStart",
            payload("SessionStart"),
            controller,
            config_path=self.config_path,
            spawner=lambda path, session: spawned.append((path, session)),
            environment={},
        )

        self.assertTrue(result.output["continue"])
        self.assertEqual(spawned, [(self.config_path, "prior-session")])

    def test_user_capture_spawns_without_waiting_for_agent_completion(self) -> None:
        controller = FakeController()
        spawned: list[tuple[Path, str]] = []

        result = handle_hook(
            "UserPromptSubmit",
            payload("UserPromptSubmit"),
            controller,
            config_path=self.config_path,
            spawner=lambda path, session: spawned.append((path, session)),
            environment={},
        )

        self.assertEqual(spawned, [(self.config_path, "main-session")])
        self.assertEqual(controller.process_calls, 0)
        self.assertEqual(
            [name for name, _value in controller.calls], ["user", "pending"]
        )
        self.assertEqual(result.output, {"continue": True})
        self.assertEqual(controller.acknowledgements, [])

    def test_session_start_failure_requests_manual_grounding(self) -> None:
        controller = FakeController()
        controller.start_error = RuntimeError("grounding failed")

        result = handle_hook(
            "SessionStart",
            payload("SessionStart"),
            controller,
            config_path=self.config_path,
            spawner=lambda *_args: None,
            environment={},
        )

        self.assertTrue(result.output["continue"])
        self.assertIn("Workspace current", result.output["systemMessage"])
        self.assertIn(
            "README와 current index",
            result.output["hookSpecificOutput"]["additionalContext"],
        )
        self.assertNotIn("grounding failed", json.dumps(result.output))

    def test_stop_only_captures_and_spawns(self) -> None:
        controller = FakeController()
        spawned: list[str] = []

        result = handle_hook(
            "Stop",
            payload("Stop"),
            controller,
            config_path=self.config_path,
            spawner=lambda _path, session: spawned.append(session),
            environment={},
        )

        self.assertEqual(spawned, ["main-session"])
        self.assertEqual(controller.calls[0][0], "stop")
        self.assertNotIn("hookSpecificOutput", result.output)

    def test_post_tool_use_only_captures_and_never_spawns_or_processes(self) -> None:
        controller = FakeController()
        spawned: list[str] = []

        result = handle_hook(
            "PostToolUse",
            payload("PostToolUse"),
            controller,
            config_path=self.config_path,
            spawner=lambda _path, session: spawned.append(session),
            environment={},
        )

        self.assertEqual(result.output, {"continue": True})
        self.assertEqual(spawned, [])
        self.assertEqual(controller.process_calls, 0)
        self.assertEqual(
            [name for name, _value in controller.calls], ["post_tool"]
        )
        self.assertNotIn("SECRET", json.dumps(result.output))

    def test_background_question_is_injected_at_next_user_safe_point(self) -> None:
        controller = FakeController()
        controller.notice = PendingNotice(
            additional_context="Maintain 판단 질문: 어느 Owner에 둘까요?",
            system_message="Maintain에 사용자 판단이 필요한 항목이 있습니다.",
            report_ids=("report-1",),
        )

        stop_result = handle_hook(
            "Stop",
            payload("Stop"),
            controller,
            config_path=self.config_path,
            spawner=lambda *_args: None,
            environment={},
        )
        user_result = handle_hook(
            "UserPromptSubmit",
            payload("UserPromptSubmit"),
            controller,
            config_path=self.config_path,
            spawner=lambda *_args: None,
            environment={},
        )

        # A detached hook cannot manufacture a host UI turn at Stop. The
        # semantic question is therefore delivered at the next safe Main turn,
        # where Main must still ask it immediately before the relevant write.
        self.assertNotIn("hookSpecificOutput", stop_result.output)
        self.assertIn(
            "어느 Owner에 둘까요?",
            user_result.output["hookSpecificOutput"]["additionalContext"],
        )
        self.assertIn("systemMessage", user_result.output)
        self.assertEqual(user_result.report_ids, ("report-1",))
        self.assertEqual(controller.acknowledgements, [])

    def test_recursion_guard_is_a_no_op(self) -> None:
        controller = FakeController()
        spawned: list[str] = []

        result = handle_hook(
            "UserPromptSubmit",
            payload("UserPromptSubmit"),
            controller,
            config_path=self.config_path,
            spawner=lambda _path, session: spawned.append(session),
            environment={CHILD_ENVIRONMENT_VARIABLE: "1"},
        )

        self.assertEqual(result.output, {"continue": True})
        self.assertEqual(controller.calls, [])
        self.assertEqual(spawned, [])

    def test_malformed_payload_and_spawner_failure_fail_open(self) -> None:
        controller = FakeController()
        malformed = handle_hook(
            "Stop",
            {"hook_event_name": "Stop"},
            controller,
            config_path=self.config_path,
            spawner=lambda *_args: None,
            environment={},
        )
        spawn_failure = handle_hook(
            "Stop",
            payload("Stop"),
            controller,
            config_path=self.config_path,
            spawner=lambda *_args: (_ for _ in ()).throw(OSError("fail")),
            environment={},
        )

        self.assertTrue(malformed.output["continue"])
        self.assertTrue(spawn_failure.output["continue"])
        self.assertIn("systemMessage", malformed.output)
        self.assertNotIn("private", json.dumps(malformed.output))

    def test_hook_output_uses_official_common_and_specific_shape(self) -> None:
        self.assertEqual(
            hook_output(
                "UserPromptSubmit",
                additional_context="context",
                system_message="notice",
            ),
            {
                "continue": True,
                "systemMessage": "notice",
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": "context",
                },
            },
        )


class DetachedWorkerTests(unittest.TestCase):
    def test_spawn_is_detached_content_silent_and_child_guarded(self) -> None:
        captured: dict[str, object] = {}

        def fake_popen(command: list[str], **kwargs: object) -> object:
            captured["command"] = command
            captured.update(kwargs)
            return object()

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target-without-reference-package"
            (target / ".codex").mkdir(parents=True)
            config = target / ".codex/context-maintain.json"
            config.write_text("{}", encoding="utf-8")
            spawn_worker(config, "main-session", popen=fake_popen)

        command = captured["command"]
        self.assertEqual(command[0], sys.executable)
        self.assertEqual(
            Path(command[1]).resolve(),
            Path(__file__).resolve().parents[1] / "hook.py",
        )
        self.assertNotIn("-m", command)
        self.assertEqual(command[-2:], ["--session-id", "main-session"])
        self.assertEqual(Path(captured["cwd"]).resolve(), target.resolve())
        self.assertIs(captured["stdin"], subprocess.DEVNULL)
        self.assertIs(captured["stdout"], subprocess.DEVNULL)
        self.assertIs(captured["stderr"], subprocess.DEVNULL)
        self.assertTrue(captured["start_new_session"])
        environment = captured["env"]
        self.assertEqual(environment[CHILD_ENVIRONMENT_VARIABLE], "1")


class CliFailOpenTests(unittest.TestCase):
    def run_main_with_stdin(
        self, argv: list[str], stdin: str
    ) -> tuple[int, dict[str, object]]:
        output = StringIO()
        old_stdin = sys.stdin
        try:
            sys.stdin = StringIO(stdin)
            with redirect_stdout(output):
                code = main(argv)
        finally:
            sys.stdin = old_stdin
        return code, json.loads(output.getvalue())

    def test_invalid_hook_json_fails_open_without_loading_config(self) -> None:
        code, output = self.run_main_with_stdin(
            ["--config", "/missing/config.json", "hook", "Stop"],
            "not-json",
        )
        self.assertEqual(code, 0)
        self.assertTrue(output["continue"])
        self.assertIn("systemMessage", output)

    def test_malformed_config_fails_open_for_hook(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".codex").mkdir()
            config = root / ".codex/context-maintain.json"
            config.write_text("{}", encoding="utf-8")
            code, output = self.run_main_with_stdin(
                ["--config", str(config), "hook", "SessionStart"],
                json.dumps(payload("SessionStart")),
            )
        self.assertEqual(code, 0)
        self.assertTrue(output["continue"])
        self.assertIn("systemMessage", output)
        self.assertIn("Workspace current", output["systemMessage"])
        self.assertIn(
            "README와 current index",
            output["hookSpecificOutput"]["additionalContext"],
        )

    def test_child_hook_no_ops_before_config_or_stdin_use(self) -> None:
        output = StringIO()
        previous = os.environ.get(CHILD_ENVIRONMENT_VARIABLE)
        os.environ[CHILD_ENVIRONMENT_VARIABLE] = "1"
        try:
            with redirect_stdout(output):
                code = main(
                    ["--config", "/missing/config.json", "hook", "Stop"]
                )
        finally:
            if previous is None:
                os.environ.pop(CHILD_ENVIRONMENT_VARIABLE, None)
            else:
                os.environ[CHILD_ENVIRONMENT_VARIABLE] = previous
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue()), {"continue": True})

    def test_pending_report_is_acknowledged_only_after_stdout_flush(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "target"
            workspace = (
                project
                / "context/work/workspaces/005-context-continuity-maintenance"
            )
            (project / ".codex").mkdir(parents=True)
            (project / "context/work/harness/maintain").mkdir(parents=True)
            workspace.mkdir(parents=True)
            (project / "context/work/harness/maintain/README.md").write_text(
                "# Maintain\n", encoding="utf-8"
            )
            config = project / ".codex/context-maintain.json"
            config.write_text(
                json.dumps(
                    {
                        "schema": "context-maintain.config.v1",
                        "workspace_id": "005-context-continuity-maintenance",
                        "work_root": "context/work",
                        "maintain_contract_path": (
                            "context/work/harness/maintain/README.md"
                        ),
                        "runtime_root": ".codex/runtime/context-maintain",
                        "sandbox": "read-only",
                    }
                ),
                encoding="utf-8",
            )
            controller = FakeController()
            controller.notice = PendingNotice(
                "Maintain 반영 완료: 상태 갱신",
                None,
                ("report-1",),
                (("a" * 32, "question-1"),),
            )

            class TracedOutput(StringIO):
                def flush(inner_self) -> None:
                    controller.trace.append("flush")
                    super().flush()

            output = TracedOutput()
            previous_stdin = sys.stdin
            try:
                sys.stdin = StringIO(json.dumps(payload("UserPromptSubmit")))
                with redirect_stdout(output):
                    code = main(
                        [
                            "--config",
                            str(config),
                            "hook",
                            "UserPromptSubmit",
                        ],
                        controller_factory=lambda _config: controller,
                        spawner=lambda *_args: None,
                    )
            finally:
                sys.stdin = previous_stdin

        self.assertEqual(code, 0)
        self.assertEqual(
            controller.trace[:3], ["flush", "ack", "workspace_ack"]
        )
        self.assertEqual(
            controller.acknowledgements,
            [("main-session", ("report-1",))],
        )
        self.assertEqual(
            controller.workspace_acknowledgements,
            [("main-session", (("a" * 32, "question-1"),))],
        )
        rendered = json.loads(output.getvalue())
        self.assertNotIn("report-1", json.dumps(rendered))
        self.assertNotIn("report_ids", json.dumps(rendered))

    def test_worker_exit_does_not_claim_retry_or_blocked_as_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "target"
            (project / ".codex").mkdir(parents=True)
            contract = project / "context/work/harness/maintain/README.md"
            contract.parent.mkdir(parents=True)
            contract.write_text("# Maintain\n", encoding="utf-8")
            (project / "context/work/workspaces").mkdir(parents=True)
            config = project / ".codex/context-maintain.json"
            config.write_text(
                json.dumps(
                    {
                        "schema": "context-maintain.config.v1",
                        "workspace_id": "005-context-continuity-maintenance",
                        "work_root": "context/work",
                        "maintain_contract_path": (
                            "context/work/harness/maintain/README.md"
                        ),
                        "runtime_root": ".context-harness/runtime/context-maintain",
                        "sandbox": "read-only",
                    }
                ),
                encoding="utf-8",
            )

            for status, expected in (
                ("idle", 0),
                ("busy", 0),
                ("already_processed", 0),
                ("processed", 0),
                ("retry", 1),
                ("blocked", 1),
            ):
                with self.subTest(status=status):
                    controller = FakeController()
                    controller.process_result = {"status": status}
                    code = main(
                        [
                            "--config",
                            str(config),
                            "worker",
                            "--session-id",
                            "main-session",
                        ],
                        controller_factory=lambda _config, value=controller: value,
                    )
                    self.assertEqual(code, expected)

    def test_worker_spawns_one_successor_when_controller_requires_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "target"
            (project / ".codex").mkdir(parents=True)
            contract = project / "context/work/harness/maintain/README.md"
            contract.parent.mkdir(parents=True)
            contract.write_text("# Maintain\n", encoding="utf-8")
            (project / "context/work/workspaces").mkdir(parents=True)
            config = project / ".codex/context-maintain.json"
            config.write_text(
                json.dumps(
                    {
                        "schema": "context-maintain.config.v1",
                        "workspace_id": "005-context-continuity-maintenance",
                        "work_root": "context/work",
                        "maintain_contract_path": (
                            "context/work/harness/maintain/README.md"
                        ),
                        "runtime_root": (
                            ".context-harness/runtime/context-maintain"
                        ),
                        "sandbox": "read-only",
                    }
                ),
                encoding="utf-8",
            )
            controller = FakeController()
            controller.process_result = {
                "status": "processed",
                "work_remaining": True,
                "successor_required": True,
            }
            controller.next_runnable = "main-session"
            spawned: list[tuple[Path, str]] = []

            code = main(
                [
                    "--config",
                    str(config),
                    "worker",
                    "--session-id",
                    "main-session",
                ],
                controller_factory=lambda _config: controller,
                spawner=lambda path, session: spawned.append((path, session)),
            )

        self.assertEqual(code, 0)
        self.assertEqual(len(spawned), 1)
        self.assertEqual(spawned[0][0].resolve(), config.resolve())
        self.assertEqual(spawned[0][1], "main-session")

    def test_worker_does_not_chain_after_retry_budget_is_exhausted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "target"
            (project / ".codex").mkdir(parents=True)
            contract = project / "context/work/harness/maintain/README.md"
            contract.parent.mkdir(parents=True)
            contract.write_text("# Maintain\n", encoding="utf-8")
            (project / "context/work/workspaces").mkdir(parents=True)
            config = project / ".codex/context-maintain.json"
            config.write_text(
                json.dumps(
                    {
                        "schema": "context-maintain.config.v1",
                        "workspace_id": "005-context-continuity-maintenance",
                        "work_root": "context/work",
                        "maintain_contract_path": (
                            "context/work/harness/maintain/README.md"
                        ),
                        "runtime_root": (
                            ".context-harness/runtime/context-maintain"
                        ),
                        "sandbox": "read-only",
                    }
                ),
                encoding="utf-8",
            )
            controller = FakeController()
            controller.process_result = {
                "status": "retry",
                "retry_attempts": 3,
                "successor_required": False,
            }
            spawned: list[tuple[Path, str]] = []

            code = main(
                [
                    "--config",
                    str(config),
                    "worker",
                    "--session-id",
                    "main-session",
                ],
                controller_factory=lambda _config: controller,
                spawner=lambda path, session: spawned.append((path, session)),
            )

        self.assertEqual(code, 1)
        self.assertEqual(spawned, [])

    def test_gap_repair_cli_preserves_explicit_approval_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "target"
            (project / ".codex").mkdir(parents=True)
            contract = project / "context/work/harness/maintain/README.md"
            contract.parent.mkdir(parents=True)
            contract.write_text("# Maintain\n", encoding="utf-8")
            (project / "context/work/workspaces").mkdir(parents=True)
            config = project / ".codex/context-maintain.json"
            config.write_text(
                json.dumps(
                    {
                        "schema": "context-maintain.config.v1",
                        "workspace_id": "005-context-continuity-maintenance",
                        "work_root": "context/work",
                        "maintain_contract_path": (
                            "context/work/harness/maintain/README.md"
                        ),
                        "runtime_root": ".context-harness/runtime/context-maintain",
                        "sandbox": "read-only",
                    }
                ),
                encoding="utf-8",
            )
            controller = FakeController()
            output = StringIO()
            with redirect_stdout(output):
                code = main(
                    [
                        "--config",
                        str(config),
                        "repair-gap",
                        "--session-id",
                        "main-session",
                        "--expected-sequence",
                        "3",
                        "--approved-by",
                        "user",
                        "--reason",
                        "missing_stop_confirmed",
                    ],
                    controller_factory=lambda _config: controller,
                )

        self.assertEqual(code, 0)
        self.assertEqual(
            controller.repairs,
            [("main-session", 3, "user", "missing_stop_confirmed")],
        )
        self.assertEqual(json.loads(output.getvalue())["sequence"], 3)


if __name__ == "__main__":
    unittest.main()
