from __future__ import annotations

import copy
import hashlib
import json

from context.work.harness.tests.support import WorkspaceFixture


class VerifyTests(WorkspaceFixture):
    def test_runs_when_recover_contract_is_invalid(self) -> None:
        recover_path = (
            self.work_root / "workspaces" / "001-example" / "recover.json"
        )
        recover_path.write_text(
            '{"project_context": "INVALID_RECOVER_CONTRACT_SECRET"\n',
            encoding="utf-8",
        )
        original_recover = recover_path.read_bytes()
        (self.project_root / "src" / "value.txt").write_text(
            "expected\n", encoding="utf-8"
        )

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertNotIn("INVALID_RECOVER_CONTRACT_SECRET", completed.stdout)
        self.assertEqual(recover_path.read_bytes(), original_recover)

    def test_uses_project_root_for_evidence_and_command_cwd(self) -> None:
        decoy_src = self.work_root / "src"
        decoy_tests = self.work_root / "tests"
        decoy_src.mkdir()
        decoy_tests.mkdir()
        (decoy_src / "value.txt").write_text(
            "expected\n", encoding="utf-8"
        )
        (decoy_tests / "__init__.py").write_text("", encoding="utf-8")
        (decoy_tests / "test_behavior.py").write_text(
            "from pathlib import Path\n"
            "import unittest\n\n"
            "class BehaviorTests(unittest.TestCase):\n"
            "    def test_value(self):\n"
            "        self.assertEqual(\n"
            "            Path('src/value.txt').read_text(encoding='utf-8'),\n"
            "            'expected\\n',\n"
            "        )\n",
            encoding="utf-8",
        )

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 1, completed.stdout)
        receipt = json.loads(self.receipt_files()[0].read_text(encoding="utf-8"))
        value_evidence = next(
            item
            for item in receipt["evidence_files"]
            if item["path"] == "src/value.txt"
        )
        self.assertEqual(
            value_evidence["sha256"], hashlib.sha256(b"wrong\n").hexdigest()
        )

    def test_rejects_verify_only_argv_limits_and_paths(self) -> None:
        invalid_contracts: list[tuple[dict[str, object], str]] = []

        shell_string = copy.deepcopy(self.verify_contract)
        shell_string["verification"]["argv"] = "python3 -m unittest"
        invalid_contracts.append((shell_string, "shell string"))

        shell_argv = copy.deepcopy(self.verify_contract)
        shell_argv["verification"]["argv"] = ["sh", "-c", "exit 0"]
        invalid_contracts.append((shell_argv, "shell"))

        env_argv = copy.deepcopy(self.verify_contract)
        env_argv["verification"]["argv"] = ["env", "python3", "-V"]
        invalid_contracts.append((env_argv, "env trampoline"))

        embedded_absolute = copy.deepcopy(self.verify_contract)
        embedded_absolute["verification"]["argv"] = [
            "python3",
            "--config=/tmp/outside.json",
        ]
        invalid_contracts.append((embedded_absolute, "absolute"))

        traversal = copy.deepcopy(self.verify_contract)
        traversal["verification"]["argv"] = ["python3", "../outside.py"]
        invalid_contracts.append((traversal, "traversal"))

        invalid_timeout = copy.deepcopy(self.verify_contract)
        invalid_timeout["verification"]["timeout_seconds"] = 0
        invalid_contracts.append((invalid_timeout, "timeout_seconds"))

        invalid_output_cap = copy.deepcopy(self.verify_contract)
        invalid_output_cap["verification"]["max_output_chars"] = 1_000_001
        invalid_contracts.append((invalid_output_cap, "max_output_chars"))

        evidence_traversal = copy.deepcopy(self.verify_contract)
        evidence_traversal["verification"]["evidence_paths"] = ["../outside"]
        invalid_contracts.append((evidence_traversal, "traverse"))

        for invalid_contract, expected_error in invalid_contracts:
            with self.subTest(expected_error=expected_error):
                self.write_work_json(
                    "workspaces/001-example/verify.json", invalid_contract
                )
                completed = self.run_cli("verify")
                self.assertEqual(completed.returncode, 2)
                self.assertIn(expected_error, completed.stderr)
                self.assertEqual(self.receipt_files(), [])

    def test_rejects_verify_contract_schema_id_and_symlinked_evidence(self) -> None:
        wrong_schema = copy.deepcopy(self.verify_contract)
        wrong_schema["schema_version"] = 2
        self.write_work_json(
            "workspaces/001-example/verify.json", wrong_schema
        )
        completed = self.run_cli("verify")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("schema_version", completed.stderr)

        wrong_id = copy.deepcopy(self.verify_contract)
        wrong_id["workspace_id"] = "002-other"
        self.write_work_json(
            "workspaces/001-example/verify.json", wrong_id
        )
        completed = self.run_cli("verify")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("does not match", completed.stderr)

        outside = (
            self.project_root
            / "context"
            / "project"
            / "outside-evidence.txt"
        )
        outside.write_text("outside\n", encoding="utf-8")
        evidence = self.project_root / "src" / "linked-evidence.txt"
        evidence.symlink_to(outside)
        linked = copy.deepcopy(self.verify_contract)
        linked["verification"]["evidence_paths"] = ["src/linked-evidence.txt"]
        self.write_work_json(
            "workspaces/001-example/verify.json", linked
        )
        completed = self.run_cli("verify")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)
        self.assertEqual(self.receipt_files(), [])

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
            (self.project_root / "src" / "value.txt").read_text(
                encoding="utf-8"
            ),
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
        self.write_work_json(
            "workspaces/001-example/verify.json", contract
        )

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 2)
        self.assertIn(
            "verify receipts directory does not exist", completed.stderr
        )
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
        self.write_work_json(
            "workspaces/001-example/verify.json", contract
        )

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("must not use symlink components", completed.stderr)
        self.assertTrue((self.project_root / "src" / "value.txt").exists())
        self.assertEqual(list(outside.iterdir()), [])

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
            self.work_root
            / "workspaces"
            / "001-example"
            / "records"
            / "old.json"
        )
        original_old_record = old_record.read_bytes()

        failed = self.run_cli("verify")

        self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
        failed_summary = json.loads(failed.stdout)
        self.assertEqual(failed_summary["status"], "verification_failed")
        failed_status = self.read_status()
        self.assertEqual(failed_status["status"], "verification_failed")
        self.assertEqual(failed_status["schema_version"], 2)
        self.assertEqual(failed_status["result"], "fail")
        self.assertEqual(
            failed_status["next_action"],
            self.verify_contract["next_actions"]["fail"],
        )
        self.assertEqual(state_index_path.read_bytes(), original_state_index)

        receipts_after_failure = self.receipt_files()
        self.assertEqual(len(receipts_after_failure), 1)
        failed_receipt_bytes = receipts_after_failure[0].read_bytes()
        failed_receipt = json.loads(failed_receipt_bytes)
        self.assertEqual(failed_receipt["exit_code"], failed.returncode)
        self.assertEqual(failed_receipt["result"], "fail")
        self.assertEqual(failed_receipt["schema_version"], 1)
        self.assertEqual(failed_receipt["workspace_id"], "001-example")
        self.assertIsInstance(failed_receipt["started_at"], str)
        self.assertIsInstance(failed_receipt["finished_at"], str)
        self.assertIsInstance(failed_receipt["stdout"], str)
        self.assertIsInstance(failed_receipt["stderr"], str)
        self.assertEqual(
            failed_receipt["evidence_capture"], "before_verification"
        )
        self.assertEqual(
            failed_status["finished_at"], failed_receipt["finished_at"]
        )
        self.assertEqual(
            failed_receipt["argv"], self.verify_contract["verification"]["argv"]
        )
        self.assertEqual(
            [item["path"] for item in failed_receipt["evidence_files"]],
            self.verify_contract["verification"]["evidence_paths"],
        )

        evidence_path = self.project_root / "src" / "value.txt"
        evidence_path.write_text("expected\n", encoding="utf-8")
        passed = self.run_cli("verify")

        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        passed_summary = json.loads(passed.stdout)
        self.assertEqual(passed_summary["status"], "verified_waiting_acceptance")
        self.assertNotEqual(passed_summary["status"], "completed")
        passed_status = self.read_status()
        self.assertEqual(passed_status["status"], "verified_waiting_acceptance")
        self.assertEqual(passed_status["result"], "pass")
        self.assertNotEqual(passed_status["status"], "completed")
        self.assertEqual(
            passed_status["next_action"],
            self.verify_contract["next_actions"]["pass"],
        )
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

    def test_captures_evidence_before_command_deletes_it(self) -> None:
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"]["argv"] = [
            "python3",
            "-m",
            "unittest",
            "tests.test_delete_evidence",
            "-v",
        ]
        self.write_work_json(
            "workspaces/001-example/verify.json", contract
        )
        expected_bytes = b"wrong\n"

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["status"], "verification_failed")
        self.assertFalse(
            (self.project_root / "src" / "value.txt").exists()
        )
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

    def test_timeout_persists_exit_124_failure_receipt_and_status(self) -> None:
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"].update(
            {
                "argv": [
                    "python3",
                    "-m",
                    "unittest",
                    "tests.test_slow",
                    "-v",
                ],
                "timeout_seconds": 0.1,
                "max_output_chars": 1000,
            }
        )
        self.write_work_json(
            "workspaces/001-example/verify.json", contract
        )

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 124, completed.stdout + completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertTrue(summary["timed_out"])
        self.assertEqual(summary["status"], "verification_failed")
        receipt_files = self.receipt_files()
        self.assertEqual(len(receipt_files), 1)
        receipt = json.loads(receipt_files[0].read_text(encoding="utf-8"))
        self.assertEqual(receipt["exit_code"], 124)
        self.assertEqual(receipt["result"], "fail")
        self.assertTrue(receipt["timeout"]["timed_out"])
        self.assertEqual(receipt["timeout"]["timeout_seconds"], 0.1)
        status = self.read_status()
        self.assertEqual(status["status"], "verification_failed")
        self.assertEqual(status["result"], "fail")
        self.assertEqual(status["receipt"], summary["receipt"])
        self.assertEqual(status["finished_at"], receipt["finished_at"])

    def test_normalizes_root_and_caps_persisted_output(self) -> None:
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"].update(
            {
                "argv": [
                    "python3",
                    "-m",
                    "unittest",
                    "tests.test_noisy",
                    "-v",
                ],
                "timeout_seconds": 2,
                "max_output_chars": 120,
            }
        )
        self.write_work_json(
            "workspaces/001-example/verify.json", contract
        )

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        receipt_path = self.receipt_files()[0]
        receipt_text = receipt_path.read_text(encoding="utf-8")
        receipt = json.loads(receipt_text)
        project_root = str(self.project_root.resolve())
        self.assertNotIn(project_root, receipt_text)
        self.assertIn("<OUTPUT_ROOT>", receipt["stdout"])
        self.assertIn("<OUTPUT_ROOT>", receipt["stderr"])
        self.assertLessEqual(len(receipt["stdout"]), 120)
        self.assertLessEqual(len(receipt["stderr"]), 120)
        capture = receipt["output_capture"]
        self.assertEqual(capture["max_chars_per_stream"], 120)
        self.assertGreater(capture["stdout"]["observed_chars"], 120)
        self.assertGreater(capture["stderr"]["observed_chars"], 120)
        self.assertTrue(capture["stdout"]["truncated"])
        self.assertTrue(capture["stderr"]["truncated"])
        self.assertEqual(
            capture["stdout"]["persisted_chars"], len(receipt["stdout"])
        )
        self.assertEqual(
            capture["stderr"]["persisted_chars"], len(receipt["stderr"])
        )
        normalization = receipt["normalization"]
        self.assertEqual(normalization["output_root_token"], "<OUTPUT_ROOT>")
        self.assertGreaterEqual(normalization["stdout_replacements"], 1)
        self.assertGreaterEqual(normalization["stderr_replacements"], 1)


if __name__ == "__main__":
    import unittest

    unittest.main()
