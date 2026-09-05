# 2026-09-04 Project·Work 도입 판단

> 현재성 메모: 이 문서는 지정 연구와 live Reference를 대조한 1차 판정이다. 이후 실제 TripProof target 대조는 [`TripProof 실제 적용 평가`](2026-09-04-04-tripproof-application-assessment.md)로 보강됐지만, 두 문서의 비물리 profile·선택적 overview 배치 판정은 사용자 정정으로 폐기됐다. 현재 Project 구조와 검증은 [`07 물리 layer 정정 기록`](2026-09-04-07-project-context-physical-layers.md)과 `current/`를 우선한다.

## 결론

외부 연구에서 바로 가져올 핵심은 새 skill 이름이나 Workflow가 아니다.

1. **Project 구성 계약의 보강:** 현재 Project context가 가진 문서 목록 위에, 공통 맥락·현재 상태·조건부 지침이라는 주장 역할, 실제 정본·책임 주체·읽기 조건·현재 권위·stale 처리 관계를 명시한다.
2. **Work의 위치 명확화:** Work를 Spec/Ticket의 대체재가 아니라 변하는 판단과 current/history의 수명을 감싸는 continuity envelope로 설명하고, 판단이 안정된 실행 구간에서는 필요에 따라 Spec·Ticket·bounded brief를 임시 실행 산출물로 사용한다.
3. **Claim 범위 제한의 pilot:** 기존 Verify가 기계 evidence에 적용하는 proof ceiling을 의미적 완료 주장에도 적용할 수 있는지 작은 read-only replay로 먼저 본다.

반대로 두 review 역할, 고정 trigger, cadence와 자동 gate를 바로 Reference에 넣을 근거는 없다.

## 외부 연구가 실제로 추가한 관점

### 문제의 중심

[대화 장면 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/04-conversation-scene-analysis.md:200)은 상위 판단이 다음 작업 선택, 미룰 범위, 구현, 근거 해석과 완료 판정의 여러 지점에서 약해졌다고 정리한다. 같은 문맥을 읽거나 vertical slice 형태를 사용하고 test가 통과한 것만으로 판단이 끝까지 효력을 갖지는 않았다.

이번 범위에서는 private 원대화를 다시 열지 않았으므로 이것을 세 보존 장면에 대한 내부 분석으로만 사용한다. 그래도 Reference가 해결해야 할 후보 문제를 “더 많은 context”가 아니라 “근거와 claim의 범위, 핵심 책임의 실제 수행, 현재 판단의 재개방”으로 좁히는 데는 충분하다.

### Project foundation

[Project context foundation](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/03-project-context-foundation-direction.md:41)은 보존 기간·읽기 조건·현재 권위를 세 디렉터리가 아니라 모든 지속 정보에 적용하는 판단축으로 둔다. 그 결과 Project 안에서 다음 책임 profile을 구분한다.

- 공통 맥락: 여러 Work에서 계속 유효할 제품 목적·domain 의미·Project-wide 제약
- 현재 상태: 다음 관련 Work가 알아야 할 현재 architecture·위험·열린 질문·기술 부채
- 조건부 지침: 관련 종류의 Work에서만 읽는 반복 판단·검증 기준과 적용·비적용·제거 조건

일반 진입점은 이 내용을 모두 복제하지 않고 실제 정본 위치, 책임 주체, 읽기 조건과 관리 규칙으로 routing해야 한다. 관리 skill은 정본이나 책임 주체가 아니다.

### Work와 실행 산출물

[Work/Spec/Ticket 비교](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md:11)는 두 방식을 배타적으로 두지 않는다.

- 판단이 움직이고 제품 의미·책임 배치·architecture를 구현 중 다시 열 가능성이 크면 living current와 선택적 Project context를 가진 Work가 유리할 수 있다.
- 요구와 해결 방향이 안정되고, 여러 fresh context나 실행자가 독립 vertical slice를 구현하며 blocker·acceptance seam을 관리해야 하면 Spec/Ticket이 유리할 수 있다.
- Work는 전후 판단과 수명을 감싸고 Spec/Ticket은 안정된 구간의 실행 snapshot이 될 수 있다.

이 관계는 Work가 더 우월하다는 효과 주장이 아니라 무엇을 위해 지속 관리비를 지불하는지 설명하는 설계 가설이다.

### 판단과 근거 범위

[해결 설계](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/05-judgment-continuity-solution-direction/05-solution-design.md:21)은 행동을 바꾸는 `판단축 + 대상 + 적용 범위 + 현재 명제`를 최소 검토 단위로 제안한다. 근거가 관찰한 artifact·revision·상태와 현재 claim의 상태를 먼저 맞추고, 근거를 지지·좁은 범위 지지·불충분·반박·무관으로 구분하며, 바뀐 판단의 영향도 관련 결과 안에서 제한한다.

이 원칙의 방향은 강하지만 정확한 분류, trigger와 review 구조의 행동 효과는 아직 pilot 전이다.

## 현재 Reference에 이미 있는 것

Live Reference에는 외부 연구의 구조적 기반 대부분이 이미 있다.

- [`context/project/README.md`](../../../../reference-project/context/project/README.md): Project common context, 상세 Owner 우선, derived overview와 작업별 선택
- [`context/work/workspaces/README.md`](../../../../reference-project/context/work/workspaces/README.md): identity, current, source, output, records와 machine receipt의 분리
- [`CREATE-AND-TRANSITION.md`](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md): successor의 독립 current, predecessor 단방향 참조, Project 자동 승격 금지
- [`Recover`](../../../../reference-project/context/work/harness/recover/README.md): 선택한 Project context와 bounded current만 읽는 packet
- [`Maintain`](../../../../reference-project/context/work/harness/maintain/README.md): 한 Workspace의 durable 변화만 기존 Owner에 반영하고 Project-level 후보 자동 승격을 하지 않는 관리 장치
- [`Verify`](../../../../reference-project/context/work/harness/verify/README.md): 구체 claim, canonical basis, evidence snapshot과 고정 실행을 기록하되 의미 충분성·사람 acceptance·Workspace 완료를 분리

그러므로 `current/source/output/records`나 Project/Work 경계를 다시 가져오는 것은 중복이다.

## 현재 Reference에서 실제로 비어 있거나 약한 것

### 1. Project 문서 목록은 있지만 주장별 책임과 읽기·권위 계약이 얕다

현재 Project README는 `overview`, `prd`, `architecture`, `decisions`의 문서 역할과 상세 Owner 우선순위를 설명한다. 하지만 다음을 일반적으로 찾게 하지는 않는다.

- 어떤 주장이 공통 맥락, 현재 상태, 조건부 지침 중 어떤 책임을 갖는가.
- 조건부 지침의 적용·비적용·재검토·제거 조건은 어디 있는가.
- 각 내용의 유효성을 계속 판단할 책임 주체가 누구인가.
- 현재 답, 초안, 당시 선택 이유와 열린 판단의 권위가 어떻게 다른가.
- 다음 관련 Work가 Project 의미와 판단 근거를 재추론하지 않게 할 최소 coverage가 무엇인가.

새 디렉터리를 만들 필요는 없지만 Project 계약 자체는 보강할 가치가 있다.

### 2. Derived overview의 freshness가 필수 입력인데 결정적 확인은 없다

현재 overview는 상세 Owner와 충돌하면 stale이며 재대조해야 하지만 모든 Recover가 반드시 읽는다. 상세 Owner 변경 때 overview freshness를 자동 확인하는 계약은 없다. 외부 연구의 `Project 현재 상태`와 stale 처리 관점은 이 빈틈을 설명하는 데 직접 유용하다.

우선 필요한 것은 자동 watcher가 아니라 다음의 명시다.

- overview가 어떤 Owner의 어떤 현재 주장을 압축하는가.
- 어느 변화가 stale 신호인가.
- 충돌 때 어느 범위의 claim을 보류하고 누가 갱신 판단을 하는가.
- 재대조 근거를 어떤 수준까지 남길 것인가.

### 3. Work는 저장 경계로는 선명하지만 실행 산출물과의 관계가 없다

현재 Work 계약은 bounded current와 Harness 관계를 잘 정의하지만, 다음은 정하지 않는다.

- Work current만으로 충분한 때와 별도 Spec/Ticket이 필요한 때
- Spec/Ticket이 현재 phase의 잠정 실행 권위를 얻고 잃는 조건
- Ticket의 국소 완료와 Work goal·제품 판단 완료의 차이
- 구현이 상위 전제를 반박할 때 실행 snapshot을 다시 여는 경계

외부 연구의 continuity envelope 설명은 이 부분을 새 필수 파일 없이 보강할 수 있다.

### 4. Verify의 claim ceiling이 Main의 의미적 완료 주장까지 이어지지 않는다

Verify는 이미 명령 통과, snapshot된 basis/evidence와 의미 충분성·acceptance를 분리한다. 그러나 Main이 국소 test·commit·interface를 근거로 더 넓은 제품·코드·Work 완료를 말하려 할 때 같은 범위 제한을 적용하는 별도 계약은 없다.

이 빈틈은 새 Verify 기능으로 넣으면 안 된다. Verify는 기계 실행을 소유하고 의미 판단을 하지 않는다. 우선 report-only replay에서 Main의 선택·범위·완료 문구가 실제로 달라지는지 확인해야 한다.

### 5. Project-level 후보의 발견과 실제 반영 사이 책임이 비어 있다

Maintain은 명시적으로 Project context 자동 반영을 소유하지 않는다. 외부 연구는 Project 계약을 읽고 후보와 근거를 판정해 기존 Owner 변경을 보조하는 얇은 project-local skill을 제안한다.

이 책임은 가능성이 있지만 지금 skill부터 만들면 안 된다. Project 계약과 고권위 사용자 판단 경계를 먼저 명시하고, 대표 Project-wide 변화 하나에서 기존 Maintain·apply-context-harness와 중복되지 않는지 확인해야 한다.

## 새로 드러난 내부 baseline 문제

외부 연구를 가져오기 전에 현재 Reference의 기준 자체를 정직하게 맞춰야 한다.

- 완료된 [`001-reference-implementation/current/memory.md`](../../001-reference-implementation/current/memory.md)는 `verify.json`이 결과별 next action을 소유하고 recovery packet schema가 `5`라고 적지만, live Verify는 next action을 금지하고 Recover packet은 schema `6`이다.
- [`001 current state`](../../001-reference-implementation/current/state.md)는 status schema `2`, 전체 test `40`개와 `verified_waiting_acceptance`를 현재형으로 적지만 live sample은 schema `3`, test `115`개와 `verification_passed`다.
- Workspace 001의 자기 규칙은 live Reference의 유효 결론이나 검증 상한이 바뀌면 current를 갱신한다고 말한다.

또한 Workspace의 사람이 읽는 `current/memory/03-project-context.md`와 machine `recover.json`이 선택 Project 문서를 함께 표현하지만 Maintain은 전자만 변경할 수 있고 후자는 금지한다. 이 권한 분리는 의도적이지만 두 표현을 함께 정렬할 Owner와 검사가 선명하지 않다.

이 문제들은 외부 연구의 효과 증거가 아니라 현재 저장소에서 직접 확인한 선행 정합성 문제다.

## 후보별 판정

| 후보 | 판정 | 이유와 배치 |
| --- | --- | --- |
| Project의 공통 맥락·현재 상태·조건부 지침 책임 profile | **변형 채택** | 디렉터리로 만들지 않고 `context/project/README.md`의 주장별 routing 계약으로 보강한다. |
| 보존 기간·읽기 조건·현재 권위 세 판단축 | **변형 채택** | 새 schema가 아니라 Project 문서와 주장 역할을 판정하는 사람·AI용 기준으로 둔다. |
| 실제 정본·책임 주체·관리 장치 분리 | **채택** | 기존 Owner 우선·Harness 비소유와 정합적이며 Project 진입점에 더 명시한다. |
| Derived overview stale 처리 | **채택할 요구, 구현은 설계 필요** | 필수 Recover 입력의 위험을 줄이는 계약과 대표 충돌 검증을 먼저 만든다. |
| Decision을 이유·대안·재검토 신호용으로 제한 | **변형 채택** | 기본 역할은 이유 기록으로 두되, sample timeout처럼 decision이 명시적 normative Owner인 예외를 금지하지 말고 실제 Owner 관계를 표시한다. |
| Work를 continuity envelope로 설명 | **변형 채택** | Work canonical에 의미를 추가하되 효과가 입증됐다고 말하지 않는다. |
| 안정된 구간의 조건부 Spec/Ticket/bounded brief | **변형 채택** | 새 필수 directory 없이 사용 조건·잠정 권위·폐기·재개방 경계만 설명한다. |
| 동일 대상·범위·revision까지만 claim을 닫는 원칙 | **pilot 후 채택 판단** | Verify와 정합적이지만 의미 판단에서 실제 행동을 바꾸는지 replay가 필요하다. |
| 기존 결과의 제한적 재판정 | **pilot** | 전체 history 재개방은 막지만 영향 검색과 세 상태의 정확성은 검증되지 않았다. |
| 얇은 Project context 반영 skill | **보류 후 대표 사례 pilot** | Project 계약·권한을 먼저 정하고 Maintain·이식 skill과 중복을 확인한다. |
| `claim-impact-review` | **보류, report-only replay 후보** | 정확한 이름·trigger·출력 형식을 채택하지 않고 최소 원칙의 행동 차이를 먼저 본다. |
| `direction-gap-review` | **보류, 독립 replay 후보** | Work-local 문맥이 못 보는 누적 공백 문제는 타당하지만 비용·읽기 경계·호출 누락이 미검증이다. |
| 모든 phase/response-end trigger, 정기 cadence, 자동 gate | **채택하지 않음** | 근거 없는 운영비와 Maintain 책임 결합을 만든다. |
| Project-wide decision/dependency graph와 상시 semantic audit | **채택하지 않음** | 현재 문제에 비해 무겁고 Workspace 독립·rippability를 훼손한다. |
| Work-first의 보편 기본값, Spec/Ticket 기본 배제 | **채택하지 않음** | 외부 연구 자체도 안정된 multi-session 실행에서 반대 조건을 인정한다. |

## 권장 구현 순서

### 0. 기준 정합성

- Outer Workspace 001의 오래된 current를 live Reference에 맞게 갱신할지, 완료 당시 snapshot으로 명시적으로 강등할지 정한다.
- `current/memory/03-project-context.md`와 `recover.json`의 인간용 설명·machine 선택 관계와 갱신 Owner를 정한다.
- Project overview freshness를 어떤 claim과 근거로 확인할지 대표 stale 사례를 먼저 잡는다.

### 1. 기존 canonical의 문서 계약 보강

- Project README에 책임 profile, 판단축, 실제 Owner·책임 주체·관리 장치, authority와 reading rules를 추가한다.
- 현재 overview·PRD·architecture·decision 각각에 어떤 claim 역할이 섞여 있는지 sample mapping을 제공하되 새 taxonomy로 고정하지 않는다.
- Work README 또는 Workspace canonical에 continuity envelope와 조건부 실행 artifact의 관계, 국소 완료와 Work 완료의 차이를 추가한다.
- Decision의 기본 rationale 역할과 명시적으로 normative Owner인 예외를 구분한다.

이 단계는 새 runtime·skill·hook·schema를 만들지 않는다.

### 2. Bounded replay

다음 장면을 같은 판정 기준으로 read-only 비교한다.

1. 국소 test가 통과했지만 넓은 code-quality goal은 남은 경우
2. end-to-end interface가 있지만 핵심 책임이 stub인 경우
3. Project overview와 실제 code/test Owner가 충돌하는 경우
4. 한 상위 전제 변경이 관련 결과와 무관한 결과에 서로 다른 영향을 주는 경우
5. 안정된 multi-session 구현에서 Work-only와 Spec/Ticket 병용의 blocker·재설명·통합 비용 비교
6. 작은 수정에서 아무 review나 Workspace 추가가 필요 없는 비적용 경우

최소 원칙을 추가한 쪽이 완료 문구만 보수적으로 바꾸는 데서 끝나지 않고 작업 후보·범위·다음 판단을 실제로 바꿀 때만 지속 Reference 후보로 올린다.

### 3. 필요한 최소 장치만 선택

- Work-local 의미 판정이 반복해서 유효하면 작은 common reference 또는 model-invoked entrypoint를 검토한다.
- 누적 공백이 Work-local 판정에서 실제로 누락될 때만 fresh-context direction review를 분리한다.
- invocation 누락과 무시된 unresolved state가 실제로 나타날 때만 결정론적 보장이나 cadence를 다시 판단한다.
- 모든 장치는 report-first, 비자동 후속 실행, 사용자 고권위 판단, 제거 가능성을 유지한다.

### 4. 실제 Project 적용과 효과 검증

Reference 안의 synthetic replay와 canonical 정렬 뒤에만 별도 실제 Project에서 적용한다. 제품·코드 변화, 사용자 정정 빈도, 잘못된 next action, current 팽창, 유지비와 invocation 누락을 관찰해야 효과를 주장할 수 있다.

## 완료 기준

이 Workspace의 작업은 다음이 성립할 때 완료 후보가 된다.

- 사용자가 채택·pilot·보류 경계를 검토하고 Reference 변경 범위를 선택했다.
- 기존 canonical을 중복하지 않고 Project·Work의 실제 Owner에 변경이 들어갔다.
- 새 문서 계약의 local link와 Reference 전체 unit test가 통과했다.
- bounded replay가 trigger·비trigger, claim 범위, 관련 결과 영향과 비자동 후속 실행을 구분했다.
- 새 역할을 만들었다면 제거해도 기존 Project/Work 운영이 계속 작동한다.
- 실제 적용 전에는 구조적 타당성과 행동 효과를 분리해 보고한다.
- 사람 acceptance와 commit은 별도 권한으로 남는다.
