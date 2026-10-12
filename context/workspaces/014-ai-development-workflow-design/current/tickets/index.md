# 설계 Ticket

전체 목표와 기준은 [Spec](../spec.md), 전체 진행은 [state](../state.md)가 맡는다. **상위 Ticket은 01~07이며, 01과 04는 각각 세 하위 Ticket으로 나뉜다.** 파일명·제목·참조에 같은 번호를 사용한다. 01-01에서 자료 기반 워크플로를 비교했고, 01-02·01-03의 품질·검증 책임 연결도 초안으로 다뤘다. 상세 진행은 각 Ticket이 소유한다. B의 검토자 직접 수정 방향은 선택했고 상세 운영 연결은 계속 설계한다.

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

**다음은 01-02다.** 사용자는 품질·설계 기준을 바로 확정하기 전에 자료의 구체적인 방법·예시·적용 조건을 정리해 함께 논의하도록 선택했다. [선택과 체크포인트](../../records/2026-10-12-18-quality-materials-next-step.md). 01-01의 역할 흐름은 잠정안으로 두고, 01-02에서 선택한 기준·배치에 따라 보완한다. 관련 Ticket의 연결은 유지하되 지금 필요한 결정에 따라 선택해서 다루며 모두를 동시에 구체화하는 순서로 고정하지 않는다. 초기 연결 초안과 개발 방식 전체의 설계 완료를 구별한다.

**04의 하위 Ticket**은 관련 주제를 다룰 때 현행 스킬을 함께 대조하고 보완한다. **05**는 기록 유지와 구별되는 경험 반영을 맡는다. **02**는 current 등을 포함한 Workspace 구성 자체도 비교한다. **06**은 프로젝트 경험을 ai-workspace 개선으로 연결하고 다시 반영하는 방법도 검토하며, 새 관리 장치의 도입은 전제하지 않는다. **06**의 기존 결합 확인과 **07**의 부분 연결 검토도 필요한 시점부터 한다.

번호는 과제의 소속을 나타내며, 모든 과제를 번호순으로 완결해야 하는 절차나 별도 agent 배치를 뜻하지 않는다. 각 과제의 설계안·운영 방식은 앞으로 구체화한다. 전제가 바뀌면 관련 Ticket과 Spec을 함께 보완한다.

[논의 지도](../design-map.md)는 과제를 가로지르는 관점을, [분할 기록](../../records/2026-10-12-09-ticket-split.md)은 나눈 이유와 정리 결과를 설명한다.
