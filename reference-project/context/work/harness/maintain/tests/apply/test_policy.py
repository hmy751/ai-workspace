"""Maintain test_policy 시나리오."""

from __future__ import annotations

import copy

from context.work.harness.workspace_contract import HarnessError

from ..support.apply import MaintainApplyFixture


class TestPolicy(MaintainApplyFixture):
    def test_rejects_restricted_machine_product_and_nested_paths(self) -> None:
        cases = (
            "current/state/status.json",
            "workspace.json",
            "recover.json",
            "verify.json",
            "records/receipts/verify/new.md",
            "source/raw-input.md",
            "output/analysis.md",
            "current/memory/nested/note.md",
            "current/memory/spec/nested/note.md",
            "current/memory/tickets/nested/note.md",
            "current/memory/tickets/status.json",
            "../../src/value.txt",
        )
        for relative_path in cases:
            with self.subTest(relative_path=relative_path):
                decision = self.decision(
                    "update",
                    changes=[
                        {
                            "path": relative_path,
                            "expected_sha256": None,
                            "content": "# forbidden\n",
                            "reason": "Must be rejected.",
                        }
                    ],
                )
                with self.assertRaises(HarnessError):
                    self.apply(decision)

    def test_rejects_symlinked_target_without_touching_target(self) -> None:
        target = self.relative("current/state/index.md")
        outside = self.project_root / "outside.md"
        outside.write_text("OUTSIDE\n", encoding="utf-8")
        target.unlink()
        target.symlink_to(outside)
        decision = self.decision(
            "update",
            changes=[
                {
                    "path": "current/state/index.md",
                    "expected_sha256": self.digest(outside),
                    "content": "# changed\n",
                    "reason": "Must not follow a symlink.",
                }
            ],
        )

        with self.assertRaisesRegex(HarnessError, "symlink"):
            self.apply(decision)

        self.assertEqual(outside.read_text(encoding="utf-8"), "OUTSIDE\n")

    def test_creates_only_new_direct_dated_record_with_null_preimage(self) -> None:
        relative_path = "records/2026-08-19-01-first-maintain-result.md"
        records_index = self.relative("records/README.md")
        records_index.write_text(
            "# Records\n\n## 사람이 읽는 기록\n",
            encoding="utf-8",
        )
        new_record = {
            "path": relative_path,
            "expected_sha256": None,
            "content": "# First Maintain result\n\nDurable analysis.\n",
            "reason": "Preserve reusable analysis.",
        }
        with self.assertRaisesRegex(HarnessError, "requires.*records/README.md"):
            self.apply(self.decision("update", changes=[new_record]))

        decision = self.decision(
            "update",
            importance="important",
            changes=[
                new_record,
                {
                    "path": "records/README.md",
                    "expected_sha256": self.digest(records_index),
                    "content": (
                        "# Records\n\n"
                        "## 사람이 읽는 기록\n\n"
                        "- [`2026-08-19-01-first-maintain-result.md`]"
                        "(2026-08-19-01-first-maintain-result.md)\n"
                    ),
                    "reason": "Keep the records entry point complete.",
                },
            ],
        )

        result = self.apply(decision)

        self.assertEqual(result["context_status"], "updated")
        self.assertEqual(
            self.relative(relative_path).read_text(encoding="utf-8"),
            decision["changes"][0]["content"],
        )
        self.assertIn(
            "(2026-08-19-01-first-maintain-result.md)",
            records_index.read_text(encoding="utf-8"),
        )

        existing = copy.deepcopy(decision)
        existing["changes"][0]["expected_sha256"] = self.digest(
            self.relative(relative_path)
        )
        with self.assertRaisesRegex(HarnessError, "append-only"):
            self.apply(existing)

    def test_rejects_invalid_record_name_and_markdown_quality(self) -> None:
        invalid_records = (
            "records/2026-02-30-01-impossible.md",
            "records/2026-08-19-00-zero.md",
            "records/2026-08-19-01.md",
            "records/note.md",
        )
        for path in invalid_records:
            with self.subTest(path=path):
                with self.assertRaises(HarnessError):
                    self.apply(
                        self.decision(
                            "update",
                            changes=[
                                {
                                    "path": path,
                                    "expected_sha256": None,
                                    "content": "# record\n",
                                    "reason": "Invalid name.",
                                }
                            ],
                        )
                    )

        target = self.relative("output/index.md")
        for content in (
            "# Missing EOF newline",
            "# Trailing whitespace \n",
            "# Broken link\n\n[missing](missing.md)\n",
        ):
            with self.subTest(content=content):
                with self.assertRaises(HarnessError):
                    self.apply(
                        self.decision(
                            "update",
                            changes=[
                                {
                                    "path": "output/index.md",
                                    "expected_sha256": self.digest(target),
                                    "content": content,
                                    "reason": "Invalid Markdown.",
                                }
                            ],
                        )
                    )
