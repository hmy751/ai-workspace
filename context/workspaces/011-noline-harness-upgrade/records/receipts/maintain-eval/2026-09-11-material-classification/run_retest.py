"""Run the revised Maintain contract against the same eight inputs."""
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

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
SETUP = json.loads((OUT / 'setup-v2.json').read_text())
PROJECT = Path(SETUP['project'])
WORKSPACE = SETUP['workspace_id']
WS = PROJECT / 'context/work/workspaces' / WORKSPACE
RUN = OUT / 'run02'
sys.path.insert(0, str(PROJECT))
from context.work.harness.maintain.codex_session import CodexMaintainSession
from context.work.harness.maintain.operation import (
    apply_maintain_decision,
    bootstrap_workspace,
)


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def scan(root):
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob('*'))
        if path.is_file() and '.git' not in path.relative_to(root).parts
    }


def hashes(data):
    return {path: hashlib.sha256(content).hexdigest() for path, content in data.items()}


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
        result = subprocess.run(
            command, cwd=PROJECT, env=env, timeout=900, **kwargs
        )
        (folder / 'stdout.jsonl').write_text(result.stdout or '')
        (folder / 'stderr.txt').write_text(result.stderr or '')
        dump(folder / 'execution.json', {
            'returncode': result.returncode,
            'elapsed_seconds': round(time.time() - started, 3),
        })
        return result


def main():
    if RUN.exists():
        raise RuntimeError('Refusing to overwrite an existing retest run')
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
        dump(RUN / 'session.json', {
            'thread_id': session.thread_id, 'workspace_id': WORKSPACE,
        })
        print('GROUNDED ' + str(session.thread_id), flush=True)
        for case in json.loads((OUT / 'cases-v2.json').read_text()):
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
            assert scan(PROJECT) == before, 'Semantic agent wrote before Guard'
            applied = apply_maintain_decision(
                PROJECT, PROJECT / 'context/work', WORKSPACE, decision
            )
            dump(folder / 'apply.json', applied)
            after = scan(PROJECT)
            changed = [
                path for path in sorted(set(before) | set(after))
                if before.get(path) != after.get(path)
            ]
            diff = []
            for path in changed:
                diff.extend(difflib.unified_diff(
                    before.get(path, b'').decode().splitlines(True),
                    after.get(path, b'').decode().splitlines(True),
                    fromfile='before/' + path,
                    tofile='after/' + path,
                ))
            (folder / 'changes.diff').write_text(''.join(diff))
            shutil.copytree(WS / 'current', folder / 'current')
            shutil.copytree(WS / 'records', folder / 'records')
            dump(folder / 'after-hashes.json', hashes(after))
            item = {
                'phase': phase, 'kind': case['kind'],
                'outcome': decision['outcome'],
                'apply': applied['context_status'],
                'changed': changed, 'summary': decision['summary'],
            }
            results.append(item)
            dump(RUN / 'progress.json', results)
            print(json.dumps(item, ensure_ascii=False), flush=True)
        dump(RUN / 'final-recover.json', bootstrap_workspace(
            PROJECT, PROJECT / 'context/work', WORKSPACE
        ))
        shutil.copytree(WS, RUN / 'after')
        final = scan(PROJECT)
        dump(RUN / 'summary.json', {
            'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'thread_id': session.thread_id, 'results': results,
            'all_changed_paths': [
                path for path in sorted(set(baseline) | set(final))
                if baseline.get(path) != final.get(path)
            ],
        })
        print('DONE run02', flush=True)
    except Exception as error:
        dump(RUN / 'failure.json', {
            'phase': recorder.phase, 'error_type': type(error).__name__,
            'error': str(error), 'thread_id': session.thread_id,
            'completed': results,
        })
        print('FAILED ' + recorder.phase + ': ' + str(error), flush=True)
        raise


if __name__ == '__main__':
    main()
