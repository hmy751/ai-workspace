"""Compose capture, warm semantic judgment, and guarded Workspace writes."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Protocol

from .config import MaintainConfig
from .intent import (
    DecisionIntent,
    DecisionIntentConflictError,
    DecisionIntentStore,
)
from .prompts import initial_grounding_prompt, response_end_prompt
from .runner import (
    CodexTimeoutError,
    CodexWarmSessionRunner,
    MaintainerDecision,
    MaintainerRunnerError,
    MaintainerTurn,
)
from .runtime import (
    MaintainRuntime,
    ProcessingDeferredError,
    RuntimeProtocolError,
)
from .writer import (
    PendingJournalError,
    StaleBaselineError,
    WriteProposal,
    WriteResult,
    acknowledge_transaction,
    apply_writes,
    recover_journal,
    sha256_text,
)


class MaintainControllerError(RuntimeError):
    """A semantic event could not be safely committed."""


class MaintainerIdentityError(MaintainControllerError):
    """The semantic result belongs to another Workspace or event."""


class FreshnessFailedError(MaintainControllerError):
    """The agent explicitly could not restore trustworthy understanding."""


class WriteDecisionMismatchError(MaintainControllerError):
    """The guarded writer result differs from the agent's declared changes."""


class RunnerLike(Protocol):
    @property
    def thread_id(self) -> str | None: ...

    def run(self, prompt: str) -> MaintainerTurn: ...


RunnerFactory = Callable[..., RunnerLike]
WriterApply = Callable[..., WriteResult]
WriterRecover = Callable[[Path, Path], WriteResult]
WriterAcknowledge = Callable[
    [Path, Path, str, tuple[WriteProposal, ...]], bool
]


MAX_PENDING_REPORTS_PER_NOTICE = 8
MAX_PENDING_NOTICE_CHARACTERS = 4000
RECOVERY_ATTEMPTS_BEFORE_WARNING = 3


@dataclass(frozen=True)
class PendingNotice:
    """Small user-facing material safe to inject into the next Main turn."""

    additional_context: str | None
    system_message: str | None
    report_ids: tuple[str, ...]
    workspace_report_acks: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class SessionStartResult:
    """Initial grounding plus any prior-session handoff notice."""

    grounded_now: bool
    summary: str | None
    notice: PendingNotice | None = None
    freshness_ready: bool = True


class MaintainController:
    """Run one session-scoped Maintainer while durable truth stays external."""

    def __init__(
        self,
        config: MaintainConfig,
        *,
        runtime: MaintainRuntime | None = None,
        runner_factory: RunnerFactory = CodexWarmSessionRunner,
        writer_apply: WriterApply = apply_writes,
        writer_recover: WriterRecover = recover_journal,
        writer_acknowledge: WriterAcknowledge = acknowledge_transaction,
    ) -> None:
        self.config = config
        self.runtime = runtime or MaintainRuntime(
            runtime_root=config.runtime_root,
            workspace_id=config.workspace_id,
        )
        self._runner_factory = runner_factory
        self._writer_apply = writer_apply
        self._writer_recover = writer_recover
        self._writer_acknowledge = writer_acknowledge

    def session_start(self, payload: object) -> SessionStartResult:
        """Record a marker and ground only a missing startup/clear agent.

        Resume reuses an existing state. Compact is only a continuity marker:
        even a missing state is not silently reset or bootstrapped by compact.
        """

        value = _payload_object(payload)
        session_id = _payload_string(value, "session_id")
        source = _payload_string(value, "source")
        self.runtime.session_start(payload)
        workspace_freshness = self.runtime.workspace_freshness_summary(
            exclude_session_id=session_id
        )
        freshness_ready = workspace_freshness.get("freshness_ready") is True
        notice = self._pending_notice(session_id, include_current=False)
        unresolved_decisions = self.runtime.workspace_unresolved_decisions(
            for_session_id=session_id
        )
        state = self._load_agent_state(session_id)
        if not freshness_ready and state.get("grounded") is True:
            state = self.runtime.save_agent_state(
                session_id,
                {
                    "thread_id": state.get("thread_id"),
                    "grounded": False,
                    "workspace_bound": bool(state.get("workspace_bound")),
                    "summary": str(state.get("summary", "")),
                },
            )
        if source == "compact":
            return SessionStartResult(False, None, notice, freshness_ready)
        if state.get("grounded") is True and _nonblank(state.get("thread_id")):
            return SessionStartResult(False, None, notice, freshness_ready)
        if source not in {"startup", "resume", "clear"}:
            return SessionStartResult(False, None, notice, freshness_ready)

        event_id = _grounding_event_id(session_id, source)
        workspace_bound = self.config.workspace_bound
        initial_thread_id = (
            str(state["thread_id"]) if _nonblank(state.get("thread_id")) else None
        )
        runner = self._new_runner(initial_thread_id=initial_thread_id)
        turn = self._ground_runner(
            runner,
            event_id=event_id,
            workspace_bound=workspace_bound,
            workspace_freshness_ready=freshness_ready,
            unresolved_decisions=unresolved_decisions,
        )
        summary = _bounded_text(turn.decision.summary, limit=800)
        if not summary:
            raise MaintainControllerError(
                "initial grounding returned no usable start summary"
            )
        self.runtime.save_agent_state(
            session_id,
            {
                "thread_id": turn.thread_id,
                "grounded": freshness_ready,
                "workspace_bound": workspace_bound,
                "summary": summary,
            },
        )
        return SessionStartResult(True, summary, notice, freshness_ready)

    def capture_user_prompt(self, payload: object) -> dict[str, Any]:
        return self.runtime.user_prompt(payload)

    def capture_stop(self, payload: object) -> dict[str, Any]:
        return self.runtime.stop(payload)

    def capture_post_tool_use(self, payload: object) -> dict[str, Any]:
        return self.runtime.post_tool_use(payload)

    def process_session(self, session_id: str) -> dict[str, Any]:
        """Process at most one event so one worker has a bounded semantic tail."""

        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        self._reconcile_committed_intent(session_id)
        workspace_freshness = self.runtime.workspace_freshness_summary(
            exclude_session_id=session_id
        )
        if workspace_freshness.get("freshness_ready") is not True:
            return {
                "status": "waiting_prior",
                "reason": "prior_session_pending",
                "processed": 0,
                "outcomes": {},
                "work_remaining": False,
                "successor_required": False,
                "retry_attempts": 0,
            }
        result = self.runtime.process_next(
            session_id,
            lambda event: self._process_event(session_id, event),
        )
        # The runtime checkpoint is the acknowledgement boundary. Clear an
        # intent only after reading that durable exact event identity.
        self._reconcile_committed_intent(session_id)
        if result.get("status") == "processed":
            outcome = str(result["outcome"])
            work_remaining = bool(result.get("work_remaining"))
            return {
                "status": "processed",
                "reason": None,
                "processed": 1,
                "outcomes": {outcome: 1},
                "work_remaining": work_remaining,
                "successor_required": work_remaining,
            }
        if result.get("status") == "deferred":
            return {
                "status": "waiting_prior",
                "reason": result.get("reason"),
                "processed": 0,
                "outcomes": {},
                "work_remaining": False,
                "successor_required": False,
                "retry_attempts": 0,
            }
        retry_attempts = 0
        if result.get("status") == "retry":
            status = self.runtime.status(session_id)
            failure = status.get("failure", {})
            attempts = (
                failure.get("attempts", 0)
                if isinstance(failure, Mapping)
                else 0
            )
            if isinstance(attempts, int) and not isinstance(attempts, bool):
                retry_attempts = max(0, attempts)
        return {
            "status": result.get("status"),
            "reason": result.get("reason"),
            "processed": 0,
            "outcomes": {},
            "work_remaining": False,
            "successor_required": (
                result.get("status") == "retry"
                and retry_attempts < RECOVERY_ATTEMPTS_BEFORE_WARNING
            ),
            "retry_attempts": retry_attempts,
        }

    def next_runnable_session_id(self) -> str | None:
        """Return one internal recovery target without exposing it in status."""

        return self.runtime.next_runnable_session_id()

    def take_pending_notice(self, session_id: str) -> PendingNotice:
        """Render bounded, raw-free material without acknowledging delivery.

        A detached background hook cannot create a new host UI turn. Therefore
        an already-produced semantic question is injected at the next
        ``UserPromptSubmit`` safe point. This adapter limitation does not change
        the Maintain contract: Main must surface the question immediately when
        it receives this notice, before the relevant write.
        """

        return self._pending_notice(session_id, include_current=True)

    def _pending_notice(
        self, session_id: str, *, include_current: bool
    ) -> PendingNotice:
        lines: list[str] = []
        needs_decision = False
        report_ids: list[str] = []
        workspace_report_acks: list[tuple[str, str]] = []
        malformed_report = False
        deferred_reports = 0
        pending_records: list[tuple[Mapping[str, Any], str | None]] = []
        if include_current:
            pending_records.extend(
                (record, None) for record in self.runtime.pending_reports(session_id)
            )
        pending_records.extend(
            (record, str(record.get("origin_session_key", "")))
            for record in self.runtime.workspace_pending_reports(
                exclude_session_id=session_id
            )
        )
        for record, origin_session_key in pending_records:
            rendered = _render_pending_report(record)
            if rendered is None:
                malformed_report = True
                continue
            report_id = record.get("report_id")
            if not isinstance(report_id, str) or not report_id:
                malformed_report = True
                continue
            line, kind = rendered
            delivered_count = len(report_ids) + len(workspace_report_acks)
            if delivered_count >= MAX_PENDING_REPORTS_PER_NOTICE or not (
                _notice_line_fits(lines, line)
            ):
                deferred_reports += 1
                continue
            lines.append(line)
            needs_decision = needs_decision or kind == "needs_decision"
            if origin_session_key is None:
                report_ids.append(report_id)
            elif len(origin_session_key) == 32:
                workspace_report_acks.append((origin_session_key, report_id))
            else:
                malformed_report = True
                lines.pop()

        if deferred_reports:
            _append_notice_line(
                lines,
                f"Maintain 보고 {deferred_reports}건은 다음 전달에 남아 있습니다.",
            )

        status = self.runtime.status(session_id) if include_current else {}
        freshness = status.get("freshness", {})
        failure = status.get("failure", {})
        retry_pending = bool(
            isinstance(failure, Mapping) and failure.get("retry_pending")
        )
        retry_attempts = (
            failure.get("attempts", 0) if isinstance(failure, Mapping) else 0
        )
        retry_exhausted = (
            retry_pending
            and isinstance(retry_attempts, int)
            and not isinstance(retry_attempts, bool)
            and retry_attempts >= RECOVERY_ATTEMPTS_BEFORE_WARNING
        )
        failure_code = (
            failure.get("code") if isinstance(failure, Mapping) else None
        )
        current_untrustworthy = include_current and not bool(
            isinstance(freshness, Mapping) and freshness.get("trustworthy")
        )
        workspace_freshness = self.runtime.workspace_freshness_summary(
            exclude_session_id=session_id
        )
        prior_warning = workspace_freshness.get("warning_required") is True
        freshness_warning = (
            retry_exhausted
            or (
                current_untrustworthy
                and failure_code != "stale_process_lease"
            )
            or prior_warning
            or malformed_report
        )
        if freshness_warning:
            _append_notice_line(
                lines,
                "Maintain 자동 복구 뒤에도 최신 상태를 신뢰할 수 없습니다. "
                "관련 Context 반영은 완료로 처리되지 않았습니다.",
            )

        additional_context = None
        if lines:
            additional_context = (
                "Maintain에서 다음 항목을 전달했습니다. Main은 이를 짧게 "
                "처리하고, 판단 질문은 관련 쓰기 전에 사용자에게 바로 "
                "물어보세요.\n- "
                + "\n- ".join(lines)
            )
        system_message = None
        if needs_decision:
            system_message = "Maintain에 사용자 판단이 필요한 항목이 있습니다."
        elif freshness_warning:
            system_message = "Maintain freshness를 자동 복구하지 못했습니다."
        return PendingNotice(
            additional_context=additional_context,
            system_message=system_message,
            report_ids=tuple(report_ids),
            workspace_report_acks=tuple(workspace_report_acks),
        )

    def acknowledge_notice(
        self, session_id: str, report_ids: tuple[str, ...]
    ) -> tuple[str, ...]:
        """Acknowledge reports only after the hook JSON was flushed to stdout."""

        acknowledged: list[str] = []
        for report_id in report_ids:
            if self.runtime.acknowledge_report(session_id, report_id):
                acknowledged.append(report_id)
        return tuple(acknowledged)

    def acknowledge_workspace_notice(
        self,
        recipient_session_id: str,
        report_acks: tuple[tuple[str, str], ...],
    ) -> tuple[tuple[str, str], ...]:
        """Acknowledge exact prior-session reports after successful delivery."""

        acknowledged: list[tuple[str, str]] = []
        for origin_session_key, report_id in report_acks:
            if self.runtime.acknowledge_workspace_report(
                origin_session_key, report_id, recipient_session_id
            ):
                acknowledged.append((origin_session_key, report_id))
        return tuple(acknowledged)

    def repair_missing_stop_gap(
        self,
        session_id: str,
        expected_sequence: int,
        *,
        approved_by: str,
        reason: str,
    ) -> dict[str, Any]:
        return self.runtime.repair_missing_stop_gap(
            session_id,
            expected_sequence,
            approved_by=approved_by,
            reason=reason,
        )

    def status(self, session_id: str | None = None) -> dict[str, Any]:
        return self.runtime.status(session_id)

    def _process_event(
        self, session_id: str, event: Mapping[str, Any]
    ) -> str | dict[str, Any]:
        runtime_session_root = self.runtime.session_runtime_root(session_id)
        intent_store = DecisionIntentStore(
            runtime_session_root, self.config.workspace_id
        )
        pending_intent = intent_store.load()
        if pending_intent is not None:
            if (
                pending_intent.event_id != event.get("event_id")
                or pending_intent.content_sha256
                != event.get("content_sha256")
            ):
                raise DecisionIntentConflictError(
                    "pending semantic intent belongs to another uncommitted event"
                )
            try:
                return self._replay_intent(session_id, pending_intent)
            except StaleBaselineError:
                intent_store.clear_if(
                    event_id=pending_intent.event_id,
                    content_sha256=pending_intent.content_sha256,
                )
                self._invalidate_grounding(session_id)
                raise

        state = self._load_agent_state(session_id)
        workspace_freshness = self.runtime.workspace_freshness_summary(
            exclude_session_id=session_id
        )
        if workspace_freshness.get("freshness_ready") is not True:
            if state.get("grounded") is True:
                self.runtime.save_agent_state(
                    session_id,
                    {
                        "thread_id": state.get("thread_id"),
                        "grounded": False,
                        "workspace_bound": bool(state.get("workspace_bound")),
                        "summary": str(state.get("summary", "")),
                    },
                )
            raise ProcessingDeferredError(
                "a prior Main session has not restored Workspace freshness"
            )
        workspace_bound = self.config.workspace_bound
        unresolved_decisions = self.runtime.workspace_unresolved_decisions(
            for_session_id=session_id
        )
        unresolved_ids = frozenset(
            str(item.get("report_id"))
            for item in unresolved_decisions
            if isinstance(item, Mapping)
            and isinstance(item.get("report_id"), str)
        )
        initial_thread_id = (
            str(state["thread_id"])
            if _nonblank(state.get("thread_id"))
            else None
        )
        runner = self._new_runner(initial_thread_id=initial_thread_id)
        try:
            runner, state = self._prepare_runner_for_event(
                session_id=session_id,
                runner=runner,
                state=state,
                event_id=str(event["event_id"]),
                workspace_bound=workspace_bound,
                workspace_freshness_ready=True,
                unresolved_decisions=unresolved_decisions,
            )
            turn = runner.run(
                self._response_prompt(
                    event,
                    workspace_bound=workspace_bound,
                    unresolved_decisions=unresolved_decisions,
                )
            )
        except CodexTimeoutError:
            # A timeout may leave the child tail running until the process API
            # completes its cleanup.  Starting an immediate replacement would
            # duplicate that expensive tail.  Keep the event unacknowledged so
            # the next hook can make one bounded retry.
            raise
        except MaintainerRunnerError:
            if initial_thread_id is None:
                # A fresh or malformed-state recovery already attempted its one
                # canonical bootstrap.  Do not spin up a second thread in the
                # same processor attempt.
                raise
            # One failed warm resume is recoverable: create exactly one
            # replacement thread, ground it from canonical, then rejudge the
            # same still-unacknowledged event.
            runner = self._new_runner(initial_thread_id=None)
            grounding = self._ground_runner(
                runner,
                event_id=f"rebootstrap:{event['event_id']}",
                workspace_bound=workspace_bound,
                workspace_freshness_ready=True,
                unresolved_decisions=unresolved_decisions,
            )
            state = self._save_grounding_state(
                session_id,
                grounding,
                workspace_bound=workspace_bound,
            )
            turn = runner.run(
                self._response_prompt(
                    event,
                    workspace_bound=workspace_bound,
                    unresolved_decisions=unresolved_decisions,
                )
            )

        decision = turn.decision
        self._validate_event_decision(
            decision,
            event,
            unresolved_report_ids=unresolved_ids,
        )
        self._validate_workspace_binding(decision, workspace_bound)
        if decision.outcome == "freshness_failed":
            raise FreshnessFailedError(
                "Maintainer reported that trustworthy freshness was not restored"
            )

        proposals = tuple(
            WriteProposal(
                path=proposal.path,
                expected_sha256=proposal.expected_sha256,
                content=proposal.content,
            )
            for proposal in decision.writes
        )
        self._validate_effective_writes(proposals, decision.changed_paths)

        previous_summary = state.get("summary")
        summary = _bounded_text(decision.summary, limit=800)
        if not summary and isinstance(previous_summary, str):
            summary = _bounded_text(previous_summary, limit=800)
        processor_result = self._processor_result(
            decision,
            summary=summary,
        )
        next_agent_state = {
            "thread_id": turn.thread_id,
            "grounded": True,
            "workspace_bound": workspace_bound,
            "summary": summary,
        }
        intent = DecisionIntent.create(
            workspace_id=self.config.workspace_id,
            event_id=str(event["event_id"]),
            content_sha256=str(event["content_sha256"]),
            thread_id=turn.thread_id,
            decision=decision,
            processor_result=processor_result,
            agent_state=next_agent_state,
        )
        # Publish before the first guarded target mutation.  A crash from this
        # point through runtime checkpoint commit reuses this exact decision.
        intent_store.persist(intent)
        try:
            self._apply_intent_writes(intent)
        except StaleBaselineError:
            # The writer rejects stale baselines before staging or mutation.
            # Discard only this semantic proposal and force the same warm
            # thread to re-ground from the latest canonical on retry.
            intent_store.clear_if(
                event_id=intent.event_id,
                content_sha256=intent.content_sha256,
            )
            self._invalidate_grounding(session_id)
            raise
        self.runtime.save_agent_state(session_id, next_agent_state)
        return _copy_processor_result(intent.processor_result)

    def _replay_intent(
        self, session_id: str, intent: DecisionIntent
    ) -> str | dict[str, Any]:
        """Finish one exact pre-checkpoint decision without another agent turn."""

        workspace_bound = self.config.workspace_bound
        recorded_bound = bool(intent.agent_state["workspace_bound"])
        if (
            recorded_bound is not workspace_bound
            and bool(intent.decision.writes)
        ):
            raise DecisionIntentConflictError(
                "Workspace binding changed while a decision awaited checkpoint"
            )
        # A no-write decision remains safe to acknowledge against the binding
        # snapshot it judged.  Persist that old bit; the next event observes a
        # false->true (or true->false) transition and performs one read-only
        # re-ground.  This prevents a concurrent Workspace creation from
        # wedging the preceding forming event forever.
        self._validate_workspace_binding(intent.decision, recorded_bound)
        self._apply_intent_writes(intent)
        self.runtime.save_agent_state(session_id, intent.agent_state)
        return _copy_processor_result(intent.processor_result)

    def _apply_intent_writes(self, intent: DecisionIntent) -> WriteResult:
        proposals = tuple(
            WriteProposal(
                path=proposal.path,
                expected_sha256=proposal.expected_sha256,
                content=proposal.content,
            )
            for proposal in intent.decision.writes
        )
        if not proposals:
            return WriteResult(changed_paths=())
        if not self.config.workspace_bound:
            raise MaintainControllerError(
                "Maintain cannot write while the selected Workspace is unbound"
            )

        writer_runtime_root = self._writer_runtime_root()
        try:
            # An exact completed marker is checked before the shared journal.
            # This lets an older checkpoint replay finish even when another
            # session has a separate damaged transaction awaiting repair.
            write_result = self._writer_apply(
                self.config.workspace_root,
                writer_runtime_root,
                proposals,
                transaction_key=intent.key,
            )
        except PendingJournalError:
            self._writer_recover(self.config.workspace_root, writer_runtime_root)
            write_result = self._writer_apply(
                self.config.workspace_root,
                writer_runtime_root,
                proposals,
                transaction_key=intent.key,
            )

        if tuple(write_result.changed_paths) != intent.decision.changed_paths:
            raise WriteDecisionMismatchError(
                "actual guarded writes do not match the Maintainer decision"
            )
        return write_result

    def _processor_result(
        self, decision: MaintainerDecision, *, summary: str
    ) -> str | dict[str, Any]:
        if decision.outcome in {"no_change", "updated_quiet"}:
            return decision.outcome
        report: dict[str, Any] = {
            "summary": summary,
            "changed_paths": list(decision.changed_paths),
        }
        if decision.outcome == "needs_decision":
            report["question"] = _bounded_text(decision.question or "", limit=500)
        return {"outcome": decision.outcome, "report": report}

    def _new_runner(self, *, initial_thread_id: str | None) -> RunnerLike:
        return self._runner_factory(
            project_root=self.config.project_root,
            sandbox=self.config.sandbox,
            codex_executable=self.config.codex_executable,
            initial_thread_id=initial_thread_id,
        )

    def _prepare_runner_for_event(
        self,
        *,
        session_id: str,
        runner: RunnerLike,
        state: Mapping[str, Any],
        event_id: str,
        workspace_bound: bool,
        workspace_freshness_ready: bool,
        unresolved_decisions: object,
    ) -> tuple[RunnerLike, dict[str, Any]]:
        grounded = state.get("grounded") is True and _nonblank(
            state.get("thread_id")
        )
        previous_bound = state.get("workspace_bound")
        if grounded and previous_bound is workspace_bound:
            return runner, dict(state)

        reason = "event-grounding" if not grounded else "workspace-binding"
        turn = self._ground_runner(
            runner,
            event_id=f"{reason}:{event_id}",
            workspace_bound=workspace_bound,
            workspace_freshness_ready=workspace_freshness_ready,
            unresolved_decisions=unresolved_decisions,
        )
        saved = self._save_grounding_state(
            session_id,
            turn,
            workspace_bound=workspace_bound,
        )
        return runner, saved

    def _ground_runner(
        self,
        runner: RunnerLike,
        *,
        event_id: str,
        workspace_bound: bool,
        workspace_freshness_ready: bool = True,
        unresolved_decisions: object = (),
    ) -> MaintainerTurn:
        turn = runner.run(
            self._initial_prompt(
                event_id,
                workspace_bound=workspace_bound,
                workspace_freshness_ready=workspace_freshness_ready,
                unresolved_decisions=unresolved_decisions,
            )
        )
        self._validate_grounding_turn(turn, event_id)
        if not _bounded_text(turn.decision.summary, limit=800):
            raise MaintainControllerError(
                "initial grounding returned no usable start summary"
            )
        return turn

    def _save_grounding_state(
        self,
        session_id: str,
        turn: MaintainerTurn,
        *,
        workspace_bound: bool,
    ) -> dict[str, Any]:
        state = {
            "thread_id": turn.thread_id,
            "grounded": True,
            "workspace_bound": workspace_bound,
            "summary": _bounded_text(turn.decision.summary, limit=800),
        }
        self.runtime.save_agent_state(session_id, state)
        return state

    def _initial_prompt(
        self,
        event_id: str,
        *,
        workspace_bound: bool,
        workspace_freshness_ready: bool = True,
        unresolved_decisions: object = (),
    ) -> str:
        return initial_grounding_prompt(
            workspace_id=self.config.workspace_id,
            workspace_path=self.config.workspace_relative_path,
            maintain_contract_path=self.config.maintain_contract_relative_path,
            event_id=event_id,
            workspace_bound=workspace_bound,
            workspace_freshness_ready=workspace_freshness_ready,
            unresolved_decisions=unresolved_decisions,
        )

    def _response_prompt(
        self,
        event: Mapping[str, Any],
        *,
        workspace_bound: bool,
        unresolved_decisions: object = (),
    ) -> str:
        assistant = event.get("assistant")
        return response_end_prompt(
            workspace_id=self.config.workspace_id,
            workspace_path=self.config.workspace_relative_path,
            maintain_contract_path=self.config.maintain_contract_relative_path,
            event_id=str(event["event_id"]),
            user_prompt=str(event["prompt"]),
            assistant_message=assistant if isinstance(assistant, str) else "",
            tool_evidence=event.get("tool_evidence", []),
            workspace_bound=workspace_bound,
            unresolved_decisions=unresolved_decisions,
        )

    def _validate_grounding_turn(
        self, turn: MaintainerTurn, event_id: str
    ) -> None:
        decision = turn.decision
        if (
            decision.workspace_id != self.config.workspace_id
            or decision.event_id != event_id
        ):
            raise MaintainerIdentityError(
                "initial grounding returned another Workspace or event identity"
            )
        if (
            decision.outcome != "no_change"
            or decision.changed_paths
            or decision.writes
            or decision.question is not None
            or decision.resolved_report_ids
        ):
            raise MaintainControllerError(
                "initial grounding must be a read-only no_change decision"
            )

    def _validate_event_decision(
        self,
        decision: MaintainerDecision,
        event: Mapping[str, Any],
        *,
        unresolved_report_ids: frozenset[str],
    ) -> None:
        # Runner production output has already passed this parser.  Rechecking
        # at the controller boundary keeps alternate/test RunnerLike adapters
        # from persisting a merely type-shaped but semantically invalid result.
        validated = MaintainerDecision.from_object(decision.to_dict())
        if validated != decision:
            raise MaintainControllerError(
                "Maintainer decision changed during canonical validation"
            )
        if decision.workspace_id != self.config.workspace_id:
            raise MaintainerIdentityError(
                "Maintainer decision returned another Workspace identity"
            )
        if decision.event_id != event.get("event_id"):
            raise MaintainerIdentityError(
                "Maintainer decision returned another event identity"
            )
        if not set(decision.resolved_report_ids).issubset(
            unresolved_report_ids
        ):
            raise MaintainControllerError(
                "Maintainer resolved an unknown or already-resolved question"
            )

    def _validate_workspace_binding(
        self, decision: MaintainerDecision, workspace_bound: bool
    ) -> None:
        if workspace_bound:
            return
        if decision.outcome.startswith("updated_") or decision.writes:
            raise MaintainControllerError(
                "an unbound Workspace cannot accept Maintain writes"
            )

    def _validate_effective_writes(
        self,
        proposals: tuple[WriteProposal, ...],
        changed_paths: tuple[str, ...],
    ) -> None:
        proposal_paths = tuple(proposal.path for proposal in proposals)
        if proposal_paths != changed_paths:
            raise WriteDecisionMismatchError(
                "changed_paths order must match guarded write order"
            )
        no_op_paths = tuple(
            proposal.path
            for proposal in proposals
            if proposal.expected_sha256 == sha256_text(proposal.content)
        )
        if no_op_paths:
            raise WriteDecisionMismatchError(
                "Maintainer declared unchanged content as changed: "
                + ", ".join(no_op_paths)
            )

    def _load_agent_state(self, session_id: str) -> dict[str, Any]:
        try:
            return self.runtime.load_agent_state(session_id)
        except RuntimeProtocolError:
            # A malformed warm-session pointer must not become a permanent
            # processor retry lock.  Runtime quarantines the bytes under a
            # content-free name and returns a safe ungrounded v2 state; this
            # attempt then performs exactly one canonical bootstrap.
            return self.runtime.quarantine_agent_state(
                session_id, reason_code="malformed"
            )

    def _invalidate_grounding(self, session_id: str) -> dict[str, Any]:
        state = self._load_agent_state(session_id)
        return self.runtime.save_agent_state(
            session_id,
            {
                "thread_id": state.get("thread_id"),
                "grounded": False,
                "workspace_bound": bool(state.get("workspace_bound")),
                "summary": str(state.get("summary", "")),
            },
        )

    def _reconcile_committed_intent(self, session_id: str) -> bool:
        committed = self.runtime.last_committed_event(session_id)
        if committed is None:
            return False
        store = DecisionIntentStore(
            self.runtime.session_runtime_root(session_id),
            self.config.workspace_id,
        )
        intent = store.load()
        if intent is None or (
            intent.event_id != str(committed["event_id"])
            or intent.content_sha256 != str(committed["content_sha256"])
        ):
            return False
        proposals = tuple(
            WriteProposal(
                path=proposal.path,
                expected_sha256=proposal.expected_sha256,
                content=proposal.content,
            )
            for proposal in intent.decision.writes
        )
        if intent.decision.resolved_report_ids:
            self.runtime.resolve_workspace_reports(
                intent.decision.resolved_report_ids
            )
        if proposals:
            self._writer_acknowledge(
                self.config.workspace_root,
                self._writer_runtime_root(),
                intent.key,
                proposals,
            )
        return store.clear_if(
            event_id=intent.event_id,
            content_sha256=intent.content_sha256,
        )

    def _writer_runtime_root(self) -> Path:
        """One writer namespace shared by every Main session of a Workspace."""

        workspace_runtime_root = getattr(
            self.runtime, "workspace_runtime_root", None
        )
        if callable(workspace_runtime_root):
            return Path(workspace_runtime_root()) / "writer"
        # Backward-compatible test doubles can expose the already namespaced
        # root directly.  Production MaintainRuntime provides the method above.
        return Path(self.runtime.root) / "writer"


def _payload_object(payload: object) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValueError("hook payload must be an object")
    return payload


def _payload_string(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _grounding_event_id(session_id: str, source: str) -> str:
    digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:24]
    return f"grounding:{source}:{digest}"


def _bounded_text(value: str, *, limit: int) -> str:
    collapsed = " ".join(value.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1].rstrip() + "…"


def _copy_processor_result(value: str | dict[str, Any]) -> str | dict[str, Any]:
    if isinstance(value, str):
        return value
    return json.loads(json.dumps(value, ensure_ascii=False))


def _notice_line_fits(lines: list[str], candidate: str) -> bool:
    header_length = len(
        "Maintain에서 다음 항목을 전달했습니다. Main은 이를 짧게 "
        "처리하고, 판단 질문은 관련 쓰기 전에 사용자에게 바로 "
        "물어보세요.\n- "
    )
    body_length = len("\n- ".join((*lines, candidate)))
    return header_length + body_length <= MAX_PENDING_NOTICE_CHARACTERS


def _append_notice_line(lines: list[str], candidate: str) -> bool:
    if not _notice_line_fits(lines, candidate):
        return False
    lines.append(candidate)
    return True


def _render_pending_report(
    record: Mapping[str, Any],
) -> tuple[str, str] | None:
    kind = record.get("kind")
    payload = record.get("payload")
    if kind not in {"updated_report", "needs_decision"} or not isinstance(
        payload, Mapping
    ):
        return None
    if kind == "updated_report":
        summary = payload.get("summary")
        paths = payload.get("changed_paths")
        if not isinstance(summary, str) or not isinstance(paths, list) or any(
            not isinstance(path, str) for path in paths
        ):
            return None
        suffix = f" (변경: {', '.join(paths)})" if paths else ""
        line = "Maintain 반영 완료: " + _bounded_text(summary, limit=500) + suffix
        return _bounded_text(line, limit=900), kind

    question = payload.get("question")
    if not isinstance(question, str) or not question.strip():
        return None
    return "Maintain 판단 질문: " + _bounded_text(question, limit=500), kind


__all__ = [
    "FreshnessFailedError",
    "MaintainController",
    "MaintainControllerError",
    "MaintainerIdentityError",
    "PendingNotice",
    "SessionStartResult",
    "WriteDecisionMismatchError",
]
