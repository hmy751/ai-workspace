# 2026-09-04 TripProof 실제 적용 평가

> 현재성 메모: 이 문서의 TripProof 사실 대조와 consumer drift는 후속 판단의 근거로 유지한다. 다만 `common/current/guidance`를 물리 경계로 강제하지 않고 `overview`를 선택적으로 두자는 배치 판정은 사용자 정정으로 폐기됐다. 현재 Project 구조와 검증은 [`07 물리 layer 정정 기록`](2026-09-04-07-project-context-physical-layers.md)과 `current/`를 우선한다.

## 결론

TripProof에서 실제로 가져올 만한 것은 완성된 Harness 구현 전체가 아니다. 가장 강한 결과는 다음 두 가지다.

1. **Project context의 내용 복원 방식:** 다음 관련 Work가 제품 목적·사용자 문제·domain 의미·현재 구현 경계·관련 판단 기준을 다시 추론하지 않도록 실제 제품 자료와 code/test Owner에서 내용을 재구성하고, 책임과 읽기 조건을 `context/project/README.md`에서 찾게 한 방식
2. **적용 검증의 반례:** Harness test와 제품 check가 통과해도 active Workspace의 사람용 current와 output target은 틀릴 수 있었다. Project producer만 검사해서는 부족하고, 영향을 받는 live consumer의 Recover와 의미적 재진입까지 대조해야 한다.

반면 현행 TripProof는 여러 제품 Work, Spec/Ticket, bounded brief를 현재 Workspace 구조 안에서 연속적으로 운영한 사례가 아니다. Project context maintainer의 장기 효과와 판단 continuity 개선도 증명되지 않았다. 따라서 Project 계약과 이식 acceptance는 직접 반영 후보지만, Work/Spec 관계·claim-scope review·maintainer는 pilot 후보로 남긴다.

## 조사 대상과 증거 지위

사용자가 지정한 실제 적용 대상은 `/Users/hammyeong-yeon/Desktop/10_work/tripproof`다.

- 조사 시점 branch: `chore/archive-project-harness`
- 조사 시점 HEAD: `8b1418d6e67c7897e933af3c8eaf0c76547c5d9b`
- working tree: clean
- `main`·`origin/main` 기준: `4` commits ahead, upstream 없음

즉 아래 구조는 실제 target working tree에는 존재하지만 main에 병합·push된 완료 상태는 아니다. 이번 조사는 read-only로 수행했고 TripProof 파일, private prompt/response와 외부 시스템은 변경하거나 열지 않았다. 보존된 test·receipt와 runtime metadata는 읽었지만 제품 test/eval을 다시 실행하지 않았으므로 장기 효과나 최신 제품 동작을 재검증했다고 말하지 않는다.

## 어떻게 적용했는가

### 적용 commit의 역할

- `3e9e95a` (`2026-08-19`): 당시 Reference의 Project context, 첫 Work Workspace, Recover·Maintain·Verify·validation을 설치했다.
- `9559a04` (`2026-08-30`): 평면 `overview.md`, `prd.md`, `architecture.md`를 제거하고 TripProof 실제 제품 의미와 구현 경계에 맞춘 Project 책임 구조로 재구성했다.
- `8b1418d` (`2026-08-31`): `project-context-maintainer`가 독자 정책을 소유하지 않고 Project 계약을 실행하는 얇은 보조 장치가 되도록 축소했다.

현재 Project context는 다음 책임으로 나뉜다.

- `common/product-domain.md`: 제품 목적, 사용자 문제, `Trip → Library → ChatAnswer → Card`의 domain 관계, 현재 구현과 아직 구현되지 않은 의미를 구분한다.
- `current/connected-surface.md`: 실제 UI/API/local state/storage·retrieval·conflict 경계를 code/test Owner와 연결한다.
- `current/runtime-proof-boundaries.md`: 확인 revision·시점, runtime wiring, test/eval이 증명하는 범위와 증명하지 못하는 범위, 갱신 책임을 적는다.
- `guidance/llm-evidence-changes.md`: LLM 제안, 의미 판단, code grounding, 사람 확인을 분리하고 적용·비적용·재검토·제거 조건을 둔다.
- `decisions/`: 당시 선택 이유와 재검토 신호를 보존하되, 현재 답의 Owner인지 이유 기록인지 문서 관계로 판정한다.

[`Project context 진입점`](/Users/hammyeong-yeon/Desktop/10_work/tripproof/context/project/README.md)은 물리적 디렉터리 이름보다 다음 책임을 분명히 한 점이 중요하다.

- 여러 Work에 계속 필요한 의미와 현재 구현 경계를 분리한다.
- 파생 설명보다 상세 code·test·product Owner를 우선한다.
- Project context 완료를 파일 존재나 link 유효성만으로 보지 않고, 다음 작업자가 제품 판단을 재추론하지 않아도 되는 내용 복원으로 본다.
- archive는 역사 근거이며 현재 queue나 권위로 자동 승격하지 않는다.
- 확인된 현재 Owner에서 의미를 더하지 않고 내용을 복원하는 일과 새 제품 결정을 구분한다.

### 재구성 과정에서 드러난 검증 방식

초기 구조와 첫 내용 재구성은 형식상 맞았지만 제품 목적·사용자 문제·대표 사용 장면을 충분히 복원하지 못했다. 연구 Workspace는 이를 실패로 판정하고 기존 파일명 힌트를 없앤 cold/blind 재구성을 다시 수행했다. fresh worker는 Project 계약과 실제 archive·code·test/eval에서 다른 파일 구성을 만들었고, 독립 review가 대표 장면과 관찰 exporter 설명의 결함을 찾은 뒤 수정되었다.

이 과정이 보여 준 핵심은 특정 파일명을 복사하는 것이 아니라, **새 작업자가 제한된 진입점에서 제품 판단과 현재 경계를 복원할 수 있는지**를 독립적으로 시험하는 것이다. 다만 raw worker prompt/result와 reviewer 원문이 target에 모두 보존된 것은 아니며, 최종 `PASS`는 narrative record다. 이를 machine Verify나 제품 효과 증거로 취급하지 않는다.

### 설치된 Work/Harness의 실제 범위

TripProof Work는 `current/memory`, `current/state`, `source`, `output`, `records`, receipt를 분리하고 다음 경계를 실제로 설치했다.

- Recover는 선택한 Project 문서와 bounded current·output index만 읽고 source/records 전체와 output target 본문을 자동으로 펼치지 않는다.
- Maintain은 Recover로 grounding한 같은 semantic thread에서 durable delta를 판단하고 제한된 Workspace Markdown Owner만 갱신한다.
- Verify는 상태 전환·인계 때 구체 claim, basis, evidence, argv와 append-only receipt를 연결하고 다음 Recover가 snapshot freshness를 계산하게 한다.
- Project-wide context 변화는 Workspace Maintain이 아니라 별도 project-context maintainer가 보조한다.

보존 기록에는 Harness test `90`개 통과, 첫 제품 Verify의 formatting 실패와 그 뒤 동일한 **선언 evidence snapshot hash**에서의 통과, server test `278`개와 client build 통과가 있다. 이 hash는 manifest 밖 command 입력 tree까지 같았다는 뜻이 아니다. private payload를 열지 않은 runtime metadata에서도 grounding된 session과 `no_change`·quiet update effect가 확인되어 hook에서 semantic resume와 guarded apply까지 실행된 흔적은 있다.

그러나 이것이 증명하는 것은 한 설치 Workspace에서 해당 경로가 작동했다는 것까지다. 새 제품 Workspace 생성·전환, 장기간 continuity, 중요 update나 ambiguity의 사용자 표면 전달, 모든 종료 경계, Project context가 실제 제품 판단을 개선한 효과는 증명되지 않았다.

## 현행 TripProof가 보여 준 결정적 결함

### Active Workspace reconciliation이 의미적으로 실패했다

현행 active/default Workspace는 여전히 설치 작업용 `001-project-context-harness-application`이고 `.codex/maintain.json`도 이 Workspace에 고정돼 있다. Project context 재구성 commit은 이 Workspace의 `current/memory`, `current/state`, `recover.json`, `output/index.md`를 함께 갱신했다. Machine `recover.json`은 새 `context/project/README.md`와 두 Decision을 정확히 선택한다. 그러나 사람용 current는 존재하지 않는 다음 파일을 새 책임 구조와 후속 변경 대상으로 서술한다.

- `common/product.md`
- `common/domain.md`
- `current/product.md`
- `current/architecture.md`

실제 파일은 `common/product-domain.md`, `current/connected-surface.md`, `current/runtime-proof-boundaries.md`다. 즉 과거 Workspace를 방치한 것이 아니라 reconciliation을 시도했지만, state에는 존재하지 않는 파일명을 새로 기록하고 output href는 바로잡지 않아 semantic acceptance가 실패했다.

따라서 원칙은 다음처럼 좁혀야 한다.

> 완료되어 소비 경로에서 내려온 역사 Workspace는 새 Project 구조에 역동기화하지 않는다. 그러나 영향을 받는 live consumer는 현재 선택과 target을 진실하게 유지하거나 successor로 전환해야 한다.

여기서 live consumer는 active/default Recover consumer에 한정하지 않는다. 최신 Reference처럼 Maintain이 기본 unbound이고 session별 explicit binding을 쓰는 경우에는 현재 binding된 Workspace도 포함한다. TripProof의 schema v1 고정 선택 방식을 일반 계약으로 옮기지 않는다.

### Output link가 존재 여부와 의미 모두 틀렸다

[`active Workspace output index`](/Users/hammyeong-yeon/Desktop/10_work/tripproof/context/work/workspaces/001-project-context-harness-application/output/index.md)는 Project, Work, `.codex`를 가리킨다고 설명하지만 두 link는 존재하지 않는 위치로 풀리고 하나는 존재하는 다른 상위 경계로 풀린다. 일반 local link checker는 존재하지 않는 두 개는 찾을 수 있지만, label과 실제 target이 다른 의미적 오지정은 존재 여부만으로 잡지 못한다.

따라서 이식 acceptance에는 두 검사가 모두 필요하다.

- link target이 실제로 존재하는가.
- 그 target이 label과 책임 설명이 말한 실제 Owner인가.

### Recover는 성공했지만 stale한 consumer를 성공적으로 읽었다

현행 Recover는 schema `6` packet을 정상 생성하고 Project README와 두 Decision을 선택한다. 연결된 과거 Verify receipt도 현재 snapshot과 달라 `stale`로 정확히 판정한다. 그러나 Recover 성공은 사람용 current의 제거된 파일명과 output의 잘못된 target을 검증하지 않는다.

이 반례 때문에 Project 변경 뒤 acceptance는 producer 문서 link 검사로 끝낼 수 없다. 영향을 받는 live consumer—active/default Recover consumer와 explicit session-bound Workspace—에서 실제 Recover를 실행하고, fresh reader가 packet의 선택·current·output target을 현재 canonical과 대조해야 한다.

사람용 current가 machine Owner의 역할을 정확히 설명하는지도 확인해야 한다. TripProof state는 `status.json`이 receipt freshness까지 소유한다고 적지만, status는 마지막 receipt/result cursor만 보존하고 freshness는 Recover가 실행 시 receipt snapshot과 현재 파일을 비교해 계산한다.

### Evidence manifest와 실행 입력 범위가 어긋났다

`npm run check`는 `black --check .`처럼 repository 범위의 Python 파일을 검사하지만 당시 `verify.json` evidence에는 Harness Python 입력 일부가 없었다. 실제 첫 실패 원인이 바로 그 manifest 밖 파일이었다. 과거 receipt가 fresh여도 실행 argv의 전체 입력이 같았다는 뜻은 아니다.

Verify가 arbitrary command를 허용할 때에는 claim과 evidence manifest가 실행의 실제 입력 closure보다 넓거나 좁지 않은지 확인해야 한다. 모든 입력을 열거하기 어렵다면 command 범위를 좁히거나 claim의 증명 범위를 그에 맞춰 낮춰야 한다.

### Target에 Reference 표본 잔재가 남았다

설치된 Work/Harness의 문서와 설정에는 `Reference Project`, `reference-project/`, 예시 Workspace ID와 다른 제품의 문구가 일부 남았다. 이는 구조 복제와 실제 target 의미 재구성을 구분하는 residue 검사가 필요하다는 근거다.

이식 뒤에는 source template의 Project 이름·sample ID·sample path·제거된 파일명을 검색하고, 남은 항목이 의도된 generic 문구인지 target 미적응 잔재인지 판정해야 한다.

## Reference에 가져올 것

### 계약에 직접 반영할 후보

1. **`context/project/README.md`를 안정된 필수 Recover routing anchor로 둔다.** README는 Project 책임과 실제 문서 routing을 소유한다. 그 자체가 모든 작업에 충분한 내용 payload는 아니며, 각 Workspace는 현재 작업에 필요한 common·current·guidance의 실제 문서를 이유와 함께 선택한다. `overview.md`는 프로젝트가 필요할 때 두는 선택적 파생 요약이지 모든 Project의 필수 Owner가 아니다.
2. **Project 책임 profile을 일반 계약에 넣는다.** 공통 제품·domain 의미, 현재 구현·지원 경계, 조건부 지침을 물리적 디렉터리가 아니라 주장별 역할로 사용한다.
3. **각 주장에 수명과 소비 관계를 드러낸다.** 보존 기간, 읽기 조건, 현재 권위·상세 Owner, 갱신 책임, stale·재검토 신호를 찾을 수 있어야 한다.
4. **내용·판단 recoverability를 Project context 완료 조건에 넣는다.** 다음 관련 Work가 제품 목적·사용자 문제·domain 관계·현재 경계·관련 판단 기준을 링크 밖에서 다시 추론해야 하면 구조가 맞아도 미완료다.
5. **파생 current의 proof ceiling을 드러낸다.** 확인 revision·시점, 상세 Owner, 확인한 범위, stale 신호와 updater를 함께 둔다.
6. **조건부 guidance의 lifecycle을 둔다.** 적용·비적용·재검토·제거 조건이 있고 실제 반복 행동을 바꿀 때만 유지한다.
7. **Decision의 역할을 관계로 판정한다.** 기본적으로 이유·대안·재검토 신호를 보존하되, 명시적으로 현재 normative Owner인 Decision 예외를 금지하지 않는다.

### 이식·변경 acceptance에 반영할 후보

1. Project context를 크게 재구성하면 영향을 받는 live consumer—active/default Recover consumer와 explicit session-bound Workspace—의 선택·사람용 current·output target을 함께 reconcile하거나 successor로 전환한다.
2. Project producer의 local link 검사와 별도로 실제 consumer Recover를 실행한다.
3. task-specific fixture가 README뿐 아니라 필요한 common·current·guidance 실제 문서를 선택하게 하고, fresh reader가 제한된 packet에서 제품 의미와 현재 경계를 복원하며 Project 선택과 output target이 실제 canonical을 가리키는지 확인한다. TripProof의 현행 README·Decision만 선택한 Recover는 README-only content recoverability를 증명하지 않는다.
4. link 존재성뿐 아니라 label·설명이 의도한 Owner를 가리키는지 semantic target을 확인한다.
5. source template 이름·ID·경로와 제거된 file-name residue를 target 전체에서 검사한다.
6. 큰 복원에서는 cold/blind worker와 독립 reviewer의 prompt·입력 범위·결과·수정 이유를 durable application record로 남긴다. 이것을 machine Verify와 혼동하지 않는다.
7. Verify claim·evidence·argv의 실제 입력 closure를 맞춘다. receipt freshness가 현재 Verify 계약의 claim·argv 변경까지 구분해야 하는지는 별도 contract-digest pilot로 검토한다.

현재 live [`apply-context-harness` skill](../../../../.agents/skills/apply-context-harness/SKILL.md)은 local link 검사와 link 없이 Project common 책임을 설명하는 bounded 검토를 이미 요구한다. 새 workflow를 중복해서 만들기보다, TripProof의 stale active consumer·misdirected output·template residue·evidence closure를 이 요구의 acceptance fixture로 보강하는 편이 맞다.

### 변형해서 Work 계약에 넣을 후보

TripProof의 과거 archive에는 `Spec → 구현 → 실제 eval → AC 성립·불성립 재기록` 흐름이 있었고, 구현 완료 뒤에도 실측이 나쁘면 `AC 불성립`을 남겼다. 그러나 이것은 현행 Work와 통합되지 않았고 일반 Ticket 층은 없었다.

따라서 새 고정 schema를 만들지 않고 다음 관계만 Work 계약 후보로 둔다.

- 여러 작업에 이어질 안정된 제품 계약인 Spec/issue가 실제 Project에 있으면 exact canonical과 필요한 section을 current/source에서 선택한다.
- `current/state`에는 현재 slice, 소수의 acceptance criteria와 다음 판단을 bounded brief로 둘 수 있다.
- 실제 code·test·artifact는 `output/index`가 canonical을 가리킨다.
- 실측 결과와 acceptance criteria의 성립·불성립은 records 또는 기존 Spec Owner에 환류한다.
- Ticket은 실제 Project가 사용할 때만 선택하며 Reference의 필수 층으로 만들지 않는다.

이는 TripProof에서 현재 적용·검증된 구조가 아니라 다음 successor Workspace에서 시험할 설계 후보다.

## Pilot 뒤에만 판단할 것

- **얇은 project-context maintainer:** 구조는 작고 책임 배치는 타당하지만 실제 제품 변화 뒤 유지한 증거가 없다. 일반 계약을 먼저 세운 뒤 다른 target 또는 실제 Project-wide 변화 하나에서 효과와 중복을 본다.
- **Claim-scope와 제한적 재판정:** Harness test 통과가 stale current/output을 닫지 못한 이번 사례를 첫 replay fixture로 쓰되, 별도 reviewer·trigger를 만들기 전에 Main의 범위·다음 행동이 실제로 달라지는지 본다.
- **Work/Spec 병용:** 실제 successor Workspace에서 안정된 multi-session slice 하나를 운영하고, 최소 한 번은 acceptance criterion의 불성립과 다음 Recover에서 그 판단 복원을 확인한다.
- **Maintain runtime 장기 경계:** 현재 metadata의 `no_change`, quiet update, session-end, turn만 남은 불완전 boundary를 replay corpus로 쓸 수 있지만 private payload 없이 결과 의미를 과장하지 않는다.

## 가져오지 않을 것

- TripProof의 `common/current/guidance` 물리 디렉터리를 모든 Project에 강제하는 것
- TripProof 제품 내용·수치·domain 용어와 `project-context-maintainer` 본문을 그대로 복사하는 것
- schema v1의 고정 `.codex/maintain.json`, 오래된 hook·Harness runtime을 live Reference로 역이식하는 것
- 설치 Workspace·receipt·status를 표본 정답으로 복제하는 것
- archived `spec-driven` skill, 중앙 work log와 implementation-note taxonomy를 원형 복원하는 것
- 근거가 없는 필수 Ticket 층, 두 reviewer, 고정 trigger·cadence와 자동 semantic gate
- narrative `PASS`를 machine evidence나 제품 효과로 승격하는 것

## 권장 반영 순서

1. `context/project/README.md`를 안정된 Recover routing anchor로 정하고, overview는 optional derived summary로 재정의한다. Workspace의 task-specific 실제 내용 선택 책임은 유지한다.
2. Project 책임 profile, actual Owner·읽기 조건·갱신·stale 신호, content recoverability를 기존 canonical에 보강한다.
3. Recover code·test·fixture와 sample Workspace의 Project 선택을 새 anchor에 맞춘다.
4. `apply-context-harness`와 Workspace 생성·전환 acceptance에 모든 영향받는 live consumer의 reconciliation, task-specific 실제 내용 선택, 실제 Recover, semantic target과 template residue 검사를 보강한다.
5. 큰 복원용 cold/blind review artifact 보존과 Verify claim·evidence·argv의 input-closure 검사를 acceptance에 포함한다.
6. TripProof 결함을 bounded regression/re-entry fixture로 실행해 producer와 consumer 양쪽을 확인한다.
7. 그 뒤에만 project maintainer, claim-scope, Work/Spec 병용을 각각 작은 pilot으로 판단한다.

이번 순서는 Project 계약과 적용 검증을 먼저 고치고, 실제 적용 근거가 없는 runtime·review 역할을 뒤로 미룬다. TripProof와 `reference-project/`는 이번 조사에서 변경하지 않았다.
