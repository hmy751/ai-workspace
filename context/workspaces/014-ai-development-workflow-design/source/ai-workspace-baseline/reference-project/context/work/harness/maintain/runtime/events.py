"""정규화된 hook의 prompt·response 연결과 접수를 소유한다."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ...workspace_contract import expect_nonempty_string, fail
from .context import RuntimeContext
from .notices import NoticeService
from .storage import RuntimeStore
from .worker import DrainWorker
from .state import (
    MAINTAIN_HOST_STATE_SCHEMA_VERSION,
    _HEX_DIGEST,
    _HOOK_EVENTS,
    _current_binding,
    _binding_snapshot,
    _snapshot_fields,
)
from .storage_io import _hash_identifier, _atomic_write_json, _read_json_object
from ..adapters.events import _hook_output


class EventIntake:
    """정규화된 hook의 prompt·response 연결과 접수."""

    def __init__(
        self,
        context: RuntimeContext,
        notices: NoticeService,
        store: RuntimeStore,
        worker: DrainWorker,
    ) -> None:
        self.context = context
        self.notices = notices
        self.store = store
        self.worker = worker

    @staticmethod
    def _payload_string(payload: Mapping[str, Any], key: str) -> str:
        if not isinstance(payload, Mapping):
            fail("Maintain hook input must be a JSON object")
        return expect_nonempty_string(payload.get(key), f"Maintain hook {key}")

    @staticmethod
    def _check_event(payload: Mapping[str, Any], command: str) -> None:
        actual = payload.get("hook_event_name")
        if actual is not None and actual != _HOOK_EVENTS[command]:
            fail(
                f"{command} received hook_event_name {actual!r}; expected "
                f"{_HOOK_EVENTS[command]!r}"
            )

    def session_start(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "session-start")
        session_id = self._payload_string(payload, "session_id")
        self.context.validate_config()
        session_directory = self.store._session_directory(session_id)
        state_path = session_directory / "session.json"
        if not session_directory.exists() or not state_path.exists():
            return _hook_output("SessionStart")
        with self.store._state_lock(session_directory):
            if not state_path.exists():
                return _hook_output("SessionStart")
            state = self.store._read_session_state(session_directory)
            current = _current_binding(state)
        if current is None:
            return _hook_output("SessionStart")
        return _hook_output(
            "SessionStart",
            additional_context=(
                "Workspace Maintain is reusing the already-grounded session "
                f"binding generation {current['generation']} for explicit "
                f"Workspace `{current['workspace_id']}`. No new Context "
                "update or freshness claim was made."
                # 한국어: 명시된 Workspace에 이미 초기 맥락을 정립한 세션 연결의
                # 해당 generation을 재사용한다. 새 Context 갱신이나 최신성 주장은 없다.
            ),
        )

    def user_prompt(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "user-prompt")
        session_id = self._payload_string(payload, "session_id")
        turn_id = self._payload_string(payload, "turn_id")
        prompt = self._payload_string(payload, "prompt")
        self.context.validate_config()
        session_directory = self.store._session_directory(session_id)
        turn_key = _hash_identifier(turn_id)
        state_path = session_directory / "session.json"
        if not session_directory.exists() or not state_path.exists():
            return _hook_output("UserPromptSubmit")

        with self.store._state_lock(session_directory):
            if not state_path.exists():
                return _hook_output("UserPromptSubmit")
            state = self.store._read_session_state(session_directory)
            self._fail_orphan_prompts(
                session_directory,
                state,
                exclude_turn_key=turn_key,
            )
            turn_path = self.store._turn_path(session_directory, turn_key)
            event_path = self.store._event_path(session_directory, turn_key)
            if turn_path.exists():
                existing = _read_json_object(
                    turn_path, "Maintain runtime user-prompt event"
                )
                if (
                    existing.get("turn_id") != turn_id
                    or existing.get("prompt") != prompt
                ):
                    fail("duplicate Maintain turn_id has different prompt content")
                _binding_snapshot(existing, state, "Maintain runtime user-prompt event")
            else:
                if event_path.exists():
                    event = _read_json_object(
                        event_path, "Maintain runtime response-end event"
                    )
                    binding = _binding_snapshot(
                        event, state, "Maintain runtime response-end event"
                    )
                    sequence = event.get("sequence")
                else:
                    binding = _current_binding(state)
                    if binding is None:
                        return _hook_output("UserPromptSubmit")
                    sequence = self.store._next_sequence(session_directory)
                if type(sequence) is not int or sequence < 1:
                    fail("Maintain runtime event sequence is invalid")
                _atomic_write_json(
                    turn_path,
                    {
                        "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                        "sequence": sequence,
                        "turn_id": turn_id,
                        "prompt": prompt,
                        "received_at": self.context.clock(),
                        **_snapshot_fields(binding),
                    },
                )
                if event_path.exists():
                    if event.get("turn_id") != turn_id:
                        fail("Maintain runtime response-end turn binding changed")
                    event["user_prompt"] = prompt
                    _atomic_write_json(event_path, event)
            notices = self.notices._take_notices(session_directory)
            unresolved = self.store._unresolved_event_keys(session_directory)
            blocking_failures = self.store._blocking_failure_keys(session_directory)
            runnable = self.store._runnable_unresolved_event_keys(
                session_directory, state
            )

        # worker가 중단되거나 시작 경쟁에서 놓친 event를 다시 처리한다.
        # drain 잠금과 effect 파일이 중복 실행의 순서와 이미 처리된 결과를 보호한다.
        if runnable:
            self.worker._start_detached_drain(session_directory.name)

        if not notices and not unresolved and not blocking_failures:
            return _hook_output("UserPromptSubmit")
        messages = [str(notice["message"]) for notice in notices]
        if unresolved:
            if blocking_failures and not runnable:
                messages.append(
                    f"{len(unresolved)} later Workspace Maintain response-end "
                    "boundary/boundaries remain pending behind a failed "
                    "semantic or apply boundary. They were not applied, do not "
                    "establish fresh or current Context, and will not be "
                    "retried on the affected binding generation."
                    # 한국어: 실패한 의미 판단·반영 경계 뒤에 후속 응답 종료 {건수}건이
                    # 대기 중이다. 반영되지 않았고 Context의 최신성·현재성을 보장하지
                    # 않으며, 해당 연결 generation에서는 재시도하지 않는다.
                )
            else:
                messages.append(
                    f"{len(unresolved)} previously accepted Workspace Maintain "
                    "response-end boundary/boundaries are still pending. They "
                    "are not completed and do not establish fresh or current "
                    "Context; a detached worker was started again."
                    # 한국어: 이전에 접수한 응답 종료 {건수}건이 아직 대기 중이다.
                    # 완료나 Context의 최신성·현재성을 보장하지 않는다. 별도로 실행되는
                    # worker를 다시 시작했다.
                )
        elif blocking_failures:
            messages.append(
                "Automatic Workspace Maintain is paused on at least one binding "
                "generation after a failed semantic or apply boundary. No later "
                "Context freshness is claimed for that generation."
                # 한국어: 의미 판단·반영 경계의 실패로 하나 이상의 연결 generation에서
                # 자동 Maintain이 중단됐다. 해당 generation의 이후 Context 최신성은
                # 주장하지 않는다.
            )
        context = (
            "Previous Workspace Maintain results requiring attention:\n- "
            # 한국어: 주의가 필요한 이전 Workspace Maintain 결과:
            + "\n- ".join(messages)
        )
        return _hook_output(
            "UserPromptSubmit",
            additional_context=context,
            system_message=(
                "Workspace Maintain has a previous result or pending boundary "
                "requiring attention."
                # 한국어: 주의가 필요한 이전 결과 또는 대기 중인 처리 경계가 있다.
            ),
        )

    def response_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "response-end")
        session_id = self._payload_string(payload, "session_id")
        turn_id = self._payload_string(payload, "turn_id")
        main_response = self._payload_string(payload, "last_assistant_message")
        self.context.validate_config()
        session_directory = self.store._session_directory(session_id)
        session_key = session_directory.name
        turn_key = _hash_identifier(turn_id)
        state_path = session_directory / "session.json"
        if not session_directory.exists() or not state_path.exists():
            return _hook_output("Stop")

        with self.store._state_lock(session_directory):
            if not state_path.exists():
                return _hook_output("Stop")
            state = self.store._read_session_state(session_directory)
            turn_path = self.store._turn_path(session_directory, turn_key)
            event_path = self.store._event_path(session_directory, turn_key)
            existing_event: dict[str, Any] | None = None
            if event_path.exists():
                existing_event = _read_json_object(
                    event_path, "Maintain runtime response-end event"
                )
            if turn_path.exists():
                turn = _read_json_object(
                    turn_path, "Maintain runtime user-prompt event"
                )
                if turn.get("turn_id") != turn_id:
                    fail("Maintain runtime prompt turn binding changed")
                sequence = turn.get("sequence")
                user_prompt = turn.get("prompt")
                binding = _binding_snapshot(
                    turn, state, "Maintain runtime user-prompt event"
                )
                if existing_event is not None:
                    existing_binding = _binding_snapshot(
                        existing_event,
                        state,
                        "Maintain runtime response-end event",
                    )
                    if existing_binding != binding:
                        fail("Maintain runtime prompt and response binding changed")
            elif existing_event is not None:
                sequence = existing_event.get("sequence")
                user_prompt = existing_event.get("user_prompt")
                binding = _binding_snapshot(
                    existing_event,
                    state,
                    "Maintain runtime response-end event",
                )
            else:
                # turn 중간 activation은 다음 prompt부터 적용한다.
                # 새 상태는 대응 prompt가 있는 응답만 접수하고, legacy v1의 응답 단독
                # 실패 기록 동작은 호환을 위해 유지한다.
                if not state["legacy"]:
                    return _hook_output("Stop")
                binding = _current_binding(state)
                if binding is None:
                    return _hook_output("Stop")
                sequence = self.store._next_sequence(session_directory)
                user_prompt = None
            if type(sequence) is not int or sequence < 1:
                fail("Maintain runtime turn sequence is invalid")
            event = {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "sequence": sequence,
                "turn_id": turn_id,
                "user_prompt": user_prompt,
                "main_response": main_response,
                "accepted_at": self.context.clock(),
                **_snapshot_fields(binding),
            }
            if existing_event is not None:
                stable_existing = {
                    key: existing_event.get(key)
                    for key in (
                        "sequence",
                        "turn_id",
                        "user_prompt",
                        "main_response",
                    )
                }
                stable_event = {
                    key: event[key]
                    for key in (
                        "sequence",
                        "turn_id",
                        "user_prompt",
                        "main_response",
                    )
                }
                if stable_existing != stable_event:
                    fail("duplicate Maintain response-end has different content")
            else:
                _atomic_write_json(event_path, event)
            runnable = self.store._runnable_unresolved_event_keys(
                session_directory, state
            )

        if runnable:
            self.worker._start_detached_drain(session_key)
        return _hook_output("Stop")

    def session_end(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        self._check_event(payload, "session-end")
        session_id = self._payload_string(payload, "session_id")
        self.context.validate_config()
        session_directory = self.store._session_directory(session_id)
        session_key = session_directory.name
        state_path = session_directory / "session.json"
        if not session_directory.exists() or not state_path.exists():
            return _hook_output("SessionEnd")

        with self.store._state_lock(session_directory):
            if not state_path.exists():
                return _hook_output("SessionEnd")
            state = self.store._read_session_state(session_directory)
            orphaned = self._fail_orphan_prompts(session_directory, state)
            unresolved = self.store._unresolved_event_keys(session_directory)
            failed = self.store._failed_effect_keys(session_directory)
            blocking_failures = self.store._blocking_failure_keys(session_directory)
            runnable = self.store._runnable_unresolved_event_keys(
                session_directory, state
            )
            notices = self.notices._take_notices(session_directory)
            _atomic_write_json(
                session_directory / "session-end.json",
                {
                    "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                    "ended_at": self.context.clock(),
                    "blocking_failure_keys": blocking_failures,
                    "failed_effect_keys": failed,
                    "orphan_prompt_keys": orphaned,
                    "surfaced_notice_count": len(notices),
                    "unresolved_event_keys": unresolved,
                },
            )
        if runnable:
            self.worker._start_detached_drain(session_key)
        if unresolved or orphaned or failed or notices:
            status_message = (
                f"Maintain session ended with {len(orphaned)} prompt(s) missing "
                f"a response-end and {len(unresolved)} accepted response-end "
                f"event(s) not yet resolved; {len(failed)} effect(s) are "
                "failed, not completed. Completion or freshness is not claimed."
            )
            # 한국어: 세션이 끝났으며 응답 종료가 없는 prompt {건수}건, 아직 해결되지
            # 않은 접수 event {건수}건이 있다. effect {건수}건은 완료가 아닌 실패다.
            # 완료나 최신성을 주장하지 않는다.
            if runnable:
                status_message += (
                    " A best-effort worker was started for accepted "
                    "response-end events."
                )
                # 한국어: 접수된 응답 종료 event 처리를 가능한 범위에서 시도하는
                # worker를 시작했다.
            elif unresolved:
                status_message += (
                    " Later events remain pending behind a failed semantic or "
                    "apply boundary on their binding generation and were not "
                    "retried."
                )
                # 한국어: 후속 event는 해당 연결 generation의 실패한 의미 판단·반영
                # 경계 뒤에서 대기하며, 재시도하지 않았다.
            notice_messages = [str(notice["message"]) for notice in notices]
            message = "\n".join([status_message, *notice_messages])
            return _hook_output(
                "SessionEnd",
                additional_context=message,
                system_message=message,
            )
        return _hook_output("SessionEnd")

    def _fail_orphan_prompts(
        self,
        session_directory: Path,
        state: Mapping[str, Any],
        *,
        exclude_turn_key: str | None = None,
    ) -> list[str]:
        """대응하는 응답 없이 다음 prompt나 세션 종료로 끝난 입력을 드러낸다."""

        turns_directory = session_directory / "turns"
        if not turns_directory.exists():
            return []
        orphaned: list[str] = []
        for turn_path in sorted(turns_directory.glob("*.json")):
            turn_key = turn_path.stem
            if turn_key == exclude_turn_key:
                continue
            if not _HEX_DIGEST.fullmatch(turn_key):
                fail("Maintain runtime contains an invalid prompt filename")
            if self.store._event_path(session_directory, turn_key).exists():
                continue
            effect_path = self.store._effect_path(session_directory, turn_key)
            if effect_path.exists():
                continue
            turn = _read_json_object(turn_path, "Maintain runtime user-prompt event")
            binding = _binding_snapshot(
                turn, state, "Maintain runtime user-prompt event"
            )
            turn_id = turn.get("turn_id")
            message = (
                f"Maintain received prompt turn `{turn_id}` without a matching "
                "response-end before the session advanced. That boundary is "
                "failed and no completion or freshness is claimed."
            )
            # 한국어: 해당 turn의 prompt를 받았지만 세션이 진행되기 전에 대응하는
            # 응답 종료를 받지 못했다. 이 경계는 실패이며 완료나 최신성을 주장하지 않는다.
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
                    "error": "prompt_without_response_end",
                    **_snapshot_fields(binding),
                },
            )
            orphaned.append(turn_key)
        return orphaned
