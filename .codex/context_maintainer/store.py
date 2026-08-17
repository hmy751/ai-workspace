"""Locked, atomic filesystem queue for response-end observe events."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import subprocess
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .config import RuntimeConfig
from .protocol import ProtocolError, event_key, validate_queue_event, value_digest


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git_fingerprint(repo_root: Path) -> Dict[str, Any]:
    """Capture a cheap content-free Git/worktree fingerprint."""

    def run(*args: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=2,
        )

    captured_at = utc_now()
    try:
        identity_result = run("rev-parse", "--verify", "HEAD", "--abbrev-ref", "HEAD")
        status_result = run("status", "--porcelain=v1", "-z", "--untracked-files=all")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "captured_at": captured_at,
            "available": False,
            "error": type(exc).__name__,
        }

    if status_result.returncode != 0:
        return {
            "captured_at": captured_at,
            "available": False,
            "error": "git_status_failed",
        }

    raw_status = status_result.stdout
    paths: List[str] = []
    for index, entry in enumerate(raw_status.split(b"\0")):
        if not entry:
            continue
        decoded = entry.decode("utf-8", errors="surrogateescape")
        if len(decoded) >= 4 and decoded[2] == " ":
            decoded = decoded[3:]
        if decoded not in paths:
            paths.append(decoded)

    identity_lines = identity_result.stdout.decode(
        "utf-8", errors="replace"
    ).splitlines()
    head = identity_lines[0] if identity_result.returncode == 0 and identity_lines else None
    branch = identity_lines[1] if len(identity_lines) > 1 else None
    if branch == "HEAD":
        branch = None

    return {
        "captured_at": captured_at,
        "available": True,
        "worktree": str(repo_root),
        "head": head,
        "branch": branch,
        "status_sha256": hashlib.sha256(raw_status).hexdigest(),
        "status_entry_count": len(paths),
        "changed_paths": paths,
    }


class RuntimeStore:
    """All mutations are serialized by one repository-local advisory lock."""

    _DIRS = ("partials", "queue", "inflight", "orphans", "ledger", "sessions")

    def __init__(
        self,
        repo_root: Path,
        config: Optional[RuntimeConfig] = None,
        runtime_root: Optional[Path] = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.config = config or RuntimeConfig.for_repo(self.repo_root)
        self.root = runtime_root or self.config.runtime_root(self.repo_root)
        self.lock_path = self.root / "runtime.lock"
        self.control_path = self.root / "control.json"
        self.cursor_path = self.root / "cursor.json"
        self.diagnostics_path = self.root / "diagnostics.json"

    def ensure_layout(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        for name in self._DIRS:
            (self.root / name).mkdir(exist_ok=True)

    @contextmanager
    def _locked(self, *, shared: bool = False) -> Iterator[None]:
        self.ensure_layout()
        with self.lock_path.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH if shared else fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _read_json(path: Path, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not path.exists():
            if default is None:
                raise ProtocolError(f"runtime file is missing: {path.name}")
            return json.loads(json.dumps(default))
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ProtocolError(f"runtime file is malformed: {path.name}") from exc
        if not isinstance(value, dict):
            raise ProtocolError(f"runtime file is not an object: {path.name}")
        return value

    @staticmethod
    def _atomic_write(path: Path, value: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.parent / f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
        encoded = (json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode(
            "utf-8"
        )
        try:
            with temporary.open("xb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass

    @staticmethod
    def _control_default() -> Dict[str, Any]:
        return {
            "protocol_version": 1,
            "next_sequence": 1,
            "last_enqueued": None,
        }

    @staticmethod
    def _cursor_default() -> Dict[str, Any]:
        return {
            "protocol_version": 1,
            "last_drained_sequence": 0,
            "last_drained_event": None,
            "last_drained_at": None,
        }

    @staticmethod
    def _diagnostics_default() -> Dict[str, Any]:
        return {
            "protocol_version": 1,
            "counts": {
                "duplicate": 0,
                "conflict": 0,
                "malformed": 0,
                "failure": 0,
                "stop_before_user": 0,
            },
            "last": {},
            "seen_tokens": [],
        }

    def _diagnostic_locked(
        self, kind: str, code: str, *, token: Optional[str] = None, key: Optional[str] = None
    ) -> None:
        diagnostics = self._read_json(
            self.diagnostics_path, self._diagnostics_default()
        )
        seen = diagnostics.setdefault("seen_tokens", [])
        if token is not None and token in seen:
            return
        if token is not None:
            seen.append(token)
            del seen[:-100]
        counts = diagnostics.setdefault("counts", {})
        counts[kind] = int(counts.get(kind, 0)) + 1
        detail: Dict[str, Any] = {"at": utc_now(), "code": code}
        if key is not None:
            detail["event_key"] = key
        diagnostics.setdefault("last", {})[kind] = detail
        self._atomic_write(self.diagnostics_path, diagnostics)

    def record_malformed(self, event_name: str, payload: Any, code: str) -> None:
        try:
            digest = value_digest(payload)
        except (TypeError, ValueError):
            digest = hashlib.sha256(type(payload).__name__.encode()).hexdigest()
        key: Optional[str] = None
        if isinstance(payload, dict):
            session_id = payload.get("session_id")
            turn_id = payload.get("turn_id")
            if isinstance(session_id, str) and isinstance(turn_id, str):
                key = event_key(session_id, turn_id)
        with self._locked():
            self._diagnostic_locked(
                "malformed",
                f"{event_name}:{code}",
                token=f"payload:{event_name}:{digest}",
                key=key,
            )

    def record_failure(self, code: str) -> None:
        with self._locked():
            self._diagnostic_locked("failure", code)

    def _ledger_path(self, key: str) -> Path:
        return self.root / "ledger" / f"{key}.json"

    def _orphan_path(self, key: str) -> Path:
        return self.root / "orphans" / f"{key}.json"

    @staticmethod
    def _raw_name(sequence: int, key: str) -> str:
        return f"{sequence:020d}-{key}.json"

    def _next_sequence_locked(self) -> int:
        control = self._read_json(self.control_path, self._control_default())
        sequence = control.get("next_sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
            raise ProtocolError("control next_sequence is invalid")
        return sequence

    def _commit_sequence_locked(self, sequence: int) -> None:
        control = self._read_json(self.control_path, self._control_default())
        next_sequence = control.get("next_sequence")
        if (
            not isinstance(next_sequence, int)
            or isinstance(next_sequence, bool)
            or next_sequence < 1
        ):
            raise ProtocolError("control next_sequence is invalid")
        if next_sequence <= sequence:
            control["next_sequence"] = sequence + 1
            self._atomic_write(self.control_path, control)

    @staticmethod
    def _waiting_ledger(partial: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "schema": "context-maintainer.identity.v1",
            "event_key": partial["event_key"],
            "sequence": partial["sequence"],
            "status": "waiting_stop",
            "prompt_sha256": value_digest(partial["user"]["prompt"]),
            "assistant_sha256": None,
            "first_seen_at": partial["received_at"],
            "updated_at": utc_now(),
        }

    def _mark_conflict_locked(
        self,
        ledger_path: Path,
        ledger: Dict[str, Any],
        *,
        kind: str,
        observed_sha256: str,
        key: str,
    ) -> None:
        ledger["conflict"] = {
            "kind": kind,
            "observed_sha256": observed_sha256,
            "detected_at": utc_now(),
        }
        ledger["updated_at"] = utc_now()
        self._atomic_write(ledger_path, ledger)
        token = f"conflict:{kind}:{key}:{observed_sha256}"
        self._diagnostic_locked(
            "conflict", kind, token=token, key=key
        )
        self._diagnostic_locked(
            "malformed", f"duplicate_{kind}_conflict", token=token + ":malformed", key=key
        )

    def _reconcile_allocations_locked(self) -> None:
        """Finish partial-first sequence commits without inventing missing evidence."""

        partials = sorted((self.root / "partials").glob("*.json"))
        for partial_path in partials:
            try:
                partial = self._read_json(partial_path)
                sequence = partial.get("sequence")
                key = partial.get("event_key")
                identity = partial.get("identity")
                user = partial.get("user")
                prompt = user.get("prompt") if isinstance(user, dict) else None
                session_id = identity.get("session_id") if isinstance(identity, dict) else None
                turn_id = identity.get("turn_id") if isinstance(identity, dict) else None
                if (
                    partial.get("schema") != "context-maintainer.partial.v1"
                    or not isinstance(sequence, int)
                    or isinstance(sequence, bool)
                    or sequence < 1
                    or not isinstance(key, str)
                    or not isinstance(identity, dict)
                    or not isinstance(session_id, str)
                    or not isinstance(turn_id, str)
                    or not isinstance(prompt, str)
                    or event_key(session_id, turn_id) != key
                ):
                    raise ProtocolError("partial allocation is invalid")
            except ProtocolError:
                token = "allocation:" + hashlib.sha256(partial_path.read_bytes()).hexdigest()
                self._diagnostic_locked(
                    "malformed", "partial_allocation", token=token
                )
                continue

            ledger_path = self._ledger_path(key)
            prompt_sha256 = value_digest(prompt)
            if ledger_path.exists():
                ledger = self._read_json(ledger_path)
                if (
                    ledger.get("sequence") != sequence
                    or ledger.get("event_key") != key
                    or ledger.get("prompt_sha256") != prompt_sha256
                ):
                    self._mark_conflict_locked(
                        ledger_path,
                        ledger,
                        kind="prompt",
                        observed_sha256=prompt_sha256,
                        key=key,
                    )
                    continue
            else:
                ledger = self._waiting_ledger(partial)
                self._atomic_write(ledger_path, ledger)

            self._commit_sequence_locked(sequence)
            if ledger.get("conflict") or ledger.get("status") != "waiting_stop":
                continue

            orphan_path = self._orphan_path(key)
            if not orphan_path.exists():
                continue
            orphan = self._read_json(orphan_path)
            if orphan.get("conflict"):
                observed = orphan["conflict"].get("observed_sha256")
                if isinstance(observed, str):
                    self._mark_conflict_locked(
                        ledger_path,
                        ledger,
                        kind="assistant",
                        observed_sha256=observed,
                        key=key,
                    )
                continue
            stop = orphan.get("stop")
            git_post = orphan.get("git_post")
            if not isinstance(stop, dict) or not isinstance(git_post, dict):
                self._diagnostic_locked(
                    "malformed", "stop_orphan", token=f"orphan:{key}", key=key
                )
                continue
            queue_path = self.root / "queue" / self._raw_name(sequence, key)
            if queue_path.exists():
                try:
                    validate_queue_event(
                        self._read_json(queue_path), expected_sequence=sequence
                    )
                except ProtocolError:
                    self._diagnostic_locked(
                        "malformed",
                        "paired_queue",
                        token=f"paired-queue:{sequence}:{key}",
                        key=key,
                    )
                    continue
            else:
                self._atomic_write(
                    queue_path, self._compose_event(partial, stop, git_post)
                )
            ledger = self._ledger(sequence, key, partial, stop, "queued")
            self._atomic_write(ledger_path, ledger)
            partial_path.unlink()
            orphan_path.unlink()
            self._mark_enqueued_locked(sequence, key)

        control = self._read_json(self.control_path, self._control_default())
        cursor = self._read_json(self.cursor_path, self._cursor_default())
        expected = int(cursor.get("last_drained_sequence", 0)) + 1
        next_sequence = control.get("next_sequence")
        if (
            isinstance(next_sequence, int)
            and not isinstance(next_sequence, bool)
            and next_sequence > expected
        ):
            used_sequences = set()
            unreadable_sequence_evidence = False
            for directory_name in ("partials", "queue", "inflight"):
                for path in (self.root / directory_name).glob("*.json"):
                    try:
                        used_sequences.add(int(path.name.split("-", 1)[0]))
                    except ValueError:
                        unreadable_sequence_evidence = True
            for ledger_path in (self.root / "ledger").glob("*.json"):
                try:
                    ledger_sequence = self._read_json(ledger_path).get("sequence")
                except ProtocolError:
                    unreadable_sequence_evidence = True
                    continue
                if isinstance(ledger_sequence, int) and not isinstance(
                    ledger_sequence, bool
                ):
                    used_sequences.add(ledger_sequence)
            last_enqueued = control.get("last_enqueued")
            last_enqueued_sequence = (
                last_enqueued.get("sequence")
                if isinstance(last_enqueued, dict)
                else None
            )
            reserved_range_has_evidence = any(
                expected <= used < next_sequence for used in used_sequences
            ) or (
                isinstance(last_enqueued_sequence, int)
                and expected <= last_enqueued_sequence < next_sequence
            )
            if not reserved_range_has_evidence and not unreadable_sequence_evidence:
                control["next_sequence"] = expected
                self._atomic_write(self.control_path, control)

    def _mark_enqueued_locked(self, sequence: int, key: str) -> None:
        control = self._read_json(self.control_path, self._control_default())
        control["last_enqueued"] = {
            "sequence": sequence,
            "event_key": key,
            "at": utc_now(),
        }
        self._atomic_write(self.control_path, control)

    def accept_session_start(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        session_id = payload["session_id"]
        session_key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:32]
        path = self.root / "sessions" / f"{session_key}.json"
        with self._locked():
            self._reconcile_allocations_locked()
            cursor = self._read_json(self.cursor_path, self._cursor_default())
            self._cleanup_completed_locked(cursor)
            existing = self._read_json(path, {})
            now = utc_now()
            starts = int(existing.get("start_count", 0)) + 1
            compacts = int(existing.get("compact_count", 0))
            if payload["source"] == "compact":
                compacts += 1
            metadata = {
                "schema": "context-maintainer.session.v1",
                "session_id": session_id,
                "first_seen_at": existing.get("first_seen_at", now),
                "last_seen_at": now,
                "latest_source": payload["source"],
                "start_count": starts,
                "compact_count": compacts,
                "cwd": payload.get("cwd"),
                "model": payload.get("model"),
            }
            self._atomic_write(path, metadata)
        return {"recorded": True, "source": payload["source"]}

    def accept_user_prompt(
        self, payload: Dict[str, Any], fingerprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        key = event_key(payload["session_id"], payload["turn_id"])
        ledger_path = self._ledger_path(key)
        with self._locked():
            self._reconcile_allocations_locked()
            if ledger_path.exists():
                ledger = self._read_json(ledger_path)
                prompt_sha256 = value_digest(payload["prompt"])
                if ledger.get("conflict"):
                    return {
                        "event_key": key,
                        "sequence": ledger.get("sequence"),
                        "conflict": True,
                    }
                if ledger.get("prompt_sha256") != prompt_sha256:
                    self._mark_conflict_locked(
                        ledger_path,
                        ledger,
                        kind="prompt",
                        observed_sha256=prompt_sha256,
                        key=key,
                    )
                    return {
                        "event_key": key,
                        "sequence": ledger.get("sequence"),
                        "conflict": True,
                    }
                self._diagnostic_locked("duplicate", "user_prompt", key=key)
                return {
                    "event_key": key,
                    "sequence": ledger.get("sequence"),
                    "duplicate": True,
                }

            sequence = self._next_sequence_locked()
            received_at = utc_now()
            partial = {
                "schema": "context-maintainer.partial.v1",
                "sequence": sequence,
                "event_key": key,
                "identity": {
                    "session_id": payload["session_id"],
                    "turn_id": payload["turn_id"],
                },
                "user": {"prompt": payload["prompt"]},
                "git": {"pre_turn": fingerprint},
                "received_at": received_at,
            }
            partial_path = self.root / "partials" / self._raw_name(sequence, key)
            self._atomic_write(partial_path, partial)
            self._atomic_write(ledger_path, self._waiting_ledger(partial))
            self._commit_sequence_locked(sequence)
            self._reconcile_allocations_locked()
            ledger = self._read_json(ledger_path)
            return {
                "event_key": key,
                "sequence": sequence,
                "paired": ledger.get("status") == "queued",
                "conflict": bool(ledger.get("conflict")),
            }

    def accept_stop(
        self, payload: Dict[str, Any], fingerprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        key = event_key(payload["session_id"], payload["turn_id"])
        ledger_path = self._ledger_path(key)
        with self._locked():
            self._reconcile_allocations_locked()
            if not ledger_path.exists():
                orphan_path = self._orphan_path(key)
                if orphan_path.exists():
                    orphan = self._read_json(orphan_path)
                    if orphan.get("conflict"):
                        return {"event_key": key, "conflict": True, "paired": False}
                    original_sha256 = value_digest(
                        orphan.get("stop", {}).get("last_assistant_message")
                    )
                    observed_sha256 = value_digest(payload["last_assistant_message"])
                    if original_sha256 != observed_sha256:
                        orphan["conflict"] = {
                            "kind": "assistant",
                            "observed_sha256": observed_sha256,
                            "detected_at": utc_now(),
                        }
                        self._atomic_write(orphan_path, orphan)
                        token = f"conflict:assistant:{key}:{observed_sha256}"
                        self._diagnostic_locked(
                            "conflict", "assistant", token=token, key=key
                        )
                        self._diagnostic_locked(
                            "malformed",
                            "duplicate_assistant_conflict",
                            token=token + ":malformed",
                            key=key,
                        )
                        return {"event_key": key, "conflict": True, "paired": False}
                    self._diagnostic_locked("duplicate", "stop_orphan", key=key)
                    return {"event_key": key, "duplicate": True, "paired": False}
                self._atomic_write(
                    orphan_path,
                    {
                        "schema": "context-maintainer.stop-orphan.v1",
                        "event_key": key,
                        "stop": payload,
                        "git_post": fingerprint,
                        "received_at": utc_now(),
                    },
                )
                self._diagnostic_locked("stop_before_user", "missing_user", key=key)
                return {"event_key": key, "stop_before_user": True, "paired": False}

            ledger = self._read_json(ledger_path)
            observed_sha256 = value_digest(payload["last_assistant_message"])
            if ledger.get("conflict"):
                return {
                    "event_key": key,
                    "sequence": ledger.get("sequence"),
                    "conflict": True,
                }
            if ledger.get("status") in {"queued", "drained"}:
                if ledger.get("assistant_sha256") != observed_sha256:
                    self._mark_conflict_locked(
                        ledger_path,
                        ledger,
                        kind="assistant",
                        observed_sha256=observed_sha256,
                        key=key,
                    )
                    return {
                        "event_key": key,
                        "sequence": ledger.get("sequence"),
                        "conflict": True,
                    }
                self._diagnostic_locked("duplicate", "stop", key=key)
                return {
                    "event_key": key,
                    "sequence": ledger.get("sequence"),
                    "duplicate": True,
                }
            sequence = ledger.get("sequence")
            if not isinstance(sequence, int) or sequence < 1:
                self._diagnostic_locked("malformed", "ledger_sequence", key=key)
                return {"event_key": key, "malformed": True}
            partial_path = self.root / "partials" / self._raw_name(sequence, key)
            try:
                partial = self._read_json(partial_path)
            except ProtocolError:
                self._diagnostic_locked(
                    "malformed",
                    "partial_missing_or_invalid",
                    token=f"partial:{sequence}:{key}",
                    key=key,
                )
                ledger["status"] = "malformed"
                ledger["updated_at"] = utc_now()
                self._atomic_write(ledger_path, ledger)
                return {"event_key": key, "sequence": sequence, "malformed": True}

            final = self._compose_event(partial, payload, fingerprint)
            queue_path = self.root / "queue" / self._raw_name(sequence, key)
            self._atomic_write(queue_path, final)
            self._atomic_write(
                ledger_path, self._ledger(sequence, key, partial, payload, "queued")
            )
            partial_path.unlink()
            self._mark_enqueued_locked(sequence, key)
            return {"event_key": key, "sequence": sequence, "paired": True}

    def _compose_event(
        self,
        partial: Dict[str, Any],
        stop: Dict[str, Any],
        post_fingerprint: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "schema": "context-maintainer.response-end.v1",
            "protocol_version": self.config.protocol_version,
            "mode": self.config.mode,
            "workspace": {
                "id": self.config.workspace,
                "path": self.config.workspace_path,
            },
            "sequence": partial["sequence"],
            "event_key": partial["event_key"],
            "identity": partial["identity"],
            "user": partial["user"],
            "assistant": {
                "message": stop["last_assistant_message"],
                "stop_hook_active": stop["stop_hook_active"],
            },
            "git": {
                "pre_turn": partial["git"]["pre_turn"],
                "post_turn": post_fingerprint,
            },
            "timestamps": {
                "user_prompt_received_at": partial["received_at"],
                "stop_received_at": utc_now(),
                "enqueued_at": utc_now(),
            },
        }

    @staticmethod
    def _ledger(
        sequence: int,
        key: str,
        partial: Dict[str, Any],
        stop: Dict[str, Any],
        status: str,
    ) -> Dict[str, Any]:
        return {
            "schema": "context-maintainer.identity.v1",
            "event_key": key,
            "sequence": sequence,
            "status": status,
            "prompt_sha256": value_digest(partial["user"]["prompt"]),
            "assistant_sha256": value_digest(stop["last_assistant_message"]),
            "first_seen_at": partial["received_at"],
            "updated_at": utc_now(),
        }

    def drain(self, *, once: bool = False) -> Dict[str, Any]:
        processed = 0
        blocked: Optional[str] = None
        with self._locked():
            self._reconcile_allocations_locked()
            cursor = self._read_json(self.cursor_path, self._cursor_default())
            self._cleanup_completed_locked(cursor)
            while True:
                expected = int(cursor.get("last_drained_sequence", 0)) + 1
                queued = sorted(
                    (self.root / "queue").glob(f"{expected:020d}-*.json")
                )
                inflight = sorted(
                    (self.root / "inflight").glob(f"{expected:020d}-*.json")
                )
                candidates = queued + inflight
                if len(candidates) != 1:
                    control = self._read_json(self.control_path, self._control_default())
                    assigned = int(control.get("next_sequence", 1)) - 1
                    if assigned >= expected:
                        blocked = "gap"
                    break
                event_path = candidates[0]
                try:
                    event = validate_queue_event(
                        self._read_json(event_path), expected_sequence=expected
                    )
                except ProtocolError:
                    token = "queue:" + hashlib.sha256(event_path.read_bytes()).hexdigest()
                    self._diagnostic_locked(
                        "malformed", "queue_event", token=token
                    )
                    blocked = "malformed"
                    break

                ledger_path = self._ledger_path(event["event_key"])
                try:
                    ledger = (
                        self._read_json(ledger_path) if ledger_path.exists() else None
                    )
                except ProtocolError:
                    self._diagnostic_locked(
                        "malformed",
                        "queue_ledger",
                        token=f"queue-ledger:{expected}:{event['event_key']}",
                        key=event["event_key"],
                    )
                    blocked = "malformed"
                    break
                if ledger is not None and (
                    ledger.get("event_key") != event["event_key"]
                    or ledger.get("sequence") != expected
                ):
                    self._diagnostic_locked(
                        "malformed",
                        "queue_ledger_identity",
                        token=f"queue-ledger-identity:{expected}:{event['event_key']}",
                        key=event["event_key"],
                    )
                    blocked = "malformed"
                    break
                if ledger is not None and ledger.get("conflict"):
                    blocked = "conflict"
                    break
                if ledger is None:
                    ledger = {
                        "schema": "context-maintainer.identity.v1",
                        "event_key": event["event_key"],
                        "sequence": expected,
                        "status": "queued",
                        "prompt_sha256": value_digest(event["user"]["prompt"]),
                        "assistant_sha256": value_digest(
                            event["assistant"]["message"]
                        ),
                        "first_seen_at": event["timestamps"].get(
                            "user_prompt_received_at", utc_now()
                        ),
                        "updated_at": utc_now(),
                        "reconstructed_from_queue": True,
                    }
                    self._atomic_write(ledger_path, ledger)

                if event_path.parent.name == "queue":
                    inflight_path = self.root / "inflight" / event_path.name
                    os.replace(event_path, inflight_path)
                    event_path = inflight_path

                previous = int(cursor.get("last_drained_sequence", 0))
                if expected != previous + 1:
                    blocked = "gap"
                    break
                cursor = {
                    "protocol_version": 1,
                    "last_drained_sequence": expected,
                    "last_drained_event": event["event_key"],
                    "last_drained_at": utc_now(),
                }
                self._atomic_write(self.cursor_path, cursor)
                ledger["status"] = "drained"
                ledger["updated_at"] = utc_now()
                ledger["drained_at"] = cursor["last_drained_at"]
                self._atomic_write(ledger_path, ledger)
                event_path.unlink()
                self._cleanup_completed_locked(cursor)
                processed += 1
                if once:
                    break

        return {
            "mode": self.config.mode,
            "workspace": self.config.workspace,
            "processed": processed,
            "blocked": blocked,
            "last_drained": cursor.get("last_drained_sequence", 0),
        }

    def _cleanup_completed_locked(self, cursor: Dict[str, Any]) -> None:
        """Remove raw residue only when cursor or ledger already proves completion."""

        completed = int(cursor.get("last_drained_sequence", 0))

        def complete_event_exists(sequence: int, key: str) -> bool:
            candidates: List[Path] = []
            for directory_name in ("queue", "inflight"):
                candidates.extend(
                    (self.root / directory_name).glob(self._raw_name(sequence, key))
                )
            if len(candidates) != 1:
                return False
            try:
                event = validate_queue_event(
                    self._read_json(candidates[0]), expected_sequence=sequence
                )
            except ProtocolError:
                return False
            return event.get("event_key") == key

        for directory_name in ("queue", "inflight"):
            for path in (self.root / directory_name).glob("*.json"):
                try:
                    sequence = int(path.name.split("-", 1)[0])
                except ValueError:
                    continue
                if sequence > completed:
                    continue
                key = path.stem.split("-", 1)[1] if "-" in path.stem else None
                if key:
                    ledger_path = self._ledger_path(key)
                    if ledger_path.exists():
                        try:
                            ledger = self._read_json(ledger_path)
                        except ProtocolError:
                            self._diagnostic_locked(
                                "malformed",
                                "completed_ledger",
                                token=f"completed-ledger:{sequence}:{key}",
                                key=key,
                            )
                        else:
                            if ledger.get("status") != "abandoned":
                                ledger["status"] = "drained"
                            ledger["updated_at"] = utc_now()
                            ledger.setdefault(
                                "drained_at", cursor.get("last_drained_at")
                            )
                            self._atomic_write(ledger_path, ledger)
                    orphan_path = self._orphan_path(key)
                    if orphan_path.exists():
                        orphan_path.unlink()
                path.unlink()

        completed_key = cursor.get("last_drained_event")
        if completed >= 1 and isinstance(completed_key, str):
            completed_orphan = self._orphan_path(completed_key)
            if completed_orphan.exists():
                completed_orphan.unlink()

        for partial_path in (self.root / "partials").glob("*.json"):
            name_parts = partial_path.stem.split("-", 1)
            if len(name_parts) != 2:
                continue
            try:
                sequence = int(name_parts[0])
            except ValueError:
                continue
            key = name_parts[1]
            ledger_path = self._ledger_path(key)
            if sequence <= completed:
                partial_path.unlink()
                continue
            if not ledger_path.exists():
                continue
            try:
                ledger = self._read_json(ledger_path)
            except ProtocolError:
                continue
            status = ledger.get("status")
            ledger_proves_completion = status in {"drained", "abandoned"}
            queued_event_is_durable = status == "queued" and complete_event_exists(
                sequence, key
            )
            if ledger.get("sequence") == sequence and (
                ledger_proves_completion or queued_event_is_durable
            ):
                partial_path.unlink()

        for orphan_path in (self.root / "orphans").glob("*.json"):
            key = orphan_path.stem
            ledger_path = self._ledger_path(key)
            if not ledger_path.exists():
                continue
            try:
                ledger = self._read_json(ledger_path)
            except ProtocolError:
                continue
            sequence = ledger.get("sequence")
            if not isinstance(sequence, int) or isinstance(sequence, bool):
                continue
            status = ledger.get("status")
            ledger_proves_completion = status in {"drained", "abandoned"}
            queued_event_is_durable = status == "queued" and complete_event_exists(
                sequence, key
            )
            if sequence <= completed or ledger_proves_completion or queued_event_is_durable:
                orphan_path.unlink()

    def status(self) -> Dict[str, Any]:
        with self._locked():
            reconcile_error = False
            try:
                self._reconcile_allocations_locked()
            except ProtocolError:
                reconcile_error = True
            control_error: Optional[str] = None
            cursor_error: Optional[str] = None
            try:
                control = self._read_json(self.control_path, self._control_default())
            except ProtocolError:
                control = self._control_default()
                control_error = "control"
            try:
                cursor = self._read_json(self.cursor_path, self._cursor_default())
            except ProtocolError:
                cursor = self._cursor_default()
                cursor_error = "cursor"
            if cursor_error is None:
                self._cleanup_completed_locked(cursor)
            try:
                diagnostics = self._read_json(
                    self.diagnostics_path, self._diagnostics_default()
                )
            except ProtocolError:
                diagnostics = self._diagnostics_default()
                diagnostics["counts"]["malformed"] = 1

            queue_files = sorted((self.root / "queue").glob("*.json")) + sorted(
                (self.root / "inflight").glob("*.json")
            )
            partial_files = sorted((self.root / "partials").glob("*.json"))
            orphan_files = sorted((self.root / "orphans").glob("*.json"))
            malformed_current = (
                int(control_error is not None)
                + int(cursor_error is not None)
                + int(reconcile_error)
            )
            sequences: List[int] = []
            oldest_timestamp: Optional[float] = None
            for path in queue_files:
                try:
                    sequence = int(path.name.split("-", 1)[0])
                    validate_queue_event(self._read_json(path), expected_sequence=sequence)
                    sequences.append(sequence)
                except (ProtocolError, ValueError):
                    malformed_current += 1
                stamp = path.stat().st_mtime
                oldest_timestamp = stamp if oldest_timestamp is None else min(
                    oldest_timestamp, stamp
                )

            last_drained = int(cursor.get("last_drained_sequence", 0))
            expected = last_drained + 1
            assigned = int(control.get("next_sequence", 1)) - 1
            gap_present = assigned >= expected and expected not in sequences
            next_available = min((seq for seq in sequences if seq > expected), default=None)
            counts = diagnostics.get("counts", {})
            conflict_keys = set()
            for ledger_path in (self.root / "ledger").glob("*.json"):
                try:
                    ledger_value = self._read_json(ledger_path)
                    if ledger_value.get("conflict"):
                        conflict_keys.add(ledger_value.get("event_key", ledger_path.stem))
                except ProtocolError:
                    malformed_current += 1
            for orphan_path in orphan_files:
                try:
                    if self._read_json(orphan_path).get("conflict"):
                        conflict_keys.add(orphan_path.stem)
                except ProtocolError:
                    malformed_current += 1
            session_count = len(list((self.root / "sessions").glob("*.json")))
            compact_count = 0
            for path in (self.root / "sessions").glob("*.json"):
                try:
                    compact_count += int(self._read_json(path).get("compact_count", 0))
                except ProtocolError:
                    malformed_current += 1

            return {
                "protocol_version": 1,
                "mode": self.config.mode,
                "workspace": {
                    "id": self.config.workspace,
                    "path": self.config.workspace_path,
                },
                "last_enqueued": control.get("last_enqueued"),
                "last_drained": {
                    "sequence": last_drained,
                    "event_key": cursor.get("last_drained_event"),
                    "at": cursor.get("last_drained_at"),
                },
                "queue": {
                    "count": len(queue_files),
                    "oldest_age_seconds": (
                        round(max(0.0, time.time() - oldest_timestamp), 3)
                        if oldest_timestamp is not None
                        else None
                    ),
                },
                "missing_pair": {
                    "count": len(partial_files) + len(orphan_files),
                    "waiting_stop": len(partial_files),
                    "stop_before_user": len(orphan_files),
                },
                "gap": {
                    "present": gap_present,
                    "expected_sequence": expected if gap_present else None,
                    "next_available_sequence": next_available,
                },
                "malformed": {
                    "total": int(counts.get("malformed", 0)),
                    "current": malformed_current,
                },
                "duplicate": {"total": int(counts.get("duplicate", 0))},
                "conflict": {
                    "total": int(counts.get("conflict", 0)),
                    "current": len(conflict_keys),
                },
                "failure": {"total": int(counts.get("failure", 0))},
                "stop_before_user": {
                    "total": int(counts.get("stop_before_user", 0)),
                    "unresolved": len(orphan_files),
                },
                "sessions": {"count": session_count, "compact_count": compact_count},
                "proof_ceiling": {
                    "queue_scope": "repo_worktree_global",
                    "cross_session_gap_isolation": False,
                    "manual_gap_recovery": False,
                },
            }
