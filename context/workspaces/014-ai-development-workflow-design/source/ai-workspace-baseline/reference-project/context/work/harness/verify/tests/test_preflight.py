"""Verify: 명령 부작용 전에 입력과 저장 경로를 검사하는지 검증한다."""

from __future__ import annotations

import copy
import json
import unittest

from .support import VerifyFixture


class VerifyPreflightTests(VerifyFixture):
    verification_scenarios = ("delete_evidence",)

    def test_validates_status_before_running_command(self) -> None:
        status_path = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "current"
            / "state"
            / "status.json"
        )
        status_path.write_text("{not-json\n", encoding="utf-8")

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("not valid JSON", completed.stderr)
        self.assertEqual(self.receipt_files(), [])
        self.assertEqual(
            (self.project_root / "src" / "value.txt").read_text(encoding="utf-8"),
            "wrong\n",
        )

        self.write_status(
            self.verified_status(
                "workspaces/001-example/records/receipts/harness-tests/"
                "verify-harness.json"
            )
        )

        wrong_receipt_type = self.run_cli("verify")

        self.assertEqual(wrong_receipt_type.returncode, 2)
        self.assertIn("product Verify receipt", wrong_receipt_type.stderr)
        self.assertEqual(self.receipt_files(), [])
        self.assertEqual(
            (self.project_root / "src" / "value.txt").read_text(encoding="utf-8"),
            "wrong\n",
        )

    def test_requires_verify_receipts_directory_before_running_command(self) -> None:
        receipts = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "records"
            / "receipts"
            / "verify"
        )
        receipts.rmdir()
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"]["argv"] = [
            "python3",
            "-m",
            "unittest",
            "tests.test_delete_evidence",
            "-v",
        ]
        self.write_work_json("workspaces/001-example/verify.json", contract)

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("verify receipts directory does not exist", completed.stderr)
        self.assertTrue((self.project_root / "src" / "value.txt").exists())

    def test_rejects_symlinked_verify_receipts_directory_before_command(self) -> None:
        receipts = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "records"
            / "receipts"
            / "verify"
        )
        receipts.rmdir()
        outside = self.project_root / "outside-verify-receipts"
        outside.mkdir()
        receipts.symlink_to(outside, target_is_directory=True)
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"]["argv"] = [
            "python3",
            "-m",
            "unittest",
            "tests.test_delete_evidence",
            "-v",
        ]
        self.write_work_json("workspaces/001-example/verify.json", contract)

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("must not use symlink components", completed.stderr)
        self.assertTrue((self.project_root / "src" / "value.txt").exists())
        self.assertEqual(list(outside.iterdir()), [])
