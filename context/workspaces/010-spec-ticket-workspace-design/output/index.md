# Spec·Ticket 설계 output

마지막 갱신: 2026-09-08

## 채택한 현재 산출물

2026-09-08 사용자가 Spec 구성요소·구성 이유·예시를 이 수준으로 결정했다. 예시 본문과 설명 문서는 서로 분리한다.

1. [Spec 구성요소와 구성 이유](spec-components-and-rationale.md): 채택한 다섯 부분의 역할과 원래 문제의식에 따른 이유. 다음 설계 논의의 기준이다.
2. [예시 Spec — 여행 상품 자료에 근거한 질문 답변](spec-example-travel-answer.md): 위 구성을 적용한 구체 본문. 실제 TripProof API나 모든 Spec의 공통 요구를 확정하는 문서는 아니다.

## 논의 과정과 근거

- [구성요소 합의와 논의 종합](../records/2026-09-08-01-spec-components-decision.md): 원문·분석 재독, 외부 자료, 축약·확장 초안, 독립 리뷰, 설명 정정, 두 문서 분리와 최종 합의.
- [첫 세션 종합](../records/2026-09-07-01-session-synthesis.md): 첫 Spec·Ticket 필요성부터 current 중복, 개발 영향, 스냅샷, memory/state, 배치 후보, 개념 트레이드오프와 010 분리까지. 당시 미결정 상태를 담은 역사 기록이다.
- [초기 Spec·Ticket과 current 비교](../../009-project-work-continuity-integration/records/2026-09-07-09-spec-ticket-current-assessment.md): 009에서 작성한 당시 공개 자료·Reference 비교. 공유 Spec 등 이후 수정된 후보를 포함한다.
- [초기 개발 영향 분석](../../009-project-work-continuity-integration/records/2026-09-07-10-spec-development-impact.md): revision 5e45310 기준 Recover·Maintain·Verify·생성·이식 접점과 당시 임시 fixture·회귀 검사.

## 아직 정하지 않은 통합 설계

Spec과 Workspace의 범위 계약, current의 goal·constraints 소유, 실제 Ticket 체계, 물리적 저장·파일 분할, 소비자별 읽기·갱신·결과 재판정과 Reference 구현·migration은 남아 있다. 다섯 구성의 채택을 필수 파일 목록이나 runtime 활성화로 해석하지 않는다. Workspace별 독립 스냅샷 조건은 유지한다.
