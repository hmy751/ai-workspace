"""실제 시간 대기 없이 프로세스 범위와 deadline 판단을 검증한다."""

from __future__ import annotations

import subprocess
import unittest
from unittest.mock import Mock, patch

from context.work.harness.verify import process_scope


class VerificationProcessScopeTests(unittest.TestCase):
    def test_leader_exit_does_not_finish_a_live_posix_group(self) -> None:
        process = Mock(pid=123)
        process.poll.side_effect = [None, 0, 0]
        with (
            patch.object(process_scope.os, "name", "posix"),
            patch.object(
                process_scope,
                "_posix_process_group_is_alive",
                side_effect=[True, True, False],
            ),
            patch.object(process_scope.time, "monotonic", side_effect=[0.0, 0.1, 0.2]),
            patch.object(process_scope.time, "sleep") as sleep,
            patch.object(process_scope, "_kill_timed_out_process") as kill,
        ):
            self.assertFalse(process_scope.wait_for_verification_scope(process, 1.0))
            self.assertEqual(process.poll.call_count, 3)
            self.assertEqual(sleep.call_count, 2)
            kill.assert_not_called()

    def test_live_group_is_killed_when_deadline_expires_even_after_leader_exit(
        self,
    ) -> None:
        process = Mock(pid=123)
        process.poll.return_value = 0
        with (
            patch.object(process_scope.os, "name", "posix"),
            patch.object(
                process_scope, "_posix_process_group_is_alive", return_value=True
            ),
            patch.object(process_scope.time, "monotonic", side_effect=[0.0, 1.0]),
            patch.object(process_scope, "_kill_timed_out_process") as kill,
        ):
            self.assertTrue(process_scope.wait_for_verification_scope(process, 1.0))
            kill.assert_called_once_with(process)

    def test_non_posix_wait_is_limited_to_the_direct_process(self) -> None:
        process = Mock()
        with (
            patch.object(process_scope.os, "name", "nt"),
            patch.object(process_scope, "_posix_process_group_is_alive") as group,
        ):
            self.assertFalse(process_scope.wait_for_verification_scope(process, 2.0))
            process.wait.assert_called_once_with(timeout=2.0)
            group.assert_not_called()

    def test_non_posix_timeout_uses_the_same_failure_signal(self) -> None:
        process = Mock()
        process.wait.side_effect = subprocess.TimeoutExpired(["verify"], 2.0)
        with (
            patch.object(process_scope.os, "name", "nt"),
            patch.object(process_scope, "_kill_timed_out_process") as kill,
        ):
            self.assertTrue(process_scope.wait_for_verification_scope(process, 2.0))
            kill.assert_called_once_with(process)
