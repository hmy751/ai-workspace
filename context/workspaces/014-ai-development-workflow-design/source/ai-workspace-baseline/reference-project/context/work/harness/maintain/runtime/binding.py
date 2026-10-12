"""명시적 Workspace 연결·해제와 generation 보존을 소유한다."""

from __future__ import annotations

from typing import Any

from ...workspace_contract import (
    HarnessError,
    expect_nonempty_string,
    validate_workspace_id,
)
from .context import RuntimeContext
from .notices import NoticeService
from .storage import RuntimeStore
from .state import (
    MAINTAIN_HOST_STATE_SCHEMA_VERSION,
    _current_binding,
    _snapshot_fields,
    _persisted_state,
)
from .storage_io import _atomic_write_json


class BindingService:
    """명시적 Workspace 연결·해제와 generation 보존."""

    def __init__(
        self,
        context: RuntimeContext,
        notices: NoticeService,
        store: RuntimeStore,
    ) -> None:
        self.context = context
        self.notices = notices
        self.store = store

    def activate(self, session_id: str, workspace_id: str) -> dict[str, Any]:
        """한 Main session의 이후 prompt를 명시적 Workspace에 연결한다.

        이미 접수된 prompt는 기존 binding snapshot을 유지하므로 늦은 응답도
        이전 generation에서 처리한다."""

        self.context.validate_config()
        session_id = expect_nonempty_string(session_id, "Maintain session id")
        workspace_id = validate_workspace_id(workspace_id)
        session_directory = self.store._session_directory(session_id)

        with self.store._state_lock(session_directory):
            state_path = session_directory / "session.json"
            if state_path.exists():
                state = self.store._read_session_state(session_directory)
            else:
                state = {
                    "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                    "current_generation": None,
                    "bindings": [],
                    "legacy": False,
                }
            current = _current_binding(state)
            if current is not None and current["workspace_id"] == workspace_id:
                return {
                    "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                    "status": "already_active",
                    "session_id": session_id,
                    **_snapshot_fields(current),
                }

            try:
                bounded_bootstrap = self.context.bootstrap(
                    self.context.project_root, self.context.work_root, workspace_id
                )
                session_type = self.context.session_type
                semantic_session = session_type(
                    self.context.project_root,
                    workspace_id,
                    runner=self.context.runner,
                )
                grounding = semantic_session.start(bounded_bootstrap)
                thread_id = expect_nonempty_string(
                    semantic_session.thread_id,
                    "grounded Maintain thread_id",
                )
            except Exception as exc:
                message = (
                    f"Maintain grounding failed for Workspace `{workspace_id}`: "
                    f"{exc}. The previous session binding was preserved."
                )
                # 한국어: 해당 Workspace의 초기 맥락 정립에 실패했다: {exc}.
                # 이전 세션 연결은 보존했다.
                self.notices._write_notice(
                    session_directory,
                    f"activation-{workspace_id}-{int(self.context.clock() * 1_000_000)}",
                    kind="failure",
                    message=message,
                )
                raise HarnessError(message) from exc

            if grounding.get("status") != "grounded":
                question = grounding.get("question")
                if not isinstance(question, str) or not question.strip():
                    question = "Maintainer grounding requires a user decision."
                    # 한국어: Maintainer의 초기 맥락 정립에 사용자 결정이 필요하다.
                message = (
                    f"Maintain could not ground Workspace `{workspace_id}` "
                    f"without a user decision: {question} The previous session "
                    "binding was preserved."
                )
                # 한국어: 사용자 결정 없이는 해당 Workspace의 초기 맥락을 정립할 수
                # 없었다: {question}. 이전 세션 연결은 보존했다.
                self.notices._write_notice(
                    session_directory,
                    f"activation-{workspace_id}-{int(self.context.clock() * 1_000_000)}",
                    kind="ambiguity",
                    message=message,
                )
                raise HarnessError(message)

            generation = (
                max(
                    (binding["generation"] for binding in state["bindings"]),
                    default=0,
                )
                + 1
            )
            binding = {
                "generation": generation,
                "workspace_id": workspace_id,
                "thread_id": thread_id,
                "grounded_at": self.context.clock(),
            }
            updated_state = {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "current_generation": generation,
                "bindings": [*state["bindings"], binding],
            }
            _atomic_write_json(state_path, updated_state)

        return {
            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
            "status": "activated",
            "session_id": session_id,
            "previous_workspace_id": (
                current["workspace_id"] if current is not None else None
            ),
            **_snapshot_fields(binding),
        }

    def deactivate(self, session_id: str) -> dict[str, Any]:
        """이전 generation을 보존하고 이후 prompt의 연결만 해제한다."""

        self.context.validate_config()
        session_id = expect_nonempty_string(session_id, "Maintain session id")
        session_directory = self.store._session_directory(session_id)
        state_path = session_directory / "session.json"
        if not session_directory.exists() or not state_path.exists():
            return {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "status": "already_unbound",
                "session_id": session_id,
                "current_binding": None,
            }
        with self.store._state_lock(session_directory):
            if not state_path.exists():
                return {
                    "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                    "status": "already_unbound",
                    "session_id": session_id,
                    "current_binding": None,
                }
            state = self.store._read_session_state(session_directory)
            current = _current_binding(state)
            if current is None:
                status = "already_unbound"
            else:
                state["current_generation"] = None
                _atomic_write_json(state_path, _persisted_state(state))
                status = "deactivated"
        return {
            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
            "status": status,
            "session_id": session_id,
            "previous_binding": (
                _snapshot_fields(current) if current is not None else None
            ),
            "current_binding": None,
        }
