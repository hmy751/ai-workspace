"""Prepare the frozen Noline fixture with the revised Reference Maintain files."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve().parents[7] / 'reference-project'
OLD_SETUP = json.loads((OUT / 'setup.json').read_text())
OLD_PROJECT = Path(OLD_SETUP['project'])
PROJECT = Path('/private/tmp/maintainer-material-eval-20260911/run02-project')
WORKSPACE = OLD_SETUP['workspace_id']
OVERLAYS = [
    'context/work/harness/maintain/README.md',
    'context/work/harness/maintain/workspace-context-maintainer.toml',
    'context/work/harness/maintain/codex_session.py',
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def replace(value):
    if isinstance(value, str):
        return value.replace(str(OLD_PROJECT), str(PROJECT))
    if isinstance(value, list):
        return [replace(item) for item in value]
    if isinstance(value, dict):
        return {key: replace(item) for key, item in value.items()}
    return value


def main():
    if PROJECT.exists():
        raise RuntimeError('Refusing to overwrite an existing retest fixture')
    PROJECT.mkdir(parents=True)
    with tarfile.open(OUT / 'baseline.tar') as archive:
        archive.extractall(PROJECT, filter='data')
    subprocess.run(['git', 'init', '-q', str(PROJECT)], check=True)
    overlays = {}
    for relative in OVERLAYS:
        source = SOURCE / relative
        target = PROJECT / relative
        shutil.copy2(source, target)
        overlays[relative] = digest(source.read_bytes())

    sys.path.insert(0, str(PROJECT))
    from context.work.harness.maintain.operation import apply_maintain_decision
    predecision = json.loads((OUT / 'prebaseline-decision.json').read_text())
    preapply = apply_maintain_decision(
        PROJECT, PROJECT / 'context/work', WORKSPACE, predecision
    )
    assert preapply['context_status'] == 'updated'

    exchange = PROJECT / 'eval-inputs'
    exchange.mkdir()
    for source in (OLD_PROJECT / 'eval-inputs').iterdir():
        (exchange / source.name).write_text(
            source.read_text().replace(str(OLD_PROJECT), str(PROJECT))
        )
    cases = replace(json.loads((OUT / 'cases.json').read_text()))
    dump(OUT / 'cases-v2.json', cases)
    manifest = {
        str(path.relative_to(PROJECT)): digest(path.read_bytes())
        for path in sorted(PROJECT.rglob('*'))
        if path.is_file() and '.git' not in path.relative_to(PROJECT).parts
    }
    dump(OUT / 'fixture-manifest-v2.json', manifest)
    dump(OUT / 'setup-v2.json', {
        **replace(OLD_SETUP),
        'project': str(PROJECT),
        'revised_reference_overlays': overlays,
        'preapply': preapply,
        'comparison_run': 'run01',
    })
    print(json.dumps({
        'fixture': str(PROJECT), 'cases': len(cases),
        'files': len(manifest), 'overlays': overlays,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
