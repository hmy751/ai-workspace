# Records

이 폴더에는 실제 Project 적용 작업에서 만든 지속 가능한 분석, migration 결정, 시도, 실패, 검증 결과를 누적한다. 여기에 있다는 이유만으로 현재 유효하거나 채택된 결론이라는 뜻은 아니다.

- 파일명은 `YYYY-MM-DD-NN-주제.md` 형식을 사용한다.
- 상세 과정과 근거는 records에 남기고, 지금도 유효한 기준은 `../current/memory.md`, 이어 갈 상태는 `../current/state.md`에 압축한다.
- 대상 Project의 원문이나 파일을 무조건 복제하지 않는다. live 경로를 참조할지 snapshot을 보존할지 먼저 provenance와 변경 가능성을 판단한다.
- 다른 Workspace의 records를 이곳에 복사하지 않고 필요한 결론과 접근점만 current에서 가리킨다.
- 이 폴더는 적용 작업을 사람이 다시 판단할 날짜별 records를 소유한다. Target에서 기계가 만든 receipt는 해당 target Workspace의 `records/receipts/<종류>/`가 소유하며 이곳에 복제하지 않는다.

## 기록

- [`2026-08-13-01-payment-recovery-project-application.md`](2026-08-13-01-payment-recovery-project-application.md): 첫 실제 Project의 배치 변경, recover·verify 시도, durable 증거 보강과 검증 상한
- [`2026-08-14-01-apply-context-harness-skill-promotion.md`](2026-08-14-01-apply-context-harness-skill-promotion.md): 첫 적용에서 반복 절차로 승격한 역할 분리, helper 계약, 검증과 portability 상한
- [`2026-08-14-02-workspace-output-map.md`](2026-08-14-02-workspace-output-map.md): Workspace goal 산출물과 실제 canonical 위치를 복제 없이 연결한 구조 결정
- [`2026-08-14-03-context-harness-rollback-for-retest.md`](2026-08-14-03-context-harness-rollback-for-retest.md): 제품 변경과 적용 snapshot을 commit으로 분리하고 reset 없이 Harness를 제거한 재테스트 기준점
- [`2026-08-14-04-blind-apply-context-harness-skill-evaluation.md`](2026-08-14-04-blind-apply-context-harness-skill-evaluation.md): 과거 002 문서를 차단한 격리 사본에서 당시 schema `3` skill의 end-to-end 이식과 독립 재검증을 수행한 결과
- [`2026-08-14-05-project-common-context-contract.md`](2026-08-14-05-project-common-context-contract.md): 실제 Project common context 최소층과 overview-first recover 계약으로 바꾼 이유, source reference 검증과 target 미검증 경계
- [`2026-08-14-06-reference-project-root-rename.md`](2026-08-14-06-reference-project-root-rename.md): 루트 `output/`을 `reference-project/`로 바꿔 Workspace output과 기준 Project 책임을 구분한 결정, skill source lookup 변경과 target 미검증 경계
- [`2026-08-14-07-target-machine-receipt-boundary-contract.md`](2026-08-14-07-target-machine-receipt-boundary-contract.md): 새 target의 종류별 machine receipt 배치, producer·Owner 경계, 직접 test와 durable verify 구분, 기존 Payment target 미적용 상한
- [`2026-08-16-01-simplified-skill-blind-reapplication.md`](2026-08-16-01-simplified-skill-blind-reapplication.md): simplified skill을 새 격리 target에 과거 application Workspace 없이 재적용한 순서, 보정 Verify, 반복 timing flake, main 재검증과 proof ceiling
- [`2026-08-16-02-project-common-context-correction-and-v3-forward-test.md`](2026-08-16-02-project-common-context-correction-and-v3-forward-test.md): v2 Project common context 결함에 대한 사용자 정정, 내용 충족 검사 보정, v3 blind forward test와 남은 proof ceiling
- [`2026-08-16-03-project-context-owner-closure-correction.md`](2026-08-16-03-project-context-owner-closure-correction.md): v3에서 독립된 공통 제품 기준·결정 Owner가 누락된 사용자 정정, skill 재보강과 미재시험·target 미보정 상태
