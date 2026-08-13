"""Run bounded verification and persist receipt/status handoff artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import signal
import subprocess
import tempfile
import threading
from typing import Any
import uuid

from ..workspace_contract import (
    HarnessError,
    STATE_STATUS_SCHEMA_VERSION,
    VERIFICATION_RECEIPT_SCHEMA_VERSION,
    WorkspaceIdentity,
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
    load_state_status,
    read_json_without_symlinks,
    reject_symlink_components,
    resolve_directory_without_symlinks,
    resolve_regular_file_without_symlinks,
    select_workspace,
    state_status_path,
    validate_relative_path,
    validate_workspace_id,
)


VERIFY_CONTRACT_SCHEMA_VERSION = 1
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_TIMEOUT_SECONDS = 300.0
DEFAULT_MAX_OUTPUT_CHARS = 100_000
MAX_OUTPUT_CHARS = 1_000_000
TIMEOUT_EXIT_CODE = 124
# Serialized receipt compatibility: this token has always represented the
# Project root used as the verification cwd, which remains the same directory.
PROJECT_ROOT_TOKEN = "<OUTPUT_ROOT>"
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


def _expect_verification_keys(value: dict[str, Any]) -> None:
    required = {"argv", "evidence_paths"}
    allowed = required | {"timeout_seconds", "max_output_chars"}
    actual = set(value)
    missing = sorted(required - actual)
    extra = sorted(actual - allowed)
    if not missing and not extra:
        return
    details = []
    if missing:
        details.append(f"missing={missing}")
    if extra:
        details.append(f"extra={extra}")
    fail(f"invalid verification keys: {', '.join(details)}")


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _verify_contract_path(identity: WorkspaceIdentity) -> str:
    return f"{identity.workspace_path}/verify.json"


def _validate_argv(value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        fail("verification.argv must be a non-empty JSON array, not a shell string")
    argv: list[str] = []
    for index, item in enumerate(value):
        argument = expect_nonempty_string(item, f"verification.argv[{index}]")
        candidates = [argument]
        if "=" in argument:
            candidates.append(argument.split("=", 1)[1])
        for candidate in candidates:
            normalized = candidate.replace("\\", "/")
            normalized_path = PurePosixPath(normalized)
            if (
                Path(candidate).is_absolute()
                or normalized_path.is_absolute()
                or PureWindowsPath(candidate).is_absolute()
            ):
                fail(f"verification.argv[{index}] must not be an absolute path")
            if ".." in normalized_path.parts:
                fail(f"verification.argv[{index}] must not contain path traversal")
        argv.append(argument)
    if Path(argv[0]).name.lower() in DISALLOWED_COMMANDS:
        fail("verification.argv must not invoke a shell or env trampoline")
    return argv


def _load_verify_contract(
    project_root: Path,
    work_root: Path,
    identity: WorkspaceIdentity,
) -> dict[str, Any]:
    contract = read_json_without_symlinks(
        work_root,
        _verify_contract_path(identity),
        "Workspace verify contract",
    )
    expect_exact_keys(
        contract,
        {"schema_version", "workspace_id", "verification", "next_actions"},
        "Workspace verify contract",
    )
    expect_schema_version(
        contract["schema_version"],
        VERIFY_CONTRACT_SCHEMA_VERSION,
        "Workspace verify contract",
    )
    if validate_workspace_id(contract["workspace_id"]) != identity.workspace_id:
        fail("verify contract workspace_id does not match the selected workspace")

    verification = contract["verification"]
    if not isinstance(verification, dict):
        fail("verification must be a JSON object")
    _expect_verification_keys(verification)
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
        fail(
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
        fail(
            "verification.max_output_chars must be an integer greater than "
            f"zero and at most {MAX_OUTPUT_CHARS}"
        )

    evidence_paths = verification["evidence_paths"]
    if not isinstance(evidence_paths, list) or not evidence_paths:
        fail("verification.evidence_paths must be a non-empty JSON array")
    validated_evidence: list[str] = []
    seen_paths: set[str] = set()
    for index, value in enumerate(evidence_paths):
        path = validate_relative_path(
            value, f"verification.evidence_paths[{index}]"
        )
        if path in seen_paths:
            fail(f"duplicate evidence path: {path}")
        seen_paths.add(path)
        resolve_regular_file_without_symlinks(
            project_root,
            path,
            f"verification.evidence_paths[{index}]",
        )
        validated_evidence.append(path)

    next_actions = contract["next_actions"]
    if not isinstance(next_actions, dict):
        fail("next_actions must be a JSON object")
    expect_exact_keys(next_actions, {"pass", "fail"}, "next_actions")
    validated_next_actions = {
        result: expect_nonempty_string(
            next_actions[result], f"next_actions.{result}"
        )
        for result in ("pass", "fail")
    }
    return {
        "schema_version": VERIFY_CONTRACT_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "verification": {
            "argv": argv,
            "evidence_paths": validated_evidence,
            "timeout_seconds": timeout_seconds,
            "max_output_chars": max_output_chars,
        },
        "next_actions": validated_next_actions,
    }


def _hash_evidence(
    project_root: Path, evidence_paths: list[str]
) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for index, relative_path in enumerate(evidence_paths):
        path = resolve_regular_file_without_symlinks(
            project_root,
            relative_path,
            f"verification.evidence_paths[{index}]",
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
                f"could not snapshot evidence file {relative_path}: {exc}"
            ) from exc
        evidence.append(
            {"path": relative_path, "sha256": digest.hexdigest(), "size": size}
        )
    return evidence


class _BoundedStreamCapture:
    """Drain, normalize, and retain only a bounded text prefix."""

    def __init__(self, max_chars: int, project_root_prefix: str) -> None:
        self.max_chars = max_chars
        self.project_root_prefix = project_root_prefix
        self.observed_chars = 0
        self.normalized_chars = 0
        self.stored_chars = 0
        self.root_replacements = 0
        self.parts: list[str] = []
        self.pending = ""
        self.read_error: str | None = None

    def _emit(self, value: str) -> None:
        self.normalized_chars += len(value)
        remaining = self.max_chars - self.stored_chars
        if remaining <= 0:
            return
        kept = value[:remaining]
        self.parts.append(kept)
        self.stored_chars += len(kept)

    def add(self, value: str) -> None:
        self.observed_chars += len(value)
        data = self.pending + value
        safe_start_limit = max(
            0, len(data) - len(self.project_root_prefix) + 1
        )
        cursor = 0
        while cursor < safe_start_limit:
            match = data.find(self.project_root_prefix, cursor)
            if match == -1 or match >= safe_start_limit:
                self._emit(data[cursor:safe_start_limit])
                cursor = safe_start_limit
                break
            self._emit(data[cursor:match])
            self._emit(PROJECT_ROOT_TOKEN)
            self.root_replacements += 1
            cursor = match + len(self.project_root_prefix)
        self.pending = data[cursor:]

    def finish(self) -> None:
        if not self.pending:
            return
        self.root_replacements += self.pending.count(self.project_root_prefix)
        self._emit(
            self.pending.replace(self.project_root_prefix, PROJECT_ROOT_TOKEN)
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
                capture.project_root_prefix, PROJECT_ROOT_TOKEN
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
    project_root: Path,
    timeout_seconds: float,
    max_output_chars: int,
) -> dict[str, Any]:
    project_root_prefix = str(project_root.resolve(strict=True))
    stdout_capture = _BoundedStreamCapture(
        max_output_chars, project_root_prefix
    )
    stderr_capture = _BoundedStreamCapture(
        max_output_chars, project_root_prefix
    )
    timed_out = False
    process_returncode: int | None = None

    try:
        process = subprocess.Popen(
            argv,
            cwd=project_root,
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
            fail("verification process did not expose stdout and stderr pipes")
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

    stdout, stdout_metadata, stdout_replacements = _capture_result(stdout_capture)
    stderr, stderr_metadata, stderr_replacements = _capture_result(stderr_capture)
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
            "output_root_token": PROJECT_ROOT_TOKEN,
            "stdout_replacements": stdout_replacements,
            "stderr_replacements": stderr_replacements,
        },
    }


def _atomic_write_status(path: Path, content: str) -> None:
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
    work_root: Path,
    identity: WorkspaceIdentity,
    receipt: dict[str, Any],
) -> str:
    records_relative = f"{identity.workspace_path}/records"
    records_dir = resolve_directory_without_symlinks(
        work_root, records_relative, "Workspace records directory"
    )
    reject_symlink_components(
        work_root, records_relative, "Workspace records directory"
    )
    content = json.dumps(
        receipt, ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".verify-receipt-", suffix=".tmp", dir=records_dir
    )
    temporary_path = Path(temporary_name)
    try:
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        except BaseException:
            raise

        for _ in range(5):
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            filename = f"verify-{timestamp}-{uuid.uuid4().hex}.json"
            receipt_path = records_dir / filename
            try:
                os.link(temporary_path, receipt_path)
            except FileExistsError:
                continue
            return f"{records_relative}/{filename}"
        fail("could not allocate a unique append-only verification receipt")
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def verify_workspace(
    project_root: Path,
    work_root: Path,
    explicit_workspace_id: str | None = None,
) -> tuple[int, dict[str, Any]]:
    """Run verify.json only, then append receipt and atomically update status."""

    identity = select_workspace(work_root, explicit_workspace_id)
    contract = _load_verify_contract(project_root, work_root, identity)
    state_directory = f"{identity.workspace_path}/current/state"
    resolve_directory_without_symlinks(
        work_root, state_directory, "Workspace state directory"
    )
    status_relative = state_status_path(identity)
    status_path = resolve_regular_file_without_symlinks(
        work_root, status_relative, "Workspace state status"
    )
    load_state_status(work_root, identity)

    verification = contract["verification"]
    evidence_collected_at = _utc_now()
    evidence_files = _hash_evidence(
        project_root, verification["evidence_paths"]
    )
    started_at = _utc_now()
    execution = _run_bounded_verification(
        verification["argv"],
        project_root,
        verification["timeout_seconds"],
        verification["max_output_chars"],
    )
    exit_code = execution["exit_code"]
    finished_at = _utc_now()
    result = "pass" if exit_code == 0 else "fail"
    receipt = {
        "schema_version": VERIFICATION_RECEIPT_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "started_at": started_at,
        "finished_at": finished_at,
        "argv": verification["argv"],
        "exit_code": exit_code,
        "process_returncode": execution["process_returncode"],
        "result": result,
        "stdout": execution["stdout"],
        "stderr": execution["stderr"],
        "timeout": {
            "timeout_seconds": verification["timeout_seconds"],
            "timed_out": execution["timed_out"],
        },
        "output_capture": execution["output_capture"],
        "normalization": execution["normalization"],
        "evidence_collected_at": evidence_collected_at,
        "evidence_capture": "before_verification",
        "evidence_files": evidence_files,
    }
    receipt_relative = _write_receipt(work_root, identity, receipt)

    next_action = contract["next_actions"][result]
    state_status = {
        "schema_version": STATE_STATUS_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "status": (
            "verified_waiting_acceptance"
            if result == "pass"
            else "verification_failed"
        ),
        "result": result,
        "receipt": receipt_relative,
        "finished_at": finished_at,
        "next_action": next_action,
    }
    _atomic_write_status(
        status_path,
        json.dumps(state_status, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
    )

    return exit_code, {
        "workspace_id": identity.workspace_id,
        "result": result,
        "exit_code": exit_code,
        "receipt": receipt_relative,
        "status": state_status["status"],
        "timed_out": execution["timed_out"],
        "next_action": next_action,
    }
