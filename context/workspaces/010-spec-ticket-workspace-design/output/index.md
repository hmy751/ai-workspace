# Spec·Ticket 설계 output

마지막 갱신: 2026-09-08

## 채택한 현재 산출물

2026-09-08 사용자가 Spec 구성요소·구성 이유·예시를 이 수준으로 결정했다. 예시 본문과 설명 문서는 서로 분리한다.

1. [Spec 구성요소와 구성 이유](spec-components-and-rationale.md): 채택한 다섯 부분의 역할과 원래 문제의식에 따른 이유. 다음 설계 논의의 기준이다.
2. [예시 Spec — 여행 상품 자료에 근거한 질문 답변](spec-example-travel-answer.md): 위 구성을 적용한 구체 본문. 실제 TripProof API나 모든 Spec의 공통 요구를 확정하는 문서는 아니다.

후속 설계에서 Spec은 `memory/spec/` 아래 다섯 구성요소를 각각 Markdown 파일로 두기로 했다. 기존 goal·작업별 constraints는 Spec이 대체하고, project-context는 유지한다. 예시 본문은 구성을 보여 주는 연구 산출물로 그대로 두며 실제 Reference 적용은 아직 하지 않았다.

Ticket은 `memory/tickets/`에 두고 정의·진행을 같은 문서에 자연스럽게 남기기로 했다. 구성은 Matt의 Ticket을 기본으로 삼되 고정하지 않고 작업에 맞게 조정한다. state는 전체 상황·판단을 맡고, 기록 보존에 필요하면 records를 사용한다. 상세 상태 체계나 자동 이동 규칙은 정하지 않았다.

## 논의 과정과 근거

- [설계 합의와 적용 전 남은 작업](../records/2026-09-08-11-design-status-and-remaining-work.md): 전체 논의가 현재 어떤 선택으로 이어졌는지, 열어 둔 부분과 실제 적용에서 남은 일을 모은 기록.
- [작성 책임 리뷰와 후속 선택](../records/2026-09-08-10-spec-ticket-authorship-independent-review.md): Maintain은 Spec·Ticket·state의 기록·갱신을, Main은 작업 조율을 맡는다. 실제 Reference 동작은 아직 변경하지 않았다.
- [memory 유지와 Ticket 관리 결정](../records/2026-09-08-07-memory-ticket-placement-decision.md): 사용자가 선택한 위치·정의/진행 통합·필요에 따른 records 사용과 선택 범위.
- [memory·Ticket 배치 제3 리뷰](../records/2026-09-08-05-memory-ticket-independent-review.md): 선택 전 유지·제거 양안과 기존 의미의 변화, reviewer의 약한 제거 선호 및 Main의 대조.
- [범위·memory 배치·기존 파일과의 관계](../records/2026-09-08-02-workspace-spec-scope.md): Spec 하나라는 가정, Workspace와 함께 유지하는 수명, goal·constraints 대체, project-context 유지와 다섯 Markdown 파일 결정.
- [구성요소 합의와 논의 종합](../records/2026-09-08-01-spec-components-decision.md): 원문·분석 재독, 외부 자료, 축약·확장 초안, 독립 리뷰, 설명 정정, 두 문서 분리와 최종 합의.
- [첫 세션 종합](../records/2026-09-07-01-session-synthesis.md): 첫 Spec·Ticket 필요성부터 current 중복, 개발 영향, 스냅샷, memory/state, 배치 후보, 개념 트레이드오프와 010 분리까지. 당시 미결정 상태를 담은 역사 기록이다.
- [초기 Spec·Ticket과 current 비교](../../009-project-work-continuity-integration/records/2026-09-07-09-spec-ticket-current-assessment.md): 009에서 작성한 당시 공개 자료·Reference 비교. 공유 Spec 등 이후 수정된 후보를 포함한다.
- [초기 개발 영향 분석](../../009-project-work-continuity-integration/records/2026-09-07-10-spec-development-impact.md): revision 5e45310 기준 Recover·Maintain·Verify·생성·이식 접점과 당시 임시 fixture·회귀 검사.

## 실제 적용의 상태

기존 Maintain의 기록·갱신과 Main의 작업 조율을 유지한다. 최종 파일 구조·기본 읽기 순서, Recover·Maintain과 생성·이식 절차의 실제 적용은 [state](../current/state.md)에서 이어간다. Ticket 항목과 개별 실행자 범위를 모두 고정하는 것을 선행 조건으로 두지 않는다. Spec 하나라는 가정과 Workspace별 독립 스냅샷 조건도 유지한다.
