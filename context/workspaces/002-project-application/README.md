# Project application Workspace

`output/`에서 검증한 context+harness 책임을 실제 기존 Project 하나에 적용하고, 그대로 가져갈 책임과 대상 Project에 맞게 바꿀 배치를 확인하는 Workspace다.

상태는 **active**다. 적용 대상은 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`이며, 구조 적용·고정 자동 검증·재진입은 완료했다. 현재는 사람의 acceptance와 실제 브라우저 동작 검증을 기다린다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 적용 목표·대상·지속 결정·검증 상한·접근점
2. [`current/state.md`](current/state.md): 현재 검증 상태·남은 불확실성·다음 행동
3. [`records/`](records/): 적용 결정, migration, 실패·성공 검증과 증거 상한

이 Workspace는 `output/context/work`의 전체 구조를 정답처럼 복제하지 않는다. 대상 Project의 기존 canonical과 배치를 먼저 확인하고, 필요한 책임과 운영 흐름만 최소로 적용한다.
