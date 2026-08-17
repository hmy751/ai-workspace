"""Validate evidence recording isolation from Recover and product state."""

from __future__ import annotations

import json

from context.work.harness.testing import HARNESS_SOURCE, WorkspaceFixture


class EphemeralWorkspaceStatePreservationTests(WorkspaceFixture):
    def _checked_in_workspace_machine_state(self) -> dict[str, bytes]:
        """Snapshot active product status/receipts without writing to them."""
        reference_work_root = HARNESS_SOURCE.parent
        index = json.loads(
            (reference_work_root / "workspaces" / "index.json").read_text(
                encoding="utf-8"
            )
        )
        workspace_root = (
            reference_work_root
            / "workspaces"
            / index["active_workspace_id"]
        )
        machine_paths = [workspace_root / "current" / "state" / "status.json"]
        receipts_root = workspace_root / "records" / "receipts"
        if receipts_root.is_dir():
            machine_paths.extend(
                path for path in receipts_root.rglob("*") if path.is_file()
            )
        return {
            str(path.relative_to(reference_work_root)): path.read_bytes()
            for path in sorted(machine_paths)
        }

    def test_ephemeral_cycle_preserves_recover_and_product_state(self) -> None:
        checked_in_before = self._checked_in_workspace_machine_state()
        status_path = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "current"
            / "state"
            / "status.json"
        )
        legacy_verify_path = (
            self.work_root / "workspaces" / "001-example" / "verify.json"
        )
        product_path = self.project_root / "src" / "value.txt"
        command_marker = self.project_root / "product-command-ran.txt"
        (self.project_root / "would-run.py").write_text(
            "from pathlib import Path\n"
            "Path('product-command-ran.txt').write_text('ran', encoding='utf-8')\n",
            encoding="utf-8",
        )
        legacy_contract = json.loads(
            legacy_verify_path.read_text(encoding="utf-8")
        )
        legacy_contract["verification"]["argv"] = [
            "python3",
            "would-run.py",
        ]
        legacy_verify_path.write_text(
            json.dumps(legacy_contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        status_before = status_path.read_bytes()
        legacy_verify_before = legacy_verify_path.read_bytes()
        product_before = product_path.read_bytes()
        legacy_receipts_before = self.receipt_files()

        first_recover = self.run_cli("recover", "001-example", "--json")
        self.assertEqual(
            first_recover.returncode,
            0,
            first_recover.stdout + first_recover.stderr,
        )
        first_packet = json.loads(first_recover.stdout)
        self.assertEqual(first_packet["workspace_id"], "001-example")

        evidence_payload = {
            "schema_version": 1,
            "observed_at": "2026-08-17T20:30:45+09:00",
            "producer": "Harness validation fixture",
            "subject": "pre-existing default timeout check",
            "method": "fixture reports an already completed check",
            "outcome": "partial",
            "result_summary": "recording isolation was the only claimed result",
            "source_refs": [],
            "unverified_scope": [
                "the product command was intentionally not executed"
            ],
        }
        evidence_input = self.project_root / "evidence-input.json"
        evidence_input.write_text(
            json.dumps(evidence_payload, ensure_ascii=False), encoding="utf-8"
        )

        recorded = self.run_cli(
            "verify",
            "001-example",
            "--input-json",
            "evidence-input.json",
        )
        self.assertEqual(
            recorded.returncode, 0, recorded.stdout + recorded.stderr
        )
        summary = json.loads(recorded.stdout)
        self.assertIs(summary["recorded"], True)
        self.assertEqual(summary["evidence_outcome"], "partial")
        receipt_path = self.work_root / summary["receipt"]
        self.assertTrue(receipt_path.is_file())
        self.assertTrue(receipt_path.name.startswith("evidence-"))

        self.assertEqual(status_path.read_bytes(), status_before)
        self.assertEqual(legacy_verify_path.read_bytes(), legacy_verify_before)
        self.assertEqual(product_path.read_bytes(), product_before)
        self.assertFalse(command_marker.exists())
        self.assertEqual(self.receipt_files(), legacy_receipts_before)

        second_recover = self.run_cli("recover", "001-example", "--json")
        self.assertEqual(
            second_recover.returncode,
            0,
            second_recover.stdout + second_recover.stderr,
        )
        second_packet = json.loads(second_recover.stdout)
        self.assertEqual(second_packet, first_packet)
        self.assertNotIn(summary["receipt"], second_recover.stdout)
        self.assertEqual(
            self._checked_in_workspace_machine_state(), checked_in_before
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
