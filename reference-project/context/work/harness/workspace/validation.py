"""Harness 공통 오류와 JSON 값의 최소 계약을 검사한다."""

from __future__ import annotations

from typing import Any, NoReturn


class HarnessError(ValueError):
    """Workspace 계약이 잘못되었거나 안전하지 않을 때 발생한다."""


def fail(message: str) -> NoReturn:
    raise HarnessError(message)


def expect_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual == expected:
        return
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    details = []
    if missing:
        details.append(f"missing={missing}")
    if extra:
        details.append(f"extra={extra}")
    fail(f"invalid {label} keys: {', '.join(details)}")


def expect_schema_version(value: Any, expected: int, label: str) -> None:
    if type(value) is not int or value != expected:
        fail(f"unsupported {label} schema_version: {value!r}")


def expect_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    if "\x00" in value:
        fail(f"{label} must not contain NUL")
    return value
