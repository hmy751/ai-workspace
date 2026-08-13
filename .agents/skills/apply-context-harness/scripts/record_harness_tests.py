#!/usr/bin/env python3
"""Run target Harness tests without a shell and write an evidence-linked receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO


class ReceiptError(RuntimeError):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def compact_utc(value: datetime) -> str:
    return value.strftime("%Y%m%dT%H%M%S%fZ")


def safe_relative_path(raw: str, label: str, *, allow_root: bool = False) -> PurePosixPath:
    path = PurePosixPath(raw)
    if allow_root and raw == ".":
        return path
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ReceiptError(f"{label} must be a project-root relative path without '..': {raw}")
    return path


def resolve_inside(root: Path, relative: PurePosixPath, label: str) -> Path:
    candidate = root.joinpath(*relative.parts)
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ReceiptError(f"{label} must not contain a symlink: {relative}")
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ReceiptError(f"{label} escapes project root: {relative}") from error
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def capture_python_sources(project_root: Path, source_root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for current, directories, filenames in os.walk(source_root, topdown=True, followlinks=False):
        current_path = Path(current)
        clean_directories = []
        for directory in sorted(directories):
            directory_path = current_path / directory
            if directory == "__pycache__":
                continue
            if directory_path.is_symlink():
                raise ReceiptError(f"Harness source directory must not be a symlink: {directory_path}")
            clean_directories.append(directory)
        directories[:] = clean_directories
        for filename in sorted(filenames):
            if not filename.endswith(".py"):
                continue
            path = current_path / filename
            if path.is_symlink() or not path.is_file():
                raise ReceiptError(f"Harness source must be a regular file, not a symlink: {path}")
            stat = path.stat()
            entries.append(
                {
                    "path": path.relative_to(project_root).as_posix(),
                    "size": stat.st_size,
                    "sha256": sha256_file(path),
                }
            )
    if not entries:
        raise ReceiptError(f"no Python source files found under {source_root}")
    return entries


class BoundedStreamCapture:
    def __init__(self, max_bytes: int) -> None:
        self.max_bytes = max_bytes
        self.observed_bytes = 0
        self.prefix = bytearray()
        self.read_error: str | None = None

    def add(self, payload: bytes) -> None:
        self.observed_bytes += len(payload)
        remaining = self.max_bytes - len(self.prefix)
        if remaining > 0:
            self.prefix.extend(payload[:remaining])

    def drain(self, stream: BinaryIO) -> None:
        try:
            while True:
                chunk = stream.read(64 * 1024)
                if not chunk:
                    break
                self.add(chunk)
        except (OSError, ValueError) as error:
            self.read_error = str(error)
        finally:
            try:
                stream.close()
            except (OSError, ValueError):
                pass

    def record(self) -> dict[str, Any]:
        captured = bytes(self.prefix)
        return {
            "encoding": "utf-8",
            "text": captured.decode("utf-8", errors="replace"),
            "original_bytes": self.observed_bytes,
            "captured_bytes": len(captured),
            "truncated": self.observed_bytes > len(captured),
            "read_error": self.read_error,
        }


def parse_test_count(stdout: dict[str, Any], stderr: dict[str, Any]) -> int | None:
    combined = f"{stdout['text']}\n{stderr['text']}"
    matches = re.findall(r"Ran\s+(\d+)\s+tests?\b", combined)
    return int(matches[-1]) if matches else None


def run_unittest(
    argv: list[str], project_root: Path, timeout_seconds: float, max_output_bytes: int
) -> dict[str, Any]:
    started_at = utc_now()
    stdout_capture = BoundedStreamCapture(max_output_bytes)
    stderr_capture = BoundedStreamCapture(max_output_bytes)
    process: subprocess.Popen[bytes] | None = None
    try:
        process = subprocess.Popen(
            argv,
            cwd=project_root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=os.name == "posix",
        )
    except FileNotFoundError as error:
        returncode = None
        exit_code = 127
        timed_out = False
        stderr_capture.add(str(error).encode("utf-8", errors="replace"))
        execution_error = str(error)
    else:
        if process.stdout is None or process.stderr is None:
            raise ReceiptError("unittest process did not expose stdout and stderr pipes")
        stdout_thread = threading.Thread(
            target=stdout_capture.drain, args=(process.stdout,), daemon=True
        )
        stderr_thread = threading.Thread(
            target=stderr_capture.drain, args=(process.stderr,), daemon=True
        )
        stdout_thread.start()
        stderr_thread.start()
        try:
            process.wait(timeout=timeout_seconds)
            timed_out = False
            execution_error = None
        except subprocess.TimeoutExpired:
            timed_out = True
            execution_error = f"command timed out after {timeout_seconds} seconds"
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
            process.wait()
        returncode = process.returncode
        exit_code = 124 if timed_out else int(process.returncode or 0)
        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)
        if stdout_thread.is_alive():
            stdout_capture.read_error = "stdout pipe did not close after unittest exit"
            process.stdout.close()
        if stderr_thread.is_alive():
            stderr_capture.read_error = "stderr pipe did not close after unittest exit"
            process.stderr.close()

    finished_at = utc_now()
    stdout = stdout_capture.record()
    stderr = stderr_capture.record()
    test_count = parse_test_count(stdout, stderr)
    if exit_code == 0 and (test_count is None or test_count < 1):
        exit_code = 5
        execution_error = "unittest discovery did not report at least one test"
    return {
        "started_at": iso_utc(started_at),
        "finished_at": iso_utc(finished_at),
        "argv": argv,
        "result": "pass" if exit_code == 0 else "fail",
        "exit_code": exit_code,
        "process_returncode": returncode,
        "timeout": {
            "seconds": timeout_seconds,
            "timed_out": timed_out,
            "termination_scope": "process_group" if os.name == "posix" else "direct_process",
        },
        "stdout": stdout,
        "stderr": stderr,
        "execution_error": execution_error,
        "test_count": test_count,
    }


def write_receipt(receipt: dict[str, Any], records_dir: Path) -> Path:
    finished_at = datetime.fromisoformat(receipt["finished_at"].replace("Z", "+00:00"))
    filename = f"harness-test-{compact_utc(finished_at)}-{receipt['receipt_id']}.json"
    destination = records_dir / filename
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=records_dir,
        prefix=f".{filename}.",
        suffix=".tmp",
        delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError as error:
            raise ReceiptError(f"refusing to overwrite receipt: {destination}") from error
        temporary.unlink()
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return destination


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--tests-start", required=True)
    parser.add_argument("--top-level", default=".")
    parser.add_argument("--pattern", default="test_*.py")
    parser.add_argument("--records-dir", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    parser.add_argument("--max-output-bytes", type=int, default=1_000_000)
    args = parser.parse_args(argv)
    if args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be positive")
    if args.max_output_bytes <= 0:
        parser.error("--max-output-bytes must be positive")
    if not args.pattern or "/" in args.pattern or "\\" in args.pattern:
        parser.error("--pattern must be a filename pattern without path separators")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        project_root = args.project_root.resolve(strict=True)
        if not project_root.is_dir():
            raise ReceiptError(f"project root is not a directory: {project_root}")

        source_relative = safe_relative_path(args.source_root, "source root")
        tests_relative = safe_relative_path(args.tests_start, "tests start")
        top_level_relative = safe_relative_path(args.top_level, "top level", allow_root=True)
        records_relative = safe_relative_path(args.records_dir, "records dir")
        source_root = resolve_inside(project_root, source_relative, "source root")
        tests_start = resolve_inside(project_root, tests_relative, "tests start")
        top_level = resolve_inside(project_root, top_level_relative, "top level")
        records_dir = resolve_inside(project_root, records_relative, "records dir")
        if not all(path.is_dir() for path in (source_root, tests_start, top_level, records_dir)):
            raise ReceiptError("source root, tests start, top level, and records dir must be directories")
        try:
            tests_start.relative_to(source_root)
        except ValueError as error:
            raise ReceiptError("tests start must be inside source root") from error

        unittest_argv = [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            tests_relative.as_posix(),
            "-t",
            top_level_relative.as_posix(),
            "-p",
            args.pattern,
            "-v",
        ]

        evidence_captured_at = utc_now()
        source_files = capture_python_sources(project_root, source_root)
        execution = run_unittest(
            unittest_argv, project_root, args.timeout_seconds, args.max_output_bytes
        )
        receipt = {
            "schema_version": 1,
            "receipt_type": "harness_test",
            "receipt_id": uuid.uuid4().hex,
            "project_root": str(project_root),
            "source_root": source_relative.as_posix(),
            "tests_start": tests_relative.as_posix(),
            "top_level": top_level_relative.as_posix(),
            "pattern": args.pattern,
            "test_framework": "python_unittest_discover",
            "evidence_capture": "before_verification",
            "evidence_captured_at": iso_utc(evidence_captured_at),
            "source_files": source_files,
            **execution,
        }
        destination = write_receipt(receipt, records_dir)
    except (ReceiptError, FileNotFoundError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(
        json.dumps(
            {
                "receipt_path": str(destination),
                "result": receipt["result"],
                "exit_code": receipt["exit_code"],
                "source_file_count": len(receipt["source_files"]),
                "test_count": receipt["test_count"],
            },
            ensure_ascii=False,
        )
    )
    return int(receipt["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
