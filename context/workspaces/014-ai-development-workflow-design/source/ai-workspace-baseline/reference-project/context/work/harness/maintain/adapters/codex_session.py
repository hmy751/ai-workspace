"""읽기 전용 Maintain 판단을 기존 Codex 세션으로 실행한다."""

from __future__ import annotations

from ..semantic.prompt import PromptBuilder
from ..resources import MAINTAIN_ROOT
from ..contracts.response import ResponseValidator

from collections.abc import Callable, Mapping, Sequence
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any, Iterator

from ...workspace_contract import (
    HarnessError,
    expect_nonempty_string,
    fail,
    validate_workspace_id,
)

CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
_THREAD_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")


def _resolve_codex_executable(value: str) -> str:
    """symlink가 함께 설치된 tool host를 가리면 실제 실행 파일 경로를 사용한다."""

    raw = expect_nonempty_string(value, "Codex executable")
    discovered = shutil.which(raw)
    if discovered is None:
        return raw
    try:
        resolved = Path(discovered).resolve(strict=True)
    except OSError:
        return raw
    sibling_host = resolved.with_name("codex-code-mode-host")
    if sibling_host.is_file() and os.access(sibling_host, os.X_OK):
        return str(resolved)
    return raw


class CodexMaintainSession:
    """최초 맥락을 구성한 뒤 같은 Codex thread에서 판단을 이어 간다."""

    def __init__(
        self,
        project_root: Path,
        workspace_id: str,
        *,
        runner: CommandRunner = subprocess.run,
        codex_executable: str = "codex",
    ) -> None:
        try:
            resolved_project_root = Path(project_root).resolve(strict=True)
        except OSError as exc:
            raise HarnessError(f"Project root is not available: {exc}") from exc
        if not resolved_project_root.is_dir():
            fail("Project root must be a directory")
        self.project_root = resolved_project_root
        self.workspace_id = validate_workspace_id(workspace_id)
        self._runner = runner
        self._codex_executable = _resolve_codex_executable(codex_executable)
        self._thread_id: str | None = None

    @classmethod
    def restore(
        cls,
        project_root: Path,
        workspace_id: str,
        *,
        thread_id: str,
        runner: CommandRunner = subprocess.run,
        codex_executable: str = "codex",
    ) -> "CodexMaintainSession":
        """검증된 thread 식별자로 판단 세션 연결을 복원한다."""

        session = cls(
            project_root,
            workspace_id,
            runner=runner,
            codex_executable=codex_executable,
        )
        session._thread_id = cls._validate_thread_id(thread_id)
        return session

    @property
    def thread_id(self) -> str | None:
        """초기 맥락 구성이 성공한 경우 검증된 thread 식별자를 반환한다."""

        return self._thread_id

    def start(
        self,
        bounded_bootstrap: Mapping[str, Any],
        *,
        output_path: Path | None = None,
    ) -> dict[str, Any]:
        """제한된 Recover 결과로 새 판단 세션의 초기 맥락을 구성한다."""

        if self._thread_id is not None:
            fail("Codex Maintain session has already been grounded")
        prompt = PromptBuilder(self.workspace_id)._grounding_prompt(bounded_bootstrap)
        schema_path = self._resource_path("grounding.schema.json")
        with self._last_message_path(output_path) as last_message_path:
            command = [
                self._codex_executable,
                "exec",
                "--json",
                "--sandbox",
                "read-only",
                "--ignore-user-config",
                *self._model_options(),
                "-C",
                str(self.project_root),
                "-c",
                "features.hooks=false",
                "--output-schema",
                str(schema_path),
                "--output-last-message",
                str(last_message_path),
                "-",
            ]
            thread_id, value = self._invoke(
                command,
                prompt,
                last_message_path,
                expected_thread_id=None,
                output_label="Maintain grounding",
            )
        ResponseValidator(self.workspace_id)._validate_grounding(value)
        self._thread_id = thread_id
        return value

    def resume(
        self,
        bounded_response_delta: Mapping[str, Any],
        *,
        output_path: Path | None = None,
    ) -> dict[str, Any]:
        """초기 맥락이 구성된 thread에 응답 종료 시점의 판단을 요청한다."""

        if self._thread_id is None:
            fail("Codex Maintain session must be grounded before resume")
        thread_id = self._thread_id
        prompt = PromptBuilder(self.workspace_id)._decision_prompt(
            bounded_response_delta
        )
        schema_path = self._resource_path("decision.schema.json")
        with self._last_message_path(output_path) as last_message_path:
            command = [
                self._codex_executable,
                "exec",
                "resume",
                thread_id,
                "--json",
                "--ignore-user-config",
                *self._model_options(),
                "-c",
                "features.hooks=false",
                "--output-schema",
                str(schema_path),
                "--output-last-message",
                str(last_message_path),
                "-",
            ]
            _, value = self._invoke(
                command,
                prompt,
                last_message_path,
                expected_thread_id=thread_id,
                output_label="Maintain decision",
            )
        ResponseValidator(self.workspace_id)._validate_decision(value)
        return value

    def _model_options(self) -> list[str]:
        """각 실행에서 수동 role과 같은 모델 설정을 읽는다."""

        try:
            import tomllib
        except ModuleNotFoundError as exc:
            raise HarnessError(
                "Codex Maintain requires Python 3.11 or newer to read its "
                "role configuration"
            ) from exc
        config_path = self._resource_path("workspace-context-maintainer.toml")
        try:
            config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            raise HarnessError(
                f"Maintain role configuration is not readable valid TOML: {exc}"
            ) from exc
        model = expect_nonempty_string(config.get("model"), "Maintain role model")
        effort = expect_nonempty_string(
            config.get("model_reasoning_effort"),
            "Maintain role model_reasoning_effort",
        )
        return [
            "--model",
            model,
            "-c",
            f"model_reasoning_effort={json.dumps(effort)}",
        ]

    def _resource_path(self, filename: str) -> Path:
        path = MAINTAIN_ROOT / filename
        if not path.is_file():
            fail(f"Maintain resource is missing: {filename}")
        return path

    @contextmanager
    def _last_message_path(self, output_path: Path | None) -> Iterator[Path]:
        if output_path is not None:
            path = Path(output_path)
            if path.exists():
                fail("temporary output path must not already exist")
            if not path.parent.is_dir():
                fail("temporary output path parent must be a directory")
            yield path
            return
        with tempfile.TemporaryDirectory(prefix="maintain-codex-") as temp_dir:
            yield Path(temp_dir) / "last-message.json"

    def _invoke(
        self,
        command: Sequence[str],
        prompt: str,
        last_message_path: Path,
        *,
        expected_thread_id: str | None,
        output_label: str,
    ) -> tuple[str, dict[str, Any]]:
        try:
            completed = self._runner(
                list(command),
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise HarnessError(f"Codex command failed to run: {exc}") from exc
        if completed.returncode != 0:
            stderr = (completed.stderr or "").strip()
            detail = f": {stderr}" if stderr else ""
            fail(f"Codex command failed with exit {completed.returncode}{detail}")
        thread_id = self._parse_thread_id(completed.stdout or "", expected_thread_id)
        try:
            raw_last_message = last_message_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise HarnessError(
                f"{output_label} last message is unavailable: {exc}"
            ) from exc
        try:
            value = json.loads(raw_last_message)
        except json.JSONDecodeError as exc:
            raise HarnessError(
                f"{output_label} last message is not valid JSON: {exc}"
            ) from exc
        if not isinstance(value, dict):
            fail(f"{output_label} last message must be a JSON object")
        return thread_id, value

    @staticmethod
    def _parse_thread_id(stdout: str, expected_thread_id: str | None) -> str:
        thread_ids: list[str] = []
        for line_number, raw_line in enumerate(stdout.splitlines(), start=1):
            if not raw_line.strip():
                continue
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise HarnessError(
                    "Codex JSONL contains invalid JSON at line " f"{line_number}: {exc}"
                ) from exc
            if not isinstance(event, dict):
                fail(f"Codex JSONL event at line {line_number} is not an object")
            if event.get("type") != "thread.started":
                continue
            thread_id = event.get("thread_id")
            try:
                validated_thread_id = CodexMaintainSession._validate_thread_id(
                    thread_id
                )
            except HarnessError as exc:
                raise HarnessError(
                    "Codex thread.started event has no valid thread_id"
                ) from exc
            thread_ids.append(validated_thread_id)
        if not thread_ids:
            fail("Codex JSONL is missing thread.started")
        if len(set(thread_ids)) != 1:
            fail("Codex JSONL contains mismatched thread ids")
        thread_id = thread_ids[0]
        if expected_thread_id is not None and thread_id != expected_thread_id:
            fail(
                "resumed Codex thread id does not match the grounded thread: "
                f"expected {expected_thread_id!r}, got {thread_id!r}"
            )
        return thread_id

    @staticmethod
    def _validate_thread_id(value: Any) -> str:
        thread_id = expect_nonempty_string(value, "Codex thread id")
        if not _THREAD_ID_PATTERN.fullmatch(thread_id):
            fail("Codex thread id contains unsupported characters")
        return thread_id
