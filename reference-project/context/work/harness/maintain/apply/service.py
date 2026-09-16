"""결정을 검증하고 변경 준비와 반영을 연결한다."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...workspace_contract import fail
from ..contracts.decision import validate_maintain_decision
from .prepare import _resolve_project_and_workspace, _prepare_changes
from .transaction import _commit_prepared_changes


def _result(
    decision: dict[str, Any],
    context_status: str,
    changed: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "context_status": context_status,
        "workspace_id": decision["workspace_id"],
        "changed": changed,
        "importance": decision["importance"],
        "summary": decision["summary"],
        "evidence": decision["evidence"],
        "unresolved": decision["unresolved"],
        "question": decision["question"],
    }


def apply_maintain_decision(
    project_root: Path,
    work_root: Path,
    workspace_id: str,
    decision: Any,
) -> dict[str, Any]:
    """명시적 Workspace와 변경 전 조건이 검증된 결정만 반영한다."""

    validated = validate_maintain_decision(decision, workspace_id)
    resolved_project_root, workspace_root, identity = _resolve_project_and_workspace(
        project_root, work_root, workspace_id
    )
    if identity.workspace_id != validated["workspace_id"]:
        fail("Maintain decision Workspace binding changed before apply")

    if validated["outcome"] == "no_change":
        return _result(validated, "no_change", [])
    if validated["outcome"] == "needs_user_decision":
        return _result(validated, "needs_user_decision", [])

    prepared = _prepare_changes(
        resolved_project_root,
        workspace_root,
        validated["changes"],
    )
    changed = _commit_prepared_changes(workspace_root, prepared)
    return _result(validated, "updated", changed)
