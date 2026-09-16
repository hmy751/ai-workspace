"""Maintain test_transaction 시나리오."""

from __future__ import annotations

from context.work.harness.workspace_contract import HarnessError

from ..support.apply import MaintainApplyFixture


class TestTransaction(MaintainApplyFixture):
    def test_no_change_preserves_every_workspace_file_byte_for_byte(self) -> None:
        before = self.workspace_bytes()

        result = self.apply(self.decision("no_change"))

        self.assertEqual(result["context_status"], "no_change")
        self.assertEqual(result["changed"], [])
        self.assertEqual(self.workspace_bytes(), before)

    def test_allowed_existing_update_requires_and_matches_preimage(self) -> None:
        target = self.relative("current/memory/spec/01-problem-goal-scope.md")
        decision = self.decision(
            "update",
            changes=[
                {
                    "path": "current/memory/spec/01-problem-goal-scope.md",
                    "expected_sha256": self.digest(target),
                    "content": (
                        "# Updated goal\n\n"
                        "Continue with the [state](../../state/index.md).\n"
                    ),
                    "reason": "The durable goal changed.",
                }
            ],
        )

        result = self.apply(decision)

        self.assertEqual(result["context_status"], "updated")
        self.assertEqual(
            result["changed"],
            [
                {
                    "path": "current/memory/spec/01-problem-goal-scope.md",
                    "reason": "The durable goal changed.",
                }
            ],
        )
        self.assertEqual(
            target.read_text(encoding="utf-8"),
            decision["changes"][0]["content"],
        )

    def test_needs_user_decision_is_zero_write(self) -> None:
        before = self.workspace_bytes()
        decision = self.decision(
            "needs_user_decision",
            question="Which source should be authoritative?",
        )

        result = self.apply(decision)

        self.assertEqual(result["context_status"], "needs_user_decision")
        self.assertEqual(result["question"], decision["question"])
        self.assertEqual(result["changed"], [])
        self.assertEqual(self.workspace_bytes(), before)

    def test_rejects_stale_existing_preimage(self) -> None:
        target = self.relative("current/state/index.md")
        expected = self.digest(target)
        target.write_text("# concurrent change\n", encoding="utf-8")
        decision = self.decision(
            "update",
            changes=[
                {
                    "path": "current/state/index.md",
                    "expected_sha256": expected,
                    "content": "# proposed change\n",
                    "reason": "A stale proposal must not overwrite.",
                }
            ],
        )

        with self.assertRaisesRegex(HarnessError, "stale"):
            self.apply(decision)

        self.assertEqual(
            target.read_text(encoding="utf-8"), "# concurrent change\n"
        )

    def test_new_file_requires_null_and_existing_file_requires_digest(self) -> None:
        new_memory = self.decision(
            "update",
            changes=[
                {
                    "path": "current/memory/04-new.md",
                    "expected_sha256": "0" * 64,
                    "content": "# New memory\n",
                    "reason": "New durable constraint.",
                }
            ],
        )
        with self.assertRaisesRegex(HarnessError, "must be null"):
            self.apply(new_memory)

        existing = self.decision(
            "update",
            changes=[
                {
                    "path": "source/index.md",
                    "expected_sha256": None,
                    "content": "# Source index\n",
                    "reason": "Update provenance.",
                }
            ],
        )
        with self.assertRaisesRegex(HarnessError, "is required"):
            self.apply(existing)
