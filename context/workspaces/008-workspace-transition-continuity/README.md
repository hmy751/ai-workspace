# Workspace transition continuity Workspace

새 Workspace가 이전 작업의 후속일 때 필요한 의미를 빠뜨리지 않으면서도 과거 Workspace 전체 상속·상호 동기화·Project context 자동 승격을 만들지 않는 Reference 계약을 정리하는 작업이다.

상태는 **Reference 문서 계약 반영·검증·독립 리뷰 완료 / 사용자 acceptance 대기**다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 이번 작업의 목표와 확정된 의미·경계
2. [`current/state.md`](current/state.md): 현재 변경 상태와 남은 확인
3. [`records/2026-08-28-01-workspace-transition-contract.md`](records/2026-08-28-01-workspace-transition-contract.md): 사용자 정정에서 도출한 문제 판정과 책임 배치
4. [`records/2026-08-28-02-validation-and-review.md`](records/2026-08-28-02-validation-and-review.md): 문서 연결·회귀 테스트·독립 리뷰 결과와 검증 상한
5. [`reference-project/context/work/workspaces/README.md`](../../../reference-project/context/work/workspaces/README.md): 실제 Workspace 생성·전환 canonical
6. [`output/index.md`](output/index.md): 선택한 현재 산출물과 proof ceiling

## 경계

- 이 Workspace는 완료된 007의 Maintain architecture를 이어받는 후속 Workspace가 아니다. 현재 live Reference와 이번 사용자 결정을 직접 근거로 별도 goal을 소유한다.
- `memory-harness-research`에서 드러난 사건은 문제를 발견한 장면일 뿐 이 Workspace의 수정 대상이 아니다.
- Recover·Maintain의 기존 실행 의미를 넓히지 않고 Workspace collection이 소유할 생성·전환 의미와 각 Harness의 비소유 경계를 문서로 정렬한다.
- 새 machine schema, Workspace parent 관계, 공통 handoff 파일, 자동 동기화와 생성 runtime은 만들지 않는다.
- 사람 acceptance와 commit은 이 Workspace가 자동으로 결정하지 않는다.
