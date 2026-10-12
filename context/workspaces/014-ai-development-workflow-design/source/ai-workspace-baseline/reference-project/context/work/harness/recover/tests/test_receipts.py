"""Recover: receipt의 형식·인계·불변성을 검증한다."""

from __future__ import annotations

import json

from .support import ReceiptFixture


class RecoverReceiptsTests(ReceiptFixture):
    def test_validates_linked_receipt_header_without_exposing_body(self) -> None:
        receipt_relative = "workspaces/001-example/records/verify-existing.json"
        status = self.verified_status(receipt_relative)
        self.write_status(status)

        missing = self.run_cli("recover", "--json")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("does not exist", missing.stderr)

        receipt = {
            "schema_version": 1,
            "workspace_id": "001-example",
            "result": "fail",
            "finished_at": status["finished_at"],
            "body_secret": "RECEIPT_BODY_MUST_NOT_ENTER_CONTEXT",
        }
        self.write_work_json(receipt_relative, receipt)
        mismatched = self.run_cli("recover", "--json")
        self.assertEqual(mismatched.returncode, 2)
        self.assertIn("result do not match", mismatched.stderr)

        receipt["result"] = "pass"
        receipt["finished_at"] = "2026-08-13T00:00:01.000Z"
        self.write_work_json(receipt_relative, receipt)
        wrong_time = self.run_cli("recover", "--json")
        self.assertEqual(wrong_time.returncode, 2)
        self.assertIn("finished_at do not match", wrong_time.stderr)

        receipt["finished_at"] = status["finished_at"]
        self.write_work_json(receipt_relative, receipt)
        recovered = self.run_cli("recover", "--json")
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        packet = json.loads(recovered.stdout)
        receipt_entry = {"path_base": "work_root", "path": receipt_relative}
        self.assertIn(receipt_entry, packet["control_paths"])
        self.assertNotIn(receipt_entry, packet["loaded_context_paths"])
        self.assertEqual(
            packet["state"]["status"]["receipt_freshness"]["status"],
            "unknown_legacy",
        )
        self.assertNotIn("RECEIPT_BODY_MUST_NOT_ENTER_CONTEXT", recovered.stdout)

    def test_accepts_nested_verify_receipt_path(self) -> None:
        receipt_relative = (
            "workspaces/001-example/records/receipts/verify/" "verify-existing.json"
        )
        status = self.verified_status(receipt_relative)
        self.write_work_json(
            receipt_relative,
            {
                "schema_version": 1,
                "workspace_id": "001-example",
                "result": "pass",
                "finished_at": status["finished_at"],
            },
        )
        self.write_status(status)

        recovered = self.run_cli("recover", "--json")

        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        packet = json.loads(recovered.stdout)
        self.assertIn(
            {"path_base": "work_root", "path": receipt_relative},
            packet["control_paths"],
        )

    def test_rejects_non_verify_receipt_types_and_malformed_names(self) -> None:
        invalid_receipts = [
            (
                "workspaces/001-example/records/receipts/harness-tests/"
                "verify-harness.json"
            ),
            (
                "workspaces/001-example/records/receipts/preflight/"
                "verify-preflight.json"
            ),
            ("workspaces/001-example/records/receipts/other/" "verify-other.json"),
            ("workspaces/001-example/records/receipts/verify/" "harness-result.json"),
            ("workspaces/001-example/records/receipts/verify/" "verify-.json"),
            ("workspaces/001-example/records/receipts/verify/" "verify-result.txt"),
            (
                "workspaces/001-example/records/receipts/verify/archive/"
                "verify-result.json"
            ),
        ]
        receipt = {
            "schema_version": 1,
            "workspace_id": "001-example",
            "result": "pass",
            "finished_at": "2026-08-13T00:00:00.000Z",
        }

        for receipt_relative in invalid_receipts:
            with self.subTest(receipt=receipt_relative):
                receipt_path = self.work_root / receipt_relative
                receipt_path.parent.mkdir(parents=True, exist_ok=True)
                self.write_work_json(receipt_relative, receipt)
                self.write_status(self.verified_status(receipt_relative))

                completed = self.run_cli("recover", "--json")

                self.assertEqual(completed.returncode, 2)
                self.assertIn("product Verify receipt", completed.stderr)

    def test_accepts_current_status_and_receipt_schemas(self) -> None:
        receipt_relative = (
            "workspaces/001-example/records/receipts/verify/" "verify-current.json"
        )
        finished_at = "2026-08-14T00:00:00.000Z"
        canonical_basis_files = [
            self.project_snapshot("context/project/common/task-context.md")
        ]
        evidence_files = [self.project_snapshot("src/value.txt")]
        self.write_work_json(
            receipt_relative,
            {
                "schema_version": 2,
                "workspace_id": "001-example",
                "claim": "제품 값이 Project 기준과 일치한다.",
                "result": "pass",
                "finished_at": finished_at,
                "snapshot_sha256": self.snapshot_sha256(
                    canonical_basis_files, evidence_files
                ),
                "canonical_basis_files": canonical_basis_files,
                "evidence_files": evidence_files,
            },
        )
        self.write_status(
            {
                "schema_version": 3,
                "workspace_id": "001-example",
                "status": "verification_passed",
                "result": "pass",
                "receipt": receipt_relative,
                "finished_at": finished_at,
            }
        )

        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        packet = json.loads(completed.stdout)
        self.assertEqual(
            packet["state"]["status"]["value"]["status"],
            "verification_passed",
        )
        self.assertNotIn("next_action", packet["state"]["status"]["value"])
        self.assertEqual(
            packet["state"]["status"]["receipt_freshness"]["status"],
            "fresh",
        )

    def test_current_receipt_reports_changed_and_missing_files_as_stale(
        self,
    ) -> None:
        receipt_relative = (
            "workspaces/001-example/records/receipts/verify/" "verify-freshness.json"
        )
        finished_at = "2026-08-14T00:00:00.000Z"
        canonical_basis_files = [
            self.project_snapshot("context/project/common/task-context.md")
        ]
        evidence_files = [self.project_snapshot("src/value.txt")]
        receipt = {
            "schema_version": 2,
            "workspace_id": "001-example",
            "claim": "제품 값이 Project 기준과 일치한다.",
            "result": "pass",
            "finished_at": finished_at,
            "snapshot_sha256": self.snapshot_sha256(
                canonical_basis_files, evidence_files
            ),
            "canonical_basis_files": canonical_basis_files,
            "evidence_files": evidence_files,
        }
        self.write_work_json(receipt_relative, receipt)
        self.write_status(
            {
                "schema_version": 3,
                "workspace_id": "001-example",
                "status": "verification_passed",
                "result": "pass",
                "receipt": receipt_relative,
                "finished_at": finished_at,
            }
        )
        evidence = self.project_root / "src" / "value.txt"
        evidence.write_text("changed\n", encoding="utf-8")

        changed = self.run_cli("recover", "--json")

        self.assertEqual(changed.returncode, 0, changed.stderr)
        freshness = json.loads(changed.stdout)["state"]["status"]["receipt_freshness"]
        self.assertEqual(freshness["status"], "stale")
        self.assertEqual(freshness["changed_file_count"], 1)
        self.assertEqual(freshness["missing_file_count"], 0)
        self.assertNotIn("src/value.txt", changed.stdout)

        evidence.unlink()
        missing = self.run_cli("recover", "--json")

        self.assertEqual(missing.returncode, 0, missing.stderr)
        freshness = json.loads(missing.stdout)["state"]["status"]["receipt_freshness"]
        self.assertEqual(freshness["status"], "stale")
        self.assertEqual(freshness["changed_file_count"], 0)
        self.assertEqual(freshness["missing_file_count"], 1)

    def test_rejects_unsafe_current_receipt_snapshot_paths(self) -> None:
        receipt_relative = (
            "workspaces/001-example/records/receipts/verify/"
            "verify-unsafe-snapshot.json"
        )
        finished_at = "2026-08-14T00:00:00.000Z"
        canonical_basis_files = [
            self.project_snapshot("context/project/common/task-context.md")
        ]
        evidence_files = [self.project_snapshot("src/value.txt")]
        receipt = {
            "schema_version": 2,
            "workspace_id": "001-example",
            "claim": "제품 값이 Project 기준과 일치한다.",
            "result": "pass",
            "finished_at": finished_at,
            "snapshot_sha256": self.snapshot_sha256(
                canonical_basis_files, evidence_files
            ),
            "canonical_basis_files": canonical_basis_files,
            "evidence_files": evidence_files,
        }
        self.write_status(
            {
                "schema_version": 3,
                "workspace_id": "001-example",
                "status": "verification_passed",
                "result": "pass",
                "receipt": receipt_relative,
                "finished_at": finished_at,
            }
        )

        receipt["evidence_files"][0]["path"] = "../outside.txt"
        receipt["snapshot_sha256"] = self.snapshot_sha256(
            receipt["canonical_basis_files"], receipt["evidence_files"]
        )
        self.write_work_json(receipt_relative, receipt)
        traversal = self.run_cli("recover")
        self.assertEqual(traversal.returncode, 2)
        self.assertIn("traverse", traversal.stderr)

        linked_path = self.project_root / "src" / "linked-value.txt"
        linked_path.symlink_to(self.project_root / "src" / "value.txt")
        receipt["evidence_files"][0] = {
            **self.project_snapshot("src/value.txt"),
            "path": "src/linked-value.txt",
        }
        receipt["snapshot_sha256"] = self.snapshot_sha256(
            receipt["canonical_basis_files"], receipt["evidence_files"]
        )
        self.write_work_json(receipt_relative, receipt)
        symlink = self.run_cli("recover")
        self.assertEqual(symlink.returncode, 2)
        self.assertIn("symlink", symlink.stderr)

    def test_rejects_receipt_symlink(self) -> None:
        outside_receipt = self.project_root / "context" / "project" / "receipt.json"
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
        receipt_relative = "workspaces/001-example/records/verify-linked.json"
        (self.work_root / receipt_relative).symlink_to(outside_receipt)
        self.write_status(self.verified_status(receipt_relative))

        completed = self.run_cli("recover")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)
