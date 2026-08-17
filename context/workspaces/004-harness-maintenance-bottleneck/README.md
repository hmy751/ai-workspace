# Harness maintenance bottleneck Workspace

Context+harness의 작은 계약 변경이 기준 Project, 이식 skill, 여러 Workspace current·records, 검증과 review까지 넓게 전파된 사례에서 시작한 유지보수 병목 분석 공간이다.

상태는 **active**다. `reference-project`의 Recover·Maintain·Verify·validation 책임 재배치는 commits `638bfbc`, `7793bab`에 보존됐다. Skill의 exact 실행 계약 중복은 제거했고 v3에서 링크형 common context는 개선했지만, target에 독립된 product criteria와 recovery decision이 있는데도 `prd/`·`decisions/` Owner를 생략할 수 있는 loophole을 사용자가 발견했다. Main은 구분되는 공통 책임별 Owner와 근거 있는 omission 규칙을 다시 보강했고 이 변경을 Workspace 기록과 함께 Git history에 보존했지만 아직 재시험하지 않았다. 사람 acceptance, 반복 timing flake 진단과 서로 다른 Project 검증 여부는 열려 있다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 유지할 안전 기준, 범위
2. [`current/state.md`](current/state.md): 현재 확인된 병목과 다음 분석 행동
3. [`output/index.md`](output/index.md): 이 Workspace goal의 선택된 개선 산출물
4. [`records/`](records/): 관찰, 후보, 결정, 실험과 검증 기록

이 Workspace는 이전 구현·적용 Workspace를 합치거나 historical record를 현재 계약에 맞춰 다시 쓰지 않는다. 교정된 책임 구조와 검증은 [`records/2026-08-14-06`](records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md), Maintain agent 배치와 등록 결정은 [`records/2026-08-14-07`](records/2026-08-14-07-reference-maintain-agent-colocation-and-registration.md), skill 간소화와 forward preflight는 [`records/2026-08-14-08`](records/2026-08-14-08-apply-context-harness-simplification-and-verification.md), v2 당시 평가는 [`records/2026-08-16-01`](records/2026-08-16-01-simplified-skill-reapplication-result.md), v3 당시 평가는 [`records/2026-08-16-02`](records/2026-08-16-02-semantic-content-closure-correction-and-v3-forward-test.md), omission loophole 교정은 [`records/2026-08-16-03`](records/2026-08-16-03-project-context-owner-omission-loophole-correction.md)에서 확인한다. 앞선 판단은 당시 상태 그대로 보존한다.
