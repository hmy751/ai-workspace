# Project application memory

마지막 갱신: `2026-08-16`

## 목표

기존 Project의 상세 canonical과 제품 코드를 보존한 채 Project common context, 명시 Workspace, Recover·Maintain·Verify Harness를 추가하고, 사람이 선택한 작업 장면을 필요한 맥락만으로 복구해 검증 결과를 지속 상태와 append-only receipt로 다시 연결할 수 있는지 확인한다.

## 대상 구분

- 원본 target `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`는 첫 적용과 rollback의 이력을 소유한다. 마지막 직접 확인에서는 Harness가 제거된 commit `9519a43`이었으며 제품 기준은 `527af89`와 같았다. 2026-08-16 재적용 대상이 아니다.
- 과거 blind target `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`는 이전 schema와 flat receipt 계약을 평가한 증거다. 새 계약이나 현재 simplified skill의 증거로 승격하지 않는다.
- v2 target `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v2`는 이식 실행과 Verify closure는 확인했지만 Project common context가 기존 문서 링크형·Workspace 요약형에 가까워 완전 성공으로 보지 않는다.
- v3 target `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3`는 link-only 문제는 개선했지만 독립된 공통 제품 기준과 채택 결정을 가진 `prd.md`·`decisions/` Owner를 생략했다. Project common context 이식 완료나 content closure 통과 증거가 아니다.

## 지속 기준

- 기존 root `README.md`, `STATUS.md`, `docs/`, `apps/`, `packages/`와 제품 test는 상세 canonical로 남긴다. `context/project/`는 링크 목록이나 한 Workspace 요약이 아니라 여러 Workspace가 직접 판단할 내용을 실제로 담아야 한다. 구분되는 공통 제품 기준·구조·채택 결정이 원자료에 있으면 overview에 억지로 합치지 말고 대응하는 Project context Owner를 구성한다. Owner 생략은 독립된 공통 내용이 없음을 원자료로 확인하고 manifest와 application record에 근거를 남길 때만 허용한다. Overview는 모든 내용을 합친 문서가 아니라 진입 요약이다.
- 적용 전에는 target HEAD·working tree·instruction file 존재 여부를 preflight로 고정한다. 승인된 manifest만 추가하고 tracked 제품 파일을 바꾸지 않는다.
- Workspace의 selected current·output·Project context만 Recover 입력으로 읽는다. Source 전체, 과거 records 본문, 다른 Workspace를 자동으로 로드하지 않는다.
- Product Verify의 claim, canonical basis, 명령, evidence snapshot은 대상 작업 장면 안에서 함께 닫는다. 더 좁은 과거 receipt는 덮어쓰지 않고 append-only 사건으로 남기며 machine status만 current receipt를 가리킨다.
- 사람용 적용 기록은 target Workspace `records/`가, 기계 JSON은 `records/receipts/{preflight,harness-tests,verify}/`가 소유한다. Harness와 helper는 생성 주체일 뿐 의미와 수명주기 Owner가 아니다.
- 설치, staging, commit, 자동 검증, 사람 acceptance를 서로 다른 상태로 취급한다. 자동 검증 통과만으로 이식 acceptance나 Workspace 완료를 선언하지 않는다.

## 검증 상한

- V3의 과거 자동 검증은 Harness와 제품 task graph 실행 증거로는 유지되지만 Project common context content closure를 증명하지 않는다. 최신 Owner closure 규칙은 skill에 반영됐으나 아직 target 재적용·재시험 증거가 없다.
- 실제 PG sandbox, 영속 DB·동시성·웹훅, Android WebView 앱 복귀, 실제 Checkout 브라우저 화면, 사람 acceptance와 운영 효과는 증명하지 않는다.
- Product receipt는 선택된 package·lockfile·source·test bytes를 보존하지만 Node/pnpm executable version과 ignored installed dependency bytes는 보존하지 않는다.
- Target `.codex/config.toml`의 parse와 adapter 경로 존재는 확인했지만 새 target-scoped Codex task에서 실제 role discovery를 실행하지 않았다.
- 동일한 descendant-process timing test가 독립 task와 main의 첫 전체 실행에서 각각 한 번 실패하고 isolated/full rerun에서 통과했다. 현재 green receipt는 유효하지만 반복 가능한 무결함을 증명하지 않는다.

## 접근점

- 첫 실제 적용 기록: [`2026-08-13-01-payment-recovery-project-application.md`](../records/2026-08-13-01-payment-recovery-project-application.md)
- 과거 blind 평가 기록: [`2026-08-14-04-blind-apply-context-harness-skill-evaluation.md`](../records/2026-08-14-04-blind-apply-context-harness-skill-evaluation.md)
- v2 재적용과 당시 상한: [`2026-08-16-01-simplified-skill-blind-reapplication.md`](../records/2026-08-16-01-simplified-skill-blind-reapplication.md)
- 사용자 정정과 v3 forward test: [`2026-08-16-02-project-common-context-correction-and-v3-forward-test.md`](../records/2026-08-16-02-project-common-context-correction-and-v3-forward-test.md)
- v3 Owner 누락과 skill 재보강: [`2026-08-16-03-project-context-owner-closure-correction.md`](../records/2026-08-16-03-project-context-owner-closure-correction.md)
- v3 target 적용 기록: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3/context/work/workspaces/001-payment-result-recovery/records/2026-08-16-01-context-harness-application.md`
- v3 독립 task thread: `01a009d3-5128-70a2-8ba3-591bcf62b1fe`
