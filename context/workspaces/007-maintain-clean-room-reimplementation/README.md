# Maintain clean-room reimplementation Workspace

Workspace 005에서 합의한 Maintainer 동작을 보존하되, Workspace 005의 최종 구현과 Workspace 006의 개선 시도가 새 architecture를 자동으로 구속하지 않는 상태에서 Reference Maintain을 다시 구현하는 작업이다.

상태는 **active / no selected implementation**이다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표와 판단 경계
2. [`current/state.md`](current/state.md): 현재 code baseline과 다음 시작점
3. [`records/2026-08-18-01-clean-room-source-and-behavior-contract.md`](records/2026-08-18-01-clean-room-source-and-behavior-contract.md): Workspace 005에서 선택한 사용자 근거와 동작 계약
4. [`records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md`](records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md): 복원 범위와 과거 topology의 근거·proof ceiling
5. [`reference-project/`](../../../reference-project/): 새 세션이 직접 읽고 현재 구조에서 다시 판단할 실제 대상
6. [`output/index.md`](output/index.md): 선택된 구현 여부

## 경계

- 005의 사용자 동작은 보존 기준이다. 005·006의 구현 topology는 필수도 금지도 아니며, 같은 구조를 유지하거나 피해야 할 의무 없이 현재 조건에서 다시 판단한다.
- 이 Workspace 문서는 `reference-project/`를 대신 설명하지 않는다. 새 세션이 실제 파일과 글로벌 AI-system references를 직접 읽는다.
- Workspace 005·006은 역사적 근거로 보존하고 재작성하지 않는다.
- Root automatic Maintain은 새 구현의 actual acceptance 전까지 비활성이다.
