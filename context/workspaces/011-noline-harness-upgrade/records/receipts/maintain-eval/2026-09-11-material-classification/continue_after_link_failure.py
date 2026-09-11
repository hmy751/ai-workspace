"""Preserve the first failure, fix exactly its broken link, continue the eval.

This is an assisted semantic continuation, not an automatic lifecycle success.
"""
import datetime
import difflib
import json
from pathlib import Path
import shutil

import run as harness
from context.work.harness.maintain.codex_session import CodexMaintainSession
from context.work.harness.maintain.operation import apply_maintain_decision, bootstrap_workspace


def capture(folder, before, after):
    changed = [p for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)]
    diff = []
    for path in changed:
        diff.extend(difflib.unified_diff(before.get(path, b'').decode().splitlines(True), after.get(path, b'').decode().splitlines(True), fromfile='before/' + path, tofile='after/' + path))
    (folder / 'changes.diff').write_text(''.join(diff))
    shutil.copytree(harness.WS / 'current', folder / 'current')
    shutil.copytree(harness.WS / 'records', folder / 'records')
    harness.dump(folder / 'after-hashes.json', harness.hashes(after))
    return changed


def main():
    out, project, run = harness.OUT, harness.PROJECT, harness.RUN
    failure = json.loads((run / 'failure.json').read_text())
    assert failure['phase'] == '01-research' and 'local Markdown link target does not exist' in failure['error']
    assert not (run / 'summary.json').exists()
    initial = harness.scan(project)
    before_hashes = json.loads((run / '01-research/before-hashes.json').read_text())
    assert harness.hashes(initial) == before_hashes, 'Original failed Guard must have zero writes'
    raw = (run / '01-research/decision.json').read_text()
    original = json.loads(raw)
    repaired = json.loads(raw)
    state_change = next(c for c in repaired['changes'] if c['path'] == 'current/state/index.md')
    old = '../../../../../eval-inputs/noline-002-additional-research-and-ticket-drafts-2026-09-11.md'
    new = '../../../../../../eval-inputs/noline-002-additional-research-and-ticket-drafts-2026-09-11.md'
    assert state_change['content'].count(old) == 1
    state_change['content'] = state_change['content'].replace(old, new)
    changed_fields = []
    for a, b in zip(original['changes'], repaired['changes']):
        for key in a:
            if a[key] != b[key]:
                changed_fields.append([a['path'], key])
    assert changed_fields == [['current/state/index.md', 'content']]
    folder = run / '01-research-assisted-link-repair'
    folder.mkdir()
    harness.dump(folder / 'decision.json', repaired)
    harness.dump(folder / 'assistance.json', {'original_guard_zero_writes': True, 'old': old, 'new': new, 'changed_fields': changed_fields, 'meaning_or_owner_hints_added_to_model': False})
    applied = apply_maintain_decision(project, project / 'context/work', harness.WORKSPACE, repaired)
    harness.dump(folder / 'apply.json', applied)
    changed = capture(folder, initial, harness.scan(project))
    results = [{'phase': '01-research', 'kind': 'actual_replay_with_manual_link_repair', 'outcome': original['outcome'], 'original_apply': 'failed', 'assisted_apply': applied['context_status'], 'changed': changed, 'summary': original['summary']}]
    harness.dump(run / 'progress.json', results)
    recorder = harness.Recorder()
    session = CodexMaintainSession.restore(project, harness.WORKSPACE, thread_id=failure['thread_id'], runner=recorder)
    print('APPLIED one-link repair; continuing same semantic thread', flush=True)
    try:
        for case in json.loads((out / 'cases.json').read_text())[1:]:
            phase = case['phase']
            recorder.phase = phase
            folder = run / phase
            folder.mkdir()
            harness.dump(folder / 'input.json', case)
            before = harness.scan(project)
            harness.dump(folder / 'before-hashes.json', harness.hashes(before))
            print('START ' + phase, flush=True)
            decision = session.resume(case['delta'])
            harness.dump(folder / 'decision.json', decision)
            assert harness.scan(project) == before, 'Semantic agent must not write before Guard'
            applied = apply_maintain_decision(project, project / 'context/work', harness.WORKSPACE, decision)
            harness.dump(folder / 'apply.json', applied)
            changed = capture(folder, before, harness.scan(project))
            result = {'phase': phase, 'kind': case['kind'], 'outcome': decision['outcome'], 'apply': applied['context_status'], 'changed': changed, 'summary': decision['summary']}
            results.append(result)
            harness.dump(run / 'progress.json', results)
            print(json.dumps(result, ensure_ascii=False), flush=True)
        packet = bootstrap_workspace(project, project / 'context/work', harness.WORKSPACE)
        harness.dump(run / 'final-recover.json', packet)
        shutil.copytree(harness.WS, run / 'after')
        final = harness.scan(project)
        harness.dump(run / 'summary.json', {'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'thread_id': session.thread_id, 'initial_failure': failure, 'manual_assistance': '01-research-assisted-link-repair/assistance.json', 'results': results, 'all_changed_paths': [p for p in sorted(set(initial) | set(final)) if initial.get(p) != final.get(p)]})
        print('DONE assisted replay', flush=True)
    except Exception as error:
        harness.dump(run / 'continuation-failure.json', {'phase': recorder.phase, 'error_type': type(error).__name__, 'error': str(error), 'completed': results})
        raise


if __name__ == '__main__':
    main()
