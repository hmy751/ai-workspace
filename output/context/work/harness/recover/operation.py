"""Build a bounded recovery packet from recover-owned inputs only."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any

from ..workspace_contract import (
    HarnessError,
    VERIFICATION_RECEIPT_SCHEMA_VERSION,
    WorkspaceIdentity,
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
    load_state_status,
    read_json_without_symlinks,
    read_text_without_symlinks,
    reject_symlink_components,
    resolve_directory_without_symlinks,
    resolve_inside_root,
    resolve_regular_file_without_symlinks,
    select_workspace,
    state_status_path,
    validate_relative_path,
    validate_workspace_id,
)


RECOVER_CONTRACT_SCHEMA_VERSION = 4
RECOVERY_PACKET_SCHEMA_VERSION = 5
PROJECT_CONTEXT_ROOT = "context/project"
REQUIRED_PROJECT_CONTEXT_PATH = "context/project/overview.md"
REQUIRED_MEMORY_FILES = (
    "01-goal.md",
    "02-constraints.md",
    "03-project-context.md",
)


def _recover_contract_path(identity: WorkspaceIdentity) -> str:
    return f"{identity.workspace_path}/recover.json"


def _load_recover_contract(
    project_root: Path,
    work_root: Path,
    identity: WorkspaceIdentity,
) -> dict[str, Any]:
    contract_path = _recover_contract_path(identity)
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
        expect_exact_keys(
            entry, {"path", "reason"}, f"project_context[{index}]"
        )
        path = validate_relative_path(
            entry["path"], f"project_context[{index}].path"
        )
        parts = PurePosixPath(path.replace("\\", "/")).parts
        if parts[:2] != ("context", "project"):
            fail(
                "Project context path must be selected from context/project/"
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

    if validated_context[0]["path"] != REQUIRED_PROJECT_CONTEXT_PATH:
        fail(
            "project_context must select context/project/overview.md first"
        )

    return {
        "schema_version": RECOVER_CONTRACT_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "project_context": validated_context,
    }


def _load_memory(
    work_root: Path, identity: WorkspaceIdentity
) -> tuple[dict[str, str], list[dict[str, str]]]:
    directory_relative = f"{identity.workspace_path}/current/memory"
    directory = resolve_directory_without_symlinks(
        work_root, directory_relative, "Workspace memory directory"
    )
    index_path = f"{directory_relative}/index.md"
    memory_index = {
        "path": index_path,
        "path_base": "work_root",
        "content": read_text_without_symlinks(
            work_root, index_path, "Workspace memory index"
        ),
    }

    missing_required = [
        name
        for name in REQUIRED_MEMORY_FILES
        if not (directory / name).is_file()
    ]
    if missing_required:
        fail(
            "Workspace memory is missing required files: "
            + ", ".join(missing_required)
        )

    entries: list[dict[str, str]] = []
    for candidate in sorted(directory.iterdir(), key=lambda path: path.name):
        if candidate.name == "index.md" or not candidate.name.endswith(".md"):
            continue
        relative_path = f"{directory_relative}/{candidate.name}"
        entries.append(
            {
                "path": relative_path,
                "path_base": "work_root",
                "content": read_text_without_symlinks(
                    work_root,
                    relative_path,
                    f"Workspace memory context {candidate.name}",
                ),
            }
        )
    return memory_index, entries


def _load_output_index(
    work_root: Path, identity: WorkspaceIdentity
) -> dict[str, str]:
    """Load only the Workspace goal-output map, never artifact bodies."""

    directory_relative = f"{identity.workspace_path}/output"
    resolve_directory_without_symlinks(
        work_root, directory_relative, "Workspace output directory"
    )
    index_path = f"{directory_relative}/index.md"
    return {
        "path": index_path,
        "path_base": "work_root",
        "content": read_text_without_symlinks(
            work_root, index_path, "Workspace output index"
        ),
    }


def _validate_linked_receipt(
    work_root: Path,
    identity: WorkspaceIdentity,
    status: dict[str, Any],
) -> str | None:
    """Validate only the status-linked receipt header; return no body."""

    if status["receipt"] is None:
        return None

    receipt_relative = status["receipt"]
    records_relative = f"{identity.workspace_path}/records"
    records_dir = resolve_directory_without_symlinks(
        work_root, records_relative, "Workspace records directory"
    )
    reject_symlink_components(
        work_root, receipt_relative, "state status receipt"
    )
    receipt_path = resolve_inside_root(
        work_root, receipt_relative, "state status receipt"
    )
    try:
        receipt_path.relative_to(records_dir)
    except ValueError as exc:
        raise HarnessError(
            "state status receipt must resolve inside this Workspace's records/"
        ) from exc
    if not receipt_path.is_file():
        fail("state status receipt must be a regular file")

    receipt = read_json_without_symlinks(
        work_root, receipt_relative, "state status receipt"
    )
    for field in ("schema_version", "workspace_id", "result", "finished_at"):
        if field not in receipt:
            fail(f"state status receipt is missing {field}")
    expect_schema_version(
        receipt["schema_version"],
        VERIFICATION_RECEIPT_SCHEMA_VERSION,
        "verification receipt",
    )
    if receipt["workspace_id"] != identity.workspace_id:
        fail("state status and receipt workspace_id do not match")
    if receipt["result"] != status["result"]:
        fail("state status and receipt result do not match")
    if receipt["finished_at"] != status["finished_at"]:
        fail("state status and receipt finished_at do not match")
    return receipt_relative


def build_recovery_packet(
    project_root: Path,
    work_root: Path,
    explicit_workspace_id: str | None = None,
) -> dict[str, Any]:
    """Build the recovery packet without reading verify.json or receipt body."""

    identity = select_workspace(work_root, explicit_workspace_id)
    recover_contract_path = _recover_contract_path(identity)
    contract = _load_recover_contract(project_root, work_root, identity)
    memory_index, memory_entries = _load_memory(work_root, identity)

    state_directory = f"{identity.workspace_path}/current/state"
    resolve_directory_without_symlinks(
        work_root, state_directory, "Workspace state directory"
    )
    state_index_path = f"{state_directory}/index.md"
    status_path = state_status_path(identity)
    state_index = {
        "path": state_index_path,
        "path_base": "work_root",
        "content": read_text_without_symlinks(
            work_root, state_index_path, "Workspace state index"
        ),
    }
    state_status = load_state_status(work_root, identity)
    linked_receipt = _validate_linked_receipt(
        work_root, identity, state_status
    )
    output_index = _load_output_index(work_root, identity)

    selected_context: list[dict[str, str]] = []
    loaded_paths = [
        {"path_base": "work_root", "path": memory_index["path"]}
    ]
    loaded_paths.extend(
        {"path_base": "work_root", "path": entry["path"]}
        for entry in memory_entries
    )
    loaded_paths.extend(
        [
            {"path_base": "work_root", "path": state_index_path},
            {"path_base": "work_root", "path": status_path},
            {"path_base": "work_root", "path": output_index["path"]},
        ]
    )
    for entry in contract["project_context"]:
        selected_context.append(
            {
                "path": entry["path"],
                "path_base": "project_root",
                "reason": entry["reason"],
                "content": read_text_without_symlinks(
                    project_root,
                    entry["path"],
                    f"selected Project context {entry['path']}",
                ),
            }
        )
        loaded_paths.append(
            {"path_base": "project_root", "path": entry["path"]}
        )

    control_paths = [
        {"path_base": "work_root", "path": identity.index_path},
        {"path_base": "work_root", "path": identity.identity_path},
        {"path_base": "work_root", "path": recover_contract_path},
    ]
    if linked_receipt is not None:
        control_paths.append(
            {"path_base": "work_root", "path": linked_receipt}
        )

    return {
        "schema_version": RECOVERY_PACKET_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "workspace": {
            "path_base": "work_root",
            "path": identity.workspace_path,
        },
        "recover_contract": {
            "path_base": "work_root",
            "path": recover_contract_path,
        },
        "control_paths": control_paths,
        "loaded_context_paths": loaded_paths,
        "memory": {"index": memory_index, "entries": memory_entries},
        "state": {
            "index": state_index,
            "status": {
                "path_base": "work_root",
                "path": status_path,
                "receipt_path_base": "work_root",
                "value": state_status,
            },
        },
        "output": {"index": output_index},
        "project_context": selected_context,
    }


def render_recovery_packet(packet: dict[str, Any]) -> str:
    """Render the recovery packet for a human without verify configuration."""

    lines = [
        f"# Workspace recovery: {packet['workspace_id']}",
        "",
        (
            "Workspace: "
            f"[{packet['workspace']['path_base']}] "
            f"{packet['workspace']['path']}"
        ),
        (
            "Recover contract: "
            f"[{packet['recover_contract']['path_base']}] "
            f"{packet['recover_contract']['path']}"
        ),
        "Control paths read to select the Workspace and validate handoff:",
    ]
    lines.extend(
        f"- [{entry['path_base']}] {entry['path']}"
        for entry in packet["control_paths"]
    )
    lines.extend(["", "Loaded context paths (in recovery order):"])
    lines.extend(
        f"- [{entry['path_base']}] {entry['path']}"
        for entry in packet["loaded_context_paths"]
    )

    memory = packet["memory"]
    lines.extend(
        ["", "## memory/index.md", "", memory["index"]["content"].rstrip()]
    )
    for entry in memory["entries"]:
        lines.extend(
            [
                "",
                (
                    "## Memory context: "
                    f"[{entry['path_base']}] {entry['path']}"
                ),
                "",
                entry["content"].rstrip(),
            ]
        )

    state = packet["state"]
    lines.extend(
        ["", "## state/index.md", "", state["index"]["content"].rstrip()]
    )
    lines.extend(["", "## state/status.json", ""])
    for field in ("status", "result", "finished_at", "receipt", "next_action"):
        value = state["status"]["value"][field]
        rendered = "null" if value is None else str(value)
        suffix = (
            f" [{state['status']['receipt_path_base']}]"
            if field == "receipt" and value is not None
            else ""
        )
        lines.append(f"- {field}: {rendered}{suffix}")

    output = packet["output"]
    lines.extend(
        ["", "## output/index.md", "", output["index"]["content"].rstrip()]
    )

    for entry in packet["project_context"]:
        lines.extend(
            [
                "",
                (
                    "## Project context: "
                    f"[{entry['path_base']}] {entry['path']}"
                ),
                "",
                f"Selection reason: {entry['reason']}",
                "",
                entry["content"].rstrip(),
            ]
        )
    return "\n".join(lines) + "\n"
