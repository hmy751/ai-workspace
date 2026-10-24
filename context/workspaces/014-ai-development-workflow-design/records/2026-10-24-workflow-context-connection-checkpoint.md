# 개발 워크플로의 완료 경계와04-03 context 연결 재개

2026-10-24. 다음 세션은 **04-03에서 개발 워크플로가 실제 context를 읽고 적용하고 갱신하며 재개하는 경로**를 구체화한다. 기존 세 스킬도 함께 대조하지만 스킬 문구 정비만으로 과제를 축소하지 않는다.01-01·01-03의 역할·진행·인계 설계와 prototype 본문 반영은 완료다. 실제 context와의 구체 연결, 운영 설치와 전체 수행 효과까지 완료한 것은 아니다.

## 사용자 질문과 설명을 바로잡은 지점

이번 대화의 직접 사용자 발화는 다음 순서다.

> 04-03은 무슨 말이지?

> 그래 좋아 그럼 워크플로나 이런건 다 된거네? 검증은 나 중에 한다 치고

> 04-03은 스킬도 스킬이지만 어쨋든 구체적으로 이게 context과 어떻게 연결되는가도 맞을까?

> 그럼 워크스페이스 기록 잘 확인하고 다른 세션이 흐름 잘 이어갈 정도로 정리해놓자

Main은 처음04-03을 세 기존 스킬 정비로 설명하고 개발 워크플로가 완료됐다고 답했다. 사용자 질문 뒤 **역할·진행·인계 설계는 완료, 실제 context 구조와 구체 연결은04-03에서 계속 완성**한다고 설명을 바로잡았다. 기존04-03에도 실제 읽기·적용·갱신·재개 관계가 있었으므로 새로운 역할이나 Ticket을 추가한 것이 아니다. 이번에는 이 설명을 current·Spec·Ticket·진입점에 일치시킨다.

사용자의 “검증은 나중”은 이 대화에서 전체 개발 흐름의 실제 수행·효과 확인을 후속으로 두는 맥락이다. 검증자 설계를 미정으로 되돌리거나 이후 실제 개발에서 필요한 검증을 생략한다는 결정으로 확대하지 않는다.

## 완료한 결과와 계속할 범위

[01-01·01-03 마감 근거](2026-10-24-ticket01-01-03-closeout-and-next-scope.md)의 기존 완료 조건 대조와 마감을 유지한다. 구현·개선 검토·수정·별도 검증·재검증·Main 완료 판단·첫 보고·기록의 책임은 실제 prototype에 반영됐다. 새 담당자는 같은 역할 논의를 처음부터 재개하지 않는다.

04-03에서는 그 책임이 실제 context의 어떤 내용·진입점·관리 지침에 연결되는지 확인하고 필요한 보완안을 만든다. 일반 재개와 한정된 역할 인수, 요약 전달과 원문 직접 읽기, 자료 열람과 실제 적용, 현재 작업 기록과 지속 정본 갱신을 구별한다. 필요한 자료를 전부 인계하거나 읽게 하는 고정 목록으로 바꾸지 않는다.

03은 context 구성·내용 정본을,02는 Work의 기록·재개 운영을 소유한다.04-03에서 필요한 부분을 함께 대조하며 각각 전체 완료를 선행 조건으로 삼지 않는다. 세 스킬은 수단이므로 유지·보완·통합·비적용을 비교한다. 자동 Maintain은 미연결이며 Main의 지침 기반 기록 책임, Work의 새 background 적용 보류는 유지한다. 실제 대상 설치·장치 의존은06, 전체 연결·적용·관찰 계획은07과 잇는다.

## 재개할 때 읽을 실물과 근거

일반 재개는 Workspace README·current/index·memory·state·output을 먼저 읽는다. 그 뒤04-03 질문에 필요한 자료를 아래에서 선택한다. 이 자료 전체를 모든 역할에 기본 입력으로 넘기라는 목록이 아니다.

| 확인할 관계 | 현재 입력 |
| --- | --- |
| 다음 범위와 완료 조건 | [04-03](../current/tickets/04-skill-improvements/04-03-context-skills.md), [Spec](../current/spec.md), 위 마감 근거 |
| 역할별 읽기·적용·인계·갱신 책임 | [development 본체](prototypes/development-workflow/skills/development/SKILL.md), 필요한 [review](prototypes/development-workflow/skills/development/references/review.md)·[verification](prototypes/development-workflow/skills/development/references/verification.md)·[execution](prototypes/development-workflow/skills/development/references/execution.md) |
| 실제 내용·진입·관리 구조 | [현재 prototype](prototypes/development-workflow/README.md), [demo context 진입](prototypes/development-workflow/noline-demo/context/README.md), 그 아래 Personal·Project·Work, [CONTENT-POLICY](prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)·[SYSTEM-GUIDANCE](prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md) |
| 기존 스킬의 실제 조항과 대상 차이 | [Noline 기준판](../source/noline-baseline/.claude/skills/README.md)과 [Reference 기준판](../source/ai-workspace-baseline/reference-project/.agents/skills)의 read-project-context·update-project-context·create-context-workspace/SKILL.md. 원본 snapshot은 읽기 전용이며 현재 채택 prototype과 구별 |
| 관계를 판단한 맥락·레퍼런스 | [동적 맥락 선택 의도](2026-10-21-dynamic-context-and-review-intent.md), [자료별 참고점과 기존 스킬 연결](2026-10-21-implementation-review-reference-comparison.md), [단계·층위·개념과 책임의 공통 메모](2026-10-24-workflow-structure-and-responsibility-guidance.md). 필요할 때 연결된 원자료를 직접 확인 |

## 다음 세션의 첫 산출물

첫 결과는 스킬별 문구 수정 목록보다 **대표 작업 장면에서의 실제 context 연결안**이다. 기존 작업 재개·역할 인수/추가 탐색·지속할 공통 사실 갱신·완료 후 재개/독립 작업 생성에서 다음 관계를 보여 준다.

- 현재 누가 어떤 질문으로 어디에 들어가 어떤 본문을 읽고 실제 판단에 적용하는가.
- 작업 중 바뀐 사실·결정·근거가 어느 Owner의 정본 또는 이번 기록으로 돌아가고 다음 재개에서 어떻게 발견되는가.
- 현재 경로의 실제 공백·중복·충돌이 무엇이며, 기존 스킬·진입 지침·본문 중 어디를 유지하거나 보완하면 되는가.
- 추가 읽기·기록·역할 왕복의 비용, 적용하지 않을 조건, 남은 사용자 선택과 후속 실제 확인은 무엇인가.

기존 합의·현재 실물·목표·원자료에 대조해 제안하고 사용자가 판단할 부분을 설명한다. 이 기록 자체는 구체 연결안의 완성이나 새 스킬 채택이 아니다. prototype의 계약을 실제 Noline 또는 운영 환경 설치 완료로 확대하지 않는다.

## 이번 정리와 별도 진행

이번에는 현재 안내·책임 범위·재개 경로를 정리했다. 구체 연결안 작성, 스킬 실행 본문 수정, 새 독립 리뷰나 제품 실행·역할 전체 수행 시험은 하지 않았다. 현재 기록과 정본 경로를 Main이 직접 대조한 것이며 새 독자의 독립 인수 성공을 주장하지 않는다.

04-02 설명 스킬은 별도 세션에서 진행 중이다. 그 세션의 미커밋 변경이 있으므로 실제 Git 상태와 해당 Ticket을 확인하며, 이번04-03 재개 기록으로 덮거나 함께 완료 처리하지 않는다.01-02·02·05·06·07의 남은 책임은 기존 마감 기록과 각 Ticket을 따른다.

확인: 변경 문서11개의 로컬 링크696개가 실제 경로에 연결됨을 확인하고 `git diff --check`를 통과했다. Main이 README·current에서04-03·현재 실물·원형 자료·첫 산출물로 내려가는 재개 경로를 읽고, 완료 범위와 다음 행동을 찾을 수 있는지 대조했다. 별도 세션의04-02 작업 변경은 보존하며 이번 변경분만 커밋한다.
