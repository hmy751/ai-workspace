"""적용 가능한 결정의 엄격한 구조·경로 표기·중복 검증."""

from __future__ import annotations

from pathlib import PurePosixPath
import re
from typing import Any

from ...workspace_contract import (
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
    validate_relative_path,
    validate_workspace_id,
)


MAINTAIN_DECISION_SCHEMA_VERSION = 1

_DECISION_KEYS = {
    "schema_version",
    "workspace_id",
    "outcome",
    "importance",
    "summary",
    "changes",
    "evidence",
    "unresolved",
    "question",
}

_CHANGE_KEYS = {"path", "expected_sha256", "content", "reason"}

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _validate_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        fail(f"{label} must be a JSON array")
    return [
        expect_nonempty_string(entry, f"{label}[{index}]")
        for index, entry in enumerate(value)
    ]


def _validate_expected_sha256(value: Any, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not _SHA256_PATTERN.fullmatch(value):
        fail(f"{label} must be null or a lowercase SHA-256 hex digest")
    return value


def _validate_change(value: Any, index: int) -> dict[str, Any]:
    label = f"Maintain decision changes[{index}]"
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    expect_exact_keys(value, _CHANGE_KEYS, label)
    path = validate_relative_path(value["path"], f"{label}.path")
    if path != path.replace("\\", "/") or PurePosixPath(path).as_posix() != path:
        fail(f"{label}.path must be a canonical POSIX relative path")
    expected_sha256 = _validate_expected_sha256(
        value["expected_sha256"], f"{label}.expected_sha256"
    )
    content = value["content"]
    if not isinstance(content, str):
        fail(f"{label}.content must be a string")
    reason = expect_nonempty_string(value["reason"], f"{label}.reason")
    return {
        "path": path,
        "expected_sha256": expected_sha256,
        "content": content,
        "reason": reason,
    }


def validate_maintain_decision(
    value: Any,
    workspace_id: str,
) -> dict[str, Any]:
    """판단 결과가 적용 계약의 정확한 필드와 조건을 만족하는지 검증한다."""

    explicit_workspace_id = validate_workspace_id(workspace_id)
    if not isinstance(value, dict):
        fail("Maintain decision must be a JSON object")
    expect_exact_keys(value, _DECISION_KEYS, "Maintain decision")
    expect_schema_version(
        value["schema_version"],
        MAINTAIN_DECISION_SCHEMA_VERSION,
        "Maintain decision",
    )
    decision_workspace_id = validate_workspace_id(value["workspace_id"])
    if decision_workspace_id != explicit_workspace_id:
        fail("Maintain decision workspace_id does not match the binding")

    outcome = value["outcome"]
    if not isinstance(outcome, str) or outcome not in {
        "no_change",
        "update",
        "needs_user_decision",
    }:
        fail(f"invalid Maintain decision outcome: {outcome!r}")
    importance = value["importance"]
    if not isinstance(importance, str) or importance not in {
        "none",
        "quiet",
        "important",
    }:
        fail(f"invalid Maintain decision importance: {importance!r}")
    summary = expect_nonempty_string(
        value["summary"], "Maintain decision summary"
    )
    raw_changes = value["changes"]
    if not isinstance(raw_changes, list):
        fail("Maintain decision changes must be a JSON array")
    changes = [
        _validate_change(change, index)
        for index, change in enumerate(raw_changes)
    ]
    paths = [change["path"] for change in changes]
    if len(paths) != len(set(paths)):
        fail("Maintain decision changes must not contain duplicate paths")
    evidence = _validate_string_list(
        value["evidence"], "Maintain decision evidence"
    )
    unresolved = _validate_string_list(
        value["unresolved"], "Maintain decision unresolved"
    )
    question = value["question"]
    if question is not None:
        question = expect_nonempty_string(
            question, "Maintain decision question"
        )

    if outcome == "no_change":
        if importance != "none" or changes or question is not None:
            fail(
                "no_change requires importance='none', no changes, and "
                "question=null"
            )
    elif outcome == "update":
        if importance not in {"quiet", "important"}:
            fail("update requires importance='quiet' or 'important'")
        if not changes:
            fail("update requires at least one change")
        if question is not None:
            fail("update requires question=null")
    else:
        if importance != "important" or changes or question is None:
            fail(
                "needs_user_decision requires importance='important', no "
                "changes, and a non-empty question"
            )

    return {
        "schema_version": MAINTAIN_DECISION_SCHEMA_VERSION,
        "workspace_id": decision_workspace_id,
        "outcome": outcome,
        "importance": importance,
        "summary": summary,
        "changes": changes,
        "evidence": evidence,
        "unresolved": unresolved,
        "question": question,
    }
