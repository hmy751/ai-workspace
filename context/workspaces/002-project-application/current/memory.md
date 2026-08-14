# Project application memory

마지막 갱신: `2026-08-14`

## 목표

실제 기존 Project 하나에서 사람과 AI가 Project 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 다시 지속 상태에 반영하는 흐름을 적용·검증한다.

## 대상과 적용 결정

- 적용 기준은 이 저장소의 [`reference-project/`](../../../../reference-project/)이고, 대상 Project는 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`다.
- 완료된 target에는 실제 내용의 `context/project/README.md`와 `context/project/overview.md`가 Project common context의 최소 진입점으로 있어야 한다. README는 이 층의 책임·상세 Owner·충돌 우선순위·갱신 조건을, overview는 여러 Workspace에 공통으로 필요한 목적·범위·구조·제약·채택 결정·검증 경계를 target 사실로 구성한다.
- 대상의 기존 `README.md`, `docs/product-brief.md`, `docs/architecture.md`, `docs/failure-scenarios.md`, `docs/roadmap.md`, `STATUS.md`, 코드와 테스트는 상세 사실의 domain canonical로 보존한다. `context/project/overview.md`는 이들을 복제하거나 링크만 나열하지 않으며, 충돌하면 상세 Owner를 우선하고 overview를 stale로 판정해 다시 대조한다. 기존 Owner 자체를 옮기는 것은 별도 승인 대상이다.
- 첫 적용에서는 repo-local `AGENTS.md`, `context/README.md`, 교체 가능한 `context/work/harness/`, `context/work/workspaces/001-payment-recovery-mvp/`를 배치했다. 이 상태는 target commit `eaacec7`에 보존했다.
- 첫 적용의 recover schema `3`은 Project-root 상대 경로 중 루트 `README.md`, `STATUS.md`, `docs/` 아래 Markdown을 직접 선택한 target-local 과거 계약이다. 새 target에 재사용하거나 새 계약 검증으로 해석하지 않는다.
- Fresh target의 recover schema `4`는 `context/project/` 아래 regular Markdown만 허용하고 `context/project/overview.md`를 첫 항목으로 요구한다. Recovery packet shape는 바뀌지 않아 packet schema `5`를 유지한다.
- 적용 전 사용자 작업 `App.tsx`, `styles.css`는 Harness와 분리해 target commit `527af89`에 보존했다. 적용 전 존재하던 untracked `context/code-map.md`는 사용자가 적용 진행 중 직접 삭제했으며 rollback에서도 복원하지 않았다.
- 현재 target에서는 `git reset` 없이 commit `9519a43`으로 Harness 적용 commit을 되돌렸다. `AGENTS.md`와 `context/`는 없고 Harness용 `.gitignore` 변경도 사라졌으며, 제품 tree는 `527af89`와 같다.
- `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`는 schema `3`과 기존 문서 직접 선택 계약 당시 skill을 blind 평가한 격리 사본이다. 새 Project context·schema `4` 계약, 원본 target이나 accepted canonical을 대신하지 않는다.
- Harness가 없어져도 기존 Project canonical과 Workspace의 README·current·records 의미가 남아야 한다.

## 반복 적용 절차

- [`reference-project/`](../../../../reference-project/)는 실제 `context/project/`와 Work Harness 관계를 보여 주는 실행 가능한 기준 Project, repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill은 target 원자료에서 실제 Project common context를 구성하는 이식 절차와 migration-only helper, 이 Workspace의 records는 실제 적용 결과와 예외를 소유한다.
- helper는 이식 전에 target 상태를 관찰·보존하고 target-specific Harness test receipt를 만드는 장치다. 제품 runtime이나 범용 설치 payload가 아니며 target에 복제하지 않는다.
- 이 절차는 `AGENTS.md`가 대상 Project 경로가 포함된 이식 요청에만 routing한다. 이 저장소의 `reference-project/`, Workspace, context maintainer와 결합된 절차여서 global skill로 등록하지 않았다.

## 검증 상한

- 구조와 선택적 복구, 고정 typecheck·test·Checkout build, receipt 누적, machine status 갱신과 후속 재복구까지 확인했다.
- Harness 계약 22개 통과는 실행 전 Python source 14개의 SHA-256·byte size와 함께 별도 receipt에 보존됐다. 제품 고정 검증은 실제 Turbo 대상 5개 package의 source·manifest·설정과 root 실행 설정 40개의 실행 전 hash를 포함한다. 이로써 Harness source와 고정 검증 입력에 대한 durable 증거 부족은 해소됐다.
- 최종 자동 검증 통과는 로컬 Mock PG vertical slice의 고정 evidence snapshot에 한정된다. 실제 브라우저 승인·취소·focus 복귀·모바일 표시, 실제 PG·영속 DB·Android WebView·웹훅·운영 효과, 사람의 acceptance는 증명하지 않는다.
- 자동 검증 통과 상태 `verified_waiting_acceptance`는 Workspace 완료나 사용자 수락을 뜻하지 않는다.
- 새 계약의 source reference에서는 전체 37개 테스트와 `recover → verify → recover` live cycle을 확인했다. 최신 verify receipt는 제품 테스트 7개 통과를 보존하고, 후속 recover는 `overview.md`를 첫 Project context로 읽어 packet schema `5`를 반환했다.
- 격리 사본의 blind end-to-end 자동 검증은 schema `3`과 기존 문서 직접 선택 계약에 대한 과거 결과다. 새 `context/project/`·schema `4`의 실제 target 이식, 원본 설치·commit·사람 acceptance·다른 Project portability는 증명하지 않는다.

## 접근점

- 이 Workspace의 상세 적용·검증 기록: [`2026-08-13-01-payment-recovery-project-application.md`](../records/2026-08-13-01-payment-recovery-project-application.md)
- 반복 절차 승격과 검증 기록: [`2026-08-14-01-apply-context-harness-skill-promotion.md`](../records/2026-08-14-01-apply-context-harness-skill-promotion.md)
- target 적용 snapshot commit: `eaacec7`
- target rollback commit: `9519a43`
- target 제품 기준 commit: `527af89`
- 재테스트 준비 rollback 기록: [`2026-08-14-03-context-harness-rollback-for-retest.md`](../records/2026-08-14-03-context-harness-rollback-for-retest.md)
- blind skill 평가 기록: [`2026-08-14-04-blind-apply-context-harness-skill-evaluation.md`](../records/2026-08-14-04-blind-apply-context-harness-skill-evaluation.md)
- Project common context·recover 계약 변경 기록: [`2026-08-14-05-project-common-context-contract.md`](../records/2026-08-14-05-project-common-context-contract.md)
- 기준 Project 루트 이름 변경 기록: [`2026-08-14-06-reference-project-root-rename.md`](../records/2026-08-14-06-reference-project-root-rename.md)
