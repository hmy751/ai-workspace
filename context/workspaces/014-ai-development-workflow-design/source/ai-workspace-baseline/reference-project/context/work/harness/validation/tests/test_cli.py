"""Harness 공통 CLI에서 세 책임의 진입점을 찾을 수 있는지 검증한다."""

from context.work.harness.testing import WorkspaceFixture


class HarnessCliTests(WorkspaceFixture):
    def test_module_help_exposes_recover_maintain_and_verify(self) -> None:
        completed = self.run_cli("--help")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("{recover,maintain,verify}", completed.stdout)
        self.assertIn("recover", completed.stdout)
        self.assertIn("maintain", completed.stdout)
        self.assertIn("verify", completed.stdout)
