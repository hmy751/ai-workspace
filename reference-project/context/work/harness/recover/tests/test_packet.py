"""Recover: packet 형식·읽기 범위·root 분리를 검증한다."""

from __future__ import annotations

import json

from context.work.harness.testing import WorkspaceFixture


class RecoverPacketTests(WorkspaceFixture):
    def test_loads_current_output_map_and_project_context_only(self) -> None:
        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        packet = json.loads(completed.stdout)
        self.assertEqual(packet["schema_version"], 6)
        self.assertEqual(packet["workspace_id"], "001-example")
        self.assertEqual(
            packet["workspace"],
            {"path_base": "work_root", "path": "workspaces/001-example"},
        )
        self.assertEqual(
            packet["recover_contract"],
            {
                "path_base": "work_root",
                "path": "workspaces/001-example/recover.json",
            },
        )
        self.assertEqual(
            packet["control_paths"],
            [
                {"path_base": "work_root", "path": "workspaces/index.json"},
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/workspace.json",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/recover.json",
                },
            ],
        )
        self.assertEqual(
            packet["loaded_context_paths"],
            [
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/index.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/spec/01-problem-goal-scope.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/spec/02-behavior-and-cases.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/spec/03-concepts-and-contracts.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/spec/04-quality-and-completion.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/spec/05-constraints-design-assumptions.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/project-context.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/tickets/index.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/state/index.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/state/status.json",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/output/index.md",
                },
                {
                    "path_base": "project_root",
                    "path": "context/project/README.md",
                },
                {
                    "path_base": "project_root",
                    "path": "context/project/common/task-context.md",
                },
                {
                    "path_base": "project_root",
                    "path": "context/project/current/task-state.md",
                },
            ],
        )
        self.assertEqual(
            packet["memory"]["index"],
            {
                "path": "workspaces/001-example/current/memory/index.md",
                "path_base": "work_root",
                "content": "WORKSPACE_MEMORY_INDEX\n",
            },
        )
        self.assertEqual(
            packet["memory"]["entries"],
            [
                {
                    "path": "workspaces/001-example/current/memory/spec/01-problem-goal-scope.md",
                    "path_base": "work_root",
                    "content": "WORKSPACE_SPEC_GOAL\n",
                },
                {
                    "path": "workspaces/001-example/current/memory/spec/02-behavior-and-cases.md",
                    "path_base": "work_root",
                    "content": "WORKSPACE_SPEC_BEHAVIOR\n",
                },
                {
                    "path": "workspaces/001-example/current/memory/spec/03-concepts-and-contracts.md",
                    "path_base": "work_root",
                    "content": "WORKSPACE_SPEC_CONTRACTS\n",
                },
                {
                    "path": "workspaces/001-example/current/memory/spec/04-quality-and-completion.md",
                    "path_base": "work_root",
                    "content": "WORKSPACE_SPEC_QUALITY\n",
                },
                {
                    "path": "workspaces/001-example/current/memory/spec/05-constraints-design-assumptions.md",
                    "path_base": "work_root",
                    "content": "WORKSPACE_SPEC_DESIGN\n",
                },
                {
                    "path": "workspaces/001-example/current/memory/project-context.md",
                    "path_base": "work_root",
                    "content": "WORKSPACE_MEMORY_PROJECT_CONTEXT\n",
                },
                {
                    "path": "workspaces/001-example/current/memory/tickets/index.md",
                    "path_base": "work_root",
                    "content": "WORKSPACE_TICKET_INDEX\n\n- [Example](001-example.md)\n",
                },
            ],
        )
        self.assertEqual(
            packet["state"]["index"]["content"],
            "# state\n\nhuman-owned current description\n",
        )
        self.assertEqual(packet["state"]["status"]["value"], self.initial_status())
        self.assertEqual(
            packet["output"]["index"],
            {
                "path": "workspaces/001-example/output/index.md",
                "path_base": "work_root",
                "content": ("WORKSPACE_OUTPUT_INDEX\n\n" "- [analysis](analysis.md)\n"),
            },
        )
        self.assertEqual(
            [entry["path"] for entry in packet["project_context"]],
            [
                "context/project/README.md",
                "context/project/common/task-context.md",
                "context/project/current/task-state.md",
            ],
        )
        self.assertEqual(
            {entry["path_base"] for entry in packet["project_context"]},
            {"project_root"},
        )
        self.assertNotIn("verification", packet)
        self.assertNotIn("verify.json", completed.stdout)
        self.assertIn("PROJECT_ROUTING_CONTEXT", completed.stdout)
        self.assertIn("PROJECT_COMMON_CONTEXT", completed.stdout)
        self.assertIn("PROJECT_CURRENT_CONTEXT", completed.stdout)
        self.assertNotIn("PROJECT_COMMON_ROUTING", completed.stdout)
        self.assertNotIn("PROJECT_CURRENT_ROUTING", completed.stdout)
        self.assertNotIn("UNSELECTED_PROJECT_GUIDANCE", completed.stdout)
        self.assertNotIn("UNSELECTED_PROJECT_DECISIONS_ROUTING", completed.stdout)
        self.assertNotIn("UNLOADED_RECORD_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_RECORD_MARKDOWN_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_SOURCE_INVENTORY_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_SOURCE_RAW_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_OUTPUT_ARTIFACT_SECRET", completed.stdout)
        self.assertFalse(
            any(
                entry["path"].startswith("workspaces/001-example/source/")
                for entry in (packet["control_paths"] + packet["loaded_context_paths"])
            )
        )
        self.assertNotIn("UNLOADED_MEMORY_NON_MARKDOWN_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_NESTED_MEMORY_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_TICKET_BODY", completed.stdout)

    def test_keeps_workspace_and_project_context_path_bases_separate(self) -> None:
        decoy_workspaces = self.project_root / "workspaces"
        decoy_workspaces.mkdir()
        (decoy_workspaces / "index.json").write_text(
            '{"invalid": "PROJECT_ROOT_WORKSPACE_DECOY"}\n',
            encoding="utf-8",
        )
        decoy_project_context = self.work_root / "context" / "project"
        decoy_project_context.mkdir(parents=True)
        (decoy_project_context / "README.md").write_text(
            "WORK_ROOT_PROJECT_CONTEXT_DECOY\n", encoding="utf-8"
        )

        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("PROJECT_ROUTING_CONTEXT", completed.stdout)
        self.assertIn("PROJECT_COMMON_CONTEXT", completed.stdout)
        self.assertIn("PROJECT_CURRENT_CONTEXT", completed.stdout)
        self.assertNotIn("PROJECT_ROOT_WORKSPACE_DECOY", completed.stdout)
        self.assertNotIn("WORK_ROOT_PROJECT_CONTEXT_DECOY", completed.stdout)

    def test_succeeds_when_verify_contract_is_invalid(self) -> None:
        (self.work_root / "workspaces" / "001-example" / "verify.json").write_text(
            '{"verification": "INVALID_VERIFY_CONTRACT_SECRET"\n',
            encoding="utf-8",
        )

        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("INVALID_VERIFY_CONTRACT_SECRET", completed.stdout)
