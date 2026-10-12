"""사용자에게 전달할 결과 알림을 소유한다."""

from __future__ import annotations

from collections.abc import Mapping
import os
from pathlib import Path
from typing import Any

from ...workspace_contract import expect_nonempty_string, fail
from .context import RuntimeContext
from .state import MAINTAIN_HOST_STATE_SCHEMA_VERSION
from .storage_io import _hash_identifier, _atomic_write_json, _read_json_object


class NoticeService:
    """사용자에게 전달할 결과 알림."""

    def __init__(self, context: RuntimeContext) -> None:
        self.context = context

    def _write_notice(
        self,
        session_directory: Path,
        notice_key: str,
        *,
        kind: str,
        message: str,
    ) -> None:
        if kind not in {"important", "ambiguity", "failure"}:
            fail("Maintain notifications are limited to important results and failures")
        safe_key = _hash_identifier(notice_key)
        path = session_directory / "notices" / f"{safe_key}.json"
        _atomic_write_json(
            path,
            {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "kind": kind,
                "message": expect_nonempty_string(message, "Maintain notice"),
                "created_at": self.context.clock(),
            },
        )

    def _take_notices(self, session_directory: Path) -> list[dict[str, Any]]:
        notices_directory = session_directory / "notices"
        if not notices_directory.exists():
            return []
        surfaced_directory = session_directory / "surfaced-notices"
        surfaced_directory.mkdir(parents=True, exist_ok=True)
        notices: list[tuple[Path, dict[str, Any]]] = []
        for path in notices_directory.glob("*.json"):
            notice = _read_json_object(path, "Maintain runtime notification")
            if notice.get("kind") not in {"important", "ambiguity", "failure"}:
                fail("Maintain runtime notification kind is invalid")
            if not isinstance(notice.get("created_at"), (int, float)):
                fail("Maintain runtime notification timestamp is invalid")
            expect_nonempty_string(
                notice.get("message"), "Maintain runtime notification message"
            )
            notices.append((path, notice))
        notices.sort(key=lambda item: (item[1]["created_at"], item[0].name))
        for path, _ in notices:
            os.replace(path, surfaced_directory / path.name)
        return [notice for _, notice in notices]

    def _notification_for_result(
        self,
        session_directory: Path,
        turn_key: str,
        result: Mapping[str, Any],
    ) -> None:
        context_status = result.get("context_status")
        importance = result.get("importance")
        workspace_id = result.get("workspace_id")
        summary = result.get("summary")
        if context_status == "needs_user_decision":
            question = result.get("question")
            self._write_notice(
                session_directory,
                turn_key,
                kind="ambiguity",
                message=(
                    f"Maintain needs a decision for Workspace `{workspace_id}`: "
                    f"{question} No related Context write was made."
                    # 한국어: 해당 Workspace에 사용자 결정이 필요하다: {question}.
                    # 관련 Context에는 아무것도 쓰지 않았다.
                ),
            )
        elif context_status == "updated" and importance == "important":
            changed = result.get("changed")
            paths = []
            if isinstance(changed, list):
                paths = [
                    str(item.get("path"))
                    for item in changed
                    if isinstance(item, Mapping) and item.get("path")
                ]
            path_text = f" Changed: {', '.join(paths)}." if paths else ""
            # 한국어: 변경한 경로가 있으면 '변경: {경로 목록}.'을 덧붙인다.
            self._write_notice(
                session_directory,
                turn_key,
                kind="important",
                message=(
                    f"Maintain updated Workspace `{workspace_id}`: {summary}."
                    f"{path_text}"
                    # 한국어: 해당 Workspace를 갱신했다: {summary}. {변경 경로 안내}
                ),
            )
