# 01-01 — 개발 진행과 사람의 판단을 연결한다

2026-10-26 구조 후속: 기존 설계 결과를 유지하며 [실행 상세의 계층 확장](../../../records/2026-10-26-development-detail-expansion.md)을 적용한다. 구현 수행은 독립 상세로, 검사 근거 판단·재사용은 검증 본문 아래 공유해서 사용하는 상세로 나눈다. 새 역할·선행 단계·권한·완료 조건을 추가하는 과제가 아니다.

상태: **설계 결과 완료 — 개발 진행·사람 판단의 합의·실행 prototype 반영·대표 대조를 완료했다.** [완료 조건별 근거와 마감](../../../records/2026-10-24-ticket01-01-03-closeout-and-next-scope.md#01-01-완료-조건별-대조)에서 기존 다섯 조건을 실제 결과에 대조했다. Main의 이번 마감 판단이며 실제 운영 설치·여러 역할의 전체 개발 수행·일반 효과의 입증과 구별한다.

## 맡은 결과와 범위

목표·Spec·Ticket에서 조사·설계·구현·개선 검토·수정·검증·첫 보고까지 이어지는 대표 작업의 진행안과 판단 책임의 선택 근거를 만든다. 사용자가 정정한 큰 틀은 구현 단계 안의 구현자·개선 검토자·Main, 이후 별도 검증자와 Main·수정 담당이 잇는 검증 및 수정 단계다. Main은 현재 대화의 전체 담당자이며 별도 lead를 추가하지 않는다.

[01-02](01-02-code-design-quality.md)는 실제 품질 기준과 구조 대비를, [01-03](01-03-behavior-verification.md)은 요구·동작을 확인할 근거·검사·실행 수단을 구체화한다. [04](../04-skill-improvements/README.md)는 이 흐름에 참여하는 기존 스킬의 실제 조건·본문·입출력·기록 연결을 맡는다. 같은 장면에서 함께 다루되 같은 판단을 별도 Ticket에서 반복 소유하지 않는다.

## 현재 결과와 근거

- [development](../../../records/prototypes/development-workflow/skills/development/SKILL.md): 맥락 이해·적용, 구현 첫 완성·인계, Main의 수정·종료·결과·기록 책임.
- [검토 상세](../../../records/prototypes/development-workflow/skills/development/references/review.md): 관련 기준을 읽고 독립적으로 대안을 비교하는 목적, 입력·추가 탐색·권한·호출, 근거와 Main의 선택.
- [검증 상세](../../../records/prototypes/development-workflow/skills/development/references/verification/INDEX.md): 독립 기대 결과·기계 검사·실제 경로·공백·재현·반환·재검증과 충분성.
- [실행 배치](../../../records/prototypes/development-workflow/skills/development/references/execution.md): 초기 모델·추론·인원, 세션 상속·재사용, 실제 입력·권한·판본과 재배정 조건.
- root/Work 진입의 일반 재개·한정 위임, work-discussion의 명시 호출, Main의 지침 기반 갱신, Personal A·B를 실제 본문에 연결했다. 자동 Maintain과 신규 기록 스킬은 연결하지 않았다.
- 독립 대조에서6번의 실제 사용 경로 완성 조건을 복원했다. 정적 문서·링크·열람 화면 확인은 완료했고, 실제 개발 전체 수행이나 일반 효과의 검증과 구별한다.

## 마감 뒤 이어갈 책임

이 Ticket의 진행·역할·인계 설계는 마쳤다. 개별 맥락 스킬의 현행 조항과 대상 차이 보완은04-03, 설명 응답의 유지·보완 판단은04-02, 품질 기준 전체 종합은01-02가 맡는다. 해당 결과에서 실제 충돌이 생기면 관련 본문을 보완한다.

실제 배치·장치 의존·설치 계획은06, 기록·재개·경험까지 잇는 전체 설계와 적용·관찰 계획은07이다. 이것을 이 Ticket의 새 완료 선행 조건으로 붙이지 않는다. [Spec·04를 포함한 다음 범위](../../../records/2026-10-24-ticket01-01-03-closeout-and-next-scope.md#spec-전체에서-완료와-남은-책임)를 따른다.

## 완료 조건과 확인 방법

- 대표 작업에서 목표를 결과로 나누고 필요한 조사·개발·검토를 찾는 방법이 구체적이다. 초안 파일 목록을 처리한 것으로 목표 달성을 대신하지 않는다.
- AI가 더 확인할 때, 판단 가능한 결과를 제시할 때, 사람의 선택이나 추가 관찰이 필요한 때를 사례로 비교한다. 중요한 사람 참여를 모두 줄이는 목표로 만들지 않는다.
- 검토 지적의 판단·수정·재확인·종료, 첫 보고와 기록의 책임이 연결된다. 01-02·01-03의 선택과 충돌하거나 빠진 부분을 드러낸다.
- 작은 변경과 큰 구조 개선에서 적용할 방법과 생략할 방법, 역할·자료·도구 비용, 이후 관찰할 품질·사용자 부담을 설명한다.
- 결과는 검토 가능한 진행안이다. 초기 연결 초안과 관련 결과를 반영한 설계 완료를 구별하며, 설계의 채택·구현·효과 확인을 완료로 앞당기지 않는다.

## 원래 논의와 현재 선택의 관계

[작업 단계 우선28](../../../records/2026-10-13-28-execution-system-priority-and-code-criteria.md), [Ticket별 과도한 분리 정정93](../../../records/2026-10-19-93-workflow-and-skills-discussion-focus.md), [Development의 본체·진입 역할103](../../../records/2026-10-19-103-prototype-session-checkpoint.md), [사용자의 역할 정정과 구체화 순서 원문](../../../source/discussion/2026-10-22-shared-criteria-independent-review/conversation.md#l1048--user)을 이어받는다.

[정리 전 Ticket](../../../records/2026-10-24-workflow-checkpoint-before.txt)에 초기 B 직접 수정·모델 미정·6번 이후 후속 등의 당시 상태를 보존했다. 현재 수정 기본값·입력·호출·종료는1~15번 합의가 소유하며 과거 후보로 되돌리지 않는다. 전체 목표와 완료 판단의 범위는 [Spec](../../spec.md)에 따른다.
