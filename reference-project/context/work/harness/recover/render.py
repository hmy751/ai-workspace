"""Recovery packet을 기존 텍스트 형식으로 출력한다."""

from __future__ import annotations

from typing import Any


def render_recovery_packet(packet: dict[str, Any]) -> str:
    """Verify 설정 없이 packet을 사람이 읽는 기존 형식으로 출력한다."""

    lines = [
        f"# Workspace recovery: {packet['workspace_id']}",
        # 한국어: Workspace 복구: {workspace_id}.
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
        # 한국어: Workspace 선택과 인계 검사를 위해 읽은 제어 경로.
    ]
    lines.extend(
        f"- [{entry['path_base']}] {entry['path']}" for entry in packet["control_paths"]
    )
    lines.extend(["", "Loaded context paths (in recovery order):"])
    # 한국어: 복구 순서대로 읽은 Context 경로.
    lines.extend(
        f"- [{entry['path_base']}] {entry['path']}"
        for entry in packet["loaded_context_paths"]
    )

    memory = packet["memory"]
    lines.extend(["", "## memory/index.md", "", memory["index"]["content"].rstrip()])
    for entry in memory["entries"]:
        lines.extend(
            [
                "",
                ("## Memory context: " f"[{entry['path_base']}] {entry['path']}"),
                # 한국어: Memory Context: [경로 기준] {경로}.
                "",
                entry["content"].rstrip(),
            ]
        )

    state = packet["state"]
    lines.extend(["", "## state/index.md", "", state["index"]["content"].rstrip()])
    lines.extend(["", "## state/status.json", ""])
    status_fields = ["status", "result", "finished_at", "receipt"]
    if "next_action" in state["status"]["value"]:
        status_fields.append("next_action")
    for field in status_fields:
        value = state["status"]["value"][field]
        rendered = "null" if value is None else str(value)
        suffix = (
            f" [{state['status']['receipt_path_base']}]"
            if field == "receipt" and value is not None
            else ""
        )
        lines.append(f"- {field}: {rendered}{suffix}")
    freshness = state["status"]["receipt_freshness"]
    lines.append(f"- receipt_freshness: {freshness['status']}")
    if freshness["snapshot_file_count"]:
        lines.append(
            "- receipt_snapshot_files: "
            f"{freshness['snapshot_file_count']} "
            f"(changed={freshness['changed_file_count']}, "
            f"missing={freshness['missing_file_count']}, "
            f"unavailable={freshness['unavailable_file_count']})"
        )

    output = packet["output"]
    lines.extend(["", "## output/index.md", "", output["index"]["content"].rstrip()])

    for entry in packet["project_context"]:
        lines.extend(
            [
                "",
                ("## Project context: " f"[{entry['path_base']}] {entry['path']}"),
                # 한국어: Project Context: [경로 기준] {경로}.
                "",
                f"Selection reason: {entry['reason']}",
                # 한국어: 선택 이유: {reason}.
                "",
                entry["content"].rstrip(),
            ]
        )
    return "\n".join(lines) + "\n"
