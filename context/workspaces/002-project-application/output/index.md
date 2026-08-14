# Project application output

마지막 갱신: `2026-08-14`

이 파일은 이 Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치를 연결한다. 산출물을 이 폴더에 복제하지 않으며, 상태와 검증 상한은 [`../current/state.md`](../current/state.md)가 소유한다.

## 현재 goal 산출물

### 첫 실제 Project 적용물

- canonical 진입점: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio/AGENTS.md`
- 적용된 Workspace: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio/context/work/workspaces/001-payment-recovery-mvp/`
- 이 Workspace에서의 역할: 기존 Project canonical을 유지한 context+harness 배치와 recover·verify·receipt 재진입 경로
- 현재 상한: 자동 구조·복구·고정 검증은 통과했지만 실제 브라우저 동작과 사람의 acceptance는 확인되지 않았다. 이후 원형·skill에 추가한 Workspace source/output/minimum-memory 계약은 이 target에 자동 적용하거나 재검증하지 않았다. 상세 근거는 [첫 적용 기록](../records/2026-08-13-01-payment-recovery-project-application.md)과 [`current/state.md`](../current/state.md)에 있다.

### 반복 적용 절차

- canonical 위치: repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill
- 이 Workspace에서의 역할: 첫 적용에서 추출한 이식 절차와 migration-only helper
- 현재 상한: 내부 검증은 통과했지만 두 번째 실제 Project 적용 전이므로 portability는 입증되지 않았다. 상세 근거는 [승격 기록](../records/2026-08-14-01-apply-context-harness-skill-promotion.md)에 있다.

## 적용 입력

- 실행 가능한 원형의 canonical은 이 저장소의 루트 [`output/`](../../../../output/)이다.
- 루트 `output/`은 첫 적용의 입력이며, 대상 Project에 배치된 goal 산출물 자체는 아니다.

이 지도에 위치가 있다는 사실은 Workspace 완료, 사용자 수락, target commit 또는 외부 동작 검증을 뜻하지 않는다.
