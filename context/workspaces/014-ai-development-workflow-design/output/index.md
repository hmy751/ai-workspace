# 현재 선택한 설계 자료와 산출물

**Ticket 03의 구성안·본문 예시는 완료됐다.** 현재 결과와 한계는 [03](../current/tickets/03-project-context.md), 완료 판단·후속 책임은 [119](../records/2026-10-20-119-ticket03-closeout.md)에서 확인한다. Workspace014 전체의 목표는 컨텍스트·코드 기준·절차·검증·기록·경험 반영이 연결된 개발 체계를 설계하는 것이다.

## 현재 결과를 읽는 곳

| 산출물 | 맡는 내용과 현재 지위 |
| --- | --- |
| [단일 적용 프로토타입](../records/prototypes/development-workflow/README.md) · [열람 화면](../records/prototypes/development-workflow/viewer.html) | 같은 폴더에서 발전시킨 본문·실행 예제·적용 장면. Markdown과 코드가 정본이며 화면은 표시 사본이다. 실제 운영 Noline에 설치한 결과는 아니다. |
| [Personal 개발 기준](../records/prototypes/development-workflow/noline-demo/context/personal/development/README.md) | 일반 판단과 조건·분할 본문·사례, 수정에 필요한 형성 자료. 개인 기준 전체 항목과 모든 문장의 최종 채택은01-02와 후속 적용에서 이어 본다. |
| [Project context](../records/prototypes/development-workflow/noline-demo/context/project/README.md) | 기기·세션 계약, 인증 개발 가이드, 코드 표현, 현재 인증 구현과 구성·읽기·관리 지침. 개인 기준의 채택·갱신 관리를 Project에 맡기지 않는다. |
| [CONTENT-POLICY](../records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md) | 지속 본문과 형성 자료의 역할·배치·읽기·갱신. 사례를 필수 서식으로 만들지 않으며 Work는 적용을 보류한다. |
| [SYSTEM-GUIDANCE](../records/prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md) | 체계 지침의 성격, 진입 본문·상세 지침의 책임과 이름·위치. [118](../records/2026-10-20-118-system-guidance-definition-and-entry.md)에 선택 이유와 확인 범위가 있다. |
| [DEVELOPMENT](../records/prototypes/development-workflow/noline-demo/context/work/DEVELOPMENT.md) · [작업 장면](../records/prototypes/development-workflow/walkthrough.md) | 필요한 기준·제품 계약을 선택해 구현·검토·갱신에 쓰는 연결 시안. 최종 역할 운영·스킬 관계·위치·Owner는01-01·04-03의 후속 결과다. |
| [Work 예시](../records/prototypes/development-workflow/noline-demo/context/work/README.md) | 기존 Spec·Ticket·current·source·output·records를 유지한 인증 이름 변경 작업. [116](../records/2026-10-20-116-defer-work-content-policy.md)의 복구 상태이며 새 background 정책을 적용한 표준이 아니다. |

본문의 목적·의미·조건은 대상물 안에서 이해할 수 있게 구성했다. 바깥014 records는 작성·평가·정정의 과정을 보존하며, 대상물 본문을 대신하는 정본이 아니다. 형성 이유를 다시 볼 필요가 있을 때는 본문 가까운 자료에서 시작한다.

## 전체 설계와 다른 Ticket의 입력

- [work-discussion prototype 본문](../records/prototypes/development-workflow/skills/work-discussion/SKILL.md): 04-01 설계 결과 완료. 기존 정의·보완 후보 대조와 요청별 반환의 최소안을 승인·반영했고 reconsider-work는 유지한다. [두 조건 수행 기록](../records/2026-10-21-ticket04-01-minimal-update-and-two-checks.md)에 확인과 한계가 있다. 사용자 위치 정정으로 Reference 수정은 원복했다. Reference·외부 Noline 설치나 운영 책임 변경은 포함하지 않는다.
- [Spec](../current/spec.md): 전체 목적·공통 기준·잠정안·선택·미정.
- [Ticket 목록](../current/tickets/index.md): 결과별 책임과 후속 연결.01-02·04-03 등의 완료 상태는03 완료로 함께 바꾸지 않는다.
- [01-02 기준 종합54](../records/2026-10-16-54-code-quality-criteria-and-remaining-work.md)와 [형식 반영72](../records/2026-10-18-72-short-common-and-detail-prototype.md): 코드 기준과 공통·상세·사례의 앞선 입력. [73](../records/2026-10-18-73-prototype-reservations-and-ticket03.md)의 당시 전체 만족 유보를 함께 읽고, 현재 본문은 위 단일 prototype에서 확인한다.
- [B 방향 선택15](../records/2026-10-12-15-reviewer-editing-choice-and-start.md): 검토자가 필요한 품질 수정을 직접 수행하는 사용자 선택. 상세 인계·최종 확인·스킬 구현은 후속 설계다.
- [원자료 조사27](../records/2026-10-13-27-source-investigation-and-proposal-reset.md)와 [작업 단계 우선순위28](../records/2026-10-13-28-execution-system-priority-and-code-criteria.md): 외부 방식의 실제 계약과 사용자가 우선 구체화할 범위.
- [설계 논의 지도](../current/design-map.md): 다음 논의에서 필요한 전체 관점. 확정 분류가 아니다.

이전 날짜별 prototype·비교·선택 이유는 [기록 색인](../records/README.md)에 보존한다. 같은 결과를 output에 복제하거나 과거 기록 전체를 현재 산출물로 다시 열거하지 않는다. 이 지도에 연결된 사실은 운영 채택·설치·장기 효과의 확인을 뜻하지 않는다.
