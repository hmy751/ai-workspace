"""Deterministic, guarded Markdown writes for one selected Workspace.

The Maintainer agent proposes text.  This module is the narrower authority that
may commit it.  It deliberately knows nothing about semantic decisions: it
checks the selected Workspace boundary, optimistic baselines, local links, and
the crash-recovery journal before replacing any file.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import tempfile
from typing import Any, Iterator, NoReturn
from urllib.parse import unquote, urlsplit
import uuid


JOURNAL_SCHEMA_VERSION = 3
COMPLETION_SCHEMA_VERSION = 1
JOURNAL_FILENAME = "maintain-write-journal.json"
LOCK_FILENAME = "maintain-write.lock"
STAGE_DIRECTORY_PREFIX = "maintain-write-stage-"
COMPLETION_DIRECTORY_NAME = "maintain-write-completed"

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_DATED_RECORD_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2})(?:-([^/]+))?\.md$"
)
_INLINE_LINK_PATTERN = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
_REFERENCE_LINK_PATTERN = re.compile(
    r"^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)", re.MULTILINE
)
_FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_INLINE_CODE_PATTERN = re.compile(r"(`+)(?!`)(.*?)(?<!`)\1(?!`)")


class GuardedWriteError(RuntimeError):
    """Base error for a write transaction that was not accepted."""


class UnsafeWriteError(GuardedWriteError):
    """A proposal escapes the Maintainer's deliberately narrow authority."""


class StaleBaselineError(GuardedWriteError):
    """At least one target no longer matches its proposed baseline."""

    def __init__(self, paths: Iterable[str]) -> None:
        self.paths = tuple(paths)
        super().__init__(
            "stale write baseline: " + ", ".join(self.paths)
        )


class BrokenMarkdownLinkError(GuardedWriteError):
    """Changed Markdown contains a local relative link with no target."""


class PendingJournalError(GuardedWriteError):
    """A previous transaction must be recovered before another can start."""


class JournalConflictError(GuardedWriteError):
    """Recovery found content that is neither the baseline nor the new text."""

    def __init__(self, paths: Iterable[str]) -> None:
        self.paths = tuple(paths)
        super().__init__(
            "write journal conflicts with current content: "
            + ", ".join(self.paths)
        )


class InvalidJournalError(GuardedWriteError):
    """The durable journal or its staged content cannot be trusted."""


class CompletedWriteConflictError(GuardedWriteError):
    """A transaction key was previously used for a different exact write."""


class InvalidCompletionError(GuardedWriteError):
    """A durable completed-write marker cannot be trusted."""


@dataclass(frozen=True)
class WriteProposal:
    """One complete replacement based on a caller-observed baseline.

    ``expected_sha256=None`` means that the target was absent when the proposal
    was prepared.  Existing targets require the lowercase SHA-256 hex digest of
    their complete bytes.
    """

    path: str
    expected_sha256: str | None
    content: str


@dataclass(frozen=True)
class WriteResult:
    """The paths whose proposed content is durably installed."""

    changed_paths: tuple[str, ...]


@dataclass(frozen=True)
class _PreparedProposal:
    path: str
    target: Path
    expected_sha256: str | None
    content_bytes: bytes
    new_sha256: str
    target_mode: int


@dataclass(frozen=True)
class _JournalEntry:
    path: str
    expected_sha256: str | None
    new_sha256: str
    stage_file: str
    target_mode: int


@dataclass(frozen=True)
class _Journal:
    transaction_id: str
    workspace_root: str
    completion_key_sha256: str | None
    request_sha256: str
    entries: tuple[_JournalEntry, ...]


@dataclass(frozen=True)
class _Completion:
    completion_key_sha256: str
    workspace_root: str
    request_sha256: str
    changed_paths: tuple[str, ...]


AfterReplace = Callable[[Path], None]


def apply_writes(
    workspace_root: Path,
    writer_runtime_root: Path,
    proposals: Iterable[WriteProposal],
    *,
    transaction_key: str | None = None,
    after_replace: AfterReplace | None = None,
) -> WriteResult:
    """Validate and atomically replace one all-baseline-consistent proposal set.

    The lock covers the complete baseline check and transaction.  A failure
    before the journal is published changes no target.  A failure after journal
    publication leaves enough staged data for :func:`recover_journal` to finish
    the transaction or report a content conflict without claiming success.

    ``writer_runtime_root`` must be the one Workspace-wide namespace shared by
    every Main session.  ``transaction_key`` must be stable for one semantic
    intent (for example, its event id plus content digest).  A durable marker
    makes an exact replay succeed even when a later session has already made a
    subsequent valid change to the same target.

    Omitting ``transaction_key`` retains the older one-shot behavior for
    callers that do not need cross-session crash replay.

    ``after_replace`` is a test seam called after each durable target replace.
    Production callers normally omit it.
    """

    workspace = _workspace_root(workspace_root)
    runtime = _runtime_root(writer_runtime_root)
    proposal_list = tuple(proposals)
    _reject_duplicate_paths(proposal_list)
    request_sha256, request_changed_paths = _request_identity(proposal_list)
    completion_key_sha256 = _completion_key_sha256(transaction_key)

    with _exclusive_lock(runtime):
        if completion_key_sha256 is not None:
            completed = _read_completion(
                runtime,
                completion_key_sha256,
                expected_workspace_root=str(workspace),
                expected_request_sha256=request_sha256,
                expected_changed_paths=request_changed_paths,
            )
            if completed is not None:
                return WriteResult(changed_paths=completed.changed_paths)

        journal_path = runtime / JOURNAL_FILENAME
        if journal_path.exists() or journal_path.is_symlink():
            raise PendingJournalError(
                "a previous Maintain write journal requires recovery"
            )

        prepared = tuple(
            _prepare_proposal(workspace, proposal) for proposal in proposal_list
        )

        # This is intentionally a separate complete pass.  No staging or target
        # mutation begins until every caller-observed baseline has been checked
        # while holding the transaction lock.
        stale = [
            item.path
            for item in prepared
            if _content_sha256(item.target) != item.expected_sha256
        ]
        if stale:
            raise StaleBaselineError(stale)

        changed = tuple(
            item
            for item in prepared
            if item.new_sha256 != item.expected_sha256
        )
        if not changed:
            if completion_key_sha256 is not None:
                _write_completion(
                    runtime,
                    _Completion(
                        completion_key_sha256=completion_key_sha256,
                        workspace_root=str(workspace),
                        request_sha256=request_sha256,
                        changed_paths=(),
                    ),
                )
            return WriteResult(changed_paths=())

        _validate_changed_markdown_links(workspace, changed)
        journal = _stage_transaction(
            runtime,
            workspace,
            changed,
            completion_key_sha256=completion_key_sha256,
            request_sha256=request_sha256,
        )
        return _finish_journal_locked(
            workspace,
            runtime,
            journal,
            after_replace=after_replace,
        )


def recover_journal(
    workspace_root: Path,
    writer_runtime_root: Path,
    *,
    after_replace: AfterReplace | None = None,
) -> WriteResult:
    """Finish the one durable transaction in ``writer_runtime_root``.

    Recovery first classifies *all* targets.  Each must still contain either
    its recorded baseline or its recorded new content.  A third value stops
    recovery before this call performs another replacement and retains the
    journal for explicit inspection or later retry.
    """

    workspace = _workspace_root(workspace_root)
    runtime = _runtime_root(writer_runtime_root)
    with _exclusive_lock(runtime):
        journal_path = runtime / JOURNAL_FILENAME
        if not journal_path.exists() and not journal_path.is_symlink():
            return WriteResult(changed_paths=())
        journal = _read_journal(runtime, journal_path)
        if journal.workspace_root != str(workspace):
            raise InvalidJournalError(
                "write journal belongs to a different Workspace root"
            )
        return _finish_journal_locked(
            workspace,
            runtime,
            journal,
            after_replace=after_replace,
        )


def acknowledge_transaction(
    workspace_root: Path,
    writer_runtime_root: Path,
    transaction_key: str,
    proposals: Iterable[WriteProposal],
) -> bool:
    """Remove one exact completion marker after its event is acknowledged.

    The caller must first durably commit the corresponding event checkpoint.
    A missing marker is an idempotent ``False``.  Reusing the same key with a
    different Workspace or proposal fingerprint is a hard conflict rather
    than permission to delete evidence belonging to another intent.
    """

    workspace = _workspace_root(workspace_root)
    runtime = _runtime_root(writer_runtime_root)
    proposal_list = tuple(proposals)
    _reject_duplicate_paths(proposal_list)
    request_sha256, request_changed_paths = _request_identity(proposal_list)
    completion_key_sha256 = _completion_key_sha256(transaction_key)
    if completion_key_sha256 is None:
        raise UnsafeWriteError("transaction_key is required for acknowledgement")

    with _exclusive_lock(runtime):
        completed = _read_completion(
            runtime,
            completion_key_sha256,
            expected_workspace_root=str(workspace),
            expected_request_sha256=request_sha256,
            expected_changed_paths=request_changed_paths,
        )
        if completed is None:
            return False
        marker = _completion_path(runtime, completion_key_sha256, create=False)
        assert marker is not None
        marker.unlink()
        _fsync_directory(marker.parent)
        return True


def sha256_text(content: str) -> str:
    """Return the baseline digest callers should use for existing UTF-8 text."""

    if not isinstance(content, str):
        raise TypeError("content must be a string")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _completion_key_sha256(value: str | None) -> str | None:
    if value is None:
        return None
    if (
        not isinstance(value, str)
        or not value
        or "\x00" in value
        or len(value) > 4096
    ):
        raise UnsafeWriteError(
            "transaction_key must be a non-empty string of at most 4096 characters"
        )
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _request_identity(
    proposals: tuple[WriteProposal, ...]
) -> tuple[str, tuple[str, ...]]:
    request: list[dict[str, str | None]] = []
    changed_paths: list[str] = []
    for proposal in proposals:
        if not isinstance(proposal, WriteProposal):
            raise TypeError("proposals must contain WriteProposal values")
        path = _normalize_write_path(proposal.path)
        expected = _validate_expected_sha256(proposal.expected_sha256, path)
        if not isinstance(proposal.content, str):
            raise TypeError(f"content for {path} must be a string")
        try:
            content_bytes = proposal.content.encode("utf-8")
        except UnicodeEncodeError as error:
            raise UnsafeWriteError(
                f"content for {path} is not valid UTF-8 text"
            ) from error
        new_sha256 = hashlib.sha256(content_bytes).hexdigest()
        request.append(
            {
                "path": path,
                "expected_sha256": expected,
                "new_sha256": new_sha256,
            }
        )
        if new_sha256 != expected:
            changed_paths.append(path)
    payload = json.dumps(
        request,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest(), tuple(changed_paths)


def _fail_unsafe(message: str) -> NoReturn:
    raise UnsafeWriteError(message)


def _workspace_root(value: Path) -> Path:
    path = Path(value)
    if path.is_symlink():
        _fail_unsafe("Workspace root must not be a symlink")
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError as error:
        raise UnsafeWriteError("Workspace root does not exist") from error
    if not resolved.is_dir():
        _fail_unsafe("Workspace root must be a directory")
    return resolved


def _runtime_root(value: Path) -> Path:
    path = Path(value)
    if path.is_symlink():
        _fail_unsafe("runtime session root must not be a symlink")
    path.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        _fail_unsafe("runtime session root must not be a symlink")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        _fail_unsafe("runtime session root must be a directory")
    return resolved


def _normalize_write_path(raw: object) -> str:
    if not isinstance(raw, str) or not raw:
        _fail_unsafe("write path must be a non-empty string")
    if "\x00" in raw:
        _fail_unsafe("write path must not contain NUL")

    slash_normalized = raw.replace("\\", "/")
    posix = PurePosixPath(slash_normalized)
    parts = posix.parts
    if (
        Path(raw).is_absolute()
        or posix.is_absolute()
        or PureWindowsPath(raw).is_absolute()
    ):
        _fail_unsafe(f"write path must be relative: {raw!r}")
    if not parts or parts == (".",) or ".." in parts:
        _fail_unsafe(f"write path must not traverse its Workspace: {raw!r}")
    if slash_normalized != posix.as_posix():
        _fail_unsafe(f"write path must be normalized: {raw!r}")

    normalized = posix.as_posix()
    if _is_allowed_markdown_path(parts):
        return normalized
    _fail_unsafe(f"Maintainer may not write this Workspace path: {normalized}")


def _is_allowed_markdown_path(parts: tuple[str, ...]) -> bool:
    if len(parts) >= 2 and parts[0] == "current":
        return parts[-1].endswith(".md") and parts[-1] != ".md"
    if len(parts) == 2 and parts[0] == "records":
        if parts[1] in {"index.md", "README.md"}:
            return True
        match = _DATED_RECORD_PATTERN.fullmatch(parts[1])
        if match is None or match.group(2) == "":
            return False
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            return False
        return True
    return parts in {("output", "index.md"), ("source", "index.md")}


def _validate_expected_sha256(value: object, path: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not _SHA256_PATTERN.fullmatch(value):
        raise UnsafeWriteError(
            f"expected_sha256 for {path} must be lowercase SHA-256 hex or None"
        )
    return value


def _prepare_proposal(
    workspace: Path, proposal: WriteProposal
) -> _PreparedProposal:
    if not isinstance(proposal, WriteProposal):
        raise TypeError("proposals must contain WriteProposal values")
    path = _normalize_write_path(proposal.path)
    expected = _validate_expected_sha256(proposal.expected_sha256, path)
    if not isinstance(proposal.content, str):
        raise TypeError(f"content for {path} must be a string")
    try:
        content_bytes = proposal.content.encode("utf-8")
    except UnicodeEncodeError as error:
        raise UnsafeWriteError(
            f"content for {path} is not valid UTF-8 text"
        ) from error
    target = _guarded_target(workspace, path)
    try:
        target_mode = stat.S_IMODE(target.lstat().st_mode) & 0o777
    except FileNotFoundError:
        target_mode = 0o644
    return _PreparedProposal(
        path=path,
        target=target,
        expected_sha256=expected,
        content_bytes=content_bytes,
        new_sha256=hashlib.sha256(content_bytes).hexdigest(),
        target_mode=target_mode,
    )


def _reject_duplicate_paths(proposals: tuple[WriteProposal, ...]) -> None:
    seen: set[str] = set()
    for proposal in proposals:
        if not isinstance(proposal, WriteProposal):
            raise TypeError("proposals must contain WriteProposal values")
        path = _normalize_write_path(proposal.path)
        if path in seen:
            raise UnsafeWriteError(f"duplicate write path: {path}")
        seen.add(path)


def _guarded_target(workspace: Path, relative_path: str) -> Path:
    current = workspace
    parts = PurePosixPath(relative_path).parts
    for index, part in enumerate(parts):
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            if index != len(parts) - 1:
                raise UnsafeWriteError(
                    f"write parent does not exist: {relative_path}"
                )
            return current
        if stat.S_ISLNK(metadata.st_mode):
            raise UnsafeWriteError(
                f"write path must not use symlink components: {relative_path}"
            )
        if index != len(parts) - 1 and not stat.S_ISDIR(metadata.st_mode):
            raise UnsafeWriteError(
                f"write parent is not a directory: {relative_path}"
            )
        if index == len(parts) - 1 and not stat.S_ISREG(metadata.st_mode):
            raise UnsafeWriteError(
                f"write target is not a regular file: {relative_path}"
            )
    return current


def _content_sha256(path: Path) -> str | None:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise UnsafeWriteError(f"write target is no longer a regular file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 128), b""):
            digest.update(chunk)
    return digest.hexdigest()


@contextmanager
def _exclusive_lock(runtime: Path) -> Iterator[None]:
    lock_path = runtime / LOCK_FILENAME
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as error:
        raise UnsafeWriteError(f"cannot open guarded writer lock: {error}") from error
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            _fail_unsafe("guarded writer lock must be a regular file")
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _completion_directory(runtime: Path, *, create: bool) -> Path | None:
    directory = runtime / COMPLETION_DIRECTORY_NAME
    try:
        metadata = directory.lstat()
    except FileNotFoundError:
        if not create:
            return None
        try:
            directory.mkdir(mode=0o700)
            _fsync_directory(runtime)
        except FileExistsError:
            pass
        try:
            metadata = directory.lstat()
        except FileNotFoundError as error:
            raise InvalidCompletionError(
                "completed-write directory disappeared during creation"
            ) from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise InvalidCompletionError(
            "completed-write marker parent must be a regular directory"
        )
    return directory


def _completion_path(
    runtime: Path, completion_key_sha256: str, *, create: bool
) -> Path | None:
    directory = _completion_directory(runtime, create=create)
    if directory is None:
        return None
    return directory / f"{completion_key_sha256}.json"


def _read_completion(
    runtime: Path,
    completion_key_sha256: str,
    *,
    expected_workspace_root: str,
    expected_request_sha256: str,
    expected_changed_paths: tuple[str, ...],
) -> _Completion | None:
    marker = _completion_path(runtime, completion_key_sha256, create=False)
    if marker is None:
        return None
    try:
        metadata = marker.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise InvalidCompletionError(
            "completed-write marker must be a regular file"
        )
    try:
        raw = marker.read_text(encoding="utf-8")
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InvalidCompletionError(
            f"completed-write marker is unreadable: {error}"
        ) from error
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "completion_key_sha256",
        "workspace_root",
        "request_sha256",
        "changed_paths",
    }:
        raise InvalidCompletionError(
            "completed-write marker has invalid top-level fields"
        )
    if value["schema_version"] != COMPLETION_SCHEMA_VERSION:
        raise InvalidCompletionError(
            "completed-write marker schema version is unsupported"
        )
    recorded_key = value["completion_key_sha256"]
    workspace_root = value["workspace_root"]
    request_sha256 = value["request_sha256"]
    raw_paths = value["changed_paths"]
    if recorded_key != completion_key_sha256:
        raise InvalidCompletionError(
            "completed-write marker key does not match its filename"
        )
    if (
        not isinstance(request_sha256, str)
        or not _SHA256_PATTERN.fullmatch(request_sha256)
    ):
        raise InvalidCompletionError(
            "completed-write marker request digest is invalid"
        )
    if not isinstance(workspace_root, str) or not workspace_root:
        raise InvalidCompletionError(
            "completed-write marker Workspace root is invalid"
        )
    if not isinstance(raw_paths, list):
        raise InvalidCompletionError(
            "completed-write marker changed_paths must be a list"
        )
    changed_paths: list[str] = []
    seen: set[str] = set()
    for raw_path in raw_paths:
        try:
            path = _normalize_write_path(raw_path)
        except GuardedWriteError as error:
            raise InvalidCompletionError(str(error)) from error
        if path in seen:
            raise InvalidCompletionError(
                "completed-write marker contains duplicate paths"
            )
        seen.add(path)
        changed_paths.append(path)
    if (
        workspace_root != expected_workspace_root
        or request_sha256 != expected_request_sha256
    ):
        raise CompletedWriteConflictError(
            "transaction_key already belongs to a different exact write"
        )
    if tuple(changed_paths) != expected_changed_paths:
        raise InvalidCompletionError(
            "completed-write marker paths do not match its exact request"
        )
    return _Completion(
        completion_key_sha256=recorded_key,
        workspace_root=workspace_root,
        request_sha256=request_sha256,
        changed_paths=tuple(changed_paths),
    )


def _write_completion(runtime: Path, completion: _Completion) -> None:
    existing = _read_completion(
        runtime,
        completion.completion_key_sha256,
        expected_workspace_root=completion.workspace_root,
        expected_request_sha256=completion.request_sha256,
        expected_changed_paths=completion.changed_paths,
    )
    if existing is not None:
        if existing.changed_paths != completion.changed_paths:
            raise CompletedWriteConflictError(
                "transaction_key completion paths do not match"
            )
        return

    marker = _completion_path(
        runtime, completion.completion_key_sha256, create=True
    )
    assert marker is not None
    payload = (
        json.dumps(
            {
                "schema_version": COMPLETION_SCHEMA_VERSION,
                "completion_key_sha256": completion.completion_key_sha256,
                "workspace_root": completion.workspace_root,
                "request_sha256": completion.request_sha256,
                "changed_paths": list(completion.changed_paths),
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".maintain-write-completed-", dir=marker.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as destination:
            destination.write(payload)
            destination.flush()
            os.fsync(destination.fileno())
        os.close(descriptor)
        descriptor = -1
        try:
            os.link(temporary_path, marker)
        except FileExistsError:
            existing = _read_completion(
                runtime,
                completion.completion_key_sha256,
                expected_workspace_root=completion.workspace_root,
                expected_request_sha256=completion.request_sha256,
                expected_changed_paths=completion.changed_paths,
            )
            if existing is None or existing.changed_paths != completion.changed_paths:
                raise CompletedWriteConflictError(
                    "transaction_key completion appeared with different paths"
                )
        _fsync_directory(marker.parent)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _validate_changed_markdown_links(
    workspace: Path, changed: tuple[_PreparedProposal, ...]
) -> None:
    proposed_paths = {item.path for item in changed}
    for item in changed:
        text = item.content_bytes.decode("utf-8")
        for raw_destination in _markdown_destinations(text):
            destination = _relative_link_destination(raw_destination)
            if destination is None:
                continue
            decoded = unquote(destination)
            link_path = Path(decoded)
            if link_path.is_absolute() or PureWindowsPath(decoded).is_absolute():
                continue

            candidate = item.target.parent / link_path
            if candidate.exists():
                continue

            # Transaction-created targets are compared lexically because the
            # target does not exist yet and therefore cannot be resolved.
            normalized = os.path.normpath(
                str(PurePosixPath(item.path).parent / PurePosixPath(decoded))
            ).replace("\\", "/")
            if normalized in proposed_paths:
                continue
            raise BrokenMarkdownLinkError(
                f"broken local Markdown link in {item.path}: {raw_destination}"
            )


def _markdown_destinations(text: str) -> Iterator[str]:
    link_text = _without_markdown_code(text)
    for match in _INLINE_LINK_PATTERN.finditer(link_text):
        raw = match.group(1).strip()
        if raw.startswith("<") and ">" in raw:
            yield raw[1 : raw.index(">")]
        else:
            # Markdown permits an optional title after a whitespace separator.
            yield raw.split(maxsplit=1)[0]
    for match in _REFERENCE_LINK_PATTERN.finditer(link_text):
        raw = match.group(1)
        if raw.startswith("<") and raw.endswith(">"):
            yield raw[1:-1]
        else:
            yield raw


def _without_markdown_code(text: str) -> str:
    """Remove fenced and inline code where link syntax is only an example."""

    visible: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        fence = _FENCE_PATTERN.match(line)
        if fence_character is None:
            if fence is not None:
                marker = fence.group(1)
                fence_character = marker[0]
                fence_length = len(marker)
                visible.append("\n" if line.endswith("\n") else "")
                continue
            visible.append(_INLINE_CODE_PATTERN.sub("", line))
            continue

        if (
            fence is not None
            and fence.group(1)[0] == fence_character
            and len(fence.group(1)) >= fence_length
        ):
            fence_character = None
            fence_length = 0
        visible.append("\n" if line.endswith("\n") else "")
    return "".join(visible)


def _relative_link_destination(raw: str) -> str | None:
    if not raw or raw.startswith("#"):
        return None
    split = urlsplit(raw)
    if split.scheme or split.netloc:
        return None
    path = split.path
    return path or None


def _stage_transaction(
    runtime: Path,
    workspace: Path,
    changed: tuple[_PreparedProposal, ...],
    *,
    completion_key_sha256: str | None,
    request_sha256: str,
) -> _Journal:
    transaction_id = uuid.uuid4().hex
    stage_directory_name = STAGE_DIRECTORY_PREFIX + transaction_id
    stage_directory = runtime / stage_directory_name
    stage_directory.mkdir(mode=0o700)
    _fsync_directory(runtime)

    entries: list[_JournalEntry] = []
    try:
        for index, item in enumerate(changed):
            stage_name = f"{index:04d}.utf8"
            stage_path = stage_directory / stage_name
            descriptor = os.open(
                stage_path,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
            try:
                with os.fdopen(descriptor, "wb", closefd=False) as destination:
                    destination.write(item.content_bytes)
                    destination.flush()
                    os.fsync(destination.fileno())
            finally:
                os.close(descriptor)
            entries.append(
                _JournalEntry(
                    path=item.path,
                    expected_sha256=item.expected_sha256,
                    new_sha256=item.new_sha256,
                    stage_file=f"{stage_directory_name}/{stage_name}",
                    target_mode=item.target_mode,
                )
            )
        _fsync_directory(stage_directory)
        journal = _Journal(
            transaction_id=transaction_id,
            workspace_root=str(workspace),
            completion_key_sha256=completion_key_sha256,
            request_sha256=request_sha256,
            entries=tuple(entries),
        )
        _write_journal_atomic(runtime, journal)
        return journal
    except BaseException:
        # Before journal publication, staged data has no recovery authority.
        if not (runtime / JOURNAL_FILENAME).exists():
            _remove_stage_files(runtime, entries, stage_directory)
        raise


def _journal_object(journal: _Journal) -> dict[str, object]:
    return {
        "schema_version": JOURNAL_SCHEMA_VERSION,
        "transaction_id": journal.transaction_id,
        "workspace_root": journal.workspace_root,
        "completion_key_sha256": journal.completion_key_sha256,
        "request_sha256": journal.request_sha256,
        "entries": [
            {
                "path": entry.path,
                "expected_sha256": entry.expected_sha256,
                "new_sha256": entry.new_sha256,
                "stage_file": entry.stage_file,
                "target_mode": entry.target_mode,
            }
            for entry in journal.entries
        ],
    }


def _write_journal_atomic(runtime: Path, journal: _Journal) -> None:
    payload = (
        json.dumps(
            _journal_object(journal),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".maintain-write-journal-", dir=runtime
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as destination:
            destination.write(payload)
            destination.flush()
            os.fsync(destination.fileno())
        os.close(descriptor)
        descriptor = -1
        os.replace(temporary_path, runtime / JOURNAL_FILENAME)
        _fsync_directory(runtime)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _read_journal(runtime: Path, journal_path: Path) -> _Journal:
    if journal_path.is_symlink() or not journal_path.is_file():
        raise InvalidJournalError("write journal must be a regular file")
    try:
        raw = journal_path.read_text(encoding="utf-8")
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InvalidJournalError(f"write journal is unreadable: {error}") from error
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "transaction_id",
        "workspace_root",
        "completion_key_sha256",
        "request_sha256",
        "entries",
    }:
        raise InvalidJournalError("write journal has invalid top-level fields")
    if value["schema_version"] != JOURNAL_SCHEMA_VERSION:
        raise InvalidJournalError("write journal schema version is unsupported")
    transaction_id = value["transaction_id"]
    if (
        not isinstance(transaction_id, str)
        or not re.fullmatch(r"[0-9a-f]{32}", transaction_id)
    ):
        raise InvalidJournalError("write journal transaction_id is invalid")
    workspace_root = value["workspace_root"]
    if not isinstance(workspace_root, str) or not workspace_root:
        raise InvalidJournalError("write journal workspace_root is invalid")
    completion_key_sha256 = value["completion_key_sha256"]
    if completion_key_sha256 is not None and (
        not isinstance(completion_key_sha256, str)
        or not _SHA256_PATTERN.fullmatch(completion_key_sha256)
    ):
        raise InvalidJournalError(
            "write journal completion_key_sha256 is invalid"
        )
    request_sha256 = value["request_sha256"]
    if (
        not isinstance(request_sha256, str)
        or not _SHA256_PATTERN.fullmatch(request_sha256)
    ):
        raise InvalidJournalError("write journal request_sha256 is invalid")
    raw_entries = value["entries"]
    if not isinstance(raw_entries, list) or not raw_entries:
        raise InvalidJournalError("write journal entries must be a non-empty list")

    entries: list[_JournalEntry] = []
    seen: set[str] = set()
    stage_prefix = STAGE_DIRECTORY_PREFIX + transaction_id
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict) or set(raw_entry) != {
            "path",
            "expected_sha256",
            "new_sha256",
            "stage_file",
            "target_mode",
        }:
            raise InvalidJournalError("write journal entry fields are invalid")
        try:
            path = _normalize_write_path(raw_entry["path"])
            expected = _validate_expected_sha256(raw_entry["expected_sha256"], path)
        except GuardedWriteError as error:
            raise InvalidJournalError(str(error)) from error
        new_sha = raw_entry["new_sha256"]
        if not isinstance(new_sha, str) or not _SHA256_PATTERN.fullmatch(new_sha):
            raise InvalidJournalError("write journal new_sha256 is invalid")
        stage_file = raw_entry["stage_file"]
        expected_stage = f"{stage_prefix}/{len(entries):04d}.utf8"
        if stage_file != expected_stage:
            raise InvalidJournalError("write journal stage_file is invalid")
        target_mode = raw_entry["target_mode"]
        if (
            not isinstance(target_mode, int)
            or isinstance(target_mode, bool)
            or target_mode < 0
            or target_mode > 0o777
        ):
            raise InvalidJournalError("write journal target_mode is invalid")
        if path in seen:
            raise InvalidJournalError("write journal contains duplicate paths")
        seen.add(path)
        stage_path = runtime / stage_file
        if stage_path.is_symlink() or stage_path.parent.is_symlink():
            raise InvalidJournalError("staged content must not use symlinks")
        if _content_sha256(stage_path) != new_sha:
            raise InvalidJournalError("staged content hash does not match journal")
        entries.append(
            _JournalEntry(
                path=path,
                expected_sha256=expected,
                new_sha256=new_sha,
                stage_file=stage_file,
                target_mode=target_mode,
            )
        )
    return _Journal(
        transaction_id=transaction_id,
        workspace_root=workspace_root,
        completion_key_sha256=completion_key_sha256,
        request_sha256=request_sha256,
        entries=tuple(entries),
    )


def _finish_journal_locked(
    workspace: Path,
    runtime: Path,
    journal: _Journal,
    *,
    after_replace: AfterReplace | None,
) -> WriteResult:
    targets: list[tuple[_JournalEntry, Path, str | None]] = []
    conflicts: list[str] = []
    for entry in journal.entries:
        target = _guarded_target(workspace, entry.path)
        current_sha = _content_sha256(target)
        if current_sha not in {entry.expected_sha256, entry.new_sha256}:
            conflicts.append(entry.path)
        targets.append((entry, target, current_sha))
    if conflicts:
        raise JournalConflictError(conflicts)

    for entry, target, observed_sha in targets:
        if observed_sha == entry.new_sha256:
            continue
        # Recheck immediately before replacing to avoid overwriting an
        # uncooperative writer that changed the file after classification.
        if _content_sha256(target) != entry.expected_sha256:
            raise JournalConflictError((entry.path,))
        stage_path = runtime / entry.stage_file
        if _content_sha256(stage_path) != entry.new_sha256:
            raise InvalidJournalError(
                f"staged content for {entry.path} is missing or corrupt"
            )
        _atomic_replace_from_stage(stage_path, target, entry.target_mode)
        if after_replace is not None:
            after_replace(target)

    # The completion marker is the idempotency boundary for the semantic
    # intent.  Publish and fsync it before removing the recovery journal.  If
    # the process dies between those steps, recovery validates the same marker
    # and only finishes cleanup; if it dies before publication, the journal can
    # recreate the marker from its content-addressed metadata.
    if journal.completion_key_sha256 is not None:
        _write_completion(
            runtime,
            _Completion(
                completion_key_sha256=journal.completion_key_sha256,
                workspace_root=journal.workspace_root,
                request_sha256=journal.request_sha256,
                changed_paths=tuple(entry.path for entry in journal.entries),
            ),
        )

    journal_path = runtime / JOURNAL_FILENAME
    journal_path.unlink()
    _fsync_directory(runtime)
    _remove_completed_stage(runtime, journal)
    return WriteResult(changed_paths=tuple(entry.path for entry in journal.entries))


def _atomic_replace_from_stage(
    stage_path: Path, target: Path, target_mode: int
) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".maintain-write-", dir=target.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with stage_path.open("rb") as source, os.fdopen(
            descriptor, "wb", closefd=False
        ) as destination:
            for chunk in iter(lambda: source.read(1024 * 128), b""):
                destination.write(chunk)
            destination.flush()
            os.fchmod(destination.fileno(), target_mode)
            os.fsync(destination.fileno())
        os.close(descriptor)
        descriptor = -1
        os.replace(temporary_path, target)
        _fsync_directory(target.parent)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _remove_completed_stage(runtime: Path, journal: _Journal) -> None:
    stage_directory = runtime / (STAGE_DIRECTORY_PREFIX + journal.transaction_id)
    _remove_stage_files(runtime, journal.entries, stage_directory)


def _remove_stage_files(
    runtime: Path,
    entries: Iterable[_JournalEntry],
    stage_directory: Path,
) -> None:
    for entry in entries:
        stage_path = runtime / entry.stage_file
        try:
            stage_path.unlink()
        except FileNotFoundError:
            pass
    try:
        stage_directory.rmdir()
    except FileNotFoundError:
        pass
    _fsync_directory(runtime)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
