"""파일 변경 전 경로·링크·기존 내용과 precondition을 함께 확인한다."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
import stat
from typing import Any

from ...workspace_contract import (
    HarnessError,
    WorkspaceIdentity,
    fail,
    reject_symlink_components,
    resolve_directory_without_symlinks,
    resolve_regular_file_without_symlinks,
    select_workspace,
)
from .policy import (
    _is_allowed_change_path,
    _validate_markdown_text,
    _validate_local_markdown_links,
    _local_markdown_targets,
)


@dataclass(frozen=True)
class _PreparedChange:
    relative_path: str
    target: Path
    expected_sha256: str | None
    content: bytes
    reason: str
    exists: bool
    current_mode: int | None


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _resolve_project_and_workspace(
    project_root: Path,
    work_root: Path,
    workspace_id: str,
) -> tuple[Path, Path, WorkspaceIdentity]:
    try:
        resolved_project_root = project_root.resolve(strict=True)
        resolved_work_root = work_root.resolve(strict=True)
    except OSError as exc:
        raise HarnessError(f"Maintain root is unavailable: {exc}") from exc
    if not resolved_project_root.is_dir() or not resolved_work_root.is_dir():
        fail("Maintain Project root and Work root must be directories")
    try:
        resolved_work_root.relative_to(resolved_project_root)
    except ValueError as exc:
        raise HarnessError(
            "Maintain Work root must be inside Project root"
        ) from exc
    identity = select_workspace(resolved_work_root, workspace_id)
    workspace_root = resolve_directory_without_symlinks(
        resolved_work_root,
        identity.workspace_path,
        "Maintain Workspace root",
    )
    return resolved_project_root, workspace_root, identity


def _prepare_changes(
    project_root: Path,
    workspace_root: Path,
    changes: list[dict[str, Any]],
) -> list[_PreparedChange]:
    prepared: list[_PreparedChange] = []
    planned_targets = {
        (workspace_root / change["path"]).resolve(strict=False)
        for change in changes
    }

    for index, change in enumerate(changes):
        label = f"Maintain decision changes[{index}]"
        relative_path = change["path"]
        allowed, append_only_record = _is_allowed_change_path(relative_path)
        if not allowed:
            fail(f"{label}.path is outside the Maintain write allowlist")

        parent_relative = PurePosixPath(relative_path).parent.as_posix()
        parent = resolve_directory_without_symlinks(
            workspace_root,
            parent_relative,
            f"{label}.path parent",
        )
        target = parent / PurePosixPath(relative_path).name
        reject_symlink_components(workspace_root, relative_path, f"{label}.path")
        if target.is_symlink():
            fail(f"{label}.path must not use symlink components")
        exists = target.exists()
        if relative_path == "records/README.md" and not exists:
            fail(
                f"{label}.path must identify the existing records entry point"
            )
        expected_sha256 = change["expected_sha256"]
        current_mode: int | None = None
        current_content: bytes | None = None
        if exists:
            target = resolve_regular_file_without_symlinks(
                workspace_root, relative_path, f"{label}.path"
            )
            if append_only_record:
                fail(f"{label}.path identifies an existing append-only record")
            if expected_sha256 is None:
                fail(
                    f"{label}.expected_sha256 is required for an existing "
                    "file"
                )
            try:
                current_content = target.read_bytes()
                current_mode = stat.S_IMODE(target.stat().st_mode)
            except OSError as exc:
                raise HarnessError(f"{label}.path is not readable: {exc}") from exc
            if _sha256(current_content) != expected_sha256:
                fail(f"{label}.path has a stale expected_sha256")
        elif expected_sha256 is not None:
            fail(f"{label}.expected_sha256 must be null for a new file")

        content = _validate_markdown_text(change["content"], f"{label}.content")
        _validate_local_markdown_links(
            project_root,
            target,
            change["content"],
            planned_targets,
            f"{label}.content",
        )
        if current_content == content:
            continue
        prepared.append(
            _PreparedChange(
                relative_path=relative_path,
                target=target,
                expected_sha256=expected_sha256,
                content=content,
                reason=change["reason"],
                exists=exists,
                current_mode=current_mode,
            )
        )

    if not prepared:
        fail("Maintain update must contain at least one material file change")

    new_memory_topics = [
        change
        for change in prepared
        if not change.exists
        and PurePosixPath(change.relative_path).parts[:2]
        == ("current", "memory")
        and change.relative_path != "current/memory/index.md"
    ]
    # Ticket 본문은 ticket 색인에서 찾고, Spec과 다른 memory 주제는
    # memory 진입점에서 직접 연결한다.
    topics_by_index: dict[str, list[_PreparedChange]] = {}
    for change in new_memory_topics:
        parts = PurePosixPath(change.relative_path).parts
        if len(parts) == 4 and parts[2] == "tickets" and parts[3] != "index.md":
            index_path = "current/memory/tickets/index.md"
        else:
            index_path = "current/memory/index.md"
        topics_by_index.setdefault(index_path, []).append(change)
    for index_path, indexed_topics in topics_by_index.items():
        memory_index = next(
            (
                change
                for change in prepared
                if change.relative_path == index_path
            ),
            None,
        )
        if memory_index is None:
            fail(
                "a new Workspace memory topic requires the same decision to "
                f"update {index_path}"
            )
        linked_targets = _local_markdown_targets(
            memory_index.target,
            memory_index.content.decode("utf-8"),
            "Maintain memory index content",
        )
        missing = [
            change.relative_path
            for change in indexed_topics
            if change.target.resolve(strict=False) not in linked_targets
        ]
        if missing:
            fail(
                f"{index_path} must link every new Workspace memory "
                f"topic: {missing}"
            )

    new_records = [
        change
        for change in prepared
        if not change.exists
        and _is_allowed_change_path(change.relative_path)[1]
    ]
    if new_records:
        records_index = next(
            (
                change
                for change in prepared
                if change.relative_path == "records/README.md"
            ),
            None,
        )
        if records_index is None:
            fail(
                "a new dated Workspace record requires the same decision to "
                "update records/README.md"
            )
        linked_targets = _local_markdown_targets(
            records_index.target,
            records_index.content.decode("utf-8"),
            "Maintain records index content",
        )
        missing = [
            change.relative_path
            for change in new_records
            if change.target.resolve(strict=False) not in linked_targets
        ]
        if missing:
            fail(
                "records/README.md must link every new dated Workspace "
                f"record: {missing}"
            )
    return prepared
