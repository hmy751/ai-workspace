# 현재 상태

2026-10-19. **본문 보완·원칙과 사례 분리·진행 정정까지 기록하고 중간 커밋으로 보존한다.** 사용자 요청과 이번 범위는 [마무리94](../records/2026-10-19-94-body-refinement-checkpoint.md)에 있다.92에서 기존 합의 안의 본문 정정을 반영했고,93에서 연결된 논의를 티켓별로 과도하게 나누던 진행을 바로잡았다. 다음은 현재 본문을 구체적으로 다듬고 워크플로·스킬을 함께 보는 것이다. 정확한 문장·기준 전체의 수용과 세부 운영 선택은 미정이다.

현재 실물은 [Noline demo context](../records/prototypes/development-workflow/noline-demo/context/README.md)다. 개인 본문은 personal, 제품 의미·현재 구현·가이드는 project, 이번 Spec·Ticket·state·source·output·records는 work가 소유한다. 연결 절차 시안은 Work의 DEVELOPMENT.md에 있으며 이 위치·이름·소유 책임은 미확정이다. 89의 구조 정정 때 이동한 예제 경로에서 검사7개와 정상·조회 실패 demo를 Main이 직접 실행했다. 이후91~94는 본문·기록·표시 확인이며 제품 동작 검사를 새로 수행한 것은 아니다. 화면은 실제 폴더 탐색으로 시작하도록 재생성하고 원문·경로·스크립트를 정적으로 확인했다. 실제 Noline·자동 Harness·UI 통합과 전체 기준 채택은 확인하지 않았다. 바깥 운영 context와 원본 Noline을 변경한 것은 아니다.01-02·03·04-03·06은 미완료다.

[7쌍 본문 비교](../records/prototypes/criteria-format-comparison-2026-10-19/README.md)는 이번 보완 전01·새 구체화의 실제 원문과 평가를 보존한다. 87에서 보완한 [이전 적용 시안](../records/prototypes/personal-project-applied-2026-10-19/README.md)은 원형으로 남기고, 조건별 적용 설명·과정 근거·지위 구별을88의 새 프로토타입으로 이어간다.66·68·72의 형식·적용 의미 반영 선택과73의 전체 유보를 구별하고, 이번 보완 요청을 질문·사례·기준 본문 전체의 채택으로 올리지 않는다.

## 현재 선택과 남은 판단

| 구분 | 유지할 의미 |
| --- | --- |
| 계속 발전시킬 실물 | [development-workflow](../records/prototypes/development-workflow/README.md) 한 폴더에서 적용 모습을 고친다. 안쪽 noline-demo/context의 personal·project·work가 적용 실물이다. 실제 운영 Noline에 설치한 것은 아니다. 기존 날짜별 원형과 기록은 보존한다. |
| Personal context 방향 | 로컬 context 아래 personal을 둔다. 현재 적용 실물은 noline-demo/context/personal/development다.89는86을 별도 ai-workspace 호스트로 고정했던 해석을 정정한다. 실제 저장소 간 배포·동기화와 운영 설치는 남아 있다. |
| Project와의 관계 | Project는 자기 제품 의미·개발 계약·현재 현실을 충분히 설명한다. 개인 기준의 참조·채택·갱신 관리 책임을 Project 본문에 두지 않는다. 작업자가 필요한 개인 판단과 대상 Project 계약을 고르고 충돌을 판단하는 연결은 workflow에서 구체화한다. |
| 구조 이해의 정정 | 실제 Noline의 Project·Work와 Workspace의 memory·state·source·output·records 관계를 확인해 demo에 반영했다. Personal은 이번 추가 층이며 실제 Noline에 기존부터 있던 것으로 소급하지 않는다. |
| 본문 구분 | 일반 기준과 상세 사례는 이번 사용자 요청으로 별도 파일에 반영했다. 짧은 핵심 대비와 적용 조건은 일반 기준 가까이에, 구체 상황·당시 판단·한계·근거는 사례에 둔다. 제품 정책·코드 가이던스도 자기 책임을 독립적으로 설명한다. 전체 기준의 운영 구성은 미정이다. |
|01-02 입력 | [시안72](../records/2026-10-18-72-short-common-and-detail-prototype.md)의 짧은 공통·이름과 가독성 독립 절은 반영했다. [73](../records/2026-10-18-73-prototype-reservations-and-ticket03.md)의 전체 만족·최종 수용 유보와 미완료를 유지한다. 개인 기준 항목 전체 채택도 아니다. |
| 전체 개발 방향 | 검토자가 품질 수정까지 직접 수행하는 B는 선택했다. 최종 실제 검증까지 이어가는 세부 운영은 잠정안이다. 전체 관계와 열린 선택은 [Spec 3절·5절](spec.md)이 소유한다. |

개인 기준의 전체 항목·실제 설치·전달·갱신 방식과 workflow를 어떤 스킬에 연결할지는 남아 있다. source의 Noline 기준판·worktree 관찰판과 가상 시안의 지위를 구별하며 제품의 최신 코드나 실행 결과로 읽지 않는다.

## 다음에 이어갈 일

**최신 진행 정정:** [93](../records/2026-10-19-93-workflow-and-skills-discussion-focus.md)에서 사용자는 티켓 소속에 따라 논의를 지나치게 쪼개지 말라고 했다. 본문 충분성은 지금 다루고, 구체 개발 워크플로와 필요한 맥락을 찾아 읽는 방법은 기존 스킬과 함께 본다. 새 작업자가 입력을 받아 읽고 실행하는 문제도 이 흐름에 포함한다. 02의 Workspace 갱신을 먼저 완성할 필요는 없으며 뒤에 다룰 수 있다. 세부 역할·운영 조건을 결정한 것은 아니다.

다음 첫 작업으로 Main이 추천한 것은 **이름 유지·설명 보완·개명·동작 수정의 판단 부분**이다. [일반 기준](../records/prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion.md), [상세 사례](../records/prototypes/development-workflow/noline-demo/context/personal/development/cases/naming-and-completion.md), [Project 가이드](../records/prototypes/development-workflow/noline-demo/context/project/guidance/code-readability.md)의 현재 문장과 필요한 수정안을 나란히 보며 다듬는다. 이 추가 편집은 아직 수행하지 않았으며 특정 문장·규칙의 채택으로 읽지 않는다. 원문 사실·사용자 판단·새 설명의 지위는 사례와 작성 근거에서 구별한다. 그 뒤 DEVELOPMENT.md의 입력 선택·전달·검토·갱신을 기존 스킬·워크플로와 대조한다. 이 절차의 최종 위치·이름·운영 책임, 검토 겸임·생략과 재실험 입력 판본 보존은 미정이다. 이번에 선택한 사례 파일 분리를 이 운영 조건의 승인으로 확대하지 않는다.

[단일 프로토타입](../records/prototypes/development-workflow/README.md)에서 개인 기준이 대상 Project의 계약과 함께 선택되고 구현·검토·기록으로 이어지는 적용 모습을 검토한다. 보완이 생기면 이 폴더를 계속 고치고 판단 이유는 기록으로 남긴다. [87](../records/2026-10-19-87-conditional-application-and-provenance.md)에서 이어받은 조건별 적용, 원래 대화·사례로 돌아가는 경로, 새 질문·사례의 지위 표시가 이 적용 모습에서도 유지되는지 확인한다. 기준을 특정 코드 모양에 맞추라는 명령으로 읽지 않고 목적·사용처·비용에 따라 유지·수정을 판단하는지 본다. [7쌍 비교](../records/prototypes/criteria-format-comparison-2026-10-19/README.md)는 보완 전 상태로 유지한다.84의 독립 책임과89의 로컬 context 배치를 실제 운영 설치나 제품 효과로 올리지 않는다.

03에서는 분리된 본문만 읽어도 의미·조건·판단을 충분히 이해할 수 있는지 보고,04-03에서는 어떤 작업 단서로 찾아 적용하며 변화를 어디에 반영하는지 연결한다. 기존 원본 이동·합치기·설치는 하지 않는다. 항목 분류와 폴더 비교만 반복하거나 한 세트를03 전체의 완료로 올리지 않는다.

재진입은 Workspace README·current/index·Spec·output과 [마무리94](../records/2026-10-19-94-body-refinement-checkpoint.md)·[단일 프로토타입](../records/prototypes/development-workflow/README.md)에서 시작한다. 조건별 적용·과정 재접근의 보완은87과 보존된 날짜별 원형에서 확인한다. 최신 위치·구조 정정은89, 앞선 선택은86, 보완 전 원문 대조는7쌍 비교에서 확인한다. 책임·적용 장면은84의 수정 시안, 결정과 새 구체화의 구별은85, 그 이전 선택·가정은81~83에서 읽는다.01-02 입력은66·68·72·73과 해당 질문의 과정 근거를 선택한다. 글로벌 위치 추천, 별도 ai-workspace 호스트 의무, Project의 개인 기준 직접 관리 책임을 현행으로 이어받지 않는다.

[74](../records/2026-10-18-74-ticket-flow-after-quality-draft.md)·[75](../records/2026-10-18-75-ticket03-session-handoff.md)의 순서는 당시 진행 선택으로 보존한다. 현재는 [93](../records/2026-10-19-93-workflow-and-skills-discussion-focus.md)의 정정에 따라 본문을 지금 다듬고01-01의 구체 워크플로를04의 관련 스킬과 함께 보는 방향으로 잇는다. 02를 그 선행 단계로 고정하지 않으며 나머지 티켓 전체의 새 순서는 정하지 않았다. 티켓별 결과 책임은 유지하되 연결된 논의를 각각 닫고 이동하는 절차로 만들지 않는다.

## 이어갈 때 유지할 조건

- 전체 목표는 좋은 구현을 돕는 컨텍스트·기준·절차·검증·기록·경험 반영의 체계다. 코드 기준 문서 작성이나 판단 연속성만으로 좁히지 않는다.
- 사용자 기준은 목적·사용처·비용에 따른 판단이다. 짧으면 합치기, 모든 로직을 Hook에 넣기, 특정 라이브러리 의무 도입 같은 규칙으로 바꾸지 않는다. 개별 Confirm·Field·Container 선택과 조건은 [01-02](tickets/01-development-workflow/01-02-code-design-quality.md)와 연결 원기록에서 찾는다.
- 실제 문서·주변 역할과 필요한 상황을 보여 준 뒤 판단할 차이를 설명한다. 과거 회고에서 기억나지 않는다고 답한 내용을 확정 사실로 쓰거나 다시 답하도록 반복 요구하지 않는다.
- 일반 원칙·구체 사례·현재 제품 계약의 역할과 사용자 선호·후보·채택·관찰의 지위를 구별한다. 시안의 walkthrough를 모든 작업자의 필수 입력으로 만들지 않는다.
- 문서가 존재하고 링크가 연결된 사실, 실제 작업에서 발견·이해·적용된 사실, 제품 실행과 장기 효과를 구별한다.

## 기록과 Git 확인

사용자는 앞선 대화까지 서브에 넘겨 Workspace 기록을 정리하고 커밋하도록 요청했다. 정리 범위·검증은 [81의 기록 정리 절](../records/2026-10-19-81-personal-context-direction-and-next-step.md#2026-10-19-기록-정리와-확인)에 남겼다. 기존76~81의 비교·정정·선택과 current·Ticket·output 안내가 그 정리 범위였다. source·기존 prototype·reference-project·전역 파일·제품은 변경하지 않았다.

앞선 정리 시작 HEAD는 `83e2e06`이며 결과는 `bcb779c`에 커밋됐다. 이후 세 본문 작성은 [82](../records/2026-10-19-82-naming-responsibility-completion-draft.md), 실제 배치·적용 장면의 첫 구체화는 [83](../records/2026-10-19-83-personal-project-applied-example.md), 위치·책임·형식 정정은 [84](../records/2026-10-19-84-personal-project-ownership-and-format-correction.md), 글로벌 위치 추천은85, 당시 위치 선택·보완 전 본문 비교는86, 조건별 적용·과정 재접근 보완은87, 단일 적용 프로토타입의 첫 작성은88, 실제 Noline 대조와 로컬 context 구조 정정은89에서 구별한다. 이후82~89의 시안·비교·안내·prototype은 `deddf66`에 커밋했다. 90의 유보·다음 판단과 안내 정리는 `ab80d78`에 커밋했다. 이후91의 본문 개선,92의 합의 재대조·사례 분리,93의 진행 정정은 앞선 턴에서 미커밋으로 남겼다. 이번에는 사용자가 기록 정리와 커밋을 요청했다. [94](../records/2026-10-19-94-body-refinement-checkpoint.md)와 최신 안내를 더한 변경이 이번 중간 커밋 범위이며, 생성된 커밋과 작업 트리는 Git에서 확인한다. 실제 제품 코드·운영 기준을 바꾼 것은 아니다. 과거 인계·검사 결과는 해당 날짜의 [기록 색인](../records/README.md)에서 찾으며 현재 제품·설계 검증 결과로 재사용하지 않는다.
