# Project application Workspace

`output/`에서 검증한 context+harness 책임을 실제 기존 Project 하나에 적용하고, 그대로 가져갈 책임과 대상 Project에 맞게 바꿀 배치를 확인하는 Workspace다.

상태는 **active**다. 원본 대상 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`의 첫 적용과 검증은 Git 이력에 보존했고, 현재 원본에서는 Harness를 제거한 clean 상태다. 격리 사본 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`에서는 과거 002 문서를 보지 않은 blind 재적용·자동 검증을 완료했지만, 원본 설치나 사람 acceptance로 보지 않는다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 적용 목표·대상·지속 결정·검증 상한·접근점
2. [`current/state.md`](current/state.md): 현재 검증 상태·남은 불확실성·다음 행동
3. [`output/index.md`](output/index.md): 이 Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치
4. [`records/`](records/): 적용 결정, migration, 실패·성공 검증과 증거 상한

이 Workspace는 `output/context/work`의 전체 구조를 정답처럼 복제하지 않는다. 대상 Project의 기존 canonical과 배치를 먼저 확인하고, 필요한 책임과 운영 흐름만 최소로 적용한다.

첫 적용에서 반복 가능한 이식 절차는 repo-local [`apply-context-harness`](../../../.agents/skills/apply-context-harness/) skill로 승격했다. skill은 실제 적용 결과를 소유하지 않으며, 각 이식의 결과와 예외는 이 Workspace의 records에 남긴다.
