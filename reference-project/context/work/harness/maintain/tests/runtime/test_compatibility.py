"""legacy runtime 호환과 read-only status snapshot을 검증한다."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

from ..support.host import MaintainHostAdapterFixture


class MaintainHostCompatibilityTests(MaintainHostAdapterFixture):
    def test_legacy_v1_state_and_event_continue_as_generation_one(self) -> None:
        self.add_workspace("002-other")
        session_id = "host-session-legacy-v1-continuity"
        session_directory = self.runtime_root / self.session_key(session_id)
        (session_directory / "events").mkdir(parents=True)
        (session_directory / "session.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_id": "001-example",
                    "thread_id": "legacy-thread-a",
                    "grounded_at": 900.0,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        legacy_turn_id = "legacy-turn-a"
        legacy_turn_key = self.session_key(legacy_turn_id)
        (session_directory / "events" / f"{legacy_turn_key}.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "sequence": 1,
                    "turn_id": legacy_turn_id,
                    "user_prompt": "legacy A prompt",
                    "main_response": "legacy A response",
                    "accepted_at": 901.0,
                }
            )
            + "\n",
            encoding="utf-8",
        )

        rebound = self.activate_session(session_id, "002-other")
        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(rebound["binding_generation"], 2)
        self.assertEqual(summary["processed"], 1)
        self.assertEqual(
            self.semantic_session_type.restore_bindings,
            [("001-example", "legacy-thread-a")],
        )
        state = json.loads(
            (session_directory / "session.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state["schema_version"], 2)
        self.assertEqual(
            [binding["generation"] for binding in state["bindings"]],
            [1, 2],
        )

    def test_deactivate_keeps_captured_turn_on_old_binding_and_future_unbound(
        self,
    ) -> None:
        session_id = "host-session-deactivate"
        self.activate_session(session_id, "001-example")
        self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-before-off", "captured prompt")
        )

        result = self.adapter.deactivate(session_id)
        self.adapter.response_end(
            self.stop_payload(
                session_id,
                "turn-before-off",
                "response after deactivation",
            )
        )
        turns_directory = self.runtime_root / self.session_key(session_id) / "turns"
        before_turn_count = len(list(turns_directory.glob("*.json")))
        next_prompt = self.adapter.user_prompt(
            self.prompt_payload(session_id, "turn-after-off", "unbound prompt")
        )
        after_turn_count = len(list(turns_directory.glob("*.json")))
        summary = self.adapter.drain(self.session_key(session_id))

        self.assertEqual(result["status"], "deactivated")
        self.assertEqual(self.adapter.status(session_id)["status"], "unbound")
        self.assertEqual(next_prompt, {"continue": True})
        self.assertEqual(after_turn_count, before_turn_count)
        self.assertEqual(summary["processed"], 1)
        self.assertEqual(
            self.semantic_session_type.restore_bindings,
            [("001-example", "maintain-thread-1")],
        )

    def test_v1_project_config_never_auto_binds_a_new_session(self) -> None:
        (self.project_root / ".codex" / "maintain.json").write_text(
            json.dumps({"schema_version": 1, "workspace_id": "001-example"}) + "\n",
            encoding="utf-8",
        )
        session_id = "host-session-v1-config-unbound"

        output = self.adapter.session_start(self.session_start_payload(session_id))

        self.assertEqual(output, {"continue": True})
        self.assertFalse((self.runtime_root / self.session_key(session_id)).exists())
        self.assertEqual(self.semantic_session_type.starts, [])

    def test_status_retries_when_activation_adds_a_generation_mid_scan(
        self,
    ) -> None:
        self.add_workspace("002-other")
        session_id = "host-session-status-generation-race"
        self.activate_session(session_id, "001-example")
        original_runtime_status = self.adapter.status_reader._runtime_status
        calls = 0

        def racing_runtime_status(
            session_directory: Path,
            state: dict[str, Any],
        ) -> dict[str, Any]:
            nonlocal calls
            calls += 1
            if calls == 1:
                self.activate_session(session_id, "002-other")
                self.adapter.user_prompt(
                    self.prompt_payload(session_id, "turn-b-race", "prompt B")
                )
                self.adapter.response_end(
                    self.stop_payload(session_id, "turn-b-race", "response B")
                )
            return original_runtime_status(session_directory, state)

        with patch.object(
            self.adapter.status_reader,
            "_runtime_status",
            side_effect=racing_runtime_status,
        ):
            status = self.adapter.status(session_id)

        self.assertEqual(calls, 2)
        self.assertEqual(status["current_binding"]["workspace_id"], "002-other")
        self.assertEqual(status["current_binding"]["binding_generation"], 2)
        self.assertEqual(status["runtime"]["unresolved_event_count"], 1)
        self.assertEqual(
            status["runtime"]["by_generation"][1]["unresolved_event_count"],
            1,
        )

    def test_status_reports_unattributed_legacy_failure_explicitly(self) -> None:
        session_id = "host-session-unassigned-legacy-failure"
        self.activate_session(session_id, "001-example")
        session_directory = self.runtime_root / self.session_key(session_id)
        effect_key = self.session_key("missing-legacy-boundary")
        effects_directory = session_directory / "effects"
        effects_directory.mkdir()
        (effects_directory / f"{effect_key}.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "failed",
                    "finished_at": 901.0,
                    "error": "legacy failure without event or turn",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        runtime = self.adapter.status(session_id)["runtime"]

        self.assertEqual(runtime["failed_effect_count"], 1)
        self.assertEqual(runtime["unassigned_failed_effect_count"], 1)
        self.assertEqual(runtime["unassigned_failed_effect_keys"], [effect_key])
        self.assertEqual(runtime["by_generation"][0]["failed_effect_count"], 0)
