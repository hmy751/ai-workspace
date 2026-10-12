# 04-03 — 맥락 읽기·갱신·Workspace 생성 스킬을 보완한다

상위 과제: [04 기존 스킬 보완](README.md)

상태: **분해 정리 완료 · 설계 작업 미착수**. 전체 기준은 [Spec](../../spec.md)에 있다.

## 맡은 결과와 범위

read-project-context, update-project-context, create-context-workspace의 **유지·보완·연결 조정안과 실제 동작·본문 예시**를 만든다. 관련 본문을 선택해 작업에 적용하는 일, 여러 작업에 지속될 공통 맥락을 갱신하는 일, 새 독립·후속 Workspace를 만드는 일을 구별한다.

[02](../02-work-records.md)·[03](../03-project-context.md)이 내용과 관리 원칙을 소유하고, 이 Ticket은 그 원칙을 스킬의 적용 조건·입력·행동·결과·기록 인계로 잇는다. 읽기·갱신·새 Workspace 생성을 매번 한 묶음으로 수행한다고 정하지 않는다.

## 처음 만들 결과와 근거

같은 기존 작업을 재개할 때, 새 공통 사실을 반영할 때, 독립·후속 작업을 열 때의 사례를 비교한다. 무엇을 읽고 실제 판단에 어떻게 적용하는지, 무엇을 갱신하고 어디에 남기는지, 어떤 경우에는 새 Workspace가 필요하지 않은지 보여 준다.

- [Noline 스킬 기준판](../../../source/noline-baseline/.claude/skills/README.md), [Reference 스킬](../../../source/ai-workspace-baseline/reference-project/.agents/skills): 실제 책임·호출·공통 계약과 두 기준판의 차이.
- [Project 기준판](../../../source/noline-baseline/context/project/README.md): 실제 내용·읽기 경로·관리 계약.
- [Project 문서 개선 비교](../../../source/reading/noline-evaluation/reviews/document-guidance-followup.md): 기준 호출·실제 편집·사용자 평가를 구별할 사례.
- [기록·재개 비교](../../../source/reading/noline-evaluation/reviews/record-timing-followup.md): 보존·열람과 적용이 다를 수 있다는 근거.

## 다른 Ticket과 주고받을 것

[01-01](../01-development-workflow/01-01-development-flow.md)·[01-02](../01-development-workflow/01-02-code-design-quality.md)·[01-03](../01-development-workflow/01-03-behavior-verification.md)가 실제 소비할 맥락을 03과 함께 검토한다. 작업 중심과 선택이 바뀔 때는 [04-01](04-01-work-decision-skills.md), 자동 Maintainer의 기록 인계 문구와 제거 후 연결은 [06](../06-framework-transition.md)과 맞춘다.

Project·Work 정본의 내용과 관리 책임을 스킬 안에 복제하지 않는다. 근거 사본과 현행 대상의 차이를 확인하며, 호출 설정·bridge의 존재를 실제 발견·호출·문서 반영·재진입 성공과 혼동하지 않는다.

## 완료 조건과 확인 방법

- 세 스킬의 현행 조항·조건·입력·산출물·기록 연결과 Noline/Reference의 필요한 차이를 확인한다.
- 재개·본문 선택과 적용·공통 맥락 갱신·Workspace 생성의 대표 사례에서 현재 대응과 보완 대응을 비교한다.
- 관련 문서를 찾는 것에서 끝나지 않고 계약·예외·현재 차이가 실제 작업에 어떻게 쓰이는지 보여 준다.
- 적용하지 않을 경우, 중복 읽기·기록·책임을 만들 수 있는 경우와 그 비용을 확인한다.
- 보완안이 02·03의 정본 책임 및 06의 전환안과 연결된다. 남은 사용자 선택과 실제 host 적용 뒤 확인할 경로를 남긴다.

현재는 과제 분할만 수행했다. 스킬·Project 본문·설정의 실제 개편이나 설치·호출·사용 효과 확인은 아직 하지 않았다.
