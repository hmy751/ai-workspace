# Workspace 기반 연속성 해결 방향

> **후속 결과 — 2026-09-08:** 이 문서는 독립 Spec을 기본으로 유지하지 않기로 했던 초기 채택 방향을 보존한다. 이후 Context Harness Reference에서는 Spec이 goal·작업별 constraints를 대체하고 Ticket을 memory에 두는 구조를 채택·구현했다. 변경된 기본 읽기 범위와 유지된 책임, 적용·검증 한계는 [Spec·Ticket 통합 결과](07-context-harness-spec-ticket-integration.md)에서 확인한다. 이 연구 저장소와 실제 TripProof에 자동 이식된 것은 아니다.

## 문서의 지위

이 문서는 [`01-problem-analysis.md`](01-problem-analysis.md)가 정리한 문제 가운데, 독립된 spec을 계속 운영하지 않고 Workspace 구조로 작업의 연속성과 컨텍스트 수명을 다루는 방향을 기록한다.

여기의 구조는 대화를 거쳐 채택한 설계 방향이다. 아직 실제 TripProof 작업에 적용해 효과를 확인한 결과는 아니다. 특히 제품 전체의 수렴, 코드 구조에 대한 신뢰, 재판단 reviewer, AI 결과물의 인지부채는 이 문서가 해결했다고 주장하지 않는다.

## 출발점

07의 중심 진단은 spec이 작업의 연속성에는 강했지만 판단의 연속성까지 보존하지는 못했다는 것이다. spec은 목표, AC, 구현 순서와 다음 시작점을 남겼다. 그러나 spec이 누적될수록 당시 판단과 기존 코드 구조가 다시 검토할 선택보다 다음 작업의 확정된 전제로 작용했다.

여기서 판단의 연속성은 이전 결론을 계속 따르는 것이 아니다. 왜 그런 판단을 했는지, 무엇이 불확실했는지, 어떤 사실이 나타나면 다시 열어야 하는지에 접근할 수 있고, 필요하면 기존 결론과 산출물을 교체할 수 있는 상태를 뜻한다. 이 문제의 원래 맥락은 [관점별 원문](../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-conceptual.md)과 [논의 순서 원문](../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-chronological.md)에 있다.

따라서 해결 방향은 spec의 내용을 최대한 오래 보존하는 것이 아니다. 작업을 이어가는 데 필요했던 기능은 살리되, 작업 지시와 장기 판단, 현재 상태, 역사 기록의 수명과 권위를 분리하는 것이다.

## 채택한 큰 방향

### 독립된 spec을 기본 작업 단위로 유지하지 않는다

장기간 누적되고 다음 작업을 계속 지휘하는 독립 spec 형식은 Workspace로 대체한다. 기존 spec 파일을 Workspace 안으로 옮기거나, spec의 모든 항목을 `current`에 다시 만드는 방식은 사용하지 않는다.

세부 plan, task, AC를 담은 임시 실행 문서도 기본 절차로 만들지 않는다. 현재 작업에서 실제로 필요해 자연스럽게 생길 수는 있지만, Workspace의 필수 계약이나 매 작업의 기본 산출물로 요구하지 않는다. 별도 실행 문서가 없어도 다음 세션이 작업을 이어갈 수 있도록 `current`와 `records`의 역할을 분명히 하는 쪽을 기본으로 삼는다.

### Workspace는 의미 있는 현재 작업 하나에 집중한다

Workspace는 기능 개발, 코드 구조 개선, 조사와 결정 등 의미 있는 작업에 사용할 수 있다. 작업 종류를 하나로 제한하지 않는다. 반대로 맥락을 별도로 복구할 필요가 없는 작은 수정마다 Workspace를 만들지는 않는다.

작업이 어느 정도 마무리되고 다른 작업으로 이동하면 새 Workspace를 연다. 과거 Workspace를 현재 상태처럼 계속 갱신하거나, 관련 Project context가 바뀌었다는 이유로 모든 과거 Workspace를 찾아다니며 동기화하지 않는다. 과거 Workspace는 당시의 current와 records를 보존하는 역사적 작업 단위로 남는다.

이를 위해 별도의 무거운 생성·완료·보관 수명주기 장치를 먼저 만들지는 않는다. 현재 선택한 Workspace에 집중하고, 다른 Workspace를 다시 다룰 명시적인 이유가 있을 때만 그 Workspace를 연다.

## Workspace 안의 책임 배치

Workspace는 spec의 파일 구조를 복제하지 않는다. 다음 세션이 현재 작업을 복구하고 필요한 자료로 이동할 수 있도록 책임을 나눈다.

| 위치                                   | 맡는 책임                                                                       | 맡지 않는 책임                            |
| -------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------- |
| `current/memory/01-goal.md`            | 작업 목적, 완료됐다고 볼 구체적 상태나 장면, 범위와 하지 않을 것                | 상세 plan, task 순서, 모든 AC             |
| `current/memory/02-constraints.md`     | 작업 중 어떤 방법을 택하더라도 지켜야 할 제약                                   | 후보 비교, 임시 선호, 과거 결정 과정      |
| `current/memory/03-project-context.md` | 이번 작업에 필요한 Project context와 선택 이유                                  | Project context 본문의 복제               |
| `current/state/index.md`               | 지금 실제 상태, 다음 행동에 영향을 주는 열린 결정, 바로 다음 행동이나 판단 지점 | 완료 과정의 누적 기록, 전체 작업 로그     |
| `current/state/status.json`            | Harness가 관리하는 최근 기계 상태와 evidence cursor                             | 사람의 다음 행동, 의미 충분성, acceptance |
| `source/`                              | 선택한 원자료, 변경하지 않은 snapshot, provenance                               | 현재 해석과 결정                          |
| `output/`                              | Workspace goal을 위해 선택한 현재 산출물과 canonical 위치                       | 후보와 탈락안, acceptance 판정            |
| `records/`                             | 판단 과정, 변경 이유, 후보 비교, 탈락안, 실행과 검증의 역사                     | 현재 상태를 대신하는 지시                 |

### current의 최소 계약

`current`는 축소된 spec이 아니라 다음 세션이 기본으로 읽는 제한된 재진입 표면이다. 필수 내용은 다음과 같다.

- 이 Workspace의 goal
- 완료됐다고 볼 수 있는 구체적 상태나 장면
- 이번 작업의 범위와 하지 않을 것
- 작업 중 반드시 지켜야 할 제약
- 이번 작업에 선택한 Project context와 선택 이유
- 지금 실제 상태
- 다음 행동을 막거나 바꾸는 현재의 열린 결정
- 바로 이어서 할 행동이나 판단 지점

완료 장면은 상세 AC 묶음이 아니다. 작업 결과를 사람이 확인할 수 있는 소수의 구체적 상태에 가깝다. 기능 작업과 구조 개선 작업의 완료 모습이 다를 수 있으므로 제품 기능 중심의 고정 형식을 두지 않는다.

열린 결정도 모든 의문을 모으는 목록이 아니다. 다음 행동을 실제로 막거나 바꾸는 현재 판단만 둔다. 판단이 바뀐 전체 과정과 이유는 records가 맡는다.

### 기본 current에서 제외하는 것

다음 내용은 모든 Workspace의 기본 current에 넣지 않는다.

- 상세 구현 순서와 task 목록
- 모든 테스트 케이스와 AC
- 과거에 완료한 일의 나열
- 판단이 바뀐 전체 과정과 이유
- 후보 비교와 탈락안
- 제품 수렴과 코드 신뢰를 평가하는 전체 workflow
- 관련 있을 수 있다는 이유만으로 모은 Project context 전체

필요한 상세 정보는 기본 current에 복제하기보다 source, output, records, Project context의 적절한 Owner에서 찾게 한다. 새 세션의 목표는 모든 내용을 처음부터 아는 것이 아니라, 현재 작업에 필요한 내용을 어디서 확인해야 하는지 아는 것이다.

## Project context와의 관계

여러 Workspace에서 계속 유효할 현재 판단은 Project context가 소유한다. 제품 목적과 핵심 도메인 의미, 여러 작업이 공유하는 제약, 현재 책임 구조, 반복해서 필요한 기술 판단 기준, 채택된 Project 결정이 후보가 될 수 있다.

Project context 반영은 Workspace 종료 때만 수행하는 승격 단계가 아니다. 작업 중 다음 조건을 만족하는 변화가 명확해진 자연스러운 경계에서 별도 skill이 기존 Project context Owner를 검토하고 반영한다.

- 현재 Workspace를 넘어 이후 작업에도 적용된다.
- 미래 작업의 판단이나 행동을 실제로 바꾼다.
- 일시적인 구현 방법이나 조사 메모가 아니다.
- 과거 기록이 아니라 지금도 유효한 내용으로 표현할 수 있다.
- 내용을 관리할 Project context Owner가 분명하다.

Main은 명확한 후보를 발견하면 이 skill을 실행할 수 있다. 제품 목적, 핵심 도메인 의미, 중요한 제약의 새로운 결정이나 현재 의미의 변경, 근거가 충돌하는 선택은 쓰기 전에 사용자 결정을 받는다. 반면 현재 권위가 확인되었거나 사용자가 명시적으로 허용한 기존 의미를 출처에 추적 가능하게, 새 의미와 미해결 충돌 없이 재구성하는 일은 새로운 제품 결정을 내리는 것과 구분한다. 과거 source와 records는 이때도 현재 권위를 자동으로 얻지 않고 역사 증거로 남으며, 어느 근거를 현재 답으로 선택해야 할지가 불명확하면 사용자 판단으로 올린다.

Skill은 현재 선택한 Workspace, 관련 source 권위·records·산출물, 기존 Project context와 실제 제품 사실을 소유하는 domain canonical Owner를 확인한다. 기존 상세 Owner가 있으면 `context/project/`를 새 정본처럼 덮어쓰지 않고 충돌 우선순위와 반영 위치를 먼저 판정한다. 다른 Workspace의 current와 records를 기본 탐색하거나 수정하지 않는다. Project context가 바뀌어도 과거 Workspace를 동기화하지 않으며, 현재 Workspace가 새 Project context 문서를 계속 필요로 할 때만 현재 선택 목록을 갱신한다. 이 복원 가능성은 Recover가 모든 Project context를 읽는다는 뜻이 아니며, Workspace는 여전히 현재 작업에 필요한 문서만 이유와 함께 선택한다.

Project context skill의 구체 구현, decision contract와 사용자 승인 UI는 별도 작업에서 정한다. 이 문서가 정하는 것은 Workspace와 skill 사이의 책임 경계다.

## Harness의 위치

Harness는 Workspace의 의미나 사람의 판단을 소유하지 않는다.

- Recover는 선택한 Workspace의 bounded current, output 지도와 선택한 Project context를 읽어 재진입을 돕는다.
- Maintain은 현재 선택한 Workspace에서 명확해진 durable 변화를 기존 Owner에 반영한다. 과거 Workspace를 살아 있는 문서처럼 갱신하는 장치로 사용하지 않는다.
- Verify는 상태 전환이나 인계에 사용한 claim, basis, evidence, 실행 결과를 연결한다.

Verify는 제품 test나 eval을 설계하거나 대체하지 않는다. 고정 실행이 통과했다는 사실도 제품 의미의 충분성, 사람 acceptance, Workspace 완료를 자동으로 뜻하지 않는다. 현재 연구에는 연구 주장을 판정할 고정 명령과 evidence 범위가 없으므로 이 Workspace에 `verify.json`을 두지 않는다.

Context Harness Reference를 이 연구 저장소에 적용하며 확인한 기존 책임과 proof ceiling은 [적용 기록](../../../workspaces/001-tripproof-spec-continuity/records/2026-08-27-01-context-harness-application.md)에 남아 있다.

## 논의 중 교정한 방향

### spec의 유효한 내용을 current에 최대한 옮기지 않는다

07 원문에서 사용자가 할 수 있어야 하는 것, 보존할 제품 의미, 범위, 대표 흐름은 spec이 분명히 해도 되는 내용의 예시였다. 이것을 모든 Workspace의 current 필수 항목으로 옮기는 것은 원문의 결론이 아니다. 해당 내용은 현재 작업에 실제로 필요할 때 goal, 완료 장면, 제약이나 선택한 Project context를 통해 들어온다.

### 제품과 코드를 Workspace의 두 고정 트랙으로 만들지 않는다

제품 수렴과 코드 구조의 신뢰는 07의 중요한 문제지만, Workspace의 공통 current 형식으로 해결하지 않는다. 구체적인 평가 workflow, reviewer 배치와 재판단 trigger는 별도 구체화로 넘긴다. 따라서 관련 평가 기준을 모든 current에 기본 주입하지 않는다.

### Project context 반영을 종료 시점에 묶지 않는다

Project context는 현재의 프로젝트 공통 맥락이다. 장기적으로 유효한 변화가 작업 중 명확해졌다면 별도 skill이 그때 반영할 수 있어야 한다. 종료는 누락 후보를 확인할 수 있는 한 시점일 뿐 반영의 필수 조건이 아니다.

### 모든 Workspace를 계속 current로 만들지 않는다

한 Project에 여러 Workspace가 있어도 현재 선택한 작업에 집중한다. Project context 변경이나 관련 코드 변경이 생길 때마다 과거 Workspace를 수정하는 것은 역사 기록과 현재 작업을 다시 섞는다.

## 이 방향이 구조적으로 다루는 문제

- spec이 작업 종료 뒤에도 다음 작업을 지휘하는 권위 문제
- 현재 상태와 판단 과정이 한 문서에 누적되는 문제
- 상세 작업 지시가 모든 새 세션에 자동으로 읽히는 문제
- Project 공통 판단과 Workspace별 상태가 복제되는 문제
- 관련된 모든 과거 Workspace를 살아 있는 기록처럼 유지하는 운영 부담
- Verify 결과를 제품 평가나 사람 acceptance로 확대하는 혼동

## 이 방향이 해결하지 않는 것

- 제품 전체가 사용자의 근본 문제로 수렴하는지 판단하는 방법
- 변경 뒤 코드베이스가 더 설명 가능하고 성장 가능한지 판단하는 방법
- 제품·코드 reviewer의 역할, 근거와 재판단 권한
- AI가 만든 코드·응답을 사람이 이해하게 하는 인지부채 skill
- Project context 관리 skill의 실제 구현과 host 연결
- 실제 TripProof 작업에서 이 구조가 효과를 내는지에 대한 적용 검증

이 항목들은 중요하지 않아서 제외한 것이 아니다. Workspace의 저장·재진입 구조와 다른 책임이므로 별도 작업에서 구체화한다.

## 다음 작업

이 문서 뒤에 남은 일은 다음과 같다.

- Project context 관리 skill을 별도 Workspace에서 구체화한다.
- 제품 수렴과 코드 신뢰의 평가 workflow를 별도 분석에서 구체화한다.
- 코드와 AI 결과물의 인지부채를 줄이는 skill을 별도로 설계한다.

이 후속 작업이 완료되기 전까지 이 문서는 Workspace가 책임질 구조적 해결 방향이며, 07 전체 문제의 최종 해결이나 적용 효과의 증명은 아니다.
