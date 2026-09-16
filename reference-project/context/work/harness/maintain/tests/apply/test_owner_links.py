"""Maintain test_owner_links 시나리오."""

from __future__ import annotations

from context.work.harness.maintain import bootstrap_workspace
from context.work.harness.workspace_contract import HarnessError

from ..support.apply import MaintainApplyFixture


class TestOwnerLinks(MaintainApplyFixture):
    def test_new_memory_topic_requires_linked_memory_index_update(self) -> None:
        new_topic = {
            "path": "current/memory/04-new.md",
            "expected_sha256": None,
            "content": "# New memory\n\nDurable constraint.\n",
            "reason": "Preserve a new durable constraint.",
        }
        with self.assertRaisesRegex(
            HarnessError, "requires.*current/memory/index.md"
        ):
            self.apply(self.decision("update", changes=[new_topic]))

        memory_index = self.relative("current/memory/index.md")
        index_content = memory_index.read_text(encoding="utf-8")
        decision = self.decision(
            "update",
            changes=[
                new_topic,
                {
                    "path": "current/memory/index.md",
                    "expected_sha256": self.digest(memory_index),
                    "content": (
                        index_content
                        + "\n- [`04-new.md`](04-new.md): New durable constraint.\n"
                    ),
                    "reason": "Keep the memory entry map complete.",
                },
            ],
        )

        result = self.apply(decision)

        self.assertEqual(result["context_status"], "updated")
        self.assertEqual(
            self.relative("current/memory/04-new.md").read_text(
                encoding="utf-8"
            ),
            new_topic["content"],
        )
        self.assertIn("(04-new.md)", memory_index.read_text(encoding="utf-8"))

    def test_ticket_create_update_and_recover_keep_progress_in_body(self) -> None:
        before = self.workspace_bytes()
        ticket = {
            "path": "current/memory/tickets/002-policy.md",
            "expected_sha256": None,
            "content": "# Policy\n\nBuild the policy.\n\nStatus: ready\n",
            "reason": "An executable task was defined in the conversation.",
        }
        # memory 색인 연결만으로 누락된 Ticket 색인을 대신할 수 없다.
        parent_index = self.relative("current/memory/index.md")
        with self.assertRaisesRegex(HarnessError, "requires.*tickets/index.md"):
            self.apply(self.decision("update", changes=[ticket, {
                "path": "current/memory/index.md",
                "expected_sha256": self.digest(parent_index),
                "content": "# Memory\n\n[Ticket](tickets/002-policy.md)\n",
                "reason": "Wrong entry point for a new Ticket.",
            }]))
        self.assertEqual(self.workspace_bytes(), before)

        index = self.relative("current/memory/tickets/index.md")
        index_change = {
            "path": "current/memory/tickets/index.md",
            "expected_sha256": self.digest(index),
            "content": index.read_text() + "\n- [Policy](002-policy.md)\n",
            "reason": "Make the new Ticket discoverable.",
        }
        result = self.apply(self.decision("update", changes=[ticket, index_change]))
        self.assertEqual(result["context_status"], "updated")
        target = self.relative(ticket["path"])
        stale_hash = self.digest(target)
        ticket["expected_sha256"] = stale_hash
        ticket["content"] = "# Policy\n\nBuild the policy.\n\nStatus: blocked\n"
        result = self.apply(self.decision("update", changes=[ticket]))
        self.assertEqual(result["context_status"], "updated")
        self.assertIn("Status: blocked", target.read_text())
        self.assertEqual(index.read_text(), index_change["content"])
        self.assertEqual(
            self.relative("current/state/index.md").read_bytes(),
            before["current/state/index.md"],
        )
        self.assertEqual(parent_index.read_bytes(), before["current/memory/index.md"])
        with self.assertRaisesRegex(HarnessError, "stale expected_sha256"):
            self.apply(self.decision("update", changes=[ticket]))

        packet = bootstrap_workspace(self.project_root, self.work_root, "001-example")
        serialized = repr(packet)
        self.assertIn("002-policy.md", serialized)
        self.assertNotIn("Status: blocked", serialized)

    def test_new_spec_file_requires_memory_link_and_enters_recover(self) -> None:
        # 기존 작성 권한으로 누락된 Spec 구성요소를 복원할 수 있다.
        path = "current/memory/spec/03-concepts-and-contracts.md"
        self.relative(path).unlink()
        change = {
            "path": path, "expected_sha256": None,
            "content": "# Contracts\n\nRestored contract meaning.\n",
            "reason": "Document the agreed contract.",
        }
        with self.assertRaisesRegex(HarnessError, "requires.*memory/index.md"):
            self.apply(self.decision("update", changes=[change]))
        index = self.relative("current/memory/index.md")
        result = self.apply(self.decision("update", changes=[change, {
            "path": "current/memory/index.md",
            "expected_sha256": self.digest(index),
            "content": index.read_text() + (
                "\n- [Contracts](spec/03-concepts-and-contracts.md)\n"
            ),
            "reason": "Keep the Spec reachable.",
        }]))
        self.assertEqual(result["context_status"], "updated")
        packet = bootstrap_workspace(self.project_root, self.work_root, "001-example")
        self.assertIn("Restored contract meaning.", repr(packet))

    def test_spec_and_ticket_updates_reject_symlinked_parents(self) -> None:
        for directory, filename in (
            ("spec", "01-problem-goal-scope.md"),
            ("tickets", "001-example.md"),
        ):
            with self.subTest(directory=directory):
                parent = self.relative(f"current/memory/{directory}")
                moved = parent.with_name(directory + "-original")
                parent.rename(moved)
                parent.symlink_to(moved, target_is_directory=True)
                target = moved / filename
                before = target.read_bytes()
                try:
                    with self.assertRaisesRegex(HarnessError, "symlink"):
                        self.apply(self.decision("update", changes=[{
                            "path": f"current/memory/{directory}/{filename}",
                            "expected_sha256": self.digest(target),
                            "content": "# Rejected\n",
                            "reason": "Must not follow a symlink.",
                        }]))
                    self.assertEqual(target.read_bytes(), before)
                finally:
                    parent.unlink()
                    moved.rename(parent)
