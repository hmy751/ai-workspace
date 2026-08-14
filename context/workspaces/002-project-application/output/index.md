# Project application output

마지막 갱신: `2026-08-14`

이 파일은 이 Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치를 연결한다. 산출물을 이 폴더에 복제하지 않으며, 상태와 검증 상한은 [`../current/state.md`](../current/state.md)가 소유한다.

## 현재 goal 산출물

### 첫 실제 Project 적용 이력

- 제품 기준 commit: `527af89`
- Harness 적용 snapshot commit: `eaacec7`
- Harness 제거 commit: `9519a43`
- 이 Workspace에서의 역할: 첫 실제 적용물과 검증 증거를 Git 이력에 보존하고, target을 다시 적용 가능한 제품 기준 상태로 되돌린 기록
- 현재 상한: 마지막 직접 확인에서 원본 target에는 Harness와 새 `context/project/`가 설치되어 있지 않았다. 첫 적용의 schema `3` snapshot과 flat receipt는 Git 이력에 보존됐지만, 실제 Project overview·schema `4`·nested receipt 계약의 target 재적용과 사람 acceptance는 확인하지 않았다. 상세 근거는 [첫 적용 기록](../records/2026-08-13-01-payment-recovery-project-application.md), [rollback 기록](../records/2026-08-14-03-context-harness-rollback-for-retest.md), [receipt 계약 기록](../records/2026-08-14-07-target-machine-receipt-boundary-contract.md), [`current/state.md`](../current/state.md)에 있다.

### 반복 적용 절차

- canonical 위치: repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill
- 이 Workspace에서의 역할: 첫 적용에서 추출한 이식 절차와 migration-only helper. 현재 절차는 target 원자료로 실제 `context/project/README.md`·`overview.md`를 구성하고 상세 Owner·충돌 우선순위를 보존하도록 요구한다.
- 현재 상한: 새 Project context와 nested receipt 계약은 source reference의 40개 테스트와 live reference cycle에서 통과했다. Helper 7개는 Python `3.14.3`과 `/usr/bin` Python `3.9.6`에서 각각 통과했지만, 원본·격리 target에는 새 계약을 적용하지 않았다. 상세 근거는 [승격 기록](../records/2026-08-14-01-apply-context-harness-skill-promotion.md), [blind 평가 기록](../records/2026-08-14-04-blind-apply-context-harness-skill-evaluation.md), [receipt 계약 기록](../records/2026-08-14-07-target-machine-receipt-boundary-contract.md)에 있다.

### 격리 blind 평가물

- 평가 target: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`
- 기준: branch `codex/context-harness-skill-test`, HEAD `527af89`
- 마지막 관찰 형태: `AGENTS.md`와 `context/` 44개 파일이 untracked이고 tracked·staged diff는 없었다.
- 이 Workspace에서의 역할: 과거 002 적용 문서를 입력으로 주지 않고 당시 skill의 preflight부터 schema `3` `recover → verify → recover`까지 재현한 평가 증거
- 현재 상한: 당시 자동 검증과 독립 review는 통과했지만 새 실제 `context/project/`·schema `4`·nested receipt 계약의 증거가 아니다. 이번 변경에서도 격리 target을 열지 않았고 commit·staging·사람 acceptance 상태를 갱신하지 않았다. 상세 근거는 [blind 평가 기록](../records/2026-08-14-04-blind-apply-context-harness-skill-evaluation.md)과 [receipt 계약 기록](../records/2026-08-14-07-target-machine-receipt-boundary-contract.md)에 있다.

## 적용 입력

- 실행 가능한 기준 Project의 canonical은 이 저장소의 루트 [`reference-project/`](../../../../reference-project/)다.
- 루트 `reference-project/`는 첫 적용의 입력이며, 대상 Project에 배치된 goal 산출물 자체는 아니다.

이 지도에 commit이 있다는 사실은 현재 설치, Workspace 완료, 사용자 수락 또는 외부 동작 검증을 뜻하지 않는다.
