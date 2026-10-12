"""Recover: 전용 설정과 입력 경로 계약을 검증한다."""

from __future__ import annotations

import copy
import json

from context.work.harness.testing import WorkspaceFixture


class RecoverContractTests(WorkspaceFixture):
    def test_rejects_recover_contract_traversal_absolute_schema_and_id(self) -> None:
        invalid_contracts: list[tuple[dict[str, object], str]] = []

        traversal = copy.deepcopy(self.recover_contract)
        traversal["project_context"][0]["path"] = "../outside.md"
        invalid_contracts.append((traversal, "traverse"))

        absolute = copy.deepcopy(self.recover_contract)
        absolute["project_context"][0]["path"] = "/tmp/outside.md"
        invalid_contracts.append((absolute, "relative"))

        legacy_schema = copy.deepcopy(self.recover_contract)
        legacy_schema["schema_version"] = 1
        invalid_contracts.append((legacy_schema, "schema_version"))

        previous_reference_schema = copy.deepcopy(self.recover_contract)
        previous_reference_schema["schema_version"] = 2
        invalid_contracts.append((previous_reference_schema, "schema_version"))

        previous_target_schema = copy.deepcopy(self.recover_contract)
        previous_target_schema["schema_version"] = 3
        invalid_contracts.append((previous_target_schema, "schema_version"))

        previous_overview_anchor_schema = copy.deepcopy(self.recover_contract)
        previous_overview_anchor_schema["schema_version"] = 4
        invalid_contracts.append((previous_overview_anchor_schema, "schema_version"))

        previous_flat_path_schema = copy.deepcopy(self.recover_contract)
        previous_flat_path_schema["schema_version"] = 5
        invalid_contracts.append((previous_flat_path_schema, "schema_version"))

        wrong_id = copy.deepcopy(self.recover_contract)
        wrong_id["workspace_id"] = "002-other"
        invalid_contracts.append((wrong_id, "does not match"))

        for invalid_contract, expected_error in invalid_contracts:
            with self.subTest(expected_error=expected_error):
                self.write_work_json(
                    "workspaces/001-example/recover.json", invalid_contract
                )
                completed = self.run_cli("recover")
                self.assertEqual(completed.returncode, 2)
                self.assertIn(expected_error, completed.stderr)

    def test_rejects_project_context_outside_boundary_and_symlinks(self) -> None:
        outside_context = copy.deepcopy(self.recover_contract)
        outside_context["project_context"][0]["path"] = "src/value.txt"
        self.write_work_json("workspaces/001-example/recover.json", outside_context)

        lexical_outside = self.run_cli("recover")
        self.assertEqual(lexical_outside.returncode, 2)
        self.assertIn("selected from context/project", lexical_outside.stderr)

        record_path = (
            self.work_root / "workspaces" / "001-example" / "records" / "old.json"
        )
        link_path = (
            self.project_root / "context" / "project" / "common" / "record-link.md"
        )
        link_path.symlink_to(record_path)
        linked_record = copy.deepcopy(self.recover_contract)
        linked_record["project_context"][0][
            "path"
        ] = "context/project/common/record-link.md"
        self.write_work_json("workspaces/001-example/recover.json", linked_record)

        linked = self.run_cli("recover")
        self.assertEqual(linked.returncode, 2)
        self.assertIn("symlink", linked.stderr)
        self.assertNotIn("UNLOADED_RECORD_SECRET", linked.stdout)

    def test_requires_each_selected_project_context_file_to_exist(self) -> None:
        task_context = (
            self.project_root / "context" / "project" / "common" / "task-context.md"
        )
        content = task_context.read_text(encoding="utf-8")
        task_context.unlink()
        try:
            missing = self.run_cli("recover")
        finally:
            task_context.write_text(content, encoding="utf-8")

        self.assertEqual(missing.returncode, 2)
        self.assertIn("does not exist", missing.stderr)

    def test_does_not_auto_load_unselected_project_layers(self) -> None:
        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("PROJECT_ROUTING_CONTEXT", completed.stdout)
        self.assertIn("PROJECT_COMMON_CONTEXT", completed.stdout)
        self.assertIn("PROJECT_CURRENT_CONTEXT", completed.stdout)
        self.assertNotIn("UNSELECTED_PROJECT_GUIDANCE", completed.stdout)
        self.assertNotIn("UNSELECTED_PROJECT_DECISIONS_ROUTING", completed.stdout)

    def test_preserves_selected_project_context_order(self) -> None:
        readme_second = copy.deepcopy(self.recover_contract)
        readme_second["project_context"] = [
            readme_second["project_context"][2],
            readme_second["project_context"][0],
            readme_second["project_context"][1],
        ]
        self.write_work_json("workspaces/001-example/recover.json", readme_second)

        misplaced = self.run_cli("recover", "--json")

        self.assertEqual(misplaced.returncode, 0, misplaced.stderr)
        packet = json.loads(misplaced.stdout)
        self.assertEqual(
            [entry["path"] for entry in packet["project_context"]],
            [
                "context/project/current/task-state.md",
                "context/project/README.md",
                "context/project/common/task-context.md",
            ],
        )

    def test_requires_project_readme_selection_but_not_first(self) -> None:
        without_readme = copy.deepcopy(self.recover_contract)
        without_readme["project_context"] = without_readme["project_context"][1:]
        self.write_work_json("workspaces/001-example/recover.json", without_readme)

        rejected = self.run_cli("recover", "--json")

        self.assertEqual(rejected.returncode, 2)
        self.assertIn("must select context/project/README.md", rejected.stderr)
        self.assertNotIn("PROJECT_COMMON_CONTEXT", rejected.stdout)

    def test_accepts_nested_markdown_from_each_project_layer(self) -> None:
        project_context_root = self.project_root / "context" / "project"
        entries = [self.recover_contract["project_context"][0]]
        for layer in ("common", "current", "guidance", "decisions"):
            nested = project_context_root / layer / "nested"
            nested.mkdir()
            path = f"context/project/{layer}/nested/context.md"
            (nested / "context.md").write_text(
                f"SELECTED_{layer.upper()}_NESTED_CONTEXT\n",
                encoding="utf-8",
            )
            entries.append({"path": path, "reason": f"{layer} layer 선택 검증"})
        contract = copy.deepcopy(self.recover_contract)
        contract["project_context"] = entries
        self.write_work_json("workspaces/001-example/recover.json", contract)

        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        packet = json.loads(completed.stdout)
        self.assertEqual(
            [entry["path"] for entry in packet["project_context"]],
            [entry["path"] for entry in entries],
        )

    def test_rejects_root_flat_and_unknown_project_context_layers(self) -> None:
        project_context_root = self.project_root / "context" / "project"
        (project_context_root / "legacy-flat.md").write_text(
            "ROOT_FLAT_PROJECT_CONTEXT_MUST_NOT_LOAD\n", encoding="utf-8"
        )
        (project_context_root / "unknown").mkdir()
        (project_context_root / "unknown" / "context.md").write_text(
            "UNKNOWN_LAYER_PROJECT_CONTEXT_MUST_NOT_LOAD\n", encoding="utf-8"
        )

        invalid_paths = (
            "context/project/legacy-flat.md",
            "context/project/unknown/context.md",
        )
        for invalid_path in invalid_paths:
            with self.subTest(path=invalid_path):
                contract = copy.deepcopy(self.recover_contract)
                contract["project_context"][1]["path"] = invalid_path
                self.write_work_json("workspaces/001-example/recover.json", contract)

                completed = self.run_cli("recover", "--json")

                self.assertEqual(completed.returncode, 2)
                self.assertIn("common/, current/, guidance/", completed.stderr)
                self.assertNotIn("MUST_NOT_LOAD", completed.stdout)

    def test_rejects_non_markdown_project_context(self) -> None:
        non_markdown = (
            self.project_root / "context" / "project" / "common" / "selected.txt"
        )
        non_markdown.write_text(
            "NON_MARKDOWN_PROJECT_CONTEXT_MUST_NOT_LOAD\n",
            encoding="utf-8",
        )
        contract = copy.deepcopy(self.recover_contract)
        contract["project_context"][0]["path"] = "context/project/common/selected.txt"
        self.write_work_json("workspaces/001-example/recover.json", contract)

        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("must be a .md file", completed.stderr)
        self.assertNotIn(
            "NON_MARKDOWN_PROJECT_CONTEXT_MUST_NOT_LOAD",
            completed.stdout,
        )
