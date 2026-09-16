"""Maintain test_decision 시나리오."""

from __future__ import annotations

import copy

from context.work.harness.maintain import validate_maintain_decision
from context.work.harness.workspace_contract import HarnessError

from ..support.apply import MaintainApplyFixture


class TestDecision(MaintainApplyFixture):
    def test_decision_schema_and_outcome_combinations_are_exact(self) -> None:
        valid_no_change = self.decision("no_change")
        validated = validate_maintain_decision(valid_no_change, "001-example")
        self.assertEqual(validated["outcome"], "no_change")

        cases: list[dict[str, object]] = []
        extra = copy.deepcopy(valid_no_change)
        extra["extra"] = True
        cases.append(extra)
        wrong_workspace = copy.deepcopy(valid_no_change)
        wrong_workspace["workspace_id"] = "002-other"
        cases.append(wrong_workspace)
        wrong_no_change = copy.deepcopy(valid_no_change)
        wrong_no_change["importance"] = "quiet"
        cases.append(wrong_no_change)
        empty_update = self.decision("update")
        cases.append(empty_update)
        ambiguous_write = self.decision(
            "needs_user_decision",
            question="Choose one?",
            changes=[
                {
                    "path": "source/index.md",
                    "expected_sha256": None,
                    "content": "# forbidden\n",
                    "reason": "Ambiguity cannot write.",
                }
            ],
        )
        cases.append(ambiguous_write)

        for decision in cases:
            with self.subTest(decision=decision):
                with self.assertRaises(HarnessError):
                    validate_maintain_decision(decision, "001-example")
