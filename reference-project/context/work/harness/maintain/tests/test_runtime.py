from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
from threading import Event, Thread
import unittest
from unittest import mock

from context.work.harness.maintain.runtime import (
    MaintainRuntime,
    ProcessingDeferredError,
    RuntimeProtocolError,
)


WORKSPACE = "005-context-continuity-maintenance"


def session_start(session: str = "session-a", source: str = "startup") -> dict[str, object]:
    return {
        "hook_event_name": "SessionStart",
        "session_id": session,
        "source": source,
    }


def user(
    turn: str,
    prompt: str = "private prompt",
    session: str = "session-a",
) -> dict[str, object]:
    return {
        "hook_event_name": "UserPromptSubmit",
        "session_id": session,
        "turn_id": turn,
        "prompt": prompt,
    }


def stop(
    turn: str,
    assistant: str | None = "private answer",
    session: str = "session-a",
) -> dict[str, object]:
    return {
        "hook_event_name": "Stop",
        "session_id": session,
        "turn_id": turn,
        "last_assistant_message": assistant,
    }


def post_tool(
    turn: str,
    *,
    tool_name: str = "apply_patch",
    tool_use_id: str = "tool-use-1",
    tool_input: object = "*** Update File: current/state.md\n@@\n-old\n+new",
    tool_response: object = None,
    session: str = "session-a",
) -> dict[str, object]:
    return {
        "hook_event_name": "PostToolUse",
        "session_id": session,
        "turn_id": turn,
        "tool_name": tool_name,
        "tool_use_id": tool_use_id,
        "tool_input": tool_input,
        "tool_response": tool_response,
    }


class FailOnce:
    def __init__(self, target: str) -> None:
        self.target = target
        self.triggered = False

    def __call__(self, point: str) -> None:
        if point == self.target and not self.triggered:
            self.triggered = True
            raise OSError(f"injected fault at {point}")


class RuntimeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.runtime_root = Path(self.temporary.name) / "runtime"
        self.runtime = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def pair(
        self,
        turn: str,
        *,
        prompt: str = "private prompt",
        assistant: str | None = "private answer",
        session: str = "session-a",
    ) -> None:
        self.runtime.user_prompt(user(turn, prompt, session))
        result = self.runtime.stop(stop(turn, assistant, session))
        self.assertTrue(result["paired"])

    def session_root(self, session: str = "session-a") -> Path:
        return self.runtime._session_root(session)


class CaptureProtocolTests(RuntimeTestCase):
    def test_requires_explicit_root_workspace_and_valid_hook_payloads(self) -> None:
        with self.assertRaises(ValueError):
            MaintainRuntime(runtime_root=self.runtime_root, workspace_id="")
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.session_start(
                {
                    "hook_event_name": "SessionStart",
                    "session_id": "session-a",
                    "source": "not-a-source",
                }
            )
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.user_prompt(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "session-a",
                    "turn_id": "turn-1",
                    "prompt": 42,
                }
            )
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.stop(
                {
                    "hook_event_name": "Stop",
                    "session_id": "session-a",
                    "turn_id": "turn-1",
                    "last_assistant_message": False,
                }
            )

    def test_pair_preserves_exact_text_until_success(self) -> None:
        prompt = "line one\nline two  "
        assistant = "answer\n"
        self.pair("turn-1", prompt=prompt, assistant=assistant)
        queue_path = next((self.session_root() / "queue").glob("*.json"))
        queued = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertEqual(queued["prompt"], prompt)
        self.assertEqual(queued["assistant"], assistant)
        self.assertEqual(queued["sequence"], 1)

    def test_stop_before_user_pairs_when_prompt_arrives(self) -> None:
        waiting = self.runtime.stop(stop("turn-1", "answer first"))
        self.assertTrue(waiting["waiting_user"])
        paired = self.runtime.user_prompt(user("turn-1", "prompt later"))
        self.assertTrue(paired["paired"])
        event = next((self.session_root() / "queue").glob("*.json"))
        value = json.loads(event.read_text(encoding="utf-8"))
        self.assertEqual(value["prompt"], "prompt later")
        self.assertEqual(value["assistant"], "answer first")

    def test_same_replay_is_duplicate_and_different_replay_is_conflict(self) -> None:
        self.pair("turn-1", prompt="original prompt", assistant="original answer")
        prompt_duplicate = self.runtime.user_prompt(
            user("turn-1", "original prompt")
        )
        stop_duplicate = self.runtime.stop(stop("turn-1", "original answer"))
        self.assertTrue(prompt_duplicate["duplicate"])
        self.assertTrue(stop_duplicate["duplicate"])

        prompt_conflict = self.runtime.user_prompt(
            user("turn-1", "different prompt")
        )
        stop_conflict = self.runtime.stop(stop("turn-1", "different answer"))
        self.assertTrue(prompt_conflict["conflict"])
        self.assertTrue(stop_conflict["conflict"])

        queue_path = next((self.session_root() / "queue").glob("*.json"))
        queued = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertEqual(queued["prompt"], "original prompt")
        self.assertEqual(queued["assistant"], "original answer")
        # The immutable original remains a duplicate even after a conflict was
        # observed; the conflicting replay never replaces it.
        self.assertTrue(
            self.runtime.stop(stop("turn-1", "original answer"))["duplicate"]
        )
        self.assertTrue(
            self.runtime.workspace_freshness_summary()["warning_required"]
        )

    def test_queue_publish_before_ledger_crash_preserves_original(self) -> None:
        fault = FailOnce("after_queue_publish_before_ledger")
        crashing = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
            fault_injector=fault,
        )
        crashing.user_prompt(user("turn-1", "crash prompt"))
        with self.assertRaises(OSError):
            crashing.stop(stop("turn-1", "original answer"))

        queue_path = next((self.session_root() / "queue").glob("*.json"))
        before = queue_path.read_bytes()
        different = crashing.stop(stop("turn-1", "different answer"))
        self.assertTrue(different["conflict"])
        self.assertEqual(queue_path.read_bytes(), before)
        same = crashing.stop(stop("turn-1", "original answer"))
        self.assertTrue(same["duplicate"])
        self.assertEqual(queue_path.read_bytes(), before)

    def test_partial_publish_crash_reconciles_without_sequence_reuse(self) -> None:
        fault = FailOnce("after_prompt_publish")
        crashing = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
            fault_injector=fault,
        )
        with self.assertRaises(OSError):
            crashing.user_prompt(user("turn-1", "first"))
        accepted = crashing.user_prompt(user("turn-2", "second"))
        self.assertEqual(accepted["sequence"], 2)
        replay = crashing.user_prompt(user("turn-1", "first"))
        self.assertTrue(replay["duplicate"])
        self.assertEqual(replay["sequence"], 1)

    def test_core_publications_fsync_their_parent_directories(self) -> None:
        with mock.patch(
            "context.work.harness.maintain.runtime._fsync_directory"
        ) as fsync_directory:
            self.pair("turn-1")
            self.runtime.process_next(
                "session-a", lambda event: "no_change"
            )

        synchronized = {call.args[0] for call in fsync_directory.call_args_list}
        session_root = self.session_root()
        self.assertIn(session_root / "partials", synchronized)
        self.assertIn(session_root / "queue", synchronized)
        self.assertIn(session_root / "ledger", synchronized)
        self.assertIn(session_root, synchronized)

    def test_work_generation_is_durable_and_content_free(self) -> None:
        before = self.runtime.work_generation("session-a")
        self.pair(
            "turn-1",
            prompt="GENERATION-SECRET-PROMPT",
            assistant="GENERATION-SECRET-ANSWER",
        )
        after = self.runtime.work_generation("session-a")
        self.assertNotEqual(before["generation"], after["generation"])
        self.assertEqual(after["queued"], 1)
        self.assertNotIn("GENERATION-SECRET", json.dumps(after))

        reopened = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
        )
        self.assertEqual(reopened.work_generation("session-a"), after)

    def test_no_git_or_subprocess_scan_occurs(self) -> None:
        with mock.patch.object(subprocess, "run") as run:
            self.runtime.session_start(session_start())
            self.pair("turn-1")
            self.runtime.status("session-a")
        run.assert_not_called()

    def test_compaction_is_a_marker_not_a_reset(self) -> None:
        self.runtime.session_start(session_start(source="startup"))
        self.pair("turn-1")
        self.assertEqual(
            self.runtime.process_next("session-a", lambda event: "no_change")[
                "status"
            ],
            "processed",
        )
        self.runtime.session_start(session_start(source="compact"))
        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["freshness"]["processed_sequence"], 1)
        metadata = json.loads(
            (self.session_root() / "session.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["compact_count"], 1)
        self.assertEqual(metadata["start_count"], 2)


class IsolationAndRecoveryTests(RuntimeTestCase):
    def test_recovery_selector_returns_oldest_queue_then_next_session(self) -> None:
        old_session = "old-private-session"
        new_session = "new-private-session"
        self.pair("old-turn", session=old_session)
        self.pair("new-turn", session=new_session)

        self.assertEqual(
            self.runtime.next_runnable_session_id(),
            old_session,
        )
        self.assertEqual(
            self.runtime.process_next(
                old_session,
                lambda event: "no_change",
            )["status"],
            "processed",
        )
        self.assertEqual(
            self.runtime.next_runnable_session_id(),
            new_session,
        )

        rendered_status = json.dumps(self.runtime.status())
        self.assertNotIn(old_session, rendered_status)
        self.assertNotIn(new_session, rendered_status)

    def test_recovery_selector_skips_incomplete_tail_and_report_only_session(
        self,
    ) -> None:
        capture_cases = {
            "user": lambda runtime: runtime.user_prompt(
                user("waiting", session="old-incomplete")
            ),
            "stop": lambda runtime: runtime.stop(
                stop("orphan", session="old-incomplete")
            ),
            "tool": lambda runtime: runtime.post_tool_use(
                post_tool("evidence", session="old-incomplete")
            ),
            "combined": lambda runtime: (
                runtime.user_prompt(
                    user("waiting", session="old-incomplete")
                ),
                runtime.stop(stop("orphan", session="old-incomplete")),
                runtime.post_tool_use(
                    post_tool("evidence", session="old-incomplete")
                ),
            ),
        }
        for name, capture in capture_cases.items():
            with self.subTest(capture=name):
                runtime = MaintainRuntime(
                    runtime_root=(
                        Path(self.temporary.name) / f"incomplete-{name}"
                    ),
                    workspace_id=WORKSPACE,
                )
                capture(runtime)
                runtime.user_prompt(user("queued", session="later-session"))
                runtime.stop(stop("queued", session="later-session"))

                summary = runtime.workspace_freshness_summary(
                    exclude_session_id="later-session"
                )
                self.assertTrue(summary["freshness_ready"])
                self.assertEqual(
                    summary["warning_required"],
                    name != "user",
                )
                self.assertEqual(
                    summary["incomplete_capture_tail_sessions"],
                    1,
                )
                self.assertEqual(
                    runtime.next_runnable_session_id(),
                    "later-session",
                )

        report_runtime = MaintainRuntime(
            runtime_root=Path(self.temporary.name) / "report-runtime",
            workspace_id=WORKSPACE,
        )
        report_runtime.user_prompt(
            user("report", session="old-report-session")
        )
        report_runtime.stop(stop("report", session="old-report-session"))
        report_runtime.process_next(
            "old-report-session",
            lambda event: {
                "outcome": "needs_decision",
                "summary": "bounded summary",
                "question": "bounded question?",
            },
        )
        report_runtime.user_prompt(
            user("queued", session="later-queued-session")
        )
        report_runtime.stop(
            stop("queued", session="later-queued-session")
        )
        self.assertEqual(
            report_runtime.next_runnable_session_id(),
            "later-queued-session",
        )

    def test_recovery_selector_recovers_retry_and_stale_lease(self) -> None:
        self.pair("retry", session="retry-session")
        retry = self.runtime.process_next(
            "retry-session",
            lambda event: (_ for _ in ()).throw(ValueError("retry")),
        )
        self.assertEqual(retry["status"], "retry")
        self.assertEqual(
            self.runtime.next_runnable_session_id(),
            "retry-session",
        )

        stale_runtime = MaintainRuntime(
            runtime_root=Path(self.temporary.name) / "stale-runtime",
            workspace_id=WORKSPACE,
        )
        stale_runtime.user_prompt(user("stale", session="stale-session"))
        stale_runtime.stop(stop("stale", session="stale-session"))
        with self.assertRaises(SystemExit):
            stale_runtime.process_next(
                "stale-session",
                lambda event: (_ for _ in ()).throw(SystemExit("killed")),
            )
        self.assertEqual(
            stale_runtime.next_runnable_session_id(),
            "stale-session",
        )

    def test_recovery_selector_never_bypasses_malformed_gap_or_active(self) -> None:
        self.pair("old", session="malformed-old")
        old_queue = next(
            (self.session_root("malformed-old") / "queue").glob("*.json")
        )
        old_queue.write_text("{}\n", encoding="utf-8")
        self.pair("new", session="valid-new")
        self.assertIsNone(self.runtime.next_runnable_session_id())

        gap_runtime = MaintainRuntime(
            runtime_root=Path(self.temporary.name) / "gap-runtime",
            workspace_id=WORKSPACE,
        )
        gap_runtime.user_prompt(user("missing", session="gap-old"))
        gap_runtime.user_prompt(user("later", session="gap-old"))
        gap_runtime.stop(stop("later", session="gap-old"))
        gap_runtime.user_prompt(user("new", session="gap-new"))
        gap_runtime.stop(stop("new", session="gap-new"))
        self.assertIsNone(gap_runtime.next_runnable_session_id())

        active_runtime = MaintainRuntime(
            runtime_root=Path(self.temporary.name) / "active-runtime",
            workspace_id=WORKSPACE,
        )
        active_runtime.user_prompt(user("old", session="active-old"))
        active_runtime.stop(stop("old", session="active-old"))
        entered = Event()
        release = Event()

        def hold(event: dict[str, object]) -> str:
            entered.set()
            self.assertTrue(release.wait(timeout=2))
            return "no_change"

        worker = Thread(
            target=lambda: active_runtime.process_next("active-old", hold)
        )
        worker.start()
        self.assertTrue(entered.wait(timeout=2))
        active_runtime.user_prompt(user("new", session="active-new"))
        active_runtime.stop(stop("new", session="active-new"))
        self.assertIsNone(active_runtime.next_runnable_session_id())
        release.set()
        worker.join(timeout=2)
        self.assertFalse(worker.is_alive())

    def test_recovery_selector_requires_queue_identity_to_match_metadata(self) -> None:
        self.pair("turn", session="private-session")
        metadata_path = self.session_root("private-session") / "session.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["session_id_sha256"] = "f" * 64
        metadata_path.write_text(
            json.dumps(metadata) + "\n",
            encoding="utf-8",
        )
        self.assertIsNone(self.runtime.next_runnable_session_id())

    def test_status_does_not_create_or_count_an_unestablished_ghost(self) -> None:
        ghost_root = self.runtime._session_root("ghost-session")
        self.assertFalse(ghost_root.exists())
        specific = self.runtime.status("ghost-session")
        self.assertEqual(specific["freshness"]["state"], "unknown")
        self.assertFalse(specific["freshness"]["trustworthy"])
        self.assertEqual(len(specific["session_id_sha256"]), 64)
        self.assertFalse(ghost_root.exists())
        self.assertFalse(self.runtime.sessions_root.exists())

        ghost_root.mkdir(parents=True)
        before = sorted(path.name for path in ghost_root.iterdir())
        aggregate = self.runtime.status()
        after = sorted(path.name for path in ghost_root.iterdir())
        self.assertEqual(aggregate["sessions"], [])
        self.assertEqual(aggregate["counts"]["sessions"], 0)
        self.assertEqual(before, after)

    def test_status_reports_invalid_metadata_without_normalizing_it(self) -> None:
        session_root = self.runtime.session_runtime_root("session-a")
        metadata_path = session_root / "session.json"
        malformed = b'{"schema":"wrong","secret":"KEEP"}\n'
        metadata_path.write_bytes(malformed)

        specific = self.runtime.status("session-a")
        aggregate = self.runtime.status()
        self.assertEqual(specific["freshness"]["state"], "unknown")
        self.assertEqual(
            specific["failure"]["code"], "malformed_session_metadata"
        )
        self.assertEqual(aggregate["counts"]["sessions"], 1)
        self.assertEqual(
            aggregate["sessions"][0]["freshness"]["state"], "unknown"
        )
        self.assertEqual(
            len(aggregate["sessions"][0]["session_id_sha256"]), 64
        )
        self.assertTrue(
            self.runtime.workspace_freshness_summary()["warning_required"]
        )
        self.assertEqual(metadata_path.read_bytes(), malformed)

    def test_public_session_root_is_opaque_and_creates_layout(self) -> None:
        path = self.runtime.session_runtime_root("session/with unsafe text")
        self.assertEqual(path.parent.name, "sessions")
        self.assertNotIn("session", path.name)
        self.assertTrue((path / "queue").is_dir())
        self.assertTrue((path / "ledger").is_dir())
        with self.assertRaises(ValueError):
            self.runtime.session_runtime_root("")

    def test_workspace_runtime_root_is_shared_and_distinct_from_sessions(self) -> None:
        workspace_root = self.runtime.workspace_runtime_root()
        first = self.runtime.session_runtime_root("session-a")
        second = self.runtime.session_runtime_root("session-b")

        self.assertEqual(first.parent, workspace_root / "sessions")
        self.assertEqual(second.parent, workspace_root / "sessions")
        self.assertNotEqual(first, second)
        metadata = json.loads(
            (workspace_root / "workspace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["workspace_id"], WORKSPACE)

    def test_workspace_runtime_root_rejects_mismatched_metadata(self) -> None:
        workspace_root = self.runtime.workspace_runtime_root()
        (workspace_root / "workspace.json").write_text(
            '{"schema":"context-maintain.workspace.v2",'
            '"workspace_id":"other","workspace_id_sha256":"bad"}\n',
            encoding="utf-8",
        )
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.workspace_runtime_root()

    def test_session_and_process_locks_never_follow_symlinks(self) -> None:
        session_root = self.runtime.session_runtime_root("session-a")
        outside = Path(self.temporary.name) / "outside-lock"
        outside.write_text("KEEP", encoding="utf-8")

        session_lock = session_root / ".lock"
        session_lock.unlink()
        session_lock.symlink_to(outside)
        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["freshness"]["state"], "unknown")
        self.assertEqual(
            status_value["failure"]["code"], "malformed_session_layout"
        )
        self.assertEqual(outside.read_text(encoding="utf-8"), "KEEP")

        session_lock.unlink()
        self.runtime.user_prompt(user("turn-1"))
        process_lock = session_root / ".process.lock"
        process_lock.symlink_to(outside)
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.process_next("session-a", lambda event: "no_change")
        self.assertEqual(outside.read_text(encoding="utf-8"), "KEEP")

    def test_gap_in_one_session_does_not_block_another(self) -> None:
        self.runtime.user_prompt(user("turn-1", session="session-a"))
        self.pair("turn-1", session="session-b")

        blocked = self.runtime.process_next("session-a", lambda event: "no_change")
        processed = self.runtime.process_next("session-b", lambda event: "no_change")
        self.assertEqual(blocked["reason"], "waiting_pair")
        self.assertEqual(processed["status"], "processed")
        self.assertEqual(
            self.runtime.status("session-b")["freshness"]["state"], "fresh"
        )

    def test_current_prompt_waiting_for_stop_is_not_yet_a_gap(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["freshness"]["state"], "behind")
        self.assertTrue(status_value["freshness"]["trustworthy"])
        self.assertFalse(status_value["gap"]["detected"])
        self.assertIsNone(status_value["failure"]["code"])

    def test_higher_sequence_behind_missing_stop_is_untrustworthy_gap(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        self.runtime.user_prompt(user("turn-2", "later prompt"))
        self.runtime.stop(stop("turn-2", "later answer"))

        status_value = self.runtime.status("session-a")
        self.assertEqual(
            status_value["freshness"]["state"], "attention_required"
        )
        self.assertFalse(status_value["freshness"]["trustworthy"])
        self.assertEqual(status_value["gap"]["code"], "missing_stop_gap")
        self.assertEqual(status_value["gap"]["expected_sequence"], 1)
        self.assertEqual(status_value["gap"]["higher_sequence"], 2)
        self.assertEqual(status_value["failure"]["code"], "missing_stop_gap")

        called = False

        def processor(event: dict[str, object]) -> str:
            nonlocal called
            called = True
            return "no_change"

        blocked = self.runtime.process_next("session-a", processor)
        self.assertEqual(blocked["reason"], "missing_stop_gap")
        self.assertFalse(called)

        # Late delivery repairs the exact event; no sequence is abandoned.
        self.runtime.stop(stop("turn-1", "late exact answer"))
        self.assertEqual(
            self.runtime.process_next("session-a", processor)["status"],
            "processed",
        )
        self.assertEqual(
            self.runtime.process_next("session-a", processor)["status"],
            "processed",
        )
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["state"], "fresh"
        )

    def test_approved_exact_gap_abandonment_preserves_provenance_and_fifo(self) -> None:
        self.runtime.user_prompt(user("turn-1", "raw prompt to remove"))
        self.pair("turn-2", prompt="later", assistant="later answer")

        with self.assertRaises(RuntimeProtocolError):
            self.runtime.repair_missing_stop_gap(
                "session-a",
                2,
                approved_by="user",
                reason="host_stop_unrecoverable",
            )
        with self.assertRaises(ValueError):
            self.runtime.repair_missing_stop_gap(
                "session-a",
                1,
                approved_by="user",
                reason="free form reason is not a code",
            )

        repaired = self.runtime.repair_missing_stop_gap(
            "session-a",
            1,
            approved_by="user",
            reason="host_stop_unrecoverable",
        )
        self.assertTrue(repaired["repaired"])
        self.assertFalse(repaired["duplicate"])
        duplicate = self.runtime.repair_missing_stop_gap(
            "session-a",
            1,
            approved_by="user",
            reason="host_stop_unrecoverable",
        )
        self.assertTrue(duplicate["duplicate"])

        first_ledger = min(
            (
                json.loads(path.read_text(encoding="utf-8"))
                for path in (self.session_root() / "ledger").glob("*.json")
            ),
            key=lambda value: value["sequence"],
        )
        self.assertEqual(first_ledger["status"], "abandoned")
        self.assertEqual(first_ledger["outcome"], "gap_abandoned")
        self.assertEqual(first_ledger["repair"]["approved_by"], "user")
        self.assertEqual(
            first_ledger["repair"]["reason"], "host_stop_unrecoverable"
        )
        self.assertFalse(list((self.session_root() / "partials").glob("*.json")))

        processed = self.runtime.process_next(
            "session-a", lambda event: "no_change"
        )
        self.assertEqual(processed["sequence"], 2)
        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["freshness"]["state"], "fresh")
        repair_status = status_value["repairs"]["gap_abandoned"]
        self.assertEqual(repair_status["count"], 1)
        self.assertEqual(repair_status["latest_sequence"], 1)
        self.assertEqual(repair_status["latest_approved_by"], "user")
        self.assertEqual(
            repair_status["latest_reason"], "host_stop_unrecoverable"
        )

    def test_gap_repair_ledger_crash_reconciles_only_approved_sequence(self) -> None:
        self.runtime.user_prompt(user("turn-1", "raw prompt"))
        self.pair("turn-2", prompt="later", assistant="later answer")
        fault = FailOnce("after_gap_repair_ledger")
        crashing = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
            fault_injector=fault,
        )
        with self.assertRaises(OSError):
            crashing.repair_missing_stop_gap(
                "session-a",
                1,
                approved_by="user",
                reason="host_stop_unrecoverable",
            )

        recovered = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
        )
        status_value = recovered.status("session-a")
        self.assertEqual(status_value["freshness"]["state"], "unknown")
        self.assertIsNone(status_value["freshness"]["processed_sequence"])
        self.assertEqual(
            recovered.process_next("session-a", lambda event: "no_change")[
                "sequence"
            ],
            2,
        )
        self.assertEqual(
            recovered.status("session-a")["freshness"]["state"], "fresh"
        )

    def test_gap_repair_checkpoint_crash_exposes_and_sweeps_raw_residue(
        self,
    ) -> None:
        self.runtime.user_prompt(user("turn-1", "repair raw prompt"))
        self.runtime.post_tool_use(post_tool("turn-1"))
        self.pair("turn-2", prompt="later", assistant="later answer")
        first_partial = next(
            (self.session_root() / "partials").glob("00000000000000000001-*.json")
        )
        first_event = json.loads(first_partial.read_text(encoding="utf-8"))
        evidence_root = (
            self.session_root() / "tool-evidence" / first_event["event_id"]
        )
        self.assertTrue(evidence_root.exists())

        crashing = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
            fault_injector=FailOnce("after_gap_repair_checkpoint"),
        )
        with self.assertRaises(OSError):
            crashing.repair_missing_stop_gap(
                "session-a",
                1,
                approved_by="user",
                reason="host_stop_unrecoverable",
            )

        recovered = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
        )
        residue = recovered.status("session-a")
        self.assertEqual(residue["freshness"]["state"], "behind")
        self.assertEqual(residue["pending"]["cleanup_residue"], 1)
        self.assertEqual(
            recovered.next_runnable_session_id(),
            "session-a",
        )

        calls = 0

        def process_later(event: dict[str, object]) -> str:
            nonlocal calls
            calls += 1
            self.assertEqual(event["sequence"], 2)
            return "no_change"

        result = recovered.process_next("session-a", process_later)
        self.assertEqual(result["status"], "processed")
        self.assertEqual(calls, 1)
        self.assertFalse(first_partial.exists())
        self.assertFalse(evidence_root.exists())
        self.assertEqual(
            recovered.status("session-a")["freshness"]["state"],
            "fresh",
        )

    def test_capture_does_not_wait_for_long_processor(self) -> None:
        self.pair("turn-1")
        entered = Event()
        release = Event()
        result: list[dict[str, object]] = []

        def processor(event: dict[str, object]) -> str:
            entered.set()
            self.assertTrue(release.wait(timeout=2))
            return "updated_quiet"

        thread = Thread(
            target=lambda: result.append(
                self.runtime.process_next("session-a", processor)
            )
        )
        thread.start()
        self.assertTrue(entered.wait(timeout=2))
        # process_next released the short state lock before entering processor.
        second = self.runtime.user_prompt(user("turn-2", "arrived meanwhile"))
        self.assertEqual(second["sequence"], 2)
        release.set()
        thread.join(timeout=2)
        self.assertFalse(thread.is_alive())
        self.assertEqual(result[0]["status"], "processed")

    def test_idle_generation_retry_closes_busy_worker_lost_wakeup(self) -> None:
        terminal_observed = Event()
        release_terminal = Event()

        def pause_terminal(point: str) -> None:
            if point == "after_terminal_observation_before_process_unlock":
                terminal_observed.set()
                self.assertTrue(release_terminal.wait(timeout=2))

        runtime = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
            fault_injector=pause_terminal,
        )
        delivered: list[int] = []
        result: list[dict[str, object]] = []
        active = Thread(
            target=lambda: result.append(
                runtime.process_next(
                    "session-a",
                    lambda event: delivered.append(event["sequence"])
                    or "no_change",
                )
            )
        )
        active.start()
        self.assertTrue(terminal_observed.wait(timeout=2))

        runtime.user_prompt(user("turn-1", "arrived in unlock window"))
        runtime.stop(stop("turn-1", "paired in unlock window"))
        contender = runtime.process_next(
            "session-a",
            lambda event: "no_change",
            process_lock_wait_seconds=0,
        )
        self.assertEqual(contender["status"], "busy")
        release_terminal.set()
        active.join(timeout=2)
        self.assertFalse(active.is_alive())
        self.assertEqual(result[0]["status"], "processed")
        self.assertEqual(delivered, [1])
        self.assertEqual(
            runtime.status("session-a")["freshness"]["state"], "fresh"
        )

    def test_bounded_waiting_worker_claims_successor_after_busy_window(self) -> None:
        self.pair("turn-1")
        first_entered = Event()
        release_first = Event()
        first_result: list[dict[str, object]] = []
        second_result: list[dict[str, object]] = []
        delivered: list[int] = []

        def first_processor(event: dict[str, object]) -> str:
            delivered.append(int(event["sequence"]))
            first_entered.set()
            self.assertTrue(release_first.wait(timeout=2))
            return "no_change"

        first_worker = Thread(
            target=lambda: first_result.append(
                self.runtime.process_next("session-a", first_processor)
            )
        )
        first_worker.start()
        self.assertTrue(first_entered.wait(timeout=2))
        self.pair("turn-2")

        second_started = Event()

        def run_second() -> None:
            second_started.set()
            second_result.append(
                self.runtime.process_next(
                    "session-a",
                    lambda event: delivered.append(int(event["sequence"]))
                    or "no_change",
                )
            )

        second_worker = Thread(target=run_second)
        second_worker.start()
        self.assertTrue(second_started.wait(timeout=2))
        second_worker.join(timeout=0.05)
        self.assertTrue(second_worker.is_alive())

        release_first.set()
        first_worker.join(timeout=2)
        second_worker.join(timeout=2)
        self.assertFalse(first_worker.is_alive())
        self.assertFalse(second_worker.is_alive())
        self.assertEqual(first_result[0]["sequence"], 1)
        self.assertEqual(second_result[0]["sequence"], 2)
        self.assertEqual(delivered, [1, 2])
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["state"], "fresh"
        )

    def test_active_processor_and_stale_lease_have_distinct_status(self) -> None:
        self.pair("turn-1")
        entered = Event()
        release = Event()

        def processor(event: dict[str, object]) -> str:
            entered.set()
            self.assertTrue(release.wait(timeout=2))
            return "no_change"

        thread = Thread(
            target=lambda: self.runtime.process_next("session-a", processor)
        )
        thread.start()
        self.assertTrue(entered.wait(timeout=2))
        active = self.runtime.status("session-a")
        self.assertEqual(active["freshness"]["state"], "processing")
        self.assertTrue(active["freshness"]["trustworthy"])
        self.assertTrue(active["pending"]["processor_active"])
        release.set()
        thread.join(timeout=2)
        self.assertFalse(thread.is_alive())

        self.pair("turn-2")

        def crash_without_checkpoint(event: dict[str, object]) -> str:
            raise SystemExit("simulated worker death")

        with self.assertRaises(SystemExit):
            self.runtime.process_next("session-a", crash_without_checkpoint)
        stale = self.runtime.status("session-a")
        self.assertEqual(stale["freshness"]["state"], "attention_required")
        self.assertFalse(stale["freshness"]["trustworthy"])
        self.assertFalse(stale["pending"]["processor_active"])
        self.assertEqual(stale["failure"]["code"], "stale_process_lease")

        # A later worker may safely replace the stale lease and retry the same
        # immutable queued event.
        recovered = self.runtime.process_next(
            "session-a", lambda event: "updated_quiet"
        )
        self.assertEqual(recovered["status"], "processed")
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["state"], "fresh"
        )

    def test_malformed_control_type_is_recovered_without_crash(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        control_path = self.session_root() / "control.json"
        control_path.write_text(
            json.dumps(
                {
                    "schema": "context-maintain.control.v2",
                    "next_sequence": "not-an-int",
                }
            ),
            encoding="utf-8",
        )
        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["freshness"]["captured_sequence"], 1)
        unchanged = json.loads(control_path.read_text(encoding="utf-8"))
        self.assertEqual(unchanged["next_sequence"], "not-an-int")
        self.runtime.stop(stop("turn-1"))
        repaired = json.loads(control_path.read_text(encoding="utf-8"))
        self.assertEqual(repaired["next_sequence"], 2)
        processed = self.runtime.process_next(
            "session-a", lambda event: "no_change"
        )
        self.assertEqual(processed["status"], "processed")

    def test_malformed_checkpoint_type_blocks_without_false_completion(self) -> None:
        self.pair("turn-1")
        checkpoint_path = self.session_root() / "checkpoint.json"
        checkpoint_path.write_text(
            json.dumps(
                {
                    "schema": "context-maintain.checkpoint.v2",
                    "last_processed_sequence": "not-an-int",
                    "pending_reports": [],
                    "failure": None,
                }
            ),
            encoding="utf-8",
        )
        called = False

        def processor(event: dict[str, object]) -> str:
            nonlocal called
            called = True
            return "no_change"

        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["freshness"]["state"], "unknown")
        self.assertIsNone(status_value["freshness"]["processed_sequence"])
        result = self.runtime.process_next("session-a", processor)
        self.assertEqual(result["reason"], "malformed_checkpoint")
        self.assertFalse(called)
        self.assertTrue(list((self.session_root() / "queue").glob("*.json")))

    def test_typed_but_impossible_checkpoint_does_not_claim_completion(self) -> None:
        self.pair("turn-1")
        checkpoint_path = self.session_root() / "checkpoint.json"
        checkpoint_path.write_text(
            json.dumps(
                {
                    "schema": "context-maintain.checkpoint.v2",
                    "last_processed_sequence": 99,
                    "last_processed_event": "invented-event",
                    "last_processed_content_sha256": "f" * 64,
                    "last_processed_at": "2026-08-17T00:00:00Z",
                    "last_outcome": "no_change",
                    "failure": None,
                    "pending_reports": [],
                }
            ),
            encoding="utf-8",
        )
        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["freshness"]["state"], "unknown")
        self.assertFalse(status_value["freshness"]["trustworthy"])
        called = False

        def processor(event: dict[str, object]) -> str:
            nonlocal called
            called = True
            return "no_change"

        result = self.runtime.process_next("session-a", processor)
        self.assertEqual(result["reason"], "malformed_checkpoint")
        self.assertFalse(called)

    def test_valid_json_with_malformed_queue_types_does_not_advance(self) -> None:
        self.pair("turn-1")
        queue_path = next((self.session_root() / "queue").glob("*.json"))
        value = json.loads(queue_path.read_text(encoding="utf-8"))
        value["sequence"] = "one"
        queue_path.write_text(json.dumps(value), encoding="utf-8")
        result = self.runtime.process_next("session-a", lambda event: "no_change")
        self.assertEqual(result["reason"], "malformed_event")
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["processed_sequence"],
            0,
        )

    def test_top_level_v1_files_are_ignored(self) -> None:
        self.runtime_root.mkdir(parents=True)
        (self.runtime_root / "control.json").write_text(
            '{"protocol_version":1,"next_sequence":900}\n', encoding="utf-8"
        )
        (self.runtime_root / "cursor.json").write_text(
            '{"protocol_version":1,"last_drained_sequence":899}\n',
            encoding="utf-8",
        )
        accepted = self.runtime.user_prompt(user("turn-1"))
        self.assertEqual(accepted["sequence"], 1)
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["processed_sequence"],
            0,
        )


class ProcessingTests(RuntimeTestCase):
    def test_workspace_warning_ignores_ordinary_behind_processing_and_stale(self) -> None:
        self.pair("turn-1")
        behind = self.runtime.workspace_freshness_summary()
        self.assertFalse(behind["freshness_ready"])
        self.assertFalse(behind["warning_required"])

        entered = Event()
        release = Event()

        def processor(event: dict[str, object]) -> str:
            entered.set()
            self.assertTrue(release.wait(timeout=2))
            return "no_change"

        worker = Thread(
            target=lambda: self.runtime.process_next("session-a", processor)
        )
        worker.start()
        self.assertTrue(entered.wait(timeout=2))
        processing = self.runtime.workspace_freshness_summary()
        self.assertFalse(processing["freshness_ready"])
        self.assertFalse(processing["warning_required"])
        release.set()
        worker.join(timeout=2)
        self.assertFalse(worker.is_alive())

        self.pair("turn-2")
        with self.assertRaises(SystemExit):
            self.runtime.process_next(
                "session-a",
                lambda event: (_ for _ in ()).throw(SystemExit("death")),
            )
        stale = self.runtime.workspace_freshness_summary()
        self.assertFalse(stale["freshness_ready"])
        self.assertFalse(stale["warning_required"])

    def test_workspace_warning_requires_three_retry_failures(self) -> None:
        self.pair("turn-1")

        def fail(event: dict[str, object]) -> str:
            raise RuntimeError("retry")

        for attempts in range(1, 4):
            self.runtime.process_next("session-a", fail)
            summary = self.runtime.workspace_freshness_summary()
            self.assertEqual(
                summary["warning_required"], attempts >= 3
            )
            self.assertEqual(
                self.runtime.next_runnable_session_id(),
                None if attempts >= 3 else "session-a",
            )

    def test_prior_session_views_never_include_a_later_session(self) -> None:
        self.runtime.session_start(session_start("old-session"))
        self.runtime.session_start(session_start("new-session"))
        self.pair("turn-new", session="new-session")
        self.runtime.process_next(
            "new-session",
            lambda event: {
                "outcome": "needs_decision",
                "report": {
                    "question": "Later question?",
                    "summary": "later session ambiguity",
                },
            },
        )

        old_summary = self.runtime.workspace_freshness_summary(
            exclude_session_id="old-session"
        )
        self.assertEqual(old_summary["sessions_considered"], 0)
        self.assertTrue(old_summary["freshness_ready"])
        self.assertEqual(
            self.runtime.workspace_pending_reports(
                exclude_session_id="old-session"
            ),
            [],
        )
        self.assertEqual(
            self.runtime.workspace_unresolved_decisions(
                for_session_id="old-session"
            ),
            [],
        )
        self.assertEqual(
            len(
                self.runtime.workspace_unresolved_decisions(
                    for_session_id="new-session"
                )
            ),
            1,
        )

    def test_workspace_readiness_ignores_only_a_pure_unpaired_prompt_tail(self) -> None:
        self.runtime.user_prompt(
            user("turn-1", "UNPAIRED-RAW-PROMPT", session="prior-session")
        )
        prior_status = self.runtime.status("prior-session")
        self.assertEqual(prior_status["freshness"]["state"], "behind")
        self.assertEqual(prior_status["pending"]["waiting_stop"], 1)

        summary = self.runtime.workspace_freshness_summary(
            exclude_session_id="new-session"
        )
        self.assertTrue(summary["freshness_ready"])
        self.assertTrue(summary["ready_for_writes"])
        self.assertFalse(summary["warning_required"])
        self.assertEqual(summary["states"], {"behind": 1})
        self.assertEqual(summary["incomplete_capture_tail_sessions"], 1)
        self.assertEqual(summary["unpaired_tail_sessions"], 1)
        partial = next(
            (self.runtime._session_root("prior-session") / "partials").glob(
                "*.json"
            )
        )
        self.assertIn("UNPAIRED-RAW-PROMPT", partial.read_text(encoding="utf-8"))

        self.runtime.user_prompt(
            user("turn-2", "higher prompt", session="prior-session")
        )
        self.runtime.stop(
            stop("turn-2", "higher answer", session="prior-session")
        )
        confirmed_gap = self.runtime.workspace_freshness_summary(
            exclude_session_id="new-session"
        )
        self.assertFalse(confirmed_gap["freshness_ready"])
        self.assertFalse(confirmed_gap["ready_for_writes"])
        self.assertTrue(confirmed_gap["warning_required"])
        self.assertEqual(
            confirmed_gap["incomplete_capture_tail_sessions"], 0
        )
        self.assertEqual(confirmed_gap["unpaired_tail_sessions"], 0)

    def test_workspace_freshness_summary_separates_reports_from_lag(self) -> None:
        self.pair("turn-a", session="session-a")
        self.runtime.process_next("session-a", lambda event: "no_change")

        self.pair("turn-c", session="session-c")
        self.runtime.process_next(
            "session-c",
            lambda event: {
                "outcome": "needs_decision",
                "report": {"question": "SECRET QUESTION"},
            },
        )

        self.pair("turn-b", session="session-b")

        all_sessions = self.runtime.workspace_freshness_summary()
        self.assertFalse(all_sessions["freshness_ready"])
        self.assertFalse(all_sessions["ready_for_writes"])
        self.assertEqual(all_sessions["states"]["behind"], 1)
        self.assertEqual(all_sessions["states"]["report_pending"], 1)
        self.assertEqual(all_sessions["pending_reports"]["count"], 1)
        self.assertEqual(
            all_sessions["pending_reports"]["kinds"]["needs_decision"], 1
        )

        prior_ready = self.runtime.workspace_freshness_summary(
            exclude_session_id="session-b"
        )
        self.assertTrue(prior_ready["freshness_ready"])
        self.assertFalse(prior_ready["ready_for_writes"])
        self.assertEqual(prior_ready["pending_reports"]["count"], 1)
        self.assertNotIn("SECRET QUESTION", json.dumps(prior_ready))

        report = self.runtime.pending_reports("session-c")[0]
        self.runtime.acknowledge_report("session-c", report["report_id"])
        self.assertEqual(self.runtime.pending_reports("session-c"), [])
        delivered = self.runtime.workspace_freshness_summary(
            exclude_session_id="session-b"
        )
        self.assertTrue(delivered["freshness_ready"])
        self.assertFalse(delivered["ready_for_writes"])
        self.assertEqual(
            [
                item["report_id"]
                for item in self.runtime.workspace_unresolved_decisions(
                    for_session_id="session-b"
                )
            ],
            [report["report_id"]],
        )
        self.runtime.resolve_workspace_reports([report["report_id"]])
        resolved = self.runtime.workspace_freshness_summary(
            exclude_session_id="session-b"
        )
        self.assertTrue(resolved["ready_for_writes"])

    def test_workspace_pending_report_uses_opaque_origin_and_exact_ack(self) -> None:
        self.pair("turn-a", session="prior-session")
        self.runtime.process_next(
            "prior-session",
            lambda event: {
                "outcome": "needs_decision",
                "report": {"question": "Which Owner should receive this?"},
            },
        )
        self.pair("turn-b", session="current-session")
        self.runtime.process_next(
            "current-session",
            lambda event: {
                "outcome": "updated_report",
                "report": {"summary": "current report"},
            },
        )

        prior = self.runtime.workspace_pending_reports(
            exclude_session_id="current-session"
        )
        self.assertEqual(len(prior), 1)
        report = prior[0]
        self.assertEqual(
            report["payload"]["question"],
            "Which Owner should receive this?",
        )
        self.assertRegex(report["origin_session_key"], r"^[0-9a-f]{32}$")
        self.assertNotIn("prior-session", json.dumps(report))
        self.assertNotIn("current report", json.dumps(report))

        with self.assertRaises(ValueError):
            self.runtime.acknowledge_workspace_report(
                "../prior-session",
                report["report_id"],
                "current-session",
            )
        self.assertFalse(
            self.runtime.acknowledge_workspace_report(
                report["origin_session_key"],
                "missing-report",
                "current-session",
            )
        )
        self.assertTrue(
            self.runtime.acknowledge_workspace_report(
                report["origin_session_key"],
                report["report_id"],
                "current-session",
            )
        )
        self.assertEqual(
            self.runtime.workspace_pending_reports(
                exclude_session_id="current-session"
            ),
            [],
        )
        summary = self.runtime.workspace_freshness_summary(
            exclude_session_id="current-session"
        )
        self.assertFalse(summary["ready_for_writes"])
        unresolved = self.runtime.workspace_unresolved_decisions(
            for_session_id="current-session"
        )
        self.assertEqual(
            unresolved,
            [
                {
                    "origin_session_key": report["origin_session_key"],
                    "report_id": report["report_id"],
                    "question": "Which Owner should receive this?",
                    "summary": "",
                }
            ],
        )
        resolution = self.runtime.resolve_workspace_reports(
            [report["report_id"]]
        )
        self.assertEqual(
            resolution["resolved_report_ids"], [report["report_id"]]
        )
        self.assertTrue(
            self.runtime.workspace_freshness_summary(
                exclude_session_id="current-session"
            )["ready_for_writes"]
        )

    def test_decision_delivery_survives_restart_and_reaches_new_session(self) -> None:
        self.pair("turn-1", session="origin-session")
        self.runtime.process_next(
            "origin-session",
            lambda event: {
                "outcome": "needs_decision",
                "report": {
                    "question": "Which Owner?",
                    "summary": "Owner remains unresolved",
                },
            },
        )
        original = self.runtime.pending_reports("origin-session")[0]
        self.assertTrue(
            self.runtime.acknowledge_report(
                "origin-session", original["report_id"]
            )
        )
        self.assertFalse(
            self.runtime.acknowledge_report(
                "origin-session", original["report_id"]
            )
        )
        self.assertEqual(self.runtime.pending_reports("origin-session"), [])

        reopened = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
        )
        self.assertEqual(reopened.pending_reports("origin-session"), [])
        for_new_session = reopened.workspace_pending_reports(
            exclude_session_id="new-session"
        )
        self.assertEqual(len(for_new_session), 1)
        delivered = for_new_session[0]
        self.assertEqual(delivered["report_id"], original["report_id"])
        self.assertTrue(
            reopened.acknowledge_workspace_report(
                delivered["origin_session_key"],
                delivered["report_id"],
                "new-session",
            )
        )
        self.assertFalse(
            reopened.acknowledge_workspace_report(
                delivered["origin_session_key"],
                delivered["report_id"],
                "new-session",
            )
        )
        self.assertEqual(
            reopened.workspace_pending_reports(
                exclude_session_id="new-session"
            ),
            [],
        )
        self.assertEqual(
            len(
                reopened.workspace_pending_reports(
                    exclude_session_id="another-new-session"
                )
            ),
            1,
        )
        self.assertEqual(
            reopened.workspace_unresolved_decisions(
                for_session_id="another-new-session"
            )[0]["report_id"],
            original["report_id"],
        )

        first = reopened.resolve_workspace_reports([original["report_id"]])
        second = reopened.resolve_workspace_reports([original["report_id"]])
        self.assertEqual(first["resolved_report_ids"], [original["report_id"]])
        self.assertEqual(second["resolved_report_ids"], [])
        self.assertEqual(
            reopened.workspace_unresolved_decisions(
                for_session_id="another-new-session"
            ),
            [],
        )

    def test_updated_report_is_removed_on_delivery_not_resolution(self) -> None:
        self.pair("turn-1")
        self.runtime.process_next(
            "session-a",
            lambda event: {
                "outcome": "updated_report",
                "report": {"summary": "durable update", "changed_paths": []},
            },
        )
        report = self.runtime.pending_reports("session-a")[0]
        ignored = self.runtime.resolve_workspace_reports([report["report_id"]])
        self.assertEqual(ignored["resolved_report_ids"], [])
        self.assertEqual(len(self.runtime.pending_reports("session-a")), 1)
        self.assertTrue(
            self.runtime.acknowledge_report("session-a", report["report_id"])
        )
        self.assertEqual(self.runtime.pending_reports("session-a"), [])
        self.assertEqual(
            self.runtime.status("session-a")["pending"]["reports"], 0
        )

    def test_unresolved_decision_view_is_bounded_and_omits_other_payload(self) -> None:
        self.pair("turn-1")
        self.runtime.process_next(
            "session-a",
            lambda event: {
                "outcome": "needs_decision",
                "report": {
                    "question": "Q" * 700,
                    "summary": "S" * 900,
                    "raw": "DO-NOT-EXPOSE",
                    "changed_paths": ["private/path"],
                },
            },
        )
        unresolved = self.runtime.workspace_unresolved_decisions(
            for_session_id="session-a"
        )
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(len(unresolved[0]["question"]), 500)
        self.assertEqual(len(unresolved[0]["summary"]), 800)
        rendered = json.dumps(unresolved)
        self.assertNotIn("DO-NOT-EXPOSE", rendered)
        self.assertNotIn("private/path", rendered)

    def test_checkpoint_strictly_validates_bounded_delivery_recipients(self) -> None:
        self.pair("turn-1")
        self.runtime.process_next(
            "session-a",
            lambda event: {
                "outcome": "needs_decision",
                "report": {"question": "Owner?", "summary": "unresolved"},
            },
        )
        checkpoint_path = self.session_root() / "checkpoint.json"
        original = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        self.assertEqual(original["pending_reports"][0]["delivered_to"], [])

        variants: list[dict[str, object]] = []
        missing = json.loads(json.dumps(original))
        missing["pending_reports"][0].pop("delivered_to")
        variants.append(missing)
        duplicate = json.loads(json.dumps(original))
        duplicate["pending_reports"][0]["delivered_to"] = ["a" * 32] * 2
        variants.append(duplicate)
        oversized = json.loads(json.dumps(original))
        oversized["pending_reports"][0]["delivered_to"] = [
            f"{index:032x}" for index in range(33)
        ]
        variants.append(oversized)
        malformed = json.loads(json.dumps(original))
        malformed["pending_reports"][0]["delivered_to"] = ["not-opaque"]
        variants.append(malformed)

        for variant in variants:
            checkpoint_path.write_text(json.dumps(variant), encoding="utf-8")
            self.assertEqual(
                self.runtime.status("session-a")["freshness"]["state"],
                "unknown",
            )
        checkpoint_path.write_text(json.dumps(original), encoding="utf-8")
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["state"],
            "report_pending",
        )

    def test_agent_state_survives_compaction_and_rejects_invalid_state(self) -> None:
        initial = self.runtime.load_agent_state("session-a")
        self.assertIsNone(initial["thread_id"])
        self.assertFalse(initial["grounded"])
        self.assertFalse(initial["workspace_bound"])
        saved = self.runtime.save_agent_state(
            "session-a",
            {
                "thread_id": "thread-123",
                "grounded": True,
                "workspace_bound": True,
                "summary": "목표와 현재 cursor를 확인했다.",
            },
        )
        self.assertIsNotNone(saved["updated_at"])
        self.runtime.session_start(session_start(source="compact"))
        self.assertEqual(self.runtime.load_agent_state("session-a"), saved)

        with self.assertRaises(RuntimeProtocolError):
            self.runtime.save_agent_state(
                "session-a",
                {
                    "thread_id": " ",
                    "grounded": True,
                    "workspace_bound": True,
                    "summary": "invalid",
                },
            )
        self.assertEqual(self.runtime.load_agent_state("session-a"), saved)

    def test_malformed_agent_state_is_quarantined_without_exposure(self) -> None:
        session_root = self.runtime.session_runtime_root("session-a")
        state_path = session_root / "agent-state.json"
        state_path.write_text(
            '{"schema":"wrong","secret":"DO-NOT-EXPOSE"}\n',
            encoding="utf-8",
        )
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.load_agent_state("session-a")

        reset = self.runtime.quarantine_agent_state("session-a")
        self.assertEqual(reset, self.runtime.load_agent_state("session-a"))
        self.assertIsNone(reset["thread_id"])
        self.assertFalse(reset["grounded"])
        self.assertFalse(reset["workspace_bound"])
        self.assertNotIn("DO-NOT-EXPOSE", json.dumps(reset))
        self.assertNotIn(
            "DO-NOT-EXPOSE",
            json.dumps(self.runtime.status("session-a")),
        )
        quarantined = list((session_root / "quarantine").glob("*.json"))
        self.assertEqual(len(quarantined), 1)
        self.assertIn(
            "DO-NOT-EXPOSE", quarantined[0].read_text(encoding="utf-8")
        )

    def test_valid_agent_state_is_not_quarantined_by_recovery_handler(self) -> None:
        saved = self.runtime.save_agent_state(
            "session-a",
            {
                "thread_id": "thread-123",
                "grounded": True,
                "workspace_bound": False,
                "summary": "forming workspace",
            },
        )
        recovered = self.runtime.quarantine_agent_state(
            "session-a", "resume_failure"
        )
        self.assertEqual(recovered, saved)
        self.assertEqual(
            list((self.session_root() / "quarantine").glob("*.json")), []
        )

    def test_agent_state_symlink_is_quarantined_without_touching_target(self) -> None:
        session_root = self.runtime.session_runtime_root("session-a")
        outside = Path(self.temporary.name) / "outside-agent-state.json"
        outside.write_text('{"external":"KEEP"}\n', encoding="utf-8")
        state_path = session_root / "agent-state.json"
        state_path.symlink_to(outside)

        with self.assertRaises(RuntimeProtocolError):
            self.runtime.load_agent_state("session-a")
        reset = self.runtime.quarantine_agent_state("session-a")
        self.assertFalse(state_path.is_symlink())
        self.assertEqual(
            outside.read_text(encoding="utf-8"), '{"external":"KEEP"}\n'
        )
        self.assertFalse(reset["workspace_bound"])
        quarantined = list((session_root / "quarantine").iterdir())
        self.assertEqual(len(quarantined), 1)
        self.assertTrue(quarantined[0].is_symlink())

    def test_last_committed_event_returns_only_valid_checkpoint_identity(self) -> None:
        self.assertIsNone(self.runtime.last_committed_event("session-a"))
        self.pair("turn-1", prompt="SECRET-PROMPT", assistant="SECRET-ANSWER")
        self.assertIsNone(self.runtime.last_committed_event("session-a"))
        event = json.loads(
            next((self.session_root() / "queue").glob("*.json")).read_text(
                encoding="utf-8"
            )
        )
        self.runtime.process_next("session-a", lambda value: "no_change")
        committed = self.runtime.last_committed_event("session-a")
        self.assertEqual(
            committed,
            {
                "sequence": 1,
                "event_id": event["event_id"],
                "content_sha256": event["content_sha256"],
            },
        )
        self.assertNotIn("SECRET", json.dumps(committed))

        (self.session_root() / "checkpoint.json").write_text(
            '{"schema":"context-maintain.checkpoint.v2",'
            '"last_processed_sequence":"bad"}\n',
            encoding="utf-8",
        )
        self.assertIsNone(self.runtime.last_committed_event("session-a"))

    def _assert_preexisting_ledger_conflict_blocks_processor(self) -> None:
        called = False

        def processor(event: dict[str, object]) -> str:
            nonlocal called
            called = True
            return "no_change"

        result = self.runtime.process_next("session-a", processor)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["reason"], "ledger_conflict")
        self.assertFalse(called)
        status_value = self.runtime.status("session-a")
        self.assertEqual(
            status_value["freshness"]["state"],
            "attention_required",
        )
        self.assertEqual(status_value["freshness"]["processed_sequence"], 0)
        self.assertGreater(status_value["integrity"]["conflicts"], 0)
        self.assertTrue(list((self.session_root() / "queue").glob("*.json")))

    def test_differing_user_replay_blocks_before_processor(self) -> None:
        self.pair("turn-1", prompt="ORIGINAL-PROMPT")
        conflict = self.runtime.user_prompt(
            user("turn-1", "DIFFERENT-PROMPT")
        )
        self.assertTrue(conflict["conflict"])
        self._assert_preexisting_ledger_conflict_blocks_processor()

    def test_differing_stop_replay_blocks_before_processor(self) -> None:
        self.pair("turn-1", assistant="ORIGINAL-ANSWER")
        conflict = self.runtime.stop(stop("turn-1", "DIFFERENT-ANSWER"))
        self.assertTrue(conflict["conflict"])
        self._assert_preexisting_ledger_conflict_blocks_processor()

    def test_late_post_tool_use_blocks_before_processor(self) -> None:
        self.pair("turn-1")
        conflict = self.runtime.post_tool_use(
            post_tool(
                "turn-1",
                tool_use_id="late-tool",
                tool_input={"path": "current/state.md"},
                tool_response={"status": "completed"},
            )
        )
        self.assertTrue(conflict["conflict"])
        self.assertTrue(conflict["late"])
        self._assert_preexisting_ledger_conflict_blocks_processor()

    def test_malformed_queue_ledger_blocks_before_processor(self) -> None:
        self.pair("turn-1")
        ledger_path = next((self.session_root() / "ledger").glob("*.json"))
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["content_sha256"] = "f" * 64
        ledger_path.write_text(json.dumps(ledger) + "\n", encoding="utf-8")

        called = False

        def processor(event: dict[str, object]) -> str:
            nonlocal called
            called = True
            return "no_change"

        result = self.runtime.process_next("session-a", processor)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["reason"], "malformed_queue_ledger")
        self.assertFalse(called)
        status_value = self.runtime.status("session-a")
        self.assertEqual(
            status_value["freshness"]["state"],
            "attention_required",
        )
        self.assertEqual(status_value["freshness"]["processed_sequence"], 0)
        self.assertGreater(status_value["integrity"]["malformed"], 0)
        self.assertTrue(list((self.session_root() / "queue").glob("*.json")))

    def test_conflict_during_processing_never_commits_outcome(self) -> None:
        self.pair("turn-1", assistant="ORIGINAL-ANSWER")

        def processor(event: dict[str, object]) -> dict[str, object]:
            conflict = self.runtime.stop(
                stop("turn-1", "DIFFERENT-DURING-PROCESSING")
            )
            self.assertTrue(conflict["conflict"])
            return {
                "outcome": "updated_report",
                "summary": "must not commit",
            }

        result = self.runtime.process_next("session-a", processor)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["reason"], "ledger_conflict")
        status_value = self.runtime.status("session-a")
        self.assertEqual(
            status_value["freshness"]["state"],
            "attention_required",
        )
        self.assertEqual(status_value["freshness"]["processed_sequence"], 0)
        self.assertEqual(status_value["pending"]["reports"], 0)
        self.assertFalse((self.session_root() / "processing.json").exists())
        self.assertTrue(list((self.session_root() / "queue").glob("*.json")))

    def test_processor_failure_preserves_raw_event_and_retry_state(self) -> None:
        self.pair("turn-1", prompt="KEEP-RAW-PROMPT", assistant="KEEP-RAW-ANSWER")

        def failing(event: dict[str, object]) -> str:
            raise RuntimeError("failure containing KEEP-RAW-PROMPT")

        failed = self.runtime.process_next("session-a", failing)
        self.assertEqual(failed["status"], "retry")
        queue_path = next((self.session_root() / "queue").glob("*.json"))
        self.assertIn("KEEP-RAW-PROMPT", queue_path.read_text(encoding="utf-8"))
        status_value = self.runtime.status("session-a")
        self.assertTrue(status_value["failure"]["retry_pending"])
        self.assertEqual(status_value["failure"]["attempts"], 1)
        self.assertNotIn("KEEP-RAW-PROMPT", json.dumps(status_value))

        retried = self.runtime.process_next(
            "session-a", lambda event: "updated_quiet"
        )
        self.assertEqual(retried["status"], "processed")
        self.assertFalse(queue_path.exists())
        self.assertFalse(self.runtime.status("session-a")["failure"]["retry_pending"])

    def test_processing_defer_preserves_queue_and_retry_budget(self) -> None:
        self.pair("turn-1")

        def deferred(event: dict[str, object]) -> str:
            raise ProcessingDeferredError("prior session became pending")

        first = self.runtime.process_next("session-a", deferred)
        self.assertEqual(
            first,
            {
                "status": "deferred",
                "reason": "prior_session_pending",
                "sequence": 1,
                "work_generation": first["work_generation"],
            },
        )
        self.assertEqual(len(first["work_generation"]), 64)
        self.assertTrue(list((self.session_root() / "queue").glob("*.json")))
        self.assertFalse((self.session_root() / "processing.json").exists())
        first_status = self.runtime.status("session-a")
        self.assertFalse(first_status["failure"]["retry_pending"])
        self.assertEqual(first_status["failure"]["attempts"], 0)
        self.assertEqual(first_status["counts"]["processor_failures"], 0)

        failed = self.runtime.process_next(
            "session-a",
            lambda event: (_ for _ in ()).throw(RuntimeError("ordinary")),
        )
        self.assertEqual(failed["status"], "retry")
        before = self.runtime.status("session-a")
        self.assertEqual(before["failure"]["attempts"], 1)

        second = self.runtime.process_next("session-a", deferred)
        self.assertEqual(second["status"], "deferred")
        after = self.runtime.status("session-a")
        self.assertEqual(after["failure"]["attempts"], 1)
        self.assertEqual(after["counts"]["processor_failures"], 1)
        self.assertTrue(list((self.session_root() / "queue").glob("*.json")))

    def test_only_committable_outcomes_advance_cursor(self) -> None:
        self.pair("turn-1")
        rejected = self.runtime.process_next(
            "session-a", lambda event: {"outcome": "freshness_failed"}
        )
        self.assertEqual(rejected["status"], "retry")
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["processed_sequence"],
            0,
        )
        accepted = self.runtime.process_next(
            "session-a", lambda event: {"outcome": "no_change"}
        )
        self.assertEqual(accepted["status"], "processed")
        self.assertEqual(
            self.runtime.status("session-a")["freshness"]["processed_sequence"],
            1,
        )

    def test_success_removes_raw_and_retains_digest_ledger_only(self) -> None:
        prompt = "DELETE-ME-PROMPT"
        assistant = "DELETE-ME-ANSWER"
        self.pair("turn-1", prompt=prompt, assistant=assistant)
        delivered: list[dict[str, object]] = []
        result = self.runtime.process_next(
            "session-a",
            lambda event: delivered.append(event) or "no_change",
        )
        self.assertEqual(result["status"], "processed")
        self.assertEqual(delivered[0]["prompt"], prompt)
        self.assertEqual(delivered[0]["assistant"], assistant)

        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.session_root().rglob("*.json")
        )
        self.assertNotIn(prompt, runtime_text)
        self.assertNotIn(assistant, runtime_text)
        ledger = json.loads(
            next((self.session_root() / "ledger").glob("*.json")).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(ledger["status"], "completed")
        self.assertEqual(len(ledger["prompt_sha256"]), 64)
        self.assertEqual(len(ledger["assistant_sha256"]), 64)

    def test_needs_decision_advances_with_atomic_pending_report(self) -> None:
        self.pair("turn-1")
        result = self.runtime.process_next(
            "session-a",
            lambda event: {
                "outcome": "needs_decision",
                "report": {"question": "Which Owner should receive this?"},
            },
        )
        self.assertEqual(result["status"], "processed")
        checkpoint = json.loads(
            (self.session_root() / "checkpoint.json").read_text(encoding="utf-8")
        )
        self.assertEqual(checkpoint["last_processed_sequence"], 1)
        self.assertEqual(len(checkpoint["pending_reports"]), 1)
        report = self.runtime.pending_reports("session-a")[0]
        self.assertEqual(report["kind"], "needs_decision")
        self.assertEqual(
            report["payload"]["question"], "Which Owner should receive this?"
        )
        status_value = self.runtime.status("session-a")
        self.assertEqual(status_value["pending"]["reports"], 1)
        self.assertNotIn("Which Owner", json.dumps(status_value))
        self.assertTrue(
            self.runtime.acknowledge_report("session-a", report["report_id"])
        )
        self.assertEqual(self.runtime.pending_reports("session-a"), [])
        self.assertEqual(self.runtime.status("session-a")["pending"]["reports"], 1)
        unresolved = self.runtime.workspace_unresolved_decisions(
            for_session_id="session-a"
        )
        self.assertEqual(unresolved[0]["report_id"], report["report_id"])
        self.runtime.resolve_workspace_reports([report["report_id"]])
        self.assertEqual(self.runtime.status("session-a")["pending"]["reports"], 0)

    def test_checkpoint_crash_residue_does_not_reprocess_event(self) -> None:
        fault = FailOnce("after_checkpoint_before_cleanup")
        crashing = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
            fault_injector=fault,
        )
        crashing.user_prompt(user("turn-1", "raw prompt"))
        crashing.stop(stop("turn-1", "raw answer"))
        calls = 0

        def processor(event: dict[str, object]) -> str:
            nonlocal calls
            calls += 1
            return "updated_quiet"

        with self.assertRaises(OSError):
            crashing.process_next("session-a", processor)
        self.assertEqual(calls, 1)
        self.assertTrue(list((self.session_root() / "queue").glob("*.json")))

        recovered = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
        )
        result = recovered.process_next("session-a", processor)
        self.assertEqual(result["status"], "idle")
        self.assertEqual(calls, 1)
        self.assertFalse(list((self.session_root() / "queue").glob("*.json")))
        status_value = recovered.status("session-a")
        self.assertEqual(status_value["freshness"]["state"], "fresh")
        self.assertFalse((self.session_root() / "processing.json").exists())

    def test_completed_ledger_crash_is_recoverable_cleanup_not_fresh(self) -> None:
        self.pair(
            "turn-1",
            prompt="COMPLETED-RAW-PROMPT",
            assistant="COMPLETED-RAW-ANSWER",
        )
        crashing = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
            fault_injector=FailOnce(
                "after_completed_ledger_before_raw_cleanup"
            ),
        )
        calls = 0

        def processor(event: dict[str, object]) -> str:
            nonlocal calls
            calls += 1
            return "updated_quiet"

        with self.assertRaises(OSError):
            crashing.process_next("session-a", processor)
        self.assertEqual(calls, 1)
        queue_path = next((self.session_root() / "queue").glob("*.json"))
        self.assertIn(
            "COMPLETED-RAW-PROMPT",
            queue_path.read_text(encoding="utf-8"),
        )

        recovered = MaintainRuntime(
            runtime_root=self.runtime_root,
            workspace_id=WORKSPACE,
        )
        residue = recovered.status("session-a")
        self.assertEqual(residue["freshness"]["state"], "behind")
        self.assertEqual(residue["pending"]["cleanup_residue"], 1)
        self.assertEqual(
            recovered.next_runnable_session_id(),
            "session-a",
        )

        result = recovered.process_next("session-a", processor)
        self.assertEqual(result["status"], "idle")
        self.assertEqual(calls, 1)
        self.assertFalse(queue_path.exists())
        self.assertEqual(
            recovered.status("session-a")["freshness"]["state"],
            "fresh",
        )

    def test_status_never_exposes_raw_conversation(self) -> None:
        self.pair(
            "turn-1",
            prompt="STATUS-MUST-NOT-SHOW-PROMPT",
            assistant="STATUS-MUST-NOT-SHOW-ANSWER",
        )
        rendered = json.dumps(self.runtime.status("session-a"), ensure_ascii=False)
        self.assertNotIn("STATUS-MUST-NOT-SHOW-PROMPT", rendered)
        self.assertNotIn("STATUS-MUST-NOT-SHOW-ANSWER", rendered)


class ToolEvidenceTests(RuntimeTestCase):
    def test_oversized_tool_payload_is_rejected_without_partial_hash(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        with self.assertRaises(RuntimeProtocolError) as caught:
            self.runtime.post_tool_use(
                post_tool(
                    "turn-1",
                    tool_name="Bash",
                    tool_input={"command": "x"},
                    tool_response={"output": "S" * 1_048_577},
                )
            )
        self.assertIn("capture bound", str(caught.exception))
        self.assertEqual(
            list((self.session_root() / "tool-evidence").rglob("*.json")),
            [],
        )
        self.assertNotIn(
            "SSSSSS",
            json.dumps(self.runtime.status("session-a")),
        )

    def test_apply_patch_and_explicit_paths_are_sanitized_into_stop_event(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        recorded = self.runtime.post_tool_use(
            post_tool(
                "turn-1",
                tool_input={
                    "patch": (
                        "*** Add File: records/new.md\nSECRET PATCH BODY\n"
                        "*** Update File: current/state.md\n"
                        "*** Delete File: ../outside.md\n"
                    ),
                    "workdir": "/project",
                    "file_path": "current/state.md",
                    "path": "../../SECRET-PATH",
                },
                tool_response={"status": "completed", "output": "SECRET OUTPUT"},
            )
        )
        self.assertTrue(recorded["recorded"])
        evidence_path = next(
            (self.session_root() / "tool-evidence").rglob("*.json")
        )
        durable = evidence_path.read_text(encoding="utf-8")
        self.assertNotIn("SECRET PATCH BODY", durable)
        self.assertNotIn("SECRET OUTPUT", durable)
        self.assertNotIn("SECRET-PATH", durable)

        paired = self.runtime.stop(stop("turn-1"))
        self.assertTrue(paired["paired"])
        event = json.loads(
            next((self.session_root() / "queue").glob("*.json")).read_text(
                encoding="utf-8"
            )
        )
        facts = event["tool_evidence"][0]["facts"]
        self.assertEqual(
            facts["patch_paths"],
            [
                {"operation": "add", "path": "records/new.md"},
                {"operation": "update", "path": "current/state.md"},
            ],
        )
        self.assertEqual(
            facts["paths"],
            [
                {"field": "file_path", "value": "current/state.md"},
            ],
        )

    def test_only_normalized_project_relative_paths_leave_hash_only_boundary(
        self,
    ) -> None:
        self.runtime.user_prompt(user("turn-1"))
        self.runtime.post_tool_use(
            post_tool(
                "turn-1",
                tool_input={
                    "patch": (
                        "*** Add File: /tmp/ABSOLUTE-SECRET\n+x\n"
                        "*** Add File: ~/HOME-SECRET\n+x\n"
                        "*** Update File: nested/../ESCAPE-SECRET\n+x\n"
                        "*** Update File: ./current//state.md\n+x\n"
                    ),
                    "cwd": "/Users/private/project",
                    "workdir": "C:\\private\\project",
                    "path": "~someone/private",
                    "file": "file:///private/external",
                    "file_path": "./records//evidence.md",
                },
                tool_response={"status": "completed"},
            )
        )
        record = json.loads(
            next((self.session_root() / "tool-evidence").rglob("*.json"))
            .read_text(encoding="utf-8")
        )
        self.assertEqual(
            record["facts"]["patch_paths"],
            [{"operation": "update", "path": "current/state.md"}],
        )
        self.assertEqual(
            record["facts"]["paths"],
            [{"field": "file_path", "value": "records/evidence.md"}],
        )
        self.assertEqual(len(record["input_sha256"]), 64)
        rendered = json.dumps(record)
        for secret in (
            "ABSOLUTE-SECRET",
            "HOME-SECRET",
            "ESCAPE-SECRET",
            "/Users/private/project",
            "C:\\private\\project",
            "~someone/private",
            "file:///private/external",
        ):
            self.assertNotIn(secret, rendered)

    def test_safe_test_command_and_small_result_omit_arguments_and_output(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        self.runtime.post_tool_use(
            post_tool(
                "turn-1",
                tool_name="functions.exec_command",
                tool_input={
                    "cmd": "python3 -m unittest private.test_secret -q",
                    "workdir": "/project",
                },
                tool_response={
                    "exit_code": 0,
                    "status": "completed",
                    "output": "TOP-SECRET" * 10000,
                },
            )
        )
        record = json.loads(
            next((self.session_root() / "tool-evidence").rglob("*.json")).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            record["facts"]["command"],
            {"kind": "test", "summary": "python -m unittest"},
        )
        self.assertEqual(
            record["facts"]["result"],
            {"exit_code": 0, "status": "completed"},
        )
        rendered = json.dumps(record)
        self.assertNotIn("private.test_secret", rendered)
        self.assertNotIn("TOP-SECRET", rendered)
        status_rendered = json.dumps(self.runtime.status("session-a"))
        self.assertNotIn("private.test_secret", status_rendered)
        self.assertNotIn("tool-use-1", status_rendered)

    def test_unsafe_command_is_hash_only_and_duplicate_conflict_is_stable(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        original = post_tool(
            "turn-1",
            tool_name="Bash",
            tool_input={"command": "TOKEN=SECRET pytest tests/test_secret.py"},
            tool_response={"output": "SECRET"},
        )
        self.assertTrue(self.runtime.post_tool_use(original)["recorded"])
        self.assertTrue(self.runtime.post_tool_use(original)["duplicate"])
        conflict = dict(original)
        conflict["tool_response"] = {"output": "different"}
        self.assertTrue(self.runtime.post_tool_use(conflict)["conflict"])

        path = next((self.session_root() / "tool-evidence").rglob("*.json"))
        record = json.loads(path.read_text(encoding="utf-8"))
        self.assertNotIn("command", record["facts"])
        self.assertNotIn("SECRET", json.dumps(record))
        blocked = self.runtime.stop(stop("turn-1"))
        self.assertTrue(blocked["conflict"])

    def test_turn_isolation_and_success_cleanup(self) -> None:
        self.runtime.user_prompt(user("turn-1"))
        self.runtime.post_tool_use(
            post_tool("turn-1", tool_use_id="tool-one")
        )
        self.runtime.stop(stop("turn-1"))
        self.runtime.user_prompt(user("turn-2"))
        self.runtime.post_tool_use(
            post_tool(
                "turn-2",
                tool_use_id="tool-two",
                tool_input="*** Add File: records/two.md\n+x",
            )
        )
        self.runtime.stop(stop("turn-2"))

        delivered: list[dict[str, object]] = []
        first = self.runtime.process_next(
            "session-a", lambda event: delivered.append(event) or "no_change"
        )
        self.assertEqual(first["status"], "processed")
        self.assertEqual(
            delivered[0]["tool_evidence"][0]["tool_use_id"], "tool-one"
        )
        remaining = list((self.session_root() / "tool-evidence").rglob("*.json"))
        self.assertEqual(len(remaining), 1)
        self.assertNotIn("tool-one", remaining[0].read_text(encoding="utf-8"))

        second = self.runtime.process_next(
            "session-a", lambda event: delivered.append(event) or "no_change"
        )
        self.assertEqual(second["status"], "processed")
        self.assertEqual(
            delivered[1]["tool_evidence"][0]["tool_use_id"], "tool-two"
        )
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in self.session_root().rglob("*.json")
        )
        self.assertNotIn("tool-one", runtime_text)
        self.assertNotIn("tool-two", runtime_text)
        self.assertNotIn("current/state.md", runtime_text)
        self.assertNotIn("records/two.md", runtime_text)
        ledger = json.loads(
            sorted((self.session_root() / "ledger").glob("*.json"))[0].read_text(
                encoding="utf-8"
            )
        )
        self.assertNotIn("tool-one", json.dumps(ledger))
        self.assertIn("tool_evidence_sha256", ledger)

    def test_malformed_and_symlink_evidence_are_rejected(self) -> None:
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.post_tool_use(
                {
                    "hook_event_name": "PostToolUse",
                    "session_id": "session-a",
                    "turn_id": "turn-1",
                    "tool_name": "Bash",
                    "tool_use_id": "tool-1",
                    "tool_input": {},
                }
            )

        self.runtime.user_prompt(user("turn-1"))
        key = next((self.session_root() / "ledger").glob("*.json")).stem
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        turn_root = self.session_root() / "tool-evidence" / key
        turn_root.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(RuntimeProtocolError):
            self.runtime.post_tool_use(post_tool("turn-1"))
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
