from __future__ import annotations

import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest import mock

from context.work.harness.maintain.config import (
    CONFIG_JSON_SCHEMA,
    MaintainConfig,
    MaintainConfigError,
    load_config,
)
from context.work.harness.maintain.controller import (
    MAX_PENDING_NOTICE_CHARACTERS,
    MAX_PENDING_REPORTS_PER_NOTICE,
    RECOVERY_ATTEMPTS_BEFORE_WARNING,
    MaintainController,
)
from context.work.harness.maintain.intent import (
    DecisionIntentError,
    DecisionIntentStore,
    INTENT_FILENAME,
    INTENT_LOCK_FILENAME,
)
from context.work.harness.maintain.runner import (
    CodexTimeoutError,
    MaintainerDecision,
    MaintainerRunnerError,
    MaintainerTurn,
    ProposedWrite,
)
from context.work.harness.maintain.runtime import MaintainRuntime
from context.work.harness.maintain.writer import apply_writes, sha256_text


WORKSPACE_ID = "005-context-continuity-maintenance"


def session_start(
    source: str = "startup", session_id: str = "main-session"
) -> dict[str, str]:
    return {
        "hook_event_name": "SessionStart",
        "session_id": session_id,
        "source": source,
    }


def user(
    turn_id: str,
    prompt: str = "user evidence",
    session_id: str = "main-session",
) -> dict[str, str]:
    return {
        "hook_event_name": "UserPromptSubmit",
        "session_id": session_id,
        "turn_id": turn_id,
        "prompt": prompt,
    }


def stop(
    turn_id: str,
    answer: str = "assistant evidence",
    session_id: str = "main-session",
) -> dict[str, str]:
    return {
        "hook_event_name": "Stop",
        "session_id": session_id,
        "turn_id": turn_id,
        "last_assistant_message": answer,
    }


def post_tool(turn_id: str) -> dict[str, object]:
    return {
        "hook_event_name": "PostToolUse",
        "session_id": "main-session",
        "turn_id": turn_id,
        "tool_name": "apply_patch",
        "tool_use_id": "tool-use-1",
        "tool_input": "*** Update File: current/state.md\n@@\n-old\n+new",
        "tool_response": {"status": "completed"},
    }


def prompt_event_id(prompt: str) -> str:
    match = re.search(r'"event_id":\s*"([^"]+)"', prompt)
    if match is None:
        raise AssertionError("prompt has no event_id")
    return match.group(1)


def first_unresolved_report_id(prompt: str) -> str:
    match = re.search(r'"report_id":\s*"([0-9a-f]{32})"', prompt)
    if match is None:
        raise AssertionError("prompt has no unresolved report id")
    return match.group(1)


def decision_for(
    prompt: str,
    *,
    outcome: str = "no_change",
    summary: str = "목표, 상태, 다음 행동",
    writes: tuple[ProposedWrite, ...] = (),
    changed_paths: tuple[str, ...] | None = None,
    question: str | None = None,
    resolved_report_ids: tuple[str, ...] = (),
) -> MaintainerDecision:
    paths = (
        tuple(write.path for write in writes)
        if changed_paths is None
        else changed_paths
    )
    return MaintainerDecision(
        outcome=outcome,
        workspace_id=WORKSPACE_ID,
        event_id=prompt_event_id(prompt),
        summary=summary,
        changed_paths=paths,
        writes=writes,
        question=question,
        evidence_paths=(),
        resolved_report_ids=resolved_report_ids,
    )


class FakeRunner:
    def __init__(
        self,
        *,
        thread_id: str,
        script: list[object],
    ) -> None:
        self._thread_id = thread_id
        self.script = script
        self.prompts: list[str] = []

    @property
    def thread_id(self) -> str:
        return self._thread_id

    def run(self, prompt: str) -> MaintainerTurn:
        self.prompts.append(prompt)
        if not self.script:
            raise AssertionError("unexpected runner call")
        step = self.script.pop(0)
        if isinstance(step, BaseException):
            raise step
        if callable(step):
            result = step(prompt)
        else:
            result = step
        if not isinstance(result, MaintainerDecision):
            raise AssertionError("fake step did not return a decision")
        return MaintainerTurn(thread_id=self._thread_id, decision=result)


class FakeRunnerFactory:
    def __init__(self, *scripts: list[object]) -> None:
        self.scripts = list(scripts)
        self.calls: list[dict[str, object]] = []
        self.runners: list[FakeRunner] = []

    def __call__(self, **kwargs: object) -> FakeRunner:
        if not self.scripts:
            raise AssertionError("unexpected runner construction")
        initial = kwargs.get("initial_thread_id")
        thread_id = (
            str(initial)
            if isinstance(initial, str)
            else f"maintainer-thread-{len(self.calls) + 1}"
        )
        runner = FakeRunner(thread_id=thread_id, script=self.scripts.pop(0))
        self.calls.append(dict(kwargs))
        self.runners.append(runner)
        return runner


class FailOnce:
    def __init__(self, point: str) -> None:
        self.point = point
        self.triggered = False

    def __call__(self, observed: str) -> None:
        if observed == self.point and not self.triggered:
            self.triggered = True
            raise OSError(f"injected fault at {observed}")


class ProjectFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name) / "project"
        self.codex = self.project / ".codex"
        self.workspace = (
            self.project
            / "context/work/workspaces"
            / WORKSPACE_ID
        )
        for path in (
            self.codex,
            self.project / "context/work/harness/maintain",
            self.workspace / "current",
            self.workspace / "current/memory",
            self.workspace / "current/state",
            self.workspace / "records",
            self.workspace / "output",
            self.workspace / "source",
        ):
            path.mkdir(parents=True, exist_ok=True)
        (self.project / "context/work/harness/maintain/README.md").write_text(
            "# Maintain\n", encoding="utf-8"
        )
        (self.workspace / "README.md").write_text(
            "# Workspace\n", encoding="utf-8"
        )
        (self.workspace / "workspace.json").write_text(
            json.dumps(
                {"schema_version": 1, "workspace_id": WORKSPACE_ID}
            ),
            encoding="utf-8",
        )
        (self.workspace / "current/index.md").write_text(
            "# Current\n", encoding="utf-8"
        )
        (self.workspace / "current/memory/index.md").write_text(
            "# Memory\n\n- [goal](01-goal.md)\n", encoding="utf-8"
        )
        (self.workspace / "current/memory/01-goal.md").write_text(
            "# Goal\n", encoding="utf-8"
        )
        (self.workspace / "current/state/index.md").write_text(
            "# State index\n", encoding="utf-8"
        )
        (self.workspace / "current/state.md").write_text(
            "# State\n\nold\n", encoding="utf-8"
        )
        (self.workspace / "output/index.md").write_text(
            "# Output\n", encoding="utf-8"
        )
        (self.workspace / "source/index.md").write_text(
            "# Source\n", encoding="utf-8"
        )
        self.config_path = self.codex / "context-maintain.json"
        self.config_value: dict[str, object] = {
            "schema": "context-maintain.config.v1",
            "workspace_id": WORKSPACE_ID,
            "work_root": "context/work",
            "maintain_contract_path": (
                "context/work/harness/maintain/README.md"
            ),
            "runtime_root": ".codex/runtime/context-maintain",
            "sandbox": "read-only",
        }
        self.write_config()
        self.config = load_config(self.config_path)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_config(self) -> None:
        self.config_path.write_text(
            json.dumps(self.config_value), encoding="utf-8"
        )

    def controller(self, factory: FakeRunnerFactory) -> MaintainController:
        return MaintainController(self.config, runner_factory=factory)

    def pair(self, controller: MaintainController, turn_id: str) -> None:
        controller.capture_user_prompt(user(turn_id))
        result = controller.capture_stop(stop(turn_id))
        self.assertTrue(result["paired"])

    def ground(self, controller: MaintainController) -> None:
        result = controller.session_start(session_start())
        self.assertTrue(result.grounded_now)


class StrictConfigTests(ProjectFixture):
    def test_schema_declares_default_executable_and_read_only_sandbox(self) -> None:
        self.assertEqual(self.config.project_root, self.project.resolve())
        self.assertEqual(self.config.codex_executable, "codex")
        self.assertEqual(
            CONFIG_JSON_SCHEMA["properties"]["codex_executable"]["default"],
            "codex",
        )
        self.assertEqual(
            CONFIG_JSON_SCHEMA["properties"]["sandbox"]["const"],
            "read-only",
        )

    def test_rejects_extra_fields_traversal_and_non_read_only(self) -> None:
        mutations = (
            {"extra": True},
            {"runtime_root": "../outside"},
            {"sandbox": "workspace-write"},
            {"workspace_id": "../other"},
            {"workspace_id": "005-Uppercase"},
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                original = dict(self.config_value)
                self.config_value.update(mutation)
                self.write_config()
                with self.assertRaises(MaintainConfigError):
                    load_config(self.config_path)
                self.config_value = original

    def test_rejects_workspace_symlink(self) -> None:
        real_workspace = self.workspace.parent / "real-workspace"
        self.workspace.rename(real_workspace)
        self.workspace.symlink_to(real_workspace, target_is_directory=True)
        with self.assertRaisesRegex(MaintainConfigError, "symlink"):
            load_config(self.config_path)

    def test_config_must_be_under_dot_codex(self) -> None:
        outside = self.project / "maintain.json"
        outside.write_text(json.dumps(self.config_value), encoding="utf-8")
        with self.assertRaisesRegex(MaintainConfigError, r"\.codex"):
            MaintainConfig.load(outside)


class ControllerSessionTests(ProjectFixture):
    def test_initial_grounding_is_saved_and_resume_reuses_warm_state(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt, summary="목표와 다음 작업")]
        )
        controller = self.controller(factory)

        result = controller.session_start(session_start())
        resumed = controller.session_start(session_start(source="resume"))

        self.assertTrue(result.grounded_now)
        self.assertEqual(result.summary, "목표와 다음 작업")
        self.assertFalse(resumed.grounded_now)
        self.assertEqual(len(factory.calls), 1)
        state = controller.runtime.load_agent_state("main-session")
        self.assertTrue(state["grounded"])
        self.assertEqual(state["thread_id"], "maintainer-thread-1")
        self.assertIn("current/", factory.runners[0].prompts[0])

    def test_compact_never_resets_or_bootstraps_missing_state(self) -> None:
        factory = FakeRunnerFactory()
        controller = self.controller(factory)

        result = controller.session_start(session_start(source="compact"))

        self.assertFalse(result.grounded_now)
        self.assertEqual(factory.calls, [])
        state = controller.runtime.load_agent_state("main-session")
        self.assertFalse(state["grounded"])

    def test_resume_with_missing_state_performs_bounded_grounding(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt, summary="resume에서 복구")]
        )
        controller = self.controller(factory)

        result = controller.session_start(session_start(source="resume"))

        self.assertTrue(result.grounded_now)
        self.assertEqual(len(factory.runners[0].prompts), 1)
        self.assertTrue(
            controller.runtime.load_agent_state("main-session")["grounded"]
        )

    def test_new_session_waits_for_prior_response_then_regrounds_warm_thread(
        self,
    ) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt, summary="대기 중 방향")],
            [
                lambda prompt: decision_for(prompt, summary="이전 세션 grounding"),
                lambda prompt: decision_for(prompt, summary="이전 응답 처리"),
            ],
            [
                lambda prompt: decision_for(prompt, summary="최신 current 재동기화"),
                lambda prompt: decision_for(prompt, summary="새 응답 처리"),
            ],
        )
        controller = self.controller(factory)
        controller.capture_user_prompt(
            user("old-turn", session_id="old-session")
        )
        controller.capture_stop(
            stop("old-turn", session_id="old-session")
        )

        started = controller.session_start(
            session_start(session_id="new-session")
        )
        self.assertFalse(started.freshness_ready)
        self.assertFalse(
            controller.runtime.load_agent_state("new-session")["grounded"]
        )
        controller.capture_user_prompt(
            user("new-turn", session_id="new-session")
        )
        controller.capture_stop(
            stop("new-turn", session_id="new-session")
        )
        blocked = controller.process_session("new-session")
        self.assertEqual(blocked["status"], "waiting_prior")
        self.assertEqual(blocked["retry_attempts"], 0)
        self.assertIsNone(
            controller.runtime.status("new-session")["failure"]["code"]
        )
        self.assertEqual(len(factory.runners), 1)

        old = controller.process_session("old-session")
        self.assertEqual(old["outcomes"], {"no_change": 1})
        resumed = controller.process_session("new-session")
        self.assertEqual(resumed["outcomes"], {"no_change": 1})
        self.assertEqual(len(factory.runners[2].prompts), 2)
        self.assertTrue(
            controller.runtime.load_agent_state("new-session")["grounded"]
        )

    def test_no_change_advances_cursor_and_keeps_warm_thread(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [lambda prompt: decision_for(prompt, summary="변화 없음")],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-1")

        result = controller.process_session("main-session")

        self.assertEqual(result["processed"], 1)
        self.assertEqual(result["outcomes"], {"no_change": 1})
        self.assertEqual(
            factory.calls[1]["initial_thread_id"], "maintainer-thread-1"
        )
        status = controller.status("main-session")
        self.assertEqual(status["freshness"]["processed_sequence"], 1)
        self.assertEqual(status["freshness"]["state"], "fresh")

    def test_sanitized_tool_evidence_reaches_response_prompt(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [lambda prompt: decision_for(prompt, summary="증거 확인")],
        )
        controller = self.controller(factory)
        self.ground(controller)
        controller.capture_user_prompt(user("turn-tool"))
        captured = controller.capture_post_tool_use(post_tool("turn-tool"))
        self.assertTrue(captured["recorded"])
        controller.capture_stop(stop("turn-tool"))

        result = controller.process_session("main-session")

        self.assertEqual(result["processed"], 1)
        response_prompt = factory.runners[1].prompts[0]
        self.assertIn('"tool_name": "apply_patch"', response_prompt)
        self.assertIn('"path": "current/state.md"', response_prompt)
        self.assertNotIn("@@", response_prompt)

    def test_guarded_current_write_and_quiet_outcome(self) -> None:
        old = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        write = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text(old),
            content="# State\n\nnew\n",
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_quiet",
                    summary="상태 반영",
                    writes=(write,),
                )
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-1")

        result = controller.process_session("main-session")

        self.assertEqual(result["outcomes"], {"updated_quiet": 1})
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            "# State\n\nnew\n",
        )
        self.assertEqual(controller.runtime.pending_reports("main-session"), [])
        self.assertFalse(
            (
                controller.runtime.session_runtime_root("main-session")
                / INTENT_FILENAME
            ).exists()
        )

    def test_routes_memory_record_index_and_output_in_one_guarded_decision(
        self,
    ) -> None:
        output_path = self.workspace / "output/index.md"
        output_before = output_path.read_text(encoding="utf-8")
        memory_index_path = self.workspace / "current/memory/index.md"
        memory_index_before = memory_index_path.read_text(encoding="utf-8")
        writes = (
            ProposedWrite(
                path="current/memory/index.md",
                expected_sha256=sha256_text(memory_index_before),
                content=(
                    "# Memory\n\n"
                    "- [goal](01-goal.md)\n"
                    "- 지속 기준\n"
                ),
            ),
            ProposedWrite(
                path="records/index.md",
                expected_sha256=None,
                content=(
                    "# Records\n\n"
                    "- [반영 기록](2026-08-17-maintain-routing.md)\n"
                ),
            ),
            ProposedWrite(
                path="records/2026-08-17-maintain-routing.md",
                expected_sha256=None,
                content="# Maintain routing\n\n지속 변화의 근거.\n",
            ),
            ProposedWrite(
                path="output/index.md",
                expected_sha256=sha256_text(output_before),
                content="# Output\n\n현재 선택 산출물 위치.\n",
            ),
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_report",
                    summary="지속 기준과 기록, 산출물 지도를 반영함",
                    writes=writes,
                )
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-routing")

        result = controller.process_session("main-session")

        self.assertEqual(result["outcomes"], {"updated_report": 1})
        for proposal in writes:
            self.assertEqual(
                (self.workspace / proposal.path).read_text(encoding="utf-8"),
                proposal.content,
            )
        notice = controller.take_pending_notice("main-session")
        self.assertIn("지속 기준과 기록", notice.additional_context or "")
        for proposal in writes:
            self.assertIn(proposal.path, notice.additional_context or "")

    def test_important_update_becomes_sanitized_pending_notice(self) -> None:
        old = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        secret_content = "# State\n\nprivate exact conversation\n"
        write = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text(old),
            content=secret_content,
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_report",
                    summary="중요 상태를 반영함",
                    writes=(write,),
                )
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-1")
        controller.process_session("main-session")

        pending = controller.runtime.pending_reports("main-session")
        serialized = json.dumps(pending, ensure_ascii=False)
        self.assertNotIn("private exact conversation", serialized)
        notice = controller.take_pending_notice("main-session")

        self.assertIn("중요 상태를 반영함", notice.additional_context or "")
        self.assertIn("current/state.md", notice.additional_context or "")
        self.assertIsNone(notice.system_message)
        self.assertNotEqual(controller.runtime.pending_reports("main-session"), [])
        controller.acknowledge_notice("main-session", notice.report_ids)
        self.assertEqual(controller.runtime.pending_reports("main-session"), [])

    def test_ambiguity_is_pending_without_write(self) -> None:
        before = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="needs_decision",
                    summary="Owner가 애매함",
                    question="이 결정을 current에 둘까요?",
                )
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-1")

        result = controller.process_session("main-session")
        notice = controller.take_pending_notice("main-session")

        self.assertEqual(result["outcomes"], {"needs_decision": 1})
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            before,
        )
        self.assertIn("이 결정을 current에 둘까요?", notice.additional_context or "")
        self.assertIsNotNone(notice.system_message)

    def test_resume_failure_rebootstraps_once_and_rejudges_same_event(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [MaintainerRunnerError("resume failed")],
            [
                lambda prompt: decision_for(prompt, summary="다시 이해함"),
                lambda prompt: decision_for(prompt, summary="재판단 완료"),
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-1")

        result = controller.process_session("main-session")

        self.assertEqual(result["processed"], 1)
        self.assertEqual(len(factory.calls), 3)
        self.assertEqual(
            factory.calls[1]["initial_thread_id"], "maintainer-thread-1"
        )
        self.assertIsNone(factory.calls[2]["initial_thread_id"])
        first_event = prompt_event_id(factory.runners[1].prompts[0])
        replay_event = prompt_event_id(factory.runners[2].prompts[1])
        self.assertEqual(first_event, replay_event)
        state = controller.runtime.load_agent_state("main-session")
        self.assertEqual(state["thread_id"], "maintainer-thread-3")

    def test_freshness_failed_is_retryable_and_never_advances_cursor(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="freshness_failed",
                    summary="신뢰 복구 실패",
                )
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-1")

        result = controller.process_session("main-session")
        status = controller.status("main-session")

        self.assertEqual(result["status"], "retry")
        self.assertEqual(status["freshness"]["processed_sequence"], 0)
        self.assertEqual(status["freshness"]["state"], "retry_pending")

    def test_retry_is_silent_until_bounded_recovery_is_exhausted(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            *[
                [
                    lambda prompt: decision_for(
                        prompt,
                        outcome="freshness_failed",
                        summary="아직 복구하지 못함",
                    )
                ]
                for _ in range(RECOVERY_ATTEMPTS_BEFORE_WARNING)
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-recovery")

        for attempt in range(1, RECOVERY_ATTEMPTS_BEFORE_WARNING + 1):
            result = controller.process_session("main-session")
            notice = controller.take_pending_notice("main-session")
            self.assertEqual(result["status"], "retry")
            self.assertEqual(result["retry_attempts"], attempt)
            self.assertEqual(
                result["successor_required"],
                attempt < RECOVERY_ATTEMPTS_BEFORE_WARNING,
            )
            if attempt < RECOVERY_ATTEMPTS_BEFORE_WARNING:
                self.assertIsNone(notice.additional_context)
                self.assertIsNone(notice.system_message)
            else:
                self.assertIn(
                    "신뢰할 수 없습니다", notice.additional_context or ""
                )
                self.assertEqual(
                    notice.system_message,
                    "Maintain freshness를 자동 복구하지 못했습니다.",
                )
        notice = controller.take_pending_notice("main-session")
        self.assertIn("신뢰할 수 없습니다", notice.additional_context or "")

    def test_stale_write_does_not_advance_cursor_or_claim_success(self) -> None:
        stale = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text("not the current file"),
            content="# State\n\nproposed\n",
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_report",
                    summary="반영 시도",
                    writes=(stale,),
                )
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-1")

        result = controller.process_session("main-session")
        status = controller.status("main-session")

        self.assertEqual(result["status"], "retry")
        self.assertEqual(status["freshness"]["processed_sequence"], 0)
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            "# State\n\nold\n",
        )
        self.assertEqual(controller.runtime.pending_reports("main-session"), [])
        self.assertFalse(
            (
                controller.runtime.session_runtime_root("main-session")
                / INTENT_FILENAME
            ).exists()
        )
        self.assertFalse(
            controller.runtime.load_agent_state("main-session")["grounded"]
        )

    def test_stale_write_is_regrounded_and_rejudged_on_retry(self) -> None:
        stale = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text("not the current file"),
            content="# State\n\nstale proposal\n",
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_quiet",
                    writes=(stale,),
                )
            ],
            [
                lambda prompt: decision_for(prompt, summary="최신본 재동기화"),
                lambda prompt: decision_for(prompt, summary="재판단 완료"),
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-stale-rejudge")

        first = controller.process_session("main-session")
        second = controller.process_session("main-session")

        self.assertEqual(first["status"], "retry")
        self.assertEqual(second["outcomes"], {"no_change": 1})
        self.assertEqual(
            controller.status("main-session")["freshness"][
                "processed_sequence"
            ],
            1,
        )
        self.assertEqual(len(factory.runners[2].prompts), 2)

    def test_crash_before_writer_replays_exact_intent_without_agent(self) -> None:
        old = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        write = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text(old),
            content="# State\n\nnew after retry\n",
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_report",
                    summary="원래 중요 보고",
                    writes=(write,),
                )
            ],
        )
        calls = 0

        def fail_before_writer(
            workspace_root: Path,
            runtime_root: Path,
            proposals: tuple[object, ...],
            *,
            transaction_key: str | None = None,
        ) -> object:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("before writer")
            return apply_writes(
                workspace_root,
                runtime_root,
                proposals,
                transaction_key=transaction_key,
            )

        controller = MaintainController(
            self.config,
            runner_factory=factory,
            writer_apply=fail_before_writer,
        )
        self.ground(controller)
        self.pair(controller, "turn-before-writer")

        first = controller.process_session("main-session")
        intent_path = (
            controller.runtime.session_runtime_root("main-session")
            / INTENT_FILENAME
        )
        self.assertEqual(first["status"], "retry")
        self.assertTrue(intent_path.exists())
        self.assertEqual(len(factory.calls), 2)
        persisted = json.loads(intent_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted["thread_id"], "maintainer-thread-1")
        self.assertEqual(persisted["decision"]["summary"], "원래 중요 보고")
        self.assertEqual(persisted["proposals"][0]["content"], write.content)
        self.assertEqual(
            persisted["processor_result"]["report"]["summary"],
            "원래 중요 보고",
        )

        replay = controller.process_session("main-session")

        self.assertEqual(replay["outcomes"], {"updated_report": 1})
        self.assertEqual(len(factory.calls), 2)
        self.assertFalse(intent_path.exists())
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            write.content,
        )
        notice = controller.take_pending_notice("main-session")
        self.assertIn("원래 중요 보고", notice.additional_context or "")

    def test_crash_after_writer_accepts_only_exact_new_targets_on_replay(
        self,
    ) -> None:
        old = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        write = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text(old),
            content="# State\n\nwriter already committed\n",
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_quiet",
                    summary="조용한 반영",
                    writes=(write,),
                )
            ],
        )
        calls = 0

        def fail_after_writer(
            workspace_root: Path,
            runtime_root: Path,
            proposals: tuple[object, ...],
            *,
            transaction_key: str | None = None,
        ) -> object:
            nonlocal calls
            result = apply_writes(
                workspace_root,
                runtime_root,
                proposals,
                transaction_key=transaction_key,
            )
            calls += 1
            if calls == 1:
                raise OSError("after writer")
            return result

        controller = MaintainController(
            self.config,
            runner_factory=factory,
            writer_apply=fail_after_writer,
        )
        self.ground(controller)
        self.pair(controller, "turn-after-writer")

        first = controller.process_session("main-session")
        self.assertEqual(first["status"], "retry")
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            write.content,
        )

        replay = controller.process_session("main-session")

        self.assertEqual(replay["outcomes"], {"updated_quiet": 1})
        self.assertEqual(len(factory.calls), 2)
        self.assertFalse(
            (
                controller.runtime.session_runtime_root("main-session")
                / INTENT_FILENAME
            ).exists()
        )

    def test_checkpoint_crash_preserves_report_and_clears_intent_on_reentry(
        self,
    ) -> None:
        old = (self.workspace / "current/state.md").read_text(encoding="utf-8")
        write = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text(old),
            content="# State\n\ncheckpoint edge\n",
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_report",
                    summary="체크포인트 직전 보고",
                    writes=(write,),
                )
            ],
        )
        runtime = MaintainRuntime(
            runtime_root=self.config.runtime_root,
            workspace_id=self.config.workspace_id,
            fault_injector=FailOnce("after_checkpoint_before_cleanup"),
        )
        controller = MaintainController(
            self.config,
            runtime=runtime,
            runner_factory=factory,
        )
        self.ground(controller)
        self.pair(controller, "turn-checkpoint")

        with self.assertRaises(OSError):
            controller.process_session("main-session")
        intent_path = runtime.session_runtime_root("main-session") / INTENT_FILENAME
        self.assertTrue(intent_path.exists())
        self.assertEqual(len(factory.calls), 2)

        recovered = controller.process_session("main-session")

        self.assertEqual(recovered["status"], "idle")
        self.assertEqual(len(factory.calls), 2)
        self.assertFalse(intent_path.exists())
        notice = controller.take_pending_notice("main-session")
        self.assertIn("체크포인트 직전 보고", notice.additional_context or "")

    def test_malformed_agent_state_is_quarantined_then_bootstrapped_once(
        self,
    ) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(prompt, summary="canonical 복구"),
                lambda prompt: decision_for(prompt, summary="복구 뒤 판단"),
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        session_root = controller.runtime.session_runtime_root("main-session")
        (session_root / "agent-state.json").write_text(
            '{"schema":"broken"}', encoding="utf-8"
        )
        self.pair(controller, "turn-malformed-state")

        result = controller.process_session("main-session")

        self.assertEqual(result["outcomes"], {"no_change": 1})
        self.assertEqual(len(factory.calls), 2)
        self.assertIsNone(factory.calls[1]["initial_thread_id"])
        self.assertEqual(len(factory.runners[1].prompts), 2)
        self.assertEqual(
            controller.runtime.status("main-session")["counts"][
                "agent_state_quarantined"
            ],
            1,
        )
        self.assertEqual(len(list((session_root / "quarantine").iterdir())), 1)

    def test_timeout_does_not_start_immediate_rebootstrap(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [CodexTimeoutError(0.01)],
            [lambda prompt: decision_for(prompt)],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-timeout")

        result = controller.process_session("main-session")

        self.assertEqual(result["status"], "retry")
        self.assertEqual(len(factory.calls), 2)
        self.assertEqual(
            controller.status("main-session")["freshness"][
                "processed_sequence"
            ],
            0,
        )

    def test_forming_no_write_intent_survives_concurrent_binding(self) -> None:
        for path in (
            self.workspace / "README.md",
            self.workspace / "current/index.md",
            self.workspace / "output/index.md",
        ):
            path.unlink()
        self.assertFalse(self.config.workspace_bound)
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt, summary="형성 중")],
            [lambda prompt: decision_for(prompt, summary="아직 형성 중")],
            [
                lambda prompt: decision_for(prompt, summary="새 Owner 이해"),
                lambda prompt: decision_for(prompt, summary="바인딩 뒤 판단"),
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.assertFalse(
            controller.runtime.load_agent_state("main-session")[
                "workspace_bound"
            ]
        )
        self.pair(controller, "turn-forming")

        with mock.patch.object(
            controller.runtime,
            "save_agent_state",
            side_effect=OSError("after intent before checkpoint"),
        ):
            first = controller.process_session("main-session")
        self.assertEqual(first["status"], "retry")
        self.assertEqual(len(factory.calls), 2)

        for path, content in (
            (self.workspace / "README.md", "# Workspace\n"),
            (self.workspace / "current/index.md", "# Current\n"),
            (self.workspace / "output/index.md", "# Output\n"),
        ):
            path.write_text(content, encoding="utf-8")
        self.assertTrue(self.config.workspace_bound)

        replay = controller.process_session("main-session")

        self.assertEqual(replay["outcomes"], {"no_change": 1})
        self.assertEqual(len(factory.calls), 2)
        self.assertFalse(
            controller.runtime.load_agent_state("main-session")[
                "workspace_bound"
            ]
        )

        self.pair(controller, "turn-bound")
        bound = controller.process_session("main-session")

        self.assertEqual(bound["outcomes"], {"no_change": 1})
        self.assertEqual(len(factory.calls), 3)
        self.assertEqual(len(factory.runners[2].prompts), 2)
        self.assertIn('"workspace_bound": true', factory.runners[2].prompts[0])
        self.assertTrue(
            controller.runtime.load_agent_state("main-session")[
                "workspace_bound"
            ]
        )

    def test_forming_workspace_rejects_agent_write_before_intent(self) -> None:
        for path in (
            self.workspace / "README.md",
            self.workspace / "current/index.md",
            self.workspace / "output/index.md",
        ):
            path.unlink()
        write = ProposedWrite(
            path="current/state.md",
            expected_sha256=sha256_text(
                (self.workspace / "current/state.md").read_text(encoding="utf-8")
            ),
            content="# State\n\nforbidden\n",
        )
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt, summary="형성 중")],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="updated_quiet",
                    writes=(write,),
                )
            ],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "turn-forming-write")

        result = controller.process_session("main-session")

        self.assertEqual(result["status"], "retry")
        self.assertFalse(
            (
                controller.runtime.session_runtime_root("main-session")
                / INTENT_FILENAME
            ).exists()
        )
        self.assertEqual(
            (self.workspace / "current/state.md").read_text(encoding="utf-8"),
            "# State\n\nold\n",
        )

    def test_pending_notice_is_bounded_and_acknowledges_only_included_ids(
        self,
    ) -> None:
        scripts: list[list[object]] = [
            [lambda prompt: decision_for(prompt)]
        ]
        for index in range(10):
            scripts.append(
                [
                    lambda prompt, index=index: decision_for(
                        prompt,
                        outcome="needs_decision",
                        summary=f"판단 {index}",
                        question=f"질문 {index}?",
                    )
                ]
            )
        factory = FakeRunnerFactory(*scripts)
        controller = self.controller(factory)
        self.ground(controller)
        for index in range(10):
            self.pair(controller, f"turn-notice-{index}")

        results = [controller.process_session("main-session") for _ in range(10)]
        notice = controller.take_pending_notice("main-session")

        self.assertTrue(
            all(
                result["outcomes"] == {"needs_decision": 1}
                for result in results
            )
        )
        self.assertEqual(
            len(notice.report_ids), MAX_PENDING_REPORTS_PER_NOTICE
        )
        self.assertLessEqual(
            len(notice.additional_context or ""),
            MAX_PENDING_NOTICE_CHARACTERS,
        )
        self.assertIn("2건은 다음 전달", notice.additional_context or "")
        controller.acknowledge_notice("main-session", notice.report_ids)
        self.assertEqual(
            len(controller.runtime.pending_reports("main-session")), 2
        )

    def test_each_worker_processes_at_most_one_response_event(self) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [lambda prompt: decision_for(prompt, summary="첫 응답")],
            [lambda prompt: decision_for(prompt, summary="둘째 응답")],
        )
        controller = self.controller(factory)
        self.ground(controller)
        self.pair(controller, "bounded-worker-1")
        self.pair(controller, "bounded-worker-2")

        first = controller.process_session("main-session")
        self.assertEqual(first["processed"], 1)
        self.assertTrue(first["work_remaining"])
        self.assertEqual(
            controller.status("main-session")["freshness"][
                "processed_sequence"
            ],
            1,
        )

        second = controller.process_session("main-session")
        self.assertEqual(second["processed"], 1)
        self.assertFalse(second["work_remaining"])
        self.assertEqual(
            controller.status("main-session")["freshness"][
                "processed_sequence"
            ],
            2,
        )

    def test_unresolved_question_survives_delivery_and_cross_session_handoff(
        self,
    ) -> None:
        factory = FakeRunnerFactory(
            [lambda prompt: decision_for(prompt)],
            [
                lambda prompt: decision_for(
                    prompt,
                    outcome="needs_decision",
                    summary="Owner 판단 필요",
                    question="memory와 state 중 어디에 둘까요?",
                )
            ],
            [lambda prompt: decision_for(prompt, summary="새 세션 grounding")],
            [
                lambda prompt: decision_for(
                    prompt,
                    summary="사용자 답을 연결함",
                    resolved_report_ids=(first_unresolved_report_id(prompt),),
                )
            ],
        )
        controller = self.controller(factory)
        controller.session_start(session_start(session_id="old-session"))
        controller.capture_user_prompt(
            user("old-turn", session_id="old-session")
        )
        controller.capture_stop(
            stop("old-turn", session_id="old-session")
        )
        controller.process_session("old-session")

        old_notice = controller.take_pending_notice("old-session")
        self.assertIn("어디에 둘까요", old_notice.additional_context or "")
        controller.acknowledge_notice("old-session", old_notice.report_ids)
        self.assertEqual(controller.runtime.pending_reports("old-session"), [])
        unresolved = controller.runtime.workspace_unresolved_decisions(
            for_session_id="session-new"
        )
        self.assertEqual(len(unresolved), 1)

        start = controller.session_start(
            session_start(session_id="new-session")
        )
        self.assertTrue(start.freshness_ready)
        self.assertIsNotNone(start.notice)
        assert start.notice is not None
        self.assertIn("어디에 둘까요", start.notice.additional_context or "")
        self.assertIn(
            unresolved[0]["report_id"], factory.runners[2].prompts[0]
        )
        controller.acknowledge_workspace_notice(
            "new-session", start.notice.workspace_report_acks
        )
        repeated = controller.take_pending_notice("new-session")
        self.assertNotIn("어디에 둘까요", repeated.additional_context or "")

        controller.capture_user_prompt(
            user(
                "new-turn",
                prompt="state에 두자",
                session_id="new-session",
            )
        )
        controller.capture_stop(
            stop("new-turn", session_id="new-session")
        )
        resolved = controller.process_session("new-session")

        self.assertEqual(resolved["outcomes"], {"no_change": 1})
        self.assertEqual(
            controller.runtime.workspace_unresolved_decisions(
                for_session_id="session-new"
            ),
            [],
        )

    def test_unrenderable_pending_report_triggers_freshness_warning(self) -> None:
        factory = FakeRunnerFactory()
        controller = self.controller(factory)
        malformed = {
            "report_id": "malformed-report",
            "kind": "updated_report",
            "payload": {"summary": 42, "changed_paths": []},
        }
        with mock.patch.object(
            controller.runtime,
            "pending_reports",
            return_value=[malformed],
        ):
            notice = controller.take_pending_notice("main-session")

        self.assertEqual(notice.report_ids, ())
        self.assertIn("신뢰할 수 없습니다", notice.additional_context or "")
        self.assertEqual(
            notice.system_message,
            "Maintain freshness를 자동 복구하지 못했습니다.",
        )

    def test_decision_intent_lock_never_follows_symlink(self) -> None:
        controller = self.controller(FakeRunnerFactory())
        session_root = controller.runtime.session_runtime_root("main-session")
        outside = self.project / "outside-lock"
        outside.write_text("do not lock through this file", encoding="utf-8")
        (session_root / INTENT_LOCK_FILENAME).symlink_to(outside)
        store = DecisionIntentStore(session_root, self.config.workspace_id)

        with self.assertRaisesRegex(DecisionIntentError, "symlink|safely"):
            store.load()

        self.assertEqual(
            outside.read_text(encoding="utf-8"),
            "do not lock through this file",
        )


if __name__ == "__main__":
    unittest.main()
