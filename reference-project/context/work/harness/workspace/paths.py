"""선언된 root 안의 상대 경로를 검사하고 symlink 없이 읽는다."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .validation import HarnessError, expect_nonempty_string, fail


def validate_relative_path(value: Any, label: str) -> str:
    raw = expect_nonempty_string(value, label)
    normalized = raw.replace("\\", "/")
    normalized_path = PurePosixPath(normalized)
    parts = normalized_path.parts
    if (
        Path(raw).is_absolute()
        or normalized_path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
    ):
        fail(f"{label} must be relative to its declared path base")
    if ".." in parts:
        fail(f"{label} must not traverse outside its declared path base")
    if not parts or parts in {(".",), ()}:
        fail(f"{label} must identify a file")
    return raw


def resolve_inside_root(
    base_root: Path,
    relative_path: str,
    label: str,
) -> Path:
    safe_relative = validate_relative_path(relative_path, label)
    resolved_root = base_root.resolve(strict=True)
    if not resolved_root.is_dir():
        fail(f"{label} path base must be a directory")
    try:
        candidate = (resolved_root / safe_relative).resolve(strict=True)
    except FileNotFoundError as exc:
        raise HarnessError(f"{label} does not exist: {safe_relative}") from exc
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise HarnessError(f"{label} resolves outside its declared path base") from exc
    return candidate


def reject_symlink_components(base_root: Path, relative_path: str, label: str) -> None:
    safe_relative = validate_relative_path(relative_path, label)
    current = base_root.resolve(strict=True)
    for part in PurePosixPath(safe_relative.replace("\\", "/")).parts:
        current = current / part
        if current.is_symlink():
            fail(f"{label} must not use symlink components")


def resolve_directory_without_symlinks(
    base_root: Path, relative_path: str, label: str
) -> Path:
    reject_symlink_components(base_root, relative_path, label)
    path = resolve_inside_root(base_root, relative_path, label)
    if not path.is_dir():
        fail(f"{label} must be a directory: {relative_path}")
    return path


def resolve_regular_file_without_symlinks(
    base_root: Path, relative_path: str, label: str
) -> Path:
    reject_symlink_components(base_root, relative_path, label)
    path = resolve_inside_root(base_root, relative_path, label)
    if not path.is_file():
        fail(f"{label} must be a regular file: {relative_path}")
    return path


def read_text_without_symlinks(base_root: Path, relative_path: str, label: str) -> str:
    path = resolve_regular_file_without_symlinks(base_root, relative_path, label)
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise HarnessError(f"{label} is not readable UTF-8 text: {exc}") from exc


def _parse_json_object(raw: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        fail(f"{label} must contain a JSON object")
    return value


def read_json_without_symlinks(
    base_root: Path, relative_path: str, label: str
) -> dict[str, Any]:
    return _parse_json_object(
        read_text_without_symlinks(base_root, relative_path, label), label
    )
