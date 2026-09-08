# Spec·Ticket 설계 합의와 적용 전 남은 작업

날짜: 2026-09-08

상태: **이 시점의 논의 정리. Reference 구현은 시작하지 않았다.**

## 정리 요청과 이 기록의 범위

사용자는 작성 책임 리뷰 뒤 기존처럼 Maintain이 기록·갱신을, Main이 작업 조율을 맡는다고 확인했다. 이어 남은 일을 물었고, Main은 최종 파일 구조·Recover 읽기·Maintain 기록 대상·생성 및 이식 절차의 실제 적용을 제시했다. 사용자는 다음과 같이 요청했다.

> 그래 일단 기록 정리부터 해봐

이 기록은 대화 처음부터 보존한 자료를 새로 대체하지 않는다. [첫 세션 종합](2026-09-07-01-session-synthesis.md), [Spec 구성 합의](2026-09-08-01-spec-components-decision.md), 그 이후 배치·Ticket·역할 논의가 지금 어떤 선택으로 이어졌는지를 한 시점의 기록으로 남긴다. 이후에도 유지할 합의는 [memory](../current/memory.md), 진행 상태와 다음 작업은 [state](../current/state.md)가 맡는다.

## 정한 내용

Spec·Ticket은 실제 개념과 용어로 사용한다. 특정 spec-driven 체계 전체를 들여오거나 자체 대체 용어로 잘게 나누는 방향은 아니다. 기존 Work-first의 이유와 개발 수정 비용은 판단 근거이며 Spec 도입을 막는 규칙이 아니다.

일단 Spec 하나가 생긴다는 전제로 이어간다. `current/memory/spec/` 아래 다음 다섯 구성요소를 각각 Markdown 파일로 둔다.

1. 문제·목표·범위
2. 요구 동작과 대표 사례
3. 핵심 개념·입출력 계약
4. 품질·완료 판단
5. 제약·현재 설계·가정

구성 이유와 구체적인 예시는 [구성 설명](../output/spec-components-and-rationale.md)과 [예시 Spec](../output/spec-example-travel-answer.md)에 나누어 두었다. 구성과 파일 분리는 정했지만 최종 파일명·전체 진입 구조를 구현한 것은 아니다.

Spec이 기존 `01-goal.md`와 `02-constraints.md`의 작업 정의를 대체한다. `03-project-context.md`는 memory에서 유지한다. Workspace 공통 관리 규칙은 원래 운영 지침이 맡는다. Spec은 필요할 때 수정할 수 있고 Workspace와 함께 스냅샷처럼 남는다. 후속 Workspace나 Project 변화에 맞춰 자동으로 계속 갱신하는 공유 문서가 아니다. [범위·배치 근거](2026-09-08-02-workspace-spec-scope.md).

Ticket은 `current/memory/tickets/`에 두고 정의·진행·막힘·결과를 같은 문서에 자연스럽게 남긴다. state는 Workspace 전체의 상황·판단·다음 행동을 맡고, 상세 이력은 필요할 때 records에 둔다. Ticket 구성은 Matt의 `to-tickets`를 참고하되 고정하지 않는다. [배치·구성에 관한 사용자 선택](2026-09-08-07-memory-ticket-placement-decision.md).

기존 Workspace 진입이 memory와 state를 함께 읽던 흐름을 이어 Spec 전체를 기본 진입에 포함한다. 전체 Workspace 담당은 Ticket을 읽고 작업을 진행하며, 개별 실행은 상황에 따라 다른 에이전트나 세션이 맡을 수 있다. 개별 실행자의 정확한 입력·실행 범위는 열어 둔다. [진입과 실행자 구상](2026-09-08-08-workspace-ticket-execution-direction.md).

**역할은 기존과 같다.** Maintain은 대화와 결과를 이해해 Spec·Ticket·state에 필요한 내용을 기록·갱신한다. 무엇을 남길지 판단하는 기존 동작을 유지한다. 작업의 설계·분해·위임·결과 회수·다음 행동 조율은 Main이 맡으며 Maintain에 넘기지 않는다. Main만 모든 파일을 작성해야 한다는 규칙은 두지 않았다. [독립 리뷰와 마지막 사용자 확인](2026-09-08-10-spec-ticket-authorship-independent-review.md).

## 열어 둔 부분과 앞선 후보의 지위

엄격한 Workspace당 Spec 개수 제한, Spec마다 새 Workspace 생성, Ticket의 고정 schema·상태명, 완료 시 자동 이동·삭제, 매 수정의 불변 사본은 정하지 않았다. 실행자를 반드시 새 세션으로 만들거나 모든 결과를 최초 Main 세션으로 회수하는 규칙도 없다. 이런 항목을 구현 전에 모두 확정하는 절차를 요구하지 않는다.

[외부 Ticket 용례 조사](2026-09-08-03-ticket-references-and-placement.md)의 정의·진행 분리 제안, [memory 제거 재검토](2026-09-08-04-memory-removal-and-records-boundary.md), [제3 리뷰](2026-09-08-05-memory-ticket-independent-review.md)의 약한 제거 선호, [Ticket 보존 배치 후보](2026-09-08-06-ticket-preservation-placement-candidate.md)는 당시 판단 근거다. 현재 선택은 memory 유지와 Ticket 정의·진행 통합이다. 과거 기록의 문구를 새 결론으로 고쳐 쓰거나 삭제하지 않았다.

[Main·Maintain 책임 분석](2026-09-08-09-main-maintain-responsibility-analysis.md)과 작성 책임 리뷰의 여러 대안은 검토 과정이다. 최종 확인은 역할 재설계가 아니라 기존 Maintain의 기록·갱신과 Main의 작업 조율을 이어가는 것이다.

## 실제 적용에서 남은 일

1. **Workspace 최종 파일 구조와 진입점 정리.** 합의한 폴더·다섯 구성 파일·기존 파일의 대체와 유지를 실제 구조로 구체화한다. 이 기록에서는 새 파일명이나 추가 index 파일을 확정하지 않는다.
2. **Recover의 읽기 반영.** Spec 전체를 기본 진입에 포함하도록 하위 폴더 읽기를 바꾼다. Workspace 진입에서 Ticket 목록과 필요한 본문을 읽을지, 본문 전체를 함께 읽을지는 아직 정하지 않았다. 직전 Main이 남은 선택으로 제시한 것이며 개별 실행자의 고정 입력 정책과는 다르다.
3. **Maintain의 기록 대상 반영.** 역할을 넓히지 않고 Spec·Ticket 하위 파일의 읽기·생성·갱신을 지원한다. 실제 결과를 기록할 때 필요한 전달과 본문 준비 시점을 대조하되, 별도 작업 조율 기능을 Maintain에 추가하지 않는다.
4. **생성·이식·기존 참조와 검증.** Workspace 생성 방식과 안내·이식 절차, 기존 goal·constraints 경로를 참조하는 부분을 대조해 필요한 변경을 적용한다. Recover·Maintain·관련 검증이 새 구조에서 동작하는지 확인한다. Verify 등은 실제 영향이 있는 부분을 확인해 반영하며 이름이 거론됐다는 이유로 책임을 확대하지 않는다.

다음 논의의 출발점은 이 선택을 반영한 전체 폴더 구조와 기본 읽기 순서다. 이번 요청은 기록 정리이며 실제 파일 배치·runtime 구현을 시작하라는 승인으로 해석하지 않는다.

## 유지할 문제의식과 확인 범위

Ticket 완료나 테스트 통과가 전체 목표 달성을 대신하지 않아야 한다. 과거 Spec·설계·구현도 새 근거가 생기면 필요한 범위에서 다시 판단할 수 있어야 한다. 결과가 부족하다는 이유만으로 목표를 낮추거나, 확인되지 않은 실행자의 보고를 실제 검증으로 올리지 않는다. 이 책임은 문서를 누가 쓰는지 하나로 해결되지 않는다.

기존 연구와 리뷰의 이유·원문·근거 위치는 원래 기록에 남겨 두었다. 이번에는 010의 진입 문서·current·output 안내·records 색인을 정리했다. 채택한 Spec 구성과 예시 본문, 다른 Workspace·Reference·외부 연구 자료는 변경하지 않았다.

이전 작업의 커밋 경계는 다음과 같다.

- `6e12f10`: 대화 처음부터의 논의를 010으로 분리해 기록.
- `6982fbe`: Spec 구성요소·이유·예시의 채택과 관련 논의 기록.
- `5320930`: Spec 배치와 기존 current 대체 결정 기록.

이후 Ticket 외부 용례·memory 재검토·리뷰·기존 역할 확인과 이번 정리는 아직 커밋하지 않았다. 문서 내부 링크와 Git diff 형식을 확인하며, 실제 Reference의 새 구조나 운영 효과를 검증한 작업은 아니다. 제품·runtime 테스트를 수행하지 않는다.
