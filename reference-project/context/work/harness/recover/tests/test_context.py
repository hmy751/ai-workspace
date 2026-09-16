"""Recover: Workspace의 제한된 읽기와 symlink 방어를 검증한다."""

from __future__ import annotations

import json

from context.work.harness.testing import WorkspaceFixture


class RecoverContextTests(WorkspaceFixture):
    def test_requires_workspace_output_index(self) -> None:
        output_index = (
            self.work_root / "workspaces" / "001-example" / "output" / "index.md"
        )
        content = output_index.read_text(encoding="utf-8")
        output_index.unlink()
        try:
            completed = self.run_cli("recover")
        finally:
            output_index.write_text(content, encoding="utf-8")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("Workspace output index does not exist", completed.stderr)

    def test_does_not_require_or_inspect_workspace_output_artifacts(self) -> None:
        artifact = (
            self.work_root / "workspaces" / "001-example" / "output" / "analysis.md"
        )
        content = artifact.read_text(encoding="utf-8")
        artifact.unlink()
        try:
            completed = self.run_cli("recover", "--json")
        finally:
            artifact.write_text(content, encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("[analysis](analysis.md)", completed.stdout)
        self.assertNotIn("UNLOADED_OUTPUT_ARTIFACT_SECRET", completed.stdout)

    def test_rejects_symlinked_workspace_output_index(self) -> None:
        output_index = (
            self.work_root / "workspaces" / "001-example" / "output" / "index.md"
        )
        content = output_index.read_text(encoding="utf-8")
        outside = self.project_root / "output-index.md"
        outside.write_text("LINKED_OUTPUT_INDEX_MUST_NOT_LOAD\n", encoding="utf-8")
        output_index.unlink()
        output_index.symlink_to(outside)
        try:
            completed = self.run_cli("recover")
        finally:
            output_index.unlink()
            output_index.write_text(content, encoding="utf-8")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)
        self.assertNotIn("LINKED_OUTPUT_INDEX_MUST_NOT_LOAD", completed.stdout)

    def test_rejects_non_regular_workspace_output_index(self) -> None:
        output_index = (
            self.work_root / "workspaces" / "001-example" / "output" / "index.md"
        )
        content = output_index.read_text(encoding="utf-8")
        output_index.unlink()
        output_index.mkdir()
        try:
            completed = self.run_cli("recover")
        finally:
            output_index.rmdir()
            output_index.write_text(content, encoding="utf-8")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("must be a regular file", completed.stderr)

    def test_requires_minimum_memory_files(self) -> None:
        memory = self.work_root / "workspaces" / "001-example" / "current" / "memory"

        for required_name in (
            "spec/01-problem-goal-scope.md",
            "spec/02-behavior-and-cases.md",
            "spec/03-concepts-and-contracts.md",
            "spec/04-quality-and-completion.md",
            "spec/05-constraints-design-assumptions.md",
            "project-context.md",
            "tickets/index.md",
        ):
            with self.subTest(required_name=required_name):
                required_path = memory / required_name
                content = required_path.read_text(encoding="utf-8")
                required_path.unlink()
                try:
                    completed = self.run_cli("recover")
                    self.assertEqual(completed.returncode, 2)
                    self.assertIn("missing required files", completed.stderr)
                    self.assertIn(required_name, completed.stderr)
                finally:
                    required_path.write_text(content, encoding="utf-8")

    def test_spec_and_ticket_entry_points_reject_symlinks(self) -> None:
        memory = self.work_root / "workspaces/001-example/current/memory"
        for relative in (
            "spec",
            "tickets",
            "spec/03-concepts-and-contracts.md",
            "tickets/index.md",
        ):
            with self.subTest(relative=relative):
                target = memory / relative
                moved = target.with_name(target.name + "-original")
                target.rename(moved)
                target.symlink_to(moved, target_is_directory=moved.is_dir())
                try:
                    completed = self.run_cli("recover", "--json")
                    self.assertEqual(completed.returncode, 2)
                    self.assertIn("symlink", completed.stderr)
                finally:
                    target.unlink()
                    moved.rename(target)

    def test_ticket_body_is_selected_later_and_not_required_by_packet(self) -> None:
        body = self.work_root / (
            "workspaces/001-example/current/memory/tickets/001-example.md"
        )
        body.unlink()
        completed = self.run_cli("recover", "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        packet = json.loads(completed.stdout)
        self.assertIn("001-example.md", packet["memory"]["entries"][-1]["content"])
        self.assertNotIn(
            body.relative_to(self.work_root).as_posix(),
            [entry["path"] for entry in packet["loaded_context_paths"]],
        )

    def test_does_not_require_or_inspect_workspace_source(self) -> None:
        source = self.work_root / "workspaces" / "001-example" / "source"
        unavailable_source = source.with_name("source-unavailable")
        source.rename(unavailable_source)
        try:
            completed = self.run_cli("recover", "--json")
        finally:
            unavailable_source.rename(source)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("UNLOADED_SOURCE_INVENTORY_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_SOURCE_RAW_SECRET", completed.stdout)

    def test_rejects_symlinked_memory_topic_and_current_directories(self) -> None:
        source = self.project_root / "context" / "project" / "linked-memory.md"
        source.write_text("LINKED_MEMORY_MUST_NOT_LOAD\n", encoding="utf-8")
        link = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "current"
            / "memory"
            / "03-linked.md"
        )
        link.symlink_to(source)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)
        self.assertNotIn("LINKED_MEMORY_MUST_NOT_LOAD", completed.stdout)
        link.unlink()

        current = self.work_root / "workspaces" / "001-example" / "current"
        for directory_name in ("memory", "state"):
            with self.subTest(directory=directory_name):
                directory = current / directory_name
                real_directory = current / f"{directory_name}-real"
                directory.rename(real_directory)
                directory.symlink_to(real_directory, target_is_directory=True)
                try:
                    completed = self.run_cli("recover")
                    self.assertEqual(completed.returncode, 2)
                    self.assertIn("symlink", completed.stderr)
                finally:
                    directory.unlink()
                    real_directory.rename(directory)
