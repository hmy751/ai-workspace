"""출력을 계속 비우되 root를 정규화한 제한된 앞부분만 보존한다."""

from __future__ import annotations

from typing import Any

# 저장된 receipt와의 호환성을 위해 Project root 정규화 토큰을 유지한다.
PROJECT_ROOT_TOKEN = "<OUTPUT_ROOT>"


class BoundedStreamCapture:
    """출력을 비우고 정규화하며 제한된 텍스트 앞부분만 보존한다."""

    def __init__(self, max_chars: int, project_root_prefix: str) -> None:
        self.max_chars = max_chars
        self.project_root_prefix = project_root_prefix
        self.observed_chars = 0
        self.normalized_chars = 0
        self.stored_chars = 0
        self.root_replacements = 0
        self.parts: list[str] = []
        self.pending = ""
        self.read_error: str | None = None

    def _emit(self, value: str) -> None:
        self.normalized_chars += len(value)
        remaining = self.max_chars - self.stored_chars
        if remaining <= 0:
            return
        kept = value[:remaining]
        self.parts.append(kept)
        self.stored_chars += len(kept)

    def add(self, value: str) -> None:
        self.observed_chars += len(value)
        data = self.pending + value
        safe_start_limit = max(0, len(data) - len(self.project_root_prefix) + 1)
        cursor = 0
        while cursor < safe_start_limit:
            match = data.find(self.project_root_prefix, cursor)
            if match == -1 or match >= safe_start_limit:
                self._emit(data[cursor:safe_start_limit])
                cursor = safe_start_limit
                break
            self._emit(data[cursor:match])
            self._emit(PROJECT_ROOT_TOKEN)
            self.root_replacements += 1
            cursor = match + len(self.project_root_prefix)
        self.pending = data[cursor:]

    def finish(self) -> None:
        if not self.pending:
            return
        self.root_replacements += self.pending.count(self.project_root_prefix)
        self._emit(self.pending.replace(self.project_root_prefix, PROJECT_ROOT_TOKEN))
        self.pending = ""

    def drain(self, stream: Any) -> None:
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                self.add(chunk)
        except (OSError, ValueError) as exc:
            self.read_error = str(exc)
        finally:
            self.finish()
            try:
                stream.close()
            except (OSError, ValueError):
                pass

    def prefix(self) -> str:
        return "".join(self.parts)


def capture_result(
    capture: BoundedStreamCapture,
) -> tuple[str, dict[str, Any], int]:
    persisted = capture.prefix()
    metadata = {
        "observed_chars": capture.observed_chars,
        "persisted_chars": len(persisted),
        "truncated": capture.normalized_chars > capture.max_chars,
        "read_error": (
            capture.read_error.replace(capture.project_root_prefix, PROJECT_ROOT_TOKEN)
            if capture.read_error is not None
            else None
        ),
    }
    return persisted, metadata, capture.root_replacements
