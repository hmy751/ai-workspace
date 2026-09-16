"""입력 검사·선확보·실행·receipt·status 반영의 순서를 조정한다."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
from typing import Any

from ..workspace.identity import select_workspace
from ..workspace.paths import (
    resolve_directory_without_symlinks,
    resolve_regular_file_without_symlinks,
)
from ..workspace.status import (
    STATE_STATUS_SCHEMA_VERSION,
    VERIFICATION_RECEIPT_SCHEMA_VERSION,
    load_state_status,
    state_status_path,
)
from .contract import VERIFY_CONTRACT_SCHEMA_VERSION, load_verify_contract
from .evidence import snapshot_files, snapshot_sha256
from .execution import run_bounded_verification
from .output import PROJECT_ROOT_TOKEN
from .storage import (
    atomic_write_status,
    resolve_verify_receipts_directory,
    write_receipt,
)


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _runtime_environment() -> dict[str, Any]:
    """실행을 해석하는 데 필요한 제한된 비민감 환경 정보만 반환한다."""

    return {
        "command_cwd": PROJECT_ROOT_TOKEN,
        "os_name": os.name,
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "verify_contract_schema_version": VERIFY_CONTRACT_SCHEMA_VERSION,
        "verification_receipt_schema_version": VERIFICATION_RECEIPT_SCHEMA_VERSION,
    }


def verify_workspace(
    project_root: Path,
    work_root: Path,
    explicit_workspace_id: str | None = None,
) -> tuple[int, dict[str, Any]]:
    """Verify 설정만 실행하고 receipt 추가 뒤 status를 atomic 갱신한다."""

    # 명령이 부작용을 일으키기 전에 계약·현재 상태·저장 경로를 검사한다.
    identity = select_workspace(work_root, explicit_workspace_id)
    contract = load_verify_contract(project_root, work_root, identity)
    state_directory = f"{identity.workspace_path}/current/state"
    resolve_directory_without_symlinks(
        work_root, state_directory, "Workspace state directory"
    )
    status_relative = state_status_path(identity)
    status_path = resolve_regular_file_without_symlinks(
        work_root, status_relative, "Workspace state status"
    )
    load_state_status(work_root, identity)
    receipts_relative, receipts_dir = resolve_verify_receipts_directory(
        work_root, identity
    )

    verification = contract["verification"]
    # 명령이 입력 파일을 변경하거나 삭제해도 실행 전 증거를 보존한다.
    inputs_collected_at = _utc_now()
    canonical_basis_files = snapshot_files(
        project_root,
        contract["canonical_basis"],
        "canonical_basis",
    )
    evidence_files = snapshot_files(
        project_root,
        verification["evidence_paths"],
        "verification.evidence_paths",
    )
    snapshot_digest = snapshot_sha256(canonical_basis_files, evidence_files)
    runtime_environment = _runtime_environment()

    started_at = _utc_now()
    execution = run_bounded_verification(
        verification["argv"],
        project_root,
        verification["timeout_seconds"],
        verification["max_output_chars"],
    )
    exit_code = execution["exit_code"]
    finished_at = _utc_now()
    result = "pass" if exit_code == 0 else "fail"

    receipt = {
        "schema_version": VERIFICATION_RECEIPT_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "claim": contract["claim"],
        "started_at": started_at,
        "finished_at": finished_at,
        "argv": verification["argv"],
        "exit_code": exit_code,
        "process_returncode": execution["process_returncode"],
        "result": result,
        "stdout": execution["stdout"],
        "stderr": execution["stderr"],
        "timeout": {
            "timeout_seconds": verification["timeout_seconds"],
            "timed_out": execution["timed_out"],
        },
        "output_capture": execution["output_capture"],
        "normalization": execution["normalization"],
        "runtime_environment": runtime_environment,
        "snapshot_sha256": snapshot_digest,
        "canonical_basis_collected_at": inputs_collected_at,
        "canonical_basis_capture": "before_verification",
        "canonical_basis_files": canonical_basis_files,
        "evidence_collected_at": inputs_collected_at,
        "evidence_capture": "before_verification",
        "evidence_files": evidence_files,
    }
    receipt_relative = write_receipt(receipts_relative, receipts_dir, receipt)

    # Receipt 추가가 성공한 뒤에만 status cursor를 교체한다.
    # Status 반영 실패 시에도 이미 추가한 receipt는 증거로 남는다.
    state_status = {
        "schema_version": STATE_STATUS_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "status": (
            "verification_passed" if result == "pass" else "verification_failed"
        ),
        "result": result,
        "receipt": receipt_relative,
        "finished_at": finished_at,
    }
    atomic_write_status(
        status_path,
        json.dumps(state_status, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )

    return exit_code, {
        "workspace_id": identity.workspace_id,
        "claim": contract["claim"],
        "result": result,
        "exit_code": exit_code,
        "receipt": receipt_relative,
        "status": state_status["status"],
        "timed_out": execution["timed_out"],
    }
