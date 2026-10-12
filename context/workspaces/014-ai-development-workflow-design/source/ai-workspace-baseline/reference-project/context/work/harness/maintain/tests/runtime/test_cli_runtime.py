"""control CLI, runtime 경로 안전성과 worker lock을 검증한다."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import threading
from unittest.mock import patch

from context.work.harness.maintain.host_adapter import (
    MaintainHostAdapter,
    main as host_adapter_main,
)
from context.work.harness.workspace_contract import HarnessError

from ..support.host import MaintainHostAdapterFixture


class MaintainHostCliRuntimeTests(MaintainHostAdapterFixture):
    def test_status_cli_uses_env_or_explicit_session_without_writing(self) -> None:
        env_session = "host-session-from-env"
        explicit_session = "host-session-explicit"
        stdout = io.StringIO()
        before_paths = set(self.project_root.rglob("*"))

        with patch.dict(os.environ, {"CODEX_SESSION_ID": env_session}, clear=False):
            with redirect_stdout(stdout):
                exit_code = host_adapter_main(
                    [
                        "status",
                        "--project-root",
                        str(self.project_root),
                        "--runtime-root",
                        str(self.runtime_root),
                    ]
                )
        env_status = json.loads(stdout.getvalue())
        after_env_paths = set(self.project_root.rglob("*"))

        stdout = io.StringIO()
        with patch.dict(os.environ, {"CODEX_SESSION_ID": env_session}, clear=False):
            with redirect_stdout(stdout):
                explicit_exit_code = host_adapter_main(
                    [
                        "status",
                        "--project-root",
                        str(self.project_root),
                        "--runtime-root",
                        str(self.runtime_root),
                        "--session-id",
                        explicit_session,
                    ]
                )
        explicit_status = json.loads(stdout.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(explicit_exit_code, 0)
        self.assertEqual(env_status["session_id"], env_session)
        self.assertEqual(explicit_status["session_id"], explicit_session)
        self.assertEqual(env_status["runtime"]["unresolved_event_count"], 0)
        self.assertEqual(after_env_paths, before_paths)
        self.assertFalse(self.runtime_root.exists())

    def test_control_cli_missing_session_is_a_nonzero_failure(self) -> None:
        stderr = io.StringIO()
        with patch.dict(os.environ, {}, clear=True):
            with redirect_stderr(stderr):
                exit_code = host_adapter_main(
                    [
                        "status",
                        "--project-root",
                        str(self.project_root),
                        "--runtime-root",
                        str(self.runtime_root),
                    ]
                )

        self.assertEqual(exit_code, 2)
        self.assertIn("requires --session-id or CODEX_SESSION_ID", stderr.getvalue())

    def test_empty_explicit_session_never_falls_back_to_ambient_session(self) -> None:
        stderr = io.StringIO()
        with patch.dict(
            os.environ,
            {"CODEX_SESSION_ID": "ambient-main-session"},
            clear=True,
        ):
            with patch.object(MaintainHostAdapter, "activate") as activate:
                with redirect_stderr(stderr):
                    exit_code = host_adapter_main(
                        [
                            "activate",
                            "001-example",
                            "--project-root",
                            str(self.project_root),
                            "--runtime-root",
                            str(self.runtime_root),
                            "--session-id",
                            "",
                        ]
                    )

        self.assertEqual(exit_code, 2)
        self.assertIn("Codex session id must be a non-empty string", stderr.getvalue())
        activate.assert_not_called()

    def test_activate_cli_accepts_positional_workspace_and_project_root(self) -> None:
        stdout = io.StringIO()
        result = {
            "schema_version": 2,
            "status": "activated",
            "session_id": "host-session-cli",
            "binding_generation": 1,
            "workspace_id": "001-example",
            "thread_id": "thread-cli",
        }
        with patch.object(
            MaintainHostAdapter, "activate", return_value=result
        ) as activate:
            with redirect_stdout(stdout):
                exit_code = host_adapter_main(
                    [
                        "activate",
                        "001-example",
                        "--project-root",
                        str(self.project_root),
                        "--runtime-root",
                        str(self.runtime_root),
                        "--session-id",
                        "host-session-cli",
                    ]
                )

        self.assertEqual(exit_code, 0)
        activate.assert_called_once_with("host-session-cli", "001-example")
        self.assertEqual(json.loads(stdout.getvalue()), result)

    def test_runtime_root_must_be_an_internal_absolute_lexical_path(self) -> None:
        outside = self.project_root.parent / "outside-maintain-runtime"
        traversal = self.project_root / ".codex" / ".." / "escaped-runtime"
        cases = [
            (Path("relative-runtime"), "absolute path"),
            (outside, "inside the Project root"),
            (traversal, "ancestor traversal"),
        ]

        for runtime_root, expected in cases:
            with self.subTest(runtime_root=runtime_root):
                with self.assertRaisesRegex(HarnessError, expected):
                    MaintainHostAdapter(
                        self.project_root,
                        runtime_root=runtime_root,
                        session_type=self.semantic_session_type,
                        popen=self.popen,
                        clock=self.clock,
                    )

    def test_preexisting_runtime_root_symlink_is_rejected(self) -> None:
        target = self.project_root / ".codex" / "linked-runtime-target"
        target.mkdir()
        linked_runtime = self.project_root / ".codex" / "linked-runtime"
        linked_runtime.symlink_to(target, target_is_directory=True)

        with self.assertRaisesRegex(HarnessError, "symlink components"):
            MaintainHostAdapter(
                self.project_root,
                runtime_root=linked_runtime,
                session_type=self.semantic_session_type,
                popen=self.popen,
                clock=self.clock,
            )

    def test_preexisting_session_directory_symlink_is_rejected(self) -> None:
        runtime_root = self.project_root / ".codex" / "session-link-runtime"
        runtime_root.mkdir()
        target = self.project_root / ".codex" / "linked-session-target"
        target.mkdir()
        session_id = "host-session-linked-directory"
        (runtime_root / self.session_key(session_id)).symlink_to(
            target, target_is_directory=True
        )
        adapter = MaintainHostAdapter(
            self.project_root,
            runtime_root=runtime_root,
            session_type=self.semantic_session_type,
            popen=self.popen,
            clock=self.clock,
        )

        with self.assertRaisesRegex(HarnessError, "symlink components"):
            adapter.session_start(self.session_start_payload(session_id))

    def test_detached_drains_wait_for_the_same_session_lock(self) -> None:
        session_id = "host-session-blocking-lock"
        self.start_bound_session(session_id)
        session_directory = self.adapter.store._session_directory(session_id)
        entered = threading.Event()
        finished = threading.Event()

        def run_second_drain() -> None:
            entered.set()
            self.adapter.drain(self.session_key(session_id))
            finished.set()

        with self.adapter.store._drain_lock(session_directory):
            worker = threading.Thread(target=run_second_drain)
            worker.start()
            self.assertTrue(entered.wait(timeout=1.0))
            self.assertFalse(finished.wait(timeout=0.05))
        worker.join(timeout=1.0)

        self.assertFalse(worker.is_alive())
        self.assertTrue(finished.is_set())
