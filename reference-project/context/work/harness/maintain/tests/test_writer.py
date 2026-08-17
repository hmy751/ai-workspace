from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import stat
import tempfile
import threading
import unittest

from context.work.harness.maintain.writer import (
    BrokenMarkdownLinkError,
    CompletedWriteConflictError,
    JOURNAL_FILENAME,
    JournalConflictError,
    StaleBaselineError,
    UnsafeWriteError,
    WriteProposal,
    acknowledge_transaction,
    apply_writes,
    recover_journal,
    sha256_text,
)


class GuardedWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.workspace = root / "workspaces" / "005-maintain"
        self.runtime = root / "runtime" / "session-1"
        for relative in (
            "current/memory",
            "records/receipts/verify",
            "output",
            "source/raw",
        ):
            (self.workspace / relative).mkdir(parents=True, exist_ok=True)
        (self.workspace / "current/state.md").write_text(
            "# State\n\nold\n", encoding="utf-8"
        )
        (self.workspace / "current/memory/index.md").write_text(
            "# Memory\n", encoding="utf-8"
        )
        (self.workspace / "output/index.md").write_text(
            "# Output\n", encoding="utf-8"
        )
        (self.workspace / "source/index.md").write_text(
            "# Source\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def proposal(
        self, path: str, content: str, *, expected: str | None = None
    ) -> WriteProposal:
        return WriteProposal(
            path=path,
            expected_sha256=expected,
            content=content,
        )

    def existing_proposal(self, path: str, content: str) -> WriteProposal:
        old = (self.workspace / path).read_text(encoding="utf-8")
        return self.proposal(path, content, expected=sha256_text(old))

    def test_updates_allowed_current_markdown(self) -> None:
        proposal = self.existing_proposal(
            "current/state.md", "# State\n\nnew\n"
        )

        result = apply_writes(self.workspace, self.runtime, [proposal])

        self.assertEqual(result.changed_paths, ("current/state.md",))
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            "# State\n\nnew\n",
        )
        self.assertFalse((self.runtime / JOURNAL_FILENAME).exists())

    def test_replacement_preserves_existing_markdown_mode(self) -> None:
        target = self.workspace / "current/state.md"
        os.chmod(target, 0o640)

        apply_writes(
            self.workspace,
            self.runtime,
            [self.existing_proposal("current/state.md", "# State\n\nnew\n")],
        )

        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o640)

    def test_new_markdown_uses_readable_non_executable_mode(self) -> None:
        target = self.workspace / "records/2026-08-17-new-record.md"

        apply_writes(
            self.workspace,
            self.runtime,
            [
                self.proposal(
                    "records/2026-08-17-new-record.md", "# Record\n"
                )
            ],
        )

        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o644)

    def test_identical_content_is_a_no_op(self) -> None:
        proposal = self.existing_proposal(
            "current/state.md", "# State\n\nold\n"
        )

        result = apply_writes(self.workspace, self.runtime, [proposal])

        self.assertEqual(result.changed_paths, ())
        self.assertFalse((self.runtime / JOURNAL_FILENAME).exists())

    def test_keyed_no_op_replay_does_not_overwrite_a_later_update(self) -> None:
        no_op = self.existing_proposal(
            "current/state.md", "# State\n\nold\n"
        )
        no_op_key = "session-1:event-no-op:digest-1"
        self.assertEqual(
            apply_writes(
                self.workspace,
                self.runtime,
                [no_op],
                transaction_key=no_op_key,
            ).changed_paths,
            (),
        )
        later = self.existing_proposal(
            "current/state.md", "# State\n\nlater update\n"
        )
        apply_writes(
            self.workspace,
            self.runtime,
            [later],
            transaction_key="session-2:event-update:digest-2",
        )

        replay = apply_writes(
            self.workspace,
            self.runtime,
            [no_op],
            transaction_key=no_op_key,
        )

        self.assertEqual(replay.changed_paths, ())
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            later.content,
        )

    def test_creates_a_dated_record(self) -> None:
        result = apply_writes(
            self.workspace,
            self.runtime,
            [
                self.proposal(
                    "records/2026-08-17-maintain-decision.md",
                    "# Decision\n",
                )
            ],
        )

        self.assertEqual(
            result.changed_paths,
            ("records/2026-08-17-maintain-decision.md",),
        )
        self.assertEqual(
            (
                self.workspace
                / "records/2026-08-17-maintain-decision.md"
            ).read_text(encoding="utf-8"),
            "# Decision\n",
        )

    def test_updates_records_index_with_same_transaction_record(self) -> None:
        index = self.workspace / "records/index.md"
        index.write_text("# Records\n", encoding="utf-8")

        result = apply_writes(
            self.workspace,
            self.runtime,
            [
                self.existing_proposal(
                    "records/index.md",
                    "# Records\n\n- [decision](2026-08-17-decision.md)\n",
                ),
                self.proposal(
                    "records/2026-08-17-decision.md",
                    "# Decision\n",
                ),
            ],
        )

        self.assertEqual(
            result.changed_paths,
            ("records/index.md", "records/2026-08-17-decision.md"),
        )

    def test_rejects_machine_product_escape_and_symlink_targets(self) -> None:
        outside = Path(self.temporary_directory.name) / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        (self.workspace / "current/link.md").symlink_to(outside)
        forbidden = (
            "current/status.json",
            "records/receipts/verify/verify-1.json",
            "source/raw/transcript.md",
            "product/app.md",
            "../other-workspace/current/state.md",
            str(outside),
            "current/link.md",
        )

        for path in forbidden:
            with self.subTest(path=path):
                with self.assertRaises(UnsafeWriteError):
                    apply_writes(
                        self.workspace,
                        self.runtime,
                        [self.proposal(path, "new\n")],
                    )

        self.assertEqual(outside.read_text(encoding="utf-8"), "outside\n")

    def test_stale_baseline_rejects_all_writes(self) -> None:
        state = self.workspace / "current/state.md"
        memory = self.workspace / "current/memory/index.md"
        memory_before = memory.read_text(encoding="utf-8")
        proposals = [
            self.proposal(
                "current/state.md",
                "# State\n\nproposed\n",
                expected=sha256_text("# State\n\nnot-current\n"),
            ),
            self.proposal(
                "current/memory/index.md",
                "# Memory\n\nchanged\n",
                expected=sha256_text(memory_before),
            ),
        ]

        with self.assertRaises(StaleBaselineError):
            apply_writes(self.workspace, self.runtime, proposals)

        self.assertEqual(state.read_text(encoding="utf-8"), "# State\n\nold\n")
        self.assertEqual(memory.read_text(encoding="utf-8"), memory_before)
        self.assertFalse((self.runtime / JOURNAL_FILENAME).exists())

    def test_crash_mid_transaction_is_completed_by_recovery(self) -> None:
        proposals = [
            self.existing_proposal(
                "current/state.md", "# State\n\nnew\n"
            ),
            self.existing_proposal(
                "current/memory/index.md", "# Memory\n\nnew\n"
            ),
        ]
        replaced = 0

        def crash_after_first(_target: Path) -> None:
            nonlocal replaced
            replaced += 1
            if replaced == 1:
                raise RuntimeError("simulated process crash")

        with self.assertRaisesRegex(RuntimeError, "simulated process crash"):
            apply_writes(
                self.workspace,
                self.runtime,
                proposals,
                after_replace=crash_after_first,
            )

        self.assertTrue((self.runtime / JOURNAL_FILENAME).exists())
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            "# State\n\nnew\n",
        )
        self.assertEqual(
            (self.workspace / "current/memory/index.md").read_text(
                encoding="utf-8"
            ),
            "# Memory\n",
        )

        recovered = recover_journal(self.workspace, self.runtime)

        self.assertEqual(
            recovered.changed_paths,
            ("current/state.md", "current/memory/index.md"),
        )
        self.assertEqual(
            (self.workspace / "current/memory/index.md").read_text(
                encoding="utf-8"
            ),
            "# Memory\n\nnew\n",
        )
        self.assertFalse((self.runtime / JOURNAL_FILENAME).exists())

    def test_recovery_conflict_stops_without_false_success(self) -> None:
        proposals = [
            self.existing_proposal(
                "current/state.md", "# State\n\nnew\n"
            ),
            self.existing_proposal(
                "current/memory/index.md", "# Memory\n\nnew\n"
            ),
        ]

        def crash(_target: Path) -> None:
            raise RuntimeError("crash")

        with self.assertRaises(RuntimeError):
            apply_writes(
                self.workspace,
                self.runtime,
                proposals,
                after_replace=crash,
            )
        conflicted = self.workspace / "current/memory/index.md"
        conflicted.write_text("# External edit\n", encoding="utf-8")

        with self.assertRaises(JournalConflictError):
            recover_journal(self.workspace, self.runtime)

        self.assertEqual(
            conflicted.read_text(encoding="utf-8"), "# External edit\n"
        )
        self.assertTrue((self.runtime / JOURNAL_FILENAME).exists())

    def test_workspace_lock_rejects_two_sessions_using_same_baseline(self) -> None:
        old = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        first_proposal = self.proposal(
            "current/state.md",
            "# State\n\nfrom session one\n",
            expected=sha256_text(old),
        )
        second_proposal = self.proposal(
            "current/state.md",
            "# State\n\nfrom session two\n",
            expected=sha256_text(old),
        )
        first_holds_workspace_lock = threading.Event()
        release_first = threading.Event()
        second_started = threading.Event()

        def hold_after_replace(_target: Path) -> None:
            first_holds_workspace_lock.set()
            if not release_first.wait(timeout=5):
                raise RuntimeError("test did not release first writer")

        def run_second_session() -> object:
            second_started.set()
            return apply_writes(
                self.workspace,
                self.runtime,
                [second_proposal],
                transaction_key="session-2:event-1:digest-2",
            )

        with ThreadPoolExecutor(max_workers=2) as executor:
            first = executor.submit(
                apply_writes,
                self.workspace,
                self.runtime,
                [first_proposal],
                transaction_key="session-1:event-1:digest-1",
                after_replace=hold_after_replace,
            )
            self.assertTrue(first_holds_workspace_lock.wait(timeout=5))
            second = executor.submit(run_second_session)
            self.assertTrue(second_started.wait(timeout=5))
            self.assertFalse(second.done())
            release_first.set()

            self.assertEqual(
                first.result(timeout=5).changed_paths,
                ("current/state.md",),
            )
            with self.assertRaises(StaleBaselineError):
                second.result(timeout=5)

        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            first_proposal.content,
        )

    def test_crash_replay_survives_a_later_session_update(self) -> None:
        old = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        first_proposal = self.proposal(
            "current/state.md",
            "# State\n\nfirst session committed\n",
            expected=sha256_text(old),
        )
        first_key = "session-1:event-1:digest-1"

        def crash_after_replace(_target: Path) -> None:
            raise RuntimeError("crash before completion marker")

        with self.assertRaisesRegex(RuntimeError, "completion marker"):
            apply_writes(
                self.workspace,
                self.runtime,
                [first_proposal],
                transaction_key=first_key,
                after_replace=crash_after_replace,
            )

        recovered = recover_journal(self.workspace, self.runtime)
        self.assertEqual(recovered.changed_paths, ("current/state.md",))

        second_proposal = self.existing_proposal(
            "current/state.md", "# State\n\nsecond session is newer\n"
        )
        second_key = "session-2:event-1:digest-2"
        apply_writes(
            self.workspace,
            self.runtime,
            [second_proposal],
            transaction_key=second_key,
        )

        replay = apply_writes(
            self.workspace,
            self.runtime,
            [first_proposal],
            transaction_key=first_key,
        )

        self.assertEqual(replay.changed_paths, ("current/state.md",))
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            second_proposal.content,
        )
        self.assertTrue(
            acknowledge_transaction(
                self.workspace,
                self.runtime,
                first_key,
                [first_proposal],
            )
        )
        self.assertFalse(
            acknowledge_transaction(
                self.workspace,
                self.runtime,
                first_key,
                [first_proposal],
            )
        )
        self.assertTrue(
            acknowledge_transaction(
                self.workspace,
                self.runtime,
                second_key,
                [second_proposal],
            )
        )

    def test_transaction_key_mismatch_cannot_replay_or_remove_marker(self) -> None:
        proposal = self.existing_proposal(
            "current/state.md", "# State\n\ncompleted once\n"
        )
        transaction_key = "session-1:event-1:digest-1"
        apply_writes(
            self.workspace,
            self.runtime,
            [proposal],
            transaction_key=transaction_key,
        )
        different = self.proposal(
            "current/state.md",
            "# State\n\ndifferent request\n",
            expected=proposal.expected_sha256,
        )

        with self.assertRaises(CompletedWriteConflictError):
            apply_writes(
                self.workspace,
                self.runtime,
                [different],
                transaction_key=transaction_key,
            )
        with self.assertRaises(CompletedWriteConflictError):
            acknowledge_transaction(
                self.workspace,
                self.runtime,
                transaction_key,
                [different],
            )
        self.assertTrue(
            acknowledge_transaction(
                self.workspace,
                self.runtime,
                transaction_key,
                [proposal],
            )
        )

    def test_acknowledges_exact_marker_while_another_transaction_needs_recovery(
        self,
    ) -> None:
        first = self.existing_proposal(
            "current/state.md", "# State\n\nfirst committed\n"
        )
        first_key = "session-1:event-1:digest-1"
        apply_writes(
            self.workspace,
            self.runtime,
            [first],
            transaction_key=first_key,
        )
        second = self.existing_proposal(
            "current/state.md", "# State\n\nsecond pending recovery\n"
        )

        def crash_after_replace(_target: Path) -> None:
            raise RuntimeError("leave the second journal pending")

        with self.assertRaisesRegex(RuntimeError, "second journal"):
            apply_writes(
                self.workspace,
                self.runtime,
                [second],
                transaction_key="session-2:event-1:digest-2",
                after_replace=crash_after_replace,
            )

        self.assertTrue((self.runtime / JOURNAL_FILENAME).exists())
        self.assertTrue(
            acknowledge_transaction(
                self.workspace,
                self.runtime,
                first_key,
                [first],
            )
        )
        self.assertTrue((self.runtime / JOURNAL_FILENAME).exists())

    def test_exact_replay_bypasses_another_conflicted_journal(self) -> None:
        first = self.existing_proposal(
            "current/state.md", "# State\n\nfirst committed\n"
        )
        first_key = "session-1:event-1:digest-1"
        apply_writes(
            self.workspace,
            self.runtime,
            [first],
            transaction_key=first_key,
        )
        second = self.existing_proposal(
            "current/state.md", "# State\n\nsecond pending recovery\n"
        )

        def crash_after_replace(_target: Path) -> None:
            raise RuntimeError("leave the second journal pending")

        with self.assertRaisesRegex(RuntimeError, "second journal"):
            apply_writes(
                self.workspace,
                self.runtime,
                [second],
                transaction_key="session-2:event-1:digest-2",
                after_replace=crash_after_replace,
            )
        target = self.workspace / "current/state.md"
        target.write_text("# State\n\nexternal conflict\n", encoding="utf-8")

        replay = apply_writes(
            self.workspace,
            self.runtime,
            [first],
            transaction_key=first_key,
        )

        self.assertEqual(replay.changed_paths, ("current/state.md",))
        self.assertEqual(
            target.read_text(encoding="utf-8"),
            "# State\n\nexternal conflict\n",
        )
        self.assertTrue((self.runtime / JOURNAL_FILENAME).exists())

    def test_rejects_broken_local_markdown_link(self) -> None:
        proposal = self.existing_proposal(
            "current/state.md", "# State\n\n[missing](missing.md)\n"
        )

        with self.assertRaises(BrokenMarkdownLinkError):
            apply_writes(self.workspace, self.runtime, [proposal])

        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            "# State\n\nold\n",
        )

    def test_ignores_link_syntax_inside_markdown_code(self) -> None:
        proposal = self.existing_proposal(
            "current/state.md",
            "# State\n\n`[inline](missing.md)`\n\n"
            "```md\n[example](also-missing.md)\n```\n",
        )

        result = apply_writes(self.workspace, self.runtime, [proposal])

        self.assertEqual(result.changed_paths, ("current/state.md",))

    def test_allows_existing_external_and_same_transaction_links(self) -> None:
        project_doc = self.workspace.parent.parent / "README.md"
        project_doc.write_text("# Project\n", encoding="utf-8")
        proposals = [
            self.existing_proposal(
                "output/index.md",
                "# Output\n\n[project](../../../README.md)\n",
            ),
            self.existing_proposal(
                "current/state.md",
                "# State\n\n[decision](../records/2026-08-17-decision.md)\n",
            ),
            self.proposal(
                "records/2026-08-17-decision.md", "# Decision\n"
            ),
        ]

        result = apply_writes(self.workspace, self.runtime, proposals)

        self.assertEqual(
            result.changed_paths,
            (
                "output/index.md",
                "current/state.md",
                "records/2026-08-17-decision.md",
            ),
        )

    def test_rejects_duplicate_normalized_paths(self) -> None:
        proposal = self.existing_proposal("current/state.md", "changed\n")
        with self.assertRaises(UnsafeWriteError):
            apply_writes(
                self.workspace,
                self.runtime,
                [proposal, proposal],
            )

    def test_journal_does_not_embed_markdown_content(self) -> None:
        marker = "PRIVATE RAW CONTENT"
        transaction_key = "PRIVATE EVENT KEY"

        def crash(_target: Path) -> None:
            raise RuntimeError("crash")

        with self.assertRaises(RuntimeError):
            apply_writes(
                self.workspace,
                self.runtime,
                [
                    self.existing_proposal(
                        "current/state.md", f"# State\n\n{marker}\n"
                    )
                ],
                transaction_key=transaction_key,
                after_replace=crash,
            )

        journal = json.loads(
            (self.runtime / JOURNAL_FILENAME).read_text(encoding="utf-8")
        )
        self.assertNotIn(marker, json.dumps(journal))
        self.assertNotIn(transaction_key, json.dumps(journal))


if __name__ == "__main__":
    unittest.main()
