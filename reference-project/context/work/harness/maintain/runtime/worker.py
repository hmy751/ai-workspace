"""접수된 event의 직렬 실행과 결과 반영을 소유한다."""

from __future__ import annotations

import subprocess
from typing import Any

from .context import RuntimeContext
from .notices import NoticeService
from .storage import RuntimeStore
from .state import (
    MAINTAIN_HOST_STATE_SCHEMA_VERSION,
    _binding_snapshot,
    _snapshot_fields,
)
from .storage_io import _atomic_write_json, _read_json_object


class DrainWorker:
    """접수된 event의 직렬 실행과 결과 반영."""

    def __init__(
        self,
        context: RuntimeContext,
        notices: NoticeService,
        store: RuntimeStore,
    ) -> None:
        self.context = context
        self.notices = notices
        self.store = store

    def _start_detached_drain(self, session_key: str) -> None:
        command = [
            self.context.python_executable,
            "-m",
            self.context.worker_module,
            "drain",
            "--project-root",
            str(self.context.project_root),
            "--runtime-root",
            str(self.context.runtime_root),
            "--config-path",
            str(self.context.config_path),
            "--session-key",
            session_key,
        ]
        try:
            self.context.popen(
                command,
                cwd=self.context.project_root,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            session_directory = self.store._directory_from_key(session_key)
            self.notices._write_notice(
                session_directory,
                f"spawn-{int(self.context.clock() * 1_000_000)}",
                kind="failure",
                message=(
                    "Maintain accepted a response-end but could not start its "
                    f"background worker: {exc}. Completion is not claimed."
                    # 한국어: 응답 종료를 접수했지만 background worker를 시작하지
                    # 못했다: {exc}. 완료를 주장하지 않는다.
                ),
            )

    def drain(self, session_key: str) -> dict[str, Any]:
        session_directory = self.store._directory_from_key(session_key)
        self.context.validate_config()
        summary = {
            "session_key": session_key,
            "processed": 0,
            "failed": 0,
            "already_resolved": 0,
            "blocked": 0,
            "busy": False,
        }
        with self.store._drain_lock(session_directory):
            with self.store._state_lock(session_directory):
                state = self.store._read_session_state(session_directory)
                events = self.store._events(session_directory)
            blocked_generations: set[int] = set()
            for turn_key, event in events:
                binding = _binding_snapshot(
                    event, state, "Maintain runtime response-end event"
                )
                workspace_id = binding["workspace_id"]
                generation = binding["generation"]
                effect_path = self.store._effect_path(session_directory, turn_key)
                if effect_path.exists():
                    summary["already_resolved"] += 1
                    effect = _read_json_object(
                        effect_path, "Maintain runtime effect"
                    )
                    if (
                        effect.get("status") == "failed"
                        and self.store._effect_blocks_later_events(effect)
                    ):
                        blocked_generations.add(generation)
                    continue
                if generation in blocked_generations:
                    summary["blocked"] += 1
                    continue
                user_prompt = event.get("user_prompt")
                turn_id = event.get("turn_id")
                main_response = event.get("main_response")
                if not all(
                    isinstance(value, str) and value.strip()
                    for value in (user_prompt, turn_id, main_response)
                ):
                    message = (
                        "Maintain could not pair a response-end with its stable "
                        "user prompt and turn_id. No completion or freshness is "
                        "claimed."
                    )
                    # 한국어: 응답 종료를 안정적인 사용자 prompt·turn_id와 짝지을 수
                    # 없었다. 완료나 최신성을 주장하지 않는다.
                    self.notices._write_notice(
                        session_directory,
                        turn_key,
                        kind="failure",
                        message=message,
                    )
                    _atomic_write_json(
                        effect_path,
                        {
                            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                            "blocks_later_events": False,
                            "status": "failed",
                            "finished_at": self.context.clock(),
                            "error": message,
                            **_snapshot_fields(binding),
                        },
                    )
                    summary["failed"] += 1
                    continue
                try:
                    session_type = self.context.session_type
                    semantic_session = session_type.restore(
                        self.context.project_root,
                        workspace_id,
                        thread_id=binding["thread_id"],
                        runner=self.context.runner,
                    )
                    decision = semantic_session.resume(
                        {
                            "workspace_id": workspace_id,
                            "turn_id": turn_id,
                            "user_prompt": user_prompt,
                            "main_response": main_response,
                        }
                    )
                    result = self.context.apply_decision(
                        self.context.project_root,
                        self.context.work_root,
                        workspace_id,
                        decision,
                    )
                    self.notices._notification_for_result(
                        session_directory, turn_key, result
                    )
                    _atomic_write_json(
                        effect_path,
                        {
                            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                            "status": "resolved",
                            "finished_at": self.context.clock(),
                            "context_status": result.get("context_status"),
                            "importance": result.get("importance"),
                            **_snapshot_fields(binding),
                        },
                    )
                    summary["processed"] += 1
                except Exception as exc:
                    message = (
                        f"Maintain failed while processing Workspace "
                        f"`{workspace_id}` response-end: {exc}. The event is "
                        "failed, not completed; inspect actual Context before "
                        "retrying."
                    )
                    # 한국어: 해당 Workspace의 응답 종료 처리에 실패했다: {exc}.
                    # 이 event는 완료가 아닌 실패이며, 재시도 전에 실제 Context를 확인한다.
                    self.notices._write_notice(
                        session_directory,
                        turn_key,
                        kind="failure",
                        message=message,
                    )
                    _atomic_write_json(
                        effect_path,
                        {
                            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                            "blocks_later_events": True,
                            "status": "failed",
                            "finished_at": self.context.clock(),
                            "error": str(exc),
                            **_snapshot_fields(binding),
                        },
                    )
                    summary["failed"] += 1
                    blocked_generations.add(generation)
        return summary
