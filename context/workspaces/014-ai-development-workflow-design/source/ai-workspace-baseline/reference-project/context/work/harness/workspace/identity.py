"""명시한 id 또는 active index에서 Workspace 정체성을 선택한다."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from .paths import read_json_without_symlinks
from .validation import (
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
)

WORKSPACE_INDEX_SCHEMA_VERSION = 1
WORKSPACE_IDENTITY_SCHEMA_VERSION = 1
WORKSPACE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


@dataclass(frozen=True)
class WorkspaceIdentity:
    """선택된 Workspace의 정체성과 Work root 상대 경로."""

    workspace_id: str
    workspace_path: str
    index_path: str | None
    identity_path: str


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
    index["active_workspace_id"] = validate_workspace_id(index["active_workspace_id"])
    return index


def select_workspace(
    work_root: Path, explicit_workspace_id: str | None
) -> WorkspaceIdentity:
    """명시한 id를 우선하고, 없을 때만 active Workspace index를 읽는다."""

    if explicit_workspace_id is None:
        index_path: str | None = "workspaces/index.json"
        workspace_id = _load_workspace_index(work_root)["active_workspace_id"]
    else:
        index_path = None
        workspace_id = validate_workspace_id(explicit_workspace_id)
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
