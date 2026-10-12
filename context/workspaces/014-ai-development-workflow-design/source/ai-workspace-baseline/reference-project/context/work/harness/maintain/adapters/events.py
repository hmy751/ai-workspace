"""두 도구 연결에서 사용하는 hook 응답과 정규화된 이벤트 이름."""

from typing import Any


def _hook_output(
    hook_event_name: str,
    *,
    additional_context: str | None = None,
    system_message: str | None = None,
) -> dict[str, Any]:
    output: dict[str, Any] = {"continue": True}
    if system_message:
        output["systemMessage"] = system_message
    if additional_context:
        output["hookSpecificOutput"] = {
            "hookEventName": hook_event_name,
            "additionalContext": additional_context,
        }
    return output
