# 04-03 — 프로토타입 통합 뒤 독립 개선 검토

2026-10-26. [통합 적용 계획](2026-10-26-context-prototype-integration-plan.md)에 따른 실행 본문을 작성한 뒤 새 읽기 전용 검토자에게 현재 사용자 요청, 앞선 합의·정정·기존 스킬·외부 고정판의 접근점, 실제 prototype을 제공했다. Main의 예상 결함·평가 결론을 먼저 주지 않고 책임 중복·누락, 별도 요청, 유지 비용, 원래 목표에 대한 개선점을 요청했다. 실제 수행 시험과 구별되는 문서·소비 경로 검토다.

## 최초 반환과 Main 판단

검토자는 직접 읽기·근거 재사용·Main 반영·Work 유지·생성/전환의 연결에서 반복 입력·전면 재독·무조건 별도 agent·일상 정정의 재승인 경로는 찾지 못했다고 반환했다. 중요한 개선은 현재 사용 안내에 남은 이전 Project 갱신 예시 한 곳이었다.

핵심 반환 원문:

> 현재 walkthrough에 이전 Project 갱신 기준이 남아 있습니다.
> “코드 연결만 바뀌면 Project current를 맞춘다”고 안내합니다.
> 기존 인증 계약 안에서 새 소비자만 추가했는데 walkthrough를 따라 구현 상태를 Project에 누적합니다.

Main은 이 지적을 채택했다. 이 파일은 과거 기록이 아니라 README에서 연결되는 현재 수행 안내다. [walkthrough](prototypes/development-workflow/walkthrough.md)의 마지막 절을 구현자의 근거 제안, Main의 지속 의미 선별, 필요한 경우의 Project 반영과 이번 구현·검사의 Work 보존으로 맞췄다. Project의 모든 구현 사실을 제거하거나 제품 공통 지원 사실까지 금지하는 변경은 하지 않았다.

검토자가 제안한 같은 수행자의 읽기→반영과 읽기만 요청의 대비는 별도 복사본 시험에서 확인한다. 문서상 허용과 실제 수행의 관찰을 합치지 않는다.

## 좁은 후속 확인

같은 검토자에게 수정된 소비 경로와 두 장면만 다시 대조하게 했다. 반환:

> 지정한 범위에서 앞선 지적은 해소됐고, 두 장면의 책임·상태·근거 연결도 확인했습니다.

| 장면 | 대조한 실행 근거와 결론 |
| --- | --- |
| 기존 계약 안의 새 소비자 제안을 받고 Project 무수정으로 종료 | [context-update](prototypes/development-workflow/skills/context-update/SKILL.md)의 근거 대조·지속 내용 선별·편집 없는 종료와 [development](prototypes/development-workflow/skills/development/SKILL.md)의 Main 검토·Work 반영이 연결된다. 제안 수신을 문서 수정이나 제품 완료로 취급하지 않는다. |
| 일부 본문만 반영하고 중단한 뒤 재개 | 필요한 미반영은 미완료로 유지하고 Main이 반영한 곳·남은 검토·반영·확인을 이어받는다. [Work 지침](prototypes/development-workflow/noline-demo/context/work/AGENTS.md)이 남은 판단·담당·다음 행동을 보존한다. 현재판은 확인하되 유효한 제안·근거를 재사용하고 원 구현자 재호출·전면 재독은 기본 요구가 아니다. |

후속 검토는 실제 중단·복구 수행이나 host 전환을 시험한 것이 아니다. 복사본의 직접 요청 수행과 최종 검사 결과는 [적용 기록](2026-10-26-context-prototype-adoption.md)에 따로 남긴다. 장기 유지 비용·자동 발견·실제 운영 효과·외부 원문의 저자 귀속을 이번 리뷰로 재입증하지 않는다.
