# Maintain behavior responsibility allocation Workspace

Workspace 005에서 완성한 Reference Maintain의 사용자 기능을 기본적으로 유지하면서, 그 동작을 구성하는 모델 판단, 지침·prompt, schema·validator, controller·runtime·writer와 사람 권한의 배치가 적절한지 점검하고 내부 코드와 작성 방식을 개선하는 Workspace다.

상태는 **active**이며 아직 구체적인 개선 대상이나 변경안은 정하지 않았다. 작업은 글로벌 [`ai-system_behavior-responsibility-allocation.md`](/Users/hammyeong-yeon/.claude/references/ai-system_behavior-responsibility-allocation.md)를 판단 기준으로 삼되, reference를 복제하거나 수정하지 않고 Workspace 안에서 실제 Maintain 동작과 책임 배치를 대조한다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 적용할 책임 배치 기준과 현재 경계
2. [`current/state.md`](current/state.md): 시작 상태, 아직 정하지 않은 것과 다음 대화의 커서
3. [`output/index.md`](output/index.md): 개선 대상인 Reference canonical과 Workspace 005 구현 baseline
4. [`records/README.md`](records/README.md): 이후 만들어질 분석·결정·검증 기록의 진입점
5. 글로벌 [`AI 동작의 판단·보장·권한 배치`](/Users/hammyeong-yeon/.claude/references/ai-system_behavior-responsibility-allocation.md): 실제 동작에서 책임 배치를 판단할 때 읽는 기준

## 범위

- Reference Maintain의 운영상 하나인 동작과 시작 조건·입력·결과·부작용·비목표 식별
- 해석·선택, 보장·거부, 권한·승인, 실행·기록 책임의 현재 배치 대조
- 지침·prompt·schema·config·validator·code·test가 각각 표현·집행·검증하는 약속 확인
- 기능을 늘리는 대신 중복, 숨은 정책, 과도한 runtime 책임과 불명확한 작성 경계 개선
- 책임을 단순화·교체·이동·제거할 때 달라지는 약속과 검증 범위 기록
- 결정된 개선의 실제 canonical 반영과 필요한 직접 test·eval·수동 확인

## 현재 범위 밖

- 구체적인 문제와 근거를 확인하기 전 새 기능이나 새 runtime 상태 추가
- Workspace 005의 historical records 재작성 또는 완료된 구현 이력 복제
- 글로벌 `ai-system_behavior-responsibility-allocation.md` 자체 수정
- 사용자 대신 정책, 중요한 예외, acceptance나 완료를 확정하는 것
- 직접 관련성이 확인되지 않은 Recover·Verify·다른 Workspace의 확장 검토

Workspace 005는 현재 구현과 그 선택·proof를 소유한다. 이 Workspace는 필요한 baseline만 연결하고, 내부 책임 배치 개선 과정과 새 결론을 독립적으로 소유한다.
