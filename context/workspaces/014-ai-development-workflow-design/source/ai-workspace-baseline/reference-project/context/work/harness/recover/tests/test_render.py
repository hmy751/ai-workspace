"""Recover: 기존 텍스트 출력과 과거 status 표시를 검증한다."""

from __future__ import annotations

import json

from context.work.harness.testing import WorkspaceFixture


class RecoverRenderTests(WorkspaceFixture):
    def test_plain_output_renders_state_without_verify_configuration(self) -> None:
        completed = self.run_cli("recover")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("## state/status.json", completed.stdout)
        self.assertIn("- status: ready_for_verification", completed.stdout)
        self.assertIn("- result: null", completed.stdout)
        self.assertIn("- finished_at: null", completed.stdout)
        self.assertIn("- receipt: null", completed.stdout)
        self.assertNotIn("- next_action:", completed.stdout)
        self.assertIn("- receipt_freshness: not_applicable", completed.stdout)
        self.assertIn("## output/index.md", completed.stdout)
        self.assertIn("WORKSPACE_OUTPUT_INDEX", completed.stdout)
        self.assertNotIn("UNLOADED_OUTPUT_ARTIFACT_SECRET", completed.stdout)
        self.assertNotIn('"status": "ready_for_verification"', completed.stdout)
        self.assertNotIn("Fixed verification argv", completed.stdout)

    def test_plain_output_preserves_legacy_next_action(
        self,
    ) -> None:
        legacy_status = {
            "schema_version": 2,
            "workspace_id": "001-example",
            "status": "ready_for_verification",
            "result": None,
            "receipt": None,
            "finished_at": None,
            "next_action": "고정 검증을 실행한다.",
        }
        self.write_status(legacy_status)

        completed = self.run_cli("recover")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("- status: ready_for_verification", completed.stdout)
        self.assertIn("- next_action: 고정 검증을 실행한다.", completed.stdout)
