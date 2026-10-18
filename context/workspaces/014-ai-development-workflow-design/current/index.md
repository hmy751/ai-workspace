# 현재 논의의 진입점

최신 결과는 [짧은 공통·상세 절을 반영한 시안72](../records/2026-10-18-72-short-common-and-detail-prototype.md)다. 사용자가 선택한 공통의 짧은 적용 관점과 이름·가독성의 별도 절을 기존 prototype에 반영했다. quality의 공통 두 문단과 네 상세 절, Project 한곳의 읽기 안내, 주문의 현재 계약·조건별 사례·작업 요구와 구현 전 판단 장면이 연결돼 있다. 01-02는 현재까지 중간 정리한 미완료 상태이며, [진행 흐름74](../records/2026-10-18-74-ticket-flow-after-quality-draft.md)에 따라 다음 중심을03으로 옮긴다. 이후 실제 맥락·진행·검증 조건을 받아01-02를 다시 종합한다. 형식 방향의 선택과 기준 모든 내용·최종 운영 배치·실제 효과의 확정은 구별한다. [후속 평가73](../records/2026-10-18-73-prototype-reservations-and-ticket03.md)에서 사용자는 현재 시안이 전반적으로 아주 마음에 드는 것은 아니며 구체화는03과 연결된다고 밝혔다. 다음 판단에서는 이 유보도 함께 읽는다.

현재 적용 장면은 [시안 입구](../records/prototypes/applied-criteria-2026-10-17/README.md)와 [주문 읽기 장면](../records/prototypes/applied-criteria-2026-10-17/order-walkthrough.md)에서 읽는다. 구성과 경계의 도출 근거는 [70](../records/2026-10-18-70-criteria-organization-proposal.md)·[71](../records/2026-10-18-71-order-reading-and-criteria-boundaries.md), 이전 적용 보완은 [68](../records/2026-10-18-68-principle-application-and-choice-basis.md)이다. [후속 재판단 장면](../records/prototypes/applied-criteria-2026-10-17/refinement-walkthrough.md)은03이 이번 결과와 과정·근거를 새 조건에 대입할 부분과 이유를 소유한다. 주문 구현·검사는 미실행이며 기존 HTTP·Field의 결과도 가상이다.

- [memory.md](memory.md): 배경과 평가에서 얻은 경험, Spec·Ticket을 쓰게 된 흐름.
- [spec.md](spec.md): 전체 작업의 목표·공통 기준·현재 전체 잠정안·선택과 미정. 3절에서 014의 Spec·Ticket과 개선할 시스템의 Spec·Ticket을 구별한다. 계속 설계할 때 읽는 작업 정의와 전체 구상의 정본이다.
- [tickets/index.md](tickets/index.md): 상위 Ticket 01~07과 하위 Ticket의 관계. 개발 방식·스킬 보완은 각 폴더의 README에서 하위 Ticket을 찾는다. 상위 문서는 범위·관계를, 개별 Ticket 본문은 상세 결과·완료 조건·진행을 소유한다.
- [state.md](state.md): 지금의 전체 단계와 다음 대화에서 이어갈 위치. 각 Ticket의 상세 상태를 복제하지 않는다.
- [design-map.md](design-map.md): 열린 논의 영역과 Ticket의 연결. 분해에서 놓친 관점을 찾는 자료이며 확정된 아키텍처가 아니다.

**이번 재개:** 전체 [Spec 3절](spec.md)과 [인계75](../records/2026-10-18-75-ticket03-session-handoff.md)·[state](state.md)에서 흐름을 복원하고, [03](tickets/03-project-context.md)과 [04-03](tickets/04-skill-improvements/04-03-context-skills.md)의 실제 문서·스킬 대조로 시작한다. [01-02](tickets/01-development-workflow/01-02-code-design-quality.md)는 넘겨받을 결과·남은 판단으로 읽는다. [형태·질문 논의 57](../records/2026-10-16-57-criteria-organization-and-guiding-questions.md)은 일반 기준·판단 질문·사례의 조직과 전달을 전체 체계에 연결하려는 사용자 요청과 현재 구성 후보를 담는다. [종합 54](../records/2026-10-16-54-code-quality-criteria-and-remaining-work.md)는 기준·적용 조건의 재료이며 fetcher 판단 수용과 실제 효과는 구별한다. 현재 다음 추천과 검증 범위는 state가 소유한다.

앞선 [개선 조언 59](../records/2026-10-16-59-format-design-objectives-advisor.md)에서 내용 구체화에 앞서 형식 설계의 목표·비교 기준·자료 활용 방식을 논의하라는 사용자 요청을 확인한다. 57의 본문 후보를 먼저 작성하는 순서로 읽지 않는다. 조언의 목표문·비교 기준은 미채택이다.

2026-10-17 후속 [참고 범위 60](../records/2026-10-17-60-reference-selection-before-format-candidates.md)은 어떤 외부 자료의 구체 부분을 대조하고 그 근거로 형식 후보를 도출할지 연결한다. 형식 제작 뒤에 외부 근거를 붙이는 순서가 아니다.

앞선 [비교안 61](../records/2026-10-17-61-reference-comparison-for-format-design.md)은 60의 자료에서 가져올 것·조정할 것·보류할 것과 사용자 생각·Spec에 비춘 이유·비용을 제시한다. 당시 비교 단계의 기록이며, 후속 시안은 아래 62에서 읽는다.

앞선 [시안 62](../records/2026-10-17-62-criteria-format-prototype.md)에서 연결본·통합본과 작업자·검토자에게 전달되는 실제 예시를 볼 수 있다. 형식 제작 요청을 수행했으며 최종 채택·제품 실행은 아직 없다.

사용자 정정 뒤의 적용 자료는 [사례 63](../records/2026-10-17-63-applied-criteria-project-example.md)이다. 한 프로젝트에 놓인 실제 문서 파일과 Main·구현자·검토자의 입력·결과를 가상으로 끝까지 채웠다. 제품 수정·검사·완료는 가정이며 원본 프로젝트에 적용한 결과가 아니다. 이후 도출 이유 설명과 산출물을 함께 본 [제3자 개선 리뷰 64](../records/2026-10-17-64-applied-format-improvement-review.md)가 이어졌다. 당시 조언과 추천은 그 기록에, 당시 시안 보완은66·68에 있고 현재 실물은72 상태다.

원문과 당시 제안은 [source](../source/README.md), 상세 과정과 비교는 [records](../records/README.md), 선택한 현재 산출물은 [output](../output/index.md)에 연결한다. Main이 이 Workspace의 수동 운영 기준으로 갱신한다. Spec·Ticket의 의미 관계를 사용하되 Reference 자동화의 파일 배치·machine 계약을 설치한 것은 아니다.

57 이후 사용자 요청으로 [외부 비교 58](../records/2026-10-16-58-principles-questions-and-pstack-comparison.md)에서 생각의 지지·보완점을 나누고 Lauren의 pstack 원칙·질문·작업 연결을 추가 확인했다. 형식과 전달 방법은 계속 논의 중이다.

이번 세션의 인계와 검증 범위는 [75](../records/2026-10-18-75-ticket03-session-handoff.md)가 소유한다. 이전 [재진입 점검 56](../records/2026-10-16-56-session-handoff-check.md)은 이전 인계의 확인 범위로 읽는다. 당시 첫 행동 뒤에 형태·질문 논의가 이어졌다. 실제 사용 코드부터 설명하는 대화 방식과 과거 회고의 불확실성은 유지하며, 현재 첫 행동은 state에서 확인한다.
