# Maintain clean-room reimplementation Workspace

Workspace 005에서 합의한 Maintainer 동작을 보존하되, Workspace 005의 최종 구현과 Workspace 006의 개선 시도가 새 architecture를 자동으로 구속하지 않는 상태에서 Reference Maintain을 다시 구현하는 작업이다.

상태는 **Reference clean-room implementation 완료 / outer root 적용은 별도 큰 범위로 보류**다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표와 판단 경계
2. [`current/state.md`](current/state.md): 현재 code baseline과 다음 시작점
3. [`records/2026-08-18-01-clean-room-source-and-behavior-contract.md`](records/2026-08-18-01-clean-room-source-and-behavior-contract.md): Workspace 005에서 선택한 사용자 근거와 동작 계약
4. [`records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md`](records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md): 복원 범위와 과거 topology의 근거·proof ceiling
5. [`records/2026-08-19-03-implementation-goal-and-reading-boundary.md`](records/2026-08-19-03-implementation-goal-and-reading-boundary.md): 실제 구현 목표, 충분한 mental model과 더 읽지 않을 과거 범위
6. [`records/2026-08-19-04-acceptance-and-first-implementation-slice.md`](records/2026-08-19-04-acceptance-and-first-implementation-slice.md): 여섯 장면의 acceptance, host 제약과 첫 구현 책임
7. [`records/2026-08-19-05-reference-implementation-and-host-evidence.md`](records/2026-08-19-05-reference-implementation-and-host-evidence.md): 실제 구현, direct test·actual Codex 장면과 당시 독립 리뷰의 proof gap
8. [`records/2026-08-19-06-purpose-rebaseline-and-remaining-scope.md`](records/2026-08-19-06-purpose-rebaseline-and-remaining-scope.md): Maintainer 목적 재기준화, 현재 유지·수정·보류와 root 연결 전 남은 범위
9. [`records/2026-08-19-07-failure-ordering-and-semantic-acceptance.md`](records/2026-08-19-07-failure-ordering-and-semantic-acceptance.md): 실패 뒤 후속 event의 최소 정책과 실제 Maintainer 연속 대화 acceptance
10. [`records/2026-08-19-08-root-connection-boundary.md`](records/2026-08-19-08-root-connection-boundary.md): Reference와 outer root Context 구조 대조, 단순 연결을 중단한 이유와 별도 적용 범위
11. [`reference-project/`](../../../reference-project/): 새 세션이 직접 읽고 현재 구조에서 다시 판단할 실제 대상
12. [`output/index.md`](output/index.md): 선택된 구현과 연결 상태

## 경계

- 005의 사용자 동작은 보존 기준이다. 005·006의 구현 topology는 필수도 금지도 아니며, 같은 구조를 유지하거나 피해야 할 의무 없이 현재 조건에서 다시 판단한다.
- 007은 분석만 하는 Workspace가 아니다. Global reference를 구현 전 설계 입력으로 적용해 reset된 `reference-project/`에 Maintain을 다시 구현한다.
- 이 Workspace 문서는 `reference-project/`를 대신 설명하지 않는다. 새 세션이 실제 파일과 글로벌 AI-system references를 직접 읽는다.
- Workspace 005·006은 역사적 근거로 보존하고 재작성하지 않는다.
- 과거 Workspace와 runtime을 넓게 다시 읽어 architecture 기준으로 만들지 않는다. 추가 근거가 필요하면 007이 지목한 exact source만 연다.
- Outer root automatic Maintain은 계속 비활성이다. Reference 미완성 때문이 아니라 outer `context/workspaces/`와 Reference `context/work/workspaces/`의 canonical·Recover·Guard 계약이 달라 별도 target 적용 판단이 필요하다.
