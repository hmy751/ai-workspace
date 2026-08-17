from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

PACKAGE_PARENT = Path(__file__).resolve().parents[2]
if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))

from context_maintainer.cli import handle_hook, render_status
from context_maintainer.config import RuntimeConfig
from context_maintainer.protocol import (
    ProtocolError,
    validate_queue_event,
    validate_session_start,
    validate_stop,
    validate_user_prompt,
)
from context_maintainer.store import RuntimeStore


FINGERPRINT = {
    "captured_at": "2026-08-17T00:00:00Z",
    "available": True,
    "head": "a" * 40,
    "branch": "codex/test",
    "status_sha256": "b" * 64,
    "status_entry_count": 0,
    "changed_paths": [],
}


def user_payload(turn: str, prompt: str = "private user prompt", session: str = "s1"):
    return {
        "hook_event_name": "UserPromptSubmit",
        "session_id": session,
        "turn_id": turn,
        "prompt": prompt,
    }


def stop_payload(turn: str, message: str = "private assistant reply", session: str = "s1"):
    return {
        "hook_event_name": "Stop",
        "session_id": session,
        "turn_id": turn,
        "last_assistant_message": message,
        "stop_hook_active": False,
    }


class StoreTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / "context/workspaces/005-context-continuity-maintenance").mkdir(
            parents=True
        )
        self.store = RuntimeStore(self.repo, RuntimeConfig.for_repo(self.repo))

    def tearDown(self):
        self.temporary.cleanup()

    def enqueue(self, turn: str, prompt: str = "prompt", message: str = "reply"):
        self.store.accept_user_prompt(validate_user_prompt(user_payload(turn, prompt)), FINGERPRINT)
        return self.store.accept_stop(validate_stop(stop_payload(turn, message)), FINGERPRINT)


class ProtocolTests(StoreTestCase):
    def test_payload_validation_and_exact_text(self):
        prompt = "line 1\nline 2  "
        assistant = "answer\n"
        self.assertEqual(validate_user_prompt(user_payload("t1", prompt))["prompt"], prompt)
        self.assertEqual(
            validate_stop(stop_payload("t1", assistant))["last_assistant_message"],
            assistant,
        )
        session = validate_session_start(
            {
                "hook_event_name": "SessionStart",
                "session_id": "s1",
                "source": "compact",
            }
        )
        self.assertEqual(session["source"], "compact")
        with self.assertRaises(ProtocolError):
            validate_user_prompt({"hook_event_name": "UserPromptSubmit"})
        with self.assertRaises(ProtocolError):
            validate_stop({**stop_payload("t1"), "stop_hook_active": "false"})
        with self.assertRaises(ProtocolError):
            validate_session_start(
                {
                    "hook_event_name": "SessionStart",
                    "session_id": "s1",
                    "source": "unknown",
                }
            )

    def test_pair_duplicate_and_fifo_order(self):
        first = self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1")), FINGERPRINT
        )
        second = self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t2")), FINGERPRINT
        )
        self.assertEqual((first["sequence"], second["sequence"]), (1, 2))
        self.store.accept_stop(validate_stop(stop_payload("t2")), FINGERPRINT)
        blocked = self.store.drain()
        self.assertEqual(blocked["processed"], 0)
        self.assertEqual(blocked["blocked"], "gap")
        self.assertEqual(self.store.status()["missing_pair"]["waiting_stop"], 1)
        self.store.accept_stop(validate_stop(stop_payload("t1")), FINGERPRINT)
        duplicate = self.store.accept_stop(validate_stop(stop_payload("t1")), FINGERPRINT)
        self.assertTrue(duplicate["duplicate"])
        drained = self.store.drain()
        self.assertEqual(drained["processed"], 2)
        self.assertEqual(drained["last_drained"], 2)
        status = self.store.status()
        self.assertEqual(status["queue"]["count"], 0)
        self.assertEqual(status["duplicate"]["total"], 1)

    def test_partial_write_failure_does_not_reserve_sequence(self):
        original_atomic_write = RuntimeStore._atomic_write

        def fail_partial(path, value):
            if path.parent.name == "partials":
                raise OSError("simulated partial write crash")
            return original_atomic_write(path, value)

        with mock.patch.object(RuntimeStore, "_atomic_write", side_effect=fail_partial):
            with self.assertRaises(OSError):
                self.store.accept_user_prompt(
                    validate_user_prompt(user_payload("t1")), FINGERPRINT
                )

        control = self.store._read_json(
            self.store.control_path, self.store._control_default()
        )
        self.assertEqual(control["next_sequence"], 1)
        self.assertFalse(self.store.status()["gap"]["present"])

    def test_partial_only_crash_reconstructs_ledger_and_control(self):
        original_atomic_write = RuntimeStore._atomic_write

        def fail_ledger(path, value):
            if path.parent.name == "ledger":
                raise OSError("simulated ledger write crash")
            return original_atomic_write(path, value)

        with mock.patch.object(RuntimeStore, "_atomic_write", side_effect=fail_ledger):
            with self.assertRaises(OSError):
                self.store.accept_user_prompt(
                    validate_user_prompt(
                        user_payload("t1", "partial survives crash")
                    ),
                    FINGERPRINT,
                )

        self.assertTrue(list((self.store.root / "partials").glob("*.json")))
        self.assertFalse(self.store.control_path.exists())
        status = self.store.status()
        self.assertEqual(status["missing_pair"]["waiting_stop"], 1)
        control = json.loads(self.store.control_path.read_text(encoding="utf-8"))
        self.assertEqual(control["next_sequence"], 2)
        ledger = json.loads(
            next((self.store.root / "ledger").glob("*.json")).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(ledger["status"], "waiting_stop")

        self.store.accept_stop(validate_stop(stop_payload("t1")), FINGERPRINT)
        drained = self.store.drain()
        self.assertEqual(drained["processed"], 1)
        self.assertEqual(drained["last_drained"], 1)

    def test_empty_control_only_reservation_is_reclaimed(self):
        self.store.ensure_layout()
        self.store._atomic_write(
            self.store.control_path,
            {
                "protocol_version": 1,
                "next_sequence": 2,
                "last_enqueued": None,
            },
        )
        status = self.store.status()
        self.assertFalse(status["gap"]["present"])
        control = json.loads(self.store.control_path.read_text(encoding="utf-8"))
        self.assertEqual(control["next_sequence"], 1)
        accepted = self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1")), FINGERPRINT
        )
        self.assertEqual(accepted["sequence"], 1)

    def test_conflicting_prompt_replay_is_not_a_duplicate_or_delivery(self):
        self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", "original prompt")), FINGERPRINT
        )
        conflict = self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", "conflicting prompt")),
            FINGERPRINT,
        )
        self.assertTrue(conflict["conflict"])
        stop_result = self.store.accept_stop(
            validate_stop(stop_payload("t1", "answer")), FINGERPRINT
        )
        self.assertTrue(stop_result["conflict"])
        drained = self.store.drain()
        self.assertEqual(drained["processed"], 0)
        self.assertEqual(drained["last_drained"], 0)
        status = self.store.status()
        self.assertEqual(status["conflict"]["current"], 1)
        self.assertEqual(status["conflict"]["total"], 1)
        self.assertGreaterEqual(status["malformed"]["total"], 1)
        self.assertEqual(status["duplicate"]["total"], 0)
        self.assertNotIn("conflicting prompt", json.dumps(status))
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.store.root.rglob("*.json")
        )
        self.assertNotIn("conflicting prompt", runtime_text)

    def test_conflicting_assistant_replay_blocks_queued_event(self):
        self.enqueue("t1", "prompt", "original answer")
        conflict = self.store.accept_stop(
            validate_stop(stop_payload("t1", "conflicting answer")), FINGERPRINT
        )
        self.assertTrue(conflict["conflict"])
        drained = self.store.drain()
        self.assertEqual(drained["processed"], 0)
        self.assertEqual(drained["blocked"], "conflict")
        self.assertEqual(drained["last_drained"], 0)
        status = self.store.status()
        self.assertEqual(status["queue"]["count"], 1)
        self.assertEqual(status["conflict"]["current"], 1)
        self.assertNotIn("conflicting answer", json.dumps(status))
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.store.root.rglob("*.json")
        )
        self.assertNotIn("conflicting answer", runtime_text)

    def test_same_prompt_replay_remains_benign_duplicate(self):
        self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", "same prompt")), FINGERPRINT
        )
        duplicate = self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", "same prompt")), FINGERPRINT
        )
        self.assertTrue(duplicate["duplicate"])
        status = self.store.status()
        self.assertEqual(status["duplicate"]["total"], 1)
        self.assertEqual(status["conflict"]["total"], 0)

    def test_stop_before_user_pairs_without_advancing_false_cursor(self):
        result = self.store.accept_stop(validate_stop(stop_payload("t1")), FINGERPRINT)
        self.assertTrue(result["stop_before_user"])
        status = self.store.status()
        self.assertEqual(status["last_drained"]["sequence"], 0)
        self.assertEqual(status["missing_pair"]["stop_before_user"], 1)
        paired = self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1")), FINGERPRINT
        )
        self.assertTrue(paired["paired"])
        self.assertEqual(self.store.drain()["last_drained"], 1)
        self.assertEqual(self.store.status()["stop_before_user"]["unresolved"], 0)

    def test_ten_concurrent_enqueues_are_atomic(self):
        def work(index: int):
            turn = f"turn-{index}"
            self.store.accept_user_prompt(
                validate_user_prompt(user_payload(turn, f"prompt-{index}")), FINGERPRINT
            )
            self.store.accept_stop(
                validate_stop(stop_payload(turn, f"reply-{index}")), FINGERPRINT
            )

        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(work, range(10)))

        queue_files = sorted((self.store.root / "queue").glob("*.json"))
        self.assertEqual(len(queue_files), 10)
        sequences = []
        for path in queue_files:
            event = validate_queue_event(json.loads(path.read_text(encoding="utf-8")))
            sequences.append(event["sequence"])
        self.assertEqual(sequences, list(range(1, 11)))
        self.assertFalse(list(self.store.root.rglob("*.tmp")))
        self.assertEqual(self.store.drain()["processed"], 10)

    def test_observe_drain_deletes_raw_and_only_advances_cursor(self):
        self.enqueue("t1", "secret prompt", "secret answer")
        queue_file = next((self.store.root / "queue").glob("*.json"))
        raw = queue_file.read_text(encoding="utf-8")
        self.assertIn("secret prompt", raw)
        self.assertIn("secret answer", raw)
        self.assertNotIn("maintenance_outcome", raw)

        result = self.store.drain(once=True)
        self.assertEqual(result["processed"], 1)
        self.assertFalse(list((self.store.root / "queue").glob("*.json")))
        cursor = json.loads(self.store.cursor_path.read_text(encoding="utf-8"))
        self.assertEqual(cursor["last_drained_sequence"], 1)
        all_runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.store.root.rglob("*.json")
        )
        self.assertNotIn("secret prompt", all_runtime_text)
        self.assertNotIn("secret answer", all_runtime_text)
        self.assertNotIn("maintenance_outcome", all_runtime_text)

    def test_status_reconciles_partial_left_after_queue_publish(self):
        self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", "crash prompt")), FINGERPRINT
        )
        partial_path = next((self.store.root / "partials").glob("*.json"))
        partial_value = json.loads(partial_path.read_text(encoding="utf-8"))
        self.store.accept_stop(
            validate_stop(stop_payload("t1", "crash reply")), FINGERPRINT
        )
        self.store._atomic_write(partial_path, partial_value)

        before_cursor = self.store.status()["last_drained"]["sequence"]
        self.assertFalse(partial_path.exists())
        self.assertEqual(before_cursor, 0)
        self.assertEqual(self.store.status()["queue"]["count"], 1)

    def test_drain_reconciles_queue_publish_before_ledger_update(self):
        self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", "publish crash prompt")),
            FINGERPRINT,
        )
        partial_path = next((self.store.root / "partials").glob("*.json"))
        partial_value = json.loads(partial_path.read_text(encoding="utf-8"))
        ledger_path = next((self.store.root / "ledger").glob("*.json"))
        waiting_ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.store.accept_stop(
            validate_stop(stop_payload("t1", "publish crash reply")), FINGERPRINT
        )
        self.store._atomic_write(partial_path, partial_value)
        self.store._atomic_write(ledger_path, waiting_ledger)

        result = self.store.drain()
        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["last_drained"], 1)
        self.assertFalse(partial_path.exists())
        self.assertFalse(list((self.store.root / "queue").glob("*.json")))
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(ledger["status"], "drained")

    def test_drain_reconciles_stop_first_queue_publish_before_ledger_write(self):
        self.store.accept_stop(
            validate_stop(stop_payload("t1", "orphan crash reply")), FINGERPRINT
        )
        orphan_path = next((self.store.root / "orphans").glob("*.json"))
        orphan_value = json.loads(orphan_path.read_text(encoding="utf-8"))
        paired = self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", "orphan crash prompt")),
            FINGERPRINT,
        )
        ledger_path = self.store._ledger_path(paired["event_key"])
        ledger_path.unlink()
        self.store._atomic_write(orphan_path, orphan_value)

        result = self.store.drain()
        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["last_drained"], 1)
        self.assertFalse(orphan_path.exists())
        self.assertFalse(list((self.store.root / "queue").glob("*.json")))
        reconstructed = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(reconstructed["status"], "drained")
        self.assertTrue(reconstructed["reconstructed_from_queue"])
        self.assertNotIn("orphan crash prompt", json.dumps(reconstructed))
        self.assertNotIn("orphan crash reply", json.dumps(reconstructed))

    def test_status_reconciles_queue_left_after_cursor_commit(self):
        self.enqueue("t1", "cursor crash prompt", "cursor crash reply")
        queue_path = next((self.store.root / "queue").glob("*.json"))
        event = json.loads(queue_path.read_text(encoding="utf-8"))
        self.store._atomic_write(
            self.store.cursor_path,
            {
                "protocol_version": 1,
                "last_drained_sequence": 1,
                "last_drained_event": event["event_key"],
                "last_drained_at": "2026-08-17T00:01:00Z",
            },
        )

        status = self.store.status()
        self.assertEqual(status["last_drained"]["sequence"], 1)
        self.assertFalse(queue_path.exists())
        ledger = json.loads(
            self.store._ledger_path(event["event_key"]).read_text(encoding="utf-8")
        )
        self.assertEqual(ledger["status"], "drained")
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.store.root.rglob("*.json")
        )
        self.assertNotIn("cursor crash prompt", runtime_text)
        self.assertNotIn("cursor crash reply", runtime_text)

    def test_malformed_ledger_blocks_before_cursor_advance(self):
        self.enqueue("t1")
        queue_path = next((self.store.root / "queue").glob("*.json"))
        event = json.loads(queue_path.read_text(encoding="utf-8"))
        ledger_path = self.store._ledger_path(event["event_key"])
        ledger_path.write_text("{not-json", encoding="utf-8")

        result = self.store.drain()
        self.assertEqual(result["blocked"], "malformed")
        self.assertEqual(result["last_drained"], 0)
        self.assertTrue(queue_path.exists())
        self.assertGreaterEqual(self.store.status()["malformed"]["total"], 1)

    def test_malformed_partial_nested_type_is_diagnostic_not_crash(self):
        self.store.ensure_layout()
        malformed_path = (
            self.store.root
            / "partials"
            / self.store._raw_name(1, "0" * 32)
        )
        self.store._atomic_write(
            malformed_path,
            {
                "schema": "context-maintainer.partial.v1",
                "sequence": 1,
                "event_key": "0" * 32,
                "identity": {"session_id": "s1", "turn_id": "t1"},
                "user": None,
                "git": {"pre_turn": FINGERPRINT},
                "received_at": "2026-08-17T00:00:00Z",
            },
        )

        status = self.store.status()
        self.assertGreaterEqual(status["malformed"]["total"], 1)
        self.assertEqual(status["last_drained"]["sequence"], 0)
        drained = self.store.drain()
        self.assertEqual(drained["processed"], 0)
        self.assertEqual(drained["last_drained"], 0)
        self.assertTrue(malformed_path.exists())

    def test_gap_and_malformed_queue_do_not_advance_cursor(self):
        self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1")), FINGERPRINT
        )
        self.enqueue("t2")
        gap = self.store.drain()
        self.assertEqual(gap["blocked"], "gap")
        self.assertEqual(gap["last_drained"], 0)

        self.store.accept_stop(validate_stop(stop_payload("t1")), FINGERPRINT)
        expected = sorted((self.store.root / "queue").glob("*.json"))[0]
        expected.write_text("{not-json", encoding="utf-8")
        malformed = self.store.drain()
        self.assertEqual(malformed["blocked"], "malformed")
        self.assertEqual(malformed["last_drained"], 0)
        status = self.store.status()
        self.assertGreaterEqual(status["malformed"]["total"], 1)
        self.assertGreaterEqual(status["malformed"]["current"], 1)

    def test_global_fifo_exposes_cross_session_gap_proof_ceiling(self):
        self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", session="session-a")),
            FINGERPRINT,
        )
        self.store.accept_user_prompt(
            validate_user_prompt(user_payload("t1", session="session-b")),
            FINGERPRINT,
        )
        self.store.accept_stop(
            validate_stop(stop_payload("t1", session="session-b")), FINGERPRINT
        )

        result = self.store.drain()
        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["blocked"], "gap")
        status = self.store.status()
        self.assertTrue(status["gap"]["present"])
        self.assertEqual(status["queue"]["count"], 1)
        self.assertEqual(status["missing_pair"]["waiting_stop"], 1)
        self.assertEqual(
            status["proof_ceiling"],
            {
                "queue_scope": "repo_worktree_global",
                "cross_session_gap_isolation": False,
                "manual_gap_recovery": False,
            },
        )
        self.assertIn("cross-session gap isolation: false", render_status(status))

    def test_session_compact_records_metadata_only(self):
        for source in ("startup", "compact"):
            self.store.accept_session_start(
                validate_session_start(
                    {
                        "hook_event_name": "SessionStart",
                        "session_id": "s1",
                        "source": source,
                        "cwd": str(self.repo),
                        "model": "test-model",
                    }
                )
            )
        status = self.store.status()
        self.assertEqual(status["sessions"], {"count": 1, "compact_count": 1})
        self.assertEqual(status["queue"]["count"], 0)
        self.assertEqual(status["last_drained"]["sequence"], 0)

    def test_malformed_payload_is_fail_open_and_recorded(self):
        result = handle_hook(
            "UserPromptSubmit",
            {"hook_event_name": "UserPromptSubmit", "prompt": "secret"},
            self.store,
        )
        self.assertTrue(result["continue"])
        self.assertEqual(self.store.status()["malformed"]["total"], 1)

    def test_status_does_not_expose_raw_conversation(self):
        self.enqueue("t1", "DO-NOT-PRINT-PROMPT", "DO-NOT-PRINT-ANSWER")
        status = self.store.status()
        json_status = json.dumps(status, ensure_ascii=False)
        human_status = render_status(status)
        for secret in ("DO-NOT-PRINT-PROMPT", "DO-NOT-PRINT-ANSWER"):
            self.assertNotIn(secret, json_status)
            self.assertNotIn(secret, human_status)

    def test_failure_counter_is_visible_without_raw_data(self):
        self.store.record_failure("synthetic_failure")
        status = self.store.status()
        self.assertEqual(status["failure"]["total"], 1)
        self.assertNotIn("synthetic_failure", json.dumps(status))

    def test_child_recursion_guard_writes_nothing(self):
        old = os.environ.get("CODEX_CONTEXT_MAINTAINER_CHILD")
        os.environ["CODEX_CONTEXT_MAINTAINER_CHILD"] = "1"
        try:
            result = handle_hook(
                "UserPromptSubmit", user_payload("t1"), self.store
            )
        finally:
            if old is None:
                os.environ.pop("CODEX_CONTEXT_MAINTAINER_CHILD", None)
            else:
                os.environ["CODEX_CONTEXT_MAINTAINER_CHILD"] = old
        self.assertEqual(result, {"continue": True})
        self.assertFalse(self.store.root.exists())

    def test_hook_cli_prints_one_valid_json_object_for_each_event(self):
        cli = Path(__file__).resolve().parents[1] / "cli.py"
        payloads = [
            (
                ["SessionStart"],
                {
                    "hook_event_name": "SessionStart",
                    "session_id": "cli-session",
                    "source": "startup",
                },
            ),
            (["UserPromptSubmit"], user_payload("cli-turn", session="cli-session")),
            (["Stop", "--drain"], stop_payload("cli-turn", session="cli-session")),
        ]
        environment = os.environ.copy()
        environment.pop("CODEX_CONTEXT_MAINTAINER_CHILD", None)
        for event_args, payload in payloads:
            result = subprocess.run(
                [
                    "/usr/bin/python3",
                    str(cli),
                    "--repo-root",
                    str(self.repo),
                    "hook",
                    *event_args,
                ],
                input=json.dumps(payload),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {"continue": True})


class RepositoryContractTests(unittest.TestCase):
    def test_runtime_directory_is_ignored(self):
        repo_root = Path(__file__).resolve().parents[3]
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "check-ignore",
                "-q",
                ".context-harness/runtime/context-maintainer/v1/probe.json",
            ],
            check=False,
        )
        self.assertEqual(result.returncode, 0)

    def test_hooks_json_has_thin_async_stop(self):
        repo_root = Path(__file__).resolve().parents[3]
        hooks = json.loads((repo_root / ".codex/hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(
            set(hooks["hooks"]), {"SessionStart", "UserPromptSubmit", "Stop"}
        )
        stop = hooks["hooks"]["Stop"][0]["hooks"][0]
        self.assertTrue(stop["async"])
        self.assertEqual(stop["type"], "command")
        self.assertIn("git rev-parse --show-toplevel", stop["command"])

    def test_config_is_explicitly_observe_only_workspace_005(self):
        repo_root = Path(__file__).resolve().parents[3]
        config = json.loads(
            (repo_root / ".codex/context_maintainer/config.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(config["mode"], "observe")
        self.assertEqual(
            config["workspace"]["id"], "005-context-continuity-maintenance"
        )
        self.assertEqual(
            config["runtime_path"],
            ".context-harness/runtime/context-maintainer/v1",
        )


if __name__ == "__main__":
    unittest.main()
