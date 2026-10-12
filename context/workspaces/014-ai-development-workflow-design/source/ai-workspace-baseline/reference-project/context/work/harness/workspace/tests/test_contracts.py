"""Workspace의 공통 값·경로·상태 계약과 기존 import 호환을 검증한다."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import unittest

from context.work.harness import workspace_contract
from context.work.harness.workspace import (
    HarnessError,
    WorkspaceIdentity,
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    validate_relative_path,
    validate_state_status,
    validate_workspace_id,
)


class WorkspaceValueContractTests(unittest.TestCase):
    def test_old_imports_refer_to_the_same_public_contracts(self) -> None:
        from context.work.harness import workspace

        self.assertEqual(set(workspace_contract.__all__), set(workspace.__all__))
        for name in workspace.__all__:
            with self.subTest(name=name):
                self.assertIs(
                    getattr(workspace_contract, name), getattr(workspace, name)
                )

    def test_identity_retains_frozen_dataclass_behavior(self) -> None:
        identity = WorkspaceIdentity(
            "001-example", "workspaces/001-example", None, "id"
        )
        self.assertEqual(
            identity,
            WorkspaceIdentity("001-example", "workspaces/001-example", None, "id"),
        )
        with self.assertRaises(FrozenInstanceError):
            identity.workspace_id = "002-other"

    def test_schema_version_requires_an_integer_not_a_boolean(self) -> None:
        expect_schema_version(1, 1, "fixture")
        for value in (True, 1.0, "1", None, 2):
            with self.subTest(value=value), self.assertRaises(HarnessError):
                expect_schema_version(value, 1, "fixture")

    def test_exact_keys_reports_missing_and_extra_fields(self) -> None:
        with self.assertRaisesRegex(HarnessError, "missing=.*required.*extra=.*extra"):
            expect_exact_keys({"extra": 1}, {"required"}, "fixture")

    def test_strings_reject_empty_values_and_nul_without_normalizing_valid_input(
        self,
    ) -> None:
        self.assertEqual(expect_nonempty_string(" 값 ", "fixture"), " 값 ")
        for value in ("", "  ", None, 1, "a\x00b"):
            with self.subTest(value=value), self.assertRaises(HarnessError):
                expect_nonempty_string(value, "fixture")

    def test_workspace_ids_reject_unsafe_or_ambiguous_values(self) -> None:
        self.assertEqual(validate_workspace_id("001-example.v2"), "001-example.v2")
        for value in (".", "..", "UPPER", "a/b", " a", "-a"):
            with self.subTest(value=value), self.assertRaises(HarnessError):
                validate_workspace_id(value)

    def test_relative_paths_reject_posix_windows_and_embedded_traversal(self) -> None:
        self.assertEqual(
            validate_relative_path("docs/설명.md", "fixture"), "docs/설명.md"
        )
        for value in ("/tmp/a", "C:/outside/a", "../a", "a/../b", "a\\..\\b", ".", ""):
            with self.subTest(value=value), self.assertRaises(HarnessError):
                validate_relative_path(value, "fixture")


class WorkspaceStatusContractTests(unittest.TestCase):
    def status(self, **changes: object) -> dict[str, object]:
        return {
            "schema_version": 3,
            "workspace_id": "001-example",
            "status": "verification_passed",
            "result": "pass",
            "receipt": "workspaces/001-example/records/receipts/verify/verify-result.json",
            "finished_at": "2026-09-16T00:00:00.000Z",
            **changes,
        }

    def test_current_and_legacy_handoffs_keep_their_own_status_names(self) -> None:
        current = self.status()
        legacy = self.status(
            schema_version=2,
            status="verified_waiting_acceptance",
            receipt="workspaces/001-example/records/verify-legacy.json",
            next_action="기록을 검토한다.",
        )
        self.assertIs(validate_state_status(current, "001-example"), current)
        self.assertIs(validate_state_status(legacy, "001-example"), legacy)
        self.assertNotIn("next_action", current)

    def test_handoff_rejects_wrong_workspace_outcome_and_receipt_namespace(
        self,
    ) -> None:
        for changes in (
            {"workspace_id": "002-other"},
            {"result": "fail"},
            {"receipt": "workspaces/002-other/records/verify-result.json"},
            {
                "receipt": "workspaces/001-example/records/receipts/other/verify-result.json"
            },
            {"receipt": "workspaces/001-example/records/receipts/verify/verify-.json"},
            {"finished_at": ""},
        ):
            with self.subTest(changes=changes), self.assertRaises(HarnessError):
                validate_state_status(self.status(**changes), "001-example")

    def test_ready_status_cannot_retain_a_completed_receipt_cursor(self) -> None:
        with self.assertRaisesRegex(HarnessError, "must not have a receipt"):
            validate_state_status(
                self.status(status="ready_for_verification", result=None), "001-example"
            )
