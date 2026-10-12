"""검증 명령을 shell 없이 실행하고 제한된 결과를 반환한다."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import threading
import time
from typing import Any

from ..workspace.validation import fail
from .output import BoundedStreamCapture, PROJECT_ROOT_TOKEN, capture_result
from .process_scope import wait_for_verification_scope

TIMEOUT_EXIT_CODE = 124
OUTPUT_DRAIN_GRACE_SECONDS = 1.0


def run_bounded_verification(
    argv: list[str],
    project_root: Path,
    timeout_seconds: float,
    max_output_chars: int,
) -> dict[str, Any]:
    project_root_prefix = str(project_root.resolve(strict=True))
    stdout_capture = BoundedStreamCapture(max_output_chars, project_root_prefix)
    stderr_capture = BoundedStreamCapture(max_output_chars, project_root_prefix)
    timed_out = False
    process_returncode: int | None = None

    try:
        process = subprocess.Popen(
            argv,
            cwd=project_root,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=(os.name == "posix"),
        )
    except OSError as exc:
        exit_code = 127
        stderr_capture.add(f"could not execute verification argv: {exc}\n")
        stderr_capture.finish()
    else:
        if process.stdout is None or process.stderr is None:
            fail("verification process did not expose stdout and stderr pipes")
        stdout_thread = threading.Thread(
            target=stdout_capture.drain, args=(process.stdout,), daemon=True
        )
        stderr_thread = threading.Thread(
            target=stderr_capture.drain, args=(process.stderr,), daemon=True
        )
        stdout_thread.start()
        stderr_thread.start()
        timed_out = wait_for_verification_scope(process, timeout_seconds)
        process_returncode = process.returncode
        drain_deadline = time.monotonic() + OUTPUT_DRAIN_GRACE_SECONDS
        stdout_thread.join(timeout=max(0.0, drain_deadline - time.monotonic()))
        stderr_thread.join(timeout=max(0.0, drain_deadline - time.monotonic()))
        if stdout_thread.is_alive():
            stdout_capture.read_error = "stdout pipe did not close after process exit"
        if stderr_thread.is_alive():
            stderr_capture.read_error = "stderr pipe did not close after process exit"
        exit_code = TIMEOUT_EXIT_CODE if timed_out else process.returncode

    stdout, stdout_metadata, stdout_replacements = capture_result(stdout_capture)
    stderr, stderr_metadata, stderr_replacements = capture_result(stderr_capture)
    return {
        "exit_code": exit_code,
        "process_returncode": process_returncode,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "output_capture": {
            "encoding": "utf-8",
            "errors": "replace",
            "limit_unit": "characters",
            "max_chars_per_stream": max_output_chars,
            "stdout": stdout_metadata,
            "stderr": stderr_metadata,
        },
        "normalization": {
            "output_root_token": PROJECT_ROOT_TOKEN,
            "stdout_replacements": stdout_replacements,
            "stderr_replacements": stderr_replacements,
        },
    }
