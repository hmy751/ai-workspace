# Workspace transition continuity Workspace

새 Workspace가 이전 작업의 후속일 때 필요한 의미를 빠뜨리지 않으면서도 과거 Workspace 전체 상속·상호 동기화·Project context 자동 승격을 만들지 않는 Reference 계약을 정리하는 작업이다.

상태는 **session별 explicit admission과 same-session generation 전환 구현 / Maintain 내부 lifecycle canonical 분리 / Reference·target 로컬 검증 완료**다. 실제 Codex UI에서 서로 다른 여러 task의 hook trust·event 전달을 함께 확인하는 acceptance는 남아 있다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 이번 작업의 목표와 확정된 의미·경계
2. [`current/state.md`](current/state.md): 현재 변경 상태와 남은 확인
3. [`records/2026-08-28-01-workspace-transition-contract.md`](records/2026-08-28-01-workspace-transition-contract.md): 사용자 정정에서 도출한 문제 판정과 책임 배치
4. [`records/2026-08-28-02-validation-and-review.md`](records/2026-08-28-02-validation-and-review.md): 문서 연결·회귀 테스트·독립 리뷰 결과와 검증 상한
5. [`records/2026-08-28-03-canonical-cohesion-and-workspace-skill.md`](records/2026-08-28-03-canonical-cohesion-and-workspace-skill.md): canonical 응집, skill·이식 경계와 격리 forward test
6. [`records/2026-08-31-04-activation-rule-recalibration.md`](records/2026-08-31-04-activation-rule-recalibration.md): 새 Main session 절대 규칙의 기원과 조건부 전환 판단으로의 보정
7. [`records/2026-09-01-05-session-scoped-binding-and-rebind.md`](records/2026-09-01-05-session-scoped-binding-and-rebind.md): Project-wide 오연결 사건, generation 전환 구현·target 적용과 검증
8. [`records/2026-09-01-06-maintain-session-lifecycle-canonical.md`](records/2026-09-01-06-maintain-session-lifecycle-canonical.md): Session binding을 새 Harness peer가 아니라 Maintain 내부 authoritative subcanonical로 둔 책임 재배치
9. [`reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md`](../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md): 실제 Workspace 생성·전환 의미 canonical
10. [`reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md`](../../../reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md): Maintain 내부 session admission·generation·hook·runtime lifecycle canonical
11. [`reference-project/.agents/skills/create-context-workspace/SKILL.md`](../../../reference-project/.agents/skills/create-context-workspace/SKILL.md): 생성·전환 canonical을 실행하는 repo-local skill
12. [`output/index.md`](output/index.md): 선택한 현재 산출물과 proof ceiling

## 경계

- 이 Workspace는 완료된 007의 Maintain architecture를 이어받는 후속 Workspace가 아니다. 현재 live Reference와 이번 사용자 결정을 직접 근거로 별도 goal을 소유한다.
- `memory-harness-research`에서 드러난 사건은 Reference 판단을 다시 여는 적용 장면이다. 이번 단계는 사용자의 명시적 요청으로 host adapter·session state·hook config와 운영 문서까지 확장했지만 Target의 연구 내용과 Workspace 004에는 이 Harness 사건을 기록하지 않는다.
- Recover·Maintain의 기존 실행 의미를 넓히지 않고 Workspace collection 아래 생성·전환 canonical과 교체 가능한 repo-local skill, 각 Harness의 비소유 경계를 정렬한다.
- Session binding은 Recover·Maintain·Verify와 나란한 새 Harness 책임이 아니다. Maintain 전체 정체성과 내부 책임 관계는 Maintain README, 생성·전환의 의미 판단은 `CREATE-AND-TRANSITION.md`, 명시적 session admission과 generation·hook·runtime lifecycle은 Maintain 내부 `SESSION-BINDING-AND-LIFECYCLE.md`가 각각 소유한다.
- Session binding state schema v2와 explicit control CLI는 만들지만 Workspace parent 관계, 공통 handoff 파일, Workspace 자동 선택·동기화와 생성 runtime은 만들지 않는다.
- 사람 acceptance와 commit은 이 Workspace가 자동으로 결정하지 않는다.
