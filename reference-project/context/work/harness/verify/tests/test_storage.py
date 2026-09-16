"""Atomic status 교체와 append-only receipt의 저장 오류를 검증한다."""

from __future__ import annotations

import json
from unittest.mock import patch

from context.work.harness.testing import WorkspaceFixture
from context.work.harness.verify import storage
from context.work.harness.workspace import HarnessError, select_workspace


class VerifyStorageTests(WorkspaceFixture):
    def test_atomic_replace_failure_preserves_status_and_removes_staging_file(
        self,
    ) -> None:
        path = self.work_root / "workspaces/001-example/current/state/status.json"
        before = path.read_bytes()
        with patch.object(storage.os, "replace", side_effect=OSError("replace failed")):
            with self.assertRaisesRegex(OSError, "replace failed"):
                storage.atomic_write_status(path, '{"replacement": true}\n')
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(list(path.parent.glob(".status.json.*.tmp")), [])

    def test_receipt_collision_never_overwrites_existing_evidence(self) -> None:
        identity = select_workspace(self.work_root, "001-example")
        relative, directory = storage.resolve_verify_receipts_directory(
            self.work_root, identity
        )
        previous = directory / "verify-existing.json"
        previous.write_text("old receipt\n", encoding="utf-8")
        with patch.object(storage.os, "link", side_effect=FileExistsError) as link:
            with self.assertRaisesRegex(HarnessError, "append-only"):
                storage.write_receipt(relative, directory, {"result": "pass"})
            self.assertEqual(link.call_count, 5)
        self.assertEqual(previous.read_text(encoding="utf-8"), "old receipt\n")
        self.assertEqual(list(directory.glob(".verify-receipt-*.tmp")), [])
        self.assertEqual(list(directory.glob("verify-*.json")), [previous])

    def test_receipt_link_failure_is_not_misreported_as_a_collision(self) -> None:
        identity = select_workspace(self.work_root, "001-example")
        relative, directory = storage.resolve_verify_receipts_directory(
            self.work_root, identity
        )
        with patch.object(
            storage.os, "link", side_effect=OSError("link failed")
        ) as link:
            with self.assertRaisesRegex(OSError, "link failed"):
                storage.write_receipt(relative, directory, {"result": "pass"})
            link.assert_called_once()
        self.assertEqual(self.receipt_files(), [])
        self.assertEqual(list(directory.glob(".verify-receipt-*.tmp")), [])

    def test_successful_receipt_is_complete_before_returning_its_cursor(self) -> None:
        identity = select_workspace(self.work_root, "001-example")
        relative, directory = storage.resolve_verify_receipts_directory(
            self.work_root, identity
        )
        payload = {"result": "pass", "claim": "선확보된 파일을 검증한다."}
        cursor = storage.write_receipt(relative, directory, payload)
        self.assertEqual(
            json.loads((self.work_root / cursor).read_text(encoding="utf-8")), payload
        )
        self.assertEqual(list(directory.glob(".verify-receipt-*.tmp")), [])
