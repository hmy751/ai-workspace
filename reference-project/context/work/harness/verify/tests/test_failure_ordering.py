"""입력·실행·receipt·status 사이에서 실패가 다음 부작용을 막는지 검증한다."""

from __future__ import annotations

from unittest.mock import patch

from context.work.harness.testing import WorkspaceFixture
from context.work.harness.verify import service
from context.work.harness.workspace.validation import HarnessError


def successful_execution() -> dict[str, object]:
    """외부 명령 없이 실행 조정·저장 순서만 검사할 성공 결과."""

    return {
        "exit_code": 0,
        "process_returncode": 0,
        "timed_out": False,
        "stdout": "",
        "stderr": "",
        "output_capture": {},
        "normalization": {},
    }


class VerifyFailureOrderingTests(WorkspaceFixture):
    def test_snapshot_failure_prevents_execution_and_all_writes(self) -> None:
        before = self.read_status()
        with (
            patch.object(
                service, "snapshot_files", side_effect=HarnessError("unreadable")
            ),
            patch.object(service, "run_bounded_verification") as execute,
        ):
            with self.assertRaisesRegex(HarnessError, "unreadable"):
                service.verify_workspace(
                    self.project_root, self.work_root, "001-example"
                )
            execute.assert_not_called()
        self.assertEqual(self.read_status(), before)
        self.assertEqual(self.receipt_files(), [])

    def test_evidence_failure_after_basis_capture_still_prevents_execution(
        self,
    ) -> None:
        with (
            patch.object(
                service,
                "snapshot_files",
                side_effect=[
                    [{"path": "basis", "sha256": "digest", "size": 1}],
                    HarnessError("evidence"),
                ],
            ) as collect,
            patch.object(service, "run_bounded_verification") as execute,
        ):
            with self.assertRaisesRegex(HarnessError, "evidence"):
                service.verify_workspace(
                    self.project_root, self.work_root, "001-example"
                )
            self.assertEqual(collect.call_count, 2)
            execute.assert_not_called()
        self.assertEqual(self.receipt_files(), [])
        self.assertEqual(self.read_status(), self.initial_status())

    def test_receipt_failure_preserves_the_previous_status_cursor(self) -> None:
        before = self.read_status()
        with (
            patch.object(
                service, "run_bounded_verification", return_value=successful_execution()
            ) as execute,
            patch.object(
                service, "write_receipt", side_effect=OSError("receipt storage")
            ),
            patch.object(service, "atomic_write_status") as update,
        ):
            with self.assertRaisesRegex(OSError, "receipt storage"):
                service.verify_workspace(
                    self.project_root, self.work_root, "001-example"
                )
            execute.assert_called_once()
            update.assert_not_called()
        self.assertEqual(self.read_status(), before)
        self.assertEqual(self.receipt_files(), [])

    def test_status_failure_keeps_the_new_receipt_and_the_previous_status(self) -> None:
        before = self.read_status()
        with (
            patch.object(
                service, "run_bounded_verification", return_value=successful_execution()
            ),
            patch.object(
                service, "atomic_write_status", side_effect=OSError("status storage")
            ),
        ):
            with self.assertRaisesRegex(OSError, "status storage"):
                service.verify_workspace(
                    self.project_root, self.work_root, "001-example"
                )
        self.assertEqual(self.read_status(), before)
        receipts = self.receipt_files()
        self.assertEqual(len(receipts), 1)
        self.assertIn('"result": "pass"', receipts[0].read_text(encoding="utf-8"))
