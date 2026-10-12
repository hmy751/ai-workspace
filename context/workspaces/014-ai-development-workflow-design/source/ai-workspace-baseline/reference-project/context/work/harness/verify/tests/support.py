"""Verify 전용 subprocess 시나리오를 필요한 테스트 묶음에서만 준비한다."""

from __future__ import annotations

from context.work.harness.testing import WorkspaceFixture


class VerifyFixture(WorkspaceFixture):
    verification_scenarios: tuple[str, ...] = ()

    def setUp(self) -> None:
        super().setUp()
        scenarios = {
            "delete_evidence": self._create_delete_evidence_scenario,
            "slow": self._create_slow_scenario,
            "noisy": self._create_noisy_scenario,
        }
        for scenario in self.verification_scenarios:
            scenarios[scenario]()

    def _create_delete_evidence_scenario(self) -> None:
        (self.project_root / "tests" / "test_delete_evidence.py").write_text(
            "from pathlib import Path\n"
            "import unittest\n\n"
            "class DeleteEvidenceTests(unittest.TestCase):\n"
            "    def test_delete_then_fail(self):\n"
            "        Path('src/value.txt').unlink()\n"
            "        self.fail('intentional failure after evidence deletion')\n",
            encoding="utf-8",
        )

    def _create_slow_scenario(self) -> None:
        (self.project_root / "tests" / "test_slow.py").write_text(
            "import time\n"
            "import unittest\n\n"
            "class SlowTests(unittest.TestCase):\n"
            "    def test_slow(self):\n"
            "        time.sleep(2)\n",
            encoding="utf-8",
        )

    def _create_noisy_scenario(self) -> None:
        (self.project_root / "tests" / "test_noisy.py").write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "import unittest\n\n"
            "class NoisyTests(unittest.TestCase):\n"
            "    def test_noisy(self):\n"
            "        roots = str(Path.cwd()) * 50\n"
            "        print(roots + 'X' * 2000)\n"
            "        print(roots + 'Y' * 2000, file=sys.stderr)\n",
            encoding="utf-8",
        )
