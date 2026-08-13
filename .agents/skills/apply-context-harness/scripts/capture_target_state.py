#!/usr/bin/env python3
"""Capture a target Git repository's pre-migration state without changing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IGNORED_WALK_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".turbo",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "vendor",
}
INSTRUCTION_NAMES = {"AGENTS.md", "CLAUDE.md"}


class CaptureError(RuntimeError):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def compact_utc(value: datetime) -> str:
    return value.strftime("%Y%m%dT%H%M%S%fZ")


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and process.returncode != 0:
        message = process.stderr.decode("utf-8", errors="replace").strip()
        raise CaptureError(f"git {' '.join(args)} failed: {message}")
    return process


def decode_paths(payload: bytes) -> list[str]:
    return [os.fsdecode(item) for item in payload.split(b"\0") if item]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head_oid(root: Path, relative_path: str, head_exists: bool) -> str | None:
    if not head_exists:
        return None
    result = run_git(root, "ls-tree", "-z", "HEAD", "--", relative_path, check=False)
    if result.returncode != 0 or not result.stdout:
        return None
    header = result.stdout.split(b"\t", 1)[0]
    parts = header.split()
    return parts[2].decode("ascii") if len(parts) >= 3 else None


def git_index_oid(root: Path, relative_path: str) -> str | None:
    result = run_git(root, "ls-files", "--stage", "-z", "--", relative_path)
    if not result.stdout:
        return None
    header = result.stdout.split(b"\t", 1)[0]
    parts = header.split()
    return parts[1].decode("ascii") if len(parts) >= 2 else None


def snapshot_path(root: Path, relative_path: str, *, head_exists: bool) -> dict[str, Any]:
    path = root / relative_path
    entry: dict[str, Any] = {
        "path": relative_path,
        "head_oid": git_head_oid(root, relative_path, head_exists),
        "index_oid": git_index_oid(root, relative_path),
    }
    try:
        stat = path.lstat()
    except FileNotFoundError:
        entry["kind"] = "missing"
        return entry

    if path.is_symlink():
        target = os.readlink(path)
        payload = os.fsencode(target)
        entry.update(
            {
                "kind": "symlink",
                "link_target": target,
                "size": len(payload),
                "sha256": sha256_bytes(payload),
            }
        )
    elif path.is_file():
        entry.update(
            {
                "kind": "file",
                "size": stat.st_size,
                "sha256": sha256_file(path),
            }
        )
    elif path.is_dir():
        entry.update({"kind": "directory", "size": stat.st_size})
    else:
        entry.update({"kind": "other", "size": stat.st_size})
    return entry


def discover_instruction_files(root: Path, *, head_exists: bool) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in IGNORED_WALK_DIRS
            and not (Path(current) / directory).is_symlink()
        )
        for filename in sorted(filenames):
            if filename not in INSTRUCTION_NAMES:
                continue
            path = Path(current) / filename
            relative_path = path.relative_to(root).as_posix()
            entries.append(snapshot_path(root, relative_path, head_exists=head_exists))
    return entries


def build_receipt(project_root: Path) -> dict[str, Any]:
    requested_root = project_root.resolve(strict=True)
    if not requested_root.is_dir():
        raise CaptureError(f"project root is not a directory: {requested_root}")

    actual_root_text = run_git(requested_root, "rev-parse", "--show-toplevel").stdout.decode(
        "utf-8", errors="strict"
    ).strip()
    actual_root = Path(actual_root_text).resolve(strict=True)
    if requested_root != actual_root:
        raise CaptureError(
            f"project root must equal the Git root: requested={requested_root} git_root={actual_root}"
        )

    head_result = run_git(actual_root, "rev-parse", "--verify", "HEAD", check=False)
    head = head_result.stdout.decode("ascii").strip() if head_result.returncode == 0 else None
    branch_result = run_git(actual_root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    branch = branch_result.stdout.decode("utf-8", errors="replace").strip() or None

    groups = {
        "worktree": decode_paths(run_git(actual_root, "diff", "--name-only", "-z", "--").stdout),
        "index": decode_paths(
            run_git(actual_root, "diff", "--cached", "--name-only", "-z", "--").stdout
        ),
        "untracked": decode_paths(
            run_git(actual_root, "ls-files", "--others", "--exclude-standard", "-z").stdout
        ),
    }
    path_states: dict[str, list[str]] = {}
    for state, paths in groups.items():
        for path in paths:
            path_states.setdefault(path, []).append(state)

    dirty_entries = []
    for path in sorted(path_states):
        entry = snapshot_path(actual_root, path, head_exists=head is not None)
        entry["states"] = path_states[path]
        dirty_entries.append(entry)

    porcelain = run_git(
        actual_root, "status", "--porcelain=v1", "--untracked-files=all"
    ).stdout.decode("utf-8", errors="replace")
    captured_at = utc_now()
    return {
        "schema_version": 1,
        "receipt_type": "context_harness_preflight",
        "receipt_id": uuid.uuid4().hex,
        "captured_at": iso_utc(captured_at),
        "project_root": str(actual_root),
        "git": {
            "head": head,
            "branch": branch,
            "status_porcelain_v1": porcelain,
            "dirty_entries": dirty_entries,
        },
        "instruction_files": discover_instruction_files(actual_root, head_exists=head is not None),
        "proof_ceiling": (
            "This receipt captures observed paths and bytes during one local capture pass. "
            "It is not an atomic snapshot; concurrent changes may make fields internally "
            "inconsistent. It does not establish authorship, intent, or a pre-existing "
            "immutable history."
        ),
    }


def write_receipt(receipt: dict[str, Any], output_dir: Path) -> Path:
    destination_dir = output_dir.resolve(strict=True)
    if not destination_dir.is_dir():
        raise CaptureError(f"output dir is not a directory: {destination_dir}")

    captured_at = datetime.fromisoformat(receipt["captured_at"].replace("Z", "+00:00"))
    filename = f"preflight-{compact_utc(captured_at)}-{receipt['receipt_id']}.json"
    destination = destination_dir / filename
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=destination_dir,
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
            raise CaptureError(f"refusing to overwrite receipt: {destination}") from error
        temporary.unlink()
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return destination


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        receipt = build_receipt(args.project_root)
        destination = write_receipt(receipt, args.output_dir)
    except (CaptureError, FileNotFoundError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "receipt_path": str(destination),
                "dirty_entry_count": len(receipt["git"]["dirty_entries"]),
                "instruction_file_count": len(receipt["instruction_files"]),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
