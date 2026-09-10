from pathlib import Path
import subprocess,json,hashlib,os
ROOT=Path('/Users/hammyeong-yeon/Desktop/context-harness')
REF=ROOT/'reference-project'
TARGET=Path('/Users/hammyeong-yeon/Desktop/10_work/noline')
HERE=Path(__file__).resolve().parent
PAYLOAD=HERE/'payload'
W='context/work/workspaces/001-noline-context-harness-application'
SKILLS=['create-context-workspace','update-project-context','work-discussion','reconsider-work','work-artifact-briefing','explanation-recovery']
def put(p,s):
 q=PAYLOAD/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s)
def get(p): return (TARGET/p).read_text()
def ref(p): return (REF/p).read_text()
def jput(p,o): put(p,json.dumps(o,ensure_ascii=False,indent=2)+'\n')
# Copy only Reference's current changed responsibility files. No target-only file is removed.
paths=subprocess.check_output(['git','diff','--name-only','f0bada9','HEAD','--','reference-project/context/work'],cwd=ROOT,text=True).splitlines()
for p in paths:
 r=p.removeprefix('reference-project/')
 if '/001-default-timeout/' in r: continue
 s=ref(r)
 if r.endswith('workspace-context-maintainer.toml'):
  s=s.replace('교체 가능한 Reference Project role.','교체 가능한 role.').replace('Main이 수동 fallback','Noline Main이 수동 fallback').replace('Reference Project의','Noline의')
 if r=='context/work/harness/maintain/README.md':
  s=s.replace('자동 lifecycle은 별도의 persisted session bridge와 hook adapter가 맡는다.', 'Claude Code는 [`.claude/settings.json`](../../../../.claude/settings.json)의 hook으로 같은 lifecycle 계약에 들어오며, 현재 semantic runner는 Codex implementation을 재사용한다. 자동 lifecycle은 별도의 persisted session bridge와 hook adapter가 맡는다.')
 if r.endswith('README.md'):
  s=s.replace('recover 001-default-timeout','recover <workspace_id>').replace('verify 001-default-timeout','verify <workspace_id>')
 if r=='context/work/AGENTS.md':
  s=s.replace('제품 코드·테스트는 Project root의 `src/`와 `tests/`에 두고','제품 코드·테스트는 Project root의 `apps/`·`packages/`와 해당 Owner에 두고')
  s=s.replace('전체 제품·Harness 검증은 Project root에서 다음 명령으로 실행한다.','전체 Harness 검증은 Project root에서 다음 명령으로 실행한다. Noline 제품 검증은 해당 app/package guide를 따른다.')
  s=s.replace("python3 -m unittest discover -s . -p 'test_*.py' -v", "python3 -B -m unittest discover -s context/work/harness -t . -p 'test_*.py' -v")
 put(r,s)
for name in SKILLS:
 for src in (REF/'.agents/skills'/name).rglob('*'):
  if src.is_file(): put(str(Path('.claude/skills')/name/src.relative_to(REF/'.agents/skills'/name)),src.read_text())
s=ref('.agents/skills/README.md').replace('# Reference Project skills','# Noline Context Harness skills')
s=s.replace('이 디렉터리는 이 Project 안에서 작업의 생성·논의·재판단·설명과 Project 맥락 갱신을 수행하는 스킬 원본을 소유한다.', '이 디렉터리는 Noline의 작업 dispatcher와 Context Harness 운영 스킬의 원본을 소유한다.')
s=s.replace('## 설치된 역할과 진입점','## 설치된 역할과 진입점\n\n- [noline-work](noline-work/SKILL.md): 기존 Noline 작업 dispatcher와 report-only agent 조율. 상세 제품 정책 Owner를 유지한다.')
a=s.index('공동 스킬 네 개는');b=s.index('\n\n다른 Project에',a)
s=s[:a]+'Noline의 `.claude/skills/`가 스킬 원본이며 `.agents/skills/`의 상대 symlink가 같은 원본을 Codex에 연결한다. 기존 bridge 모델을 유지하므로 별도 `.codex/skills/` 연결은 만들지 않는다. 호출 설정과 상대 연결의 존재는 실제 host의 발견·호출·Maintain 동작을 증명하지 않는다. Codex adapter와 Noline 전용 Claude hook은 같은 Maintain 계약에 연결되며, actual-host proof는 별도다.'+s[b:]
put('.claude/skills/README.md',s)
put('.agents/skills/README.md','# Noline skill bridge\n\n원본과 호출 조건은 [Claude skill 색인](../../.claude/skills/README.md)이 소유한다. 각 스킬 디렉터리는 같은 이름의 `.claude/skills/` 원본을 가리키는 상대 symlink다. 이 연결은 실제 session의 발견·호출을 증명하지 않는다.\n')
# Keep old flat bodies at their paths as historical text; cease current authority explicitly.
for old,new in [('overview.md','common/product.md'),('prd.md','common/product.md'),('architecture.md','current/architecture.md')]:
 put('context/project/'+old, f'> 2026-09-09 전환: 아래는 최초 이식 당시 원문 보존이다. 현재 판단은 [Project 진입점](README.md)과 [{new}]({new})을 따른다. 이 파일은 더 이상 현재 layer의 정본이나 Recover 입력이 아니다.\n\n'+get('context/project/'+old))
s=ref('context/project/README.md')
a=s.index('## 이 Reference sample의 현재 배치');b=s.index('## 내용 복원 완료 조건',a)
s=s[:a]+'''## Noline의 현재 배치

- [`common/product.md`](common/product.md): 여행 중 일정·경비를 이어갈 사용자 목적, 활성화된 여행의 데이터 관계와 공통 제약
- [`current/architecture.md`](current/architecture.md): client·server·schema·UI의 현재 책임, 지원 경계와 검증 경로
- [`guidance/README.md`](guidance/README.md): 기존 Noline rule·guard·runbook Owner와 조건부 설명 기준의 소비 관계
- [`decisions/0001-selective-local-first.md`](decisions/0001-selective-local-first.md): Selective Local-First 선택의 근거 요약. 상세 결정은 `.claude/decisions/`가 유지한다.

기존 flat `overview.md`, `prd.md`, `architecture.md`는 최초 이식 당시 본문을 보존하며 현재 authority에서는 내려왔다. 원문을 삭제하거나 상세 제품 Owner를 이동하지 않았다.

'''+s[b:]
s=s.replace('제품 코드와 테스트는 이 경계의 내용이 아니며 각각 [`../../src/`](../../src/)와 [`../../tests/`](../../tests/)가 소유한다.', 'Noline의 상세 의미는 root [`CLAUDE.md`](../../CLAUDE.md), [`.claude/context/`](../../.claude/context/), [rules](../../.claude/rules/), [guards](../../.claude/guards/), [runbooks](../../.claude/runbooks/)가 소유한다. 제품 코드와 테스트는 [`apps/`](../../apps/)·[`packages/`](../../packages/)가 소유하며, 충돌 시 상세 Owner와 실제 코드를 대조해 이 층을 갱신한다.')
put('context/project/README.md',s.replace('# Project context','# Noline Project context',1))
put('context/project/common/README.md','''# Noline의 지속 제품 맥락

여러 Work에 계속 필요한 사용자 장면·제품 목적·domain 관계와 Project-wide 제약을 둔다. [제품 의미와 공통 기준](product.md)을 읽고, 현재 구현과 검증 범위는 [current](../current/README.md)에서 별도로 확인한다.

제품 의미를 바꾸는 책임자가 관련 상세 Owner와 대조해 갱신한다. 특정 Workspace의 목표나 검증 결과는 여기에 올리지 않는다.
''')
put('context/project/common/product.md','''# 여행 중 일정과 경비를 이어가는 제품 기준

새 Work의 목적·보존할 동작·데이터 경계를 판단할 때 읽는다. Root [CLAUDE.md](../../../CLAUDE.md)의 불변식과 [README](../../../README.md)의 제품 장면, [Selective Activation](../../../.claude/context/selective-activation-architecture.md)이 상세 Owner다. 이 본문은 여러 작업이 필요한 의미를 재서술하며 충돌 시 상세 Owner를 대조한다.

## 사용자 장면과 성공 기준

Noline은 여행 중 연결이 끊겨도 일정 확인·기록과 경비 관리를 이어가기 위한 여행 관리 앱이다. 사용자는 필요한 여행을 활성화하여 오프라인 데이터를 준비한다. 모든 여행을 로컬에 쌓기보다 활성 여행에 저장과 동기화 책임을 집중한다. 제품 성공의 기준은 네트워크가 불안정해도 핵심 입력을 잃지 않고, 복구 뒤 변경을 서버와 맞출 수 있는 것이다. 기능이나 이식 검사 통과만으로 실제 서비스가 이 기준을 달성했다고 판단하지 않는다.

Trip은 여행 단위이며 Schedule과 Expense가 그 여행의 일정·경비를 나타낸다. 활성 여행의 데이터는 Local SQLite를 기준으로 읽고 쓰며 비활성 여행은 Server API가 기준이다. Activation Router가 Data Entity의 Local/Remote 선택을 맡는다. 지도·검색·길찾기는 사용자가 소유한 sync data가 아니므로 Policy Layer의 네트워크 사용·제한 판단을 따른다.

오프라인 활성 여행은 제목·날짜·금액 같은 핵심 내용을 입력하고, 좌표 등 온라인 보강이 필요한 정보는 복구 뒤 보완하는 장면을 지원 목표로 둔다. 비활성 여행의 오프라인 편집과 오프라인 여행 생성은 이 모델의 지원 범위가 아니다. 통화는 자동 환산 합계로 섞지 않고 통화별로 관리한다. 현재 배포 대상은 iOS이며 Android 설정의 존재를 동등한 배포·검증으로 보지 않는다.

## 함께 지킬 데이터 관계

로컬 변경과 `sync_queue` 기록은 같은 transaction에 둬 한쪽만 남는 상태를 막는다. Entity ID는 클라이언트의 `generateId()`로 만들고 서버가 수용한다. `@repo/schema`의 Zod 계약에서 client/server 타입을 추론한다. 시간은 timezone을 포함한 ISO 8601 datetime으로 저장·전송하고, 서버는 인증과 사용자 소유권을 확인한다.

삭제·비활성화는 pending sync와 soft delete·cleanup 조건을 지켜 아직 서버에 반영하지 않은 입력을 보존한다. 정책상 제한은 기존 `useAppPolicy`, `PolicyErrorDisplay`, `NetworkStatusIndicator`를 통해 사용자에게 설명한다. 상세 규칙은 [rules](../../../.claude/rules/README.md)와 [guards](../../../.claude/guards/README.md)가 유지한다.

## 범위와 갱신

특정 릴리스의 완성, 실제 동기화 성공, 외부 지도·OAuth·DB의 운영 상태와 사람 acceptance는 이 문서가 보장하지 않는다. 현재 구조·확인 범위는 [구현 지도](../current/architecture.md), 선택 이유는 [Decision](../decisions/0001-selective-local-first.md)에 있다. 후속 제품 리팩토링의 목표와 범위는 아직 선택되지 않았다.

제품·domain 의미를 바꾸는 책임자가 관련 자료와 함께 갱신한다. 위 지원 경계나 불변식이 바뀌거나 상세 Owner와 충돌하면 재검토한다. 2026-09-09 기준 원자료를 확인했고, 특정 Workspace의 이식 완료를 Project 제품 완료로 올리지 않는다.
''')
put('context/project/current/README.md','''# Noline의 현재 구현 맥락

[구조·지원·검증 지도](architecture.md)는 현재 구현 책임과 증명 범위를 보여 준다. 목적과 지속 제약은 [common](../common/README.md), 조건부 실행 판단은 [guidance](../guidance/README.md)가 맡는다.

구현·설정·테스트를 바꾸는 책임자가 관련 상세 Owner를 대조해 갱신한다. 코드나 검증 경로가 달라지면 이 지도는 stale 후보이며 과거 pass를 현재 사실로 유지하지 않는다.
''')
put('context/project/current/architecture.md','''# 현재 구현과 검증 경계

작업 범위와 영향을 받을 책임, 실제로 확인할 명령을 정할 때 읽는다. 2026-09-09 `b4ed41f6`의 제품 tree, root guide·package 구성과 아래 상세 Owner를 대조했다. 이번 이식에서 제품 코드는 바꾸지 않았으며 앱 전체 동작을 재실행한 사실은 없다.

## 구성과 흐름

[client](../../../apps/client/CLAUDE.md)는 React Native·Expo 화면, FSD entity/data/repository 구조, SQLite와 활성화·정책 UI를 맡는다. [server](../../../apps/server/CLAUDE.md)는 Express route, 인증·user scope, PostgreSQL/Drizzle와 sync endpoint를 맡는다. [schema](../../../packages/schema/CLAUDE.md)는 Zod entity/request/response/sync 계약을, [UI](../../../packages/ui/CLAUDE.md)는 domain logic과 분리된 공유 primitive를 맡는다. pnpm workspace가 각 package의 개발·검증 명령을 연결한다.

Trip·Schedule·Expense의 data hook은 repository를 호출하고 repository의 Activation Router가 local/remote 구현을 고른다. Trip 자체 query와 child entity query는 활성 판단 단위가 다르므로 실제 변경에서는 [Activation Router rule](../../../.claude/rules/activation-router.md)을 확인한다. 활성화된 여행은 SQLite와 queue를 사용하고, Sync Engine은 queue에 남은 변경을 서버로 보낸다. Router의 데이터 위치 선택과 Sync Engine의 동기화 수행은 다른 책임이다.

실제 sync source는 [engine](../../../apps/client/src/shared/services/sync/engine.ts), [queue](../../../apps/client/src/shared/services/sync/queue.ts), [cleanup job](../../../apps/client/src/shared/services/sync/cleanup-job.ts)에서 찾는다. 비활성화 시 pending task가 있으면 cleanup을 미루는 모델을 따른다. 지도·검색·길찾기는 [Policy 설명](../../../.claude/context/policy-architecture.md)을 따르며 Data Router를 확대 적용하지 않는다.

## 지원 경계와 확인 방법

제품 문서는 iOS 중심 배포, 활성 여행의 오프라인 핵심 입력, 온라인 보강과 통화별 관리를 설명한다. Android 동등 지원, 외부 공급자·운영 DB 상태, 실제 네트워크 전환·동시 sync의 성공은 이번 source 대조만으로 확인되지 않는다. 기능별 현재 여부는 해당 source와 실제 환경에서 다시 판정한다.

제품 변경은 해당 app/package guide에서 검증을 선택한다. `pnpm schema build`, `pnpm server typecheck`, `pnpm server build`는 package 수준 확인이며 iOS 실기기나 외부 서비스 acceptance를 대신하지 않는다. `pnpm harness:check`는 AI 지침의 bridge·링크·expected surface·whitespace를 확인한다. Python Harness tests는 Recover·Maintain·Verify 계약을 임시 fixture에서 확인한다. 어느 쪽도 여행 기능의 동작 테스트가 아니다.

Root [Context Harness](../../README.md)는 Project layer와 Workspace Spec·Ticket·state를 연결한다. Noline의 `.claude/skills/` 원본은 `.agents/skills/` bridge로 공유한다. Codex·Claude lifecycle wrapper가 설치돼 있지만 새 session은 unbound이며 hook trust·사용자 explicit activation·실제 event receipt 전에는 `activation_pending`이다. Claude adapter의 semantic runner는 기존 Codex 구현을 재사용한다.

상세 Owner와 코드·테스트·runtime이 바뀌면 변경 책임자가 관련 부분을 갱신한다. [기존 Noline 문서 지도](../../../.claude/README.md)와 실제 source가 이 요약에 우선하며 전체 상세 문서 최신화 여부를 이 지도만으로 주장하지 않는다.
''')
s=ref('context/project/guidance/README.md').replace('현재 default-timeout 제품 검증의 선택 문서에도 추가하지 않으며,','현재 이식 Workspace의 기본 Recover에도 추가하지 않으며,')
s+='\n## 기존 Noline 실행 기준\n\n[Rules](../../../.claude/rules/README.md), [Guards](../../../.claude/guards/README.md), [Runbooks](../../../.claude/runbooks/README.md)는 기존 작업·경로별 정책 Owner로 유지한다. 이 폴더의 설명 기준이 이들을 대체하거나 모든 작업의 필수 절차를 늘리지 않는다.\n'
put('context/project/guidance/README.md',s)
put('context/project/guidance/explanation-and-evidence-criteria.md',ref('context/project/guidance/explanation-and-evidence-criteria.md'))
s=ref('context/project/decisions/README.md').replace('[`0001-default-timeout.md`](0001-default-timeout.md): 기본 timeout을 `5000`밀리초로 정한 이유와 해당 값의 normative Owner','[`0001-selective-local-first.md`](0001-selective-local-first.md): Selective Local-First의 선택 의미와 상세 결정 접근점')
s+='\nNoline의 기존 [상세 Decision Owner](../../../.claude/decisions/)는 그대로 유지한다. 중요한 하네스 선택도 기존 Owner에 기록하고 여기에는 관련 재진입 경로를 연결한다.\n'
put('context/project/decisions/README.md',s)
put('context/project/decisions/0001-selective-local-first.md',get('context/project/decisions/0001-selective-local-first.md')+'\n## 현재 authority와 재검토\n\n현재 제품 의미는 [common](../common/product.md), 구현 경계는 [current](../current/architecture.md)에서 읽는다. 이 문서는 선택 이유의 요약이며 상세 rule·code의 Owner를 대체하지 않는다. 활성 여행의 범위, 오프라인 편집 정책 또는 데이터·서비스 소유 구분을 바꾸는 요구가 생기면 기존 상세 결정과 함께 재검토한다. 당시 자료에 없는 대안·불확실성을 새로 꾸며 기록하지 않는다.\n')
print('saved payload phase 1')
# Initial installation memory is retained byte-for-byte as selected prior source.
removed=[]
for name in ['01-goal.md','02-constraints.md','03-project-context.md']:
 old=f'{W}/current/memory/{name}'
 put(f'{W}/source/prior-memory/{name}.txt',get(old))
 removed.append(old)
put(f'{W}/current/memory/index.md',ref('context/work/workspaces/001-default-timeout/current/memory/index.md'))
put(f'{W}/current/memory/spec/01-problem-goal-scope.md','''# 문제·목표·범위

기존 Noline Context Harness 이식 작업을 이어 최신 Reference의 Project layer, Spec·Ticket, Recover·Maintain과 운영 skill을 보완한다. 첫 이식의 상세 Owner 보존과 default-unbound 연결은 유지한다. 다음 작업자가 필요한 Project 맥락과 이번 작업의 결과·남은 판단을 구별해 복구하는 것이 목표다.

사용자는 최신 이식을 승인하면서 기존 문서 전체 정비는 제외했고, 지나친 제약을 추가하지 말라고 했다. 기존 상세 `.claude/context/rules/guards/runbooks` 전면 재작성과 제품 리팩토링은 범위 밖이다. 후속 리팩토링의 구체 목표는 아직 정하지 않았다.

이 Work는 기존 active `001-noline-context-harness-application`을 이어간다. 새 제품 작업을 대신 만들거나 active id를 바꾸지 않는다.
''')
put(f'{W}/current/memory/spec/02-behavior-and-cases.md','''# 요구 동작과 대표 사례

새 주체가 명시 id로 Recover하면 Noline의 제품 의미와 현재 구현·검증 경계, 이식 작업 Spec 전체와 Ticket 색인·현재 상태·output 지도를 읽는다. id가 없으면 기존 active Workspace를 사용하며 두 선택의 결과 내용이 대응해야 한다. 상세 source·records 전체와 Ticket 본문은 필요할 때 선택한다.

기존 flat Project 문서를 현재 입력으로 반복 소비하지 않고 새 layer를 선택한다. 이전 목표·제약 원문은 source에 바이트를 보존하되 Spec과 중복되는 현재 작업 정의로 읽히지 않는다.

기존 Noline dispatcher·agents·Claude adapter와 두 host wrapper는 계속 존재해야 한다. 새 session은 Workspace를 자동으로 선택하지 않고, unbound status 조회는 runtime이나 Workspace write를 만들지 않는다. 실제 activation은 Main의 사용자 선택과 host trust 이후 별도다.

Verify pass는 구조 검사 결과로만 읽는다. 제품 기능 성공이나 후속 리팩토링 효과, 사람 acceptance로 확대하지 않는다.
''')
put(f'{W}/current/memory/spec/03-concepts-and-contracts.md','''# 핵심 개념·입출력 계약

Project common은 여러 Work의 제품 의미, current는 교체되는 구현 현실, guidance는 조건부 판단을 맡는다. 상세 Noline 제품·규칙 Owner는 기존 위치에 남는다. Decision은 선택의 이유·재검토 신호를 보존하며 현재 답을 기본적으로 대신하지 않는다.

Work당 하나의 Spec을 다섯 파일에 나누고 실행 범위·설계·진행·결과는 필요한 Ticket에 둔다. 전체 상황과 다음 행동은 state가 맡는다. 내용과 유지 책임은 [Spec·Ticket canonical](../../../../SPEC-AND-TICKETS.md)을 따른다.

`workspace.json`은 identity, `recover.json`은 Project 문서 선택·이유, `verify.json`은 claim·basis·argv·evidence, `status.json`은 마지막 Verify result와 receipt cursor를 소유한다. Recover가 실행 시 계산하는 freshness는 선언 snapshot의 현재 일치만 의미한다. `output/index.md`는 사람이 찾을 실제 산출물 지도로 machine 결과의 정본이 아니다.

Reference source는 `87d21023f6acd8ae709322d48da9851594f9acb0`, target preflight는 `b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4`이다. 상세 적용과 증거는 [기록](../../../records/README.md)에서 선택한다.
''')
put(f'{W}/current/memory/spec/04-quality-and-completion.md','''# 품질·완료 판단

선택한 Project 문서만 읽어 Noline의 사용자 장면·목적·데이터 관계·현재 지원과 proof 경계를 설명할 수 있어야 한다. 상세 Owner와 내용이 맞고, 기존 사용자 파일과 제품 코드·Noline 전용 연결이 보존돼야 한다.

최신 Spec·Ticket을 explicit/default Recover가 읽고 Maintain의 해당 쓰기 경계가 관련 test에서 확인돼야 한다. 여섯 Reference skill의 원본·frontmatter·호출 설정·상대 bridge·canonical과 공통 기준 링크를 확인한다. 관련 tests에서 전체 Harness tests와 임시 validation으로 넓히고, 구조 검사·Verify·후속 Recover를 실제로 실행한다.

기존 descendant timeout의 timing failure가 재현되면 숨기거나 테스트를 약화하지 않고 원본 로그와 범위를 남긴다. 파일 존재·test 통과는 의미 판단의 충분성, 실제 skill discovery·invocation·문서 반영 또는 host trust·event delivery를 증명하지 않는다. 구현자가 아닌 reviewer가 원자료·diff·증거를 대조한 뒤 남은 판단을 Main에게 돌린다.

사람 acceptance, Workspace 완료·보관과 target commit은 별도다. 제품 기능 변경·제품 검증과 후속 리팩토링 효과 평가도 이번 구조 검사로 완료하지 않는다.
''')
put(f'{W}/current/memory/spec/05-constraints-design-assumptions.md','''# 제약·현재 설계·가정

기존 사용자 파일과 상세 canonical, `noline-work`, `noline-*` report-only agents, Claude adapter·test·settings·wrappers를 보존한다. `.claude/skills/`가 원본이고 `.agents/skills/`가 상대 bridge인 Noline 모델을 유지한다. 여섯 Reference skill을 같은 모델에 적응하며 별도 `.codex/skills/`를 만들지 않는다.

승인 범위는 최신 이식이며 기존 문서 전체 정비·제품 리팩토링은 제외한다. 나머지 구성·구현·검증은 현재 Owner와 실제 근거를 보고 정한다. 기존 Project flat 본문은 현재 authority를 내려 원문을 보존하고 필요한 사실을 layer에 재서술한다. 옛 goal·constraints는 source에 보존하고 Spec이 현재 정의를 맡는다.

Target branch·index·기존 runtime을 바꾸거나 host trust·session activation을 실행하지 않는다. `.codex/maintain-runtime/`·`.claude/maintain-runtime/`의 private payload를 기록에 복제하지 않는다. 새 session은 default-unbound다. 자동 연결이 없을 때 허용된 문서 반영은 Maintain 수동 fallback을 따르며 설치·접수와 실제 반영을 구별한다.

정적 bridge·설정 검사로 실제 host discovery를 알 수 있다는 가정은 하지 않는다. 후속 리팩토링으로 효과를 평가할 때 이식·맥락 정비 비용과 제품 코드 출발 상태를 함께 보존한다.
''')
put(f'{W}/current/memory/project-context.md','''# 선택한 Project 맥락

[Project README](../../../../../project/README.md)는 common/current/guidance와 Decision의 책임을 찾는 안정된 진입점이다. [제품 기준](../../../../../project/common/product.md)은 Noline의 사용자 장면과 보존할 데이터 관계를, [현재 구현 지도](../../../../../project/current/architecture.md)는 상세 Owner·실행 흐름·검증 상한을 설명한다. [Selective Local-First 결정](../../../../../project/decisions/0001-selective-local-first.md)은 기존 선택의 이유를 연결한다.

선택·이유의 machine canonical은 [recover.json](../../recover.json)이다. 설명 기준은 이 이식의 기본 Recover 입력이 아니며 해당 스킬의 조건이 맞을 때 읽는다. 상세 `.claude` 문서 전체·source·records·Ticket 본문은 필요한 것만 추가 선택한다.
''')
put(f'{W}/current/memory/tickets/index.md','''# 실행할 Ticket

- [최신 Context Harness 보완](001-upgrade.md): 기존 Noline 이식의 책임과 입력을 최신 Reference에 맞추고 보존·검증 근거를 남긴다.

진행과 실제 결과는 Ticket 본문이 소유한다. 아직 정하지 않은 제품 리팩토링 Ticket은 만들지 않았다.
''')
put(f'{W}/current/memory/tickets/001-upgrade.md','''# 최신 Context Harness 보완

## 맡은 결과와 범위

기존 설치에서 최신 Project layer·Decision, Spec·Ticket, Recover·Maintain과 여섯 운영 skill을 사용할 수 있게 한다. 기존 사용자 작업·Noline 제품 및 도구별 연결을 유지한다. 범위와 보존 조건은 Spec을 따른다.

## 실행 맥락과 접근

Source `87d2102`와 target `b4ed41f6`에서 시작했다. 현재 detailed `.claude` Owner를 옮기지 않고 Project layer에 필요한 사실을 재서술한다. 최신 실행 계약은 원본 책임 파일을 가져오고 Noline 전용 Claude adapter와 기존 bridge를 보존한다. 이전 설치는 `f0bada9`를 사용했다. 이전 일회성 준비물은 사라져 fresh preflight를 다시 확보했다.

## 완료 조건과 확인 방법

관련·전체 Harness tests, bridge·링크·skill checks, explicit/default Recover, Verify 입력 범위와 후속 freshness, 보호 대상 hash를 대조한다. 이식 의미와 보존을 독립 reviewer가 확인한다. 실제 host discovery·activation과 제품 acceptance는 별도 확인이다.

## 현재 상태와 실제 결과

최신 파일과 문서 전환을 준비했다. 적용·실행 결과는 [2026-09-09 적용 기록](../../../records/2026-09-09-01-reference-upgrade.md)에 남긴다. 이 본문은 최종 검증·독립 검토 결과를 받은 뒤 갱신한다.
''')
rec=json.loads(get(f'{W}/recover.json'));rec['schema_version']=6
rec['project_context']=[{'path':p,'reason':r} for p,r in [
 ('context/project/README.md','물리 layer와 authority, 내용 복원·갱신 계약을 찾는다.'),
 ('context/project/common/product.md','Noline 사용자 장면과 데이터 관계·지원 경계를 이식에서 보존한다.'),
 ('context/project/current/architecture.md','현재 제품·Harness Owner와 검증 상한을 구별한다.'),
 ('context/project/decisions/0001-selective-local-first.md','기존 데이터·서비스 책임 선택의 이유를 확인한다.')]]
jput(f'{W}/recover.json',rec)
put(f'{W}/README.md',get(f'{W}/README.md').replace('최초 적용하는 작업을 소유한다.','최초 적용하고 최신 Reference로 보완하는 같은 작업을 소유한다.').replace('목표·제약·선택한 Project context','Spec·Ticket·선택한 Project context'))
put(f'{W}/source/index.md',get(f'{W}/source/index.md')+'''\n## 2026-09-09 보완의 선택 원자료

옛 memory의 [goal](prior-memory/01-goal.md.txt), [constraints](prior-memory/02-constraints.md.txt), [Project 선택](prior-memory/03-project-context.md.txt)은 전환 전 바이트를 보존한다. 현재 Work 정의가 아니며 최초 이식의 범위·근거를 되짚을 때만 읽는다. 새 preflight 기계 증거는 [records/receipts/preflight/](../records/receipts/preflight/)에 둔다.
''')
put(f'{W}/current/state/index.md','''# 현재 이식 상태

2026-09-09 기존 이식 HEAD `b4ed41f6`에서 최신 Reference `87d2102` 보완을 진행 중이다. Project layer·Spec·Ticket·운영 skill과 Recover·Maintain을 함께 전환하며 제품 리팩토링은 아직 선택하지 않았다. 상세 실행 결과와 보호 근거는 [적용 기록](../../records/2026-09-09-01-reference-upgrade.md)에서 확인한다.

다음 행동은 적용된 파일의 검증과 독립 검토다. Codex·Claude hook은 설치돼 있지만 actual-host trust·explicit activation·같은 generation의 runtime event receipt가 확인되지 않아 `activation_pending`이다. Preflight에서 두 host runtime 디렉터리는 없었다.

[status.json](status.json)은 마지막 Verify result·receipt cursor·시각만 소유한다. [verify.json](../../verify.json)은 claim·basis·argv·evidence를, [recover.json](../../recover.json)은 Project 선택을, [workspace.json](../../workspace.json)은 identity를 맡는다. Recover가 계산하는 freshness는 선언 snapshot의 현재 일치이며 사람용 상태의 최신성이나 undeclared input을 증명하지 않는다.

후속 리팩토링 목표·효과 평가, 실제 host skill discovery·invocation·문서 유지 흐름, 제품 기능과 사람 acceptance, commit·Workspace 완료는 아직 수행한 결과가 아니다.
''')
put(f'{W}/output/index.md',get(f'{W}/output/index.md').replace('여러 Workspace가 공유하는 Noline common context','Noline의 common/current/guidance와 Decision')+'''\n- [운영 skill 색인](../../../../../.claude/skills/README.md): 여섯 Reference skill과 기존 dispatcher의 원본·호출 조건·bridge\n- [Spec·Ticket 계약](../../SPEC-AND-TICKETS.md): Work 정의·실행·유지 책임의 canonical\n\n현재 설치 결과와 검증 범위는 [적용 기록](../records/2026-09-09-01-reference-upgrade.md)이 연결한다.\n''')
# Add narrow routing to existing Noline owners.
put('CLAUDE.md',get('CLAUDE.md')+'''\n## Context Harness 운영 진입\n\n- `context/work/`의 Workspace·Harness를 다룰 때 [Work 지침](context/work/AGENTS.md)을 먼저 읽는다.\n- Project 의미·현재 구현·조건부 기준은 [Project 계약](context/project/README.md)을 따른다. 여러 Work에 계속 유효할 변화나 누락 복원은 [update-project-context](.claude/skills/update-project-context/SKILL.md)로 연결한다.\n- 작업 생성·논의·재판단·작업물 설명·설명 복구는 [skill 색인](.claude/skills/README.md)의 각 호출 조건을 따른다. 새 독립·후속 Workspace 생성에는 create-context-workspace를 사용하고 기존 Workspace 수정에는 다시 호출하지 않는다.\n- Spec·Ticket·state와 Main·Maintain의 역할은 [운영 기준](context/work/workspaces/SPEC-AND-TICKETS.md)이 소유한다. 스킬 호출을 session activation이나 실제 문서 반영으로 간주하지 않는다.\n- Maintain 연결·전환·해제는 [session binding 계약](context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md)을 따른다. Main은 사용자가 명시한 현재 session에만 control을 실행하며 subagent에게 위임하지 않는다. active index나 대화 주제로 binding을 추론하지 않는다.\n''')
put('context/README.md',get('context/README.md').replace('Noline의 제품 목적·구조·제약·채택 결정을 실제 내용으로 정리하는 Project common context','Noline의 지속 의미·현재 구현·조건부 기준을 common/current/guidance 물리 layer로 나누고 Decision을 연결하는 Project context'))
put('context/work/README.md',get('context/work/README.md')+'\nWorkspace의 Work당 Spec 하나, 실행할 Ticket과 Main·Maintain의 유지 관계는 [Spec·Ticket 계약](workspaces/SPEC-AND-TICKETS.md)을 따른다.\n')
put('.claude/harness/README.md',get('.claude/harness/README.md')+'''\n## Context Harness 보완\n\n[Project layer](../../context/project/README.md)와 [Spec·Ticket](../../context/work/workspaces/SPEC-AND-TICKETS.md)이 지속 내용과 유지 책임을 소유한다. [운영 skill 색인](../skills/README.md)은 생성·Project 갱신·논의·재판단·작업물 설명·설명 복구를 연결한다. `.claude/skills/` 원본과 `.agents/skills/` 상대 bridge를 유지하며 기존 dispatcher·agents와 각 host adapter를 대체하지 않는다. 적용 선택은 [2026-09-09 Decision](../decisions/2026-09-09-context-harness-upgrade.md)에 있다.\n''')
put('.claude/decisions/2026-09-09-context-harness-upgrade.md','''# Decision: Context Harness 보완

2026-09-09 사용자가 기존 설치를 최신 이식 skill로 보완하도록 승인했다. 기존 상세 문서 전체 정비와 제품 리팩토링은 제외하고 기존 사용자 작업·Noline 고유 연결을 보존한다.

Project의 지속 의미·현재 현실·조건부 기준을 물리 layer로 분리하고 기존 flat 본문은 현재 authority에서 내려 원문을 보존한다. active 이식 Workspace는 새 제품 계획을 만들지 않고 최신 Spec·Ticket으로 이어간다. 이전 goal·constraints 원문은 해당 Workspace source에 보존한다.

Reference skill은 Noline의 `.claude/skills/` 원본과 `.agents/skills/` 상대 bridge에 적응한다. 동등 내용을 별도 `.codex/skills/`에 중복 설치하지 않는다. 기존 Claude hook·test·settings·wrappers·agents를 유지하고 최신 Recover·Maintain 계약을 함께 올린다.

기존 상세 Owner 전체를 지금 재작성하면 승인 범위와 후속 리팩토링의 출발 상태가 불필요하게 달라지므로 필요한 Project 재서술과 운영 연결만 바꾼다. 이 선택은 상세 문서가 모두 최신이라는 판정이 아니다. 실제 후속 작업에서 충돌이 확인되거나 제품 책임·지원 경계가 바뀌면 관련 Owner만 다시 대조한다.

[적용 Workspace 기록](../../context/work/workspaces/001-noline-context-harness-application/records/2026-09-09-01-reference-upgrade.md)이 source 판본·검증·미확인을 소유한다. 설치가 host activation·제품 acceptance·commit을 뜻하지 않는다.
''')
# The regular-file closure excludes Git/index content; default full check remains unchanged.
s=get('scripts/check-harness.mjs').replace("const expectedSkills = ['create-context-workspace', 'noline-work'];", "const expectedSkills = ['noline-work', "+', '.join(repr(x) for x in SKILLS)+'];')
s=s.replace("checkOnlyEntries('.claude/skills', expectedSkills);", "checkOnlyEntries('.claude/skills', [...expectedSkills, 'README.md']);").replace("checkOnlyEntries('.agents/skills', expectedSkills);", "checkOnlyEntries('.agents/skills', [...expectedSkills, 'README.md']);")
s=s.replace("  checkSymlink('.agents/skills/noline-work', '../../.claude/skills/noline-work');\n  checkSymlink('.agents/skills/create-context-workspace', '../../.claude/skills/create-context-workspace');", "  for (const name of expectedSkills) {\n    checkSymlink(`.agents/skills/${name}`, `../../.claude/skills/${name}`);\n  }")
s=s.replace("    'context/project/overview.md',", "    'context/project/common/README.md',\n    'context/project/current/README.md',\n    'context/project/guidance/README.md',\n    'context/project/decisions/README.md',")
s=s.replace("    'context/work/workspaces/CREATE-AND-TRANSITION.md',", "    'context/work/workspaces/CREATE-AND-TRANSITION.md',\n    'context/work/workspaces/SPEC-AND-TICKETS.md',")
s=s.replace('checkGitDiffWhitespace();', "// Durable Verify snapshots regular inputs; Git/index whitespace is checked by the default run.\nif (!process.argv.includes('--no-git-diff')) checkGitDiffWhitespace();")
put('scripts/check-harness.mjs',s)
(HERE/'removed.json').write_text(json.dumps(removed,indent=2)+'\n')
(HERE/'symlinks.json').write_text(json.dumps({f'.agents/skills/{n}':f'../../.claude/skills/{n}' for n in SKILLS if n!='create-context-workspace'},indent=2)+'\n')
print('saved payload phase 2')
put(f'{W}/records/receipts/preflight/preflight-20260909T140507056185Z-f1caf35fc6894327a7d811ffd7622f3c.json',(HERE/'preflight.json').read_text())
put(f'{W}/records/2026-09-09-01-reference-upgrade.md','''# 최신 Reference 보완 적용

2026-09-09 사용자가 승인한 범위에서 기존 Context Harness를 보완한다. Source `87d21023f6acd8ae709322d48da9851594f9acb0`의 Reference는 clean이며 target은 `feat/noline-context-harness`, `b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4`에서 시작한다. 이전 설치는 `f0bada9`를 사용했다. 사라진 이전 준비물을 재사용하지 않고 새 preflight를 확보했다.

## 적용과 보존

Project common/current/guidance와 Decision 계약을 구성하고, 기존 active 이식 Work를 Spec 다섯 파일·Ticket으로 이어간다. 최신 Recover·Maintain 원본의 변경분과 tests를 적용하되 Noline Claude adapter·settings·wrappers와 기존 agents·dispatcher는 유지한다. 여섯 Reference skill은 `.claude/skills/` 원본과 `.agents/skills/` 상대 bridge에 적응한다.

기존 상세 문서 전체 정비와 제품 리팩토링은 하지 않는다. Flat Project 본문은 전환 안내 뒤에 원문을 보존하고 현재 authority에서는 내려왔다. 이전 memory 세 파일의 바이트는 [prior-memory](../source/prior-memory/)에 보존한다. [Fresh preflight](receipts/preflight/preflight-20260909T140507056185Z-f1caf35fc6894327a7d811ffd7622f3c.json)는 기존 untracked 18개 entry를 보호 목록으로 고정한다. Private 원문은 해석·복제하지 않았다.

Active/default 및 변경 대상 consumer는 `001-noline-context-harness-application` 하나다. Preflight에서 두 host runtime 디렉터리가 없어 current-generation bound consumer는 관찰되지 않았다. 이 Workspace의 Project 선택·memory·state·output을 reconcile하며 active id는 바꾸지 않는다.

## 검증 입력과 상한

직접 `node scripts/check-harness.mjs`는 기존 Git whitespace 확인까지 유지한다. Durable Verify는 `node scripts/check-harness.mjs --no-git-diff`로 regular-file 검사를 실행한다. 그 명령이 읽는 모든 현재 Markdown 본문, 설정·agent 본문과 검사 스크립트를 evidence로 선언한다. Package manager·lockfile·compiler·제품 소스는 이 argv가 실행하지 않으므로 그 내용을 검증했다고 하지 않는다.

Symlink의 연결과 directory membership·링크 target 존재는 실행 당시 관찰이며 regular-file snapshot freshness가 이후 topology의 동일성을 보장하지 않는다. Git HEAD·index·whitespace는 별도 직접 검사 결과다. 새 Markdown이나 entry가 추가되면 Verify 입력 closure를 다시 구성하고 실행해야 한다. Node/OS와 외부 상태는 snapshot할 제품 입력이 아니다. Receipt는 선언 snapshot과 해당 실행 사건에만 한정한다.

Harness 테스트는 별도 [Harness test receipt](receipts/harness-tests/)에서 보존하고 Product Verify의 구조 검사와 구별한다. Ephemeral validation은 임시 fixture만 사용한다. 기존 descendant timeout timing failure는 원본 test를 바꾸지 않고 실제 결과로 남긴다.

## 현재 결과

적용 파일과 검증을 진행 중이며 실제 결과를 회수한 뒤 이 절을 갱신한다. 독립 reviewer가 원자료·target diff·증거를 직접 대조한다. 실제 target-root skill discovery·invocation·Main 결과 전달·문서 유지와 Codex/Claude host trust·explicit activation·event receipt는 미확인이다. Maintain 상태는 `activation_pending`이며 새 session default-unbound를 유지한다. Stage·commit·branch 변경·제품 acceptance·Workspace 완료는 수행하지 않는다.
''')
put(f'{W}/records/README.md',get(f'{W}/records/README.md')+'\n- [2026-09-09 최신 Reference 보완](2026-09-09-01-reference-upgrade.md): 적용 범위·보존·검증 입력과 실제 결과\n')
put(f'{W}/records/receipts/harness-tests/README.md','# Harness test receipt\n\n최신 보완의 target Harness source snapshot과 실제 단위·회귀 검사 결과를 이 폴더에 보존한다. Product Verify receipt와 사람 acceptance를 대신하지 않는다.\n')
# Resolve the command's regular content reads (directory/topology observations stay a proof ceiling).
active=['CLAUDE.md','README.md','START_GUIDE.md','.claude/README.md','.claude/harness','.claude/audits/2026-05-06-harness-execution-plan.md','.claude/skills','.claude/agents','.claude/rules','.claude/guards','.claude/runbooks','.claude/context','.claude/decisions','context','apps/client/CLAUDE.md','apps/server/CLAUDE.md','packages/schema/CLAUDE.md','packages/ui/CLAUDE.md']
evidence=set()
for base in [TARGET,PAYLOAD]:
 for name in active:
  p=base/name
  if not p.exists(): continue
  for f in ([p] if p.is_file() else p.rglob('*.md')):
   if f.is_file() and f.suffix=='.md' and not f.is_symlink(): evidence.add(str(f.relative_to(base)))
evidence.difference_update(removed)
evidence.update(['scripts/check-harness.mjs','.codex/maintain.json','.claude/settings.json'])
for n in ['noline-context-collector','noline-harness-observer','noline-policy-checker']:
 evidence.add(f'.codex/agents/{n}.toml')
# Include callable skill definitions, root routing and wrappers/configuration in the installation record as supporting inputs.
for p in (PAYLOAD/'.claude/skills').rglob('openai.yaml'): evidence.add(str(p.relative_to(PAYLOAD)))
evidence.update(['.codex/config.toml','.codex/hooks.json','.codex/hooks/maintain.py','.claude/hooks/maintain.py',f'{W}/recover.json',f'{W}/verify.json'])
v=json.loads(get(f'{W}/verify.json'))
v['claim']='Noline의 현재 지침·Context Harness regular input과 실행 시 관찰한 bridge·경로 구조가 정해진 구조 검사를 통과한다. 선언 파일 freshness는 이후 directory·symlink topology, Git index 또는 제품 동작을 증명하지 않는다.'
v['canonical_basis']=['.claude/harness/README.md','.claude/decisions/2026-09-09-context-harness-upgrade.md',f'{W}/current/memory/spec/04-quality-and-completion.md']
v['verification']['argv']=['node','scripts/check-harness.mjs','--no-git-diff']
v['verification']['evidence_paths']=sorted(evidence-set(v['canonical_basis']))
jput(f'{W}/verify.json',v)
# Persist exact intent and preimages, including ignored/existing ancestor checks.
links=json.loads((HERE/'symlinks.json').read_text())
allpaths=sorted({str(p.relative_to(PAYLOAD)) for p in PAYLOAD.rglob('*') if p.is_file()}|set(removed)|set(links))
def stamp(p):
 if p.is_symlink():return {'kind':'symlink','target':os.readlink(p)}
 if p.is_file():return {'kind':'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size}
 if p.is_dir():return {'kind':'directory'}
 return {'kind':'absent'}
items=[]
for name in allpaths:
 current=stamp(TARGET/name)
 if name in links and current['kind']!='absent': raise ValueError(('unexpected skill conflict',name,current))
 ancestors=[]
 for p in (TARGET/name).parents:
  if p==TARGET: break
  state=stamp(p);ancestors.append({'path':str(p.relative_to(TARGET)),**state})
  if state['kind'] not in ['absent','directory']:raise ValueError(('ancestor collision',name,state))
 ignored=subprocess.run(['git','check-ignore','--no-index',name],cwd=TARGET,capture_output=True,text=True).returncode==0
 if ignored:raise ValueError(('ignored payload collision',name))
 items.append({'path':name,'before':current,'action':'remove-after-byte-copy' if name in removed else 'symlink' if name in links else 'write','after':{'kind':'symlink','target':links[name]} if name in links else {'kind':'absent'} if name in removed else stamp(PAYLOAD/name),'ancestors':ancestors,'ignored':ignored})
pre=json.loads((HERE/'preflight.json').read_text());dirty={e['path'] for e in pre['git']['dirty_entries']}
assert not dirty.intersection(allpaths)
jput(f'{W}/records/receipts/application/paths-20260909.json',{'source_commit':'87d21023f6acd8ae709322d48da9851594f9acb0','target_head':'b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4','items':items,'protected':pre['git']['dirty_entries'],'runtime_directories_present':False,'evidence_regular_files':len(evidence)})
(HERE/'paths.json').write_text(json.dumps({'items':items,'protected':pre['git']['dirty_entries']},ensure_ascii=False,indent=2)+'\n')
(HERE/'manifest.md').write_text('''# Noline 재이식 manifest

사용자가 승인한 동일 범위를 fresh preflight로 다시 고정했다. Source `87d2102` Reference clean, target `feat/noline-context-harness @ b4ed41f6`. Exact new/modify/remove-after-copy paths, old/new hashes, actual ancestor kind·ignore 확인은 paths.json이 소유한다. 보호 18개 entry와 payload 교집합은 없다. 기존 untracked 18개 entry를 유지한다. Session runtime은 양 host 모두 없다.

Source Work·Workspace·Recover·Maintain·Verify 계약 변경분은 동일 경계에 설치한다. 기존 Noline Claude 설명·role 이름·adapter·tests·settings·wrappers는 보존한다. 최신 Python runtime·tests는 원본과 동일하며 sample 제품·Workspace·receipt는 제외한다. Work 지침의 제품 경로·검증 명령만 Noline에 적응한다.

Project common/current/guidance와 Decision root는 설치·적응한다. common/product는 root guide·제품 README·Selective Activation 상세 Owner의 사용자 장면·데이터 불변식·범위를 재서술한다. current/architecture는 app/package 경계·Router/Sync/Policy 흐름·검증 상한을 재서술한다. guidance는 기존 rules/guards/runbooks Owner를 유지하고 공동 설명 기준을 조건부 설치한다. 본문이 없는 layer는 없다. 기존 flat 파일은 본문을 그대로 유지한 채 현재 authority에서 내렸음을 안내한다.

여섯 Reference skill은 `.claude/skills/<name>/`에 원본을 두고 `.agents/skills/<name>` 상대 bridge로 적응한다. 기존 create-context-workspace는 갱신하고 나머지 다섯을 추가한다. noline-work와 noline agents는 보존한다. Reference의 별도 `.codex/skills/` alias는 Noline discovery model과 중복되어 제외한다. 각 frontmatter/openai.yaml, root router·색인·canonical·공동 guidance 연결을 검사한다. 정적 설치를 실제 discovery·invocation으로 보고하지 않는다.

기존 active 001 이식 Workspace를 schema 6·Spec 다섯 파일·Ticket 하나로 적응한다. 이전 memory는 source/prior-memory에 원문 바이트를 보존하고 옛 current 세 파일만 내린다. Root README와 common/product·current/architecture·기존 Decision을 Recover에 선택한다. Guidance는 설명 스킬의 조건에서 선택하므로 기본 입력에서 제외한다. 제품 리팩토링은 계획하지 않는다. Machine preflight·path manifest·Harness tests는 records/receipts/<종류>에 둔다.

검사기는 새 skill 허용 목록·Project 진입과 Spec 계약을 맞추고 --no-git-diff를 추가한다. 기본 직접 검사는 동일 Git whitespace 확인을 유지한다. Verify는 regular 본문 closure를 선언하고 Git/index 검사만 직접 확인으로 분리한다. Symlink·directory membership·linked target 존재의 미래 동일성은 freshness가 증명하지 않는다는 ceiling을 claim과 기록에 둔다. 명령은 pnpm·lockfile·compiler나 제품 source를 실행하지 않는다.

검증은 관련 unit → 전체 Harness suite·ephemeral validation, local link lexical/resolved·semantic review, skill shape/bridge, all live consumer explicit/default Recover, Verify→Recover, 보존 hash 대조다. 신규 sample id/timeout residue는 test fixture 의미만 허용하고 live 내용에는 남기지 않는다. 과거 원문·기록 속 옛 Project 경로는 provenance로만 유지한다. 독립 review는 Main이 회수한다. Actual host trust/activation, 제품 acceptance, Workspace 완료·stage·commit은 범위 밖이다.

'''+ '\n'.join(f"- {i['action']}: `{i['path']}`" for i in items)+'\n')
print('saved manifest',len(items),'paths;',len(evidence),'regular evidence files')
