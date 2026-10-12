"""Verify 전용 claim·argv·evidence 경로와 실행 한도를 검사한다."""

from __future__ import annotations

import math
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from ..workspace.identity import WorkspaceIdentity, validate_workspace_id
from ..workspace.paths import (
    read_json_without_symlinks,
    resolve_regular_file_without_symlinks,
    validate_relative_path,
)
from ..workspace.validation import (
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
)

VERIFY_CONTRACT_SCHEMA_VERSION = 2
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_TIMEOUT_SECONDS = 300.0
DEFAULT_MAX_OUTPUT_CHARS = 100_000
MAX_OUTPUT_CHARS = 1_000_000
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


def load_verify_contract(
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
        {
            "schema_version",
            "workspace_id",
            "claim",
            "canonical_basis",
            "verification",
        },
        "Workspace verify contract",
    )
    expect_schema_version(
        contract["schema_version"],
        VERIFY_CONTRACT_SCHEMA_VERSION,
        "Workspace verify contract",
    )
    if validate_workspace_id(contract["workspace_id"]) != identity.workspace_id:
        fail("verify contract workspace_id does not match the selected workspace")

    claim = expect_nonempty_string(contract["claim"], "verification claim")

    canonical_basis = _validate_snapshot_paths(
        project_root,
        contract["canonical_basis"],
        "canonical_basis",
    )

    verification = contract["verification"]
    if not isinstance(verification, dict):
        fail("verification must be a JSON object")
    _expect_verification_keys(verification)
    argv = _validate_argv(verification["argv"])

    timeout_seconds = verification.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
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

    max_output_chars = verification.get("max_output_chars", DEFAULT_MAX_OUTPUT_CHARS)
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

    validated_evidence = _validate_snapshot_paths(
        project_root,
        verification["evidence_paths"],
        "verification.evidence_paths",
    )
    return {
        "schema_version": VERIFY_CONTRACT_SCHEMA_VERSION,
        "workspace_id": identity.workspace_id,
        "claim": claim,
        "canonical_basis": canonical_basis,
        "verification": {
            "argv": argv,
            "evidence_paths": validated_evidence,
            "timeout_seconds": timeout_seconds,
            "max_output_chars": max_output_chars,
        },
    }


def _validate_snapshot_paths(
    project_root: Path,
    values: Any,
    field: str,
) -> list[str]:
    if not isinstance(values, list) or not values:
        fail(f"{field} must be a non-empty JSON array")
    validated: list[str] = []
    seen_paths: set[str] = set()
    for index, value in enumerate(values):
        label = f"{field}[{index}]"
        path = validate_relative_path(value, label)
        if path in seen_paths:
            fail(f"duplicate {field} path: {path}")
        seen_paths.add(path)
        resolve_regular_file_without_symlinks(project_root, path, label)
        validated.append(path)
    return validated
