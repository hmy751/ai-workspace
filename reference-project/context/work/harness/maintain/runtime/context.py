"""런타임에 주입하는 경로·실행 의존성. 도구 선택은 연결 코드가 담당한다."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable
from typing import Any

from ..semantic.session import SemanticSessionFactory
from ...workspace_contract import (
    expect_exact_keys,
    expect_schema_version,
    validate_workspace_id,
    expect_nonempty_string,
    fail,
)
from .storage_io import _read_json_object
from .state import (
    MAINTAIN_HOST_CONFIG_SCHEMA_VERSION,
    _LEGACY_HOST_CONFIG_SCHEMA_VERSION,
    _CONFIG_V1_KEYS,
    _CONFIG_V2_KEYS,
)


@dataclass
class RuntimeContext:
    project_root: Path
    work_root: Path
    runtime_root: Path
    config_path: Path
    worker_module: str
    session_type: SemanticSessionFactory
    runner: Callable[..., Any]
    popen: Callable[..., Any]
    clock: Callable[[], float]
    python_executable: str
    bootstrap: Callable[..., dict[str, Any]]
    apply_decision: Callable[..., dict[str, Any]]

    def validate_config(self) -> None:
        path = self.config_path
        value = _read_json_object(path, "Maintain host configuration")
        schema_version = value.get("schema_version")
        if schema_version == _LEGACY_HOST_CONFIG_SCHEMA_VERSION:
            # v1 설정은 기존 연결의 이관을 위해 읽기만 지원한다.
            # 기존 workspace_id로 새 session을 자동 연결하지 않는다.
            expect_exact_keys(value, _CONFIG_V1_KEYS, "Maintain host configuration")
            expect_schema_version(
                schema_version,
                _LEGACY_HOST_CONFIG_SCHEMA_VERSION,
                "Maintain host configuration",
            )
            validate_workspace_id(value["workspace_id"])
            return
        expect_exact_keys(value, _CONFIG_V2_KEYS, "Maintain host configuration")
        expect_schema_version(
            schema_version,
            MAINTAIN_HOST_CONFIG_SCHEMA_VERSION,
            "Maintain host configuration",
        )
        mode = expect_nonempty_string(value["mode"], "Maintain host configuration mode")
        if mode != "explicit":
            fail("Maintain host configuration mode must be 'explicit'")
