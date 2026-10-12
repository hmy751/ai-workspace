"""경로 검증과 JSON 입출력의 파일 시스템 경계."""

from __future__ import annotations

from collections.abc import Mapping
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from ...workspace_contract import HarnessError, fail


def _hash_identifier(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _reject_existing_symlink_components(path: Path, label: str) -> None:
    if not path.is_absolute():
        fail(f"{label} must be an absolute path")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            fail(f"{label} must not use symlink components")


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    _reject_existing_symlink_components(path, "Maintain runtime write path")
    path.parent.mkdir(parents=True, exist_ok=True)
    _reject_existing_symlink_components(path, "Maintain runtime write path")
    descriptor, raw_temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(raw_temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            descriptor = -1
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)
        raise


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    _reject_existing_symlink_components(path, label)
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise HarnessError(f"{label} is not readable UTF-8 JSON: {exc}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        fail(f"{label} must contain a JSON object")
    return value
