# Project application output

마지막 갱신: `2026-08-16`

이 파일은 이 Workspace goal의 적용 결과와 실제 canonical 위치를 연결한다. 산출물을 이 폴더에 복제하지 않으며, 현재 상태와 proof ceiling은 [`../current/state.md`](../current/state.md)가 소유한다.

## 현재 선택된 절차 상태

- 절차 canonical: repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill
- 현재 변경: 구분되는 공통 제품 기준·구조·채택 결정을 overview에 합치거나 생략하지 않고 대응 Project context Owner로 구성하며, 생략 시 원자료 근거를 manifest와 application record에 남기도록 보강
- 검증 상태: 이 재보강 뒤 blind reapplication이나 target 검증은 수행하지 않았다.

## 최신 target 결과와 미완료 경계

### V3 forward test

- Target: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3`
- Branch와 baseline/HEAD: `codex/context-harness-skill-test-v3`, `527af898b114902ebc3f027c5bd09397949da1d3`
- Target Workspace: `context/work/workspaces/001-payment-result-recovery/`
- Project common context: `context/project/README.md`, `context/project/overview.md`, `context/project/architecture.md`
- Target 적용·검증 기록: `context/work/workspaces/001-payment-result-recovery/records/2026-08-16-01-context-harness-application.md`, `2026-08-16-02-install-validation-and-verify.md`
- 이 Workspace에서의 역할: link-only 문제 개선과 당시 실행·검증 사실을 보존하는 과거 forward-test 결과
- 현재 상한: `README.md`, `overview.md`, `architecture.md`만 만들고 원자료의 독립된 공통 제품 기준과 채택 결정에 대응하는 `prd.md`·`decisions/` Owner를 생략했다. 따라서 Project common context 이식 완료나 content closure 통과로 보지 않는다. Target은 미보정·untracked 상태이고 새 규칙 재시험도 없다. 상세는 [최신 정정 기록](../records/2026-08-16-03-project-context-owner-closure-correction.md)에 있다.

## 구분해서 보존하는 이전 결과

### Simplified-skill v2 재적용

- Target: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v2`
- Branch와 baseline/HEAD: `codex/context-harness-skill-test-v2`, `527af898b114902ebc3f027c5bd09397949da1d3`
- Target Workspace: `context/work/workspaces/001-payment-result-recovery/`
- 사람용 적용 기록: `context/work/workspaces/001-payment-result-recovery/records/2026-08-16-initial-harness-application.md`
- 이 Workspace에서의 역할: 과거 application Workspace 없이 이식과 Verify closure를 재구성한 실행 증거
- 현재 상한: Harness와 Product Verify는 통과했지만 Project common context가 기존 문서 링크형·첫 Workspace 요약형에 가까워 완전 성공으로 보지 않는다. 상세는 [v2 기록](../records/2026-08-16-01-simplified-skill-blind-reapplication.md)과 [v3 correction 기록](../records/2026-08-16-02-project-common-context-correction-and-v3-forward-test.md)에 있다.

### 원본 Project 첫 적용

- Target: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`
- 제품 기준 commit `527af89`, Harness 적용 snapshot `eaacec7`, Harness 제거 commit `9519a43`
- 역할: 첫 실제 적용과 rollback을 Git 이력에 보존한 증거
- 현재 상한: 마지막 직접 확인에서 Harness 미설치 상태였으며 이번 v2 재적용 대상이 아니다. 상세 근거는 [첫 적용 기록](../records/2026-08-13-01-payment-recovery-project-application.md)과 [rollback 기록](../records/2026-08-14-03-context-harness-rollback-for-retest.md)에 있다.

### 과거 blind 평가

- Target: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`
- Branch와 baseline/HEAD: `codex/context-harness-skill-test`, `527af89`
- 역할: 당시 schema `3`과 기존 문서 직접 선택·flat receipt 계약을 과거 application Workspace 입력 없이 재현한 증거
- 현재 상한: 현재 simplified skill·v2 schema·nested receipt의 증거가 아니다. 상세 근거는 [과거 blind 평가 기록](../records/2026-08-14-04-blind-apply-context-harness-skill-evaluation.md)에 있다.

## 적용 입력 이력

- 실행 기준 Project: 루트 [`reference-project/`](../../../../reference-project/)
- V2와 v3가 사용한 live Reference commit: `7793babc81f80562d677438a9190abebe182faed`
- 현재 source 상태 상한: 내용 충족과 책임별 Owner closure를 포함한 skill source 문서는 이 Workspace 기록과 함께 Git history에 보존됐다. V3 payload의 Harness runtime은 위 commit의 tracked Reference를 사용했고 skill 절차는 당시 main의 수정본을 사용했다. 최신 Owner closure 규칙은 아직 target에 재시험하지 않았다.

이 지도는 현재 설치·commit·Workspace 완료·사용자 수락·외부 시스템 동작을 선언하지 않는다.
