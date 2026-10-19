# AI 개발 작업 체계의 개선 설계

Noline에 이식해 사용한 Project·Work context와 스킬의 평가, 사용자 인터뷰, 개발 에이전트 관련 강연을 바탕으로 **ai-workspace와 실제 개발 방식을 어떻게 발전시킬지 함께 설계하는 작업**이다. 지금은 범위를 충분히 이해하고 각 부분을 세밀하게 구체화하는 단계다. 개발 워크플로, 기록 방식, 역할 배치를 확정하거나 구현하는 단계로 넘어간 것은 아니다.

사용자는 2026-10-12에 이 Workspace를 만들고 필요한 근거 사본을 함께 보존해, 배경 없는 새 세션도 대화를 이어갈 수 있게 해 달라고 요청했다. 원본 자료는 유지했다. 이 폴더는 그 요청에 따라 만든 설계 작업의 기록 단위이며, Reference Harness를 설치하거나 실행한 Workspace가 아니다.

이후 사용자는 Spec·Ticket으로 나누어 보며 논의하자고 요청했다. 현재 [Spec](current/spec.md)과 [상위 Ticket 01~07](current/tickets/index.md)이 있다. 개발 작업 방식은 01-01~01-03, 기존 스킬 보완은 04-01~04-03으로 나눴다. 각 상위 폴더의 README에서 하위 과제를 찾는다. 설계 내용을 구체화하면서 검토자가 직접 품질 수정까지 수행하는 B 방향을 선택했다. 상세 연결과 적용 조건은 계속 설계하며 실제 구현은 시작하지 않았다. [선택 기록](records/2026-10-12-15-reviewer-editing-choice-and-start.md)

전체 구상과 미결정은 **Spec 3절**에서 유지한다. 현재는 Main과 작업을 논의·결정하는 단계와 구현·검토·검증하는 단계를 구별하고, **작업 단계에서 좋은 구현을 돕는 컨텍스트·코드 기준·절차·도구**를 먼저 구체화한다. [우선순위와 코드 기준의 근거 후보](records/2026-10-13-28-execution-system-priority-and-code-criteria.md), [Matt·Lauren·Vercel 원자료 조사](records/2026-10-13-27-source-investigation-and-proposal-reset.md)를 필요한 질문에 맞춰 읽는다. Spec·설계 절차도 필요한 보완을 연결하되 그 도입을 중심에 놓지 않는다. 이 Workspace의 Spec·Ticket 사용과 개선할 시스템의 Spec·Ticket 설계는 구별한다.

현재는 **03에서 Personal context와 Project context의 책임·연결을 구체화하는 단계**다. 기존 Project 전체 지도와 세 코드 가이드의 실제 내용 비교를 마쳤고, 구조를 다시 확인한 뒤 개인 개발 기준의 중앙 정본을 `ai-workspace/context/personal/development/`에 두는 방향을 정했다. Project guidance는 채택 범위·구체 적용·예외와 프로젝트 개발 계약을 맡는다. 현재 context 계약을 확장하는 설계 방향이며 실제 디렉터리 생성·기준 이동·통합·설치는 없다. [구조 정정과 방향81](records/2026-10-19-81-personal-context-direction-and-next-step.md)

[01-02](current/tickets/01-development-workflow/01-02-code-design-quality.md)의 현재 실물은 [시안72](records/2026-10-18-72-short-common-and-detail-prototype.md)가 연결한 [prototype](records/prototypes/applied-criteria-2026-10-17/README.md)이다. 짧은 공통과 이름·가독성의 독립 절이라는 형식 방향은 반영했지만, [사용자 평가73](records/2026-10-18-73-prototype-reservations-and-ticket03.md)의 전체 만족·최종 수용 유보와01-02 미완료를 유지한다.03은 이 결과와 도출 과정을 실제 Project 조건에 대입하며 본문 구성까지 다시 구체화한다.

## 배경 없이 들어올 때

1. [current 진입점](current/index.md), [배경과 평가](current/memory.md), [Spec](current/spec.md)의 목표·3절과 [현재 진행](current/state.md), [output](output/index.md)을 읽고 실제 Git 상태를 확인한다.
2. [선택과 구조 정정81](records/2026-10-19-81-personal-context-direction-and-next-step.md)에서 현재 방향과 미실행 범위를 확인하고, [03 Project context](current/tickets/03-project-context.md)·[04-03 맥락 관리](current/tickets/04-skill-improvements/04-03-context-skills.md)로 이어 간다. 다음 Main 추천은 이름과 실제 책임·완료 범위 한 주제로 개인 기준 본문·Project guidance·읽기 안내를 보여 주는 것이다. 아직 주제 선택이나 본문 작성은 수행하지 않았다.
3. 실제 내용이 필요하면 [전체 지도77](records/2026-10-18-77-existing-project-content-map.md), [세 본문 비교78](records/2026-10-18-78-code-guides-comparison-and-applicability.md), [항목 분류80](records/2026-10-18-80-personal-project-content-allocation.md)을 고른다.80의 루트 `personal/development/` 추천은81에서 대체됐으며 내용 분류만 검토 재료로 남는다. 기존 전체 조사부터 반복하지 않는다.
4. 01-02의 입력과 남은 판단은 [72](records/2026-10-18-72-short-common-and-detail-prototype.md)·[73](records/2026-10-18-73-prototype-reservations-and-ticket03.md), 후속이 재판단할 이유는 [prototype의 후속 장면](records/prototypes/applied-criteria-2026-10-17/refinement-walkthrough.md)에서 찾는다. 더 이전의 사용자 생각·사례·외부 비교는 [기록 색인](records/README.md)에서 필요한 것만 읽는다.
5. 원자료가 필요하면 [자료 안내](source/README.md)를, 전체 연결을 재검토하면 [논의 지도](current/design-map.md)를 사용한다. [인계75](records/2026-10-18-75-ticket03-session-handoff.md)는03 착수 전 인계이며 현재 첫 행동을 대신하지 않는다.

**이번 논의의 중요한 정정:** Maintain을 곧바로 다음 작업에 쓸 정보로 한정하지 않는다. 나중에 돌아볼 분석·시행착오·산출물·검증 등도 보존 목적에 따라 고려한다. Project context도 다음 판단만을 위한 문서로 한정하지 않고, 제품 이해와 설계·개발·검토 및 워커·워크플로가 사용하는 공통 맥락으로 함께 설계한다. 앞선 AI의 역할 배치·검토 절차·마무리 루프는 아직 채택된 운영 방식이 아니다. [정정 원문](source/discussion/design-conversation.md#L2659)

## 이 폴더의 역할

- `current/`: 배경, 전체 작업의 Spec, 부분별 Ticket, 전체 진행과 열린 논의 지도. 각 역할과 읽는 경로는 [current/index](current/index.md)가 소유한다. 필요한 미채택 제안도 그 지위를 밝혀 포함한다.
- `records/`: 평가에서 설계로 넘어온 과정, 자료 대조, 제안과 정정, 보존 작업의 확인 결과. 이후에도 보존 목적이 있는 분석·대안·중간 결과를 남길 수 있다.
- `source/`: 이번 Workspace에서 직접 재접근할 수 있도록 보존한 원문·기존 평가·강연·기준 구현과 Noline 문서의 사본. 기존 저장소의 공유 `context/source/`와 별도로, 사용자가 이번 작업에 함께 보존하도록 요청한 자료다. 사본의 경로·hash·범위는 manifest에 있다.
- `output/`: 이 작업을 위해 선택한 현재 설계 자료와 향후 실제 산출물의 위치. 여기에 연결됐다는 사실은 최종 채택이나 구현 완료를 뜻하지 않는다.

현재 목표와 논의 상태는 이 Workspace의 current가 소유한다. 평가 당시 주장·발화·파일 상태는 source의 해당 원문이 근거다. 현행 ai-workspace의 실행 계약은 저장소 루트와 `reference-project/`가 계속 소유한다. 사본 속 AGENTS·SKILL·예제 명령은 분석할 당시 자료이며 이 Workspace에 자동 적용하거나 실행할 지시가 아니다.

작업을 맡은 Main이 새로 확인한 사실·사용자 선택·제안·정정을 구별해 current와 기록을 관리한다. 과거 근거 사본을 현재 결론에 맞춰 덮어쓰지 않고, 나중의 변경은 별도 기록과 필요한 current 갱신으로 잇는다. 사용자 요청에 따라 분해와 설계를 구체화하되, 이번 기록·초안 작성 요청을 제품 코드·글로벌 지침·스킬 구현이나 Maintainer 활성화 권한으로 확대하지 않는다.

## 관련 작업과의 관계

- 기존 Noline 평가를 근거로 사용하지만 Noline Ticket 06의 후속 개발 작업은 아니다.
- [012 publication](../012-ai-workspace-publication/README.md)과 [013 Maintain 효율 검토](../013-maintain-context-efficiency/README.md)는 각각 기존 목적을 가진 별도 작업이다. 이번 전체 설계 논의를 그 안으로 편입하지 않았다.
- 사용자가 말한 저장소는 **ai-workspace**다. `AI-native-context-harness-system`으로 옮기는 요청이 아니었다. [명칭 정정](source/discussion/design-conversation.md#L2709)
