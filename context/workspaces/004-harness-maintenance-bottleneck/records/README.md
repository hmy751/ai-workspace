# Records

이 폴더에는 context+harness 유지보수 병목을 분석하며 만든 지속 가능한 관찰, 후보, 비교, 결정, 실험과 검증 기록을 누적한다. 여기에 있다는 이유만으로 현재 채택된 개선안이라는 뜻은 아니다.

- 파일명은 `YYYY-MM-DD-NN-주제.md` 형식을 사용한다.
- 시간 추정과 실제 계측을 구분한다.
- 안전 계약을 줄이는 것과 중복 설명·불필요한 순차 작업을 줄이는 것을 혼동하지 않는다.
- 다른 Workspace의 historical record를 현재 결론에 맞춰 다시 쓰지 않는다.
- 현재 채택된 기준은 `../current/memory.md`, 이어 갈 문제와 다음 행동은 `../current/state.md`, 선택된 결과는 `../output/index.md`에 압축한다.

## 기록

- [`2026-08-14-01-workspace-creation-and-problem-frame.md`](2026-08-14-01-workspace-creation-and-problem-frame.md): 새 Workspace 생성 결정, 직전 작업에서 확인한 병목과 분석 시작점
- [`2026-08-14-02-recover-verify-purpose-and-activation-hypotheses.md`](2026-08-14-02-recover-verify-purpose-and-activation-hypotheses.md): Harness 원래 목적, 현재 Recover·verify 구현 방법, 활성 시점별 책임 분리 가설과 미결정 범위
- [`2026-08-14-03-harness-responsibilities-actors-and-implementation-layers.md`](2026-08-14-03-harness-responsibilities-actors-and-implementation-layers.md): Recover·Maintain·Verify·Handoff·Harness check의 현재 사실, 책임·활성 시점·주체·구현 층위 후보와 미결정 범위
- [`2026-08-14-04-current-scope-and-maintain-boundary-correction.md`](2026-08-14-04-current-scope-and-maintain-boundary-correction.md): 현재 분석 대상을 Reference Recover·Verify로 좁히고 Maintain 책임과 outer repo-local agent를 분리한 사용자 정정
- [`2026-08-14-05-reference-recover-verify-implementation-and-verification.md`](2026-08-14-05-reference-recover-verify-implementation-and-verification.md): Maintain이 설명에만 있던 당시 Reference 구현·검증과 이후 철회된 완료 판단
- [`2026-08-14-06-reference-maintain-structural-correction-and-verification.md`](2026-08-14-06-reference-maintain-structural-correction-and-verification.md): 사용자 완료 거절 뒤 Maintain 구조를 교정한 책임 계층, review 수정, 최종 검증과 proof ceiling
- [`2026-08-14-07-reference-maintain-agent-colocation-and-registration.md`](2026-08-14-07-reference-maintain-agent-colocation-and-registration.md): Maintain agent 정의를 책임 디렉터리에 두고 root 설정은 발견 등록만 맡긴 사용자 결정과 확인 범위
- [`2026-08-14-08-apply-context-harness-simplification-and-verification.md`](2026-08-14-08-apply-context-harness-simplification-and-verification.md): Reference 실행 계약과 이식 절차의 중복 소유를 줄인 skill 간소화, forward preflight, review와 proof ceiling
- [`2026-08-16-01-simplified-skill-reapplication-result.md`](2026-08-16-01-simplified-skill-reapplication-result.md): 같은 Payment target blind 재적용에서 확인한 skill 중복 제거 효과, 위험 기반 review의 P1 발견, reporting 보완과 proof ceiling
- [`2026-08-16-02-semantic-content-closure-correction-and-v3-forward-test.md`](2026-08-16-02-semantic-content-closure-correction-and-v3-forward-test.md): v2의 Project common context 의미 결함, skill의 semantic content closure 보강, blind v3에서의 해소와 proof ceiling
- [`2026-08-16-03-project-context-owner-omission-loophole-correction.md`](2026-08-16-03-project-context-owner-omission-loophole-correction.md): v3의 PRD·decision Owner omission loophole, 책임별 Owner closure 규칙 보강과 미재시험 상태
