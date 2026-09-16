"""검사된 입력을 읽기 전용 recovery packet으로 조립한다."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..workspace.identity import select_workspace
from ..workspace.status import state_status_path
from .context import load_memory, load_output_index, load_project_context, load_state
from .contract import load_recover_contract, recover_contract_path
from .receipts import validate_linked_receipt

RECOVERY_PACKET_SCHEMA_VERSION = 6


def build_recovery_packet(
    project_root: Path,
    work_root: Path,
    explicit_workspace_id: str | None = None,
) -> dict[str, Any]:
    """verify.json과 receipt 본문을 노출하지 않는 읽기 전용 packet을 만든다."""

    identity = select_workspace(work_root, explicit_workspace_id)
    contract_path = recover_contract_path(identity)
    contract = load_recover_contract(project_root, work_root, identity)
    memory_index, memory_entries = load_memory(work_root, identity)

    state_index, state_status = load_state(work_root, identity)
    status_path = state_status_path(identity)
    linked_receipt, receipt_freshness = validate_linked_receipt(
        project_root, work_root, identity, state_status
    )
    output_index = load_output_index(work_root, identity)

    selected_context = load_project_context(project_root, contract["project_context"])

    # Context 본문과 선택·인계 검사용 제어 경로를 구별한다.
    # Receipt는 검사했더라도 모델에 읽힐 본문 목록에는 포함하지 않는다.
    loaded_paths = [{"path_base": "work_root", "path": memory_index["path"]}]
    loaded_paths.extend(
        {"path_base": "work_root", "path": entry["path"]} for entry in memory_entries
    )
    loaded_paths.extend(
        [
            {"path_base": "work_root", "path": state_index["path"]},
            {"path_base": "work_root", "path": status_path},
            {"path_base": "work_root", "path": output_index["path"]},
        ]
    )
    loaded_paths.extend(
        {"path_base": "project_root", "path": entry["path"]}
        for entry in selected_context
    )

    control_paths = [
        {"path_base": "work_root", "path": identity.identity_path},
        {"path_base": "work_root", "path": contract_path},
    ]
    if identity.index_path is not None:
        control_paths.insert(0, {"path_base": "work_root", "path": identity.index_path})
    if linked_receipt is not None:
        control_paths.append({"path_base": "work_root", "path": linked_receipt})

    return {
        "schema_version": RECOVERY_PACKET_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "workspace": {
            "path_base": "work_root",
            "path": identity.workspace_path,
        },
        "recover_contract": {
            "path_base": "work_root",
            "path": contract_path,
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
                "receipt_freshness": receipt_freshness,
                "value": state_status,
            },
        },
        "output": {"index": output_index},
        "project_context": selected_context,
    }
