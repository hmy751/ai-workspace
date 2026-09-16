"""쓰기 없는 binding·event 상태 조회를 소유한다."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ...workspace_contract import HarnessError, expect_nonempty_string, fail
from .context import RuntimeContext
from .storage import RuntimeStore
from .state import (
    MAINTAIN_HOST_STATE_SCHEMA_VERSION,
    _BINDING_SNAPSHOT_KEYS,
    _STATUS_SNAPSHOT_ATTEMPTS,
    _HEX_DIGEST,
    _current_binding,
    _binding_snapshot,
    _snapshot_fields,
)
from .storage_io import _read_json_object


class StatusReader:
    """쓰기 없는 binding·event 상태 조회."""

    def __init__(self, context: RuntimeContext, store: RuntimeStore) -> None:
        self.context = context
        self.store = store

    def status(self, session_id: str) -> dict[str, Any]:
        """런타임 파일을 생성하지 않고 Main session의 연결 상태를 읽는다."""

        self.context.validate_config()
        session_id = expect_nonempty_string(session_id, "Maintain session id")
        session_directory = self.store._session_directory(session_id)
        state_path = session_directory / "session.json"
        if not session_directory.exists() or not state_path.exists():
            return {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "status": "unbound",
                "session_id": session_id,
                "current_binding": None,
                "bindings": [],
                "runtime": self._empty_runtime_status(),
            }
        # 상태 파일은 원자적으로 교체되므로 조회 과정에서 lock 파일을 만들지 않는다.
        # 조회 전후의 session을 대조해 새 generation을 과거 binding으로 해석하지 않는다.
        state, runtime = self._stable_status_snapshot(session_directory)
        current = _current_binding(state)
        bindings = [
            _snapshot_fields(binding) | {"grounded_at": binding["grounded_at"]}
            for binding in state["bindings"]
        ]
        return {
            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
            "status": "active" if current is not None else "unbound",
            "session_id": session_id,
            "current_binding": (
                _snapshot_fields(current) if current is not None else None
            ),
            "bindings": bindings,
            "runtime": runtime,
        }

    def _stable_status_snapshot(
        self, session_directory: Path
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        for _ in range(_STATUS_SNAPSHOT_ATTEMPTS):
            before = self.store._read_session_state(session_directory)
            try:
                runtime = self._runtime_status(session_directory, before)
            except HarnessError:
                after = self.store._read_session_state(session_directory)
                if after != before:
                    continue
                raise
            after = self.store._read_session_state(session_directory)
            if after == before:
                return before, runtime
        fail(
            "Maintain runtime changed repeatedly while status was taking a "
            "read-only snapshot; retry status"
        )

    @staticmethod
    def _empty_runtime_status() -> dict[str, Any]:
        return {
            "unresolved_event_count": 0,
            "unresolved_event_keys": [],
            "runnable_event_count": 0,
            "runnable_event_keys": [],
            "failed_effect_count": 0,
            "failed_effect_keys": [],
            "unassigned_failed_effect_count": 0,
            "unassigned_failed_effect_keys": [],
            "blocking_failure_count": 0,
            "blocking_failure_keys": [],
            "open_prompt_count": 0,
            "open_prompt_keys": [],
            "by_generation": [],
        }

    def _runtime_status(
        self,
        session_directory: Path,
        state: Mapping[str, Any],
    ) -> dict[str, Any]:
        events = self.store._events(session_directory)
        blocking_failure_keys = self.store._blocking_failure_keys(session_directory)
        blocking_failure_set = set(blocking_failure_keys)
        blocked_generations: set[int] = set()
        event_generations: dict[str, int] = {}
        for turn_key, event in events:
            binding = _binding_snapshot(
                event, state, "Maintain runtime response-end event"
            )
            event_generations[turn_key] = binding["generation"]
            if turn_key in blocking_failure_set:
                blocked_generations.add(binding["generation"])

        unresolved_event_keys = [
            turn_key
            for turn_key, _ in events
            if not self.store._effect_path(session_directory, turn_key).exists()
        ]
        runnable_event_keys = [
            turn_key
            for turn_key in unresolved_event_keys
            if event_generations[turn_key] not in blocked_generations
        ]
        failed_effect_keys = self.store._failed_effect_keys(session_directory)
        failed_effect_generations: dict[str, int] = {}
        unassigned_failed_effect_keys: list[str] = []
        for turn_key in failed_effect_keys:
            if turn_key in event_generations:
                failed_effect_generations[turn_key] = event_generations[turn_key]
                continue
            effect_path = self.store._effect_path(session_directory, turn_key)
            effect = _read_json_object(
                effect_path, "Maintain runtime effect"
            )
            snapshot_present = [
                key in effect for key in _BINDING_SNAPSHOT_KEYS
            ]
            if any(snapshot_present):
                binding = _binding_snapshot(
                    effect, state, "Maintain runtime effect"
                )
                failed_effect_generations[turn_key] = binding["generation"]
                continue
            turn_path = self.store._turn_path(session_directory, turn_key)
            if turn_path.exists():
                turn = _read_json_object(
                    turn_path, "Maintain runtime user-prompt event"
                )
                binding = _binding_snapshot(
                    turn, state, "Maintain runtime user-prompt event"
                )
                failed_effect_generations[turn_key] = binding["generation"]
                continue
            unassigned_failed_effect_keys.append(turn_key)

        open_prompt_keys: list[str] = []
        open_prompt_generations: dict[str, int] = {}
        turns_directory = session_directory / "turns"
        if turns_directory.exists():
            for path in sorted(turns_directory.glob("*.json")):
                turn_key = path.stem
                if not _HEX_DIGEST.fullmatch(turn_key):
                    fail("Maintain runtime contains an invalid prompt filename")
                if self.store._event_path(session_directory, turn_key).exists():
                    continue
                if self.store._effect_path(session_directory, turn_key).exists():
                    continue
                turn = _read_json_object(
                    path, "Maintain runtime user-prompt event"
                )
                binding = _binding_snapshot(
                    turn, state, "Maintain runtime user-prompt event"
                )
                open_prompt_keys.append(turn_key)
                open_prompt_generations[turn_key] = binding["generation"]

        by_generation: list[dict[str, Any]] = []
        for binding in state["bindings"]:
            generation = binding["generation"]
            generation_events = [
                key
                for key, event_generation in event_generations.items()
                if event_generation == generation
            ]
            generation_failed = [
                key
                for key, effect_generation in failed_effect_generations.items()
                if effect_generation == generation
            ]
            generation_blocking = [
                key for key in generation_events if key in blocking_failure_set
            ]
            generation_unresolved = [
                key for key in unresolved_event_keys if key in generation_events
            ]
            generation_runnable = [
                key for key in runnable_event_keys if key in generation_events
            ]
            generation_open = [
                key
                for key, prompt_generation in open_prompt_generations.items()
                if prompt_generation == generation
            ]
            by_generation.append(
                {
                    **_snapshot_fields(binding),
                    "unresolved_event_count": len(generation_unresolved),
                    "runnable_event_count": len(generation_runnable),
                    "failed_effect_count": len(generation_failed),
                    "blocking_failure_count": len(generation_blocking),
                    "open_prompt_count": len(generation_open),
                }
            )

        return {
            "unresolved_event_count": len(unresolved_event_keys),
            "unresolved_event_keys": unresolved_event_keys,
            "runnable_event_count": len(runnable_event_keys),
            "runnable_event_keys": runnable_event_keys,
            "failed_effect_count": len(failed_effect_keys),
            "failed_effect_keys": failed_effect_keys,
            "unassigned_failed_effect_count": len(
                unassigned_failed_effect_keys
            ),
            "unassigned_failed_effect_keys": unassigned_failed_effect_keys,
            "blocking_failure_count": len(blocking_failure_keys),
            "blocking_failure_keys": blocking_failure_keys,
            "open_prompt_count": len(open_prompt_keys),
            "open_prompt_keys": open_prompt_keys,
            "by_generation": by_generation,
        }
