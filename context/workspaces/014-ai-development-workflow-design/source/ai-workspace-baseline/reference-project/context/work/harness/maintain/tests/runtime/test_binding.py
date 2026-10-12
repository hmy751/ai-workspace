"""명시적 binding, generation 전환과 session 격리를 검증한다."""

from __future__ import annotations

from context.work.harness.maintain.host_adapter import MaintainHostAdapter
from context.work.harness.workspace_contract import HarnessError

from ..support.host import MaintainHostAdapterFixture
from ..support.semantic import (
    AmbiguousStartSession,
    FailingSecondWorkspaceSession,
    FailingStartSession,
)


class MaintainHostBindingTests(MaintainHostAdapterFixture):
    def test_unbound_session_hooks_are_quiet_and_write_nothing(self) -> None:
        session_id = "host-session-unbound"
        before = self.workspace_bytes()

        start = self.adapter.session_start(self.session_start_payload(session_id))
        prompt = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-1", "unrelated prompt")
        )
        stop = self.adapter.response_end(
            self.stop_payload(session_id, "turn-1", "unrelated response")
        )
        end = self.adapter.session_end(
            {
                "hook_event_name": "SessionEnd",
                "session_id": session_id,
                "reason": "complete",
            }
        )

        self.assertEqual(start, {"continue": True})
        self.assertEqual(prompt, {"continue": True})
        self.assertEqual(stop, {"continue": True})
        self.assertEqual(end, {"continue": True})
        self.assertEqual(self.bootstrap_calls, 0)
        self.assertEqual(self.semantic_session_type.starts, [])
        self.assertEqual(self.workspace_bytes(), before)
        self.assertFalse(self.runtime_root.exists())

    def test_explicit_activation_grounds_once_and_session_start_reuses(self) -> None:
        session_id = "host-session-a"
        first = self.activate_session(session_id)
        second = self.activate_session(session_id)
        start = self.adapter.session_start(self.session_start_payload(session_id))

        self.assertEqual(first["status"], "activated")
        self.assertEqual(second["status"], "already_active")
        self.assertEqual(self.bootstrap_calls, 1)
        self.assertEqual(len(self.semantic_session_type.starts), 1)
        self.assertIn(
            "reusing",
            start["hookSpecificOutput"]["additionalContext"],
        )

    def test_failed_initial_activation_does_not_commit_binding(self) -> None:
        failing = MaintainHostAdapter(
            self.project_root,
            runtime_root=self.project_root / ".codex" / "failed-runtime",
            session_type=FailingStartSession,
            popen=self.popen,
            clock=self.clock,
        )
        with self.assertRaisesRegex(HarnessError, "previous session binding"):
            failing.activate("host-session-failure", "001-example")

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

        with self.assertRaisesRegex(HarnessError, "Which source is authoritative?"):
            adapter.activate("host-session-ambiguous", "001-example")
        session_directory = runtime_root / self.session_key("host-session-ambiguous")
        self.assertFalse((session_directory / "session.json").exists())

    def test_drain_reuses_exact_grounded_thread_for_later_turns(self) -> None:
        session_id = "host-session-thread-reuse"
        self.start_bound_session(session_id)

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
            self.semantic_session_type.restores,
            ["maintain-thread-1", "maintain-thread-1"],
        )
        self.assertEqual(
            [delta["turn_id"] for delta in self.semantic_session_type.deltas],
            ["turn-1", "turn-2"],
        )

    def test_no_change_has_no_workspace_write_or_notification(self) -> None:
        session_id = "host-session-no-change"
        before = self.workspace_bytes()
        self.start_bound_session(session_id)
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
        self.start_bound_session(session_id)
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-pair", "USER_MARKER")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-pair", "RESPONSE_MARKER")
        )

        self.adapter.drain(self.session_key(session_id))

        self.assertEqual(
            self.semantic_session_type.deltas,
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
        self.start_bound_session(session_id)
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-duplicate", "prompt")
        )
        payload = self.stop_payload(session_id, "turn-duplicate", "same response")
        self.adapter.response_end(payload)
        self.adapter.response_end(payload)

        first = self.adapter.drain(self.session_key(session_id))
        second = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(first["processed"], 1)
        self.assertEqual(second["processed"], 0)
        self.assertEqual(second["already_resolved"], 1)
        self.assertEqual(len(self.semantic_session_type.deltas), 1)
        self.assertEqual(len(self.apply_calls), 1)

    def test_two_host_sessions_keep_runtime_and_threads_isolated(self) -> None:
        for session_id in ("host-session-left", "host-session-right"):
            self.start_bound_session(session_id)
            self.adapter.user_prompt(
                self.prompt_payload(session_id, "turn-1", f"prompt {session_id}")
            )
            self.adapter.response_end(
                self.stop_payload(session_id, "turn-1", f"response {session_id}")
            )

        self.adapter.drain(self.session_key("host-session-right"))
        self.adapter.drain(self.session_key("host-session-left"))

        self.assertEqual(
            self.semantic_session_type.restores,
            ["maintain-thread-2", "maintain-thread-1"],
        )
        self.assertEqual(
            {delta["user_prompt"] for delta in self.semantic_session_type.deltas},
            {
                "prompt host-session-left",
                "prompt host-session-right",
            },
        )
        runtime_directories = {
            path.name for path in self.runtime_root.iterdir() if path.is_dir()
        }
        self.assertEqual(
            runtime_directories,
            {
                self.session_key("host-session-left"),
                self.session_key("host-session-right"),
            },
        )

    def test_concurrent_sessions_bind_different_workspaces_or_remain_unbound(
        self,
    ) -> None:
        self.add_workspace("002-other")
        left = "host-session-workspace-a"
        right = "host-session-workspace-b"
        unrelated = "host-session-unbound-c"

        self.activate_session(left, "001-example")
        self.activate_session(right, "002-other")
        self.adapter.user_prompt(self.prompt_payload(left, "left", "prompt A"))
        self.adapter.response_end(self.stop_payload(left, "left", "response A"))
        self.adapter.user_prompt(self.prompt_payload(right, "right", "prompt B"))
        self.adapter.response_end(self.stop_payload(right, "right", "response B"))
        self.adapter.user_prompt(
            self.prompt_payload(unrelated, "none", "unrelated prompt")
        )
        self.adapter.response_end(
            self.stop_payload(unrelated, "none", "unrelated response")
        )

        self.adapter.drain(self.session_key(right))
        self.adapter.drain(self.session_key(left))

        self.assertEqual(
            self.semantic_session_type.restore_bindings,
            [
                ("002-other", "maintain-thread-2"),
                ("001-example", "maintain-thread-1"),
            ],
        )
        self.assertEqual(self.adapter.status(left)["status"], "active")
        self.assertEqual(self.adapter.status(right)["status"], "active")
        self.assertEqual(self.adapter.status(unrelated)["status"], "unbound")
        self.assertFalse((self.runtime_root / self.session_key(unrelated)).exists())

    def test_same_session_rebind_keeps_current_turn_on_a_and_next_turn_on_b(
        self,
    ) -> None:
        self.add_workspace("002-other")
        session_id = "host-session-rebind-current-turn"
        self.activate_session(session_id, "001-example")
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-a", "prompt captured on A")
        )

        rebound = self.activate_session(session_id, "002-other")
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-a", "response completed after B")
        )
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-b", "next prompt on B")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-b", "next response on B")
        )
        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(rebound["previous_workspace_id"], "001-example")
        self.assertEqual(rebound["binding_generation"], 2)
        self.assertEqual(summary["processed"], 2)
        self.assertEqual(
            self.semantic_session_type.restore_bindings,
            [
                ("001-example", "maintain-thread-1"),
                ("002-other", "maintain-thread-2"),
            ],
        )
        self.assertEqual(
            [delta["workspace_id"] for delta in self.semantic_session_type.deltas],
            ["001-example", "002-other"],
        )

    def test_failed_successor_grounding_preserves_predecessor_binding(
        self,
    ) -> None:
        self.add_workspace("002-other")
        session_id = "host-session-failed-rebind"
        self.activate_session(session_id, "001-example")
        self.adapter.context.session_type = FailingSecondWorkspaceSession

        with self.assertRaisesRegex(
            HarnessError, "previous session binding was preserved"
        ):
            self.activate_session(session_id, "002-other")

        status = self.adapter.status(session_id)
        self.assertEqual(status["status"], "active")
        self.assertEqual(status["current_binding"]["workspace_id"], "001-example")
        self.assertEqual(status["current_binding"]["binding_generation"], 1)
        self.assertEqual(len(status["bindings"]), 1)

    def test_late_predecessor_event_uses_its_snapshotted_thread_after_rebind(
        self,
    ) -> None:
        self.add_workspace("002-other")
        session_id = "host-session-late-predecessor"
        self.activate_session(session_id, "001-example")
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "late-a", "late A prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "late-a", "late A response")
        )
        self.activate_session(session_id, "002-other")

        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(summary["processed"], 1)
        self.assertEqual(
            self.semantic_session_type.restore_bindings,
            [("001-example", "maintain-thread-1")],
        )
        self.assertEqual(
            self.semantic_session_type.deltas[0]["workspace_id"], "001-example"
        )

    def test_failed_predecessor_generation_does_not_block_successor(self) -> None:
        self.add_workspace("002-other")
        session_id = "host-session-generation-local-failure"
        self.activate_session(session_id, "001-example")
        for turn_id in ("a-failure", "a-later"):
            self.adapter.user_prompt(
                self.prompt_payload(session_id, turn_id, f"prompt {turn_id}")
            )
            self.adapter.response_end(
                self.stop_payload(session_id, turn_id, f"response {turn_id}")
            )
        self.semantic_session_type.resume_errors = [HarnessError("A failed")]
        first = self.adapter.drain(self.session_key(session_id))
        runtime_status = self.adapter.status(session_id)["runtime"]

        self.activate_session(session_id, "002-other")
        self.adapter.user_prompt(self.prompt_payload(session_id, "b-valid", "prompt B"))
        self.adapter.response_end(
            self.stop_payload(session_id, "b-valid", "response B")
        )
        second = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(first["failed"], 1)
        self.assertEqual(first["blocked"], 1)
        self.assertEqual(runtime_status["failed_effect_count"], 1)
        self.assertEqual(runtime_status["blocking_failure_count"], 1)
        self.assertEqual(runtime_status["unresolved_event_count"], 1)
        self.assertEqual(runtime_status["runnable_event_count"], 0)
        self.assertEqual(second["processed"], 1)
        self.assertEqual(second["blocked"], 1)
        self.assertEqual(
            self.semantic_session_type.restore_bindings[-1],
            ("002-other", "maintain-thread-2"),
        )
        self.assertEqual(
            self.semantic_session_type.deltas[-1]["workspace_id"], "002-other"
        )

    def test_repeat_rebind_a_to_b_to_a_creates_distinct_generations(self) -> None:
        self.add_workspace("002-other")
        session_id = "host-session-repeat-rebind"

        first = self.activate_session(session_id, "001-example")
        second = self.activate_session(session_id, "002-other")
        third = self.activate_session(session_id, "001-example")

        status = self.adapter.status(session_id)
        self.assertEqual(
            [
                first["binding_generation"],
                second["binding_generation"],
                third["binding_generation"],
            ],
            [1, 2, 3],
        )
        self.assertEqual(status["current_binding"]["workspace_id"], "001-example")
        self.assertEqual(status["current_binding"]["binding_generation"], 3)
        self.assertEqual(
            [binding["workspace_id"] for binding in status["bindings"]],
            ["001-example", "002-other", "001-example"],
        )
