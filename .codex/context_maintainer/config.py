"""Static configuration for the Workspace 005 dogfood runtime."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class RuntimeConfig:
    """The v1 runtime is deliberately fixed to one workspace and observe mode."""

    mode: str = "observe"
    workspace: str = "005-context-continuity-maintenance"
    workspace_path: str = "context/workspaces/005-context-continuity-maintenance"
    protocol_version: int = 1
    runtime_path: str = ".context-harness/runtime/context-maintainer/v1"

    @classmethod
    def for_repo(cls, repo_root: Path) -> "RuntimeConfig":
        config_path = Path(__file__).with_name("config.json")
        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
            workspace = raw["workspace"]
            config = cls(
                mode=raw["mode"],
                workspace=workspace["id"],
                workspace_path=workspace["path"],
                protocol_version=raw["protocol_version"],
                runtime_path=raw["runtime_path"],
            )
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError("context maintainer config.json is invalid") from exc
        if config.mode != "observe" or config.protocol_version != 1:
            raise RuntimeError("v1 context maintainer must use observe mode")
        if config.workspace != "005-context-continuity-maintenance":
            raise RuntimeError("v1 context maintainer is restricted to Workspace 005")
        if config.runtime_path != ".context-harness/runtime/context-maintainer/v1":
            raise RuntimeError("v1 context maintainer runtime path is invalid")
        workspace = repo_root / config.workspace_path
        if not workspace.is_dir():
            raise RuntimeError(f"configured workspace is missing: {workspace}")
        return config

    def runtime_root(self, repo_root: Path) -> Path:
        return repo_root / self.runtime_path
