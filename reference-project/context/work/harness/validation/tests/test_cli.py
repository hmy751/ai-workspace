"""Harness 공통 CLI에서 두 책임의 진입점을 찾을 수 있는지 검증한다."""

from context.work.harness.testing import WorkspaceFixture


class HarnessCliTests(WorkspaceFixture):
    def test_module_help_exposes_recover_and_verify(self) -> None:
        completed = self.run_cli("--help")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("{recover,verify}", completed.stdout)
        self.assertIn("recover", completed.stdout)
        self.assertIn("verify", completed.stdout)

    def test_retired_maintain_command_is_rejected(self) -> None:
        completed = self.run_cli("maintain", "bootstrap", "001-example")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("invalid choice", completed.stderr)
