# 목표와 유지할 범위

## 사용자 요청

2026-09-09: “그럼 니가 서브 시킬래? 이식 아까 이식할때 문서 전체 까진 말고 제약 두고”. 이어 “근데 너무 많은 제약은 주지말고”라고 조정했다.

대상은 `/Users/hammyeong-yeon/Desktop/10_work/noline`이다. 최신 이식 skill에 따라 기존 설치를 보완한다. 내부 worker가 실행하고 Main이 구체 변경안·근거·독립 검토 결과를 판단한다.

## 범위

- 최신 이식 skill에 따라 Noline의 기존 설치를 보완한다.
- 기존 상세 문서 전체 정비와 제품 리팩토링은 이번에 하지 않는다.
- 기존 사용자 작업과 Noline 고유 연결을 보존한다.
- 사용자 정정으로 확인한 이식 기준의 허점은 source의 이식 skill과 Reference 원본에서도 보완한다. Source 변경과 target에 실제 적용한 판본을 구분한다.
- Noline 후속 작업에서 검증된 공통 Harness 개선은 제품별 Workspace 상태와 분리해 Reference에 역반영하고, 원래 근거와 새 검증의 입증 범위를 구별한다.
- Noline 적용 결과의 결함을 곧바로 제품별 수정안으로 복제하지 않는다. 기존 Reference 계약의 실행 누락과 원천 계약의 실제 공백을 구별하고, 공통 공백만 source 계약에 역반영한다.
- 사용자가 한정한 주제의 Project Owner 이동은 해당 범위에서 끝까지 수행할 수 있어야 한다. Ticket·Workspace·evidence 묶음은 근거이지 문서 책임이 아니며, Project 문서는 지속 주제·판단 질문·수명·갱신 Owner로 구성하고 이전 canonical과 live consumer의 관계까지 닫는다.
- 외부 target의 commit이나 파일이 공통 판단의 핵심 근거라면 링크만 남기지 않는다. target의 현재 canonical 전체를 복제하지 않으면서, 판단 재검토에 필요한 최소 원문·판본 식별자·검토 결과와 한계를 source-side 기록에 함께 보존한다.

파일 구성·전환 방식·조사·검증은 live skill과 worker의 판단에 맡긴다. Main의 초기 세부 brief는 구현 정답이나 추가 gate가 아니며, 별도 문서·확인 절차를 불필요하게 늘리지 않는다. 후속 정정을 worker에게 전달했다.

## 평가와의 관계

사용자는 이식 뒤 리팩토링으로 개선안을 평가한다. 정비 전 코드·문서 상태와 개입 판본, 실제 준비·유지 비용을 보존한다. 정비 과정에서 얻은 이해를 제외한 채 결과를 특정 스킬의 단독 효과로 해석하지 않는다. 실제 후속 개발·재진입이 없으면 그 효과는 미확인으로 둔다.

평가 원자료는 `/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/09-improvement-evaluation/`이며 이번 이식에서 수정하지 않는다. 의존 문장·판본과 해석은 [선행 기록](../../010-spec-ticket-workspace-design/records/2026-09-09-02-noline-installed-state-assessment.md)에 보존했다.
