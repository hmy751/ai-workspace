from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from context.work.harness.maintain.config import (
    MaintainConfigError,
    load_config,
)


class FormingWorkspaceConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name) / "project"
        self.codex = self.project / ".codex"
        self.work_root = self.project / "context/work"
        self.contract = self.work_root / "harness/maintain/README.md"
        self.workspace = self.work_root / "workspaces/002-forming"
        self.codex.mkdir(parents=True)
        self.contract.parent.mkdir(parents=True)
        self.contract.write_text("# Maintain\n", encoding="utf-8")
        (self.work_root / "workspaces").mkdir()
        self.config_path = self.codex / "context-maintain.json"
        self.config_path.write_text(
            json.dumps(
                {
                    "schema": "context-maintain.config.v1",
                    "workspace_id": "002-forming",
                    "work_root": "context/work",
                    "maintain_contract_path": (
                        "context/work/harness/maintain/README.md"
                    ),
                    "runtime_root": ".context-harness/runtime/context-maintain",
                    "sandbox": "read-only",
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_flat_workspace(self) -> None:
        for path, content in (
            (self.workspace / "README.md", "# Workspace\n"),
            (
                self.workspace / "current/index.md",
                "# Current\n\n- [memory](memory.md)\n- [state](state.md)\n",
            ),
            (self.workspace / "current/memory.md", "# Goal memory\n"),
            (self.workspace / "current/state.md", "# Current state\n"),
            (self.workspace / "output/index.md", "# Goal output\n"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def write_machine_workspace(self, workspace_id: str = "002-forming") -> None:
        identity = {
            "schema_version": 1,
            "workspace_id": workspace_id,
        }
        for path, content in (
            (
                self.workspace / "workspace.json",
                json.dumps(identity),
            ),
            (self.workspace / "README.md", "# Workspace\n"),
            (
                self.workspace / "current/memory/index.md",
                "# Memory\n\n- [goal](01-goal.md)\n",
            ),
            (
                self.workspace / "current/memory/01-goal.md",
                "# Goal\n",
            ),
            (
                self.workspace / "current/state/index.md",
                "# State\n",
            ),
            (self.workspace / "output/index.md", "# Output\n"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_explicit_absent_workspace_binds_only_after_flat_owner_links(self) -> None:
        config = load_config(self.config_path)

        self.assertEqual(config.workspace_root, self.workspace.resolve())
        self.assertFalse(config.workspace_bound)

        # Three conventional filenames do not prove identity, goal, and the
        # actual current Owners selected by the index.
        for path, content in (
            (self.workspace / "README.md", "# Workspace\n"),
            (self.workspace / "current/index.md", "# Current\n"),
            (self.workspace / "output/index.md", "# Output\n"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        self.assertFalse(config.workspace_bound)

        self.write_flat_workspace()
        self.assertTrue(config.workspace_bound)

    def test_machine_profile_requires_exact_identity_and_goal_entrypoint(self) -> None:
        config = load_config(self.config_path)
        self.write_machine_workspace()

        self.assertTrue(config.workspace_bound)

        (self.workspace / "current/memory/index.md").write_text(
            "# Memory without a goal link\n", encoding="utf-8"
        )
        self.assertFalse(config.workspace_bound)

    def test_machine_identity_mismatch_is_rejected_not_flattened(self) -> None:
        config = load_config(self.config_path)
        self.write_machine_workspace(workspace_id="003-other")

        with self.assertRaisesRegex(MaintainConfigError, "does not match"):
            _ = config.workspace_bound

    def test_partial_workspace_remains_unbound(self) -> None:
        self.workspace.mkdir()
        (self.workspace / "README.md").write_text(
            "# Workspace\n", encoding="utf-8"
        )

        config = load_config(self.config_path)

        self.assertFalse(config.workspace_bound)

    def test_binding_entrypoint_symlink_is_rejected(self) -> None:
        self.workspace.mkdir()
        outside = self.project / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        (self.workspace / "README.md").symlink_to(outside)

        config = load_config(self.config_path)

        with self.assertRaisesRegex(MaintainConfigError, "symlink"):
            _ = config.workspace_bound

    def test_flat_index_must_link_real_local_memory_and_state_owners(self) -> None:
        config = load_config(self.config_path)
        self.write_flat_workspace()
        (self.workspace / "current/index.md").write_text(
            "# Current\n\n- [memory](../memory.md)\n- [state](state.md)\n",
            encoding="utf-8",
        )

        self.assertFalse(config.workspace_bound)

    def test_checked_in_reference_machine_workspace_is_bound(self) -> None:
        reference_root = Path(__file__).resolve().parents[5]
        config = load_config(reference_root / ".codex/context-maintain.json")

        self.assertEqual(config.workspace_id, "001-default-timeout")
        self.assertTrue(config.workspace_bound)

    def test_manual_fallback_is_portable_and_root_connection_stays_thin(self) -> None:
        maintain_root = Path(__file__).resolve().parents[1]
        canonical_agent = (
            maintain_root / "workspace-context-maintainer.toml"
        ).read_text(encoding="utf-8")
        self.assertIn(".codex/context-maintain.json", canonical_agent)
        self.assertIn("workspace_id", canonical_agent)
        self.assertIn("work_root", canonical_agent)
        self.assertIn("maintain_contract_path", canonical_agent)

        repository_root = Path(__file__).resolve().parents[6]
        root_config_path = repository_root / ".codex/context-maintain.json"
        root_agent_path = (
            repository_root / ".codex/workspace-context-maintainer.toml"
        )
        if not root_config_path.exists() or not root_agent_path.exists():
            self.skipTest("root connection settings are outside this Project copy")

        root_config = load_config(root_config_path)
        self.assertEqual(
            root_config.workspace_id,
            "005-context-continuity-maintenance",
        )
        self.assertTrue(root_config.workspace_bound)
        root_agent = root_agent_path.read_text(encoding="utf-8")
        self.assertIn(
            "Maintain의 의미·판단·쓰기 계약을 여기서 다시 정의하지 않는다.",
            root_agent,
        )
        self.assertIn(".codex/context-maintain.json", root_agent)
        self.assertIn("workspace-context-maintainer.toml", root_agent)
        self.assertNotIn("Durable 변화가 없으면", root_agent)
        root_registration = (
            repository_root / ".codex/config.toml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'config_file = "workspace-context-maintainer.toml"',
            root_registration,
        )


if __name__ == "__main__":
    unittest.main()
