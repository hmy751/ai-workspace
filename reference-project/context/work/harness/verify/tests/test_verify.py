from __future__ import annotations

import copy
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
from unittest import mock

from context.work.harness.testing import WorkspaceFixture
from context.work.harness.verify import record_evidence
from context.work.harness.workspace_contract import HarnessError


RECEIPT_KEYS = {
    "schema_version",
    "receipt_type",
    "workspace_id",
    "recorded_at",
    "observed_at",
    "producer",
    "subject",
    "method",
    "outcome",
    "result_summary",
    "source_refs",
    "unverified_scope",
}


class VerifyEvidenceTests(WorkspaceFixture):
    def evidence_payload(self, outcome: str = "pass") -> dict[str, object]:
        return {
            "schema_version": 1,
            "observed_at": "2026-08-17T20:30:45.123+09:00",
            "producer": "Main task",
            "subject": "selected unit tests",
            "method": "python3 -m unittest tests.test_behavior -v",
            "outcome": outcome,
            "result_summary": "1 test completed with its reported outcome",
            "source_refs": [
                {
                    "kind": "local-command",
                    "locator": "task transcript: verification command 1",
                }
            ],
            "unverified_scope": ["browser behavior was not checked"],
        }

    def evidence_receipts(self, workspace_id: str = "001-example") -> list[Path]:
        return sorted(
            (
                self.work_root
                / "workspaces"
                / workspace_id
                / "records"
                / "receipts"
                / "verify"
            ).glob("evidence-*.json")
        )

    def run_verify_stdin(
        self, payload: object, workspace_id: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, "-m", "context.work.harness", "verify"]
        if workspace_id is not None:
            command.append(workspace_id)
        command.extend(["--input-json", "-"])
        return subprocess.run(
            command,
            cwd=self.project_root,
            input=json.dumps(payload, ensure_ascii=False),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_records_exact_receipt_and_non_judgmental_summary(self) -> None:
        payload = self.evidence_payload("partial")

        summary = record_evidence(self.work_root, payload)

        self.assertEqual(
            set(summary),
            {"workspace_id", "receipt", "recorded", "evidence_outcome"},
        )
        self.assertEqual(summary["workspace_id"], "001-example")
        self.assertIs(summary["recorded"], True)
        self.assertEqual(summary["evidence_outcome"], "partial")
        self.assertNotIn("verified", summary)
        self.assertNotIn("status", summary)
        self.assertNotIn("result", summary)

        receipts = self.evidence_receipts()
        self.assertEqual(len(receipts), 1)
        self.assertEqual(
            summary["receipt"],
            receipts[0].relative_to(self.work_root).as_posix(),
        )
        receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
        self.assertEqual(set(receipt), RECEIPT_KEYS)
        self.assertEqual(receipt["schema_version"], 1)
        self.assertEqual(
            receipt["receipt_type"], "recorded_verification_evidence"
        )
        self.assertEqual(receipt["workspace_id"], "001-example")
        for key, value in payload.items():
            self.assertEqual(receipt[key], value)
        recorded_at = receipt["recorded_at"]
        self.assertTrue(recorded_at.endswith("Z"))
        self.assertIsNotNone(
            datetime.fromisoformat(recorded_at[:-1] + "+00:00").utcoffset()
        )

    def test_cli_records_pass_fail_and_partial_with_exit_zero(self) -> None:
        for index, outcome in enumerate(("pass", "fail", "partial"), start=1):
            with self.subTest(outcome=outcome):
                completed = self.run_verify_stdin(self.evidence_payload(outcome))

                self.assertEqual(
                    completed.returncode,
                    0,
                    completed.stdout + completed.stderr,
                )
                summary = json.loads(completed.stdout)
                self.assertIs(summary["recorded"], True)
                self.assertEqual(summary["evidence_outcome"], outcome)
                self.assertEqual(len(self.evidence_receipts()), index)

    def test_does_not_run_product_command_or_change_legacy_files_or_status(
        self,
    ) -> None:
        marker = self.project_root / "product-command-ran.txt"
        command = self.project_root / "would_run.py"
        command.write_text(
            "from pathlib import Path\n"
            "Path('product-command-ran.txt').write_text('ran', encoding='utf-8')\n",
            encoding="utf-8",
        )
        legacy_contract = copy.deepcopy(self.verify_contract)
        legacy_contract["verification"]["argv"] = ["python3", "would_run.py"]
        self.write_work_json(
            "workspaces/001-example/verify.json", legacy_contract
        )
        verify_path = self.work_root / "workspaces/001-example/verify.json"
        status_path = (
            self.work_root
            / "workspaces/001-example/current/state/status.json"
        )
        product_path = self.project_root / "src/value.txt"
        original_verify = verify_path.read_bytes()
        original_status = status_path.read_bytes()
        original_product = product_path.read_bytes()
        input_path = self.project_root / "evidence.json"
        input_path.write_text(
            json.dumps(self.evidence_payload(), ensure_ascii=False),
            encoding="utf-8",
        )

        completed = self.run_cli(
            "verify", "--input-json", "evidence.json"
        )

        self.assertEqual(
            completed.returncode, 0, completed.stdout + completed.stderr
        )
        self.assertFalse(marker.exists())
        self.assertEqual(verify_path.read_bytes(), original_verify)
        self.assertEqual(status_path.read_bytes(), original_status)
        self.assertEqual(product_path.read_bytes(), original_product)

    def test_malformed_legacy_artifacts_are_not_read_or_reinterpreted(self) -> None:
        verify_path = self.work_root / "workspaces/001-example/verify.json"
        status_path = (
            self.work_root
            / "workspaces/001-example/current/state/status.json"
        )
        old_receipt = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify/verify-old.json"
        )
        verify_path.write_text('{"legacy": INVALID\n', encoding="utf-8")
        status_path.write_text('{"legacy": INVALID\n', encoding="utf-8")
        old_receipt.write_text('{"legacy": INVALID\n', encoding="utf-8")
        original_verify = verify_path.read_bytes()
        original_status = status_path.read_bytes()
        original_receipt = old_receipt.read_bytes()

        completed = self.run_verify_stdin(self.evidence_payload())

        self.assertEqual(
            completed.returncode, 0, completed.stdout + completed.stderr
        )
        self.assertEqual(verify_path.read_bytes(), original_verify)
        self.assertEqual(status_path.read_bytes(), original_status)
        self.assertEqual(old_receipt.read_bytes(), original_receipt)
        self.assertEqual(len(self.evidence_receipts()), 1)

    def test_rejects_wrong_shape_schema_time_enum_empty_nul_and_extra(
        self,
    ) -> None:
        base = self.evidence_payload()
        invalid: list[tuple[object, str]] = []

        invalid.append(([base], "JSON object"))

        wrong_schema = copy.deepcopy(base)
        wrong_schema["schema_version"] = 2
        invalid.append((wrong_schema, "schema_version"))

        missing = copy.deepcopy(base)
        del missing["method"]
        invalid.append((missing, "missing"))

        extra = copy.deepcopy(base)
        extra["claim"] = "legacy semantic claim"
        invalid.append((extra, "extra"))

        no_timezone = copy.deepcopy(base)
        no_timezone["observed_at"] = "2026-08-17T20:30:45"
        invalid.append((no_timezone, "timezone"))

        bad_date = copy.deepcopy(base)
        bad_date["observed_at"] = "2026-13-17T20:30:45Z"
        invalid.append((bad_date, "valid RFC3339"))

        bad_outcome = copy.deepcopy(base)
        bad_outcome["outcome"] = "success"
        invalid.append((bad_outcome, "pass"))

        blank_producer = copy.deepcopy(base)
        blank_producer["producer"] = "  "
        invalid.append((blank_producer, "producer"))

        nul_subject = copy.deepcopy(base)
        nul_subject["subject"] = "subject\x00hidden"
        invalid.append((nul_subject, "NUL"))

        refs_not_array = copy.deepcopy(base)
        refs_not_array["source_refs"] = {}
        invalid.append((refs_not_array, "JSON array"))

        ref_not_object = copy.deepcopy(base)
        ref_not_object["source_refs"] = ["transcript"]
        invalid.append((ref_not_object, "JSON object"))

        ref_missing = copy.deepcopy(base)
        ref_missing["source_refs"] = [{"kind": "ci"}]
        invalid.append((ref_missing, "missing"))

        ref_extra = copy.deepcopy(base)
        ref_extra["source_refs"] = [
            {"kind": "ci", "locator": "run/1", "hash": "abc"}
        ]
        invalid.append((ref_extra, "extra"))

        ref_nul = copy.deepcopy(base)
        ref_nul["source_refs"] = [
            {"kind": "ci", "locator": "run/1\x00secret"}
        ]
        invalid.append((ref_nul, "NUL"))

        no_unverified_scope = copy.deepcopy(base)
        no_unverified_scope["unverified_scope"] = []
        invalid.append((no_unverified_scope, "non-empty JSON array"))

        blank_unverified_scope = copy.deepcopy(base)
        blank_unverified_scope["unverified_scope"] = [" "]
        invalid.append((blank_unverified_scope, "non-empty string"))

        for payload, expected_error in invalid:
            with self.subTest(expected_error=expected_error):
                with self.assertRaisesRegex(HarnessError, expected_error):
                    record_evidence(self.work_root, payload)  # type: ignore[arg-type]

        self.assertEqual(self.evidence_receipts(), [])

    def test_empty_or_unresolvable_source_references_are_recorded_as_given(
        self,
    ) -> None:
        without_refs = self.evidence_payload()
        without_refs["source_refs"] = []
        inaccessible_ref = self.evidence_payload("partial")
        inaccessible_ref["source_refs"] = [
            {
                "kind": "artifact",
                "locator": "/not/opened/and/does-not-exist/../result.json",
            }
        ]

        record_evidence(self.work_root, without_refs)
        record_evidence(self.work_root, inaccessible_ref)

        receipts = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in self.evidence_receipts()
        ]
        self.assertEqual(len(receipts), 2)
        self.assertIn([], [receipt["source_refs"] for receipt in receipts])
        self.assertIn(
            inaccessible_ref["source_refs"],
            [receipt["source_refs"] for receipt in receipts],
        )

    def test_collision_never_overwrites_an_existing_receipt(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        existing = receipts_directory / "evidence-fixed.json"
        existing.write_bytes(b"ORIGINAL_RECEIPT\n")

        with mock.patch(
            "context.work.harness.verify.operation._receipt_filename",
            return_value=existing.name,
        ):
            with self.assertRaisesRegex(HarnessError, "append-only"):
                record_evidence(self.work_root, self.evidence_payload())

        self.assertEqual(existing.read_bytes(), b"ORIGINAL_RECEIPT\n")
        self.assertEqual(
            list(receipts_directory.glob(".evidence-receipt-*.tmp")), []
        )

    def test_fsyncs_receipts_directory_after_publishing_receipt(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_parent = receipts_directory.parent
        observed: list[tuple[Path, int]] = []

        def capture_fsync(directory: Path) -> None:
            observed.append((directory, len(self.evidence_receipts())))

        with mock.patch(
            "context.work.harness.verify.operation._fsync_directory",
            side_effect=capture_fsync,
        ):
            summary = record_evidence(self.work_root, self.evidence_payload())

        self.assertEqual(
            observed,
            [
                (receipts_parent.resolve(), 0),
                (receipts_directory.resolve(), 1),
            ],
        )
        self.assertIs(summary["recorded"], True)

    def test_does_not_report_recorded_when_directory_fsync_fails(self) -> None:
        with mock.patch(
            "context.work.harness.verify.operation._fsync_directory",
            side_effect=[None, HarnessError("directory fsync failed")],
        ):
            with self.assertRaisesRegex(HarnessError, "directory fsync failed"):
                record_evidence(self.work_root, self.evidence_payload())

        self.assertEqual(len(self.evidence_receipts()), 1)

    def test_creates_missing_verify_leaf_and_fsyncs_parent(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_parent = receipts_directory.parent
        receipts_directory.rmdir()

        with mock.patch(
            "context.work.harness.verify.operation._fsync_directory"
        ) as fsync_directory:
            summary = record_evidence(self.work_root, self.evidence_payload())

        self.assertTrue(receipts_directory.is_dir())
        self.assertIs(summary["recorded"], True)
        self.assertEqual(
            fsync_directory.call_args_list,
            [
                mock.call(receipts_parent.resolve()),
                mock.call(receipts_directory.resolve()),
            ],
        )

    def test_retry_resyncs_parent_after_leaf_creation_fsync_failure(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_parent = receipts_directory.parent
        receipts_directory.rmdir()

        with mock.patch(
            "context.work.harness.verify.operation._fsync_directory",
            side_effect=HarnessError("parent fsync failed"),
        ):
            with self.assertRaisesRegex(HarnessError, "parent fsync failed"):
                record_evidence(self.work_root, self.evidence_payload())

        self.assertTrue(receipts_directory.is_dir())
        with mock.patch(
            "context.work.harness.verify.operation._fsync_directory"
        ) as fsync_directory:
            summary = record_evidence(self.work_root, self.evidence_payload())

        self.assertEqual(
            fsync_directory.call_args_list,
            [
                mock.call(receipts_parent.resolve()),
                mock.call(receipts_directory.resolve()),
            ],
        )
        self.assertIs(summary["recorded"], True)

    def test_requires_existing_non_symlink_receipts_parent(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_directory.rmdir()
        receipts_directory.parent.rmdir()

        with self.assertRaisesRegex(HarnessError, "does not exist"):
            record_evidence(self.work_root, self.evidence_payload())

    def test_rejects_receipts_parent_symlink(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_parent = receipts_directory.parent
        receipts_directory.rmdir()
        receipts_parent.rmdir()

        outside = self.project_root / "outside-receipts-parent"
        outside.mkdir()
        receipts_parent.symlink_to(outside, target_is_directory=True)

        with self.assertRaisesRegex(HarnessError, "symlink"):
            record_evidence(self.work_root, self.evidence_payload())
        self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_verify_leaf_symlink(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_directory.rmdir()

        outside = self.project_root / "outside-receipts"
        outside.mkdir()
        receipts_directory.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(HarnessError, "symlink"):
            record_evidence(self.work_root, self.evidence_payload())
        self.assertEqual(list(outside.iterdir()), [])

    def test_fails_closed_if_verify_leaf_appears_during_creation(self) -> None:
        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_directory.rmdir()

        with mock.patch(
            "context.work.harness.verify.operation.os.mkdir",
            side_effect=FileExistsError("racing entry"),
        ):
            with self.assertRaisesRegex(HarnessError, "changed while"):
                record_evidence(self.work_root, self.evidence_payload())

        self.assertFalse(receipts_directory.exists())

    def test_selects_active_or_explicit_workspace_safely(self) -> None:
        second_root = self.work_root / "workspaces/002-second"
        (second_root / "records/receipts/verify").mkdir(parents=True)
        self.write_work_json(
            "workspaces/002-second/workspace.json",
            {"schema_version": 1, "workspace_id": "002-second"},
        )

        active = record_evidence(self.work_root, self.evidence_payload())
        explicit = record_evidence(
            self.work_root, self.evidence_payload("fail"), "002-second"
        )

        self.assertEqual(active["workspace_id"], "001-example")
        self.assertEqual(explicit["workspace_id"], "002-second")
        self.assertEqual(len(self.evidence_receipts("001-example")), 1)
        self.assertEqual(len(self.evidence_receipts("002-second")), 1)

    def test_cli_reads_stdin_and_safe_file_but_rejects_unsafe_paths(self) -> None:
        stdin_result = self.run_verify_stdin(self.evidence_payload())
        self.assertEqual(
            stdin_result.returncode,
            0,
            stdin_result.stdout + stdin_result.stderr,
        )

        input_path = self.project_root / "evidence-input.json"
        input_path.write_text(
            json.dumps(self.evidence_payload("fail"), ensure_ascii=False),
            encoding="utf-8",
        )
        file_result = self.run_cli(
            "verify", "001-example", "--input-json", "evidence-input.json"
        )
        self.assertEqual(
            file_result.returncode,
            0,
            file_result.stdout + file_result.stderr,
        )
        self.assertEqual(
            json.loads(file_result.stdout)["evidence_outcome"], "fail"
        )
        receipt_count = len(self.evidence_receipts())

        linked_input = self.project_root / "linked-input.json"
        linked_input.symlink_to(input_path)
        unsafe_inputs = (
            "../evidence-input.json",
            str(input_path),
            "linked-input.json",
        )
        for unsafe_input in unsafe_inputs:
            with self.subTest(unsafe_input=unsafe_input):
                completed = self.run_cli(
                    "verify", "--input-json", unsafe_input
                )
                self.assertEqual(completed.returncode, 2)
        self.assertEqual(len(self.evidence_receipts()), receipt_count)

    def test_cli_returns_two_for_input_or_storage_errors(self) -> None:
        malformed = self.project_root / "malformed.json"
        malformed.write_text('{"schema_version": 1\n', encoding="utf-8")
        input_error = self.run_cli(
            "verify", "--input-json", "malformed.json"
        )

        self.assertEqual(input_error.returncode, 2)
        self.assertIn("not valid JSON", input_error.stderr)

        receipts_directory = (
            self.work_root
            / "workspaces/001-example/records/receipts/verify"
        )
        receipts_directory.rmdir()
        receipts_directory.parent.rmdir()
        storage_error = self.run_verify_stdin(self.evidence_payload())

        self.assertEqual(storage_error.returncode, 2)
        self.assertIn("does not exist", storage_error.stderr)


if __name__ == "__main__":
    import unittest

    unittest.main()
