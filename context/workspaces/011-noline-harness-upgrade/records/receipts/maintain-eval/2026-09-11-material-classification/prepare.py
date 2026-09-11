"""Freeze an isolated historical fixture and exact response-end replay inputs."""
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile

OUT = Path(__file__).resolve().parent
TARGET = Path('/Users/hammyeong-yeon/Desktop/10_work/noline')
BASE = 'a612ba4c49b92b1193e75e1d56bdefcdcd86bbda'
WORKSPACE = '002-code-readability-refactoring'
TEMP = Path('/private/tmp/maintainer-material-eval-20260911')
PROJECT = TEMP / 'run01-project'
MAIN = Path('/Users/hammyeong-yeon/.codex/sessions/2026/09/10/rollout-2026-09-10T21-56-54-01a08b64-7f25-7972-ac3e-496cb4af1de7.jsonl')
MAINTAIN = MAIN.with_name('rollout-2026-09-10T21-58-08-01a08b65-9ef2-7ec3-a9fa-3b2e23ef1514.jsonl')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def messages(path):
    for number, line in enumerate(path.open(), 1):
        obj = json.loads(line)
        value = obj.get('payload', {})
        if obj.get('type') == 'response_item' and value.get('type') == 'message':
            yield number, obj['timestamp'], value.get('role'), '\n'.join(c.get('text', '') for c in value.get('content', []))


def main():
    if PROJECT.exists():
        raise RuntimeError('Refusing to overwrite an existing fixture')
    PROJECT.mkdir(parents=True)
    archive = subprocess.check_output(['git', '-C', str(TARGET), 'archive', BASE])
    (OUT / 'baseline.tar').write_bytes(archive)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(PROJECT, filter='data')
    subprocess.run(['git', 'init', '-q', str(PROJECT)], check=True)
    sys.path.insert(0, str(PROJECT))
    from context.work.harness.maintain.operation import apply_maintain_decision

    all_inputs = []
    historical = []
    predecision = None
    for line, timestamp, role, text in messages(MAINTAIN):
        if role == 'user' and '<bounded_response_delta>' in text:
            value = json.loads(text.split('<bounded_response_delta>')[1].split('</bounded_response_delta>')[0])
            if line in [101, 131, 143, 162, 181, 193]:
                all_inputs.append({'line': line, 'timestamp': timestamp, 'delta': value})
        if role == 'assistant':
            try:
                value = json.loads(text)
            except json.JSONDecodeError:
                continue
            if line == 92:
                predecision = value
            if line in [124, 136, 155, 174, 186, 205]:
                historical.append({'line': line, 'timestamp': timestamp, 'decision': value})
    assert len(all_inputs) == 6 and len(historical) == 6 and predecision
    # The commit preceded one automatic state update. Its exact preimage must match.
    preapply = apply_maintain_decision(PROJECT, PROJECT / 'context/work', WORKSPACE, predecision)
    assert preapply['context_status'] == 'updated', preapply
    expected = next(c['expected_sha256'] for c in historical[0]['decision']['changes'] if c['path'] == 'current/state/index.md')
    state = PROJECT / 'context/work/workspaces' / WORKSPACE / 'current/state/index.md'
    assert digest(state.read_bytes()) == expected

    research_name = 'noline-002-additional-research-and-ticket-drafts-2026-09-11.md'
    research = None
    for raw in MAIN.open():
        obj = json.loads(raw)
        value = obj.get('payload', {})
        code = value.get('input', '')
        if value.get('type') != 'custom_tool_call' or '*** Add File: /private/tmp/' + research_name not in code:
            continue
        match = re.search(r'tools\.apply_patch\(("(?:[^"\\]|\\.)*")\)', code)
        assert match
        patch = json.loads(match.group(1))
        content = patch.split('*** Add File: /private/tmp/' + research_name + '\n', 1)[1].split('*** End Patch', 1)[0]
        research = '\n'.join(line[1:] for line in content.splitlines() if line.startswith('+')) + '\n'
    assert research and digest(research.encode()) == 'f9656715bc0935258e664b189c412da4b2c04ca24cd4f2775c605eeb5134c1c4'
    agreement_path = Path('/private/tmp/noline-002-agreed-ticket-workflow-2026-09-11.md')
    agreement = agreement_path.read_text()
    assert digest(agreement.encode()) == 'e7e11b6517294d7e7108520def47cb6281ecace9378c284d57d1b2db7acd8814'
    (OUT / 'research-original.md').write_text(research)
    (OUT / 'agreement-original.md').write_text(agreement)
    exchange = PROJECT / 'eval-inputs'
    exchange.mkdir()
    replacements = {
        str(TARGET): str(PROJECT),
        '/private/tmp/' + research_name: str(exchange / research_name),
        str(agreement_path): str(exchange / agreement_path.name),
    }

    def relocate(text):
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    # Read permission points only to task inputs; original external workspaces stay untouched.
    (exchange / research_name).write_text(relocate(research))
    (exchange / agreement_path.name).write_text(relocate(agreement))
    dump(OUT / 'historical-inputs.json', all_inputs)
    dump(OUT / 'historical-decisions.json', historical)
    dump(OUT / 'prebaseline-decision.json', predecision)
    phases = ['01-research', '02-boundary-explanation', '03-misunderstanding', '04-correction', '05-coverage-explanation', '06-adoption']
    cases = []
    for phase, entry in zip(phases, all_inputs):
        delta = {key: relocate(value) if isinstance(value, str) else value for key, value in entry['delta'].items()}
        cases.append({'phase': phase, 'kind': 'actual_replay', 'source_line': entry['line'], 'delta': delta})
    cases.append({'phase': '07-restatement', 'kind': 'synthetic_control', 'delta': {
        'workspace_id': WORKSPACE, 'turn_id': 'eval-restatement',
        'user_prompt': '방금 합의한 진행 방식을 다시 설명만 해줘. 결정이나 진행 상태는 그대로야.',
        'main_response': 'Ticket은 관련된 여러 개선 관점을 적용할 코드 범위로 구성합니다. 각 범위에서 바텀부터 살피며 변경 전후 동작과 개선 효과를 확인하고, 전체 분석 주제의 확인한 범위와 남은 범위를 함께 관리합니다. 사용자는 여전히 Ticket을 검토 중이며 새 결정이나 상태 변화는 없습니다.'
    }})
    cases.append({'phase': '08-progression', 'kind': 'synthetic_lifecycle', 'delta': {
        'workspace_id': WORKSPACE, 'turn_id': 'eval-progression',
        'user_prompt': '티켓 검토 끝났어. 경비 합계 표시부터 진행해. 합의한 방식대로 변경 전 검사부터 시작하자.',
        'main_response': '첫 실행 범위로 경비 합계 표시를 선택했습니다. 해당 Ticket의 보존 조건과 개선 목표를 바탕으로 변경 전 검사를 준비하는 단계로 넘어갑니다. 다른 초안과 후속 후보는 유지합니다. 제품 코드 수정이나 테스트 실행은 아직 하지 않았고, 구체적인 테스트 runner는 다음 작업에서 정합니다.'
    }})
    dump(OUT / 'cases.json', cases)
    manifest = {}
    for path in sorted(PROJECT.rglob('*')):
        if path.is_file() and '.git' not in path.relative_to(PROJECT).parts:
            manifest[str(path.relative_to(PROJECT))] = digest(path.read_bytes())
    dump(OUT / 'fixture-manifest.json', manifest)
    dump(OUT / 'setup.json', {
        'project': str(PROJECT), 'workspace_id': WORKSPACE, 'target_commit': BASE,
        'baseline_archive_sha256': digest(archive), 'preapply': preapply,
        'baseline_state_matches_historical_next_preimage': True,
        'path_relocations': replacements,
        'caveats': ['Fresh grounding at historical current; the original Maintainer warm history before research is not replayed.', 'Six exact historical response-end inputs plus two explicitly synthetic cases.', 'Inputs from later records-location hints and later fixes are excluded.', 'The immutable historical context contains past operating issues; no actual Noline hook or worker is invoked.']
    })
    print(json.dumps({'fixture': str(PROJECT), 'cases': len(cases), 'files': len(manifest), 'matched_original_research_hash': True, 'matched_preimage': True}))


if __name__ == '__main__':
    main()
