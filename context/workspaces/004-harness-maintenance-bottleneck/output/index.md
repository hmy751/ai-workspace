# Harness maintenance bottleneck output

마지막 갱신: `2026-08-16`

## Workspace goal

Context+harness의 안전성과 재진입 가능성을 유지하면서, Reference 실행 책임과 target 이식 절차의 중복 소유 및 반복 검증 병목을 줄인다.

## 현재 선택된 산출물

### Committed Reference

- [`Harness 책임과 실행 경계`](../../../../reference-project/context/work/harness/README.md): Recover·Maintain·Verify와 Harness validation의 관계
- [`Recover 계약과 구현`](../../../../reference-project/context/work/harness/recover/): explicit Workspace 선택, read-only recovery, verification snapshot freshness
- [`Maintain 계약`](../../../../reference-project/context/work/harness/maintain/): 자연스러운 의미 변화 경계, 기존 Context Owner routing, main 검토와 비소유 범위
- [`Reference Maintain agent`](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml): Maintain 계약과 같은 책임 디렉터리에 둔 교체 가능한 Codex 실행 장치
- [`Project agent 등록`](../../../../reference-project/.codex/config.toml): 하위 Maintain agent 정의의 발견 경로만 등록하는 Project 설정
- [`Work 운영 규칙`](../../../../reference-project/context/work/AGENTS.md): Work·Harness 작업 지침과 Maintain agent 호출·main 검토 routing
- [`Verify 계약과 구현`](../../../../reference-project/context/work/harness/verify/): claim·canonical basis·evidence snapshot과 durable machine receipt
- [`Harness validation`](../../../../reference-project/context/work/harness/validation/): checked-in 제품 상태를 바꾸지 않는 ephemeral `recover → verify → recover` 회귀 검사

이 Reference 결과는 commits `638bfbc`, `7793bab`에 보존됐다.

### Skill simplification and Project context Owner closure

- [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/SKILL.md): live Reference를 이식하며 target의 구분되는 공통 책임별 Project context Owner와 근거 있는 omission을 구성·보고하는 절차
- [`Application contract`](../../../../.agents/skills/apply-context-harness/references/application-contract.md): overview 합본을 막고 책임별 Owner closure, omission 근거, 충돌과 evidence closure를 판단하는 기준
- [`Repo-local skill index`](../../../../.agents/skills/README.md): Reference와 이식 절차의 분리된 역할

Reference 교정과 proof ceiling은 [`2026-08-14-06`](../records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md), agent 배치와 등록은 [`2026-08-14-07`](../records/2026-08-14-07-reference-maintain-agent-colocation-and-registration.md), skill 간소화와 forward 검증은 [`2026-08-14-08`](../records/2026-08-14-08-apply-context-harness-simplification-and-verification.md)에 있다. V2 당시 평가는 [`2026-08-16-01`](../records/2026-08-16-01-simplified-skill-reapplication-result.md), v3 당시 평가는 [`2026-08-16-02`](../records/2026-08-16-02-semantic-content-closure-correction-and-v3-forward-test.md), 현재 Owner omission 교정은 [`2026-08-16-03`](../records/2026-08-16-03-project-context-owner-omission-loophole-correction.md)에 있다. 상세 근거는 [`Workspace 002 correction record`](../../002-project-application/records/2026-08-16-03-project-context-owner-closure-correction.md)가 소유한다. 최신 skill은 Git history에 보존됐지만 재시험·사람 acceptance 전이며, 이 Workspace는 target 산출물을 복제하지 않는다.
