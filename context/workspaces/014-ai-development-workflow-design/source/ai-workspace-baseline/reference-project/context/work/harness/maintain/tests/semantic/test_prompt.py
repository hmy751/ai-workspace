"""실행 도구 없이 판단 입력 구성과 입력 경계를 검증한다."""

import unittest

from context.work.harness.maintain.semantic.prompt import PromptBuilder
from context.work.harness.workspace_contract import HarnessError


class PromptTests(unittest.TestCase):
    def test_grounding_and_delta_keep_explicit_workspace_and_payload(self) -> None:
        prompt = PromptBuilder("001-example")
        grounding = prompt._grounding_prompt({"marker": "초기 근거"})
        delta = prompt._decision_prompt({"marker": "이번 응답"})
        self.assertIn("Explicit workspace_id: 001-example", grounding)
        self.assertIn("초기 근거", grounding)
        self.assertIn("<bounded_bootstrap>", grounding)
        self.assertIn("이번 응답", delta)
        self.assertIn("<bounded_response_delta>", delta)
        self.assertNotIn("초기 근거", delta)

    def test_nonserializable_payload_is_rejected_before_execution(self) -> None:
        with self.assertRaisesRegex(HarnessError, "not JSON serializable"):
            PromptBuilder("001-example")._decision_prompt({"invalid": object()})
