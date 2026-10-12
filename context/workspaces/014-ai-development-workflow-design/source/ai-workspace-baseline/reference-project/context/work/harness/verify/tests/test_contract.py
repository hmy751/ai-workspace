"""Verify: 전용 설정과 입력 경로 계약을 검증한다."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest

from .support import VerifyFixture


class VerifyContractTests(VerifyFixture):
    def test_runs_when_recover_contract_is_invalid(self) -> None:
        recover_path = self.work_root / "workspaces" / "001-example" / "recover.json"
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

    def test_canonical_basis_is_not_limited_to_recover_project_layers(
        self,
    ) -> None:
        (self.project_root / "PRODUCT.md").write_text(
            "PROJECT_ROOT_NORMATIVE_OWNER\n", encoding="utf-8"
        )
        (self.project_root / "src" / "value.txt").write_text(
            "expected\n", encoding="utf-8"
        )
        contract = copy.deepcopy(self.verify_contract)
        contract["canonical_basis"] = ["PRODUCT.md"]
        self.write_work_json("workspaces/001-example/verify.json", contract)

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        receipt = json.loads(self.receipt_files()[0].read_text(encoding="utf-8"))
        self.assertEqual(receipt["canonical_basis_files"][0]["path"], "PRODUCT.md")

    def test_uses_project_root_for_evidence_and_command_cwd(self) -> None:
        decoy_src = self.work_root / "src"
        decoy_tests = self.work_root / "tests"
        decoy_src.mkdir()
        decoy_tests.mkdir()
        (decoy_src / "value.txt").write_text("expected\n", encoding="utf-8")
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

        blank_claim = copy.deepcopy(self.verify_contract)
        blank_claim["claim"] = "  "
        invalid_contracts.append((blank_claim, "verification claim"))

        no_basis = copy.deepcopy(self.verify_contract)
        no_basis["canonical_basis"] = []
        invalid_contracts.append((no_basis, "canonical_basis"))

        basis_traversal = copy.deepcopy(self.verify_contract)
        basis_traversal["canonical_basis"] = ["../outside"]
        invalid_contracts.append((basis_traversal, "canonical_basis"))

        old_semantic_actions = copy.deepcopy(self.verify_contract)
        old_semantic_actions["next_actions"] = {
            "pass": "accept it",
            "fail": "fix it",
        }
        invalid_contracts.append((old_semantic_actions, "next_actions"))

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
        wrong_schema["schema_version"] = 1
        self.write_work_json("workspaces/001-example/verify.json", wrong_schema)
        completed = self.run_cli("verify")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("schema_version", completed.stderr)

        wrong_id = copy.deepcopy(self.verify_contract)
        wrong_id["workspace_id"] = "002-other"
        self.write_work_json("workspaces/001-example/verify.json", wrong_id)
        completed = self.run_cli("verify")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("does not match", completed.stderr)

        outside = self.project_root / "context" / "project" / "outside-evidence.txt"
        outside.write_text("outside\n", encoding="utf-8")
        evidence = self.project_root / "src" / "linked-evidence.txt"
        evidence.symlink_to(outside)
        linked = copy.deepcopy(self.verify_contract)
        linked["verification"]["evidence_paths"] = ["src/linked-evidence.txt"]
        self.write_work_json("workspaces/001-example/verify.json", linked)
        completed = self.run_cli("verify")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)
        self.assertEqual(self.receipt_files(), [])

        basis = self.project_root / "context" / "project" / "linked-basis.md"
        basis.symlink_to(outside)
        linked_basis = copy.deepcopy(self.verify_contract)
        linked_basis["canonical_basis"] = ["context/project/linked-basis.md"]
        self.write_work_json("workspaces/001-example/verify.json", linked_basis)
        completed = self.run_cli("verify")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)
        self.assertEqual(self.receipt_files(), [])
