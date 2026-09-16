"""런타임 파일·잠금·순서와 상태 조회를 소유한다."""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import contextmanager
import fcntl
import os
from pathlib import Path
from typing import Any, Iterator

from ...workspace_contract import (
    HarnessError,
    expect_exact_keys,
    expect_schema_version,
    fail,
)
from .context import RuntimeContext
from .state import (
    MAINTAIN_HOST_STATE_SCHEMA_VERSION,
    _LEGACY_HOST_STATE_SCHEMA_VERSION,
    _SESSION_V1_KEYS,
    _SESSION_V2_KEYS,
    _HEX_DIGEST,
    _validated_binding,
    _binding_snapshot,
)
from .storage_io import (
    _hash_identifier,
    _reject_existing_symlink_components,
    _atomic_write_json,
    _read_json_object,
)


class RuntimeStore:
    """런타임 파일·잠금·순서와 상태 조회."""

    def __init__(self, context: RuntimeContext) -> None:
        self.context = context

    def _session_directory(self, session_id: str) -> Path:
        path = self.context.runtime_root / _hash_identifier(session_id)
        self._validate_runtime_path(path, "Maintain runtime session directory")
        return path

    def _directory_from_key(self, session_key: str) -> Path:
        if not _HEX_DIGEST.fullmatch(session_key):
            fail("Maintain runtime session key must be a SHA-256 digest")
        path = self.context.runtime_root / session_key
        self._validate_runtime_path(path, "Maintain runtime session directory")
        return path

    def _validate_runtime_path(self, path: Path, label: str) -> None:
        if not path.is_absolute() or ".." in path.parts:
            fail(f"{label} must be an absolute lexical descendant of the Project")
        try:
            relative = path.relative_to(self.context.project_root)
        except ValueError as exc:
            raise HarnessError(f"{label} must stay inside the Project root") from exc
        if not relative.parts:
            fail(f"{label} must be below the Project root")
        current = self.context.project_root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                fail(f"{label} must not use symlink components")
            if current.exists() and not current.is_dir():
                fail(f"{label} components must be directories")

    def _prepare_session_directory(self, session_directory: Path) -> None:
        self._validate_runtime_path(self.context.runtime_root, "Maintain runtime root")
        self._validate_runtime_path(
            session_directory, "Maintain runtime session directory"
        )
        try:
            session_directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise HarnessError(
                f"Maintain runtime session directory is unavailable: {exc}"
            ) from exc
        self._validate_runtime_path(self.context.runtime_root, "Maintain runtime root")
        self._validate_runtime_path(
            session_directory, "Maintain runtime session directory"
        )

    @contextmanager
    def _state_lock(self, session_directory: Path) -> Iterator[None]:
        self._prepare_session_directory(session_directory)
        lock_path = session_directory / ".state.lock"
        _reject_existing_symlink_components(lock_path, "Maintain state lock")
        descriptor = os.open(
            lock_path,
            os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    @contextmanager
    def _drain_lock(self, session_directory: Path) -> Iterator[None]:
        self._prepare_session_directory(session_directory)
        lock_path = session_directory / ".drain.lock"
        _reject_existing_symlink_components(lock_path, "Maintain drain lock")
        descriptor = os.open(
            lock_path,
            os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        try:
            # drain은 별도 worker에서만 실행하며 잠금을 기다린다.
            # 잠금 대기 없이 종료하면 첫 worker의 snapshot 이후 접수된 event가
            # 처리되지 않은 채 남을 수 있다.
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def _read_session_state(self, session_directory: Path) -> dict[str, Any]:
        path = session_directory / "session.json"
        value = _read_json_object(path, "Maintain runtime session state")
        schema_version = value.get("schema_version")
        if schema_version == _LEGACY_HOST_STATE_SCHEMA_VERSION:
            expect_exact_keys(
                value, _SESSION_V1_KEYS, "Maintain runtime session state"
            )
            expect_schema_version(
                schema_version,
                _LEGACY_HOST_STATE_SCHEMA_VERSION,
                "Maintain runtime session state",
            )
            binding = _validated_binding(
                {
                    "generation": 1,
                    "workspace_id": value["workspace_id"],
                    "thread_id": value["thread_id"],
                    "grounded_at": value["grounded_at"],
                }
            )
            return {
                "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
                "current_generation": 1,
                "bindings": [binding],
                "legacy": True,
            }

        expect_exact_keys(
            value, _SESSION_V2_KEYS, "Maintain runtime session state"
        )
        expect_schema_version(
            schema_version,
            MAINTAIN_HOST_STATE_SCHEMA_VERSION,
            "Maintain runtime session state",
        )
        raw_bindings = value["bindings"]
        if not isinstance(raw_bindings, list) or not raw_bindings:
            fail("Maintain runtime bindings must be a non-empty list")
        bindings = [_validated_binding(item) for item in raw_bindings]
        generations = [item["generation"] for item in bindings]
        if len(set(generations)) != len(generations):
            fail("Maintain runtime binding generations must be unique")
        if generations != sorted(generations):
            fail("Maintain runtime bindings must be ordered by generation")
        current_generation = value["current_generation"]
        if current_generation is not None and (
            type(current_generation) is not int
            or current_generation not in generations
        ):
            fail(
                "Maintain runtime current_generation must name a persisted "
                "binding or be null"
            )
        return {
            "schema_version": MAINTAIN_HOST_STATE_SCHEMA_VERSION,
            "current_generation": current_generation,
            "bindings": bindings,
            "legacy": False,
        }

    def _next_sequence(self, session_directory: Path) -> int:
        path = session_directory / "next-sequence.json"
        if path.exists():
            value = _read_json_object(path, "Maintain runtime sequence state")
            expect_exact_keys(value, {"next"}, "Maintain runtime sequence state")
            next_value = value["next"]
            if type(next_value) is not int or next_value < 1:
                fail("Maintain runtime next sequence must be a positive integer")
        else:
            next_value = 1
        _atomic_write_json(path, {"next": next_value + 1})
        return next_value

    @staticmethod
    def _turn_path(session_directory: Path, turn_key: str) -> Path:
        return session_directory / "turns" / f"{turn_key}.json"

    @staticmethod
    def _event_path(session_directory: Path, turn_key: str) -> Path:
        return session_directory / "events" / f"{turn_key}.json"

    @staticmethod
    def _effect_path(session_directory: Path, turn_key: str) -> Path:
        return session_directory / "effects" / f"{turn_key}.json"

    def _events(self, session_directory: Path) -> list[tuple[str, dict[str, Any]]]:
        events_directory = session_directory / "events"
        if not events_directory.exists():
            return []
        events: list[tuple[str, dict[str, Any]]] = []
        for path in events_directory.glob("*.json"):
            turn_key = path.stem
            if not _HEX_DIGEST.fullmatch(turn_key):
                fail("Maintain runtime contains an invalid event filename")
            event = _read_json_object(path, "Maintain runtime response-end event")
            sequence = event.get("sequence")
            if type(sequence) is not int or sequence < 1:
                fail("Maintain runtime event sequence is invalid")
            events.append((turn_key, event))
        events.sort(key=lambda item: (item[1]["sequence"], item[0]))
        return events

    def _unresolved_event_keys(self, session_directory: Path) -> list[str]:
        return [
            turn_key
            for turn_key, _ in self._events(session_directory)
            if not self._effect_path(session_directory, turn_key).exists()
        ]

    def _failed_effect_keys(self, session_directory: Path) -> list[str]:
        effects_directory = session_directory / "effects"
        if not effects_directory.exists():
            return []
        failed: list[str] = []
        for path in sorted(effects_directory.glob("*.json")):
            if not _HEX_DIGEST.fullmatch(path.stem):
                fail("Maintain runtime contains an invalid effect filename")
            effect = _read_json_object(path, "Maintain runtime effect")
            if effect.get("status") == "failed":
                failed.append(path.stem)
        return failed

    @staticmethod
    def _effect_blocks_later_events(effect: Mapping[str, Any]) -> bool:
        if "blocks_later_events" not in effect:
            # 이전 v1 effect에는 연결 실패와 판단·반영 실패의 구분이 없다.
            # 불확실한 판단 세션에서 후속 변경을 적용하지 않도록 기존 실패는 차단한다.
            return effect.get("status") == "failed"
        blocks_later = effect.get("blocks_later_events")
        if type(blocks_later) is not bool:
            fail("Maintain runtime effect blocking flag must be boolean")
        return blocks_later

    def _blocking_failure_keys(self, session_directory: Path) -> list[str]:
        blocking: list[str] = []
        for turn_key, _ in self._events(session_directory):
            effect_path = self._effect_path(session_directory, turn_key)
            if not effect_path.exists():
                continue
            effect = _read_json_object(
                effect_path, "Maintain runtime effect"
            )
            if (
                effect.get("status") == "failed"
                and self._effect_blocks_later_events(effect)
            ):
                blocking.append(turn_key)
        return blocking

    def _blocking_generations(
        self,
        session_directory: Path,
        state: Mapping[str, Any],
    ) -> set[int]:
        blocking: set[int] = set()
        for turn_key, event in self._events(session_directory):
            effect_path = self._effect_path(session_directory, turn_key)
            if not effect_path.exists():
                continue
            effect = _read_json_object(
                effect_path, "Maintain runtime effect"
            )
            if (
                effect.get("status") == "failed"
                and self._effect_blocks_later_events(effect)
            ):
                binding = _binding_snapshot(
                    event, state, "Maintain runtime response-end event"
                )
                blocking.add(binding["generation"])
        return blocking

    def _runnable_unresolved_event_keys(
        self,
        session_directory: Path,
        state: Mapping[str, Any],
    ) -> list[str]:
        blocked_generations = self._blocking_generations(
            session_directory, state
        )
        runnable: list[str] = []
        for turn_key, event in self._events(session_directory):
            if self._effect_path(session_directory, turn_key).exists():
                continue
            binding = _binding_snapshot(
                event, state, "Maintain runtime response-end event"
            )
            if binding["generation"] not in blocked_generations:
                runnable.append(turn_key)
        return runnable
