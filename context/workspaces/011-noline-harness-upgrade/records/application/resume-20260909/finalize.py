from pathlib import Path
import json,hashlib,shutil
T=Path('/Users/hammyeong-yeon/Desktop/10_work/noline');H=Path(__file__).resolve().parent
W=T/'context/work/workspaces/001-noline-context-harness-application'
R=W/'records/receipts'
# Preserve the first complete raw run, including its failure, independently of the repeat receipt.
for src,name in [('/private/tmp/noline-upgrade-all-tests.log','2026-09-09-first-full-run.log'),('/private/tmp/noline-upgrade-related-tests.log','2026-09-09-related-tests.log')]:
 shutil.copyfile(src,R/'harness-tests'/name)
closure=Path('/private/tmp/noline-upgrade-input-closure.log').read_text();d=json.loads(closure[closure.index('{'):]);assert not d['missing']
(R/'application/input-closure-20260909.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# A preapply manifest does not self-hash its containing receipt.
p=R/'application/paths-20260909.json';m=json.loads(p.read_text());selfpath=str(p.relative_to(T));m['items']=[x for x in m['items'] if x['path']!=selfpath];m['phase']='pre-apply intent; later verification/state/report edits are not represented as final hashes';p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
receipt='harness-test-20260909T143128349049Z-ca581a4a12244cabba828fe6315ad037.json'
p=R/'harness-tests/README.md';p.write_text('''# Harness test evidence

- [관련 63 tests](2026-09-09-related-tests.log): sandbox 직접 실행에서 전부 통과했다.
- [첫 전체 122 tests](2026-09-09-first-full-run.log): sandbox 직접 실행에서 descendant timeout timing failure 한 건이 재현됐다. PID 파일 생성 전 exit 124였으며 원본 테스트를 바꾸지 않았다.
- [Source snapshot을 동반한 전체 재실행]('''+receipt+'''): 승인된 target receipt 쓰기 권한으로 실행해 같은 source의 122 tests가 통과했다. Helper가 Python source 27개를 snapshot했다. 첫 실패를 지우거나 timing 문제가 해결됐다고 해석하지 않는다.

임시 Workspace validation도 전체 실행에 포함되어 pass했다. Product Verify의 구조 검사, 실제 host acceptance와 구별한다.
''')
p=W/'records/2026-09-09-01-reference-upgrade.md';s=p.read_text();s=s.replace('적용 파일과 검증을 진행 중이며 실제 결과를 회수한 뒤 이 절을 갱신한다. 독립 reviewer가 원자료·target diff·증거를 직접 대조한다.', '''적용 후 직접 `node scripts/check-harness.mjs`가 통과했고 명시·기본 Recover는 같은 15개 context 경로를 읽었다. Spec 다섯 본문·Ticket 색인·state·output과 선택한 Project 문서 네 개가 들어오며 옛 memory와 Ticket 본문은 기본 packet에 없다. 여섯 skill의 전체 파일은 승인된 Source와 같고 상대 bridge·frontmatter·호출 설정과 JSON/TOML parse를 확인했다.

관련 63 tests는 전부 통과했다. 첫 전체 122 tests에서 `test_timeout_covers_descendant_after_group_leader_exits`의 PID 파일 생성 timing failure 한 건이 재현됐다. 원본 log를 보존했다. 승인된 receipt 쓰기 실행에서 source 27개를 snapshot한 전체 재실행은 122 tests가 통과했다. 첫 실패와 재실행 성공의 실행 환경 차이를 유지하며 timing 문제가 해결됐다고 주장하지 않는다. Ephemeral validation은 두 전체 실행에서 pass했다.

Node의 실제 regular file 읽기를 계측해 [input closure](receipts/application/input-closure-20260909.json)와 선언 evidence를 대조했고 빠진 content input은 없었다. 이후 이 문서·현재 상태를 최종 반영해 실행하는 Verify의 result와 receipt cursor는 [machine status](../current/state/status.json)에서 확인한다. 이 문서가 과거 receipt의 입력 freshness를 소급해 보증하지 않는다.

기존 사용자 파일 18개 entry의 hash가 preflight와 같았고 제품 코드·기존 상세 문서·Claude/Codex 고유 연결 보존을 Main도 직접 확인했다. 구현과 별개의 reviewer는 실제 target 내용·보존 및 explicit/default Recover에서 P1/P2가 없다고 Main에게 보고했다. 최종 receipt 증거 대조와 이식 결과 수락은 Main에게 남아 있다.''')
s=s.replace('새 session default-unbound를 유지한다.', 'Codex status는 현재 session을 unbound로, Claude status는 명시한 read-only probe id를 unbound로 반환했다. Claude wrapper를 selector 없이 호출하면 오류가 나는 기존 동작도 유지된다. 두 status 조회 뒤 runtime 디렉터리는 생성되지 않았다. 이는 actual-host lifecycle의 격리 장면을 대신하지 않는다. 새 session default-unbound를 유지한다.')
p.write_text(s)
p=W/'current/state/index.md';s=p.read_text();s=s.replace('보완을 진행 중이다.','보완을 적용했다.').replace('다음 행동은 적용된 파일의 검증과 독립 검토다.','''직접 구조 검사와 explicit/default Recover가 통과했다. 관련 tests 63개는 pass했고, 첫 전체 122-test 실행은 기존 timeout timing failure 한 건, source snapshot을 동반한 재실행은 122개 pass였다. 테스트를 약화하지 않았고 양쪽 결과를 보존했다. 같은 선언 파일의 hash 일치와 directory/symlink topology의 현재성은 구별한다.

다음 행동은 최종 receipt를 포함한 Main의 독립 검토 회수와, 사용자가 실제 후속 작업을 정했을 때 그 Work를 시작하는 것이다. Main이 회수한 reviewer 보고에서는 실제 target 내용·보존·Recover에 P1/P2가 없었으며 마지막 증거 대조가 남아 있다.''');p.write_text(s)
p=W/'current/memory/tickets/001-upgrade.md';s=p.read_text();s=s.replace('최신 파일과 문서 전환을 준비했다. 적용·실행 결과는','''최신 파일과 문서 전환을 적용했다. 관련 63 tests·구조 검사·explicit/default Recover와 skill 정적 검사가 통과했다. 전체 122 tests는 첫 실행에서 timeout timing failure 1건, source snapshot 재실행에서 전부 pass였으며 두 결과를 보존했다. Main이 회수한 독립 reviewer는 target 내용·보존·Recover의 P1/P2가 없다고 보고했다. 최종 Verify 사건과 증거 대조는 machine cursor와 Main 검토를 따른다. 적용·실행 결과는''').replace('이 본문은 최종 검증·독립 검토 결과를 받은 뒤 갱신한다.','실제 host·제품 acceptance와 Workspace 완료를 뜻하지 않는다.');p.write_text(s)
# Verify's content closure did not change: reports were edited in-place and new receipts/logs are non-Markdown.
pre=json.loads((H/'preflight.json').read_text());protected=[]
for e in pre['git']['dirty_entries']:
 p=T/e['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'];protected.append(e['path'])
(H/'verification-summary.json').write_text(json.dumps({'related_tests':{'count':63,'result':'pass'},'first_full_tests':{'count':122,'result':'fail','failures':1,'test':'test_timeout_covers_descendant_after_group_leader_exits','runtime':'sandbox direct execution'},'durable_full_tests':{'count':122,'result':'pass','source_files':27,'receipt':str(R/'harness-tests'/receipt),'runtime':'approved target receipt write execution'},'protected_unchanged':protected,'skill_count':6,'recover_loaded_paths':15,'content_closure_missing':d['missing'],'maintain':'activation_pending'},ensure_ascii=False,indent=2)+'\n')
print('Final human context and both test runs preserved; Verify pending.')
