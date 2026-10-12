"""Recover: 상태 인계 계약 위반을 거부하는지 검증한다."""

from __future__ import annotations

import json

from context.work.harness.testing import WorkspaceFixture


class RecoverStatusTests(WorkspaceFixture):
    def test_rejects_invalid_state_status(self) -> None:
        legacy_schema = self.initial_status()
        legacy_schema["schema_version"] = 1
        self.write_status(legacy_schema)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("schema_version", completed.stderr)

        inconsistent = self.initial_status()
        inconsistent["status"] = "verification_passed"
        self.write_status(inconsistent)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("inconsistent", completed.stderr)

        wrong_type = self.initial_status()
        wrong_type["status"] = ["ready_for_verification"]
        self.write_status(wrong_type)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("invalid Workspace state status", completed.stderr)

        legacy_with_current_status = {
            "schema_version": 2,
            "workspace_id": "001-example",
            "status": "verification_passed",
            "result": "pass",
            "receipt": "workspaces/001-example/records/verify-existing.json",
            "finished_at": "2026-08-13T00:00:00.000Z",
            "next_action": "receipt를 검토한다.",
        }
        self.write_status(legacy_with_current_status)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("invalid Workspace state status", completed.stderr)

        current_with_legacy_key = {
            "schema_version": 3,
            "workspace_id": "001-example",
            "status": "ready_for_verification",
            "result": None,
            "receipt": None,
            "finished_at": None,
            "next_action": "v3에는 이 필드가 없다.",
        }
        self.write_status(current_with_legacy_key)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("extra=['next_action']", completed.stderr)

    def test_rejects_missing_malformed_and_symlinked_status(self) -> None:
        status_path = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "current"
            / "state"
            / "status.json"
        )
        status_path.unlink()

        missing = self.run_cli("recover")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("does not exist", missing.stderr)

        status_path.write_text("{not-json\n", encoding="utf-8")
        malformed = self.run_cli("recover")
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("not valid JSON", malformed.stderr)

        status_path.unlink()
        outside_status = self.project_root / "context" / "project" / "status.json"
        outside_status.write_text(json.dumps(self.initial_status()), encoding="utf-8")
        status_path.symlink_to(outside_status)
        linked = self.run_cli("recover")
        self.assertEqual(linked.returncode, 2)
        self.assertIn("symlink", linked.stderr)
