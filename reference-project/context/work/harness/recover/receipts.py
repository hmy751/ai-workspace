"""연결된 Verify receipt의 인계 정합성과 선언된 파일 최신성을 확인한다."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from ..workspace.identity import WorkspaceIdentity
from ..workspace.paths import (
    read_json_without_symlinks,
    reject_symlink_components,
    resolve_directory_without_symlinks,
    resolve_inside_root,
    validate_relative_path,
)
from ..workspace.status import SUPPORTED_VERIFICATION_RECEIPT_SCHEMA_VERSIONS
from ..workspace.validation import (
    HarnessError,
    expect_exact_keys,
    expect_nonempty_string,
    fail,
)


def _validate_receipt_snapshot_list(
    receipt: dict[str, Any], field: str
) -> list[dict[str, Any]]:
    value = receipt.get(field)
    if not isinstance(value, list) or not value:
        fail(f"verification receipt {field} must be a non-empty JSON array")

    snapshots: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for index, entry in enumerate(value):
        label = f"verification receipt {field}[{index}]"
        if not isinstance(entry, dict):
            fail(f"{label} must be a JSON object")
        expect_exact_keys(entry, {"path", "sha256", "size"}, label)
        path = validate_relative_path(entry["path"], f"{label}.path")
        if path in seen_paths:
            fail(f"duplicate verification receipt {field} path: {path}")
        seen_paths.add(path)
        sha256 = expect_nonempty_string(entry["sha256"], f"{label}.sha256")
        if len(sha256) != 64 or any(
            character not in "0123456789abcdef" for character in sha256
        ):
            fail(f"{label}.sha256 must be a lowercase SHA-256 hex digest")
        size = entry["size"]
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            fail(f"{label}.size must be a nonnegative integer")
        snapshots.append({"path": path, "sha256": sha256, "size": size})
    return snapshots


def _compare_project_file_to_snapshot(
    project_root: Path, snapshot: dict[str, Any], label: str
) -> str:
    """안전 위반은 거부하고 파일의 일치·변경·누락·읽기 불가를 구별한다."""

    relative_path = snapshot["path"]
    reject_symlink_components(project_root, relative_path, label)
    resolved_root = project_root.resolve(strict=True)
    try:
        path = (resolved_root / relative_path).resolve(strict=True)
    except FileNotFoundError:
        return "missing"
    except OSError:
        return "unavailable"
    try:
        path.relative_to(resolved_root)
    except ValueError as exc:
        raise HarnessError(f"{label} resolves outside Project root") from exc
    if not path.is_file():
        return "unavailable"

    digest = hashlib.sha256()
    size = 0
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(chunk)
                digest.update(chunk)
    except OSError:
        return "unavailable"
    if size == snapshot["size"] and digest.hexdigest() == snapshot["sha256"]:
        return "matched"
    return "changed"


def _receipt_freshness(
    project_root: Path, receipt: dict[str, Any]
) -> dict[str, int | str]:
    schema_version = receipt["schema_version"]
    empty_counts = {
        "snapshot_file_count": 0,
        "changed_file_count": 0,
        "missing_file_count": 0,
        "unavailable_file_count": 0,
    }
    if schema_version == 1:
        return {"status": "unknown_legacy", **empty_counts}

    expect_nonempty_string(receipt.get("claim"), "verification receipt claim")
    snapshots_by_field: dict[str, list[dict[str, Any]]] = {}
    snapshots: list[tuple[str, dict[str, Any]]] = []
    for field in ("canonical_basis_files", "evidence_files"):
        validated = _validate_receipt_snapshot_list(receipt, field)
        snapshots_by_field[field] = validated
        snapshots.extend((field, entry) for entry in validated)

    snapshot_sha256 = expect_nonempty_string(
        receipt.get("snapshot_sha256"),
        "verification receipt snapshot_sha256",
    )
    if len(snapshot_sha256) != 64 or any(
        character not in "0123456789abcdef" for character in snapshot_sha256
    ):
        fail(
            "verification receipt snapshot_sha256 must be a lowercase "
            "SHA-256 hex digest"
        )
    serialized_snapshots = json.dumps(
        snapshots_by_field,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    if hashlib.sha256(serialized_snapshots).hexdigest() != snapshot_sha256:
        fail(
            "verification receipt snapshot_sha256 does not match its "
            "declared snapshots"
        )

    counts = {
        "matched": 0,
        "changed": 0,
        "missing": 0,
        "unavailable": 0,
    }
    for index, (field, snapshot) in enumerate(snapshots):
        result = _compare_project_file_to_snapshot(
            project_root,
            snapshot,
            f"verification receipt {field}[{index}].path",
        )
        counts[result] += 1
    stale_count = counts["changed"] + counts["missing"] + counts["unavailable"]
    return {
        "status": "fresh" if stale_count == 0 else "stale",
        "snapshot_file_count": len(snapshots),
        "changed_file_count": counts["changed"],
        "missing_file_count": counts["missing"],
        "unavailable_file_count": counts["unavailable"],
    }


def validate_linked_receipt(
    project_root: Path,
    work_root: Path,
    identity: WorkspaceIdentity,
    status: dict[str, Any],
) -> tuple[str | None, dict[str, int | str]]:
    """연결된 receipt를 검사해 경로와 제한된 최신성 요약을 반환한다."""

    if status["receipt"] is None:
        return None, {
            "status": "not_applicable",
            "snapshot_file_count": 0,
            "changed_file_count": 0,
            "missing_file_count": 0,
            "unavailable_file_count": 0,
        }

    receipt_relative = status["receipt"]
    records_relative = f"{identity.workspace_path}/records"
    records_dir = resolve_directory_without_symlinks(
        work_root, records_relative, "Workspace records directory"
    )
    reject_symlink_components(work_root, receipt_relative, "state status receipt")
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
    receipt_schema_version = receipt["schema_version"]
    if (
        type(receipt_schema_version) is not int
        or receipt_schema_version not in SUPPORTED_VERIFICATION_RECEIPT_SCHEMA_VERSIONS
    ):
        fail(
            "unsupported verification receipt schema_version: "
            f"{receipt_schema_version!r}"
        )
    if receipt["workspace_id"] != identity.workspace_id:
        fail("state status and receipt workspace_id do not match")
    if receipt["result"] != status["result"]:
        fail("state status and receipt result do not match")
    if receipt["finished_at"] != status["finished_at"]:
        fail("state status and receipt finished_at do not match")
    return receipt_relative, _receipt_freshness(project_root, receipt)
