"""Request policy configuration validation."""

from __future__ import annotations

from dataclasses import dataclass


DEFAULT_REQUEST_TIMEOUT_MS = 5000
_ALLOWED_KEYS = frozenset({"request_timeout_ms"})


@dataclass(frozen=True, slots=True)
class RequestPolicy:
    """Validated, immutable policy values used by request execution."""

    request_timeout_ms: int


def load_request_policy(config: dict[str, object]) -> RequestPolicy:
    """Validate a request policy dictionary and return immutable values.

    ``request_timeout_ms`` may be omitted, in which case the product default is
    used. Explicit values must be positive integers. Booleans are rejected even
    though Python models ``bool`` as a subclass of ``int``.
    """

    if not isinstance(config, dict):
        raise TypeError("request policy config must be a dict")

    unknown_keys = set(config).difference(_ALLOWED_KEYS)
    if unknown_keys:
        unknown = ", ".join(sorted(str(key) for key in unknown_keys))
        raise ValueError(f"unknown request policy key(s): {unknown}")

    request_timeout_ms = config.get(
        "request_timeout_ms", DEFAULT_REQUEST_TIMEOUT_MS
    )
    if isinstance(request_timeout_ms, bool) or not isinstance(
        request_timeout_ms, int
    ):
        raise TypeError("request_timeout_ms must be an integer")
    if request_timeout_ms <= 0:
        raise ValueError("request_timeout_ms must be greater than zero")

    return RequestPolicy(request_timeout_ms=request_timeout_ms)
