"""Verify: 명령이 파일을 삭제해도 실행 전 evidence를 남기는지 검증한다."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest

from .support import VerifyFixture


class VerifyEvidenceTests(VerifyFixture):
    verification_scenarios = ("delete_evidence",)

    def test_captures_evidence_before_command_deletes_it(self) -> None:
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"]["argv"] = [
            "python3",
            "-m",
            "unittest",
            "tests.test_delete_evidence",
            "-v",
        ]
        self.write_work_json("workspaces/001-example/verify.json", contract)
        expected_bytes = b"wrong\n"

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["status"], "verification_failed")
        self.assertFalse((self.project_root / "src" / "value.txt").exists())
        receipt_files = self.receipt_files()
        self.assertEqual(len(receipt_files), 1)
        receipt = json.loads(receipt_files[0].read_text(encoding="utf-8"))
        self.assertEqual(receipt["exit_code"], 1)
        self.assertEqual(receipt["result"], "fail")
        value_evidence = next(
            item
            for item in receipt["evidence_files"]
            if item["path"] == "src/value.txt"
        )
        self.assertEqual(value_evidence["size"], len(expected_bytes))
        self.assertEqual(
            value_evidence["sha256"], hashlib.sha256(expected_bytes).hexdigest()
        )
        status = self.read_status()
        self.assertEqual(status["receipt"], summary["receipt"])
        self.assertEqual(status["finished_at"], receipt["finished_at"])

    def test_captures_canonical_basis_before_command_deletes_it(self) -> None:
        basis_path = (
            self.project_root / "context" / "project" / "common" / "task-context.md"
        )
        expected_bytes = basis_path.read_bytes()
        delete_basis_test = self.project_root / "tests" / "test_delete_basis.py"
        delete_basis_test.write_text(
            "from pathlib import Path\n"
            "import unittest\n\n"
            "class DeleteBasisTests(unittest.TestCase):\n"
            "    def test_delete_then_fail(self):\n"
            "        Path('context/project/common/task-context.md').unlink()\n"
            "        self.fail('intentional failure after basis deletion')\n",
            encoding="utf-8",
        )
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"]["argv"] = [
            "python3",
            "-m",
            "unittest",
            "tests.test_delete_basis",
            "-v",
        ]
        self.write_work_json("workspaces/001-example/verify.json", contract)

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        self.assertFalse(basis_path.exists())
        receipt = json.loads(self.receipt_files()[0].read_text(encoding="utf-8"))
        basis_snapshot = receipt["canonical_basis_files"][0]
        self.assertEqual(
            basis_snapshot["path"],
            "context/project/common/task-context.md",
        )
        self.assertEqual(basis_snapshot["size"], len(expected_bytes))
        self.assertEqual(
            basis_snapshot["sha256"], hashlib.sha256(expected_bytes).hexdigest()
        )
