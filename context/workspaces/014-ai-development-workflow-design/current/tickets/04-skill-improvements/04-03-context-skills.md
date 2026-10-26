# 04-03 — 맥락 읽기·갱신·Workspace 생성 스킬을 보완한다

2026-10-26 **제안·검토 후 반영 방향의 구체화:** [2번](../../../records/2026-10-26-context-02-role-execution-proposal.md)의 기존 결과 반환에 반영 제안·근거를 연결하고, [3번](../../../records/2026-10-26-context-03-change-records-proposal.md)에서 Main의 검토·실제 반영·중요한 제안의 보존과 재사용을 구체화했다. [앞선 대화 대조·이번 근거와 리뷰](../../../records/2026-10-26-context-proposal-review-apply-design.md)와 [통합안](../../../records/2026-10-26-context-integrated-proposal.md)으로 이어 본다. 구현자 직접 수정 기본값은 대체한 후보이며 이번에는 설계·기록·재진입만 맞췄다. 1번 한정 실행 반영은 유지하고 USAGE/context-update 사용감·정확한 형태·설치·수행 효과와04-03 전체 완료는 아직이다.

## 지금 이어갈 지점 — 워크플로와 실제 context의 통합 연결

**다음은3번의 실제 반영 범위·종료 조건이다.** [이번2번 논의·리뷰·구체화](../../../records/2026-10-26-context-proposal-review-apply-design.md)를 입력으로 [3번 초안](../../../records/2026-10-26-context-03-change-records-proposal.md)을 순차 검토한다. 담당자의 제안과 Main 검토 관계를 다시 시작하지 않고, 채택된 의미의 본문·관련 경로 반영과 완료, Main의 Work·진행 중 담당자·이전 근거 연결, 개발 중·직접 요청·루프 입력의 같은 수행을 구체적으로 본다. 이후4번의 남은 완료·연속 세부와 전체 흐름을 확인한다. 기록·커밋 요청을 실제 스킬 생성 승인으로 확대하지 않는다.

역할·진행·인계 설계,03의 실제 context·관리 계약, 기존 스킬과 Work/Harness, 잠정 틀과 외부 고정판을 종합한 [통합안](../../../records/2026-10-26-context-integrated-proposal.md)을 사용자와 검토한다. 기존 합의 복원만으로 끝내지 않고 네 항목에서 무엇을 유지·보완·공통화할지와 실제 흐름을 설명한다. 일반 읽기에 목표 정의·전체 완료를 흡수하지 않고, 형성 자료의 이해 목적과 제안·검토·반영의 현재 책임을 유지한다. 관련 선택이 바뀌면 다른 항목의 의존도 함께 맞춘다. 아래 원래 입력과 완료 조건은 유지한다.

- 시작·재개와 수행 중 추가 탐색: Main과 담당자가 무엇을 읽고 어떻게 실제 판단에 적용하는가. 담당자 원문 직접 읽기와 질문별 선택은 이미 합의된 입력이다.
- 작업 중 변화와 연속성: 현재 Work의 선택·판단·상태, 지속할 Personal·Project 본문을 각각 누가 어떤 기준으로 유지하는가.
- 경험 개선과 작업 생성: 현재 사실을 맞추는 것과 앞으로의 방식을 재판단하는 것, 기존 Work 재개와 새 독립 목표의 인수를 구별한다.
- 실행 수단의 구성: 기존 스킬 재구성, 공통 진입, 수행 흐름 흡수와 독립 과업별 스킬을 같은 장면에 대입해 비교한다. 독립 스킬이 별도 agent·전체 재독·보고서를 요구한다고 가정하지 않는다.

03의 context 정본과 관리 기준,02의 기록 운영,05의 경험 개선,06의 실제 배치·전환,07의 전체 연결을 함께 보되 각 Ticket을 스킬 단계로 바꾸지 않는다. 기존 스킬의 독립 존속·새 스킬 신설·정확한 이름과 개수는 아직 채택하지 않았다. 아래 날짜별 기록은 형성 경과다.

## 04-02 마감에서 이어받는 연결

2026-10-26 [04-02 설계 마감](../../../records/2026-10-26-ticket04-02-closeout-and-followups.md)의 explain·development 책임을 현재 입력으로 사용한다.04-03은 실제 자료 선택·원문 읽기·맥락 적용과 Owner별 갱신 경로를 잇되 설명 방법이나 조사·검증의 전체 책임을 새 맥락 스킬로 흡수하지 않는다. 실제 읽기·갱신 연결에서 현재 실행 지침과 충돌이 발견되면 해당04-02 본문에 반환한다. 이 인계는04-03의 추가 세부안 채택·실행 반영·설치 승인이 아니며 기존 진행 상태를 유지한다.

## 기존 진행과 입력

2026-10-24 다음 범위: [01-01·01-03의 설계 마감](../../../records/2026-10-24-ticket01-01-03-closeout-and-next-scope.md)과 실제 development·review·verification·execution을 입력으로 받는다. 새 역할을 다시 설계하는 대신 read/update/create의 현행 조항·Noline/Reference 차이와 재개/본문 선택·적용/공통 갱신/Workspace 생성 장면을 대조해 유지·보완·비적용 조건을 만든다. 연결 안내와 Main 직접 수행만으로 개별 스킬 보완을 완료 처리하지 않는다. 이번에는 후속 범위만 갱신했고 스킬 보완·설치는 착수하지 않았다.

**14~15번의 연결·기록 책임을 prototype 실행 본문에 반영했다.** [대조와 범위](../../../records/2026-10-23-development-workflow-1-15-integration.md)를 읽는다. root/Work의 일반 재개·한정 위임, development의 조건별 맥락 선택·재판단·갱신, work-discussion의 명시 호출과 Main 기록 책임을 맞췄다. 설치된 호환 스킬이 없으면 Main이 실제 관리 지침으로 수행한다. 보존 원형 read/update/reconsider/create 스킬 자체의 대상별 보완·설치와 실제 효과는 남아 있어 이 Ticket 전체 완료는 아니다. 자동 Maintain·신규 기록 스킬은 연결하지 않는다. 아래 날짜별 미적용·미정 표기는 당시 경과다.

2026-10-23 6번 연결: [통합된 구현 완성·인계안](../../../records/2026-10-23-implementation-completion-and-handoff-proposal.md)에서 관련 자료·지침의 선택·이해·적용과 필요한 재탐색을 구현자의 수행 책임으로 명시했다. 내용 정본은 Personal·Project·Work가 유지하고, 인계는 판단을 가른 자료·적용 이유를 연결한다. 실제 읽기·갱신 스킬 본문이나 호출 설정은 변경하지 않았으며7번 초기 입력·8번 동적 탐색과 함께 후속 구체화한다.

2026-10-23 prototype 적용: [development SKILL.md](../../../records/prototypes/development-workflow/skills/development/SKILL.md)와 검토 상세에 확정1~5번·구성 개선 리뷰를 반영하고 DEVELOPMENT 진입을 이전했다. [적용 기록](../../../records/2026-10-23-development-skill-prototype-adoption.md)을 따른다. Personal·Project·Work의 내용 Owner와 일반 수행의 Owner를 구별하며 상세 인계·호출·수정·종료·모델·기존 맥락 스킬 연결은 후속이다. 다음은6번 구현 완성·인계다. 아래 날짜별 미적용·위치 미정은 당시 상태이며 Ticket 전체·운영 설치는 아직 완료가 아니다.

2026-10-22 연결 방향: [관련 기준 공유·별도 판단의 선택](../../../records/2026-10-22-shared-criteria-and-independent-review-decision.md)에 맞춰 Main 초기 선택과 서브의 질문별 추가 탐색을 구체화한다. 검토자에게 Personal을 기본적으로 숨기는 안 대신 관련 기준을 공유하는 방향이며, 정확한 본문·사례·형성 자료의 읽기 범위는 미정이다. 기존 Project 읽기의 질문별 선택을 살리고 일반 재진입과 한정 검토 위임·실제 대화/지침 상속·갱신 Owner를 대조한다. 이번에는 논의만 기록했고 스킬·DEVELOPMENT·설정은 변경하지 않았다.

상위 과제: [04 기존 스킬 보완](README.md)

2026-10-21 사용자 후속 구상: [동적 맥락 선택과 검토 입력](../../../records/2026-10-21-dynamic-context-and-review-intent.md)에 따라 초기 전달에 더해 구현 결과·요구·새 질문을 보고 필요한 정본을 다시 선택하는 방식을 비교한다. Personal 기반 구현과 별도 관점 검토에 서로 어떤 원칙·사례·Project 계약을 줄지, 담당자의 추가 탐색과 Main 판단을 어떻게 연결할지 구체화한다. Vercel의 작업별 선택과 우리 반복 절차 제안을 구별하며, 정확한 읽기 범위·수정·검증 배치는 미정이다.

2026-10-21 비교 제안: [자료별 참고점과 기존 스킬 연결](../../../records/2026-10-21-implementation-review-reference-comparison.md)에 구현·검토 중 필요한 본문 선택, 실제 작업 적용, 지속할 의미가 바뀔 때의 갱신을 연결했다. Main이 고른 자료에서 시작하되 실행 담당자도 새 판단에 필요한 원문을 추가로 찾는 안을 권고했다. Personal·Project의 내용 책임과 기존 읽기·갱신·새 Workspace 생성의 조건을 유지하며, 실행 skill의 구성·DEVELOPMENT의 최종 위치는 후속 판단이다. 실제 본문 보완이나 설치는 수행하지 않았다.

2026-10-21 자료 수집:01-01과 함께 **구현 / 검토 및 수정**을 큰 논의 단위로 보고, 기존 강연뿐 아니라 [Matt·pstack 로컬 원문과 연결 자료](../../../source/workflow-references/README.md)를 확보했다. Vercel은 기존 article의 실제 모드·읽기 조건·확인 절을 연결한다. [수집 기록](../../../records/2026-10-21-workflow-reference-source-collection.md)에 원문·참조·판본과 남은 범위를 구별했다. 이후 실제 행동과 필요한 맥락을 대조하며, 이번 수집을 기존 스킬 보완·설치 완료로 처리하지 않는다.

2026-10-20 후속 입력: [03](../03-project-context.md)의 본문·사례·형성 자료와 읽기·갱신 책임 구체화를 완료 결과로 이어받는다. 현재 CONTENT-POLICY와 SYSTEM-GUIDANCE의 구별, 일반 적용과 의미 수정 시 선택적으로 읽는 자료를 실제 기존 스킬의 조건·입력·행동과 대조한다.01-01과 DEVELOPMENT의 최종 위치·Owner를 판단하며 Work의 새 background 적용은 보류한다. [마감119](../../../records/2026-10-20-119-ticket03-closeout.md)는 결과 연결이며 스킬 수정·설치·호출 효과의 완료가 아니다.

2026-10-19 당시 후속 입력: [103](../../../records/2026-10-19-103-prototype-session-checkpoint.md)에서 사용자는 Development의 최종 위치·역할과 스킬 관계를 워크플로 관련 작업 때 더 구체화하기로 했다.01-01과 함께 스킬 본문 통합 또는 별도 절차 문서 연결을 비교하되 현재 안을 확정하지 않는다. [102](../../../records/2026-10-19-102-personal-project-update-ownership.md)의 Personal·Work·Project별 갱신 기본값과 필요한 설명 중복 허용을 실제 스킬 행동에 연결한다. 이번 세션은 기록·커밋이며 스킬 수정·설치는 하지 않는다.

상태: **Project 읽기·갱신 스킬 첫 대조와 workflow 시안 수정 완료 · 실제 스킬 보완은 미완료**.76에서 기존 read/update 스킬과 읽기·관리 기준을 비교했고82·83에 본문·적용 장면을 만들었다. 앞선 [책임 정정84](../../../records/2026-10-19-84-personal-project-ownership-and-format-correction.md)는 Project가 개인 문서를 관리하는 직접 연결을 대체한다. 현재는 [88](../../../records/2026-10-19-88-living-applied-prototype.md)의 [단일 프로토타입 workflow](../../../records/prototypes/development-workflow/skills/development/SKILL.md)에서 입력 선택·충돌 판단·구현/검토 인계·결과별 갱신을 구체화하며 실제 스킬 수정·호출 효과·Workspace 생성 대조는 미완료다. 전체 기준은 [Spec](../../spec.md)에 있다.

[중간 정리90](../../../records/2026-10-19-90-prototype-checkpoint-and-open-design.md): 사용자는 DEVELOPMENT.md의 현재 위치를 미완성의 예로 짚었다. 이 파일이 Work의 확정 운영 계약이라는 전제 없이 위치·이름·소유 책임, 기존 read/update/작업 스킬과의 행동 분담을 구체화한다. 이번 커밋·정리는 대체 위치 선택이나 실제 skill 설치가 아니다.

[정정89](../../../records/2026-10-19-89-local-context-structure-correction.md)은 개인 기준을 별도 ai-workspace 호스트로 분리한 해석을 대체한다. 현재 demo는 같은 context 안의 personal·project를 Work의 DEVELOPMENT.md에서 선택하고, 필요한 본문과 이유를 Work memory에 남긴다. 기존 read-project-context의 제품 본문 선택 책임과 개인 기준의 선택을 구별한다. 실제 운영 skill·자동 호출·동기화 방식은 후속 설계이며 이번에는 설치하지 않았다.

[합의 대조와 반영92](../../../records/2026-10-19-92-principles-cases-and-agreement-reconciliation.md): 일반 기준에서 필요한 상세 사례로 내려가는 읽기 경로를 절차 시안에 연결했다. B의 검토자 직접 수정 방향을 유지하고 검토 겸임·생략 조건은 미정으로 남겼다. DEVELOPMENT의 최종 위치·책임과 실제 스킬 연결·설치는 아직 결정하거나 수행하지 않았다.

## 맡은 결과와 범위

Personal의 일반 판단과 Project의 제품·개발 계약은 각각 독립 본문이 소유한다. [현재 workflow](../../../records/prototypes/development-workflow/skills/development/SKILL.md)는 Main이 작업 단서로 필요한 개인 주제와 대상 Project 본문을 고르고, 충돌·열린 선택을 판단하며, 구현자·검토자에게 필요한 입력을 전달하고 결과를 각 책임에 돌려보내는 모습을 다룬다. 이 연결을 Project README의 개인 문서 안내·채택·갱신 관리로 대신하지 않는다. 개인 기준은89에 따라 demo context/personal에서 찾는다. 현재 경로와 수동 절차는 구성했으며 기존 스킬 반영과 실제 자율 발견 효과는 남아 있다. 새 스킬을 설치한 것은 아니다.

2026-10-18 현재 시안 연결: [반영72](../../../records/2026-10-18-72-short-common-and-detail-prototype.md)는 사용자가 선택한 짧은 공통·이름과 가독성의 독립 절을 실제 문서와 읽기 안내에 연결한다. [주문 장면](../../../records/prototypes/applied-criteria-2026-10-17/order-walkthrough.md)에서 같은 작업 경로와 develop 역할을 받은 뒤 Project 안내·현재 계약·필요한 상세·조건별 사례로 내려가는 문구를 대조한다. 당시 시안은 Project 한곳의 읽기 안내를 역할 절차가 참조했다. Personal까지 포함한 현재 연결 책임은84에서 다시 나누며,72의 배치를 독립 기준 연결의 확정 구조로 확대하지 않는다. 가상 develop를 기존 스킬의 대조·실제 발견·적용 효과 확인으로 대신하지 않는다.

03과 함께 [후속 재판단 장면](../../../records/prototypes/applied-criteria-2026-10-17/refinement-walkthrough.md)의 공통 충분성·이름 절의 독립성·상세 분량과 배치·사례 배치·제품 값과 Work 요구·읽기와 갱신 책임을 실제 기존 스킬·Project에 대입한다. 본문을 찾는 조건과 실제 판단·갱신에 쓰는 행동을 비교하고, 구성이 달라지면03의 읽기 안내와01-02의 설명도 함께 맞춘다. 선택된 형식 방향을 다시 묻거나 같은 시안만 반복하기보다 필요한 근거와 새 조건으로 다음 판단을 진행한다.

read-project-context, update-project-context, create-context-workspace를 포함한 기존 수단과 새 workflow를 대조해 **유지·재구성·통합·흡수·필요한 신설의 비교안과 실제 동작·본문 예시**를 만든다. 관련 본문을 선택해 작업에 적용하는 일, 지속할 맥락을 관리하는 일, 경험으로 방식을 개선하는 일, 새 독립·후속 Workspace를 만드는 일의 관계를 구별한다. 기존 이름·개수나 새 스킬 신설을 완료 조건으로 삼지 않는다.

[02](../02-work-records.md)·[03](../03-project-context.md)이 내용과 관리 원칙을 소유하고, 이 Ticket은 그 원칙을 스킬의 적용 조건·입력·행동·결과·기록 인계로 잇는다. 읽기·갱신·새 Workspace 생성을 매번 한 묶음으로 수행한다고 정하지 않는다.

## 처음 만들 결과와 근거

같은 기존 작업을 재개할 때, 새 공통 사실을 반영할 때, 독립·후속 작업을 열 때의 사례를 비교한다. 무엇을 읽고 실제 판단에 어떻게 적용하는지, 무엇을 갱신하고 어디에 남기는지, 어떤 경우에는 새 Workspace가 필요하지 않은지 보여 준다.

- [Noline 스킬 기준판](../../../source/noline-baseline/.claude/skills/README.md), [Reference 스킬](../../../source/ai-workspace-baseline/reference-project/.agents/skills): 실제 책임·호출·공통 계약과 두 기준판의 차이.
- [Project 기준판](../../../source/noline-baseline/context/project/README.md): 실제 내용·읽기 경로·관리 계약.
- [Project 문서 개선 비교](../../../source/reading/noline-evaluation/reviews/document-guidance-followup.md): 기준 호출·실제 편집·사용자 평가를 구별할 사례.
- [기록·재개 비교](../../../source/reading/noline-evaluation/reviews/record-timing-followup.md): 보존·열람과 적용이 다를 수 있다는 근거.

## 다른 Ticket과 주고받을 것

읽기·갱신 행동을 구체화할 때 [01-02의 과정과 후속 재검토 65](../../../records/2026-10-18-65-criteria-status-and-cross-ticket-refinement.md)를 진입점으로 삼는다. Main이 기준을 골라 준 가상 전달 장면만으로 실제 스킬의 발견·적용을 보장하지 않고, 필요한 자료를 고르는 조건과 일반 기준·사례·현재 계약의 지위를 함께 판단한다. 기존 스킬·도구·비용에 비춰 다른 전달량이나 배치가 필요하면 01-02 기준의 설명·읽기 안내와 03의 구성을 함께 재검토한다.

[01-01](../01-development-workflow/01-01-development-flow.md)·[01-02](../01-development-workflow/01-02-code-design-quality.md)·[01-03](../01-development-workflow/01-03-behavior-verification.md)가 실제 소비할 맥락을 03과 함께 검토한다. 작업 중심과 선택이 바뀔 때는 [04-01](04-01-work-decision-skills.md), 자동 Maintainer의 기록 인계 문구와 제거 후 연결은 [06](../06-framework-transition.md)과 맞춘다.

Project·Work 정본의 내용과 관리 책임을 스킬 안에 복제하지 않는다. 근거 사본과 현행 대상의 차이를 확인하며, 호출 설정·bridge의 존재를 실제 발견·호출·문서 반영·재진입 성공과 혼동하지 않는다.

## 완료 조건과 확인 방법

- 세 스킬의 현행 조항·조건·입력·산출물·기록 연결과 Noline/Reference의 필요한 차이를 확인한다.
- 재개·본문 선택과 적용·공통 맥락 갱신·Workspace 생성의 대표 사례에서 현재 대응과 보완 대응을 비교한다.
- 관련 문서를 찾는 것에서 끝나지 않고 계약·예외·현재 차이가 실제 작업에 어떻게 쓰이는지 보여 준다.
- 적용하지 않을 경우, 중복 읽기·기록·책임을 만들 수 있는 경우와 그 비용을 확인한다.
- 보완안이 02·03의 정본 책임 및 06의 전환안과 연결된다. 남은 사용자 선택과 실제 host 적용 뒤 확인할 경로를 남긴다.

현재는 [네 항목 재종합안](../../../records/2026-10-26-context-integrated-proposal.md)에 전체 대조를 반영해 사용자와 흐름·추가 조건을 검토할 상태다. [이번 반영 근거](../../../records/2026-10-26-context-whole-scope-reconciliation.md)는 초기 개선 리뷰와 구별한다. 기존 스킬 대조·대표 장면·입력/반환·비적용/비용·후속 책임을 설계안에 연결했다. 위 1번 한정 반영 외 세부 채택·실행 연결·호출 효과·운영 설치·Ticket 완료는 별도다.02·05·06·07의 전체 과제를 이 결과만으로 완료 처리하지 않는다.
