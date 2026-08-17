# Verify를 가벼운 증거 기록 보조로 낮춘 경계

기록일: `2026-08-17`

## 이 기록의 경계

[응답 종료 Maintain 계약과 Verify 논의 재개](2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md) 이후, Verify의 원래 목적과 Main 작업 중복을 다시 따져 제품 검증 주체가 아닌 선택적 증거 수집·기록 보조로 낮추기로 한 대화를 보존한다. Recover는 추가 변경 요구 없이 유지했고, response-end Maintain의 기술 실행 구조는 다음 설계 커서로 남겼다.

## 최소 사용자 발화 근거

사용자는 현재 Verify가 Main의 실제 작업과 겹친다고 짚었다.

> 일단 메인 작업과 너무 겹치는 것 같아
>
> 애초에 메인이 작업하고 테스트도 작성해서 할때도 있고 한데 그런겻들이 겹치니까
>
> verify 너무 거대해

이어 Verify 장치를 유지하되 책임을 크게 낮추는 방향을 제시했다.

> verify 를 유지하고 근데 지금 처럼 확 낮추는거지
>
> 검증이나 test나 eval같은걸 잘 남겨서 context를 잘 유지하는데 도움을 주는거지 직접 코드 테스트 검증 평가를 책임지는게 아니라
>
> json으로 남길수 있을때는 남기고

최종 의도는 다음처럼 확인됐다.

> 그냥 나중에 헤깔리지 않도록 증거수집정도 로 기록 관리 차원 정도
>
> 괜히 막 여러 테스트 파일 다 검증하게 하는 뭐이런 느낌은 아니고

## 원래 Verify가 커진 이유의 재검토

현재 Reference Verify는 claim, canonical basis, fixed product argv와 evidence path를 입력으로 받아 기준·evidence snapshot을 만들고, 명령을 직접 실행한 뒤 append-only receipt와 machine status를 갱신한다. 이 구현과 실제 시간 특성은 [운영 지연과 역할 진단](2026-08-17-01-harness-operation-latency-and-role-diagnosis.md)에 정리되어 있다.

이 구조는 초기 Reference에서 default timeout 값을 의도적으로 깨뜨린 실패와 수정 후 성공을 다음 Recover까지 이어 보는 end-to-end cycle, 그리고 commit 전 세션이 바뀌어도 실행 결과와 당시 파일 상태가 사라지지 않는 durable evidence를 확인하려고 커졌다. 이 실험은 Harness가 실패·성공 증거를 보존할 수 있음을 보여 줬지만, 모든 일상 작업에 Main과 분리된 Verify 실행이 필수라는 효과 증거는 아니다.

일상 작업에서는 Main이 변경을 이해하고 test·eval을 작성하거나 선택해 직접 실행할 수 있다. 이 뒤 Verify가 같은 제품 명령을 다시 실행하고 여러 기준·test 파일을 snapshot하면 새로운 제품 판단을 더하지 않은 채 실행과 관리만 중복될 수 있다. 사용자가 납득하지 못한 핵심은 증거 보존 필요성 자체보다 이 증거 장치에 제품 검증 책임이 과도하게 넘어온 것이었다.

## 선택한 책임 배치

### 실제 검증은 작업 주체가 소유한다

- Main과 제품 코드가 필요한 test를 작성·선택하고 실행한다.
- CI, eval runner, browser 자동화나 사람이 자기 경계의 확인을 수행할 수 있다.
- 검증 범위가 충분한지, 추가 확인이 필요한지, 사용자 목표를 달성했는지는 Main·사용자·필요한 독립 reviewer가 판단한다.
- 제품 test와 eval의 canonical은 제품 코드, script, CI와 해당 평가 시스템에 남는다.

### Verify는 이미 일어난 사건의 최소 증거만 보존한다

Verify의 새 목표는 다음과 같다.

> Main·CI·eval·사람이 실제로 수행한 확인 중 나중에 다시 볼 가치가 있는 사건을 출처와 결과가 헷갈리지 않도록 작게 보존한다.

최소 증거 후보는 다음이다.

- 확인한 날짜·시각
- producer, 확인자 또는 결과 출처
- 무엇을 어떤 방법으로 확인했는지
- pass·fail·partial 같은 구체 결과와 필요한 수치
- commit, CI run, artifact, screenshot, trace 같은 원자료 접근점
- 자동 확인 밖에 남은 미확인 범위

이는 새 고정 JSON schema를 승인한 목록이 아니라, 다음 세션에서 결과의 정체와 상한을 혼동하지 않게 하는 최소 의미다.

### Maintain이 배치와 수명주기를 판단한다

- Maintain은 매 AI 응답 종료에 실제 작업 delta와 test·eval·수동 확인 결과를 관찰한다.
- 현재 행동에 필요한 최신 결과는 `current/state`, 후속 작업에서 다시 볼 중요한 사건은 records에 배치하고, 장기 검증 기준은 필요한 경우 memory에 둔다.
- 지속 가치가 있고 구조화가 자연스러운 증거가 필요할 때만 Verify evidence helper를 사용한다.
- Verify는 `current/records` 중 어디에 무엇을 둘지, 그 결과가 현재 작업에서 무엇을 뜻하는지 직접 결정하지 않는다.
- 이후 관련 변경으로 과거 결과의 현재 의미가 달라지면 Maintain이 상태를 정합화하며, 의미가 애매하면 사용자에게 즉시 보고한다.

## 형식은 증거 성격에 맞춘다

- 로컬 명령 결과, CI run, 정량 eval처럼 기계 결과가 자연스럽게 존재하면 JSON evidence를 선택할 수 있다.
- 사람의 브라우저 확인, UX 판단, 정성 eval은 Markdown record나 원자료 링크로 충분하다.
- 모든 test 실행을 JSON으로 승격하지 않는다.
- File path와 hash는 이미 결과에 포함돼 있거나 나중에 그 증거를 식별하는 데 꼭 필요할 때만 둔다.
- 원자료가 CI나 별도 artifact system에 안정적으로 남아 있으면 그 접근점과 필요한 식별자만 연결할 수 있다.

## Verify에서 내린 책임

축소된 Verify는 다음을 소유하지 않는다.

- 제품 test·eval 설계, 작성과 선택
- 제품 명령 재실행
- 여러 canonical·code·test 파일의 일괄 hash와 충분성 검사
- coverage나 검증 범위가 충분한지 판단
- exit code `0`만으로 `verification_passed` 상태 생성
- 사람 acceptance, Workspace completion 또는 제품 목표 달성 선언
- 독립 reviewer 역할

따라서 Verify는 모든 응답이나 handoff에 반드시 거치는 별도 gate가 아니다. Maintain workflow가 보존 가치 있는 증거를 발견했을 때 부르는 하위 기록 장치다.

## 구현 상태와 proof ceiling

- 현재 Reference Verify 구현은 fixed argv 실행, basis/evidence snapshot, receipt와 status 갱신을 그대로 수행한다.
- 이번 대화에서는 Reference 코드, JSON 계약, receipt 또는 Recover 동작을 수정하지 않았다.
- 축소된 evidence helper의 호출 조건, JSON 형식, 보존 기간과 migration 방법은 아직 구현·확정하지 않았다.
- 과거 receipt는 당시 Reference cycle의 historical evidence로 보존하며 새 계약으로 다시 해석하거나 삭제하지 않는다.
- 선택한 책임 경계는 제품 검증 품질, context freshness 개선 또는 latency 감소 효과를 아직 증명하지 않는다.

## 다음 설계 커서

Verify 책임 논의는 여기서 닫고, 사용자가 앞서 요구한 Verify 외 나머지 두 구현면으로 돌아간다.

1. 매 AI 응답 종료를 감지해 그 응답의 delta와 근거 위치를 maintainer에 넘기고 main을 막지 않게 실행하는 trigger·delivery 구조
2. `delta 분류 → Owner 선택 → 동시 수정 재확인 → write → 링크·상태 확인 → ambiguity 또는 자동 반영 보고` 갱신 workflow

Verify evidence helper는 두 번째 workflow에서 필요할 때만 호출한다. 다음 재진입 커서는 [current state](../current/state.md)에 둔다.
