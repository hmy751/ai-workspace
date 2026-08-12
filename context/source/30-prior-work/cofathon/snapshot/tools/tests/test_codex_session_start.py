from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "codex-session-start.py"
SPEC = importlib.util.spec_from_file_location("cofathon_codex_session_start", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
session_start = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(session_start)


class SessionStartTests(unittest.TestCase):
    def run_hook(self, source: str) -> tuple[dict, dict]:
        payload = {
            "session_id": f"test-{source}",
            "source": source,
            "cwd": str(session_start.ROOT),
        }
        stdout = StringIO()
        stderr = StringIO()
        with tempfile.TemporaryDirectory() as directory:
            audit_file = Path(directory) / "audit.jsonl"
            with (
                patch.object(session_start, "AUDIT_FILE", audit_file),
                patch("sys.stdin", StringIO(json.dumps(payload))),
                redirect_stdout(stdout),
                redirect_stderr(stderr),
            ):
                self.assertEqual(session_start.main(), 0)
            audit = json.loads(audit_file.read_text(encoding="utf-8"))

        self.assertEqual(stderr.getvalue(), "")
        return json.loads(stdout.getvalue()), audit

    def test_main_reentry_sources_receive_full_contract(self) -> None:
        for source in ("startup", "resume", "clear", "future-source"):
            with self.subTest(source=source):
                output, audit = self.run_hook(source)
                context = output["hookSpecificOutput"]["additionalContext"]

                self.assertTrue(context.startswith("[COFATHON_SESSION_START_V2]"))
                self.assertIn("첫 final 응답", context)
                self.assertNotIn("support-evidence-artifact.md", context)
                self.assertEqual(audit["source"], source)
                self.assertEqual(audit["mode"], "main_reentry")

    def test_compact_receives_refresh_without_startup_stop(self) -> None:
        output, audit = self.run_hook("compact")
        context = output["hookSpecificOutput"]["additionalContext"]

        self.assertTrue(context.startswith("[COFATHON_CONTEXT_REFRESH_V2]"))
        self.assertIn("진행 중인 사용자 요청을 보존하고 계속하라", context)
        self.assertNotIn("[COFATHON_SESSION_START_V2]", context)
        self.assertNotIn("support-evidence-artifact.md", context)
        self.assertEqual(audit["mode"], "compact_refresh")

    def test_audit_records_contract_and_target_snapshots(self) -> None:
        _, audit = self.run_hook("startup")

        self.assertEqual(audit["session_id"], "test-startup")
        self.assertEqual(len(audit["reentry_section_sha256"]), 64)
        self.assertEqual(len(audit["additional_context_sha256"]), 64)
        self.assertEqual(len(audit["targets"]), 3)
        self.assertEqual(
            [target["path"] for target in audit["targets"]],
            [str(path.relative_to(session_start.ROOT)) for path in session_start.REENTRY_FILES],
        )
        for target in audit["targets"]:
            self.assertGreater(target["bytes"], 0)
            self.assertEqual(len(target["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
