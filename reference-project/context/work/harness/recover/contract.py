"""Recover 전용 설정과 선택된 Project 문서의 경계를 검사한다."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

from ..workspace.identity import WorkspaceIdentity, validate_workspace_id
from ..workspace.paths import (
    read_json_without_symlinks,
    resolve_directory_without_symlinks,
    resolve_regular_file_without_symlinks,
    validate_relative_path,
)
from ..workspace.validation import (
    HarnessError,
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
)

RECOVER_CONTRACT_SCHEMA_VERSION = 6
PROJECT_CONTEXT_ROOT = "context/project"
REQUIRED_PROJECT_CONTEXT_PATH = "context/project/README.md"
PROJECT_CONTEXT_CONTENT_LAYERS = frozenset(
    {"common", "current", "guidance", "decisions"}
)


def recover_contract_path(identity: WorkspaceIdentity) -> str:
    return f"{identity.workspace_path}/recover.json"


def load_recover_contract(
    project_root: Path,
    work_root: Path,
    identity: WorkspaceIdentity,
) -> dict[str, Any]:
    contract_path = recover_contract_path(identity)
    contract = read_json_without_symlinks(
        work_root, contract_path, "Workspace recover contract"
    )
    expect_exact_keys(
        contract,
        {"schema_version", "workspace_id", "project_context"},
        "Workspace recover contract",
    )
    expect_schema_version(
        contract["schema_version"],
        RECOVER_CONTRACT_SCHEMA_VERSION,
        "Workspace recover contract",
    )
    if validate_workspace_id(contract["workspace_id"]) != identity.workspace_id:
        fail("recover contract workspace_id does not match the selected workspace")

    project_context = contract["project_context"]
    if not isinstance(project_context, list) or not project_context:
        fail("project_context must be a non-empty JSON array")

    project_context_root = resolve_directory_without_symlinks(
        project_root, PROJECT_CONTEXT_ROOT, "Project context directory"
    )
    validated_context: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for index, entry in enumerate(project_context):
        if not isinstance(entry, dict):
            fail(f"project_context[{index}] must be a JSON object")
        expect_exact_keys(entry, {"path", "reason"}, f"project_context[{index}]")
        path = validate_relative_path(entry["path"], f"project_context[{index}].path")
        parts = PurePosixPath(path.replace("\\", "/")).parts
        if parts[:2] != ("context", "project"):
            fail("Project context path must be selected from context/project/")
        if path != REQUIRED_PROJECT_CONTEXT_PATH and (
            len(parts) < 4 or parts[2] not in PROJECT_CONTEXT_CONTENT_LAYERS
        ):
            fail(
                "Project context path must be context/project/README.md or "
                "selected from context/project/common/, current/, guidance/, "
                "or decisions/"
            )
        if PurePosixPath(path).suffix != ".md":
            fail("Project context path must be a .md file")
        if path in seen_paths:
            fail(f"duplicate Project context path: {path}")
        seen_paths.add(path)
        resolved = resolve_regular_file_without_symlinks(
            project_root, path, f"project_context[{index}].path"
        )
        try:
            resolved.relative_to(project_context_root)
        except ValueError as exc:
            raise HarnessError(
                "Project context path must resolve inside context/project/"
            ) from exc
        reason = expect_nonempty_string(
            entry["reason"], f"project_context[{index}].reason"
        )
        validated_context.append({"path": path, "reason": reason})

    if REQUIRED_PROJECT_CONTEXT_PATH not in seen_paths:
        fail("project_context must select context/project/README.md")

    return {
        "schema_version": RECOVER_CONTRACT_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "project_context": validated_context,
    }
