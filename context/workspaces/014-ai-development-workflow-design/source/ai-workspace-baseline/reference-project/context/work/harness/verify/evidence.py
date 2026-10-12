"""명령 실행 전에 기준·evidence 파일을 snapshot하고 식별한다."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from ..workspace.paths import resolve_regular_file_without_symlinks
from ..workspace.validation import HarnessError


def snapshot_files(
    project_root: Path,
    relative_paths: list[str],
    field: str,
) -> list[dict[str, Any]]:
    snapshots: list[dict[str, Any]] = []
    for index, relative_path in enumerate(relative_paths):
        path = resolve_regular_file_without_symlinks(
            project_root,
            relative_path,
            f"{field}[{index}]",
        )
        digest = hashlib.sha256()
        size = 0
        try:
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(chunk)
                    digest.update(chunk)
        except OSError as exc:
            raise HarnessError(
                f"could not snapshot {field} file {relative_path}: {exc}"
            ) from exc
        snapshots.append(
            {"path": relative_path, "sha256": digest.hexdigest(), "size": size}
        )
    return snapshots


def snapshot_sha256(
    canonical_basis_files: list[dict[str, Any]],
    evidence_files: list[dict[str, Any]],
) -> str:
    serialized = json.dumps(
        {
            "canonical_basis_files": canonical_basis_files,
            "evidence_files": evidence_files,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()
