from __future__ import annotations

from collections.abc import Sequence
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from context.work.harness.maintain.runner import (
    CHILD_ENVIRONMENT_VARIABLE,
    DECISION_OUTCOMES,
    DEFAULT_DECISION_SCHEMA,
    CodexProcessError,
    CodexProtocolError,
    CodexTimeoutError,
    CodexTurnError,
    CodexWarmSessionRunner,
)


def decision(
    *,
    event_id: str,
    outcome: str = "no_change",
) -> dict[str, object]:
    writes: list[dict[str, object]] = []
    changed_paths: list[str] = []
    if outcome.startswith("updated_"):
        changed_paths = ["current/state/index.md"]
        writes = [
            {
                "path": "current/state/index.md",
                "expected_sha256": "0" * 64,
                "content": "# updated state\n",
            }
        ]
    return {
        "outcome": outcome,
        "workspace_id": "005-context-continuity-maintenance",
        "event_id": event_id,
        "summary": "지속 반영할 변화가 없다.",
        "changed_paths": changed_paths,
        "writes": writes,
        "question": None,
        "evidence_paths": [],
        "resolved_report_ids": [],
    }


def jsonl(
    *,
    thread_id: str,
    result: dict[str, object],
    terminal: dict[str, object] | None = None,
) -> str:
    events = [
        {"type": "thread.started", "thread_id": thread_id},
        {"type": "turn.started"},
        {
            "type": "item.completed",
            "item": {
                "id": "item-1",
                "type": "agent_message",
                "text": json.dumps(result, ensure_ascii=False),
            },
        },
        terminal or {"type": "turn.completed", "usage": {}},
    ]
    return "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n"


class FakeProcessRunner:
    def __init__(
        self, responses: Sequence[subprocess.CompletedProcess[str]]
    ) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[list[str], dict[str, object]]] = []

    def __call__(
        self, arguments: list[str], **kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        self.calls.append((list(arguments), dict(kwargs)))
        if not self.responses:
            raise AssertionError("Unexpected subprocess call")
        return self.responses.pop(0)


def completed(
    stdout: str,
    *,
    returncode: int = 0,
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["codex"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


class CodexWarmSessionRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name) / "project"
        self.project_root.mkdir()
        self.schema = Path(self.temporary_directory.name) / "decision.schema.json"
        self.schema.write_text("{}\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def make_runner(
        self, fake: FakeProcessRunner
    ) -> CodexWarmSessionRunner:
        return CodexWarmSessionRunner(
            project_root=self.project_root,
            sandbox="read-only",
            decision_schema=self.schema,
            process_runner=fake,
        )

    def test_bootstrap_then_resumes_the_same_thread(self) -> None:
        fake = FakeProcessRunner(
            [
                completed(jsonl(thread_id="thread-1", result=decision(event_id="1"))),
                completed(
                    jsonl(
                        thread_id="thread-1",
                        result=decision(
                            event_id="2", outcome="updated_quiet"
                        ),
                    )
                ),
            ]
        )
        runner = self.make_runner(fake)

        first = runner.run("bootstrap prompt")
        second = runner.run("delta prompt")

        self.assertEqual(first.thread_id, "thread-1")
        self.assertEqual(first.decision.event_id, "1")
        self.assertEqual(second.thread_id, "thread-1")
        self.assertEqual(second.decision.outcome, "updated_quiet")
        self.assertEqual(runner.thread_id, "thread-1")
        self.assertEqual(
            fake.calls[0][0],
            [
                "codex",
                "exec",
                "-C",
                str(runner.project_root),
                "-s",
                "read-only",
                "--json",
                "--output-schema",
                str(runner.decision_schema),
                "-",
            ],
        )
        self.assertEqual(
            fake.calls[1][0],
            [
                "codex",
                "exec",
                "resume",
                "thread-1",
                "--json",
                "--output-schema",
                str(runner.decision_schema),
                "-",
            ],
        )
        for _, keyword_arguments in fake.calls:
            environment = keyword_arguments["env"]
            self.assertIsInstance(environment, dict)
            self.assertEqual(
                environment[CHILD_ENVIRONMENT_VARIABLE],  # type: ignore[index]
                "1",
            )
            self.assertEqual(keyword_arguments["cwd"], runner.project_root)
            self.assertEqual(keyword_arguments["check"], False)
            self.assertEqual(keyword_arguments["timeout"], 90.0)
        self.assertEqual(fake.calls[0][1]["input"], "bootstrap prompt")
        self.assertEqual(fake.calls[1][1]["input"], "delta prompt")

    def test_failed_resume_preserves_thread_for_caller_replay(self) -> None:
        replay_prompt = "event-2 prompt"
        fake = FakeProcessRunner(
            [
                completed(jsonl(thread_id="thread-1", result=decision(event_id="1"))),
                completed("", returncode=7, stderr="temporary failure"),
                completed(jsonl(thread_id="thread-1", result=decision(event_id="2"))),
            ]
        )
        runner = self.make_runner(fake)
        runner.run("event-1 prompt")

        with self.assertRaisesRegex(CodexProcessError, "status 7"):
            runner.run(replay_prompt)

        self.assertEqual(runner.thread_id, "thread-1")
        replayed = runner.run(replay_prompt)
        self.assertEqual(replayed.decision.event_id, "2")
        self.assertEqual(fake.calls[1][0], fake.calls[2][0])

    def test_uses_last_completed_agent_message(self) -> None:
        earlier = {
            "type": "item.completed",
            "item": {"type": "agent_message", "text": "not final JSON"},
        }
        final = {
            "type": "item.completed",
            "item": {
                "type": "agent_message",
                "text": json.dumps(decision(event_id="last")),
            },
        }
        stream = "\n".join(
            json.dumps(event)
            for event in (
                {"type": "thread.started", "thread_id": "thread-1"},
                earlier,
                final,
                {"type": "turn.completed"},
            )
        )
        fake = FakeProcessRunner([completed(stream)])

        turn = self.make_runner(fake).run("prompt")

        self.assertEqual(turn.decision.event_id, "last")

    def test_rejects_malformed_stream_without_committing_thread(self) -> None:
        cases = {
            "malformed JSONL": "{not-json\n",
            "missing thread": "\n".join(
                [
                    json.dumps(
                        {
                            "type": "item.completed",
                            "item": {
                                "type": "agent_message",
                                "text": json.dumps(decision(event_id="1")),
                            },
                        }
                    ),
                    json.dumps({"type": "turn.completed"}),
                ]
            ),
            "missing completion": "\n".join(
                [
                    json.dumps(
                        {"type": "thread.started", "thread_id": "thread-1"}
                    ),
                    json.dumps(
                        {
                            "type": "item.completed",
                            "item": {
                                "type": "agent_message",
                                "text": json.dumps(decision(event_id="1")),
                            },
                        }
                    ),
                ]
            ),
            "invalid final decision": jsonl(
                thread_id="thread-1",
                result={"outcome": "no_change"},
            ),
        }

        for name, stream in cases.items():
            with self.subTest(name=name):
                runner = self.make_runner(FakeProcessRunner([completed(stream)]))
                with self.assertRaises(CodexProtocolError):
                    runner.run("prompt")
                self.assertIsNone(runner.thread_id)

    def test_rejects_turn_failed_and_error_events(self) -> None:
        cases = [
            (
                jsonl(
                    thread_id="thread-1",
                    result=decision(event_id="1"),
                    terminal={
                        "type": "turn.failed",
                        "error": {"message": "model failed"},
                    },
                ),
                "model failed",
            ),
            "\n".join(
                [
                    json.dumps(
                        {"type": "thread.started", "thread_id": "thread-1"}
                    ),
                    json.dumps({"type": "error", "message": "stream failed"}),
                ]
            ),
        ]

        for case in cases:
            if isinstance(case, tuple):
                stream, expected = case
            else:
                stream, expected = case, "stream failed"
            with self.subTest(expected=expected):
                runner = self.make_runner(FakeProcessRunner([completed(stream)]))
                with self.assertRaisesRegex(CodexTurnError, expected):
                    runner.run("prompt")
                self.assertIsNone(runner.thread_id)

    def test_rejects_thread_change_on_resume(self) -> None:
        fake = FakeProcessRunner(
            [
                completed(jsonl(thread_id="thread-1", result=decision(event_id="1"))),
                completed(jsonl(thread_id="thread-2", result=decision(event_id="2"))),
            ]
        )
        runner = self.make_runner(fake)
        runner.run("first")

        with self.assertRaisesRegex(CodexProtocolError, "different thread id"):
            runner.run("second")

        self.assertEqual(runner.thread_id, "thread-1")

    def test_timeout_is_retryable_and_prompt_is_not_in_argv(self) -> None:
        calls: list[tuple[list[str], dict[str, object]]] = []

        def timeout_runner(
            arguments: list[str], **kwargs: object
        ) -> subprocess.CompletedProcess[str]:
            calls.append((list(arguments), dict(kwargs)))
            raise subprocess.TimeoutExpired(arguments, kwargs["timeout"])

        runner = CodexWarmSessionRunner(
            project_root=self.project_root,
            sandbox="read-only",
            decision_schema=self.schema,
            process_runner=timeout_runner,
            process_timeout_seconds=12.5,
        )
        prompt = "private " + ("delta " * 10_000)

        with self.assertRaisesRegex(CodexTimeoutError, "12.5 seconds"):
            runner.run(prompt)

        self.assertNotIn(prompt, calls[0][0])
        self.assertEqual(calls[0][0][-1], "-")
        self.assertEqual(calls[0][1]["input"], prompt)
        self.assertEqual(calls[0][1]["timeout"], 12.5)
        self.assertIsNone(runner.thread_id)

    def test_rejects_question_outside_needs_decision(self) -> None:
        invalid = decision(event_id="1")
        invalid["question"] = "이 질문은 버려지면 안 된다."
        runner = self.make_runner(
            FakeProcessRunner(
                [completed(jsonl(thread_id="thread-1", result=invalid))]
            )
        )

        with self.assertRaisesRegex(
            CodexProtocolError, "Only a needs_decision"
        ):
            runner.run("prompt")

    def test_needs_decision_requires_self_contained_nonblank_summary(self) -> None:
        result = decision(event_id="event-1", outcome="needs_decision")
        result["summary"] = ""
        result["question"] = "state Owner에 둘까요?"
        fake = FakeProcessRunner(
            [completed(jsonl(thread_id="thread-1", result=result))]
        )
        runner = self.make_runner(fake)

        with self.assertRaisesRegex(CodexProtocolError, "handoff summary"):
            runner.run("prompt")

        self.assertIsNone(runner.thread_id)

    def test_decision_schema_matches_the_parser_contract(self) -> None:
        schema = json.loads(DEFAULT_DECISION_SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(schema["type"], "object")
        self.assertEqual(schema["additionalProperties"], False)
        self.assertEqual(
            set(schema["required"]),
            {
                "outcome",
                "workspace_id",
                "event_id",
                "summary",
                "changed_paths",
                "writes",
                "question",
                "evidence_paths",
                "resolved_report_ids",
            },
        )
        self.assertEqual(
            set(schema["properties"]["outcome"]["enum"]),
            DECISION_OUTCOMES,
        )


if __name__ == "__main__":
    unittest.main()
