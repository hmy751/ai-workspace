"""저장 상태 버전과 generation 귀속 규칙. 도구별 세션 선택과 독립적이다."""

from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Any

from ...workspace_contract import (
    expect_exact_keys,
    expect_nonempty_string,
    fail,
    validate_workspace_id,
)


MAINTAIN_HOST_CONFIG_SCHEMA_VERSION = 2
MAINTAIN_HOST_STATE_SCHEMA_VERSION = 2

_LEGACY_HOST_CONFIG_SCHEMA_VERSION = 1
_LEGACY_HOST_STATE_SCHEMA_VERSION = 1

_CONFIG_V1_KEYS = {"schema_version", "workspace_id"}
_CONFIG_V2_KEYS = {"schema_version", "mode"}

_SESSION_V1_KEYS = {
    "schema_version",
    "workspace_id",
    "thread_id",
    "grounded_at",
}

_SESSION_V2_KEYS = {
    "schema_version",
    "current_generation",
    "bindings",
}

_BINDING_KEYS = {
    "generation",
    "workspace_id",
    "thread_id",
    "grounded_at",
}

_BINDING_SNAPSHOT_KEYS = (
    "binding_generation",
    "workspace_id",
    "thread_id",
)

_STATUS_SNAPSHOT_ATTEMPTS = 5
_HEX_DIGEST = re.compile(r"^[0-9a-f]{64}$")

_HOOK_EVENTS = {
    "session-start": "SessionStart",
    "user-prompt": "UserPromptSubmit",
    "response-end": "Stop",
    "session-end": "SessionEnd",
}


def _validated_binding(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail("Maintain runtime binding must be a JSON object")
    expect_exact_keys(value, _BINDING_KEYS, "Maintain runtime binding")
    generation = value["generation"]
    if type(generation) is not int or generation < 1:
        fail("Maintain runtime binding generation must be a positive integer")
    grounded_at = value["grounded_at"]
    if not isinstance(grounded_at, (int, float)) or isinstance(grounded_at, bool):
        fail("Maintain runtime grounded_at must be a number")
    return {
        "generation": generation,
        "workspace_id": validate_workspace_id(value["workspace_id"]),
        "thread_id": expect_nonempty_string(
            value["thread_id"], "Maintain runtime thread_id"
        ),
        "grounded_at": grounded_at,
    }


def _binding_for_generation(
    state: Mapping[str, Any], generation: int
) -> dict[str, Any]:
    for binding in state["bindings"]:
        if binding["generation"] == generation:
            return dict(binding)
    fail(
        f"Maintain runtime event names unknown binding generation {generation}"
    )


def _current_binding(state: Mapping[str, Any]) -> dict[str, Any] | None:
    generation = state["current_generation"]
    if generation is None:
        return None
    return _binding_for_generation(state, generation)


def _binding_snapshot(
    value: Mapping[str, Any],
    state: Mapping[str, Any],
    label: str,
) -> dict[str, Any]:
    present = [key in value for key in _BINDING_SNAPSHOT_KEYS]
    if not any(present):
        if value.get("schema_version") != _LEGACY_HOST_STATE_SCHEMA_VERSION:
            fail(f"{label} is missing its binding snapshot")
        return _binding_for_generation(state, 1)
    if not all(present):
        fail(f"{label} has a partial binding snapshot")
    generation = value["binding_generation"]
    if type(generation) is not int or generation < 1:
        fail(f"{label} binding_generation must be a positive integer")
    binding = _binding_for_generation(state, generation)
    workspace_id = validate_workspace_id(value["workspace_id"])
    thread_id = expect_nonempty_string(value["thread_id"], f"{label} thread_id")
    if (
        workspace_id != binding["workspace_id"]
        or thread_id != binding["thread_id"]
    ):
        fail(f"{label} binding snapshot changed")
    return binding


def _snapshot_fields(binding: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "binding_generation": binding["generation"],
        "workspace_id": binding["workspace_id"],
        "thread_id": binding["thread_id"],
    }


def _persisted_state(state: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
        "current_generation": state["current_generation"],
        "bindings": state["bindings"],
    }
