"""Verify: 시간 초과와 일반 POSIX descendant 종료를 검증한다."""

from __future__ import annotations

import copy
import json
import os
import signal
import time
import unittest

from .support import VerifyFixture


class VerifyProcessTests(VerifyFixture):
    verification_scenarios = ("slow",)

    def test_timeout_persists_exit_124_failure_receipt_and_status(self) -> None:
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"].update(
            {
                "argv": [
                    "python3",
                    "-m",
                    "unittest",
                    "tests.test_slow",
                    "-v",
                ],
                "timeout_seconds": 0.1,
                "max_output_chars": 1000,
            }
        )
        self.write_work_json("workspaces/001-example/verify.json", contract)

        completed = self.run_cli("verify")

        self.assertEqual(completed.returncode, 124, completed.stdout + completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertTrue(summary["timed_out"])
        self.assertEqual(summary["status"], "verification_failed")
        receipt_files = self.receipt_files()
        self.assertEqual(len(receipt_files), 1)
        receipt = json.loads(receipt_files[0].read_text(encoding="utf-8"))
        self.assertEqual(receipt["exit_code"], 124)
        self.assertEqual(receipt["result"], "fail")
        self.assertTrue(receipt["timeout"]["timed_out"])
        self.assertEqual(receipt["timeout"]["timeout_seconds"], 0.1)
        status = self.read_status()
        self.assertEqual(status["status"], "verification_failed")
        self.assertEqual(status["result"], "fail")
        self.assertEqual(status["receipt"], summary["receipt"])
        self.assertEqual(status["finished_at"], receipt["finished_at"])

    @unittest.skipUnless(
        os.name == "posix", "process-group descendant coverage is POSIX-only"
    )
    def test_timeout_covers_descendant_after_group_leader_exits(self) -> None:
        launcher = self.project_root / "tests" / "spawn-descendant.py"
        descendant_pid_path = self.project_root / "descendant.pid"
        # 새 shell 파일의 첫 실행 지연을 group 종료 검사에 섞지 않는다.
        # 설치된 Python이 launcher를 읽고 같은 session의 일반 child를 만든다.
        launcher.write_text(
            "from pathlib import Path\n"
            "import subprocess\n"
            "import sys\n"
            "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])\n"
            "Path('descendant.pid').write_text(str(child.pid), encoding='utf-8')\n",
            encoding="utf-8",
        )

        def kill_descendant_if_alive() -> None:
            if not descendant_pid_path.is_file():
                return
            descendant_pid = int(descendant_pid_path.read_text(encoding="utf-8"))
            try:
                os.kill(descendant_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        # Assertion 이전에도 cleanup을 등록해 실패한 검사에서 child를 남기지 않는다.
        self.addCleanup(kill_descendant_if_alive)
        contract = copy.deepcopy(self.verify_contract)
        contract["verification"].update(
            {
                "argv": ["python3", "tests/spawn-descendant.py"],
                "timeout_seconds": 0.3,
                "max_output_chars": 1000,
            }
        )
        self.write_work_json("workspaces/001-example/verify.json", contract)

        started = time.monotonic()
        completed = self.run_cli("verify")
        elapsed = time.monotonic() - started

        self.assertEqual(completed.returncode, 124, completed.stdout + completed.stderr)
        self.assertLess(elapsed, 2.0)
        self.assertTrue(
            descendant_pid_path.is_file(), completed.stdout + completed.stderr
        )
        descendant_pid = int(descendant_pid_path.read_text(encoding="utf-8"))

        def descendant_is_alive() -> bool:
            try:
                os.kill(descendant_pid, 0)
            except ProcessLookupError:
                return False
            return True

        disappearance_deadline = time.monotonic() + 1.0
        while descendant_is_alive() and time.monotonic() < disappearance_deadline:
            time.sleep(0.005)
        self.assertFalse(descendant_is_alive())

        summary = json.loads(completed.stdout)
        self.assertTrue(summary["timed_out"])
        receipt = json.loads(self.receipt_files()[0].read_text(encoding="utf-8"))
        self.assertEqual(receipt["process_returncode"], 0)
        self.assertEqual(receipt["exit_code"], 124)
        self.assertEqual(receipt["result"], "fail")
        self.assertTrue(receipt["timeout"]["timed_out"])
        self.assertEqual(receipt["timeout"]["timeout_seconds"], 0.3)
