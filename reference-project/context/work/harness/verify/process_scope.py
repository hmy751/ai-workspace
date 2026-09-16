"""검증 프로세스와 일반 POSIX descendant의 실행 시간을 제한한다."""

from __future__ import annotations

import os
import signal
import subprocess
import time

PROCESS_SCOPE_POLL_SECONDS = 0.005
PROCESS_SCOPE_CLEANUP_SECONDS = 1.0


def _posix_process_group_is_alive(process_group_id: int) -> bool:
    """검증의 POSIX process group이 아직 존재하는지 확인한다."""

    try:
        os.killpg(process_group_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # 플랫폼 정책이 신호 전달을 막아도 group 자체는 존재한다.
        return True
    return True


def _kill_timed_out_process(process: subprocess.Popen[str]) -> None:
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except ProcessLookupError:
        pass
    process.wait()

    if os.name != "posix":
        return

    # Leader가 종료돼도 일반 descendant는 같은 group에 남을 수 있다.
    # SIGKILL이 반영될 시간을 짧게 기다리되 cleanup 자체도 제한한다.
    cleanup_deadline = time.monotonic() + PROCESS_SCOPE_CLEANUP_SECONDS
    while _posix_process_group_is_alive(process.pid):
        if time.monotonic() >= cleanup_deadline:
            break
        time.sleep(PROCESS_SCOPE_POLL_SECONDS)


def wait_for_verification_scope(
    process: subprocess.Popen[str], timeout_seconds: float
) -> bool:
    """검증 실행 범위를 기다리고 시간 초과 여부를 반환한다."""

    if os.name != "posix":
        # 비-POSIX에서는 표준 라이브러리로 직접 프로세스만 제한한다.
        # POSIX에서는 새 group에 남는 일반 descendant도 같은 제한을 받는다.
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            _kill_timed_out_process(process)
            return True
        return False

    deadline = time.monotonic() + timeout_seconds
    while True:
        leader_finished = process.poll() is not None
        group_alive = _posix_process_group_is_alive(process.pid)
        if leader_finished and not group_alive:
            return False

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            _kill_timed_out_process(process)
            return True
        time.sleep(min(PROCESS_SCOPE_POLL_SECONDS, remaining))
