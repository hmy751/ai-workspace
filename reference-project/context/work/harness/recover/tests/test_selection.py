"""Recover: 명시한 id와 active 선택의 권한 경계를 검증한다."""

from __future__ import annotations

import copy
import json

from context.work.harness.testing import WorkspaceFixture


class RecoverSelectionTests(WorkspaceFixture):
    def test_explicit_workspace_does_not_require_or_read_active_index(
        self,
    ) -> None:
        index_path = self.work_root / "workspaces" / "index.json"
        index_path.write_text("{not-json\n", encoding="utf-8")

        malformed = self.run_cli("recover", "001-example", "--json")

        self.assertEqual(malformed.returncode, 0, malformed.stderr)
        packet = json.loads(malformed.stdout)
        self.assertNotIn(
            {"path_base": "work_root", "path": "workspaces/index.json"},
            packet["control_paths"],
        )

        index_path.unlink()
        missing = self.run_cli("recover", "001-example", "--json")

        self.assertEqual(missing.returncode, 0, missing.stderr)
        packet = json.loads(missing.stdout)
        self.assertEqual(packet["workspace_id"], "001-example")
        self.assertNotIn("workspaces/index.json", missing.stdout)

    def test_active_workspace_fallback_still_validates_index(self) -> None:
        index_path = self.work_root / "workspaces" / "index.json"
        index_path.write_text("{not-json\n", encoding="utf-8")

        malformed = self.run_cli("recover")

        self.assertEqual(malformed.returncode, 2)
        self.assertIn("Workspace index is not valid JSON", malformed.stderr)

    def test_rejects_workspace_identity_extra_responsibility(self) -> None:
        identity = copy.deepcopy(self.identity)
        identity["project_context"] = []
        self.write_work_json("workspaces/001-example/workspace.json", identity)

        completed = self.run_cli("recover")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("Workspace identity keys", completed.stderr)
        self.assertIn("extra", completed.stderr)
