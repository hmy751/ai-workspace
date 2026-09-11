"""Run the unchanged Maintainer bridge and Guard on the frozen fixture."""
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
SETUP = json.loads((OUT / 'setup.json').read_text())
PROJECT = Path(SETUP['project'])
WORKSPACE = SETUP['workspace_id']
WS = PROJECT / 'context/work/workspaces' / WORKSPACE
RUN = OUT / 'run01'
sys.path.insert(0, str(PROJECT))
from context.work.harness.maintain.codex_session import CodexMaintainSession
from context.work.harness.maintain.operation import bootstrap_workspace, apply_maintain_decision


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def scan(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.relative_to(root).parts}


def hashes(data):
    return {p: hashlib.sha256(b).hexdigest() for p, b in data.items()}


class Recorder:
    phase = '00-grounding'

    def __call__(self, command, **kwargs):
        folder = RUN / self.phase
        folder.mkdir(exist_ok=True)
        (folder / 'prompt.txt').write_text(kwargs['input'])
        dump(folder / 'command.json', command)
        started = time.time()
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        result = subprocess.run(command, cwd=PROJECT, env=env, timeout=900, **kwargs)
        (folder / 'stdout.jsonl').write_text(result.stdout or '')
        (folder / 'stderr.txt').write_text(result.stderr or '')
        dump(folder / 'execution.json', {'returncode': result.returncode, 'elapsed_seconds': round(time.time() - started, 3)})
        return result


def main():
    if RUN.exists():
        raise RuntimeError('Refusing to overwrite an existing run')
    RUN.mkdir()
    recorder = Recorder()
    session = CodexMaintainSession(PROJECT, WORKSPACE, runner=recorder)
    baseline = scan(PROJECT)
    packet = bootstrap_workspace(PROJECT, PROJECT / 'context/work', WORKSPACE)
    dump(RUN / 'bootstrap.json', packet)
    shutil.copytree(WS, RUN / 'before')
    results = []
    try:
        print('START grounding', flush=True)
        grounding = session.start(packet)
        dump(RUN / 'grounding.json', grounding)
        dump(RUN / 'session.json', {'thread_id': session.thread_id, 'workspace_id': WORKSPACE})
        print('GROUNDED ' + str(session.thread_id), flush=True)
        for case in json.loads((OUT / 'cases.json').read_text()):
            phase = case['phase']
            recorder.phase = phase
            folder = RUN / phase
            folder.mkdir()
            dump(folder / 'input.json', case)
            before = scan(PROJECT)
            dump(folder / 'before-hashes.json', hashes(before))
            print('START ' + phase, flush=True)
            decision = session.resume(case['delta'])
            dump(folder / 'decision.json', decision)
            after_judge = scan(PROJECT)
            if after_judge != before:
                raise RuntimeError('Semantic agent modified fixture files before Guard')
            applied = apply_maintain_decision(PROJECT, PROJECT / 'context/work', WORKSPACE, decision)
            dump(folder / 'apply.json', applied)
            after = scan(PROJECT)
            changes = [p for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)]
            diff = []
            for path in changes:
                diff.extend(difflib.unified_diff(before.get(path, b'').decode().splitlines(True), after.get(path, b'').decode().splitlines(True), fromfile='before/' + path, tofile='after/' + path))
            (folder / 'changes.diff').write_text(''.join(diff))
            shutil.copytree(WS / 'current', folder / 'current')
            shutil.copytree(WS / 'records', folder / 'records')
            dump(folder / 'after-hashes.json', hashes(after))
            result = {'phase': phase, 'kind': case['kind'], 'outcome': decision['outcome'], 'apply': applied['context_status'], 'changed': changes, 'summary': decision['summary']}
            results.append(result)
            dump(RUN / 'progress.json', results)
            print(json.dumps(result, ensure_ascii=False), flush=True)
        final_packet = bootstrap_workspace(PROJECT, PROJECT / 'context/work', WORKSPACE)
        dump(RUN / 'final-recover.json', final_packet)
        shutil.copytree(WS, RUN / 'after')
        final = scan(PROJECT)
        changed = [p for p in sorted(set(baseline) | set(final)) if baseline.get(p) != final.get(p)]
        dump(RUN / 'summary.json', {'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'thread_id': session.thread_id, 'results': results, 'all_changed_paths': changed})
        print('DONE ' + str(RUN), flush=True)
    except Exception as error:
        dump(RUN / 'failure.json', {'phase': recorder.phase, 'error_type': type(error).__name__, 'error': str(error), 'thread_id': session.thread_id, 'completed': results})
        print('FAILED ' + recorder.phase + ': ' + str(error), flush=True)
        raise


if __name__ == '__main__':
    main()
