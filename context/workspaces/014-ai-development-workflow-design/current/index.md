# 현재 논의의 진입점

구현·검토 논의의 현재 선택은 [관련 기준 공유·별도 판단](../records/2026-10-22-shared-criteria-and-independent-review-decision.md)이다. 입력을 숨기는 방식보다 관련 기준을 공유하면서 현재 선택과 적용을 재검토하고 Main이 종합하는 방향을 받아들였다. 상세 입력·권한·수정·반복 조건은 미정이다. 실제 문서로 공통·차등·조건부 입력을 정하는 것은 Main의 다음 추천이며, 1~5번 전체가 확정된 것은 아니다. 재개 시 해당 기록의 ‘다른 세션이 이어받아야 할 대화의 뉘앙스’와 ‘재개할 때 필요한 최소 경로’를 먼저 읽고 사용자가 지목한 항목을 이어간다. 아래 과거 03 마감의 재진입 설명과 구별한다.

**Ticket 03의 구성안·본문 예시 구체화를 완료했다.** [state](state.md)에서 마감 상태와 후속 범위, [03](tickets/03-project-context.md)에서 완료 조건별 근거, [119](../records/2026-10-20-119-ticket03-closeout.md)에서 이번 마무리 판단을 읽는다. Workspace014 전체와 다른 Ticket은 계속 열려 있다.

현재 산출물은 [development-workflow](../records/prototypes/development-workflow/README.md)의 본문·사례·코드·작업 장면이다. [CONTENT-POLICY](../records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)는 본문과 형성 자료의 관리를, [SYSTEM-GUIDANCE](../records/prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md)는 체계 지침과 진입·상세의 역할을 설명한다. 실제 운영 Noline·스킬·하네스 설치는 하지 않았다.

04-02를 이어갈 때는 [해당 Ticket](tickets/04-skill-improvements/04-02-artifact-explanation.md)과 [원문 중심 source](../source/artifact-explanation-scenes/README.md)를 먼저 읽는다. 네 장면의 원문과 당시 코드·최초 diff·도구 기록을 확보했고 [비교 설계](../records/2026-10-22-ticket04-02-historical-materials-and-comparison-design.md)를 준비했다. 첫 보고 전 적용 배치와 같은 시점의 본문 비교를 구별하며 아직 응답 시험을 실행하지 않았다. 전체 실행·DB 복원과의 차이도 유지한다.

## 재진입

1. [state](state.md)와 [output](../output/index.md)에서 이번에 끝낸 결과·현재 실물·다음 행동을 확인하고 Git 상태를 대조한다.
2. [memory](memory.md)의 대상물 경계·독립 책임·형성 자료·체계 지침에 관한 지속 기준과 [Spec](spec.md)의 전체 목표·3절·5절을 읽는다.
3. 다음 워크플로 논의를 재개할 때는 [01-01](tickets/01-development-workflow/01-01-development-flow.md)과 [04-03](tickets/04-skill-improvements/04-03-context-skills.md), 현재 DEVELOPMENT를 함께 본다. 이번 마무리는 후속 착수가 아니며02를 선행 완료 조건으로 두지 않는다.

## 문서별 책임

- [memory.md](memory.md): 단계가 바뀌어도 유지할 사용자 의도·기준·선택과 배경.
- [spec.md](spec.md): 전체 목표·공통 기준·전체 잠정안과 미결정.
- [tickets/index.md](tickets/index.md): 01~07과 하위 결과의 관계. 상세 결과·완료 조건은 각 Ticket이 맡는다.
- [state.md](state.md): 지금의 상태·다음 행동·검증 상한.
- [design-map.md](design-map.md): 전체안에서 놓친 관점을 살필 논의 지도. 확정 아키텍처가 아니다.

## 필요한 이유를 다시 볼 때

| 질문 | 접근점 |
| --- | --- |
|03에서 무엇을 끝냈고 무엇을 남겼는가 | [119](../records/2026-10-20-119-ticket03-closeout.md)와03 완료 조건 대조 |
| 체계 지침·진입 본문·상세를 왜 구별했는가 | [118](../records/2026-10-20-118-system-guidance-definition-and-entry.md)와 실제 본문 옆 형성 자료 |
| 본문·사례와 형성 맥락·기록·근거는 어떻게 구성했는가 | [CONTENT-POLICY](../records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md), 적용·정정 마무리[117](../records/2026-10-20-117-content-policy-application-checkpoint.md) |
| Work에 적용하지 않는 이유는 무엇인가 | [116](../records/2026-10-20-116-defer-work-content-policy.md)의 사용자 정정·기존 제약·복구 대조 |
| 개인 기준과 Project의 관리 책임은 무엇인가 | [102](../records/2026-10-19-102-personal-project-update-ownership.md), 현재 memory |
|01-02에서 무엇을 이어받았는가 | [해당 Ticket](tickets/01-development-workflow/01-02-code-design-quality.md), [72](../records/2026-10-18-72-short-common-and-detail-prototype.md)·[73](../records/2026-10-18-73-prototype-reservations-and-ticket03.md). 당시 형식 선택과 전체 유보를 구별한다. |
| 기존 Project 내용과 원자료는 무엇이었는가 | [지도77](../records/2026-10-18-77-existing-project-content-map.md), [비교78](../records/2026-10-18-78-code-guides-comparison-and-applicability.md), [자료 안내](../source/README.md) |

과거 시안·정정·검토는 [records](../records/README.md)에서 필요한 만큼 선택한다. 보존 원문을 현재 결론으로 덮어쓰지 않고, 과거의 미완료·첫 행동과 현재03 완료를 구별한다. Main이 수동으로 관리하며 Reference의 자동화·JSON 계약을 설치한 Workspace는 아니다.
