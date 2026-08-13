# Project application memory

마지막 갱신: `2026-08-13`

## 목표

실제 기존 Project 하나에서 사람과 AI가 Project 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 다시 지속 상태에 반영하는 흐름을 적용·검증한다.

## 적용 기준

- [`output/`](../../../../output/)은 책임과 흐름을 검증한 reference이지, 모든 Project에 그대로 복사할 범용 템플릿이 아니다.
- 대상 Project의 기존 canonical, 디렉터리 배치, 테스트와 운영 방식을 먼저 확인한다.
- 경로 이름보다 Project common context, Workspace current/records, recover/verify 책임과 인계가 실제로 어디에 귀속되는지를 본다.
- 필요한 최소 경계부터 적용하고, Harness가 없어져도 Project와 Workspace의 의미가 남도록 한다.
- 다른 Desktop 저장소는 사용자가 대상과 작업 범위를 지정한 뒤에만 읽거나 수정한다.

## Reference 접근점

- 실행 가능한 reference: [`output/README.md`](../../../../output/README.md)
- Project–Workspace 최초 합의: [`001 record 03`](../../001-reference-implementation/records/2026-08-13-03-project-workspace-context-agreement.md)
- Project·Work root 분리 결과와 검증 상한: [`001 record 07`](../../001-reference-implementation/records/2026-08-13-07-project-work-context-boundary.md)

## 완료 의미

- 대상 Project와 변경 권한·범위가 명확하다.
- 대상 Project의 기존 context와 작업 상태를 훼손하지 않고 필요한 최소 구조를 적용했다.
- 실제 작업 하나에서 복구·행동·검증·지속 상태 반영·재진입을 확인했다.
- reference와 달리 적용한 부분, 아직 증명하지 못한 범위, 제거 가능한 Harness 경계를 기록했다.
