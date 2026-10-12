# 04-01 — 작업 정의·재판단 스킬을 보완한다

상위 과제: [04 기존 스킬 보완](README.md)

상태: **분해 정리 완료 · 설계 작업 미착수**. 전체 기준은 [Spec](../../spec.md)에 있다.

## 맡은 결과와 범위

work-discussion과 reconsider-work의 **유지·구체화·관계 수정 후보와 실제 본문·동작 보완안**을 만든다. 구현 전 원하는 결과·보존할 경계·사람의 선택을 정리하는 책임과, 실제 결과·새 조건·누적 부담 때문에 가정과 후속 작업을 다시 보는 책임을 구별한다.

work-discussion은 현행 직접 호출 조건에서 출발하고 일반 작업 대화의 목표 이해와 관계를 살핀다. reconsider-work는 판단 변경이 기존 결과·의존 작업·Spec·Ticket에 미치는 영향까지 잇는다. 모든 대화에 인터뷰를 붙이거나 매 Ticket 종료를 자동 발동점으로 만들지 않는다.

## 처음 만들 결과와 근거

기록을 읽고도 작업 중심을 다시 잡은 장면과, 가독성 작업에서 동작 개선을 함께 선택한 장면을 사용해 현재 스킬의 요구·실제 대응·보완 대응을 비교한다. “왜 이렇게 했나”가 설명 요청인지 선택 재검토인지 달라지는 조건도 [04-02](04-02-artifact-explanation.md)과 대조한다.

- [Noline 스킬 기준판](../../../source/noline-baseline/.claude/skills/README.md), [Reference 스킬](../../../source/ai-workspace-baseline/reference-project/.agents/skills): 두 기준판의 실제 조항과 호출·기록 연결.
- [사용자 인터뷰](../../../source/noline-evaluation/reviews/interview-20261012.md): 작업 중심·질문 의도와 회고의 불확실성.
- [기록 시점·재개 비교](../../../source/reading/noline-evaluation/reviews/record-timing-followup.md), [철회·후속 구현 비교](../../../source/reading/noline-evaluation/reviews/withdrawal-followup-comparison.md): 원인 단정 없이 비교할 실제 사례.

## 다른 Ticket과 주고받을 것

[01-01](../01-development-workflow/01-01-development-flow.md)은 일반 개발 진행과 판단 책임을, 이 Ticket은 그 중 두 스킬의 조건·입력·행동·반환·기록 연결을 맡는다. [02](../02-work-records.md)의 기록 운영, [03](../03-project-context.md)의 맥락, [06](../06-framework-transition.md)의 Maintainer 제거 이후 인계와 맞춘다.

[04-02](04-02-artifact-explanation.md)·[04-03](04-03-context-skills.md)과 같은 현행 스킬 근거를 재사용한다. 한 스킬의 개선으로 다른 스킬의 책임을 중복하거나 비우는지 함께 확인한다.

## 완료 조건과 확인 방법

- 두 스킬의 실제 책임·호출 조건·입력·결과·기록 연결을 확인하고, 유지할 조항과 보완할 후보를 근거에 연결한다.
- 이미 있는 기준의 수행 부족, 기준의 구체성 부족, 맥락·코드·도구·책임 배치 문제를 구별하며 가를 수 없는 부분을 남긴다.
- 실제 장면에서 작업 정의와 재판단 전후의 대응, 바뀐 선택이 관련 결과에 미치는 영향을 보여 준다.
- 적용·생략할 경우와 과도한 질문·조사·기록이 생길 경우를 비교한다. 스킬 이름이나 설명 문구만 바꾼 안으로 끝내지 않는다.
- 본문·동작 보완안, 사용자 선택이 필요한 차이, 다른 Ticket의 영향과 후속 관찰을 제시한다. 기존 유지도 근거 있는 결과가 될 수 있다.

현재는 범위·근거·완료 조건을 분리한 상태다. 스킬 개편안의 비교·채택·구현·실제 효과 확인은 아직 수행하지 않았다.
