# 설계 Ticket

전체 목표·기준·현재 전체 잠정안은 [Spec](../spec.md), 전체 진행은 [state](../state.md)가 맡는다. 이 목록은 **014의 설계 작업을 나누는 Ticket**이며 개선할 시스템의 Ticket 표준을 확정한 것이 아니다. **상위 Ticket은 01~07이며, 01과 04는 각각 세 하위 Ticket으로 나뉜다.** 파일명·제목·참조에 같은 번호를 사용한다. 01-01에서 자료 기반 워크플로를 비교했고, 01-02·01-03의 품질·검증 책임 연결도 초안으로 다뤘다. 상세 진행은 각 Ticket이 소유한다. B의 검토자 직접 수정 방향은 선택했고 상세 운영 연결은 계속 설계한다.

| 상위 Ticket | 하위 Ticket |
| --- | --- |
| [01 개발 작업 방식](01-development-workflow/README.md) | [01-01 진행·사람 판단](01-development-workflow/01-01-development-flow.md), [01-02 품질·검토·수정](01-development-workflow/01-02-code-design-quality.md), [01-03 동작 검증·도구](01-development-workflow/01-03-behavior-verification.md) |
| [02 기록·Workspace 구성·Maintain](02-work-records.md) | — |
| [03 Project context](03-project-context.md) | — |
| [04 기존 스킬 보완](04-skill-improvements/README.md) | [04-01 작업 정의·재판단](04-skill-improvements/04-01-work-decision-skills.md), [04-02 브리핑·설명 복구](04-skill-improvements/04-02-artifact-explanation.md), [04-03 맥락 관리](04-skill-improvements/04-03-context-skills.md) |
| [05 경험 반영 루프](05-learning-loop.md) | — |
| [06 기반 전환·프로젝트 간 개선 반영](06-framework-transition.md) | — |
| [07 전체 연결과 후속 적용](07-integrated-rehearsal.md) | — |

상위 01·04의 README는 목적·범위와 하위 결과의 관계를 소유한다. 하위 Ticket은 상세 결과·완료 조건·진행을 소유한다. 나머지 상위 Ticket은 각 본문이 직접 결과를 맡는다. 진행을 두 곳에서 중복 관리하지 않는다.

## 이어갈 순서와 관계

**다음 중심은03이다.01-02는 중간 정리 상태로 두며 미완료다.** 사용자가 다음03과 이후 Ticket 흐름을 요청해 [추천 순서74](../../records/2026-10-18-74-ticket-flow-after-quality-draft.md)를 정리했다. 중심 진행은03 → 02 → 01-01 → 01-03 → 01-02 재방문 → 04-02 → 05 → 06 → 07을 제안한다.04-03은03·02,04-01은01-01과 함께 본다.06의 기존 결합과07의 부분 연결은 필요한 시점부터 확인한다. 이후 사용자는 “그래 좋아”라고 동의하고 다음 세션에서 이어가기로 했다([인계75](../../records/2026-10-18-75-ticket03-session-handoff.md)). 이를 현재 진행 방향으로 삼되, 새 조건에 따라 조정할 수 있으며 각 단계의 미정을 무조건 닫은 뒤에만 다음으로 가는 절차로 만들지 않는다.

현재 반영본은 [시안72](../../records/2026-10-18-72-short-common-and-detail-prototype.md)다. 사용자가 공통을 짧게 두고 이름·가독성을 별도 절로 두는 방향을 선택해 실제 prototype 본문·읽기 안내와 주문 문서에 반영했다. [70](../../records/2026-10-18-70-criteria-organization-proposal.md)·[71](../../records/2026-10-18-71-order-reading-and-criteria-boundaries.md)은 도출 근거, [68](../../records/2026-10-18-68-principle-application-and-choice-basis.md)은 이전 시안 보완, [69](../../records/2026-10-18-69-ticket-boundaries-and-next-design-step.md)는 잔여 책임의 전체 대조다. 다음은 반영본의 남은 판단을 확인하고03·04-03의 실제 Project·기존 스킬,01-01·01-03의 실행·검증 조건으로 잇는 것이다. 후속은 필요한 과정·근거와 새 조건을 함께 보고 기준 본문까지 다시 판단한다. 이번 형식 방향의 선택과 모든 기준·최종 운영 배치·효과 확인·Ticket 완료는 구별한다.

2026-10-18 과정 재사용 보완: 후속 Ticket은 결과물뿐 아니라 해당 판단의 조건·대안·사용자 정정을 선택해 읽고 새 조건에 따라 현재 안을 재구체화한다. [65](../../records/2026-10-18-65-criteria-status-and-cross-ticket-refinement.md)에 후속 판단별 과정 근거와 변경 반영 위치를 연결했다. 일반 원칙·구체 사례의 범위와 후보·채택·제품 계약 등의 지위를 구별하는 사용자 방향도 반영했다. 이 연결만으로 각 Ticket의 설계나 실제 적용이 완료된 것은 아니다.

지금까지의 구체 논의는 [01-02](01-development-workflow/01-02-code-design-quality.md)에 중간 정리했고, 다음 중심은03이다. [적용 사례 63](../../records/2026-10-17-63-applied-criteria-project-example.md)과 도출 이유를 함께 본 [개선 리뷰 및 후속 연결 제안 64](../../records/2026-10-17-64-applied-format-improvement-review.md)는 앞선 설계·리뷰 근거다. Main은 일반 기준·질문·조건별 선택 장면을 중심으로 03·01-01/04·02와 맞닿는 읽기·전달·기록 경계를 함께 구체화하는 것을 추천한다. 짧은 공통·이름 절의 형식 방향은72에 반영했고, 최종 운영 배치·실제 제품 수정·테스트·효과 확인은 미완료다. 사례별 기준은 [54](../../records/2026-10-16-54-code-quality-criteria-and-remaining-work.md), 사용자 생각은 [57](../../records/2026-10-16-57-criteria-organization-and-guiding-questions.md), 상세 상태는 해당 Ticket, 전체 연결은 Spec 3절에서 관리한다.

현재는 [작업 단계의 시스템을 먼저 구체화한다](../../records/2026-10-13-28-execution-system-priority-and-code-criteria.md). Main과 작업을 논의·결정하는 단계는 구별하고, 좋은 구현을 돕는 컨텍스트·코드 기준·작업 절차·검증 수단을 [원자료 조사](../../records/2026-10-13-27-source-investigation-and-proposal-reset.md)와 구체 사례로 논의한다. 선행 설계 도입이나 알림 설정 인수 예시의 상세화를 다음 순서로 고정하지 않는다. 필요한 질문에 따라 01·03·04 등을 연결하되 전체 범위와 Ticket 분할은 유지한다.

01-02 자료 논의를 진행한 뒤 사용자는 **전체 방향과 Spec·Ticket을 어떻게 사용해 설계를 모을지 먼저 재검토해 달라**고 요청했다. [요청과 제안](../../records/2026-10-13-20-overall-design-and-ticket-direction.md). 이후 세션이 바뀌어도 현재 구상을 복원하도록 [Spec 3절](../spec.md)에 전체 잠정안과 주요 미결정, 두 종류의 Spec·Ticket을 구별해 보완했다. B 선택과 01-02의 탐색을 폐기한 것은 아니며, 전체안의 필요한 질문에 따라 Ticket을 선택한다. 실제 Ticket 구조·번호와 완료 상태는 바꾸지 않았다.

**04의 하위 Ticket**은 관련 주제를 다룰 때 현행 스킬을 함께 대조하고 보완한다. **05**는 기록 유지와 구별되는 경험 반영을 맡는다. **02**는 current 등을 포함한 Workspace 구성 자체도 비교한다. **06**은 프로젝트 경험을 ai-workspace 개선으로 연결하고 다시 반영하는 방법도 검토하며, 새 관리 장치의 도입은 전제하지 않는다. **06**의 기존 결합 확인과 **07**의 부분 연결 검토도 필요한 시점부터 한다.

번호는 과제의 소속을 나타내며, 모든 과제를 번호순으로 완결해야 하는 절차나 별도 agent 배치를 뜻하지 않는다. 각 과제의 설계안·운영 방식은 앞으로 구체화한다. 전제가 바뀌면 관련 Ticket과 Spec을 함께 보완한다.

[논의 지도](../design-map.md)는 과제를 가로지르는 관점을, [분할 기록](../../records/2026-10-12-09-ticket-split.md)은 나눈 이유와 정리 결과를 설명한다.
