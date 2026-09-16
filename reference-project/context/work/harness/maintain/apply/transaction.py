"""준비한 파일의 stage·최종 precondition·반영을 소유한다."""

from __future__ import annotations

import os
from pathlib import Path
import tempfile

from ...workspace_contract import (
    HarnessError,
    fail,
    reject_symlink_components,
    resolve_regular_file_without_symlinks,
)
from .prepare import _PreparedChange, _sha256


def _stage_change(change: _PreparedChange) -> Path:
    descriptor, raw_path = tempfile.mkstemp(
        prefix=".maintain-",
        suffix=".tmp",
        dir=change.target.parent,
    )
    staged_path = Path(raw_path)
    try:
        if change.current_mode is not None:
            os.fchmod(descriptor, change.current_mode)
        else:
            os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(change.content)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        staged_path.unlink(missing_ok=True)
        raise
    return staged_path


def _precondition_still_holds(
    workspace_root: Path, change: _PreparedChange
) -> None:
    reject_symlink_components(
        workspace_root, change.relative_path, "Maintain write target"
    )
    if change.target.is_symlink():
        fail("Maintain write target must not be a symlink")
    if change.exists:
        target = resolve_regular_file_without_symlinks(
            workspace_root, change.relative_path, "Maintain write target"
        )
        try:
            current = target.read_bytes()
        except OSError as exc:
            raise HarnessError(
                f"Maintain write target is unreadable: {exc}"
            ) from exc
        if _sha256(current) != change.expected_sha256:
            fail(f"Maintain write target became stale: {change.relative_path}")
    elif change.target.exists():
        fail(f"Maintain new write target now exists: {change.relative_path}")


def _commit_prepared_changes(
    workspace_root: Path, prepared: list[_PreparedChange]
) -> list[dict[str, str]]:
    staged: list[tuple[_PreparedChange, Path]] = []
    applied: list[dict[str, str]] = []
    try:
        for change in prepared:
            try:
                staged.append((change, _stage_change(change)))
            except OSError as exc:
                raise HarnessError(
                    "Maintain could not stage the proposed content for "
                    f"{change.relative_path}: {exc}"
                ) from exc
        for change, staged_path in staged:
            try:
                _precondition_still_holds(workspace_root, change)
                if change.exists:
                    os.replace(staged_path, change.target)
                else:
                    os.link(staged_path, change.target)
                    staged_path.unlink()
                if change.target.is_symlink() or not change.target.is_file():
                    fail(
                        "Maintain applied target is not a regular file: "
                        f"{change.relative_path}"
                    )
                if change.target.read_bytes() != change.content:
                    fail(
                        "Maintain applied content does not match the decision: "
                        f"{change.relative_path}"
                    )
                applied.append(
                    {"path": change.relative_path, "reason": change.reason}
                )
            except (OSError, HarnessError) as exc:
                changed = [entry["path"] for entry in applied]
                detail = f"; files already changed: {changed}" if changed else ""
                if isinstance(exc, HarnessError):
                    raise HarnessError(f"{exc}{detail}") from exc
                raise HarnessError(
                    f"Maintain write failed for {change.relative_path}: {exc}{detail}"
                ) from exc
    finally:
        for _, staged_path in staged:
            try:
                staged_path.unlink(missing_ok=True)
            except OSError:
                pass
    return applied
