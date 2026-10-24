# 설계 Ticket

전체 목표·기준·현재 전체 잠정안은 [Spec](../spec.md), 전체 진행은 [state](../state.md)가 맡는다. 이 목록은 **014의 설계 작업을 나누는 Ticket**이며 개선할 시스템의 Ticket 표준을 확정한 것이 아니다. **상위 Ticket은 01~07이며, 01과 04는 각각 세 하위 Ticket으로 나뉜다.** 파일명·제목·참조에 같은 번호를 사용한다. 01-01에서 자료 기반 워크플로를 비교했고, 01-02·01-03의 품질·검증 책임 연결도 초안으로 다뤘다. 상세 진행은 각 Ticket이 소유한다. 01-01·01-03은 합의·실행 본문·대표 대조를 완료 조건에 맞춰 설계 마감했다.01-02의 품질 기준 전체 종합과04-03의 개별 맥락 스킬 보완은 남아 있다. [이번 마감과 Spec·04의 다음 범위](../../records/2026-10-24-ticket01-01-03-closeout-and-next-scope.md)에서 완료 범위와 후속 책임을 확인한다.

| 상위 Ticket | 하위 Ticket |
| --- | --- |
| [01 개발 작업 방식](01-development-workflow/README.md) | [01-01 진행·사람 판단](01-development-workflow/01-01-development-flow.md), [01-02 품질·검토·수정](01-development-workflow/01-02-code-design-quality.md), [01-03 동작 검증·도구](01-development-workflow/01-03-behavior-verification.md) |
| [02 기록·Workspace 구성·Maintain](02-work-records.md) | — |
| [03 Project context](03-project-context.md) | — |
| [04 기존 스킬 보완](04-skill-improvements/README.md) | [04-01 작업 정의·재판단](04-skill-improvements/04-01-work-decision-skills.md), [04-02 설명 구성·적용](04-skill-improvements/04-02-artifact-explanation.md), [04-03 맥락 관리](04-skill-improvements/04-03-context-skills.md) |
| [05 경험 반영 루프](05-learning-loop.md) | — |
| [06 기반 전환·프로젝트 간 개선 반영](06-framework-transition.md) | — |
| [07 전체 연결과 후속 적용](07-integrated-rehearsal.md) | — |

상위 01·04의 README는 목적·범위와 하위 결과의 관계를 소유한다. 하위 Ticket은 상세 결과·완료 조건·진행을 소유한다. 나머지 상위 Ticket은 각 본문이 직접 결과를 맡는다. 진행을 두 곳에서 중복 관리하지 않는다.

## 이어갈 순서와 관계

**2026-10-20:03의 구성안·대표 본문 구체화를 완료했다.** [완료 조건 대조119](../../records/2026-10-20-119-ticket03-closeout.md)와 [03 결과](03-project-context.md)를 후속 입력으로 사용한다.01-02·04-03 등 다른 Ticket의 완료로 확대하지 않으며 이번 마무리에서 새 작업을 시작하지 않았다.

다음 중심은 **01-01과04-03을 함께 보는 워크플로·기존 스킬 구체화**다. 현재 DEVELOPMENT에서 입력 선택·인계·검토·최종 확인과 결과별 갱신을 읽고, 기존 스킬이 맡는 행동과 비교한다. 절차 본문의 최종 이름·위치·Owner와 실제 운영은 그때 판단한다. [사용자 후속 방향103](../../records/2026-10-19-103-prototype-session-checkpoint.md)과 현재 [state](../state.md#다음에-이어갈-일)에 재개 조건이 있다.

| 후속 결과 |03에서 이어받을 것과 경계 |
| --- | --- |
|01-01·04-03 | 독립된 Personal·Project 본문과 선택·충돌·갱신 기본값, 체계 지침과 진입·상세의 구별. 공통 역할·인계·수정·검증은01-01·01-03에서 마쳤고, 개별 맥락 스킬의 조건·행동 보완은04-03이 잇는다. |
|02 | Work는 기존 형태와 제약을 유지한다. [116](../../records/2026-10-20-116-defer-work-content-policy.md)의 복구 이유와 형성 맥락·기록 관계를 필요한 때 논의한다.01-01의 선행 완료 조건은 아니다. |
|01-02·01-03 | 현재 본문 구성과 사례를 사용해 품질 검토·수정 방법 및 실행 증거를 구체화한다.01-02의 기준 전체 수용·완결은 남아 있다. |
|06·07 | 실제 배치·전환과 부분 결과의 전체 연결·사용 효과. 데모 파일 구성만으로 운영 설치가 끝났다고 보지 않는다. |
|05 | 기록 유지와 별개로 경험에서 개선 후보를 만들고 채택·반영·효과를 판단한다. |

현재 Personal·Project 관리 단위는 독립 본문과 연결을 갖춘 안이다. 모든 계약·가이드의 최종 묶음을 일률 확정하지 않았으며, 후속에서 새 조건이나 실제 누락·중복이 드러나면03 결과도 함께 보완한다. 완료는 수정 금지를 뜻하지 않는다.

번호는 결과 책임을 식별한다. 모든 과제를 번호순으로 완결하거나 별도 agent를 붙이는 절차가 아니다. 사용자는93에서 연결된 논의를 티켓 경계로 지나치게 분리하지 말고02는 뒤에 다룰 수 있다고 정정했다. [74](../../records/2026-10-18-74-ticket-flow-after-quality-draft.md)·[75](../../records/2026-10-18-75-ticket03-session-handoff.md)의 이전 순서는 당시 기록으로 보존한다.

전체 목표와 공통 기준은 [Spec](../spec.md), 현재 행동은 [state](../state.md), 영역을 가로지르는 관점은 [논의 지도](../design-map.md)에서 찾는다. [과정 연결65](../../records/2026-10-18-65-criteria-status-and-cross-ticket-refinement.md)를 통해 필요한 이전 조건·대안·정정을 골라 읽고 후속의 새 판단을 현재 본문에 돌려준다.
