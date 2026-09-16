"""명시적 Workspace의 기존 Recover 결과를 bounded 초기 맥락으로 사용한다."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..recover import build_recovery_packet
from ..workspace_contract import fail, validate_workspace_id


def bootstrap_workspace(
    project_root: Path,
    work_root: Path,
    workspace_id: str,
) -> dict[str, Any]:
    """명시적으로 선택한 Workspace의 제한된 Recover 결과를 구성한다."""

    explicit_workspace_id = validate_workspace_id(workspace_id)
    packet = build_recovery_packet(
        project_root,
        work_root,
        explicit_workspace_id,
    )
    if packet["workspace_id"] != explicit_workspace_id:
        fail("Maintain bootstrap Workspace binding changed during recovery")
    if any(
        entry["path_base"] == "work_root" and entry["path"] == "workspaces/index.json"
        for entry in packet["control_paths"]
    ):
        fail("Maintain bootstrap must not use the active Workspace index")
    return packet
