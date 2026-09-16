"""의미 판단 응답의 형태와 명시적 Workspace 귀속을 검증한다."""

from __future__ import annotations

import re
from typing import Any

from ...workspace_contract import (
    expect_exact_keys,
    expect_nonempty_string,
    expect_schema_version,
    fail,
    validate_workspace_id,
)


_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

_GROUNDING_KEYS = {
    "schema_version",
    "workspace_id",
    "status",
    "starting_state",
    "unresolved",
    "question",
}

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


class ResponseValidator:
    def __init__(self, workspace_id: str) -> None:
        self.workspace_id = workspace_id

    def _validate_grounding(self, value: dict[str, Any]) -> None:
        expect_exact_keys(value, _GROUNDING_KEYS, "Maintain grounding")
        expect_schema_version(value["schema_version"], 1, "Maintain grounding")
        self._expect_workspace(value["workspace_id"], "Maintain grounding")
        status = value["status"]
        if status not in {"grounded", "needs_user_decision"}:
            fail(f"invalid Maintain grounding status: {status!r}")
        expect_nonempty_string(
            value["starting_state"], "Maintain grounding starting_state"
        )
        self._expect_string_list(value["unresolved"], "grounding unresolved")
        question = value["question"]
        if status == "grounded":
            if question is not None:
                fail("grounded Maintain result must have question=null")
        elif not isinstance(question, str) or not question.strip():
            fail("needs_user_decision grounding must have a non-empty question")

    def _validate_decision(self, value: dict[str, Any]) -> None:
        expect_exact_keys(value, _DECISION_KEYS, "Maintain decision")
        expect_schema_version(value["schema_version"], 1, "Maintain decision")
        self._expect_workspace(value["workspace_id"], "Maintain decision")
        outcome = value["outcome"]
        importance = value["importance"]
        if outcome not in {"no_change", "update", "needs_user_decision"}:
            fail(f"invalid Maintain decision outcome: {outcome!r}")
        if importance not in {"none", "quiet", "important"}:
            fail(f"invalid Maintain decision importance: {importance!r}")
        expect_nonempty_string(value["summary"], "Maintain decision summary")
        changes = value["changes"]
        if type(changes) is not list:
            fail("Maintain decision changes must be an array")
        for index, change in enumerate(changes):
            if not isinstance(change, dict):
                fail(f"Maintain decision change {index} must be an object")
            expect_exact_keys(change, _CHANGE_KEYS, f"Maintain change {index}")
            expect_nonempty_string(change["path"], f"Maintain change {index} path")
            expected_sha256 = change["expected_sha256"]
            if expected_sha256 is not None and (
                not isinstance(expected_sha256, str)
                or not _SHA256_PATTERN.fullmatch(expected_sha256)
            ):
                fail(
                    f"Maintain change {index} expected_sha256 must be null or "
                    "64 lowercase hexadecimal characters"
                )
            if not isinstance(change["content"], str):
                fail(f"Maintain change {index} content must be a string")
            expect_nonempty_string(
                change["reason"], f"Maintain change {index} reason"
            )
        self._expect_string_list(value["evidence"], "decision evidence")
        self._expect_string_list(value["unresolved"], "decision unresolved")
        question = value["question"]
        if outcome == "no_change":
            if importance != "none" or changes or question is not None:
                fail("no_change requires importance=none, no changes, question=null")
        elif outcome == "update":
            if importance not in {"quiet", "important"}:
                fail("update requires importance=quiet or important")
            if not changes or question is not None:
                fail("update requires changes and question=null")
        else:
            if importance != "important" or changes:
                fail(
                    "needs_user_decision requires importance=important and no changes"
                )
            if not isinstance(question, str) or not question.strip():
                fail("needs_user_decision requires a non-empty question")

    def _expect_workspace(self, value: Any, label: str) -> None:
        workspace_id = validate_workspace_id(value)
        if workspace_id != self.workspace_id:
            fail(
                f"{label} workspace_id does not match the explicit Workspace: "
                f"expected {self.workspace_id!r}, got {workspace_id!r}"
            )

    @staticmethod
    def _expect_string_list(value: Any, label: str) -> None:
        if type(value) is not list:
            fail(f"Maintain {label} must be an array")
        for index, item in enumerate(value):
            if not isinstance(item, str):
                fail(f"Maintain {label} item {index} must be a string")
