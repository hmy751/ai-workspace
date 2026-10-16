# 현재 논의의 진입점

- [memory.md](memory.md): 배경과 평가에서 얻은 경험, Spec·Ticket을 쓰게 된 흐름.
- [spec.md](spec.md): 전체 작업의 목표·공통 기준·현재 전체 잠정안·선택과 미정. 3절에서 014의 Spec·Ticket과 개선할 시스템의 Spec·Ticket을 구별한다. 계속 설계할 때 읽는 작업 정의와 전체 구상의 정본이다.
- [tickets/index.md](tickets/index.md): 상위 Ticket 01~07과 하위 Ticket의 관계. 개발 방식·스킬 보완은 각 폴더의 README에서 하위 Ticket을 찾는다. 상위 문서는 범위·관계를, 개별 Ticket 본문은 상세 결과·완료 조건·진행을 소유한다.
- [state.md](state.md): 지금의 전체 단계와 다음 대화에서 이어갈 위치. 각 Ticket의 상세 상태를 복제하지 않는다.
- [design-map.md](design-map.md): 열린 논의 영역과 Ticket의 연결. 분해에서 놓친 관점을 찾는 자료이며 확정된 아키텍처가 아니다.

**이번 재개:** 전체 [Spec 3절](spec.md) → [state](state.md) → [01-02](tickets/01-development-workflow/01-02-code-design-quality.md)에서 흐름을 복원한다. [최신 종합 54](../records/2026-10-16-54-code-quality-criteria-and-remaining-work.md)에 기준·적용 조건·미확정과 다음 작업을 모았다. 계획 42의 추가 영역을 살펴보고 fetcher 검토 판단에 사용자 수용을 얻었으나 실제 수정·검증 효과는 미확인이다. 상세 사례는 54의 링크에서 선택한다. 현재 다음 추천과 검증 범위는 state가 소유한다.

원문과 당시 제안은 [source](../source/README.md), 상세 과정과 비교는 [records](../records/README.md), 선택한 현재 산출물은 [output](../output/index.md)에 연결한다. Main이 이 Workspace의 수동 운영 기준으로 갱신한다. Spec·Ticket의 의미 관계를 사용하되 Reference 자동화의 파일 배치·machine 계약을 설치한 것은 아니다.

다른 세션에서 이어갈 때는 [재진입 점검 56](../records/2026-10-16-56-session-handoff-check.md)의 확인 범위와 첫 행동을 함께 본다. 실제 사용 코드부터 설명하는 대화 방식과 과거 회고의 불확실성을 보존하며, 상태의 최신 원천은 위 current 문서다.
