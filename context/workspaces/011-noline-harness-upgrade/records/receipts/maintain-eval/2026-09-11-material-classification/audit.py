"""Check preserved decisions, actual file changes, and runtime metadata."""
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path(__file__).resolve().parent
SETUP = json.loads((OUT / 'setup.json').read_text())
PROJECT = Path(SETUP['project'])
PREFIX = 'context/work/workspaces/' + SETUP['workspace_id'] + '/'


def read(relative):
    return json.loads((OUT / relative).read_text())


def main():
    initial = read('fixture-manifest.json')
    summary = read('run01/summary.json')
    rows = []
    for result in summary['results']:
        phase = result['phase']
        folder = '01-research-assisted-link-repair' if phase == '01-research' else phase
        before = read('run01/' + phase + '/before-hashes.json')
        after = read('run01/' + folder + '/after-hashes.json')
        decision = read('run01/' + folder + '/decision.json')
        actual = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
        declared = sorted(PREFIX + c['path'] for c in decision['changes'])
        assert actual == sorted(result['changed'])
        assert actual == declared, (phase, actual, declared)
        for change in decision['changes']:
            path = PREFIX + change['path']
            assert before.get(path) == change['expected_sha256']
            assert after[path] == hashlib.sha256(change['content'].encode()).hexdigest()
        rows.append({'phase': phase, 'outcome': decision['outcome'], 'changed_paths': actual,
                     'declared_matches_actual': True,
                     'elapsed_seconds': read('run01/' + phase + '/execution.json')['elapsed_seconds']})

    final = read('run01/08-progression/after-hashes.json')
    changed = sorted(p for p in set(initial) | set(final) if initial.get(p) != final.get(p))
    assert changed == summary['all_changed_paths']
    assert all(p.startswith(PREFIX + 'current/') and p.endswith('.md') for p in changed)
    live = {p.relative_to(PROJECT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PROJECT.rglob('*') if p.is_file() and '.git' not in p.relative_to(PROJECT).parts}
    assert live == final, 'No reader/model changes outside guarded decision expected'

    rollout = Path('/Users/hammyeong-yeon/.codex/sessions/2026/09/11/rollout-2026-09-11T10-46-36-01a08e25-2d26-7f32-bfd2-544667ef4c79.jsonl')
    contexts = []
    for line in rollout.open():
        event = json.loads(line)
        if event['type'] == 'turn_context':
            payload = event['payload']
            contexts.append({k: payload.get(k) for k in ('turn_id', 'cwd', 'model', 'effort', 'approval_policy', 'sandbox_policy')})
    assert len(contexts) == 9
    assert all(c['sandbox_policy'] == {'type': 'read-only'} for c in contexts)

    state_before = next(c['content'] for c in read('prebaseline-decision.json')['changes'] if c['path'] == 'current/state/index.md').encode()
    with tarfile.open(OUT / 'baseline.tar') as archive:
        analysis_before = archive.extractfile(PREFIX + 'current/memory/analysis-items.md').read()
    sizes = {}
    for path, before in [('current/state/index.md', state_before), ('current/memory/analysis-items.md', analysis_before)]:
        sizes[path] = {'before_utf8_bytes': len(before), 'after_utf8_bytes': (PROJECT / PREFIX / path).stat().st_size}

    value = {'phases': rows, 'changed_paths': changed,
             'initial_scanned_file_paths': len(initial), 'final_scanned_file_paths': len(final),
             'scan_scope': 'Like run.py: readable file paths including symlink targets, excluding .git',
             'records_changed': [p for p in changed if p.startswith(PREFIX + 'records/')],
             'all_changes_current_markdown_only': True,
             'original_source_product_machine_files_unchanged': True,
             'live_fixture_matches_final_guarded_state': True,
             'sizes': sizes, 'maintainer_turn_contexts': contexts}
    (OUT / 'audit.json').write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in value.items() if k not in ('phases', 'maintainer_turn_contexts')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
