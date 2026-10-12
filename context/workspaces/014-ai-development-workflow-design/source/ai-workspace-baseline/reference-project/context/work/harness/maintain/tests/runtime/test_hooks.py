"""prompt·response-end·session-end hook의 접수와 사용자 전달을 검증한다."""

from __future__ import annotations

import hashlib
import json

from ..support.host import MaintainHostAdapterFixture
from ..support.semantic import FailingPopen


class MaintainHostHookLifecycleTests(MaintainHostAdapterFixture):
    def test_initial_activation_does_not_capture_the_unbound_current_turn(
        self,
    ) -> None:
        session_id = "host-session-initial-cutover"
        self.adapter.user_prompt(
            self.prompt_payload(
                session_id, "turn-unbound", "activate during this response"
            )
        )

        self.activate_session(session_id, "001-example")
        stop = self.adapter.response_end(
            self.stop_payload(
                session_id,
                "turn-unbound",
                "activation command ran in this response",
            )
        )
        session_directory = self.runtime_root / self.session_key(session_id)
        events_directory = session_directory / "events"

        self.assertEqual(stop, {"continue": True})
        self.assertFalse(events_directory.exists())
        self.assertEqual(self.popen.calls, [])

        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-bound", "next prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-bound", "next response")
        )
        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(summary["processed"], 1)
        self.assertEqual(
            [delta["turn_id"] for delta in self.semantic_session_type.deltas],
            ["turn-bound"],
        )

    def test_ambiguity_and_important_update_surface_on_next_prompt(self) -> None:
        session_id = "host-session-notifications"
        self.start_bound_session(session_id)
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-ambiguity", "choose source")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-ambiguity", "Which source?")
        )
        self.semantic_session_type.decisions = [
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
        self.semantic_session_type.decisions = [
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
        important_context = important_output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("updated Workspace", important_context)
        self.assertIn("current/state/index.md", important_context)

    def test_response_end_only_enqueues_and_starts_detached_drain(self) -> None:
        session_id = "host-session-detached"
        self.start_bound_session(session_id)
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-detached", "prompt")
        )

        self.adapter.response_end(
            self.stop_payload(session_id, "turn-detached", "response")
        )

        self.assertEqual(self.semantic_session_type.deltas, [])
        self.assertEqual(len(self.popen.calls), 1)
        command, options = self.popen.calls[0]
        self.assertIn("drain", command)
        self.assertTrue(options["start_new_session"])
        event_directory = self.runtime_root / self.session_key(session_id) / "events"
        self.assertEqual(len(list(event_directory.glob("*.json"))), 1)

    def test_next_prompt_exposes_prior_prompt_without_response_end_once(self) -> None:
        session_id = "host-session-orphan-prompt"
        self.start_bound_session(session_id)
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
        effect_directory = self.runtime_root / self.session_key(session_id) / "effects"
        effects = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in effect_directory.glob("*.json")
        ]
        self.assertEqual([effect["status"] for effect in effects], ["failed"])
        self.assertEqual(effects[0]["binding_generation"], 1)
        self.assertEqual(effects[0]["workspace_id"], "001-example")
        runtime = self.adapter.status(session_id)["runtime"]
        self.assertEqual(runtime["failed_effect_count"], 1)
        self.assertEqual(runtime["unassigned_failed_effect_count"], 0)
        self.assertEqual(runtime["by_generation"][0]["failed_effect_count"], 1)
        self.assertEqual(self.semantic_session_type.deltas, [])

    def test_session_end_exposes_prompt_without_response_end(self) -> None:
        session_id = "host-session-end-orphan"
        self.start_bound_session(session_id)
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
                self.runtime_root / self.session_key(session_id) / "session-end.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(len(session_end["orphan_prompt_keys"]), 1)
        self.assertEqual(session_end["unresolved_event_keys"], [])

    def test_later_user_prompt_rekicks_an_unresolved_response_end(self) -> None:
        session_id = "host-session-rekick"
        self.start_bound_session(session_id)
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
        self.adapter.context.popen = failing_popen
        self.start_bound_session(session_id)
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
