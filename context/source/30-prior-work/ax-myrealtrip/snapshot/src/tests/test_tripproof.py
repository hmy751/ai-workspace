from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scripts" / "tripproof.py"
FIXTURES = ROOT / "fixtures" / "loop-01"
CASE = FIXTURES / "case.json"


def run_cli(*args: str, expected_code: int = 0) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ENGINE), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != expected_code:
        raise AssertionError(
            f"unexpected exit {completed.returncode}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        )
    stream = completed.stdout if expected_code == 0 else completed.stderr
    return json.loads(stream)


def evaluate(plan: str, reply: str | None = None) -> dict:
    args = ["evaluate", "--case", str(CASE), "--plan", plan]
    if reply:
        args.extend(
            [
                "--reply",
                str(FIXTURES / reply),
                "--include-reply-decisions",
            ]
        )
    return run_cli(*args)


class Loop01EngineTests(unittest.TestCase):
    def assert_case_rejected(self, case: dict) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text(json.dumps(case, ensure_ascii=False), encoding="utf-8")
            return run_cli("validate", "--case", str(path), expected_code=2)

    def evaluate_reply_payload(
        self, reply: dict, *, expected_code: int = 0
    ) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reply.json"
            path.write_text(json.dumps(reply, ensure_ascii=False), encoding="utf-8")
            return run_cli(
                "evaluate",
                "--case",
                str(CASE),
                "--plan",
                "revision-a-c",
                "--reply",
                str(path),
                "--include-reply-decisions",
                expected_code=expected_code,
            )

    def test_original_stops_at_stroller_and_preserves_unknowns(self) -> None:
        result = evaluate("original")
        self.assertEqual(result["overall_status"], "보류")
        self.assertEqual(result["next_action"], "추가 확인")
        self.assertEqual(result["first_blocker"]["cell"], "participation")
        self.assertEqual(result["first_blocker"]["status"], "충돌")
        self.assertEqual(result["cells"]["start_time"]["status"], "답변 대기")
        self.assertEqual(result["cells"]["minor_ticket"]["status"], "정상")
        self.assertTrue(result["cells"]["minor_ticket"]["procedure"])

    def test_authorized_revision_preserves_original_and_follow_on_impacts(self) -> None:
        result = evaluate("revision-a-c")
        self.assertEqual(result["overall_status"], "확인 후 진행")
        self.assertEqual(result["next_action"], "추가 확인")
        self.assertEqual(result["participants"], ["A", "C"])
        self.assertEqual(result["cells"]["participation"]["status"], "정상")
        self.assertEqual(result["cells"]["base_price"]["burden"], "기본 투어비 유지")
        self.assertEqual(result["cells"]["start_time"]["status"], "답변 대기")
        self.assertEqual(result["cells"]["minor_ticket"]["status"], "정상")
        self.assertEqual(
            result["cells"]["minor_ticket"]["burden"],
            "미성년자 티켓 사전 메시지와 별도 구매 필요",
        )
        self.assertEqual(result["preserved_original"]["overall_status"], "보류")
        self.assertEqual(
            result["preserved_original"]["participation"]["status"], "충돌"
        )
        comparison = run_cli(
            "compare",
            "--case",
            str(CASE),
            "--before-plan",
            "original",
            "--after-plan",
            "revision-a-c",
        )
        unchanged = {
            item["path"]: item["value"]
            for item in comparison["decision_diff"]["unchanged_focus"]
        }
        self.assertEqual(
            unchanged["cells.minor_ticket.burden"],
            "미성년자 티켓 사전 메시지와 별도 구매 필요",
        )

    def test_vague_reply_has_no_decision_diff(self) -> None:
        comparison = run_cli(
            "compare",
            "--case",
            str(CASE),
            "--before-plan",
            "revision-a-c",
            "--after-plan",
            "revision-a-c",
            "--after-reply",
            str(FIXTURES / "reply-vague.json"),
        )
        self.assertEqual(comparison["decision_diff"]["changes"], [])
        rejected = comparison["after"]["reply_decisions"]["rejected"]
        self.assertEqual(rejected[0]["claim_id"], "vague-start-time-approved")

    def test_denied_reply_only_changes_time_to_conflict(self) -> None:
        before = evaluate("revision-a-c")
        after = evaluate("revision-a-c", "reply-denied.json")
        self.assertEqual(after["cells"]["start_time"]["status"], "충돌")
        self.assertEqual(after["cells"]["minor_ticket"], before["cells"]["minor_ticket"])
        self.assertEqual(after["overall_status"], "보류")
        self.assertEqual(after["next_action"], "추가 확인")
        self.assertEqual(after["cells"]["base_price"], before["cells"]["base_price"])
        self.assertEqual(
            after["preserved_original"], before["preserved_original"]
        )

    def test_complete_reply_updates_only_revision_and_enables_checkout_review(self) -> None:
        before = evaluate("revision-a-c")
        result = evaluate("revision-a-c", "reply-complete.json")
        self.assertEqual(result["overall_status"], "진행 가능")
        self.assertEqual(result["next_action"], "결제 검토")
        self.assertEqual(result["cells"]["start_time"]["status"], "정상")
        self.assertEqual(result["cells"]["minor_ticket"]["status"], "정상")
        self.assertEqual(
            result["cells"]["minor_ticket"], before["cells"]["minor_ticket"]
        )
        self.assertEqual(result["cells"]["base_price"]["burden"], "기본 투어비 유지")
        self.assertEqual(result["preserved_original"]["overall_status"], "보류")
        self.assertEqual(
            result["preserved_original"]["participation"]["status"], "충돌"
        )
        self.assertIn("보증하지 않습니다", result["boundary"])

    def test_complete_reply_is_idempotent(self) -> None:
        first = evaluate("revision-a-c", "reply-complete.json")
        second = evaluate("revision-a-c", "reply-complete.json")
        self.assertEqual(first, second)

    def test_same_input_is_deterministic_and_blocker_order_is_stable(self) -> None:
        first_raw = subprocess.check_output(
            [
                sys.executable,
                str(ENGINE),
                "evaluate",
                "--case",
                str(CASE),
                "--plan",
                "original",
            ],
            text=True,
        )
        second_raw = subprocess.check_output(
            [
                sys.executable,
                str(ENGINE),
                "evaluate",
                "--case",
                str(CASE),
                "--plan",
                "original",
            ],
            text=True,
        )
        self.assertEqual(first_raw, second_raw)
        result = json.loads(first_raw)
        self.assertEqual(list(result["cells"]), sorted(result["cells"]))
        self.assertEqual(result["first_blocker"]["cell"], "participation")

    def test_provenance_layers_remain_separate(self) -> None:
        result = evaluate("revision-a-c", "reply-complete.json")
        layers = result["provenance_layers"]
        self.assertEqual(layers["user_input_plan_id"], "revision-a-c")
        self.assertEqual(layers["seller_reply_id"], "reply-complete")
        self.assertIn("fact-stroller-allowed", layers["public_fact_claim_ids"])
        self.assertIn("fixture-conversation-continuity", layers["demo_assumption_ids"])

        case = json.loads(CASE.read_text(encoding="utf-8"))
        self.assertTrue(
            all(item["provenance"]["kind"] == "public_fact" for item in case["public_facts"])
        )
        self.assertTrue(
            all(item["provenance"]["kind"] == "user_input" for item in case["travel_party"])
        )

    def test_public_fact_value_types_are_strict(self) -> None:
        bad_values = {
            "stroller_allowed": "false",
            "default_start_time": "3pm",
            "alternate_start_requires_confirmation": 1,
            "flat_group_price_through": True,
            "minor_ticket_preparation": {"procedure": " "},
        }
        for fact_type, bad_value in bad_values.items():
            with self.subTest(fact_type=fact_type):
                case = json.loads(CASE.read_text(encoding="utf-8"))
                fact = next(
                    item for item in case["public_facts"] if item["type"] == fact_type
                )
                fact["value"] = bad_value
                error = self.assert_case_rejected(case)
                self.assertEqual(error["error"], "ContractError")

    def test_user_and_plan_shape_invariants_are_strict(self) -> None:
        mutations = {
            "requirement_bool": lambda case: case["requirements"][0].update(value=1),
            "is_minor_bool": lambda case: case["travel_party"][2].update(
                is_minor=1
            ),
            "age_int": lambda case: case["travel_party"][2].update(age=True),
            "iso_date": lambda case: case["plans"][0].update(date="2026-02-30"),
            "hhmm_time": lambda case: case["plans"][0].update(start_time="4pm"),
            "unique_participants": lambda case: case["plans"][0].update(
                participant_ids=["A", "A"]
            ),
            "nonempty_id": lambda case: case.update(case_id=" "),
        }
        for name, mutate in mutations.items():
            with self.subTest(invariant=name):
                case = json.loads(CASE.read_text(encoding="utf-8"))
                mutate(case)
                error = self.assert_case_rejected(case)
                self.assertEqual(error["error"], "ContractError")

    def test_seller_claim_schema_rejects_duplicates_and_ticket_claims(self) -> None:
        reply = json.loads(
            (FIXTURES / "reply-complete.json").read_text(encoding="utf-8")
        )
        duplicate_id = copy.deepcopy(reply)
        duplicate_id["claims"].append(copy.deepcopy(duplicate_id["claims"][0]))
        error = self.evaluate_reply_payload(duplicate_id, expected_code=2)
        self.assertIn("duplicate seller claim_id", error["message"])

        ticket_claim = copy.deepcopy(reply)
        ticket_claim["claims"][0]["type"] = "minor_ticket_procedure"
        error = self.evaluate_reply_payload(ticket_claim, expected_code=2)
        self.assertIn("unsupported", error["message"])

        integer_boolean = copy.deepcopy(reply)
        integer_boolean["claims"][0]["value"] = 1
        error = self.evaluate_reply_payload(integer_boolean, expected_code=2)
        self.assertIn("boolean", error["message"])

        mixed_provenance = copy.deepcopy(reply)
        mixed_provenance["claims"][0]["provenance"]["kind"] = "seller_reply"
        error = self.evaluate_reply_payload(mixed_provenance, expected_code=2)
        self.assertIn("must match", error["message"])

    def test_conflicting_time_claims_are_order_independent_errors(self) -> None:
        reply = json.loads(
            (FIXTURES / "reply-complete.json").read_text(encoding="utf-8")
        )
        approved = copy.deepcopy(reply["claims"][0])
        approved["claim_id"] = "approved"
        denied = copy.deepcopy(approved)
        denied["claim_id"] = "denied"
        denied["value"] = False

        messages = []
        for claims in ([approved, denied], [denied, approved]):
            candidate = copy.deepcopy(reply)
            candidate["claims"] = claims
            error = self.evaluate_reply_payload(candidate, expected_code=2)
            messages.append(error["message"])
        self.assertEqual(messages[0], messages[1])
        self.assertIn("conflicting", messages[0])

        duplicate = copy.deepcopy(approved)
        duplicate["claim_id"] = "approved-again"
        candidate = copy.deepcopy(reply)
        candidate["claims"] = [approved, duplicate]
        error = self.evaluate_reply_payload(candidate, expected_code=2)
        self.assertIn("duplicate", error["message"])

    def test_revision_must_reference_an_original_plan_directly(self) -> None:
        case = json.loads(CASE.read_text(encoding="utf-8"))
        revision = next(
            plan for plan in case["plans"] if plan["plan_id"] == "revision-a-c"
        )
        revision["base_plan_id"] = "revision-a-c"
        revision["authorized_changes"] = []
        error = self.assert_case_rejected(case)
        self.assertIn("must reference an original plan", error["message"])

        case = json.loads(CASE.read_text(encoding="utf-8"))
        revision = next(
            plan for plan in case["plans"] if plan["plan_id"] == "revision-a-c"
        )
        next_revision = copy.deepcopy(revision)
        next_revision["plan_id"] = "revision-next"
        next_revision["base_plan_id"] = "revision-a-c"
        next_revision["authorized_changes"] = []
        case["plans"].append(next_revision)
        error = self.assert_case_rejected(case)
        self.assertIn("must reference an original plan", error["message"])

    def test_exhausted_options_requires_boolean_and_user_provenance(self) -> None:
        case = json.loads(CASE.read_text(encoding="utf-8"))
        revision = next(
            plan for plan in case["plans"] if plan["plan_id"] == "revision-a-c"
        )
        revision["authorized_options_exhausted"] = "true"
        error = self.assert_case_rejected(case)
        self.assertIn("must be a boolean", error["message"])

        case = json.loads(CASE.read_text(encoding="utf-8"))
        revision = next(
            plan for plan in case["plans"] if plan["plan_id"] == "revision-a-c"
        )
        revision["authorized_options_exhausted"] = True
        error = self.assert_case_rejected(case)
        self.assertIn("provenance is required", error["message"])

        revision["authorized_options_exhausted_provenance"] = {
            "kind": "user_input",
            "source_ref": "turn-5",
            "excerpt": "더 허용할 수정안은 없어",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text(json.dumps(case, ensure_ascii=False), encoding="utf-8")
            result = run_cli("validate", "--case", str(path))
            exhausted_result = run_cli(
                "evaluate",
                "--case",
                str(path),
                "--plan",
                "revision-a-c",
                "--reply",
                str(FIXTURES / "reply-denied.json"),
            )
        self.assertTrue(result["valid"])
        self.assertEqual(exhausted_result["next_action"], "다른 상품 검토")

    def test_unauthorized_revision_is_rejected(self) -> None:
        case = json.loads(CASE.read_text(encoding="utf-8"))
        bad = copy.deepcopy(case)
        revision = next(plan for plan in bad["plans"] if plan["plan_id"] == "revision-a-c")
        revision["start_time"] = "15:00"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad-case.json"
            path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
            error = run_cli(
                "validate", "--case", str(path), expected_code=2
            )
        self.assertEqual(error["error"], "ContractError")
        self.assertIn("unauthorized", error["message"])


if __name__ == "__main__":
    unittest.main()
