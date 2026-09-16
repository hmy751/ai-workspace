"""Verify: root 정규화와 출력 보존 한도를 검증한다."""

from __future__ import annotations

import copy
import json
import unittest

from .support import VerifyFixture


class VerifyOutputTests(VerifyFixture):
    verification_scenarios = ("noisy",)

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
        self.write_work_json("workspaces/001-example/verify.json", contract)

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
        self.assertEqual(capture["stdout"]["persisted_chars"], len(receipt["stdout"]))
        self.assertEqual(capture["stderr"]["persisted_chars"], len(receipt["stderr"]))
        normalization = receipt["normalization"]
        self.assertEqual(normalization["output_root_token"], "<OUTPUT_ROOT>")
        self.assertGreaterEqual(normalization["stdout_replacements"], 1)
        self.assertGreaterEqual(normalization["stderr_replacements"], 1)
