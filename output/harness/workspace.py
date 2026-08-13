#!/usr/bin/env python3
"""Recover and verify one bounded Workspace inside this Project.

The harness deliberately uses only the Python standard library.  A Workspace
manifest chooses the small set of Project context files needed for the current
task and owns one fixed verification argv.  Verification receipts are
append-only; ``current/state/status.json`` is the mutable machine cursor used
on the next re-entry while ``current/state/index.md`` remains human-owned.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import signal
import subprocess
import sys
import tempfile
import threading
from typing import Any, NoReturn
import uuid


SCHEMA_VERSION = 1
RECOVERY_SCHEMA_VERSION = 2
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_TIMEOUT_SECONDS = 300.0
DEFAULT_MAX_OUTPUT_CHARS = 100_000
MAX_OUTPUT_CHARS = 1_000_000
TIMEOUT_EXIT_CODE = 124
OUTPUT_ROOT_TOKEN = "<OUTPUT_ROOT>"
WORKSPACE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
VALID_STATE_STATUSES = {
    "ready_for_verification",
    "verification_failed",
    "verified_waiting_acceptance",
}
DISALLOWED_COMMANDS = {
    "bash",
    "csh",
    "dash",
    "env",
    "fish",
    "ksh",
    "powershell",
    "pwsh",
    "sh",
    "tcsh",
    "zsh",
}


class HarnessError(ValueError):
    """Raised when a Workspace contract is invalid or unsafe."""


def _fail(message: str) -> NoReturn:
    raise HarnessError(message)


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _expect_exact_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        details = []
        if missing:
            details.append(f"missing={missing}")
        if extra:
            details.append(f"extra={extra}")
        _fail(f"invalid {label} keys: {', '.join(details)}")


def _expect_bounded_keys(
    value: dict[str, Any], required: set[str], allowed: set[str], label: str
) -> None:
    actual = set(value)
    missing = sorted(required - actual)
    extra = sorted(actual - allowed)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing={missing}")
        if extra:
            details.append(f"extra={extra}")
        _fail(f"invalid {label} keys: {', '.join(details)}")


def _expect_schema_version(value: Any, label: str) -> None:
    if type(value) is not int or value != SCHEMA_VERSION:
        _fail(f"unsupported {label} schema_version: {value!r}")


def _expect_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"{label} must be a non-empty string")
    if "\x00" in value:
        _fail(f"{label} must not contain NUL")
    return value


def _validate_workspace_id(value: Any) -> str:
    workspace_id = _expect_nonempty_string(value, "workspace id")
    if not WORKSPACE_ID_PATTERN.fullmatch(workspace_id):
        _fail(
            "workspace id must contain only lowercase letters, digits, '.', "
            "'_' or '-', and must start with a letter or digit"
        )
    if workspace_id in {".", ".."}:
        _fail("workspace id must not be '.' or '..'")
    return workspace_id


def _validate_relative_path(value: Any, label: str) -> str:
    raw = _expect_nonempty_string(value, label)
    path = Path(raw)
    normalized = raw.replace("\\", "/")
    normalized_parts = PurePosixPath(normalized).parts
    if (
        path.is_absolute()
        or PurePosixPath(normalized).is_absolute()
        or PureWindowsPath(raw).is_absolute()
    ):
        _fail(f"{label} must be relative to the output root")
    if ".." in normalized_parts:
        _fail(f"{label} must not traverse outside the output root")
    if not normalized_parts or normalized_parts in {(".",), ()}:
        _fail(f"{label} must identify a file")
    return raw


def _resolve_inside_root(
    root: Path, relative_path: str, label: str, *, must_exist: bool = True
) -> Path:
    safe_relative = _validate_relative_path(relative_path, label)
    root = root.resolve(strict=True)
    try:
        candidate = (root / safe_relative).resolve(strict=must_exist)
    except FileNotFoundError as exc:
        raise HarnessError(f"{label} does not exist: {safe_relative}") from exc
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise HarnessError(f"{label} resolves outside the output root") from exc
    return candidate


def _read_text_inside_root(root: Path, relative_path: str, label: str) -> str:
    path = _resolve_inside_root(root, relative_path, label)
    if not path.is_file():
        _fail(f"{label} must be a regular file: {relative_path}")
    return path.read_text(encoding="utf-8")


def _read_json_inside_root(
    root: Path, relative_path: str, label: str
) -> dict[str, Any]:
    raw = _read_text_inside_root(root, relative_path, label)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        _fail(f"{label} must contain a JSON object")
    return value


def _load_index(root: Path) -> dict[str, Any]:
    index = _read_json_inside_root(
        root, "workspaces/index.json", "Workspace index"
    )
    _expect_exact_keys(
        index, {"schema_version", "active_workspace_id"}, "Workspace index"
    )
    _expect_schema_version(index["schema_version"], "Workspace index")
    index["active_workspace_id"] = _validate_workspace_id(
        index["active_workspace_id"]
    )
    return index


def _validate_argv(value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        _fail("verification.argv must be a non-empty JSON array, not a shell string")
    argv: list[str] = []
    for index, item in enumerate(value):
        argument = _expect_nonempty_string(item, f"verification.argv[{index}]")
        candidates = [argument]
        if "=" in argument:
            candidates.append(argument.split("=", 1)[1])
        for candidate in candidates:
            normalized = candidate.replace("\\", "/")
            normalized_parts = PurePosixPath(normalized).parts
            if (
                Path(candidate).is_absolute()
                or PurePosixPath(normalized).is_absolute()
                or PureWindowsPath(candidate).is_absolute()
            ):
                _fail(f"verification.argv[{index}] must not be an absolute path")
            if ".." in normalized_parts:
                _fail(
                    f"verification.argv[{index}] must not contain path traversal"
                )
        argv.append(argument)
    executable = Path(argv[0]).name.lower()
    if executable in DISALLOWED_COMMANDS:
        _fail("verification.argv must not invoke a shell or env trampoline")
    return argv


def _load_manifest(root: Path, workspace_id: str) -> dict[str, Any]:
    manifest_path = f"workspaces/{workspace_id}/workspace.json"
    manifest = _read_json_inside_root(root, manifest_path, "Workspace manifest")
    _expect_exact_keys(
        manifest,
        {
            "schema_version",
            "workspace_id",
            "project_context",
            "verification",
            "next_actions",
        },
        "Workspace manifest",
    )
    _expect_schema_version(manifest["schema_version"], "Workspace manifest")
    manifest_workspace_id = _validate_workspace_id(manifest["workspace_id"])
    if manifest_workspace_id != workspace_id:
        _fail("Workspace manifest id does not match the selected workspace")

    project_context = manifest["project_context"]
    if not isinstance(project_context, list) or not project_context:
        _fail("project_context must be a non-empty JSON array")
    validated_context = []
    seen_context_paths: set[str] = set()
    for index, entry in enumerate(project_context):
        if not isinstance(entry, dict):
            _fail(f"project_context[{index}] must be a JSON object")
        _expect_exact_keys(entry, {"path", "reason"}, f"project_context[{index}]")
        path = _validate_relative_path(
            entry["path"], f"project_context[{index}].path"
        )
        first_part = PurePosixPath(path.replace("\\", "/")).parts[0]
        if first_part != "docs":
            _fail("Project context path must be selected from docs/")
        if path in seen_context_paths:
            _fail(f"duplicate Project context path: {path}")
        seen_context_paths.add(path)
        resolved_context = _resolve_inside_root(
            root, path, f"project_context[{index}].path"
        )
        docs_root = _resolve_inside_root(root, "docs", "Project docs directory")
        if not docs_root.is_dir():
            _fail("Project docs path must be a directory")
        try:
            resolved_context.relative_to(docs_root)
        except ValueError as exc:
            raise HarnessError(
                "Project context path must resolve inside docs/"
            ) from exc
        if not resolved_context.is_file():
            _fail(f"Project context path must be a regular file: {path}")
        reason = _expect_nonempty_string(
            entry["reason"], f"project_context[{index}].reason"
        )
        validated_context.append({"path": path, "reason": reason})

    verification = manifest["verification"]
    if not isinstance(verification, dict):
        _fail("verification must be a JSON object")
    _expect_bounded_keys(
        verification,
        {"argv", "evidence_paths"},
        {"argv", "evidence_paths", "timeout_seconds", "max_output_chars"},
        "verification",
    )
    argv = _validate_argv(verification["argv"])
    timeout_seconds = verification.get(
        "timeout_seconds", DEFAULT_TIMEOUT_SECONDS
    )
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
        or timeout_seconds > MAX_TIMEOUT_SECONDS
    ):
        _fail(
            "verification.timeout_seconds must be a finite number greater "
            f"than zero and at most {MAX_TIMEOUT_SECONDS:g}"
        )
    timeout_seconds = float(timeout_seconds)
    max_output_chars = verification.get(
        "max_output_chars", DEFAULT_MAX_OUTPUT_CHARS
    )
    if (
        isinstance(max_output_chars, bool)
        or not isinstance(max_output_chars, int)
        or max_output_chars <= 0
        or max_output_chars > MAX_OUTPUT_CHARS
    ):
        _fail(
            "verification.max_output_chars must be an integer greater than "
            f"zero and at most {MAX_OUTPUT_CHARS}"
        )
    evidence_paths = verification["evidence_paths"]
    if not isinstance(evidence_paths, list) or not evidence_paths:
        _fail("verification.evidence_paths must be a non-empty JSON array")
    validated_evidence_paths: list[str] = []
    seen_evidence_paths: set[str] = set()
    for index, value in enumerate(evidence_paths):
        path = _validate_relative_path(
            value, f"verification.evidence_paths[{index}]"
        )
        if path in seen_evidence_paths:
            _fail(f"duplicate evidence path: {path}")
        seen_evidence_paths.add(path)
        resolved = _resolve_inside_root(
            root, path, f"verification.evidence_paths[{index}]"
        )
        if not resolved.is_file():
            _fail(f"evidence path must be a regular file: {path}")
        validated_evidence_paths.append(path)

    next_actions = manifest["next_actions"]
    if not isinstance(next_actions, dict):
        _fail("next_actions must be a JSON object")
    _expect_exact_keys(next_actions, {"pass", "fail"}, "next_actions")
    validated_next_actions = {
        outcome: _expect_nonempty_string(
            next_actions[outcome], f"next_actions.{outcome}"
        )
        for outcome in ("pass", "fail")
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "workspace_id": workspace_id,
        "project_context": validated_context,
        "verification": {
            "argv": argv,
            "evidence_paths": validated_evidence_paths,
            "timeout_seconds": timeout_seconds,
            "max_output_chars": max_output_chars,
        },
        "next_actions": validated_next_actions,
    }


def _validate_state_status(
    status: dict[str, Any], workspace_id: str
) -> dict[str, Any]:
    _expect_exact_keys(
        status,
        {
            "schema_version",
            "workspace_id",
            "status",
            "result",
            "receipt",
            "finished_at",
            "next_action",
        },
        "Workspace state status",
    )
    _expect_schema_version(status["schema_version"], "Workspace state status")
    if _validate_workspace_id(status["workspace_id"]) != workspace_id:
        _fail("state status workspace_id does not match the selected workspace")
    if (
        not isinstance(status["status"], str)
        or status["status"] not in VALID_STATE_STATUSES
    ):
        _fail(f"invalid Workspace state status: {status['status']!r}")
    if status["result"] is not None and (
        not isinstance(status["result"], str)
        or status["result"] not in {"pass", "fail"}
    ):
        _fail("state status result must be null, 'pass', or 'fail'")
    for field in ("receipt", "finished_at"):
        if status[field] is not None and not isinstance(status[field], str):
            _fail(f"state status {field} must be a string or null")
    _expect_nonempty_string(status["next_action"], "state status next_action")
    expected_result = {
        "ready_for_verification": None,
        "verification_failed": "fail",
        "verified_waiting_acceptance": "pass",
    }[status["status"]]
    if status["result"] != expected_result:
        _fail("state status and result are inconsistent")
    if status["status"] == "ready_for_verification":
        if any(
            status[field] is not None
            for field in ("receipt", "finished_at")
        ):
            _fail("ready_for_verification status must not have a receipt or time")
    else:
        receipt = _expect_nonempty_string(status["receipt"], "state status receipt")
        _expect_nonempty_string(
            status["finished_at"], "state status finished_at"
        )
        receipt = _validate_relative_path(receipt, "state status receipt")
        expected_prefix = f"workspaces/{workspace_id}/records/"
        if not receipt.startswith(expected_prefix) or not receipt.endswith(".json"):
            _fail("state status receipt must identify this Workspace's JSON record")
    return status


def _reject_symlink_components(
    root: Path, relative_path: str, label: str
) -> None:
    safe_relative = _validate_relative_path(relative_path, label)
    current = root.resolve(strict=True)
    for part in PurePosixPath(safe_relative.replace("\\", "/")).parts:
        current = current / part
        if current.is_symlink():
            _fail(f"{label} must not use symlink components")


def _resolve_directory_without_symlinks(
    root: Path, relative_path: str, label: str
) -> Path:
    _reject_symlink_components(root, relative_path, label)
    path = _resolve_inside_root(root, relative_path, label)
    if not path.is_dir():
        _fail(f"{label} must be a directory: {relative_path}")
    return path


def _resolve_regular_file_without_symlinks(
    root: Path, relative_path: str, label: str
) -> Path:
    _reject_symlink_components(root, relative_path, label)
    path = _resolve_inside_root(root, relative_path, label)
    if not path.is_file():
        _fail(f"{label} must be a regular file: {relative_path}")
    return path


def _read_text_without_symlinks(
    root: Path, relative_path: str, label: str
) -> str:
    path = _resolve_regular_file_without_symlinks(root, relative_path, label)
    return path.read_text(encoding="utf-8")


def _read_json_without_symlinks(
    root: Path, relative_path: str, label: str
) -> dict[str, Any]:
    raw = _read_text_without_symlinks(root, relative_path, label)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HarnessError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        _fail(f"{label} must contain a JSON object")
    return value


def _load_state_status(root: Path, workspace_id: str) -> dict[str, Any]:
    status_relative = f"workspaces/{workspace_id}/current/state/status.json"
    status = _read_json_without_symlinks(
        root, status_relative, "Workspace state status"
    )
    return _validate_state_status(status, workspace_id)


def _validate_state_receipt(
    root: Path, workspace_id: str, status: dict[str, Any]
) -> str | None:
    """Validate the receipt referenced by state without returning its body."""

    if status["receipt"] is None:
        return None

    receipt_relative = status["receipt"]
    records_relative = f"workspaces/{workspace_id}/records"
    _reject_symlink_components(root, records_relative, "Workspace records path")
    records_dir = _resolve_inside_root(
        root, records_relative, "Workspace records path"
    )
    if not records_dir.is_dir():
        _fail("Workspace records path must be a directory")

    _reject_symlink_components(root, receipt_relative, "state status receipt")
    receipt_path = _resolve_inside_root(
        root, receipt_relative, "state status receipt"
    )
    try:
        receipt_path.relative_to(records_dir)
    except ValueError as exc:
        raise HarnessError(
            "state status receipt must resolve inside this Workspace's records/"
        ) from exc
    if not receipt_path.is_file():
        _fail("state status receipt must be a regular file")

    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise HarnessError(
            f"state status receipt is not readable JSON: {exc}"
        ) from exc
    if not isinstance(receipt, dict):
        _fail("state status receipt must contain a JSON object")
    for field in ("schema_version", "workspace_id", "result", "finished_at"):
        if field not in receipt:
            _fail(f"state status receipt is missing {field}")
    _expect_schema_version(receipt["schema_version"], "verification receipt")
    if receipt["workspace_id"] != workspace_id:
        _fail("state status and receipt workspace_id do not match")
    if receipt["result"] != status["result"]:
        _fail("state status and receipt result do not match")
    if receipt["finished_at"] != status["finished_at"]:
        _fail("state status and receipt finished_at do not match")
    return receipt_relative


def _select_workspace_id(root: Path, explicit_id: str | None) -> str:
    index = _load_index(root)
    if explicit_id is None:
        return index["active_workspace_id"]
    return _validate_workspace_id(explicit_id)


def _load_memory_context(
    root: Path, workspace_id: str
) -> tuple[str, str, list[dict[str, str]]]:
    memory_directory_relative = f"workspaces/{workspace_id}/current/memory"
    memory_directory = _resolve_directory_without_symlinks(
        root, memory_directory_relative, "Workspace memory directory"
    )
    memory_index_path = f"{memory_directory_relative}/index.md"
    memory_index = _read_text_without_symlinks(
        root, memory_index_path, "Workspace memory index"
    )

    memory_context: list[dict[str, str]] = []
    for candidate in sorted(
        memory_directory.iterdir(), key=lambda path: path.name
    ):
        if candidate.name == "index.md" or not candidate.name.endswith(".md"):
            continue
        relative_path = f"{memory_directory_relative}/{candidate.name}"
        content = _read_text_without_symlinks(
            root, relative_path, f"Workspace memory context {candidate.name}"
        )
        memory_context.append({"path": relative_path, "content": content})
    return memory_index_path, memory_index, memory_context


def recover(root: Path, explicit_id: str | None) -> dict[str, Any]:
    """Build a bounded recovery packet for one Workspace."""

    workspace_id = _select_workspace_id(root, explicit_id)
    manifest = _load_manifest(root, workspace_id)
    memory_index_path, memory_index, memory_context = _load_memory_context(
        root, workspace_id
    )
    state_directory_relative = f"workspaces/{workspace_id}/current/state"
    _resolve_directory_without_symlinks(
        root, state_directory_relative, "Workspace state directory"
    )
    state_index_path = f"{state_directory_relative}/index.md"
    state_status_path = f"{state_directory_relative}/status.json"
    state_index = _read_text_without_symlinks(
        root, state_index_path, "Workspace state index"
    )
    state_status = _load_state_status(root, workspace_id)
    receipt_control_path = _validate_state_receipt(
        root, workspace_id, state_status
    )

    selected_context = []
    loaded_paths = [memory_index_path]
    loaded_paths.extend(entry["path"] for entry in memory_context)
    loaded_paths.extend([state_index_path, state_status_path])
    for entry in manifest["project_context"]:
        content = _read_text_inside_root(
            root, entry["path"], f"selected Project context {entry['path']}"
        )
        selected_context.append(
            {
                "path": entry["path"],
                "reason": entry["reason"],
                "content": content,
            }
        )
        loaded_paths.append(entry["path"])

    control_paths = [
        "workspaces/index.json",
        f"workspaces/{workspace_id}/workspace.json",
    ]
    if receipt_control_path is not None:
        control_paths.append(receipt_control_path)

    return {
        "schema_version": RECOVERY_SCHEMA_VERSION,
        "workspace_id": workspace_id,
        "manifest_path": f"workspaces/{workspace_id}/workspace.json",
        "control_paths": control_paths,
        "loaded_context_paths": loaded_paths,
        "memory_index": memory_index,
        "memory_context": memory_context,
        "state_index": state_index,
        "state_status": state_status,
        "project_context": selected_context,
        "verification": manifest["verification"],
    }


def _format_recovery_packet(packet: dict[str, Any]) -> str:
    lines = [
        f"# Workspace recovery: {packet['workspace_id']}",
        "",
        f"Manifest: {packet['manifest_path']}",
        "Control paths read to select the Workspace and context:",
    ]
    lines.extend(f"- {path}" for path in packet["control_paths"])
    lines.extend([
        "",
        "Loaded context paths (in recovery order):",
    ])
    lines.extend(f"- {path}" for path in packet["loaded_context_paths"])
    lines.extend(["", "## memory/index.md", "", packet["memory_index"].rstrip()])
    for entry in packet["memory_context"]:
        lines.extend(
            [
                "",
                f"## Memory context: {entry['path']}",
                "",
                entry["content"].rstrip(),
            ]
        )
    lines.extend(["", "## state/index.md", "", packet["state_index"].rstrip()])
    lines.extend(["", "## state/status.json", ""])
    for field in ("status", "result", "finished_at", "receipt", "next_action"):
        value = packet["state_status"][field]
        rendered = "null" if value is None else str(value)
        lines.append(f"- {field}: {rendered}")
    for entry in packet["project_context"]:
        lines.extend(
            [
                "",
                f"## Project context: {entry['path']}",
                "",
                f"Selection reason: {entry['reason']}",
                "",
                entry["content"].rstrip(),
            ]
        )
    lines.extend(
        [
            "",
            "## Fixed verification argv",
            "",
            json.dumps(packet["verification"]["argv"], ensure_ascii=False),
        ]
    )
    return "\n".join(lines) + "\n"


def _hash_evidence(root: Path, evidence_paths: list[str]) -> list[dict[str, Any]]:
    evidence = []
    for index, relative_path in enumerate(evidence_paths):
        path = _resolve_inside_root(
            root, relative_path, f"verification.evidence_paths[{index}]"
        )
        if not path.is_file():
            _fail(f"evidence path must be a regular file: {relative_path}")
        digest = hashlib.sha256()
        size = 0
        try:
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(chunk)
                    digest.update(chunk)
        except OSError as exc:
            raise HarnessError(
                f"could not snapshot evidence file {relative_path}: {exc}"
            ) from exc
        evidence.append(
            {
                "path": relative_path,
                "sha256": digest.hexdigest(),
                "size": size,
            }
        )
    return evidence


class _BoundedStreamCapture:
    """Drain, normalize, and retain only a bounded text prefix."""

    def __init__(self, max_chars: int, output_root_prefix: str) -> None:
        self.max_chars = max_chars
        self.output_root_prefix = output_root_prefix
        self.observed_chars = 0
        self.normalized_chars = 0
        self.stored_chars = 0
        self.root_replacements = 0
        self.parts: list[str] = []
        self.pending = ""
        self.read_error: str | None = None

    def _emit(self, text: str) -> None:
        self.normalized_chars += len(text)
        remaining = self.max_chars - self.stored_chars
        if remaining > 0:
            kept = text[:remaining]
            self.parts.append(kept)
            self.stored_chars += len(kept)

    def add(self, text: str) -> None:
        self.observed_chars += len(text)
        data = self.pending + text
        safe_start_limit = max(
            0, len(data) - len(self.output_root_prefix) + 1
        )
        cursor = 0
        while cursor < safe_start_limit:
            match = data.find(self.output_root_prefix, cursor)
            if match == -1 or match >= safe_start_limit:
                self._emit(data[cursor:safe_start_limit])
                cursor = safe_start_limit
                break
            self._emit(data[cursor:match])
            self._emit(OUTPUT_ROOT_TOKEN)
            self.root_replacements += 1
            cursor = match + len(self.output_root_prefix)
        self.pending = data[cursor:]

    def finish(self) -> None:
        if not self.pending:
            return
        self.root_replacements += self.pending.count(self.output_root_prefix)
        self._emit(
            self.pending.replace(self.output_root_prefix, OUTPUT_ROOT_TOKEN)
        )
        self.pending = ""

    def drain(self, stream: Any) -> None:
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                self.add(chunk)
        except (OSError, ValueError) as exc:
            self.read_error = str(exc)
        finally:
            self.finish()
            try:
                stream.close()
            except (OSError, ValueError):
                pass

    def prefix(self) -> str:
        return "".join(self.parts)


def _capture_result(
    capture: _BoundedStreamCapture,
) -> tuple[str, dict[str, Any], int]:
    persisted = capture.prefix()
    metadata = {
        "observed_chars": capture.observed_chars,
        "persisted_chars": len(persisted),
        "truncated": capture.normalized_chars > capture.max_chars,
        "read_error": (
            capture.read_error.replace(
                capture.output_root_prefix, OUTPUT_ROOT_TOKEN
            )
            if capture.read_error is not None
            else None
        ),
    }
    return persisted, metadata, capture.root_replacements


def _kill_timed_out_process(process: subprocess.Popen[str]) -> None:
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except ProcessLookupError:
        pass
    process.wait()


def _run_bounded_verification(
    argv: list[str],
    root: Path,
    timeout_seconds: float,
    max_output_chars: int,
) -> dict[str, Any]:
    output_root_prefix = str(root.resolve(strict=True))
    stdout_capture = _BoundedStreamCapture(
        max_output_chars, output_root_prefix
    )
    stderr_capture = _BoundedStreamCapture(
        max_output_chars, output_root_prefix
    )
    timed_out = False
    process_returncode: int | None = None

    try:
        process = subprocess.Popen(
            argv,
            cwd=root,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=(os.name == "posix"),
        )
    except OSError as exc:
        exit_code = 127
        stderr_capture.add(f"could not execute verification argv: {exc}\n")
        stderr_capture.finish()
    else:
        if process.stdout is None or process.stderr is None:
            _fail("verification process did not expose stdout and stderr pipes")
        stdout_thread = threading.Thread(
            target=stdout_capture.drain, args=(process.stdout,), daemon=True
        )
        stderr_thread = threading.Thread(
            target=stderr_capture.drain, args=(process.stderr,), daemon=True
        )
        stdout_thread.start()
        stderr_thread.start()
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill_timed_out_process(process)
        process_returncode = process.returncode
        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)
        if stdout_thread.is_alive():
            stdout_capture.read_error = "stdout pipe did not close after process exit"
        if stderr_thread.is_alive():
            stderr_capture.read_error = "stderr pipe did not close after process exit"
        exit_code = TIMEOUT_EXIT_CODE if timed_out else process.returncode

    stdout, stdout_metadata, stdout_replacements = _capture_result(
        stdout_capture
    )
    stderr, stderr_metadata, stderr_replacements = _capture_result(
        stderr_capture
    )
    return {
        "exit_code": exit_code,
        "process_returncode": process_returncode,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "output_capture": {
            "encoding": "utf-8",
            "errors": "replace",
            "limit_unit": "characters",
            "max_chars_per_stream": max_output_chars,
            "stdout": stdout_metadata,
            "stderr": stderr_metadata,
        },
        "normalization": {
            "output_root_token": OUTPUT_ROOT_TOKEN,
            "stdout_replacements": stdout_replacements,
            "stderr_replacements": stderr_replacements,
        },
    }


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=False, exist_ok=True)
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


def _write_receipt(
    root: Path, workspace_id: str, receipt: dict[str, Any]
) -> str:
    records_relative = f"workspaces/{workspace_id}/records"
    _reject_symlink_components(root, records_relative, "Workspace records path")
    records_dir = _resolve_inside_root(
        root, records_relative, "Workspace records directory"
    )
    if not records_dir.is_dir():
        _fail("Workspace records path must be a directory")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    filename = f"verify-{timestamp}-{uuid.uuid4().hex}.json"
    receipt_path = records_dir / filename
    _atomic_write(
        receipt_path,
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    return f"{records_relative}/{filename}"


def verify(root: Path, explicit_id: str | None) -> int:
    """Run a Workspace's fixed verification and persist its result."""

    workspace_id = _select_workspace_id(root, explicit_id)
    manifest = _load_manifest(root, workspace_id)
    state_directory_relative = f"workspaces/{workspace_id}/current/state"
    _resolve_directory_without_symlinks(
        root, state_directory_relative, "Workspace state directory"
    )
    state_status_relative = f"{state_directory_relative}/status.json"
    state_status_path = _resolve_regular_file_without_symlinks(
        root, state_status_relative, "Workspace state status"
    )
    _load_state_status(root, workspace_id)

    argv = manifest["verification"]["argv"]
    evidence_collected_at = _utc_now()
    evidence_files = _hash_evidence(
        root, manifest["verification"]["evidence_paths"]
    )
    started_at = _utc_now()
    execution = _run_bounded_verification(
        argv,
        root,
        manifest["verification"]["timeout_seconds"],
        manifest["verification"]["max_output_chars"],
    )
    exit_code = execution["exit_code"]
    finished_at = _utc_now()
    result = "pass" if exit_code == 0 else "fail"
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "workspace_id": workspace_id,
        "started_at": started_at,
        "finished_at": finished_at,
        "argv": argv,
        "exit_code": exit_code,
        "process_returncode": execution["process_returncode"],
        "result": result,
        "stdout": execution["stdout"],
        "stderr": execution["stderr"],
        "timeout": {
            "timeout_seconds": manifest["verification"]["timeout_seconds"],
            "timed_out": execution["timed_out"],
        },
        "output_capture": execution["output_capture"],
        "normalization": execution["normalization"],
        "evidence_collected_at": evidence_collected_at,
        "evidence_capture": "before_verification",
        "evidence_files": evidence_files,
    }
    receipt_relative = _write_receipt(root, workspace_id, receipt)

    state_status = {
        "schema_version": SCHEMA_VERSION,
        "workspace_id": workspace_id,
        "status": (
            "verified_waiting_acceptance"
            if result == "pass"
            else "verification_failed"
        ),
        "result": result,
        "receipt": receipt_relative,
        "finished_at": finished_at,
        "next_action": manifest["next_actions"][result],
    }
    _atomic_write(
        state_status_path,
        json.dumps(state_status, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
    )

    summary = {
        "workspace_id": workspace_id,
        "result": result,
        "exit_code": exit_code,
        "receipt": receipt_relative,
        "status": state_status["status"],
        "timed_out": execution["timed_out"],
        "next_action": state_status["next_action"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return exit_code


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recover or verify a bounded Project Workspace"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    recover_parser = subparsers.add_parser(
        "recover", help="print the active Workspace recovery packet"
    )
    recover_parser.add_argument("workspace_id", nargs="?")
    recover_parser.add_argument(
        "--json", action="store_true", dest="as_json", help="emit JSON"
    )

    verify_parser = subparsers.add_parser(
        "verify", help="run the Workspace's fixed verification argv"
    )
    verify_parser.add_argument("workspace_id", nargs="?")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    arguments = parser.parse_args(argv)
    output_root = Path(__file__).resolve().parent.parent
    try:
        if arguments.command == "recover":
            packet = recover(output_root, arguments.workspace_id)
            if arguments.as_json:
                print(json.dumps(packet, ensure_ascii=False, indent=2))
            else:
                print(_format_recovery_packet(packet), end="")
            return 0
        return verify(output_root, arguments.workspace_id)
    except HarnessError as exc:
        print(f"workspace harness error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
