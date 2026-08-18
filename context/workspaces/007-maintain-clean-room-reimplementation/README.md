# Maintain clean-room reimplementation Workspace

Workspace 005에서 합의한 Maintainer의 사용자-facing 동작을 보존하되, Workspace 005의 최종 구현과 Workspace 006의 개선 시도에서 architecture를 이어받지 않고 Reference Maintain을 다시 구현하는 작업이다.

상태는 **active / ready for fresh-session design**이다. `005의 동작은 입력`, `005·006의 구현 topology는 입력이 아님`을 이 Workspace의 출발 경계로 둔다.

## 읽는 순서

1. [`current/index.md`](current/index.md): 현재 Context의 범위와 재진입 순서
2. [`current/memory.md`](current/memory.md): 보존할 여섯 사용자 장면, 책임·소유 경계와 금지선
3. [`current/state.md`](current/state.md): reset된 code baseline, 검증 상한과 다음 행동
4. [`records/2026-08-18-01-clean-room-source-and-behavior-contract.md`](records/2026-08-18-01-clean-room-source-and-behavior-contract.md): Workspace 005 원문 근거와 글로벌 reference 적용
5. [`records/2026-08-18-02-code-reset-baseline-and-excluded-topologies.md`](records/2026-08-18-02-code-reset-baseline-and-excluded-topologies.md): 정확한 복원 경계와 반복하지 않을 구조
6. [`records/2026-08-18-03-clean-room-implementation-handoff.md`](records/2026-08-18-03-clean-room-implementation-handoff.md): 새 세션 실행용 handoff packet
7. [`output/index.md`](output/index.md): 아직 선택된 구현이 없다는 현재 output 경계

## 이 Workspace가 소유하는 것

- 사용자에게 관찰되는 Maintain 동작과 acceptance 장면
- 모델·규칙 기반 장치·사람 사이의 판단·보장·권한 배치
- Reference Maintain의 새 구조, 구현, 검증과 선택 근거
- 새 구현이 root의 얇은 연결로 활성화되기 전 proof ceiling
- 구현 중 생긴 지속 가능한 결정·실패·검증 기록

## 이 Workspace가 소유하지 않는 것

- Workspace 005 records와 당시 합의·실험·구현 이력의 재작성
- Workspace 006의 `completed pair`, attention, migration·compatibility 코드를 이어 고치는 일
- 글로벌 `ai-system_*` reference 수정
- 제품 test·eval을 Maintain이나 Verify가 대신 소유하게 만드는 일
- 실제 host acceptance 전에 root hook·agent를 다시 활성화하는 일
- repository history rewrite나 사용자 소유 `.DS_Store` 변경

## 완료의 의미

코드와 unit test가 생겼다는 사실만으로 완료하지 않는다. 여섯 사용자 장면을 구조 독립적 acceptance로 연결하고, 재사용 가능한 책임·구현·검증을 Reference에서 함께 찾을 수 있으며, 실제 host에서 초기 grounding·warm continuity·response-end 비차단·보고·실패 장면을 확인한 뒤에만 root 연결을 선택할 수 있다.
