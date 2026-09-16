"""Recover와 Verify가 인계하는 status와 receipt 경로 계약을 소유한다."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .identity import WorkspaceIdentity, validate_workspace_id
from .paths import read_json_without_symlinks, validate_relative_path
from .validation import expect_exact_keys, expect_nonempty_string, fail

LEGACY_STATE_STATUS_SCHEMA_VERSION = 2
STATE_STATUS_SCHEMA_VERSION = 3
SUPPORTED_STATE_STATUS_SCHEMA_VERSIONS = frozenset(
    {LEGACY_STATE_STATUS_SCHEMA_VERSION, STATE_STATUS_SCHEMA_VERSION}
)
LEGACY_VERIFICATION_RECEIPT_SCHEMA_VERSION = 1
VERIFICATION_RECEIPT_SCHEMA_VERSION = 2
SUPPORTED_VERIFICATION_RECEIPT_SCHEMA_VERSIONS = frozenset(
    {
        LEGACY_VERIFICATION_RECEIPT_SCHEMA_VERSION,
        VERIFICATION_RECEIPT_SCHEMA_VERSION,
    }
)
STATE_STATUSES_BY_SCHEMA_VERSION = {
    LEGACY_STATE_STATUS_SCHEMA_VERSION: {
        "ready_for_verification": None,
        "verification_failed": "fail",
        "verified_waiting_acceptance": "pass",
    },
    STATE_STATUS_SCHEMA_VERSION: {
        "ready_for_verification": None,
        "verification_failed": "fail",
        "verification_passed": "pass",
    },
}


def validate_verification_receipt_path(value: Any, workspace_id: str) -> str:
    """해당 Workspace가 소유한 제품 Verify receipt 경로만 허용한다."""

    receipt = validate_relative_path(value, "state status receipt")
    records_prefix = f"workspaces/{workspace_id}/records"
    allowed_prefixes = (
        f"{records_prefix}/receipts/verify/verify-",
        f"{records_prefix}/verify-",
    )
    for prefix in allowed_prefixes:
        if not receipt.startswith(prefix):
            continue
        filename_suffix = receipt[len(prefix) :]
        if (
            filename_suffix != ".json"
            and filename_suffix.endswith(".json")
            and "/" not in filename_suffix
            and "\\" not in filename_suffix
        ):
            return receipt
    fail(
        "state status receipt must identify this Workspace's product Verify "
        "receipt at records/receipts/verify/verify-*.json or legacy "
        "records/verify-*.json"
    )


def validate_state_status(status: dict[str, Any], workspace_id: str) -> dict[str, Any]:
    schema_version = status.get("schema_version")
    if (
        type(schema_version) is not int
        or schema_version not in SUPPORTED_STATE_STATUS_SCHEMA_VERSIONS
    ):
        fail(
            "unsupported Workspace state status schema_version: " f"{schema_version!r}"
        )
    expected_keys = {
        "schema_version",
        "workspace_id",
        "status",
        "result",
        "receipt",
        "finished_at",
    }
    if schema_version == LEGACY_STATE_STATUS_SCHEMA_VERSION:
        expected_keys.add("next_action")
    expect_exact_keys(
        status,
        expected_keys,
        "Workspace state status",
    )
    if validate_workspace_id(status["workspace_id"]) != workspace_id:
        fail("state status workspace_id does not match the selected workspace")
    expected_results = STATE_STATUSES_BY_SCHEMA_VERSION[schema_version]
    if (
        not isinstance(status["status"], str)
        or status["status"] not in expected_results
    ):
        fail(f"invalid Workspace state status: {status['status']!r}")
    if status["result"] is not None and (
        not isinstance(status["result"], str)
        or status["result"] not in {"pass", "fail"}
    ):
        fail("state status result must be null, 'pass', or 'fail'")
    for field in ("receipt", "finished_at"):
        if status[field] is not None and not isinstance(status[field], str):
            fail(f"state status {field} must be a string or null")
    if schema_version == LEGACY_STATE_STATUS_SCHEMA_VERSION:
        expect_nonempty_string(status["next_action"], "state status next_action")

    expected_result = expected_results[status["status"]]
    if status["result"] != expected_result:
        fail("state status and result are inconsistent")
    if status["status"] == "ready_for_verification":
        if any(status[field] is not None for field in ("receipt", "finished_at")):
            fail("ready_for_verification status must not have a receipt or time")
        return status

    validate_verification_receipt_path(
        expect_nonempty_string(status["receipt"], "state status receipt"),
        workspace_id,
    )
    expect_nonempty_string(status["finished_at"], "state status finished_at")
    return status


def state_status_path(identity: WorkspaceIdentity) -> str:
    return f"{identity.workspace_path}/current/state/status.json"


def load_state_status(work_root: Path, identity: WorkspaceIdentity) -> dict[str, Any]:
    status = read_json_without_symlinks(
        work_root, state_status_path(identity), "Workspace state status"
    )
    return validate_state_status(status, identity.workspace_id)
