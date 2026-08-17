# Harness maintenance bottleneck Workspace

Context+harness의 작은 계약 변경이 기준 Project, 이식 skill, 여러 Workspace current·records, 검증과 review까지 넓게 전파된 사례에서 시작한 유지보수 병목 분석 공간이다.

상태는 **paused**다. `reference-project`의 Recover·Maintain·Verify·validation 책임 재배치는 commits `638bfbc`, `7793bab`에, skill 간소화와 Project context Owner closure 교정은 commit `f082035`에 보존됐다. 최신 skill 교정은 아직 재시험·사람 acceptance 전이다. 이후 제기된 일상 운영 지연, `current/records` 신뢰성과 background maintenance 설계는 별도 [`Workspace 005`](../005-context-continuity-maintenance/)가 소유한다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 유지할 안전 기준, 범위
2. [`current/state.md`](current/state.md): 현재 확인된 병목과 다음 분석 행동
3. [`output/index.md`](output/index.md): 이 Workspace goal의 선택된 개선 산출물
4. [`records/`](records/): 관찰, 후보, 결정, 실험과 검증 기록

이 Workspace는 이전 구현·적용 Workspace를 합치거나 historical record를 현재 계약에 맞춰 다시 쓰지 않는다. 교정된 책임 구조와 검증은 [`records/2026-08-14-06`](records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md), Maintain agent 배치와 등록 결정은 [`records/2026-08-14-07`](records/2026-08-14-07-reference-maintain-agent-colocation-and-registration.md), skill 간소화와 forward preflight는 [`records/2026-08-14-08`](records/2026-08-14-08-apply-context-harness-simplification-and-verification.md), v2 당시 평가는 [`records/2026-08-16-01`](records/2026-08-16-01-simplified-skill-reapplication-result.md), v3 당시 평가는 [`records/2026-08-16-02`](records/2026-08-16-02-semantic-content-closure-correction-and-v3-forward-test.md), omission loophole 교정은 [`records/2026-08-16-03`](records/2026-08-16-03-project-context-owner-omission-loophole-correction.md)에서 확인한다. 앞선 판단은 당시 상태 그대로 보존한다.
