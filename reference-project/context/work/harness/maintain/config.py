"""Strict, repo-local configuration for the Maintain runtime adapter.

The configuration file must live below the target Project's ``.codex/``
directory.  The directory containing that ``.codex/`` directory is therefore
the target Project root; callers cannot point a reusable Reference adapter at
an unrelated repository with a second root field.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Mapping


CONFIG_SCHEMA_NAME = "context-maintain.config.v1"
DEFAULT_CODEX_EXECUTABLE = "codex"
WORKSPACE_MACHINE_BINDING_ENTRYPOINTS = (
    PurePosixPath("README.md"),
    PurePosixPath("current/memory/index.md"),
    PurePosixPath("current/memory/01-goal.md"),
    PurePosixPath("current/state/index.md"),
    PurePosixPath("output/index.md"),
)
WORKSPACE_FLAT_BINDING_ENTRYPOINTS = (
    PurePosixPath("README.md"),
    PurePosixPath("current/index.md"),
    PurePosixPath("current/memory.md"),
    PurePosixPath("current/state.md"),
    PurePosixPath("output/index.md"),
)
WORKSPACE_BINDING_ENTRYPOINTS = tuple(
    dict.fromkeys(
        WORKSPACE_MACHINE_BINDING_ENTRYPOINTS
        + WORKSPACE_FLAT_BINDING_ENTRYPOINTS
    )
)

# Kept next to the parser so the optional executable default and the
# read-only-only sandbox contract cannot drift apart.
CONFIG_JSON_SCHEMA: Mapping[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema",
        "workspace_id",
        "work_root",
        "maintain_contract_path",
        "runtime_root",
        "sandbox",
    ],
    "properties": {
        "schema": {"const": CONFIG_SCHEMA_NAME},
        "workspace_id": {
            "type": "string",
            "pattern": "^[a-z0-9][a-z0-9._-]*$",
        },
        "work_root": {"type": "string", "minLength": 1},
        "maintain_contract_path": {"type": "string", "minLength": 1},
        "runtime_root": {"type": "string", "minLength": 1},
        "codex_executable": {
            "type": "string",
            "minLength": 1,
            "default": DEFAULT_CODEX_EXECUTABLE,
        },
        "sandbox": {"const": "read-only"},
    },
}

_WORKSPACE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
_REQUIRED_FIELDS = frozenset(CONFIG_JSON_SCHEMA["required"])
_ALLOWED_FIELDS = frozenset(CONFIG_JSON_SCHEMA["properties"])


class MaintainConfigError(ValueError):
    """The adapter configuration cannot safely select one target Workspace."""


@dataclass(frozen=True)
class MaintainConfig:
    """Validated absolute paths plus prompt-safe Project-relative paths."""

    config_path: Path
    project_root: Path
    workspace_id: str
    work_root: Path
    workspace_root: Path
    maintain_contract_path: Path
    runtime_root: Path
    codex_executable: str = DEFAULT_CODEX_EXECUTABLE
    sandbox: str = "read-only"

    @property
    def workspace_relative_path(self) -> str:
        return self.workspace_root.relative_to(self.project_root).as_posix()

    @property
    def maintain_contract_relative_path(self) -> str:
        return self.maintain_contract_path.relative_to(
            self.project_root
        ).as_posix()

    @property
    def workspace_bound(self) -> bool:
        """Whether identity/current/output Owners now exist for this Workspace.

        This is evaluated on access rather than frozen at config-load time so a
        Main task can form an explicitly named Workspace during the session.
        Maintain may follow that conversation while this is false, but it must
        not create or write the Workspace on the user's behalf.
        """

        return _workspace_bound(self.workspace_root, self.workspace_id)

    @classmethod
    def load(cls, path: str | Path) -> "MaintainConfig":
        return load_config(path)


def load_config(path: str | Path) -> MaintainConfig:
    """Load schema v1 without accepting coercion, extras, or path escape."""

    config_path = Path(path).expanduser()
    if config_path.is_symlink():
        raise MaintainConfigError("Maintain config must not be a symlink")
    try:
        config_path = config_path.resolve(strict=True)
    except FileNotFoundError as error:
        raise MaintainConfigError("Maintain config does not exist") from error
    if not config_path.is_file():
        raise MaintainConfigError("Maintain config must be a regular file")

    codex_directory = next(
        (parent for parent in config_path.parents if parent.name == ".codex"),
        None,
    )
    if codex_directory is None:
        raise MaintainConfigError(
            "Maintain config must live below the target Project .codex directory"
        )
    if codex_directory.is_symlink():
        raise MaintainConfigError("the target Project .codex directory is a symlink")
    project_root = codex_directory.parent.resolve(strict=True)

    try:
        value = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise MaintainConfigError("Maintain config is not valid UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise MaintainConfigError("Maintain config must be a JSON object")

    actual = frozenset(value)
    missing = sorted(_REQUIRED_FIELDS - actual)
    extra = sorted(actual - _ALLOWED_FIELDS)
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append("missing fields: " + ", ".join(missing))
        if extra:
            details.append("unexpected fields: " + ", ".join(extra))
        raise MaintainConfigError("invalid Maintain config (" + "; ".join(details) + ")")

    if value.get("schema") != CONFIG_SCHEMA_NAME:
        raise MaintainConfigError(f"schema must be {CONFIG_SCHEMA_NAME!r}")
    workspace_id = _required_string(value, "workspace_id")
    if not _WORKSPACE_ID_PATTERN.fullmatch(workspace_id) or workspace_id in {
        ".",
        "..",
    }:
        raise MaintainConfigError(
            "workspace_id must use lowercase safe path characters"
        )

    work_relative = _relative_path(value, "work_root")
    contract_relative = _relative_path(value, "maintain_contract_path")
    runtime_relative = _relative_path(value, "runtime_root")

    work_root = _project_path(
        project_root, work_relative, label="work_root", require="directory"
    )
    workspace_root = _project_path(
        project_root,
        work_relative / "workspaces" / workspace_id,
        label="workspace path",
        require=None,
    )
    maintain_contract_path = _project_path(
        project_root,
        contract_relative,
        label="maintain_contract_path",
        require="file",
    )
    runtime_root = _project_path(
        project_root, runtime_relative, label="runtime_root", require=None
    )

    sandbox = _required_string(value, "sandbox")
    if sandbox != "read-only":
        raise MaintainConfigError("sandbox must be exactly 'read-only'")
    codex_executable_value = value.get(
        "codex_executable", DEFAULT_CODEX_EXECUTABLE
    )
    if (
        not isinstance(codex_executable_value, str)
        or not codex_executable_value.strip()
        or "\x00" in codex_executable_value
    ):
        raise MaintainConfigError("codex_executable must be a non-blank string")

    return MaintainConfig(
        config_path=config_path,
        project_root=project_root,
        workspace_id=workspace_id,
        work_root=work_root,
        workspace_root=workspace_root,
        maintain_contract_path=maintain_contract_path,
        runtime_root=runtime_root,
        codex_executable=codex_executable_value,
        sandbox=sandbox,
    )


def _required_string(value: Mapping[str, Any], field: str) -> str:
    candidate = value.get(field)
    if not isinstance(candidate, str) or not candidate.strip():
        raise MaintainConfigError(f"{field} must be a non-blank string")
    if "\x00" in candidate:
        raise MaintainConfigError(f"{field} must not contain NUL")
    return candidate


def _relative_path(value: Mapping[str, Any], field: str) -> PurePosixPath:
    raw = _required_string(value, field)
    if "\\" in raw:
        raise MaintainConfigError(f"{field} must use normalized POSIX separators")
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or path.parts in {(), (".",)}
        or ".." in path.parts
        or path.as_posix() != raw
    ):
        raise MaintainConfigError(f"{field} must be a normalized Project-relative path")
    return path


def _project_path(
    project_root: Path,
    relative: PurePosixPath,
    *,
    label: str,
    require: str | None,
) -> Path:
    candidate = project_root.joinpath(*relative.parts)
    current = project_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise MaintainConfigError(f"{label} must not cross a symlink")
        if not current.exists():
            break

    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(project_root)
    except ValueError as error:
        raise MaintainConfigError(f"{label} escapes the target Project") from error

    if require == "directory" and not resolved.is_dir():
        raise MaintainConfigError(f"{label} must be an existing directory")
    if require == "file" and not resolved.is_file():
        raise MaintainConfigError(f"{label} must be an existing regular file")
    if require is None and resolved.exists() and not resolved.is_dir():
        raise MaintainConfigError(f"{label} must be a directory or absent")
    return resolved


def _workspace_bound(workspace_root: Path, workspace_id: str) -> bool:
    if workspace_root.is_symlink():
        raise MaintainConfigError("workspace path must not be a symlink")
    if not workspace_root.exists():
        return False
    if not workspace_root.is_dir():
        raise MaintainConfigError("workspace path must be a directory or absent")

    identity_path = workspace_root / "workspace.json"
    if identity_path.is_symlink():
        raise MaintainConfigError(
            "Workspace machine identity must not be a symlink"
        )
    if identity_path.exists():
        return _machine_workspace_bound(
            workspace_root, workspace_id, identity_path
        )
    return _flat_workspace_bound(workspace_root)


def _machine_workspace_bound(
    workspace_root: Path,
    workspace_id: str,
    identity_path: Path,
) -> bool:
    if not identity_path.is_file():
        raise MaintainConfigError(
            "Workspace machine identity must be a regular file"
        )
    try:
        identity = json.loads(identity_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise MaintainConfigError(
            "Workspace machine identity is not valid UTF-8 JSON"
        ) from error
    if not isinstance(identity, dict) or set(identity) != {
        "schema_version",
        "workspace_id",
    }:
        raise MaintainConfigError(
            "Workspace machine identity must contain only schema_version "
            "and workspace_id"
        )
    if type(identity.get("schema_version")) is not int or identity[
        "schema_version"
    ] != 1:
        raise MaintainConfigError(
            "Workspace machine identity schema_version must be 1"
        )
    if identity.get("workspace_id") != workspace_id:
        raise MaintainConfigError(
            "Workspace machine identity does not match configured workspace_id"
        )

    documents = _binding_documents(
        workspace_root, WORKSPACE_MACHINE_BINDING_ENTRYPOINTS
    )
    if documents is None:
        return False
    memory_index = documents[PurePosixPath("current/memory/index.md")]
    return _has_direct_local_link(memory_index, "01-goal.md")


def _flat_workspace_bound(workspace_root: Path) -> bool:
    documents = _binding_documents(
        workspace_root, WORKSPACE_FLAT_BINDING_ENTRYPOINTS
    )
    if documents is None:
        return False
    current_index = documents[PurePosixPath("current/index.md")]
    return _has_direct_local_link(
        current_index, "memory.md"
    ) and _has_direct_local_link(current_index, "state.md")


def _binding_documents(
    workspace_root: Path,
    entrypoints: tuple[PurePosixPath, ...],
) -> dict[PurePosixPath, str] | None:
    documents: dict[PurePosixPath, str] = {}
    for relative in entrypoints:
        current = workspace_root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise MaintainConfigError(
                    "Workspace binding entrypoints must not cross a symlink"
                )
        if not current.exists():
            return None
        if not current.is_file():
            raise MaintainConfigError(
                "Workspace binding entrypoints must be regular files"
            )
        try:
            content = current.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise MaintainConfigError(
                "Workspace binding entrypoints must be readable UTF-8"
            ) from error
        if not content.strip():
            return None
        documents[relative] = content
    return documents


_MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _has_direct_local_link(content: str, filename: str) -> bool:
    """Accept a direct sibling Markdown link, never a guessed Owner path."""
    for match in _MARKDOWN_LINK.finditer(content):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        target = target.split("#", 1)[0]
        if target in {filename, f"./{filename}"}:
            return True
    return False


__all__ = [
    "CONFIG_JSON_SCHEMA",
    "CONFIG_SCHEMA_NAME",
    "DEFAULT_CODEX_EXECUTABLE",
    "WORKSPACE_BINDING_ENTRYPOINTS",
    "WORKSPACE_FLAT_BINDING_ENTRYPOINTS",
    "WORKSPACE_MACHINE_BINDING_ENTRYPOINTS",
    "MaintainConfig",
    "MaintainConfigError",
    "load_config",
]
