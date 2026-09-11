"""Prepare a phase-05 fixture for the narrowed third Maintain replay."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve().parents[7] / "reference-project"
SETUP_V2 = json.loads((OUT / "setup-v2.json").read_text())
FROM_PROJECT = Path(SETUP_V2["project"])
PROJECT = Path("/private/tmp/maintainer-material-eval-20260911/run03-project")
WORKSPACE = SETUP_V2["workspace_id"]
RELATIVE_WS = Path("context/work/workspaces") / WORKSPACE
PHASE_FIVE = OUT / "run02/05-coverage-explanation"
OVERLAYS = [
    "context/work/harness/maintain/README.md",
    "context/work/harness/maintain/workspace-context-maintainer.toml",
    "context/work/harness/maintain/codex_session.py",
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def replace(value):
    if isinstance(value, str):
        return value.replace(str(FROM_PROJECT), str(PROJECT))
    if isinstance(value, list):
        return [replace(item) for item in value]
    if isinstance(value, dict):
        return {key: replace(item) for key, item in value.items()}
    return value


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    if PROJECT.exists():
        raise RuntimeError("Refusing to overwrite an existing targeted fixture")
    shutil.copytree(FROM_PROJECT, PROJECT, symlinks=True)
    workspace = PROJECT / RELATIVE_WS
    shutil.rmtree(workspace / "current")
    shutil.rmtree(workspace / "records")
    shutil.copytree(PHASE_FIVE / "current", workspace / "current")
    shutil.copytree(PHASE_FIVE / "records", workspace / "records")

    overlays = {}
    for relative in OVERLAYS:
        source = SOURCE / relative
        target = PROJECT / relative
        shutil.copy2(source, target)
        overlays[relative] = digest(source.read_bytes())

    exchange = PROJECT / "eval-inputs"
    for path in exchange.iterdir():
        if path.is_file():
            path.write_text(path.read_text().replace(str(FROM_PROJECT), str(PROJECT)))

    cases = replace(json.loads((OUT / "cases-v2.json").read_text())[-3:])
    dump(OUT / "cases-v3.json", cases)
    manifest = {
        str(path.relative_to(PROJECT)): digest(path.read_bytes())
        for path in sorted(PROJECT.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(PROJECT).parts
    }
    dump(OUT / "fixture-manifest-v3.json", manifest)
    dump(OUT / "setup-v3.json", {
        **replace(SETUP_V2),
        "project": str(PROJECT),
        "revised_reference_overlays": overlays,
        "starting_state": "run02 after 05-coverage-explanation",
        "comparison_run": "run02",
    })
    print(json.dumps({
        "fixture": str(PROJECT), "cases": len(cases),
        "files": len(manifest), "overlays": overlays,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
