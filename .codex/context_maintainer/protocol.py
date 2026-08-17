"""Wire validation and stable identifiers for the v1 observe protocol."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional


SESSION_SOURCES = {"startup", "resume", "clear", "compact"}
HOOK_EVENTS = {"SessionStart", "UserPromptSubmit", "Stop"}


class ProtocolError(ValueError):
    """A hook or queued event does not satisfy the v1 protocol."""


def event_key(session_id: str, turn_id: str) -> str:
    material = (session_id + "\0" + turn_id).encode("utf-8")
    return hashlib.sha256(material).hexdigest()[:32]


def value_digest(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _object(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ProtocolError("hook payload must be a JSON object")
    return payload


def _string(payload: Dict[str, Any], field: str, *, nonempty: bool = True) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or (nonempty and not value):
        raise ProtocolError(f"{field} must be a non-empty string")
    return value


def _event_name(payload: Dict[str, Any], expected: str) -> None:
    actual = _string(payload, "hook_event_name")
    if actual != expected:
        raise ProtocolError(
            f"hook_event_name must be {expected!r}, received {actual!r}"
        )


def validate_session_start(payload: Any) -> Dict[str, Any]:
    value = _object(payload)
    _event_name(value, "SessionStart")
    source = _string(value, "source")
    if source not in SESSION_SOURCES:
        raise ProtocolError("source must be startup, resume, clear, or compact")
    return {
        "session_id": _string(value, "session_id"),
        "source": source,
        "cwd": value.get("cwd") if isinstance(value.get("cwd"), str) else None,
        "model": value.get("model") if isinstance(value.get("model"), str) else None,
    }


def validate_user_prompt(payload: Any) -> Dict[str, Any]:
    value = _object(payload)
    _event_name(value, "UserPromptSubmit")
    prompt = value.get("prompt")
    if not isinstance(prompt, str):
        raise ProtocolError("prompt must be a string")
    return {
        "session_id": _string(value, "session_id"),
        "turn_id": _string(value, "turn_id"),
        "prompt": prompt,
    }


def validate_stop(payload: Any) -> Dict[str, Any]:
    value = _object(payload)
    _event_name(value, "Stop")
    assistant = value.get("last_assistant_message")
    if assistant is not None and not isinstance(assistant, str):
        raise ProtocolError("last_assistant_message must be a string or null")
    active = value.get("stop_hook_active")
    if not isinstance(active, bool):
        raise ProtocolError("stop_hook_active must be a boolean")
    return {
        "session_id": _string(value, "session_id"),
        "turn_id": _string(value, "turn_id"),
        "last_assistant_message": assistant,
        "stop_hook_active": active,
    }


def validate_queue_event(
    payload: Any, expected_sequence: Optional[int] = None
) -> Dict[str, Any]:
    value = _object(payload)
    if value.get("schema") != "context-maintainer.response-end.v1":
        raise ProtocolError("queue event schema is not v1")
    sequence = value.get("sequence")
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
        raise ProtocolError("queue event sequence must be a positive integer")
    if expected_sequence is not None and sequence != expected_sequence:
        raise ProtocolError("queue event sequence does not match FIFO position")
    identity = value.get("identity")
    if not isinstance(identity, dict):
        raise ProtocolError("queue event identity must be an object")
    session_id = _string(identity, "session_id")
    turn_id = _string(identity, "turn_id")
    if value.get("event_key") != event_key(session_id, turn_id):
        raise ProtocolError("queue event key does not match identity")
    user = value.get("user")
    assistant = value.get("assistant")
    if not isinstance(user, dict) or not isinstance(user.get("prompt"), str):
        raise ProtocolError("queue event user prompt is invalid")
    if not isinstance(assistant, dict):
        raise ProtocolError("queue event assistant payload is invalid")
    if assistant.get("message") is not None and not isinstance(
        assistant.get("message"), str
    ):
        raise ProtocolError("queue event assistant message is invalid")
    if not isinstance(assistant.get("stop_hook_active"), bool):
        raise ProtocolError("queue event stop_hook_active is invalid")
    git_value = value.get("git")
    if not isinstance(git_value, dict):
        raise ProtocolError("queue event git fingerprints are missing")
    if not isinstance(git_value.get("pre_turn"), dict) or not isinstance(
        git_value.get("post_turn"), dict
    ):
        raise ProtocolError("queue event git fingerprints are invalid")
    return value
