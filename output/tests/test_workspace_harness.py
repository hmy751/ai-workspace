from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HARNESS_SOURCE = Path(__file__).resolve().parents[1] / "harness" / "workspace.py"
STATE_BEGIN = "<!-- workspace-state:begin -->"
STATE_END = "<!-- workspace-state:end -->"


class WorkspaceHarnessTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        for directory in (
            "harness",
            "docs",
            "src",
            "tests",
            "workspaces/001-example/current",
            "workspaces/001-example/records",
        ):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        shutil.copy2(HARNESS_SOURCE, self.root / "harness" / "workspace.py")

        (self.root / "docs" / "selected.md").write_text(
            "SELECTED_PROJECT_CONTEXT\n", encoding="utf-8"
        )
        (self.root / "docs" / "not-selected.md").write_text(
            "UNSELECTED_PROJECT_SECRET\n", encoding="utf-8"
        )
        (self.root / "src" / "value.txt").write_text(
            "wrong\n", encoding="utf-8"
        )
        (self.root / "tests" / "__init__.py").write_text("", encoding="utf-8")
        (self.root / "tests" / "test_behavior.py").write_text(
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
        (self.root / "tests" / "test_delete_evidence.py").write_text(
            "from pathlib import Path\n"
            "import unittest\n\n"
            "class DeleteEvidenceTests(unittest.TestCase):\n"
            "    def test_delete_then_fail(self):\n"
            "        Path('src/value.txt').unlink()\n"
            "        self.fail('intentional failure after evidence deletion')\n",
            encoding="utf-8",
        )
        (self.root / "tests" / "test_slow.py").write_text(
            "import time\n"
            "import unittest\n\n"
            "class SlowTests(unittest.TestCase):\n"
            "    def test_slow(self):\n"
            "        time.sleep(2)\n",
            encoding="utf-8",
        )
        (self.root / "tests" / "test_noisy.py").write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "import unittest\n\n"
            "class NoisyTests(unittest.TestCase):\n"
            "    def test_noisy(self):\n"
            "        roots = str(Path.cwd()) * 50\n"
            "        print(roots + 'X' * 2000)\n"
            "        print(roots + 'Y' * 2000, file=sys.stderr)\n",
            encoding="utf-8",
        )
        (self.root / "workspaces" / "001-example" / "records" / "old.json").write_text(
            '{"secret": "UNLOADED_RECORD_SECRET"}\n', encoding="utf-8"
        )

        self.index = {
            "schema_version": 1,
            "active_workspace_id": "001-example",
        }
        self.manifest = {
            "schema_version": 1,
            "workspace_id": "001-example",
            "project_context": [
                {
                    "path": "docs/selected.md",
                    "reason": "fixture에서 필요한 유일한 Project 기준",
                }
            ],
            "verification": {
                "argv": [
                    "python3",
                    "-m",
                    "unittest",
                    "tests.test_behavior",
                    "-v",
                ],
                "evidence_paths": ["src/value.txt", "tests/test_behavior.py"],
            },
            "next_actions": {
                "pass": "사람의 수락 여부를 결정한다.",
                "fail": "첫 실패를 수정하고 다시 검증한다.",
            },
        }
        self._write_json("workspaces/index.json", self.index)
        self._write_json("workspaces/001-example/workspace.json", self.manifest)
        (self.root / "workspaces" / "001-example" / "current" / "memory.md").write_text(
            "WORKSPACE_MEMORY\n", encoding="utf-8"
        )
        self._write_state()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _write_json(self, relative_path: str, value: object) -> None:
        (self.root / relative_path).write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _initial_marker(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "workspace_id": "001-example",
            "status": "ready_for_verification",
            "result": None,
            "receipt": None,
            "finished_at": None,
            "next_action": "고정 검증을 실행한다.",
        }

    def _write_state(self, marker: dict[str, object] | None = None) -> None:
        marker = marker or self._initial_marker()
        content = (
            "# state\n\n"
            "human-owned current description\n\n"
            f"{STATE_BEGIN}\n"
            f"{json.dumps(marker, ensure_ascii=False, indent=2)}\n"
            f"{STATE_END}\n"
        )
        (self.root / "workspaces" / "001-example" / "current" / "state.md").write_text(
            content, encoding="utf-8"
        )

    def _run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "harness/workspace.py", *arguments],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def _read_marker(self) -> dict[str, object]:
        state = (
            self.root / "workspaces" / "001-example" / "current" / "state.md"
        ).read_text(encoding="utf-8")
        marker_text = state.split(STATE_BEGIN, 1)[1].split(STATE_END, 1)[0]
        return json.loads(marker_text)

    def _receipt_files(self) -> list[Path]:
        return sorted(
            (self.root / "workspaces" / "001-example" / "records").glob(
                "verify-*.json"
            )
        )

    def _verified_marker(
        self,
        receipt: str,
        *,
        result: str = "pass",
        finished_at: str = "2026-08-13T00:00:00.000Z",
    ) -> dict[str, object]:
        return {
            "schema_version": 1,
            "workspace_id": "001-example",
            "status": (
                "verified_waiting_acceptance"
                if result == "pass"
                else "verification_failed"
            ),
            "result": result,
            "receipt": receipt,
            "finished_at": finished_at,
            "next_action": "receipt를 검토한다.",
        }

    def test_recover_loads_only_current_and_selected_project_context(self) -> None:
        completed = self._run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        packet = json.loads(completed.stdout)
        self.assertEqual(packet["workspace_id"], "001-example")
        self.assertEqual(
            packet["control_paths"],
            [
                "workspaces/index.json",
                "workspaces/001-example/workspace.json",
            ],
        )
        self.assertEqual(
            packet["loaded_context_paths"],
            [
                "workspaces/001-example/current/memory.md",
                "workspaces/001-example/current/state.md",
                "docs/selected.md",
            ],
        )
        self.assertEqual(packet["memory"], "WORKSPACE_MEMORY\n")
        self.assertEqual(
            [entry["path"] for entry in packet["project_context"]],
            ["docs/selected.md"],
        )
        self.assertIn("SELECTED_PROJECT_CONTEXT", completed.stdout)
        self.assertNotIn("UNSELECTED_PROJECT_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_RECORD_SECRET", completed.stdout)

    def test_recover_rejects_traversal_absolute_schema_and_shell_string(self) -> None:
        invalid_manifests = []

        traversal = copy.deepcopy(self.manifest)
        traversal["project_context"][0]["path"] = "../outside.md"
        invalid_manifests.append((traversal, "traverse"))

        absolute = copy.deepcopy(self.manifest)
        absolute["project_context"][0]["path"] = "/tmp/outside.md"
        invalid_manifests.append((absolute, "relative"))

        wrong_schema = copy.deepcopy(self.manifest)
        wrong_schema["schema_version"] = 2
        invalid_manifests.append((wrong_schema, "schema_version"))

        shell_string = copy.deepcopy(self.manifest)
        shell_string["verification"]["argv"] = "python3 -m unittest"
        invalid_manifests.append((shell_string, "shell string"))

        shell_argv = copy.deepcopy(self.manifest)
        shell_argv["verification"]["argv"] = ["sh", "-c", "exit 0"]
        invalid_manifests.append((shell_argv, "shell"))

        embedded_absolute = copy.deepcopy(self.manifest)
        embedded_absolute["verification"]["argv"] = [
            "python3",
            "--config=/tmp/outside.json",
        ]
        invalid_manifests.append((embedded_absolute, "absolute"))

        invalid_timeout = copy.deepcopy(self.manifest)
        invalid_timeout["verification"]["timeout_seconds"] = 0
        invalid_manifests.append((invalid_timeout, "timeout_seconds"))

        invalid_output_cap = copy.deepcopy(self.manifest)
        invalid_output_cap["verification"]["max_output_chars"] = 1_000_001
        invalid_manifests.append((invalid_output_cap, "max_output_chars"))

        for invalid_manifest, expected_error in invalid_manifests:
            with self.subTest(expected_error=expected_error):
                self._write_json(
                    "workspaces/001-example/workspace.json", invalid_manifest
                )
                completed = self._run_cli("recover")
                self.assertEqual(completed.returncode, 2)
                self.assertIn(expected_error, completed.stderr)

    def test_recover_rejects_project_context_outside_resolved_docs(self) -> None:
        outside_docs = copy.deepcopy(self.manifest)
        outside_docs["project_context"][0]["path"] = "src/value.txt"
        self._write_json("workspaces/001-example/workspace.json", outside_docs)

        lexical_outside = self._run_cli("recover")
        self.assertEqual(lexical_outside.returncode, 2)
        self.assertIn("selected from docs", lexical_outside.stderr)

        record_path = (
            self.root / "workspaces" / "001-example" / "records" / "old.json"
        )
        link_path = self.root / "docs" / "record-link.md"
        link_path.symlink_to(record_path)
        linked_record = copy.deepcopy(self.manifest)
        linked_record["project_context"][0]["path"] = "docs/record-link.md"
        self._write_json("workspaces/001-example/workspace.json", linked_record)

        resolved_outside = self._run_cli("recover")
        self.assertEqual(resolved_outside.returncode, 2)
        self.assertIn("resolve inside docs", resolved_outside.stderr)
        self.assertNotIn("UNLOADED_RECORD_SECRET", resolved_outside.stdout)

    def test_recover_rejects_invalid_or_duplicate_state_marker(self) -> None:
        marker = self._initial_marker()
        marker["schema_version"] = 9
        self._write_state(marker)

        wrong_schema = self._run_cli("recover")
        self.assertEqual(wrong_schema.returncode, 2)
        self.assertIn("schema_version", wrong_schema.stderr)

        inconsistent_marker = self._initial_marker()
        inconsistent_marker["status"] = "verified_waiting_acceptance"
        self._write_state(inconsistent_marker)

        inconsistent = self._run_cli("recover")
        self.assertEqual(inconsistent.returncode, 2)
        self.assertIn("inconsistent", inconsistent.stderr)

        wrong_type_marker = self._initial_marker()
        wrong_type_marker["status"] = ["ready_for_verification"]
        self._write_state(wrong_type_marker)

        wrong_type = self._run_cli("recover")
        self.assertEqual(wrong_type.returncode, 2)
        self.assertIn("invalid state marker status", wrong_type.stderr)

        state_path = self.root / "workspaces" / "001-example" / "current" / "state.md"
        valid_state = (
            f"{STATE_BEGIN}\n"
            f"{json.dumps(self._initial_marker())}\n"
            f"{STATE_END}\n"
        )
        state_path.write_text(valid_state + valid_state, encoding="utf-8")

        duplicate = self._run_cli("recover")
        self.assertEqual(duplicate.returncode, 2)
        self.assertIn("exactly one", duplicate.stderr)

    def test_recover_validates_receipt_without_loading_its_body(self) -> None:
        receipt_relative = (
            "workspaces/001-example/records/verify-existing.json"
        )
        marker = self._verified_marker(receipt_relative)
        self._write_state(marker)

        missing = self._run_cli("recover", "--json")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("does not exist", missing.stderr)

        receipt = {
            "schema_version": 1,
            "workspace_id": "001-example",
            "result": "fail",
            "finished_at": marker["finished_at"],
            "body_secret": "RECEIPT_BODY_MUST_NOT_ENTER_CONTEXT",
        }
        self._write_json(receipt_relative, receipt)
        mismatched = self._run_cli("recover", "--json")
        self.assertEqual(mismatched.returncode, 2)
        self.assertIn("result do not match", mismatched.stderr)

        receipt["result"] = "pass"
        receipt["finished_at"] = "2026-08-13T00:00:01.000Z"
        self._write_json(receipt_relative, receipt)
        wrong_time = self._run_cli("recover", "--json")
        self.assertEqual(wrong_time.returncode, 2)
        self.assertIn("finished_at do not match", wrong_time.stderr)

        receipt["finished_at"] = marker["finished_at"]
        self._write_json(receipt_relative, receipt)
        recovered = self._run_cli("recover", "--json")
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        packet = json.loads(recovered.stdout)
        self.assertIn(receipt_relative, packet["control_paths"])
        self.assertNotIn(receipt_relative, packet["loaded_context_paths"])
        self.assertNotIn("RECEIPT_BODY_MUST_NOT_ENTER_CONTEXT", recovered.stdout)

    def test_recover_rejects_receipt_symlink(self) -> None:
        outside_receipt = self.root / "docs" / "receipt.json"
        outside_receipt.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_id": "001-example",
                    "result": "pass",
                    "finished_at": "2026-08-13T00:00:00.000Z",
                }
            ),
            encoding="utf-8",
        )
        receipt_relative = "workspaces/001-example/records/linked.json"
        (self.root / receipt_relative).symlink_to(outside_receipt)
        self._write_state(self._verified_marker(receipt_relative))

        completed = self._run_cli("recover")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)

    def test_verify_persists_failure_then_pass_without_completing(self) -> None:
        failed = self._run_cli("verify")

        self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
        failed_summary = json.loads(failed.stdout)
        self.assertEqual(failed_summary["status"], "verification_failed")
        failed_marker = self._read_marker()
        self.assertEqual(failed_marker["status"], "verification_failed")
        self.assertEqual(failed_marker["result"], "fail")
        self.assertEqual(
            failed_marker["next_action"], self.manifest["next_actions"]["fail"]
        )

        receipts_after_failure = self._receipt_files()
        self.assertEqual(len(receipts_after_failure), 1)
        failed_receipt = json.loads(
            receipts_after_failure[0].read_text(encoding="utf-8")
        )
        self.assertEqual(failed_receipt["exit_code"], failed.returncode)
        self.assertEqual(failed_receipt["result"], "fail")
        self.assertEqual(failed_receipt["schema_version"], 1)
        self.assertEqual(failed_receipt["workspace_id"], "001-example")
        self.assertIsInstance(failed_receipt["started_at"], str)
        self.assertIsInstance(failed_receipt["finished_at"], str)
        self.assertIsInstance(failed_receipt["stdout"], str)
        self.assertIsInstance(failed_receipt["stderr"], str)
        self.assertEqual(failed_receipt["evidence_capture"], "before_verification")
        self.assertEqual(
            failed_marker["finished_at"], failed_receipt["finished_at"]
        )
        self.assertEqual(
            failed_receipt["argv"], self.manifest["verification"]["argv"]
        )
        self.assertEqual(
            [item["path"] for item in failed_receipt["evidence_files"]],
            self.manifest["verification"]["evidence_paths"],
        )

        evidence_path = self.root / "src" / "value.txt"
        evidence_path.write_text("expected\n", encoding="utf-8")
        passed = self._run_cli("verify")

        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        passed_summary = json.loads(passed.stdout)
        self.assertEqual(
            passed_summary["status"], "verified_waiting_acceptance"
        )
        self.assertNotEqual(passed_summary["status"], "completed")
        passed_marker = self._read_marker()
        self.assertEqual(
            passed_marker["status"], "verified_waiting_acceptance"
        )
        self.assertEqual(passed_marker["result"], "pass")
        self.assertNotEqual(passed_marker["status"], "completed")
        self.assertEqual(
            passed_marker["next_action"], self.manifest["next_actions"]["pass"]
        )

        receipts_after_pass = self._receipt_files()
        self.assertEqual(len(receipts_after_pass), 2)
        self.assertNotEqual(receipts_after_pass[0].name, receipts_after_pass[1].name)
        receipt_by_result = {
            receipt["result"]: receipt
            for receipt in (
                json.loads(path.read_text(encoding="utf-8"))
                for path in receipts_after_pass
            )
        }
        passed_receipt = receipt_by_result["pass"]
        self.assertEqual(passed_receipt["exit_code"], passed.returncode)
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
        self.assertEqual(passed_marker["receipt"], passed_summary["receipt"])

    def test_verify_keeps_result_when_command_deletes_evidence(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["verification"]["argv"] = [
            "python3",
            "-m",
            "unittest",
            "tests.test_delete_evidence",
            "-v",
        ]
        self._write_json("workspaces/001-example/workspace.json", manifest)
        expected_bytes = b"wrong\n"

        completed = self._run_cli("verify")

        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["status"], "verification_failed")
        self.assertFalse((self.root / "src" / "value.txt").exists())
        receipt_files = self._receipt_files()
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
        marker = self._read_marker()
        self.assertEqual(marker["receipt"], summary["receipt"])
        self.assertEqual(marker["finished_at"], receipt["finished_at"])

    def test_verify_timeout_persists_failure_receipt_and_state(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["verification"].update(
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
        self._write_json("workspaces/001-example/workspace.json", manifest)

        completed = self._run_cli("verify")

        self.assertEqual(completed.returncode, 124, completed.stdout + completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertTrue(summary["timed_out"])
        self.assertEqual(summary["status"], "verification_failed")
        receipt_files = self._receipt_files()
        self.assertEqual(len(receipt_files), 1)
        receipt = json.loads(receipt_files[0].read_text(encoding="utf-8"))
        self.assertEqual(receipt["exit_code"], 124)
        self.assertEqual(receipt["result"], "fail")
        self.assertTrue(receipt["timeout"]["timed_out"])
        self.assertEqual(receipt["timeout"]["timeout_seconds"], 0.1)
        marker = self._read_marker()
        self.assertEqual(marker["status"], "verification_failed")
        self.assertEqual(marker["result"], "fail")
        self.assertEqual(marker["receipt"], summary["receipt"])
        self.assertEqual(marker["finished_at"], receipt["finished_at"])

    def test_verify_normalizes_root_and_caps_persisted_output(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["verification"].update(
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
        self._write_json("workspaces/001-example/workspace.json", manifest)

        completed = self._run_cli("verify")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        receipt_path = self._receipt_files()[0]
        receipt_text = receipt_path.read_text(encoding="utf-8")
        receipt = json.loads(receipt_text)
        output_root = str(self.root.resolve())
        self.assertNotIn(output_root, receipt_text)
        self.assertNotIn(output_root, receipt["stdout"])
        self.assertNotIn(output_root, receipt["stderr"])
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
        self.assertGreaterEqual(
            normalization["stdout_replacements"], 1
        )
        self.assertGreaterEqual(
            normalization["stderr_replacements"], 1
        )


if __name__ == "__main__":
    unittest.main()
