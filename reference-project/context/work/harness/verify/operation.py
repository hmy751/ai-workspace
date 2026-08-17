"""Record evidence produced by an existing verification activity."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any
import uuid

from ..workspace_contract import (
    HarnessError,
    WorkspaceIdentity,
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
    resolve_directory_without_symlinks,
    select_workspace,
)


EVIDENCE_SCHEMA_VERSION = 1
EVIDENCE_RECEIPT_TYPE = "recorded_verification_evidence"
EVIDENCE_OUTCOMES = frozenset({"pass", "fail", "partial"})
_INPUT_KEYS = {
    "schema_version",
    "observed_at",
    "producer",
    "subject",
    "method",
    "outcome",
    "result_summary",
    "source_refs",
    "unverified_scope",
}
_SOURCE_REF_KEYS = {"kind", "locator"}
_RFC3339_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
_RECEIPT_ALLOCATION_ATTEMPTS = 8


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _validate_rfc3339(value: Any, label: str) -> str:
    timestamp = expect_nonempty_string(value, label)
    if not _RFC3339_PATTERN.fullmatch(timestamp):
        fail(f"{label} must be an RFC3339 timestamp with a timezone")
    normalized = (
        timestamp[:-1] + "+00:00"
        if timestamp.endswith("Z")
        else timestamp
    )
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise HarnessError(
            f"{label} must be a valid RFC3339 timestamp with a timezone"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        fail(f"{label} must include a timezone")
    return timestamp


def _validate_source_refs(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        fail("evidence source_refs must be a JSON array")
    validated: list[dict[str, str]] = []
    for index, item in enumerate(value):
        label = f"evidence source_refs[{index}]"
        if not isinstance(item, dict):
            fail(f"{label} must be a JSON object")
        expect_exact_keys(item, _SOURCE_REF_KEYS, label)
        validated.append(
            {
                "kind": expect_nonempty_string(item["kind"], f"{label}.kind"),
                "locator": expect_nonempty_string(
                    item["locator"], f"{label}.locator"
                ),
            }
        )
    return validated


def _validate_unverified_scope(value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        fail("evidence unverified_scope must be a non-empty JSON array")
    return [
        expect_nonempty_string(item, f"evidence unverified_scope[{index}]")
        for index, item in enumerate(value)
    ]


def _validate_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        fail("verification evidence payload must be a JSON object")
    expect_exact_keys(payload, _INPUT_KEYS, "verification evidence payload")
    expect_schema_version(
        payload["schema_version"],
        EVIDENCE_SCHEMA_VERSION,
        "verification evidence payload",
    )
    outcome = expect_nonempty_string(payload["outcome"], "evidence outcome")
    if outcome not in EVIDENCE_OUTCOMES:
        fail("evidence outcome must be 'pass', 'fail', or 'partial'")
    return {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "observed_at": _validate_rfc3339(
            payload["observed_at"], "evidence observed_at"
        ),
        "producer": expect_nonempty_string(
            payload["producer"], "evidence producer"
        ),
        "subject": expect_nonempty_string(payload["subject"], "evidence subject"),
        "method": expect_nonempty_string(payload["method"], "evidence method"),
        "outcome": outcome,
        "result_summary": expect_nonempty_string(
            payload["result_summary"], "evidence result_summary"
        ),
        "source_refs": _validate_source_refs(payload["source_refs"]),
        "unverified_scope": _validate_unverified_scope(
            payload["unverified_scope"]
        ),
    }


def _resolve_receipts_directory(
    work_root: Path, identity: WorkspaceIdentity
) -> tuple[str, Path]:
    relative = f"{identity.workspace_path}/records/receipts/verify"
    parent_relative = f"{identity.workspace_path}/records/receipts"
    parent = resolve_directory_without_symlinks(
        work_root,
        parent_relative,
        "Workspace receipts directory",
    )
    directory = parent / "verify"
    try:
        directory_status = directory.lstat()
    except FileNotFoundError:
        try:
            os.mkdir(directory, mode=0o755)
        except FileExistsError as exc:
            raise HarnessError(
                "Workspace verification evidence receipts directory changed "
                "while it was being created"
            ) from exc
        except OSError as exc:
            raise HarnessError(
                "could not create Workspace verification evidence receipts "
                f"directory: {exc}"
            ) from exc
    except OSError as exc:
        raise HarnessError(
            "could not inspect Workspace verification evidence receipts "
            f"directory: {exc}"
        ) from exc
    else:
        if stat.S_ISLNK(directory_status.st_mode):
            fail(
                "Workspace verification evidence receipts directory must not "
                "be a symlink"
            )
        if not stat.S_ISDIR(directory_status.st_mode):
            fail(
                "Workspace verification evidence receipts directory must be "
                f"a directory: {relative}"
            )

    # Sync the parent on every call.  If a previous process created the leaf
    # but failed while syncing this entry, a retry must not silently skip the
    # durability boundary merely because the leaf now exists.
    _fsync_directory(parent)
    directory = resolve_directory_without_symlinks(
        work_root,
        relative,
        "Workspace verification evidence receipts directory",
    )
    return relative, directory


def _receipt_filename() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"evidence-{timestamp}-{uuid.uuid4().hex}.json"


def _fsync_directory(directory: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(directory, flags)
    except OSError as exc:
        raise HarnessError(
            f"could not open verification evidence receipt directory: {exc}"
        ) from exc
    try:
        os.fsync(descriptor)
    except OSError as exc:
        raise HarnessError(
            "could not make the verification evidence directory update "
            f"durable: {exc}"
        ) from exc
    finally:
        os.close(descriptor)


def _write_receipt(
    receipts_relative: str,
    receipts_directory: Path,
    receipt: dict[str, Any],
) -> str:
    content = json.dumps(
        receipt, ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".evidence-receipt-",
            suffix=".tmp",
            dir=receipts_directory,
        )
    except OSError as exc:
        raise HarnessError(
            f"could not create verification evidence receipt: {exc}"
        ) from exc

    temporary_path = Path(temporary_name)
    try:
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        except OSError as exc:
            raise HarnessError(
                f"could not write verification evidence receipt: {exc}"
            ) from exc

        for _ in range(_RECEIPT_ALLOCATION_ATTEMPTS):
            filename = _receipt_filename()
            receipt_path = receipts_directory / filename
            try:
                os.link(temporary_path, receipt_path)
            except FileExistsError:
                continue
            except OSError as exc:
                raise HarnessError(
                    f"could not publish verification evidence receipt: {exc}"
                ) from exc
            _fsync_directory(receipts_directory)
            return f"{receipts_relative}/{filename}"
        fail(
            "could not allocate a unique append-only verification evidence "
            "receipt"
        )
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            # A complete published receipt remains authoritative. A failed cleanup
            # leaves only a dot-prefixed temporary file, never a second receipt.
            pass


def record_evidence(
    work_root: Path,
    payload: dict[str, Any],
    explicit_workspace_id: str | None = None,
) -> dict[str, Any]:
    """Validate and append evidence without running or judging verification."""

    identity = select_workspace(work_root, explicit_workspace_id)
    validated = _validate_payload(payload)
    receipts_relative, receipts_directory = _resolve_receipts_directory(
        work_root, identity
    )
    recorded_at = _utc_now()
    receipt = {
        **validated,
        "receipt_type": EVIDENCE_RECEIPT_TYPE,
        "workspace_id": identity.workspace_id,
        "recorded_at": recorded_at,
    }
    receipt_relative = _write_receipt(
        receipts_relative, receipts_directory, receipt
    )
    return {
        "workspace_id": identity.workspace_id,
        "receipt": receipt_relative,
        "recorded": True,
        "evidence_outcome": validated["outcome"],
    }
