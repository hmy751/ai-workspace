"""Verify: receipt의 형식·인계·불변성을 검증한다."""

from __future__ import annotations

import hashlib
import json

from .support import VerifyFixture


class VerifyReceiptsTests(VerifyFixture):
    def test_reads_legacy_status_then_writes_machine_only_status(self) -> None:
        self.write_status(
            {
                "schema_version": 2,
                "workspace_id": "001-example",
                "status": "ready_for_verification",
                "result": None,
                "receipt": None,
                "finished_at": None,
                "next_action": "고정 검증을 실행한다.",
            }
        )

        completed = self.run_cli("verify", "001-example")

        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        status = self.read_status()
        self.assertEqual(status["schema_version"], 3)
        self.assertEqual(status["status"], "verification_failed")
        self.assertNotIn("next_action", status)

    def test_persists_failure_then_pass_without_completing_or_overwriting(self) -> None:
        state_index_path = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "current"
            / "state"
            / "index.md"
        )
        status_path = state_index_path.parent / "status.json"
        original_state_index = state_index_path.read_bytes()
        old_record = (
            self.work_root / "workspaces" / "001-example" / "records" / "old.json"
        )
        original_old_record = old_record.read_bytes()

        failed = self.run_cli("verify")

        self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
        failed_summary = json.loads(failed.stdout)
        self.assertEqual(failed_summary["status"], "verification_failed")
        failed_status = self.read_status()
        self.assertEqual(failed_status["status"], "verification_failed")
        self.assertEqual(failed_status["schema_version"], 3)
        self.assertEqual(failed_status["result"], "fail")
        self.assertNotIn("next_action", failed_status)
        self.assertEqual(state_index_path.read_bytes(), original_state_index)

        receipts_after_failure = self.receipt_files()
        self.assertEqual(len(receipts_after_failure), 1)
        failed_receipt_bytes = receipts_after_failure[0].read_bytes()
        failed_receipt = json.loads(failed_receipt_bytes)
        self.assertEqual(failed_receipt["exit_code"], failed.returncode)
        self.assertEqual(failed_receipt["result"], "fail")
        self.assertEqual(failed_receipt["schema_version"], 2)
        self.assertEqual(failed_receipt["workspace_id"], "001-example")
        self.assertEqual(failed_receipt["claim"], self.verify_contract["claim"])
        self.assertIsInstance(failed_receipt["started_at"], str)
        self.assertIsInstance(failed_receipt["finished_at"], str)
        self.assertIsInstance(failed_receipt["stdout"], str)
        self.assertIsInstance(failed_receipt["stderr"], str)
        self.assertEqual(failed_receipt["evidence_capture"], "before_verification")
        self.assertEqual(failed_status["finished_at"], failed_receipt["finished_at"])
        self.assertEqual(
            failed_receipt["argv"], self.verify_contract["verification"]["argv"]
        )
        self.assertEqual(
            [item["path"] for item in failed_receipt["evidence_files"]],
            self.verify_contract["verification"]["evidence_paths"],
        )
        self.assertEqual(
            [item["path"] for item in failed_receipt["canonical_basis_files"]],
            self.verify_contract["canonical_basis"],
        )
        self.assertEqual(
            failed_receipt["canonical_basis_capture"],
            "before_verification",
        )
        self.assertEqual(
            failed_receipt["canonical_basis_collected_at"],
            failed_receipt["evidence_collected_at"],
        )
        runtime = failed_receipt["runtime_environment"]
        self.assertEqual(runtime["command_cwd"], "<OUTPUT_ROOT>")
        self.assertIsInstance(runtime["python_version"], str)
        self.assertIsInstance(runtime["python_implementation"], str)
        self.assertIsInstance(runtime["platform_system"], str)
        self.assertEqual(runtime["verify_contract_schema_version"], 2)
        self.assertEqual(runtime["verification_receipt_schema_version"], 2)
        expected_snapshot = json.dumps(
            {
                "canonical_basis_files": failed_receipt["canonical_basis_files"],
                "evidence_files": failed_receipt["evidence_files"],
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        self.assertEqual(
            failed_receipt["snapshot_sha256"],
            hashlib.sha256(expected_snapshot).hexdigest(),
        )
        self.assertNotIn("next_action", failed_receipt)

        evidence_path = self.project_root / "src" / "value.txt"
        evidence_path.write_text("expected\n", encoding="utf-8")
        passed = self.run_cli("verify")

        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        passed_summary = json.loads(passed.stdout)
        self.assertEqual(passed_summary["status"], "verification_passed")
        self.assertNotEqual(passed_summary["status"], "completed")
        self.assertEqual(passed_summary["claim"], self.verify_contract["claim"])
        self.assertNotIn("next_action", passed_summary)
        passed_status = self.read_status()
        self.assertEqual(passed_status["status"], "verification_passed")
        self.assertEqual(passed_status["result"], "pass")
        self.assertNotEqual(passed_status["status"], "completed")
        self.assertNotIn("next_action", passed_status)
        self.assertEqual(state_index_path.read_bytes(), original_state_index)
        self.assertEqual(old_record.read_bytes(), original_old_record)

        receipts_after_pass = self.receipt_files()
        self.assertEqual(len(receipts_after_pass), 2)
        self.assertNotEqual(receipts_after_pass[0].name, receipts_after_pass[1].name)
        self.assertEqual(receipts_after_failure[0].read_bytes(), failed_receipt_bytes)
        passed_receipt = next(
            json.loads(path.read_text(encoding="utf-8"))
            for path in receipts_after_pass
            if json.loads(path.read_text(encoding="utf-8"))["result"] == "pass"
        )
        value_evidence = next(
            item
            for item in passed_receipt["evidence_files"]
            if item["path"] == "src/value.txt"
        )
        expected_bytes = b"expected\n"
        self.assertEqual(value_evidence["size"], len(expected_bytes))
        self.assertEqual(
            value_evidence["sha256"], hashlib.sha256(expected_bytes).hexdigest()
        )
        self.assertEqual(passed_status["receipt"], passed_summary["receipt"])
        temporary_status_files = list(status_path.parent.glob(".status.json.*.tmp"))
        self.assertEqual(temporary_status_files, [])
        temporary_receipt_files = list(
            receipts_after_pass[0].parent.glob(".verify-receipt-*.tmp")
        )
        self.assertEqual(temporary_receipt_files, [])
