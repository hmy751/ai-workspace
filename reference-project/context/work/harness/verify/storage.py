"""Receipt를 덮어쓰지 않고 추가한 뒤 status를 atomic 교체한다."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from typing import Any
import uuid

from ..workspace.identity import WorkspaceIdentity
from ..workspace.paths import resolve_directory_without_symlinks
from ..workspace.validation import fail


def atomic_write_status(path: Path, content: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    except BaseException:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        raise


def resolve_verify_receipts_directory(
    work_root: Path,
    identity: WorkspaceIdentity,
) -> tuple[str, Path]:
    receipts_relative = f"{identity.workspace_path}/records/receipts/verify"
    receipts_dir = resolve_directory_without_symlinks(
        work_root,
        receipts_relative,
        "Workspace verify receipts directory",
    )
    return receipts_relative, receipts_dir


def write_receipt(
    receipts_relative: str,
    receipts_dir: Path,
    receipt: dict[str, Any],
) -> str:
    content = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".verify-receipt-", suffix=".tmp", dir=receipts_dir
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())

        # Hard link로 새 이름만 추가한다. 충돌해도 기존 receipt를 덮지 않는다.
        for _ in range(5):
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            filename = f"verify-{timestamp}-{uuid.uuid4().hex}.json"
            receipt_path = receipts_dir / filename
            try:
                os.link(temporary_path, receipt_path)
            except FileExistsError:
                continue
            return f"{receipts_relative}/{filename}"
        fail("could not allocate a unique append-only verification receipt")
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
