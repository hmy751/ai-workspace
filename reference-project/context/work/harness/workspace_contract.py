"""Minimal contract shared by Workspace recovery and verification."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
from typing import Any, NoReturn


WORKSPACE_INDEX_SCHEMA_VERSION = 1
WORKSPACE_IDENTITY_SCHEMA_VERSION = 1
STATE_STATUS_SCHEMA_VERSION = 2
VERIFICATION_RECEIPT_SCHEMA_VERSION = 1

WORKSPACE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
VALID_STATE_STATUSES = {
    "ready_for_verification",
    "verification_failed",
    "verified_waiting_acceptance",
}


class HarnessError(ValueError):
    """Raised when a Workspace contract is invalid or unsafe."""


@dataclass(frozen=True)
class WorkspaceIdentity:
    """Selected Workspace identity and its work-root-relative paths."""

    workspace_id: str
    workspace_path: str
    index_path: str
    identity_path: str


def fail(message: str) -> NoReturn:
    raise HarnessError(message)


def expect_exact_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    actual = set(value)
    if actual == expected:
        return
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    details = []
    if missing:
        details.append(f"missing={missing}")
    if extra:
        details.append(f"extra={extra}")
    fail(f"invalid {label} keys: {', '.join(details)}")


def expect_schema_version(value: Any, expected: int, label: str) -> None:
    if type(value) is not int or value != expected:
        fail(f"unsupported {label} schema_version: {value!r}")


def expect_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    if "\x00" in value:
        fail(f"{label} must not contain NUL")
    return value


def validate_workspace_id(value: Any) -> str:
    workspace_id = expect_nonempty_string(value, "workspace id")
    if not WORKSPACE_ID_PATTERN.fullmatch(workspace_id):
        fail(
            "workspace id must contain only lowercase letters, digits, '.', "
            "'_' or '-', and must start with a letter or digit"
        )
    if workspace_id in {".", ".."}:
        fail("workspace id must not be '.' or '..'")
    return workspace_id


def validate_relative_path(value: Any, label: str) -> str:
    raw = expect_nonempty_string(value, label)
    normalized = raw.replace("\\", "/")
    normalized_path = PurePosixPath(normalized)
    parts = normalized_path.parts
    if (
        Path(raw).is_absolute()
        or normalized_path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
    ):
        fail(f"{label} must be relative to its declared path base")
    if ".." in parts:
        fail(f"{label} must not traverse outside its declared path base")
    if not parts or parts in {(".",), ()}:
        fail(f"{label} must identify a file")
    return raw


def resolve_inside_root(
    base_root: Path,
    relative_path: str,
    label: str,
) -> Path:
    safe_relative = validate_relative_path(relative_path, label)
    resolved_root = base_root.resolve(strict=True)
    if not resolved_root.is_dir():
        fail(f"{label} path base must be a directory")
    try:
        candidate = (resolved_root / safe_relative).resolve(strict=True)
    except FileNotFoundError as exc:
        raise HarnessError(f"{label} does not exist: {safe_relative}") from exc
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise HarnessError(
            f"{label} resolves outside its declared path base"
        ) from exc
    return candidate


def reject_symlink_components(
    base_root: Path, relative_path: str, label: str
) -> None:
    safe_relative = validate_relative_path(relative_path, label)
    current = base_root.resolve(strict=True)
    for part in PurePosixPath(safe_relative.replace("\\", "/")).parts:
        current = current / part
        if current.is_symlink():
            fail(f"{label} must not use symlink components")


def resolve_directory_without_symlinks(
    base_root: Path, relative_path: str, label: str
) -> Path:
    reject_symlink_components(base_root, relative_path, label)
    path = resolve_inside_root(base_root, relative_path, label)
    if not path.is_dir():
        fail(f"{label} must be a directory: {relative_path}")
    return path


def resolve_regular_file_without_symlinks(
    base_root: Path, relative_path: str, label: str
) -> Path:
    reject_symlink_components(base_root, relative_path, label)
    path = resolve_inside_root(base_root, relative_path, label)
    if not path.is_file():
        fail(f"{label} must be a regular file: {relative_path}")
    return path


def read_text_without_symlinks(
    base_root: Path, relative_path: str, label: str
) -> str:
    path = resolve_regular_file_without_symlinks(
        base_root, relative_path, label
    )
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise HarnessError(f"{label} is not readable UTF-8 text: {exc}") from exc


def _parse_json_object(raw: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        fail(f"{label} must contain a JSON object")
    return value


def read_json_without_symlinks(
    base_root: Path, relative_path: str, label: str
) -> dict[str, Any]:
    return _parse_json_object(
        read_text_without_symlinks(base_root, relative_path, label), label
    )


def _load_workspace_index(work_root: Path) -> dict[str, Any]:
    index = read_json_without_symlinks(
        work_root, "workspaces/index.json", "Workspace index"
    )
    expect_exact_keys(
        index, {"schema_version", "active_workspace_id"}, "Workspace index"
    )
    expect_schema_version(
        index["schema_version"],
        WORKSPACE_INDEX_SCHEMA_VERSION,
        "Workspace index",
    )
    index["active_workspace_id"] = validate_workspace_id(
        index["active_workspace_id"]
    )
    return index


def select_workspace(
    work_root: Path, explicit_workspace_id: str | None
) -> WorkspaceIdentity:
    """Select active/explicit id, then load identity-only workspace.json."""

    index_path = "workspaces/index.json"
    index = _load_workspace_index(work_root)
    workspace_id = (
        index["active_workspace_id"]
        if explicit_workspace_id is None
        else validate_workspace_id(explicit_workspace_id)
    )
    workspace_path = f"workspaces/{workspace_id}"
    identity_path = f"{workspace_path}/workspace.json"
    identity = read_json_without_symlinks(
        work_root, identity_path, "Workspace identity"
    )
    expect_exact_keys(
        identity, {"schema_version", "workspace_id"}, "Workspace identity"
    )
    expect_schema_version(
        identity["schema_version"],
        WORKSPACE_IDENTITY_SCHEMA_VERSION,
        "Workspace identity",
    )
    if validate_workspace_id(identity["workspace_id"]) != workspace_id:
        fail("Workspace identity id does not match the selected workspace")
    return WorkspaceIdentity(
        workspace_id=workspace_id,
        workspace_path=workspace_path,
        index_path=index_path,
        identity_path=identity_path,
    )


def validate_state_status(
    status: dict[str, Any], workspace_id: str
) -> dict[str, Any]:
    expect_exact_keys(
        status,
        {
            "schema_version",
            "workspace_id",
            "status",
            "result",
            "receipt",
            "finished_at",
            "next_action",
        },
        "Workspace state status",
    )
    expect_schema_version(
        status["schema_version"],
        STATE_STATUS_SCHEMA_VERSION,
        "Workspace state status",
    )
    if validate_workspace_id(status["workspace_id"]) != workspace_id:
        fail("state status workspace_id does not match the selected workspace")
    if (
        not isinstance(status["status"], str)
        or status["status"] not in VALID_STATE_STATUSES
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
    expect_nonempty_string(status["next_action"], "state status next_action")

    expected_result = {
        "ready_for_verification": None,
        "verification_failed": "fail",
        "verified_waiting_acceptance": "pass",
    }[status["status"]]
    if status["result"] != expected_result:
        fail("state status and result are inconsistent")
    if status["status"] == "ready_for_verification":
        if any(status[field] is not None for field in ("receipt", "finished_at")):
            fail("ready_for_verification status must not have a receipt or time")
        return status

    receipt = validate_relative_path(
        expect_nonempty_string(status["receipt"], "state status receipt"),
        "state status receipt",
    )
    expect_nonempty_string(status["finished_at"], "state status finished_at")
    expected_prefix = f"workspaces/{workspace_id}/records/"
    if not receipt.startswith(expected_prefix) or not receipt.endswith(".json"):
        fail("state status receipt must identify this Workspace's JSON record")
    return status


def state_status_path(identity: WorkspaceIdentity) -> str:
    return f"{identity.workspace_path}/current/state/status.json"


def load_state_status(
    work_root: Path, identity: WorkspaceIdentity
) -> dict[str, Any]:
    status = read_json_without_symlinks(
        work_root, state_status_path(identity), "Workspace state status"
    )
    return validate_state_status(status, identity.workspace_id)
