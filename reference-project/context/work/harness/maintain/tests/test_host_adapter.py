from __future__ import annotations

import hashlib
import json
from pathlib import Path
import threading
import unittest
from typing import Any

from context.work.harness.maintain.host_adapter import MaintainHostAdapter
from context.work.harness.maintain.operation import (
    apply_maintain_decision,
    bootstrap_workspace,
)
from context.work.harness.testing import WorkspaceFixture
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
    deltas: list[dict[str, Any]] = []
    decisions: list[dict[str, object]] = []
    resume_errors: list[Exception] = []

    @classmethod
    def reset(cls) -> None:
        cls.starts = []
        cls.restores = []
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


class MaintainHostAdapterTests(WorkspaceFixture):
    def setUp(self) -> None:
        super().setUp()
        FakeSemanticSession.reset()
        codex_directory = self.project_root / ".codex"
        codex_directory.mkdir()
        (codex_directory / "maintain.json").write_text(
            json.dumps(
                {"schema_version": 1, "workspace_id": "001-example"}
            )
            + "\n",
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
            session_type=FakeSemanticSession,
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
    def prompt_payload(
        session_id: str, turn_id: str, prompt: str
    ) -> dict[str, object]:
        return {
            "hook_event_name": "UserPromptSubmit",
            "session_id": session_id,
            "turn_id": turn_id,
            "prompt": prompt,
        }

    @staticmethod
    def stop_payload(
        session_id: str, turn_id: str, response: str
    ) -> dict[str, object]:
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

    def workspace_bytes(self) -> dict[str, bytes]:
        workspace = self.work_root / "workspaces" / "001-example"
        return {
            path.relative_to(workspace).as_posix(): path.read_bytes()
            for path in sorted(workspace.rglob("*"))
            if path.is_file()
        }

    def test_session_start_grounds_once_and_reuses_only_after_success(self) -> None:
        first = self.adapter.session_start(
            self.session_start_payload("host-session-a")
        )
        second = self.adapter.session_start(
            self.session_start_payload("host-session-a")
        )

        self.assertEqual(self.bootstrap_calls, 1)
        self.assertEqual(len(FakeSemanticSession.starts), 1)
        self.assertIn("systemMessage", first)
        self.assertIn("grounded", first["systemMessage"])
        self.assertNotIn("systemMessage", second)
        self.assertIn(
            "reusing",
            second["hookSpecificOutput"]["additionalContext"],
        )

        failing = MaintainHostAdapter(
            self.project_root,
            runtime_root=self.project_root / ".codex" / "failed-runtime",
            session_type=FailingStartSession,
            popen=self.popen,
            clock=self.clock,
        )
        failure = failing.session_start(
            self.session_start_payload("host-session-failure")
        )
        self.assertIn("not grounded", failure["systemMessage"])
        failed_directory = (
            self.project_root
            / ".codex"
            / "failed-runtime"
            / self.session_key("host-session-failure")
        )
        self.assertFalse((failed_directory / "session.json").exists())

    def test_ambiguous_grounding_never_commits_or_claims_grounded(self) -> None:
        runtime_root = self.project_root / ".codex" / "ambiguous-runtime"
        adapter = MaintainHostAdapter(
            self.project_root,
            runtime_root=runtime_root,
            session_type=AmbiguousStartSession,
            popen=self.popen,
            clock=self.clock,
        )

        output = adapter.session_start(
            self.session_start_payload("host-session-ambiguous")
        )

        self.assertIn("could not ground", output["systemMessage"])
        self.assertIn(
            "Which source is authoritative?", output["systemMessage"]
        )
        session_directory = runtime_root / self.session_key(
            "host-session-ambiguous"
        )
        self.assertFalse((session_directory / "session.json").exists())

    def test_drain_reuses_exact_grounded_thread_for_later_turns(self) -> None:
        session_id = "host-session-thread-reuse"
        self.adapter.session_start(self.session_start_payload(session_id))

        for number in (1, 2):
            turn_id = f"turn-{number}"
            self.adapter.user_prompt(
                self.prompt_payload(session_id, turn_id, f"prompt {number}")
            )
            self.adapter.response_end(
                self.stop_payload(session_id, turn_id, f"response {number}")
            )
        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(summary["processed"], 2)
        self.assertEqual(
            FakeSemanticSession.restores,
            ["maintain-thread-1", "maintain-thread-1"],
        )
        self.assertEqual(
            [delta["turn_id"] for delta in FakeSemanticSession.deltas],
            ["turn-1", "turn-2"],
        )

    def test_no_change_has_no_workspace_write_or_notification(self) -> None:
        session_id = "host-session-no-change"
        before = self.workspace_bytes()
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-1", "Explain the current state")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-1", "The state is already current")
        )

        summary = self.adapter.drain(self.session_key(session_id))
        prompt_output = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-2", "Continue")
        )

        self.assertEqual(summary["processed"], 1)
        self.assertEqual(len(self.apply_calls), 1)
        self.assertEqual(self.apply_calls[0]["outcome"], "no_change")
        self.assertEqual(self.workspace_bytes(), before)
        self.assertNotIn("hookSpecificOutput", prompt_output)

    def test_prompt_and_response_are_paired_by_stable_turn_id(self) -> None:
        session_id = "host-session-pair"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-pair", "USER_MARKER")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-pair", "RESPONSE_MARKER")
        )

        self.adapter.drain(self.session_key(session_id))

        self.assertEqual(
            FakeSemanticSession.deltas,
            [
                {
                    "workspace_id": "001-example",
                    "turn_id": "turn-pair",
                    "user_prompt": "USER_MARKER",
                    "main_response": "RESPONSE_MARKER",
                }
            ],
        )

    def test_duplicate_response_end_has_one_semantic_and_apply_effect(self) -> None:
        session_id = "host-session-duplicate"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-duplicate", "prompt")
        )
        payload = self.stop_payload(
            session_id, "turn-duplicate", "same response"
        )
        self.adapter.response_end(payload)
        self.adapter.response_end(payload)

        first = self.adapter.drain(self.session_key(session_id))
        second = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(first["processed"], 1)
        self.assertEqual(second["processed"], 0)
        self.assertEqual(second["already_resolved"], 1)
        self.assertEqual(len(FakeSemanticSession.deltas), 1)
        self.assertEqual(len(self.apply_calls), 1)

    def test_two_host_sessions_keep_runtime_and_threads_isolated(self) -> None:
        for session_id in ("host-session-left", "host-session-right"):
            self.adapter.session_start(self.session_start_payload(session_id))
            self.adapter.user_prompt(
                self.prompt_payload(session_id, "turn-1", f"prompt {session_id}")
            )
            self.adapter.response_end(
                self.stop_payload(session_id, "turn-1", f"response {session_id}")
            )

        self.adapter.drain(self.session_key("host-session-right"))
        self.adapter.drain(self.session_key("host-session-left"))

        self.assertEqual(
            FakeSemanticSession.restores,
            ["maintain-thread-2", "maintain-thread-1"],
        )
        self.assertEqual(
            {delta["user_prompt"] for delta in FakeSemanticSession.deltas},
            {
                "prompt host-session-left",
                "prompt host-session-right",
            },
        )
        runtime_directories = {
            path.name
            for path in self.runtime_root.iterdir()
            if path.is_dir()
        }
        self.assertEqual(
            runtime_directories,
            {
                self.session_key("host-session-left"),
                self.session_key("host-session-right"),
            },
        )

    def test_failure_is_effect_once_but_never_recorded_as_completed(self) -> None:
        session_id = "host-session-failure"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-failure", "prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-failure", "response")
        )
        FakeSemanticSession.resume_errors = [HarnessError("semantic crash")]

        first = self.adapter.drain(self.session_key(session_id))
        second = self.adapter.drain(self.session_key(session_id))
        next_prompt = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-after-failure", "what happened?")
        )

        self.assertEqual(first["failed"], 1)
        self.assertEqual(second["already_resolved"], 1)
        self.assertEqual(len(FakeSemanticSession.deltas), 1)
        effect_files = list(
            (
                self.runtime_root
                / self.session_key(session_id)
                / "effects"
            ).glob("*.json")
        )
        self.assertEqual(len(effect_files), 1)
        effect = json.loads(effect_files[0].read_text(encoding="utf-8"))
        self.assertEqual(effect["status"], "failed")
        self.assertNotEqual(effect["status"], "completed")
        notification = next_prompt["hookSpecificOutput"]["additionalContext"]
        self.assertIn("failed, not completed", notification)
        self.assertIn("semantic crash", notification)

    def test_ambiguity_and_important_update_surface_on_next_prompt(self) -> None:
        session_id = "host-session-notifications"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-ambiguity", "choose source")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-ambiguity", "Which source?")
        )
        FakeSemanticSession.decisions = [
            {
                "schema_version": 1,
                "workspace_id": "001-example",
                "outcome": "needs_user_decision",
                "importance": "important",
                "summary": "Source authority is ambiguous.",
                "changes": [],
                "evidence": ["The user named two possible sources."],
                "unresolved": ["source authority"],
                "question": "Which source is authoritative?",
            }
        ]
        before_ambiguity = self.workspace_bytes()

        self.adapter.drain(self.session_key(session_id))
        ambiguity_output = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-important", "Use source A")
        )

        self.assertEqual(self.workspace_bytes(), before_ambiguity)
        self.assertIn(
            "Which source is authoritative?",
            ambiguity_output["hookSpecificOutput"]["additionalContext"],
        )

        state_path = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "current"
            / "state"
            / "index.md"
        )
        original = state_path.read_bytes()
        new_content = "# state\n\nImportant durable update.\n"
        FakeSemanticSession.decisions = [
            {
                "schema_version": 1,
                "workspace_id": "001-example",
                "outcome": "update",
                "importance": "important",
                "summary": "The current state changed materially.",
                "changes": [
                    {
                        "path": "current/state/index.md",
                        "expected_sha256": hashlib.sha256(original).hexdigest(),
                        "content": new_content,
                        "reason": "Preserve the material current-state change.",
                    }
                ],
                "evidence": ["The user selected source A."],
                "unresolved": [],
                "question": None,
            }
        ]
        self.adapter.response_end(
            self.stop_payload(
                session_id,
                "turn-important",
                "The important state is now recorded.",
            )
        )
        self.adapter.drain(self.session_key(session_id))
        important_output = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-after-update", "continue")
        )

        self.assertEqual(state_path.read_text(encoding="utf-8"), new_content)
        important_context = important_output["hookSpecificOutput"][
            "additionalContext"
        ]
        self.assertIn("updated Workspace", important_context)
        self.assertIn("current/state/index.md", important_context)

    def test_response_end_only_enqueues_and_starts_detached_drain(self) -> None:
        session_id = "host-session-detached"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-detached", "prompt")
        )

        self.adapter.response_end(
            self.stop_payload(session_id, "turn-detached", "response")
        )

        self.assertEqual(FakeSemanticSession.deltas, [])
        self.assertEqual(len(self.popen.calls), 1)
        command, options = self.popen.calls[0]
        self.assertIn("drain", command)
        self.assertTrue(options["start_new_session"])
        event_directory = (
            self.runtime_root
            / self.session_key(session_id)
            / "events"
        )
        self.assertEqual(len(list(event_directory.glob("*.json"))), 1)

    def test_next_prompt_exposes_prior_prompt_without_response_end_once(self) -> None:
        session_id = "host-session-orphan-prompt"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-orphan", "first prompt")
        )

        output = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-next", "next prompt")
        )
        repeated = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-next", "next prompt")
        )

        notification = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("without a matching response-end", notification)
        self.assertNotIn("hookSpecificOutput", repeated)
        effect_directory = (
            self.runtime_root
            / self.session_key(session_id)
            / "effects"
        )
        effects = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in effect_directory.glob("*.json")
        ]
        self.assertEqual([effect["status"] for effect in effects], ["failed"])
        self.assertEqual(FakeSemanticSession.deltas, [])

    def test_session_end_exposes_prompt_without_response_end(self) -> None:
        session_id = "host-session-end-orphan"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-orphan", "prompt")
        )

        output = self.adapter.session_end(
            {
                "hook_event_name": "SessionEnd",
                "session_id": session_id,
                "reason": "other",
            }
        )

        self.assertIn("1 prompt(s) missing", output["systemMessage"])
        session_end = json.loads(
            (
                self.runtime_root
                / self.session_key(session_id)
                / "session-end.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(len(session_end["orphan_prompt_keys"]), 1)
        self.assertEqual(session_end["unresolved_event_keys"], [])

    def test_later_user_prompt_rekicks_an_unresolved_response_end(self) -> None:
        session_id = "host-session-rekick"
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-1", "prompt one")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-1", "response one")
        )
        self.assertEqual(len(self.popen.calls), 1)

        output = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-2", "prompt two")
        )

        self.assertEqual(len(self.popen.calls), 2)
        self.assertIn("systemMessage", output)
        pending_context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("still pending", pending_context)
        self.assertIn("not completed", pending_context)
        self.assertIn("do not establish fresh or current Context", pending_context)

    def test_pending_boundary_and_notice_share_one_prompt_context(self) -> None:
        session_id = "host-session-pending-with-notice"
        failing_popen = FailingPopen()
        self.adapter._popen = failing_popen
        self.adapter.session_start(self.session_start_payload(session_id))
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-1", "prompt one")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-1", "response one")
        )

        output = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-2", "prompt two")
        )

        self.assertEqual(
            set(output), {"continue", "systemMessage", "hookSpecificOutput"}
        )
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("could not start its background worker", context)
        self.assertIn("still pending", context)
        self.assertEqual(context.count("Previous Workspace Maintain results"), 1)
        self.assertEqual(len(failing_popen.calls), 2)

    def test_runtime_root_must_be_an_internal_absolute_lexical_path(self) -> None:
        outside = self.project_root.parent / "outside-maintain-runtime"
        traversal = self.project_root / ".codex" / ".." / "escaped-runtime"
        cases = [
            (Path("relative-runtime"), "absolute path"),
            (outside, "inside the Project root"),
            (traversal, "ancestor traversal"),
        ]

        for runtime_root, expected in cases:
            with self.subTest(runtime_root=runtime_root):
                with self.assertRaisesRegex(HarnessError, expected):
                    MaintainHostAdapter(
                        self.project_root,
                        runtime_root=runtime_root,
                        session_type=FakeSemanticSession,
                        popen=self.popen,
                        clock=self.clock,
                    )

    def test_preexisting_runtime_root_symlink_is_rejected(self) -> None:
        target = self.project_root / ".codex" / "linked-runtime-target"
        target.mkdir()
        linked_runtime = self.project_root / ".codex" / "linked-runtime"
        linked_runtime.symlink_to(target, target_is_directory=True)

        with self.assertRaisesRegex(HarnessError, "symlink components"):
            MaintainHostAdapter(
                self.project_root,
                runtime_root=linked_runtime,
                session_type=FakeSemanticSession,
                popen=self.popen,
                clock=self.clock,
            )

    def test_preexisting_session_directory_symlink_is_rejected(self) -> None:
        runtime_root = self.project_root / ".codex" / "session-link-runtime"
        runtime_root.mkdir()
        target = self.project_root / ".codex" / "linked-session-target"
        target.mkdir()
        session_id = "host-session-linked-directory"
        (runtime_root / self.session_key(session_id)).symlink_to(
            target, target_is_directory=True
        )
        adapter = MaintainHostAdapter(
            self.project_root,
            runtime_root=runtime_root,
            session_type=FakeSemanticSession,
            popen=self.popen,
            clock=self.clock,
        )

        with self.assertRaisesRegex(HarnessError, "symlink components"):
            adapter.session_start(self.session_start_payload(session_id))

    def test_detached_drains_wait_for_the_same_session_lock(self) -> None:
        session_id = "host-session-blocking-lock"
        self.adapter.session_start(self.session_start_payload(session_id))
        session_directory = self.adapter._session_directory(session_id)
        entered = threading.Event()
        finished = threading.Event()

        def run_second_drain() -> None:
            entered.set()
            self.adapter.drain(self.session_key(session_id))
            finished.set()

        with self.adapter._drain_lock(session_directory):
            worker = threading.Thread(target=run_second_drain)
            worker.start()
            self.assertTrue(entered.wait(timeout=1.0))
            self.assertFalse(finished.wait(timeout=0.05))
        worker.join(timeout=1.0)

        self.assertFalse(worker.is_alive())
        self.assertTrue(finished.is_set())


if __name__ == "__main__":
    unittest.main()
