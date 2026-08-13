from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
CAPTURE_SCRIPT = SCRIPTS_DIR / "capture_target_state.py"
HARNESS_SCRIPT = SCRIPTS_DIR / "record_harness_tests.py"


def run(*argv: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def init_repo(root: Path) -> None:
    result = run("git", "init", "-q", str(root))
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    (root / "tracked.txt").write_text("before\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# instructions\n", encoding="utf-8")
    for command in (
        ("git", "-C", str(root), "add", "tracked.txt", "AGENTS.md"),
        (
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Test User",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-q",
            "-m",
            "initial",
        ),
    ):
        result = run(*command)
        if result.returncode != 0:
            raise AssertionError(result.stderr)


class CaptureTargetStateTest(unittest.TestCase):
    def test_captures_dirty_and_instruction_files_without_writing_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            project = base / "project"
            project.mkdir()
            output = base / "receipts"
            output.mkdir()
            init_repo(project)
            (project / "tracked.txt").write_text("after\n", encoding="utf-8")
            (project / "new.txt").write_text("new\n", encoding="utf-8")

            result = run(
                sys.executable,
                str(CAPTURE_SCRIPT),
                "--project-root",
                str(project),
                "--output-dir",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            receipt = json.loads(Path(summary["receipt_path"]).read_text(encoding="utf-8"))

            dirty = {entry["path"]: entry for entry in receipt["git"]["dirty_entries"]}
            self.assertEqual(set(dirty), {"new.txt", "tracked.txt"})
            self.assertEqual(dirty["tracked.txt"]["states"], ["worktree"])
            self.assertEqual(
                dirty["tracked.txt"]["sha256"],
                hashlib.sha256(b"after\n").hexdigest(),
            )
            self.assertEqual(
                [entry["path"] for entry in receipt["instruction_files"]], ["AGENTS.md"]
            )
            self.assertIn("not an atomic snapshot", receipt["proof_ceiling"])
            self.assertIn("concurrent changes", receipt["proof_ceiling"])
            self.assertEqual(
                run("git", "-C", str(project), "status", "--short").stdout.splitlines(),
                [" M tracked.txt", "?? new.txt"],
            )

    def test_rejects_project_subdirectory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            project.mkdir()
            output = Path(temporary) / "receipts"
            output.mkdir()
            init_repo(project)
            child = project / "child"
            child.mkdir()
            result = run(
                sys.executable,
                str(CAPTURE_SCRIPT),
                "--project-root",
                str(child),
                "--output-dir",
                str(output),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("must equal the Git root", result.stderr)


class RecordHarnessTestsTest(unittest.TestCase):
    def prepare_project(self, base: Path) -> Path:
        project = base / "project"
        source = project / "context/work/harness"
        tests = source / "tests"
        records = project / "context/work/workspaces/001-demo/records"
        tests.mkdir(parents=True)
        records.mkdir(parents=True)
        for package in (
            project / "context",
            project / "context/work",
            source,
            tests,
        ):
            (package / "__init__.py").write_text("", encoding="utf-8")
        (source / "operation.py").write_text("VALUE = 1\n", encoding="utf-8")
        return project

    def helper_args(self, project: Path) -> list[str]:
        return [
            sys.executable,
            str(HARNESS_SCRIPT),
            "--project-root",
            str(project),
            "--source-root",
            "context/work/harness",
            "--tests-start",
            "context/work/harness/tests",
            "--top-level",
            ".",
            "--pattern",
            "test_*.py",
            "--records-dir",
            "context/work/workspaces/001-demo/records",
        ]

    def test_records_passing_command_and_source_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.prepare_project(Path(temporary))
            (project / "context/work/harness/tests/test_operation.py").write_text(
                "import unittest\n\n"
                "class OperationTest(unittest.TestCase):\n"
                "    def test_value(self):\n"
                "        self.assertEqual(1, 1)\n",
                encoding="utf-8",
            )
            result = run(*self.helper_args(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            receipt = json.loads(Path(summary["receipt_path"]).read_text(encoding="utf-8"))
            self.assertEqual(receipt["result"], "pass")
            self.assertEqual(receipt["test_count"], 1)
            self.assertEqual(receipt["test_framework"], "python_unittest_discover")
            self.assertEqual(receipt["evidence_capture"], "before_verification")
            self.assertEqual(len(receipt["source_files"]), 4)
            self.assertFalse(receipt["stdout"]["truncated"])

    def test_records_failing_command_and_returns_its_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.prepare_project(Path(temporary))
            (project / "context/work/harness/tests/test_operation.py").write_text(
                "import unittest\n\n"
                "class OperationTest(unittest.TestCase):\n"
                "    def test_value(self):\n"
                "        self.fail('expected failure')\n",
                encoding="utf-8",
            )
            result = run(*self.helper_args(project))
            self.assertEqual(result.returncode, 1, result.stderr)
            summary = json.loads(result.stdout)
            receipt = json.loads(Path(summary["receipt_path"]).read_text(encoding="utf-8"))
            self.assertEqual(receipt["result"], "fail")
            self.assertEqual(receipt["exit_code"], 1)

    def test_zero_discovery_is_never_a_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.prepare_project(Path(temporary))
            args = self.helper_args(project)
            args[args.index("--pattern") + 1] = "nothing_matches_*.py"
            result = run(*args)
            self.assertEqual(result.returncode, 5, result.stderr)
            summary = json.loads(result.stdout)
            receipt = json.loads(Path(summary["receipt_path"]).read_text(encoding="utf-8"))
            self.assertEqual(receipt["result"], "fail")
            self.assertEqual(receipt["exit_code"], 5)
            self.assertEqual(receipt["test_count"], 0)

    def test_noisy_output_is_drained_with_bounded_retention(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.prepare_project(Path(temporary))
            (project / "context/work/harness/tests/test_operation.py").write_text(
                "import unittest\n\n"
                "class OperationTest(unittest.TestCase):\n"
                "    def test_noisy_failure(self):\n"
                "        print('x' * 10000)\n"
                "        self.fail('expected failure')\n",
                encoding="utf-8",
            )
            result = run(*self.helper_args(project), "--max-output-bytes", "128")
            self.assertEqual(result.returncode, 1, result.stderr)
            summary = json.loads(result.stdout)
            receipt = json.loads(Path(summary["receipt_path"]).read_text(encoding="utf-8"))
            self.assertTrue(receipt["stdout"]["truncated"])
            self.assertEqual(receipt["stdout"]["captured_bytes"], 128)
            self.assertGreater(receipt["stdout"]["original_bytes"], 128)

    @unittest.skipUnless(hasattr(__import__("os"), "killpg"), "requires POSIX process groups")
    def test_timeout_kills_unittest_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.prepare_project(Path(temporary))
            marker = project / "escaped.txt"
            test_source = (
                "import subprocess\n"
                "import sys\n"
                "import time\n"
                "import unittest\n\n"
                "class OperationTest(unittest.TestCase):\n"
                "    def test_timeout(self):\n"
                f"        marker = {str(marker)!r}\n"
                "        subprocess.Popen([sys.executable, '-c', "
                "'import time; from pathlib import Path; time.sleep(1); '"
                "+ f'Path({marker!r}).write_text(\\\"escaped\\\")'])\n"
                "        time.sleep(30)\n"
            )
            (project / "context/work/harness/tests/test_operation.py").write_text(
                test_source, encoding="utf-8"
            )
            result = run(*self.helper_args(project), "--timeout-seconds", "0.3")
            self.assertEqual(result.returncode, 124, result.stderr)
            summary = json.loads(result.stdout)
            receipt = json.loads(Path(summary["receipt_path"]).read_text(encoding="utf-8"))
            self.assertTrue(receipt["timeout"]["timed_out"])
            self.assertEqual(receipt["timeout"]["termination_scope"], "process_group")
            time.sleep(1.2)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
