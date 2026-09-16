"""Recover가 선택한 Workspace·Project 본문을 정해진 범위와 순서로 읽는다."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..workspace.identity import WorkspaceIdentity
from ..workspace.paths import (
    read_text_without_symlinks,
    resolve_directory_without_symlinks,
)
from ..workspace.status import load_state_status
from ..workspace.validation import fail

REQUIRED_MEMORY_FILES = (
    "spec/01-problem-goal-scope.md",
    "spec/02-behavior-and-cases.md",
    "spec/03-concepts-and-contracts.md",
    "spec/04-quality-and-completion.md",
    "spec/05-constraints-design-assumptions.md",
    "project-context.md",
    "tickets/index.md",
)


def load_memory(
    work_root: Path, identity: WorkspaceIdentity
) -> tuple[dict[str, str], list[dict[str, str]]]:
    """Spec·memory 본문과 Ticket 색인만 읽고 Ticket 본문은 제외한다."""

    directory_relative = f"{identity.workspace_path}/current/memory"
    directory = resolve_directory_without_symlinks(
        work_root, directory_relative, "Workspace memory directory"
    )
    spec_directory = resolve_directory_without_symlinks(
        work_root, f"{directory_relative}/spec", "Workspace Spec directory"
    )
    resolve_directory_without_symlinks(
        work_root, f"{directory_relative}/tickets", "Workspace Ticket directory"
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
        name for name in REQUIRED_MEMORY_FILES if not (directory / name).is_file()
    ]
    if missing_required:
        fail(
            "Workspace memory is missing required files: " + ", ".join(missing_required)
        )

    entries: list[dict[str, str]] = []
    # Spec을 기본 작업 정의로 읽는다. Ticket 본문은 읽는 주체가 색인에서
    # 선택하며, 그 밖의 중첩 memory는 재귀적으로 읽지 않는다.
    candidates = [
        f"spec/{path.name}"
        for path in sorted(spec_directory.iterdir(), key=lambda path: path.name)
        if path.name.endswith(".md")
    ]
    candidates.extend(
        path.name
        for path in sorted(directory.iterdir(), key=lambda path: path.name)
        if path.name != "index.md" and path.name.endswith(".md")
    )
    candidates.append("tickets/index.md")
    for name in candidates:
        relative_path = f"{directory_relative}/{name}"
        entries.append(
            {
                "path": relative_path,
                "path_base": "work_root",
                "content": read_text_without_symlinks(
                    work_root,
                    relative_path,
                    f"Workspace memory context {name}",
                ),
            }
        )
    return memory_index, entries


def load_output_index(work_root: Path, identity: WorkspaceIdentity) -> dict[str, str]:
    """Goal 산출물 지도만 읽고 연결된 산출물 본문은 읽지 않는다."""

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


def load_state(
    work_root: Path, identity: WorkspaceIdentity
) -> tuple[dict[str, str], dict[str, Any]]:
    """사람용 state 색인을 먼저 읽고 machine status 계약을 검사한다."""

    directory_relative = f"{identity.workspace_path}/current/state"
    resolve_directory_without_symlinks(
        work_root, directory_relative, "Workspace state directory"
    )
    index_path = f"{directory_relative}/index.md"
    index = {
        "path": index_path,
        "path_base": "work_root",
        "content": read_text_without_symlinks(
            work_root, index_path, "Workspace state index"
        ),
    }
    return index, load_state_status(work_root, identity)


def load_project_context(
    project_root: Path, selections: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Recover 계약이 검사한 Project 선택만 선언 순서대로 읽는다."""

    return [
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
        for entry in selections
    ]
