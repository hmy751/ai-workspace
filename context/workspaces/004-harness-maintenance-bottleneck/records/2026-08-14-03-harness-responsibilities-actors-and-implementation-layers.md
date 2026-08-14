# Harness 책임·주체·구현 층위 종합

기록일: `2026-08-14`
상태: 현재 구현 사실 확인, 책임 모델과 재배치 방향은 사용자 검토 전 후보

## 기록 경계와 근거 상태

이 기록은 지금까지의 Recover·Maintain·Verify·Harness 책임 논의를 한곳에 모으되 근거의 권위를 다음처럼 구분한다.

- **확인된 사실**: 현재 저장소의 코드·계약·receipt·기존 검증 기록에서 직접 확인한 동작이다. 이번 record 작성 중 runtime을 다시 실행했다는 뜻은 아니다.
- **보고된 배경**: 저장된 [이전 대화 source](../../../source/00-intake/2026-08-14-harness-maintenance-background/README.md)의 작업 시간·과정 설명과, 이번 세션에서 main이 전달한 두 차례 독립 reviewer 의견이다. Source와 reviewer 권고는 분석 입력이지 canonical truth나 채택 결정이 아니다.
- **후보 판단**: 이번 세션의 사용자 질문·정정, reviewer 관점, main의 코드 대조를 바탕으로 논의 중인 책임·활성 시점·주체·방법의 구분이다. 새 설계나 구현 승인으로 쓰지 않는다.
- **미결정**: schema, 명령, agent, migration, 첫 구현 slice처럼 사용자가 아직 선택하지 않은 항목이다.

이 Workspace는 [`context` canonical](../../../README.md)이 정의한 Project common context와 Workspace `current/source/output/records`의 책임 구조를 전제로 한다. 그 Context 구조 자체를 이번 병목 개선 대상으로 다시 설계하지 않는다.

초기 목적과 Recover·verify 활성 시점 가설은 [앞선 기록](2026-08-14-02-recover-verify-purpose-and-activation-hypotheses.md)에 보존한다. 이 기록은 그 결론을 덮지 않고 Maintain, Handoff, Harness check, 주체와 구현 층위를 추가한다.

## 확인된 현재 구현 사실

### Workspace 선택은 explicit id에서도 global index를 먼저 읽는다

현재 [`select_workspace`](../../../../reference-project/context/work/harness/workspace_contract.py)는 `explicit_workspace_id`의 유무와 관계없이 먼저 `workspaces/index.json`을 읽고 exact schema와 active id를 검증한다. 그 뒤 explicit id가 있으면 그것을 사용한다. 따라서 명시적으로 특정 Workspace를 실행하려 해도 global index가 없거나 malformed이면 선택 전에 실패한다.

이것은 현재 코드 동작이다. Explicit task Workspace를 index보다 우선하는 계약으로 바꾸자는 것은 아래의 후보 판단이며 아직 구현 결정이 아니다.

### Recover는 재진입과 일부 구조 완전성 검사를 함께 수행한다

현재 [`Recover`](../../../../reference-project/context/work/harness/recover/README.md)는 다음을 한 read-only 흐름에 둔다.

- active 또는 explicit Workspace 선택
- root 이탈·symlink를 막는 안전한 파일 접근
- `workspace.json`, `recover.json`, current memory·state, output index, 선택한 Project context 로딩
- exact schema, 필수 memory 파일, `overview.md` 첫 순서 같은 구조 완전성 검사
- status가 가리키는 receipt의 schema·Workspace id·result·finished time header 최소 대조
- 선택한 내용과 provenance의 recovery packet 조립

Recover는 Workspace source·records 전체, output artifact 본문, `verify.json`을 자동으로 읽지 않고 어떤 파일도 갱신하지 않는다.

### Verify는 고정 계약 실행과 durable machine state 갱신을 한 흐름에 둔다

현재 Workspace의 [`verify.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/verify.json)은 정적인 argv, evidence paths, timeout, 출력 상한, pass/fail next action을 둔다. [`verify_workspace`](../../../../reference-project/context/work/harness/verify/operation.py)는 다음 순서로 동작한다.

1. Workspace와 `verify.json`, 기존 machine status, receipt 디렉터리의 계약·안전 조건 확인
2. evidence 파일의 hash와 byte size를 실행 전에 확보
3. 고정 argv를 shell 없이 timeout·출력 상한 아래 subprocess로 실행
4. exit code `0`이면 pass, 그 외에는 fail로 판정
5. 성공·실패 모두 append-only receipt로 추가
6. receipt, result, finished time, next action을 [`status.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/current/state/status.json)에 atomic 반영

Verify는 사람용 current·records를 의미에 맞게 고치지 않고 acceptance나 completed를 결정하지 않는다.

### Receipt의 현재 증명 범위와 빈틈

현재 [sample receipt](../../../../reference-project/context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json)는 Workspace id, argv, 실행 전 evidence hash·size, 시간, timeout, stdout·stderr, exit code와 pass/fail을 남긴다. 따라서 특정 파일 snapshot에서 특정 명령이 실행돼 어떤 결과를 냈는지는 추적할 수 있다.

반면 현재 contract와 receipt에는 다음 연결이 명시적 필드로 없다.

- 이번 검사로 확인하려는 구체적인 검증 대상 문장
- 그 문장을 지지하는 Project canonical 기준과 기준 revision
- 실행 environment 또는 Project revision
- receipt가 현재 코드·기준에도 여전히 fresh한지 판별하는 연결

따라서 receipt는 실행 사실을 durable하게 남기지만, 무엇을 의미상 증명하려 했고 현재도 그 증거가 유효한지를 혼자 완결하지 않는다.

### Harness live 회귀가 제품 Workspace 상태를 바꿀 수 있다

현재 reference 책임 변경 검증에서는 실제 active default-timeout Workspace에 `recover → verify → recover`를 실행해 새 product verify receipt와 `verified_waiting_acceptance` status를 남긴 사례가 있다. [Machine receipt 변경 기록](../../001-reference-implementation/records/2026-08-14-05-machine-receipt-boundary-and-durable-verify.md)

이는 실제 연결을 검증하는 장점이 있지만, Harness 자체의 schema·path·회귀 변경을 확인하는 실행도 active 제품 Workspace의 durable receipt와 최신 machine cursor를 바꿀 수 있다는 결합을 만든다.

## 논의하며 선명해진 책임 구분 후보

아래는 책임 모델 후보이며, 같은 이름의 새 CLI·Python module·agent를 만들겠다는 뜻이 아니다. **책임**, **활성 시점**, **실행 주체**, **구현 방법**을 별개 축으로 본다.

### Recover

맥락 연속성이 끊긴 새 세션·새 작업 주체의 재진입에서, 선택된 Workspace의 현재 맥락을 안전하고 제한적으로 복구하는 책임 후보다. Workspace를 처음 만드는 행위나 모든 구조 migration 검사를 곧바로 Recover의 본질로 보지 않는다.

### Maintain

작업 중 생긴 의미 변화를 지속 Context에 반영하는 책임 후보다.

- 사용자 목표·범위 정정
- 결정, blocker, 실패와 다음 행동
- 다음 작업에서도 재사용할 분석과 검증 해석
- current에서 내릴 완료 과정
- 선택하거나 교체한 output과 records 접근점

이 책임은 제품 명령의 exit code를 receipt와 status에 쓰는 Verify와 다르다. 현재 repo의 `context maintainer routing`은 새 프로그램명이 아니라, 자연스러운 작업 경계에서 지정 Workspace의 `context_maintainer`를 호출하고 main이 실제 diff·파일·test·사용자 정정과 대조하는 기존 운영 규칙이다. [Repo-local 운영 규칙](../../../../AGENTS.md)

Maintain 자체도 하나의 불투명한 동작으로 보지 않고 다음 단계로 나눠 볼 수 있다.

1. 파일·Git·test 등 변화 사실 감지: deterministic program이 도울 수 있음
2. 무엇이 다음 작업에도 지속할 의미인지 판단: agent 책임 후보
3. current·records·output owner에 맞게 갱신: agent 책임 후보
4. 사용자 의도와 실제 diff 대조: main 책임

### Verify

다른 시간이나 주체가 의존할 **구체적인 검증 대상 문장**을 실제 Project 검사와 durable evidence에 연결하는 책임 후보다. 여기서 검증 대상 문장은 복잡한 새 registry를 뜻하지 않고, “이번 검사로 무엇을 확인하려는가”를 명시한다는 뜻이다.

Deterministic runner, 실행 전 evidence hash, 제한 subprocess, append-only receipt는 이 책임을 구현하는 유효한 현재 수단이다. 다만 exit code와 static next action만으로 검증 대상·기준·freshness까지 충분한지는 별도 검토한다.

### Workspace 선택과 routing

Workspace 선택은 현재 task가 어느 Workspace 상태를 읽고 쓰는지 정하는 결속 책임으로 볼 수 있다. Explicit task Workspace를 주 권위로 삼고 repository-global active는 id가 없는 재진입의 편의 default 또는 hint로 낮출 수 있다는 후보가 나왔다.

이는 active index를 제거하거나 fallback 계약을 확정했다는 뜻이 아니다. 현재 코드는 explicit id에서도 global index를 먼저 검증한다.

### Handoff

Handoff는 매 세션의 core step이 아니라, 다른 task·AI·사람에게 작업 소유권을 명시적으로 넘길 때 Maintain 결과와 필요시 Verify evidence를 전달하는 선택적 workflow 후보다. 일반적인 다음 세션은 최신 Context를 Recover하면 별도 handoff packet 없이도 재진입할 수 있다는 구분이다.

어떤 handoff에서 Verify를 필수로 할지는 아직 정하지 않았다.

### Harness check

Harness 생성·이식·migration·schema·path 방어·호환·회귀를 제품 Verify와 구분해 검사하는 책임 후보다. 기본 실행 주체는 deterministic tests/program이며, 이를 위해 새 상시 검증 agent를 만든다는 뜻이 아니다. 독립 reviewer는 의미 위험이나 실패 영향이 큰 변경에서만 선택할 수 있는 후보로 둔다.

### 사람 판단

목표와 범위 정정, 결과 acceptance, Workspace completed 전이, Workspace 결과의 Project canonical 반영은 사람 책임으로 유지한다. Machine fact나 agent 해석이 이 결정을 자동 대체하지 않는다.

## 주체와 구현 층위 후보

### Deterministic program

- Workspace id·root·path 안전과 bounded read
- 파일 hash·revision·freshness 같은 기계 사실 계산
- 제한된 Project 명령 실행
- append-only receipt와 machine cursor 생성

### Agent

- 기본 packet 밖에서 필요한 Context 추가 선택
- 어떤 변화가 지속할 의미인지 판단
- 검증 대상과 선택한 test의 충분성 판단
- current·records·output 의미 갱신

### Skill 또는 workflow routing

- Workspace 생성·재진입
- 의미 변화 뒤 maintenance
- durable evidence가 필요한 상태 전환
- 명시적 ownership handoff
- Harness 자체 변경

각 활성 시점에 맞는 program·agent·사람을 호출한다. Skill이 책임의 Owner이거나 모든 동작을 직접 구현해야 한다는 뜻은 아니다.

### Human

- 목표·범위 정정
- 검증 결과 acceptance
- 완료 선언
- Project canonical 반영

## 현재 방식과 후보 방향 비교

| 판단 대상 | 현재 방식에서 확인한 결합 | 검토할 후보 방향 | 상태 |
|---|---|---|---|
| Workspace 선택 | explicit id에서도 global active index를 먼저 검증 | explicit task Workspace를 주 권위로 하고 active는 optional default/hint로 제한 | 후보 |
| Recover | 안전한 재진입 읽기와 exact 구조 완전성 검사를 매 실행에 함께 수행 | read safety·선택·packet 중심을 유지하고 생성·migration 검사를 별도 시점으로 옮길지 분류 | 후보 |
| Maintain | Verify 밖의 의미 갱신이 운영 routing에는 있으나 핵심 workflow 설명에서 흐릿함 | 의미 변화 감지·판단·context 갱신·main 검토를 별도 책임으로 드러냄 | 후보 |
| Verify | static argv·evidence·next action, exit 기반 status 전이 | 검증 대상·canonical 근거·revision·environment·freshness를 필요한 수준만 명시하면서 deterministic runner 유지 | 후보 |
| Harness 회귀 | live product Workspace verify로 실제 receipt와 status를 변경 | fixture·canary·non-durable Harness check와 product 상태 인계를 분리할지 검토 | 후보 |
| Handoff | durable verify와 다음 재진입 설명에 섞여 보일 수 있음 | 명시적 ownership transfer 때만 선택적으로 수행 | 후보 |
| Acceptance | pass 뒤 사람 검토를 요구 | 사람 acceptance·completed·canonical 반영 분리 유지 | 현재 경계 유지 후보 |

## 보존해야 할 현재 효과

책임을 재배치하더라도 다음 효과를 잃지 않는 방향을 우선 검토한다.

- 필요한 Context만 선택하는 복구
- Recover의 read-only 성질
- root 이탈·symlink·unsafe command 방어
- 실제 Project 검사의 제한 실행
- 실행 전 evidence와 append-only receipt
- machine fact, agent interpretation, human acceptance의 구분
- Harness를 제거해도 Context 의미와 source·output·records를 읽을 수 있는 제거 가능성

이 목록은 구체적인 검사 위치와 schema를 현재 그대로 영구 고정한다는 뜻이 아니다.

## 아직 결정하지 않은 것

- 이 책임 모델 자체를 최종 채택할지
- 새 CLI·module·agent를 만들지. 특히 Maintain Python module이나 상시 Harness verifier agent를 만든다는 결정은 없음
- explicit id와 global active fallback의 최종 계약
- Recover 검사 중 무엇을 생성·migration preflight로 옮길지
- 검증 대상·canonical 기준·freshness를 어떤 schema로 표현할지
- Git revision과 environment를 receipt에 어디까지 포함할지
- status·receipt schema migration과 과거 receipt 호환 방식
- 어떤 handoff에서 Verify가 필수인지
- 첫 구현 slice와 실제 변경 파일 범위
- 이 책임 재배치가 약 20분 병목을 얼마나 줄이는지

## 다음 판단

구현 계획을 확정하기 전에 다음 축을 한 장의 사용자 검토용 병목 지도에 붙인다.

1. 책임
2. 활성 시점
3. 실행 주체
4. 현재 구현과 후보 이동
5. 보호하는 실패와 이동 시 잃는 증거

그 지도에서 직전 machine receipt 사례의 canonical Owner, 반드시 함께 바뀌는 consumer, 링크만 필요한 historical record, 변경 위험에 맞는 검증 강도를 연결한다. 사용자 검토 전에는 runtime, root routing, skill, schema를 변경하지 않는다.
