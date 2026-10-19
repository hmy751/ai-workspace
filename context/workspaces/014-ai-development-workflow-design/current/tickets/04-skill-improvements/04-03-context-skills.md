# 04-03 — 맥락 읽기·갱신·Workspace 생성 스킬을 보완한다

상위 과제: [04 기존 스킬 보완](README.md)

상태: **Project 읽기·갱신 스킬 첫 대조 완료 · 보완 설계와 Workspace 생성 대조는 미완료**.03 시작 요청에 따라 [76](../../../records/2026-10-18-76-ticket03-first-comparison-and-discussion.md)에서 Noline·Reference의 read/update 스킬과 읽기·관리 기준을 비교했다. 기존 선택적 읽기·공통 맥락 갱신 책임을 확인했으며, 본문과 연결한 실제 동작 예시·호출 효과·스킬 수정은 아직 없다. 전체 기준은 [Spec](../../spec.md)에 있다.

## 맡은 결과와 범위

[81의 Personal context 방향](../../../records/2026-10-19-81-personal-context-direction-and-next-step.md)에 따라03의 다음 본문 구성에서는 개인 기준과 Project의 실제 의미·계약을 어떻게 찾아 함께 적용하고, 바뀐 의미를 어느 정본에 반영할지 연결한다. 개인 기준 중앙 정본과 Project의 채택 관계는 방향을 정했지만 실제 접근·전달·갱신 방식은 미정이다. 이 연결을 위해 전체 개인 기준을 매번 읽히거나 현행 스킬을 이미 고친 것으로 전제하지 않는다.

2026-10-18 현재 시안 연결: [반영72](../../../records/2026-10-18-72-short-common-and-detail-prototype.md)는 사용자가 선택한 짧은 공통·이름과 가독성의 독립 절을 실제 문서와 읽기 안내에 연결한다. [주문 장면](../../../records/prototypes/applied-criteria-2026-10-17/order-walkthrough.md)에서 같은 작업 경로와 develop 역할을 받은 뒤 Project 안내·현재 계약·필요한 상세·조건별 사례로 내려가는 문구를 대조한다. 읽기 안내는 Project 한곳이 소유하며 역할 절차는 그곳을 참조한다. 가상 develop를 기존 스킬의 대조·실제 발견·적용 효과 확인으로 대신하지 않는다.

03과 함께 [후속 재판단 장면](../../../records/prototypes/applied-criteria-2026-10-17/refinement-walkthrough.md)의 공통 충분성·이름 절의 독립성·상세 분량과 배치·사례 배치·제품 값과 Work 요구·읽기와 갱신 책임을 실제 기존 스킬·Project에 대입한다. 본문을 찾는 조건과 실제 판단·갱신에 쓰는 행동을 비교하고, 구성이 달라지면03의 읽기 안내와01-02의 설명도 함께 맞춘다. 선택된 형식 방향을 다시 묻거나 같은 시안만 반복하기보다 필요한 근거와 새 조건으로 다음 판단을 진행한다.

read-project-context, update-project-context, create-context-workspace의 **유지·보완·연결 조정안과 실제 동작·본문 예시**를 만든다. 관련 본문을 선택해 작업에 적용하는 일, 여러 작업에 지속될 공통 맥락을 갱신하는 일, 새 독립·후속 Workspace를 만드는 일을 구별한다.

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

현재는 과제 분할과 가상 시안의 접점 연결에 이어76에서 기존 read/update 스킬과 읽기·관리 계약의 첫 대조를 수행했다. Workspace 생성 스킬의 상세 대조, 실제 본문에 대입한 보완안과 호출 효과는 남아 있다. 기존 스킬·Project 본문·설정의 개편이나 설치는 하지 않았다.
