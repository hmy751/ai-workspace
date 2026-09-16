"""Maintain test_bootstrap 시나리오."""

from __future__ import annotations

from context.work.harness.maintain import bootstrap_workspace
from context.work.harness.workspace_contract import HarnessError

from ..support.apply import MaintainApplyFixture


class TestBootstrap(MaintainApplyFixture):
    def test_bootstrap_is_explicit_and_bounded_by_recover(self) -> None:
        (self.work_root / "workspaces" / "index.json").write_text(
            "not valid json\n", encoding="utf-8"
        )

        packet = bootstrap_workspace(self.project_root, self.work_root, "001-example")

        self.assertEqual(packet["workspace_id"], "001-example")
        self.assertNotIn(
            "workspaces/index.json",
            [entry["path"] for entry in packet["control_paths"]],
        )
        serialized = repr(packet)
        for excluded in (
            "UNLOADED_RECORD_SECRET",
            "UNLOADED_RECORD_MARKDOWN_SECRET",
            "UNLOADED_SOURCE_INVENTORY_SECRET",
            "UNLOADED_SOURCE_RAW_SECRET",
            "UNLOADED_OUTPUT_ARTIFACT_SECRET",
            "UNSELECTED_PROJECT_GUIDANCE",
            "UNSELECTED_PROJECT_DECISIONS_ROUTING",
        ):
            self.assertNotIn(excluded, serialized)
        with self.assertRaises(HarnessError):
            bootstrap_workspace(self.project_root, self.work_root, None)  # type: ignore[arg-type]
