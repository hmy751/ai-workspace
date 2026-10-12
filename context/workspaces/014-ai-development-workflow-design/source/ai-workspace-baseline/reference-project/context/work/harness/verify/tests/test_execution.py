"""명령 시작 실패의 반환 계약과 shell 없는 실행 옵션을 검증한다."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from context.work.harness.verify import execution


class VerificationExecutionTests(unittest.TestCase):
    def test_launch_failure_returns_127_and_normalizes_the_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with patch.object(
                execution.subprocess, "Popen", side_effect=OSError(f"{root}/missing")
            ) as launch:
                result = execution.run_bounded_verification(
                    ["missing"], root, 1.0, 1000
                )
            self.assertEqual(result["exit_code"], 127)
            self.assertIsNone(result["process_returncode"])
            self.assertFalse(result["timed_out"])
            self.assertEqual(result["stdout"], "")
            self.assertIn("<OUTPUT_ROOT>/missing", result["stderr"])
            self.assertNotIn(str(root), result["stderr"])
            self.assertFalse(launch.call_args.kwargs["shell"])
            self.assertEqual(launch.call_args.kwargs["cwd"], root)
            self.assertEqual(launch.call_args.kwargs["encoding"], "utf-8")

    def test_launch_failure_output_obeys_the_same_capture_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(
                execution.subprocess, "Popen", side_effect=OSError("x" * 100)
            ):
                result = execution.run_bounded_verification(["missing"], root, 1.0, 10)
            self.assertEqual(result["exit_code"], 127)
            self.assertEqual(len(result["stderr"]), 10)
            self.assertTrue(result["output_capture"]["stderr"]["truncated"])
