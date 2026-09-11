"""Give a fresh reader the final normal recovery packet, without the replay."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
SETUP_NAME = os.environ.get('MAINTAIN_EVAL_SETUP', 'setup.json')
RUN_NAME = os.environ.get('MAINTAIN_EVAL_RUN', 'run01')
DEST_NAME = os.environ.get('MAINTAIN_EVAL_REENTRY', 'reentry01')
SETUP = json.loads((OUT / SETUP_NAME).read_text())
PROJECT = Path(SETUP['project'])
DEST = OUT / DEST_NAME
sys.path.insert(0, str(PROJECT))
from context.work.harness.maintain.codex_session import CodexMaintainSession
from context.work.harness.maintain.operation import bootstrap_workspace


def main():
    assert (OUT / RUN_NAME / 'summary.json').is_file(), 'Replay must complete before reentry'
    if DEST.exists():
        raise RuntimeError('Refusing to overwrite an existing reader run')
    DEST.mkdir()
    packet = bootstrap_workspace(PROJECT, PROJECT / 'context/work', SETUP['workspace_id'])
    (DEST / 'packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2) + '\n')
    schema = {
        'type': 'object', 'additionalProperties': False,
        'properties': {
            'answers': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'properties': {
                    'question': {'type': 'string'}, 'answer': {'type': 'string'},
                    'evidence': {'type': 'array', 'items': {
                        'type': 'object', 'additionalProperties': False,
                        'properties': {'path': {'type': 'string'}, 'excerpt': {'type': 'string'}},
                        'required': ['path', 'excerpt']
                    }},
                    'unresolved': {'type': 'array', 'items': {'type': 'string'}}
                }, 'required': ['question', 'answer', 'evidence', 'unresolved']
            }},
            'additional_files_read': {'type': 'array', 'items': {'type': 'string'}}
        }, 'required': ['answers', 'additional_files_read']
    }
    (DEST / 'schema.json').write_text(json.dumps(schema, ensure_ascii=False, indent=2) + '\n')
    prompt = '''이 Workspace 작업에 새로 들어온 주체로서 현재 문서에서 아래 내용을 파악해 주세요. 답변은 한국어로 쓰고 각 판단의 정확한 문서 경로와 짧은 원문 발췌를 제시하세요. 확인할 수 없는 것은 추정으로 채우지 말고 미확인으로 남기세요.

1. 지금 첫 실행 범위와 다음 행동은 무엇이며, 현재까지 실제 구현·검사는 어디까지 이루어졌나요?
2. 이 작업에서 Ticket의 코드 범위와 이름·조건식·변환·타입 같은 분석 주제는 어떤 관계인가요? 그 관계를 정하면서 어떤 이해를 바로잡았고, 현재 작업에 어떤 영향이 있나요?
3. 현재 후보에 관해 코드 조사로 보고된 사실과 실제 동작 검사로 확인된 사실을 어떻게 구별할 수 있나요? 한 Ticket의 완료로 전체 Work를 끝냈다고 판단할 수 있나요?

아래는 일반 Recover가 제공하는 전체 packet입니다. 필요한 상세 문서는 이 packet에 연결된 현재 Workspace의 current·records·output·source 문서 중에서 선택해 읽을 수 있습니다. 이 읽기 범위는 다음 root 안으로 한정합니다: ''' + str(PROJECT / 'context/work/workspaces' / SETUP['workspace_id']) + '''.
새 테스트·제품 실행·파일 수정은 하지 마세요. 원래 대화 로그, 다른 Workspace, Project 밖 파일, eval-inputs의 전달용 원문, 평가 기록·채점표·모델 실행 로그는 읽지 마세요. 내부 작업이 기억난다고 가정하지 말고 제공된 문서의 근거로만 답하세요.

<recovery_packet>
''' + json.dumps(packet, ensure_ascii=False, indent=2) + '\n</recovery_packet>\n'
    (DEST / 'prompt.txt').write_text(prompt)
    executable = CodexMaintainSession(PROJECT, SETUP['workspace_id'])._codex_executable
    command = [executable, 'exec', '--json', '--sandbox', 'read-only', '--ignore-user-config', '-C', str(PROJECT), '-c', 'features.hooks=false', '--output-schema', str(DEST / 'schema.json'), '--output-last-message', str(DEST / 'answers.json'), '-']
    (DEST / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    started = time.time()
    print('START fresh reentry reader', flush=True)
    result = subprocess.run(command, input=prompt, text=True, capture_output=True, cwd=PROJECT, env=env, timeout=900)
    (DEST / 'stdout.jsonl').write_text(result.stdout or '')
    (DEST / 'stderr.txt').write_text(result.stderr or '')
    (DEST / 'execution.json').write_text(json.dumps({'returncode': result.returncode, 'elapsed_seconds': round(time.time() - started, 3)}, indent=2) + '\n')
    if result.returncode:
        raise RuntimeError('Fresh reader failed: ' + result.stderr[-2000:])
    value = json.loads((DEST / 'answers.json').read_text())
    print(json.dumps(value, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
