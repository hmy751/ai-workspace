"""semantic·apply 실패의 차단 범위와 effect-once 동작을 검증한다."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from context.work.harness.maintain.host_adapter import MaintainHostAdapter
from context.work.harness.maintain.operation import bootstrap_workspace
from context.work.harness.workspace_contract import HarnessError

from ..support.host import MaintainHostAdapterFixture


class MaintainHostFailureOrderingTests(MaintainHostAdapterFixture):
    def test_failure_is_effect_once_but_never_recorded_as_completed(self) -> None:
        session_id = "host-session-failure"
        self.start_bound_session(session_id)
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-failure", "prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-failure", "response")
        )
        self.semantic_session_type.resume_errors = [HarnessError("semantic crash")]

        first = self.adapter.drain(self.session_key(session_id))
        second = self.adapter.drain(self.session_key(session_id))
        next_prompt = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-after-failure", "what happened?")
        )

        self.assertEqual(first["failed"], 1)
        self.assertEqual(second["already_resolved"], 1)
        self.assertEqual(len(self.semantic_session_type.deltas), 1)
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

    def test_semantic_failure_keeps_later_events_pending_without_rekick(
        self,
    ) -> None:
        session_id = "host-session-blocked-after-semantic-failure"
        self.start_bound_session(session_id)
        before = self.workspace_bytes()

        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-failure", "first prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-failure", "first response")
        )
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-later", "later prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-later", "later response")
        )
        self.semantic_session_type.resume_errors = [HarnessError("semantic crash")]

        first = self.adapter.drain(self.session_key(session_id))
        second = self.adapter.drain(self.session_key(session_id))
        popen_count = len(self.popen.calls)
        attention = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-attention", "what is pending?")
        )

        self.assertEqual(first["failed"], 1)
        self.assertEqual(first["blocked"], 1)
        self.assertEqual(first["processed"], 0)
        self.assertEqual(second["already_resolved"], 1)
        self.assertEqual(second["blocked"], 1)
        self.assertEqual(len(self.semantic_session_type.deltas), 1)
        self.assertEqual(self.apply_calls, [])
        self.assertEqual(self.workspace_bytes(), before)
        self.assertEqual(len(self.popen.calls), popen_count)

        effects_directory = (
            self.runtime_root
            / self.session_key(session_id)
            / "effects"
        )
        failed_key = self.session_key("turn-failure")
        later_key = self.session_key("turn-later")
        failed_effect = json.loads(
            (effects_directory / f"{failed_key}.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIs(failed_effect["blocks_later_events"], True)
        self.assertFalse((effects_directory / f"{later_key}.json").exists())
        context = attention["hookSpecificOutput"]["additionalContext"]
        self.assertIn("remain pending behind a failed semantic", context)
        self.assertIn("will not be retried on the affected binding", context)

        popen_count = len(self.popen.calls)
        ending = self.adapter.session_end(
            {
                "hook_event_name": "SessionEnd",
                "session_id": session_id,
                "cwd": "/unused/by-direct-test",
                "reason": "complete",
            }
        )
        self.assertEqual(len(self.popen.calls), popen_count)
        end_context = ending["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Later events remain pending", end_context)
        self.assertIn("binding generation and were not retried", end_context)

    def test_apply_failure_blocks_later_event(self) -> None:
        apply_attempts: list[dict[str, object]] = []

        def failing_apply(
            project_root: Path,
            work_root: Path,
            workspace_id: str,
            decision: dict[str, object],
        ) -> dict[str, Any]:
            apply_attempts.append(decision)
            raise HarnessError("guarded apply crash")

        adapter = MaintainHostAdapter(
            self.project_root,
            runtime_root=self.runtime_root,
            session_type=self.semantic_session_type,
            runner=lambda *args, **kwargs: None,
            popen=self.popen,
            clock=self.clock,
            python_executable="fixture-python",
            bootstrap=bootstrap_workspace,
            apply_decision=failing_apply,
        )
        session_id = "host-session-blocked-after-apply-failure"
        adapter.activate(session_id, "001-example")
        adapter.user_prompt(
            self.prompt_payload(session_id, "turn-failure", "first prompt")
        )
        adapter.response_end(
            self.stop_payload(session_id, "turn-failure", "first response")
        )
        adapter.user_prompt(
            self.prompt_payload(session_id, "turn-later", "later prompt")
        )
        adapter.response_end(
            self.stop_payload(session_id, "turn-later", "later response")
        )

        summary = adapter.drain(self.session_key(session_id))

        self.assertEqual(summary["failed"], 1)
        self.assertEqual(summary["blocked"], 1)
        self.assertEqual(len(apply_attempts), 1)
        self.assertEqual(len(self.semantic_session_type.deltas), 1)

    def test_legacy_failed_effect_blocks_later_event_fail_closed(self) -> None:
        session_id = "host-session-legacy-failure"
        self.start_bound_session(session_id)
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-failure", "first prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-failure", "first response")
        )
        self.semantic_session_type.resume_errors = [HarnessError("legacy crash")]
        self.adapter.drain(self.session_key(session_id))

        effect_path = (
            self.runtime_root
            / self.session_key(session_id)
            / "effects"
            / f"{self.session_key('turn-failure')}.json"
        )
        legacy_effect = json.loads(effect_path.read_text(encoding="utf-8"))
        del legacy_effect["blocks_later_events"]
        effect_path.write_text(
            json.dumps(legacy_effect) + "\n", encoding="utf-8"
        )

        popen_count = len(self.popen.calls)
        attention = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-later", "later prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-later", "later response")
        )
        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(summary["already_resolved"], 1)
        self.assertEqual(summary["blocked"], 1)
        self.assertEqual(len(self.semantic_session_type.deltas), 1)
        self.assertEqual(len(self.popen.calls), popen_count)
        context = attention["hookSpecificOutput"]["additionalContext"]
        self.assertIn("paused on at least one binding generation", context)

    def test_unpaired_event_failure_does_not_block_later_semantic_event(
        self,
    ) -> None:
        session_id = "host-session-nonblocking-pairing-failure"
        session_directory = self.runtime_root / self.session_key(session_id)
        session_directory.mkdir(parents=True)
        (session_directory / "session.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_id": "001-example",
                    "thread_id": "legacy-unpaired-thread",
                    "grounded_at": 900.0,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.adapter.response_end(
            self.stop_payload(
                session_id,
                "turn-without-prompt",
                "response without a captured prompt",
            )
        )
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-valid", "valid prompt")
        )
        self.adapter.response_end(
            self.stop_payload(session_id, "turn-valid", "valid response")
        )

        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(summary["failed"], 1)
        self.assertEqual(summary["processed"], 1)
        self.assertEqual(summary["blocked"], 0)
        self.assertEqual(len(self.semantic_session_type.deltas), 1)
        self.assertEqual(
            self.semantic_session_type.deltas[0]["turn_id"], "turn-valid"
        )
        failed_effect = json.loads(
            (
                self.runtime_root
                / self.session_key(session_id)
                / "effects"
                / f"{self.session_key('turn-without-prompt')}.json"
            ).read_text(encoding="utf-8")
        )
        self.assertIs(failed_effect["blocks_later_events"], False)
