from __future__ import annotations

import copy
import json

from context.work.harness.tests.support import WorkspaceFixture


class RecoverTests(WorkspaceFixture):
    def test_loads_only_recover_owned_current_and_project_context(self) -> None:
        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        packet = json.loads(completed.stdout)
        self.assertEqual(packet["schema_version"], 4)
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
                    "path": "workspaces/001-example/current/memory/01-goal.md",
                },
                {
                    "path_base": "work_root",
                    "path": "workspaces/001-example/current/memory/02-decisions.md",
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
                    "path_base": "project_root",
                    "path": "context/project/selected.md",
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
                    "path": (
                        "workspaces/001-example/current/memory/01-goal.md"
                    ),
                    "path_base": "work_root",
                    "content": "WORKSPACE_MEMORY_GOAL\n",
                },
                {
                    "path": (
                        "workspaces/001-example/current/memory/02-decisions.md"
                    ),
                    "path_base": "work_root",
                    "content": "WORKSPACE_MEMORY_DECISIONS\n",
                },
            ],
        )
        self.assertEqual(
            packet["state"]["index"]["content"],
            "# state\n\nhuman-owned current description\n",
        )
        self.assertEqual(
            packet["state"]["status"]["value"], self.initial_status()
        )
        self.assertEqual(
            [entry["path"] for entry in packet["project_context"]],
            ["context/project/selected.md"],
        )
        self.assertEqual(
            {entry["path_base"] for entry in packet["project_context"]},
            {"project_root"},
        )
        self.assertNotIn("verification", packet)
        self.assertNotIn("verify.json", completed.stdout)
        self.assertIn("SELECTED_PROJECT_CONTEXT", completed.stdout)
        self.assertNotIn("UNSELECTED_PROJECT_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_RECORD_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_RECORD_MARKDOWN_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_MEMORY_NON_MARKDOWN_SECRET", completed.stdout)
        self.assertNotIn("UNLOADED_NESTED_MEMORY_SECRET", completed.stdout)

    def test_succeeds_when_verify_contract_is_invalid(self) -> None:
        (
            self.work_root / "workspaces" / "001-example" / "verify.json"
        ).write_text(
            '{"verification": "INVALID_VERIFY_CONTRACT_SECRET"\n',
            encoding="utf-8",
        )

        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("INVALID_VERIFY_CONTRACT_SECRET", completed.stdout)

    def test_module_help_exposes_recover_and_verify(self) -> None:
        completed = self.run_cli("--help")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("{recover,verify}", completed.stdout)
        self.assertIn("recover", completed.stdout)
        self.assertIn("verify", completed.stdout)

    def test_keeps_workspace_and_project_context_path_bases_separate(self) -> None:
        decoy_workspaces = self.project_root / "workspaces"
        decoy_workspaces.mkdir()
        (decoy_workspaces / "index.json").write_text(
            '{"invalid": "PROJECT_ROOT_WORKSPACE_DECOY"}\n',
            encoding="utf-8",
        )
        decoy_project_context = self.work_root / "context" / "project"
        decoy_project_context.mkdir(parents=True)
        (decoy_project_context / "selected.md").write_text(
            "WORK_ROOT_PROJECT_CONTEXT_DECOY\n", encoding="utf-8"
        )

        completed = self.run_cli("recover", "--json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("SELECTED_PROJECT_CONTEXT", completed.stdout)
        self.assertNotIn("PROJECT_ROOT_WORKSPACE_DECOY", completed.stdout)
        self.assertNotIn("WORK_ROOT_PROJECT_CONTEXT_DECOY", completed.stdout)

    def test_plain_output_renders_state_without_verify_configuration(self) -> None:
        completed = self.run_cli("recover")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("## state/status.json", completed.stdout)
        self.assertIn("- status: ready_for_verification", completed.stdout)
        self.assertIn("- result: null", completed.stdout)
        self.assertIn("- finished_at: null", completed.stdout)
        self.assertIn("- receipt: null", completed.stdout)
        self.assertIn("- next_action: 고정 검증을 실행한다.", completed.stdout)
        self.assertNotIn('"status": "ready_for_verification"', completed.stdout)
        self.assertNotIn("Fixed verification argv", completed.stdout)

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
        self.write_work_json(
            "workspaces/001-example/recover.json", outside_context
        )

        lexical_outside = self.run_cli("recover")
        self.assertEqual(lexical_outside.returncode, 2)
        self.assertIn("selected from context/project", lexical_outside.stderr)

        record_path = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "records"
            / "old.json"
        )
        link_path = (
            self.project_root / "context" / "project" / "record-link.md"
        )
        link_path.symlink_to(record_path)
        linked_record = copy.deepcopy(self.recover_contract)
        linked_record["project_context"][0]["path"] = (
            "context/project/record-link.md"
        )
        self.write_work_json(
            "workspaces/001-example/recover.json", linked_record
        )

        linked = self.run_cli("recover")
        self.assertEqual(linked.returncode, 2)
        self.assertIn("symlink", linked.stderr)
        self.assertNotIn("UNLOADED_RECORD_SECRET", linked.stdout)

    def test_rejects_workspace_identity_extra_responsibility(self) -> None:
        identity = copy.deepcopy(self.identity)
        identity["project_context"] = []
        self.write_work_json(
            "workspaces/001-example/workspace.json", identity
        )

        completed = self.run_cli("recover")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("Workspace identity keys", completed.stderr)
        self.assertIn("extra", completed.stderr)

    def test_rejects_invalid_state_status(self) -> None:
        legacy_schema = self.initial_status()
        legacy_schema["schema_version"] = 1
        self.write_status(legacy_schema)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("schema_version", completed.stderr)

        inconsistent = self.initial_status()
        inconsistent["status"] = "verified_waiting_acceptance"
        self.write_status(inconsistent)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("inconsistent", completed.stderr)

        wrong_type = self.initial_status()
        wrong_type["status"] = ["ready_for_verification"]
        self.write_status(wrong_type)

        completed = self.run_cli("recover")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("invalid Workspace state status", completed.stderr)

    def test_rejects_missing_malformed_and_symlinked_status(self) -> None:
        status_path = (
            self.work_root
            / "workspaces"
            / "001-example"
            / "current"
            / "state"
            / "status.json"
        )
        status_path.unlink()

        missing = self.run_cli("recover")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("does not exist", missing.stderr)

        status_path.write_text("{not-json\n", encoding="utf-8")
        malformed = self.run_cli("recover")
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("not valid JSON", malformed.stderr)

        status_path.unlink()
        outside_status = (
            self.project_root / "context" / "project" / "status.json"
        )
        outside_status.write_text(
            json.dumps(self.initial_status()), encoding="utf-8"
        )
        status_path.symlink_to(outside_status)
        linked = self.run_cli("recover")
        self.assertEqual(linked.returncode, 2)
        self.assertIn("symlink", linked.stderr)

    def test_rejects_symlinked_memory_topic_and_current_directories(self) -> None:
        source = (
            self.project_root / "context" / "project" / "linked-memory.md"
        )
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

    def test_validates_linked_receipt_header_without_exposing_body(self) -> None:
        receipt_relative = "workspaces/001-example/records/verify-existing.json"
        status = self.verified_status(receipt_relative)
        self.write_status(status)

        missing = self.run_cli("recover", "--json")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("does not exist", missing.stderr)

        receipt = {
            "schema_version": 1,
            "workspace_id": "001-example",
            "result": "fail",
            "finished_at": status["finished_at"],
            "body_secret": "RECEIPT_BODY_MUST_NOT_ENTER_CONTEXT",
        }
        self.write_work_json(receipt_relative, receipt)
        mismatched = self.run_cli("recover", "--json")
        self.assertEqual(mismatched.returncode, 2)
        self.assertIn("result do not match", mismatched.stderr)

        receipt["result"] = "pass"
        receipt["finished_at"] = "2026-08-13T00:00:01.000Z"
        self.write_work_json(receipt_relative, receipt)
        wrong_time = self.run_cli("recover", "--json")
        self.assertEqual(wrong_time.returncode, 2)
        self.assertIn("finished_at do not match", wrong_time.stderr)

        receipt["finished_at"] = status["finished_at"]
        self.write_work_json(receipt_relative, receipt)
        recovered = self.run_cli("recover", "--json")
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        packet = json.loads(recovered.stdout)
        receipt_entry = {"path_base": "work_root", "path": receipt_relative}
        self.assertIn(receipt_entry, packet["control_paths"])
        self.assertNotIn(receipt_entry, packet["loaded_context_paths"])
        self.assertNotIn("RECEIPT_BODY_MUST_NOT_ENTER_CONTEXT", recovered.stdout)

    def test_rejects_receipt_symlink(self) -> None:
        outside_receipt = (
            self.project_root / "context" / "project" / "receipt.json"
        )
        outside_receipt.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_id": "001-example",
                    "result": "pass",
                    "finished_at": "2026-08-13T00:00:00.000Z",
                }
            ),
            encoding="utf-8",
        )
        receipt_relative = "workspaces/001-example/records/linked.json"
        (self.work_root / receipt_relative).symlink_to(outside_receipt)
        self.write_status(self.verified_status(receipt_relative))

        completed = self.run_cli("recover")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("symlink", completed.stderr)


if __name__ == "__main__":
    import unittest

    unittest.main()
