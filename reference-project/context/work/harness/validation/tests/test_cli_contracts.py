"""공통 CLI의 입력 경계·오류 반환과 기존 공개 경로 호환을 검증한다."""

from __future__ import annotations

import io
import unittest
from unittest.mock import patch

from context.work.harness import cli, recover, verify
from context.work.harness.recover import operation as recover_compat
from context.work.harness.verify import operation as verify_compat
from context.work.harness.workspace import HarnessError


class HarnessCliContractTests(unittest.TestCase):
    def test_legacy_operation_paths_refer_to_the_public_implementations(self) -> None:
        self.assertIs(
            recover_compat.build_recovery_packet, recover.build_recovery_packet
        )
        self.assertIs(
            recover_compat.render_recovery_packet, recover.render_recovery_packet
        )
        self.assertIs(verify_compat.verify_workspace, verify.verify_workspace)

    def test_harness_contract_error_returns_two_on_stderr_without_success_output(
        self,
    ) -> None:
        output, errors = io.StringIO(), io.StringIO()
        with (
            patch.object(
                cli, "build_recovery_packet", side_effect=HarnessError("unsafe")
            ),
            patch.object(cli.sys, "stdout", output),
            patch.object(cli.sys, "stderr", errors),
        ):
            exit_code = cli.main(["recover", "001-example", "--json"])
        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(errors.getvalue(), "workspace harness error: unsafe\n")
