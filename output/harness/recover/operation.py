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
    resolve_inside_output,
    resolve_regular_file_without_symlinks,
    select_workspace,
    state_status_path,
    validate_relative_path,
    validate_workspace_id,
)


RECOVER_CONTRACT_SCHEMA_VERSION = 1
RECOVERY_PACKET_SCHEMA_VERSION = 3


def _recover_contract_path(identity: WorkspaceIdentity) -> str:
    return f"{identity.workspace_path}/recover.json"


def _load_recover_contract(
    root: Path, identity: WorkspaceIdentity
) -> dict[str, Any]:
    contract_path = _recover_contract_path(identity)
    contract = read_json_without_symlinks(
        root, contract_path, "Workspace recover contract"
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

    docs_root = resolve_directory_without_symlinks(
        root, "docs", "Project docs directory"
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
        if not parts or parts[0] != "docs":
            fail("Project context path must be selected from docs/")
        if path in seen_paths:
            fail(f"duplicate Project context path: {path}")
        seen_paths.add(path)
        resolved = resolve_regular_file_without_symlinks(
            root, path, f"project_context[{index}].path"
        )
        try:
            resolved.relative_to(docs_root)
        except ValueError as exc:
            raise HarnessError(
                "Project context path must resolve inside docs/"
            ) from exc
        reason = expect_nonempty_string(
            entry["reason"], f"project_context[{index}].reason"
        )
        validated_context.append({"path": path, "reason": reason})

    return {
        "schema_version": RECOVER_CONTRACT_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "project_context": validated_context,
    }


def _load_memory(
    root: Path, identity: WorkspaceIdentity
) -> tuple[dict[str, str], list[dict[str, str]]]:
    directory_relative = f"{identity.workspace_path}/current/memory"
    directory = resolve_directory_without_symlinks(
        root, directory_relative, "Workspace memory directory"
    )
    index_path = f"{directory_relative}/index.md"
    memory_index = {
        "path": index_path,
        "content": read_text_without_symlinks(
            root, index_path, "Workspace memory index"
        ),
    }

    entries: list[dict[str, str]] = []
    for candidate in sorted(directory.iterdir(), key=lambda path: path.name):
        if candidate.name == "index.md" or not candidate.name.endswith(".md"):
            continue
        relative_path = f"{directory_relative}/{candidate.name}"
        entries.append(
            {
                "path": relative_path,
                "content": read_text_without_symlinks(
                    root,
                    relative_path,
                    f"Workspace memory context {candidate.name}",
                ),
            }
        )
    return memory_index, entries


def _validate_linked_receipt(
    root: Path, identity: WorkspaceIdentity, status: dict[str, Any]
) -> str | None:
    """Validate only the status-linked receipt header; return no body."""

    if status["receipt"] is None:
        return None

    receipt_relative = status["receipt"]
    records_relative = f"{identity.workspace_path}/records"
    records_dir = resolve_directory_without_symlinks(
        root, records_relative, "Workspace records directory"
    )
    reject_symlink_components(root, receipt_relative, "state status receipt")
    receipt_path = resolve_inside_output(
        root, receipt_relative, "state status receipt"
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
        root, receipt_relative, "state status receipt"
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
    root: Path, explicit_workspace_id: str | None = None
) -> dict[str, Any]:
    """Build the recovery packet without reading verify.json or receipt body."""

    identity = select_workspace(root, explicit_workspace_id)
    recover_contract_path = _recover_contract_path(identity)
    contract = _load_recover_contract(root, identity)
    memory_index, memory_entries = _load_memory(root, identity)

    state_directory = f"{identity.workspace_path}/current/state"
    resolve_directory_without_symlinks(
        root, state_directory, "Workspace state directory"
    )
    state_index_path = f"{state_directory}/index.md"
    status_path = state_status_path(identity)
    state_index = {
        "path": state_index_path,
        "content": read_text_without_symlinks(
            root, state_index_path, "Workspace state index"
        ),
    }
    state_status = load_state_status(root, identity)
    linked_receipt = _validate_linked_receipt(root, identity, state_status)

    selected_context: list[dict[str, str]] = []
    loaded_paths = [memory_index["path"]]
    loaded_paths.extend(entry["path"] for entry in memory_entries)
    loaded_paths.extend([state_index_path, status_path])
    for entry in contract["project_context"]:
        selected_context.append(
            {
                "path": entry["path"],
                "reason": entry["reason"],
                "content": read_text_without_symlinks(
                    root,
                    entry["path"],
                    f"selected Project context {entry['path']}",
                ),
            }
        )
        loaded_paths.append(entry["path"])

    control_paths = [
        identity.index_path,
        identity.identity_path,
        recover_contract_path,
    ]
    if linked_receipt is not None:
        control_paths.append(linked_receipt)

    return {
        "schema_version": RECOVERY_PACKET_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "workspace_path": identity.workspace_path,
        "recover_contract_path": recover_contract_path,
        "control_paths": control_paths,
        "loaded_context_paths": loaded_paths,
        "memory": {"index": memory_index, "entries": memory_entries},
        "state": {
            "index": state_index,
            "status": {"path": status_path, "value": state_status},
        },
        "project_context": selected_context,
    }


def render_recovery_packet(packet: dict[str, Any]) -> str:
    """Render the recovery packet for a human without verify configuration."""

    lines = [
        f"# Workspace recovery: {packet['workspace_id']}",
        "",
        f"Workspace: {packet['workspace_path']}",
        f"Recover contract: {packet['recover_contract_path']}",
        "Control paths read to select the Workspace and validate handoff:",
    ]
    lines.extend(f"- {path}" for path in packet["control_paths"])
    lines.extend(["", "Loaded context paths (in recovery order):"])
    lines.extend(f"- {path}" for path in packet["loaded_context_paths"])

    memory = packet["memory"]
    lines.extend(
        ["", "## memory/index.md", "", memory["index"]["content"].rstrip()]
    )
    for entry in memory["entries"]:
        lines.extend(
            ["", f"## Memory context: {entry['path']}", "", entry["content"].rstrip()]
        )

    state = packet["state"]
    lines.extend(
        ["", "## state/index.md", "", state["index"]["content"].rstrip()]
    )
    lines.extend(["", "## state/status.json", ""])
    for field in ("status", "result", "finished_at", "receipt", "next_action"):
        value = state["status"]["value"][field]
        rendered = "null" if value is None else str(value)
        lines.append(f"- {field}: {rendered}")

    for entry in packet["project_context"]:
        lines.extend(
            [
                "",
                f"## Project context: {entry['path']}",
                "",
                f"Selection reason: {entry['reason']}",
                "",
                entry["content"].rstrip(),
            ]
        )
    return "\n".join(lines) + "\n"
