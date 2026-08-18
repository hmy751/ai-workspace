# Maintain behavior responsibility allocation Workspace

Workspace 005에서 합의한 Reference Maintain의 목적과 사용자 경험을 보존하면서, 당시 구현을 책임 배치 관점에서 개선하려 했던 Workspace다.

상태는 **stopped**다. 기존 코드를 개선 대상으로 둔 채 시작하면서 구현 topology에 판단이 계속 묶였고, 첫 구조 변경도 compatibility와 crash protocol을 다시 키웠다. 사용자는 이 접근을 더 보정하지 않고, Workspace 005의 합의와 글로벌 AI-system references에서 새 구현을 도출하는 별도 Workspace로 책임을 옮기기로 결정했다. 006의 코드 변경은 선택된 산출물이 아니며 새 구현의 architecture로 이어받지 않는다.

## 읽는 순서

1. [`current/state.md`](current/state.md): 중단 상태, 검증 상한과 이관 커서
2. [`records/2026-08-18-05-clean-room-restart-decision.md`](records/2026-08-18-05-clean-room-restart-decision.md): 왜 006을 멈추고 코드 기준선을 되돌리는지
3. [`records/2026-08-18-03-self-check-and-purpose-first-reset.md`](records/2026-08-18-03-self-check-and-purpose-first-reset.md): Workspace 005에서 복원한 사용자 mental model
4. [`records/2026-08-18-04-completed-response-and-workspace-attention.md`](records/2026-08-18-04-completed-response-and-workspace-attention.md): 선택되지 않은 구현 시도와 proof ceiling
5. [`records/README.md`](records/README.md): 기록 전체의 진입점

## 이 Workspace가 보존하는 것

- Reference Maintain의 운영상 하나인 동작과 시작 조건·입력·결과·부작용·비목표 식별
- Workspace 005 records에서 사용자 목적, 실패한 Observe 실험과 교체 가능한 기술 후보를 시간순으로 복원
- 목적에서 필요한 최소 semantic 판단·durable state·source of truth를 먼저 도출
- 해석·선택, 보장·거부, 권한·승인, 실행·기록 책임의 현재 배치 대조
- 현재 파일·protocol을 유지할 이유와 제거·통합·파생 가능성, 추가 실패·복구·검증 비용 대조
- 지침·prompt·schema·config·validator·code·test가 각각 표현·집행·검증해야 하는 최소 약속 확인
- 기능을 늘리는 대신 중복, 숨은 정책, 과도한 runtime 책임과 불명확한 작성 경계 제거
- 책임을 단순화·교체·이동·제거할 때 달라지는 약속과 검증 범위 기록
- 기존 topology를 개선하는 접근이 다시 compatibility 중심 설계로 커진 과정과 중단 이유

## 더 하지 않는 것

- 006의 implementation diff를 수정하거나 새 architecture로 승격
- 006 안에서 Reference Maintain을 계속 구현
- Workspace 005의 historical records 재작성
- 새 Workspace의 current나 결정을 006에 대신 기록

Workspace 005는 당시의 합의·실험·최종 구현과 proof를 소유한다. 006은 기존 구현 개선 시도의 기록만 소유하며, 다음 구현은 별도 Workspace가 독립적으로 판단한다.
