# Simplified skill blind 재적용

## 목적과 경계

2026-08-16에 simplified `apply-context-harness`가 과거 application Workspace의 답을 받지 않고도 기존 Payment recovery Project에서 첫 Workspace 장면과 검증 closure를 구성할 수 있는지 새 격리 target에서 평가했다.

- 독립 task thread: `01a00054-46b1-7a90-b4f1-1cbf1f49de2c`
- 모델: `gpt-5.6-terra`
- Target: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v2`
- Target branch: `codex/context-harness-skill-test-v2`
- Target baseline/HEAD: `527af898b114902ebc3f027c5bd09397949da1d3`
- Live Reference commit: `7793babc81f80562d677438a9190abebe182faed`

초기 prompt에는 simplified skill 호출, target 경로, 첫 Workspace 장면, 과거 application Workspace를 읽지 말라는 경계만 제공했다. Source checkout에는 uncommitted simplified skill 문서와 Workspace 004 문서가 있었지만 live Reference의 tracked Harness만 payload로 사용했고 그 uncommitted 문서는 target payload에서 제외했다. 이 평가는 같은 Payment Project의 새 사본에 대한 재적용이며 서로 다른 Project portability 시험이 아니다.

## 적용 순서

1. 독립 task는 target preflight를 수행했다. Baseline working tree는 clean이었고 기존 instruction file은 없었다. 보존 copy SHA-256은 `8a1bc85c8880c06173a9c5cea70d5762d538a3818caab18f370b897d8411f27b`다.
2. 첫 manifest는 사용자 approval 전에 중단해 target write를 `0`으로 유지했다.
3. Main은 manifest를 승인하면서 selected output, claim, canonical basis, Verify, evidence closure를 target task graph에서 다시 닫도록 요청했다.
4. 독립 task는 root `AGENTS.md`, `.codex/config.toml`, `context/project/`, `context/work/`, `context/work/workspaces/001-payment-result-recovery/`를 추가했다. Reference sample Workspace, sample 제품 코드·test, 과거 receipt와 과거 application Workspace는 복사하지 않았다.
5. 기존 root `README.md`, `STATUS.md`, `docs/`, `apps/`, `packages/`는 detailed canonical로 유지했고 tracked 제품 파일은 바꾸지 않았다.
6. Target 사람용 적용 기록은 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v2/context/work/workspaces/001-payment-result-recovery/records/2026-08-16-initial-harness-application.md`에 남겼다.

마지막 확인에서 새 non-ignored 파일은 `55`개로 모두 untracked였고 tracked diff와 staged diff는 `0`이었다. Stage·commit·사람 acceptance는 수행하지 않았다.

## Harness와 Recover 검증

Target에 설치된 Harness runtime `22`개는 current Reference의 tracked Harness와 byte-identical했다.

- 독립 task 첫 full Harness run: `45/46`. `test_timeout_covers_descendant_after_group_leader_exits`만 실패했다.
- 독립 task isolated rerun: 통과.
- 독립 task receipt-producing full rerun: `46/46` 통과.
- Main 첫 full Harness run: `45/46`. 같은 test만 실패했다.
- Main 해당 범위 isolated rerun: `5/5` 통과.
- Main 두 번째 full Harness run: `46/46` 통과.
- Ephemeral validation: 독립 task와 main direct에서 각각 `1/1` 통과.

독립 task의 두 번째 full run은 target `records/receipts/harness-tests/`에 durable receipt로 남았다. 그러나 두 실행 주체의 첫 full run에서 같은 descendant PID disappearance timing assertion이 실패했으므로 이 결과를 안정적인 all-green으로 해석하지 않는다. Receipt가 보존하는 마지막 실행의 통과와 반복 timing flake를 함께 유지한다.

Follow-up explicit Recover는 packet schema `6`을 반환했다. Current machine status는 schema `3`, `verification_passed`이고 current receipt freshness는 `fresh`였다. Receipt snapshot의 changed·missing·unavailable은 모두 `0`이었다. Loaded context는 selected current·output·Project context에 한정됐다.

## Product Verify 보정

첫 durable Verify는 `pnpm --filter @payment-recovery/payment-api test`로 API test `5/5`를 통과했다. 이 receipt는 append-only 과거 검증 사건으로 남아 있다.

Independent review는 Workspace의 첫 장면이 Checkout의 결과 불명 안내까지 포함하지만 Verify가 API만 실행한다는 P1을 제기했다. 다음 current Verify로 보정했다.

`pnpm exec vitest run apps/payment-api/src/app.test.ts apps/checkout-web/src/payment-view-model.test.ts`

- 독립 task: `9/9` 통과, current durable receipt 생성
- Main direct rerun: `9/9` 통과
- Snapshot: canonical basis `3`개와 evidence `13`개, 합계 `16`개
- Current status: 보정 receipt를 가리키도록 갱신

이 Verify는 Mock PG 승인 후 응답 유실에서 Payment API가 같은 attempt를 `UNKNOWN → RECONCILING → PAID`로 수렴시키고 provider confirm을 한 번만 호출하며, Checkout view model이 결과 불명 상태에서 재결제를 권하지 않는다는 claim을 직접 실행한다. Independent review P1은 이 보정과 status linkage 확인으로 해결됐다.

## Main 재검증

Main은 local Markdown link, TOML parse와 adapter `config_file` 해석, 새 파일 trailing whitespace, source Reference Harness byte 일치, target tracked·staged diff `0`, 보정 Product Verify `9/9`, 반복 flake 뒤 isolated와 두 번째 full run 통과를 직접 확인했다.

Target root, `apps/payment-api/`, `apps/checkout-web/`, `packages/provider-mock/`에는 ignored `node_modules`가 존재한다. Product receipt는 package·lockfile·선택 source·test bytes를 snapshot하지만 Node/pnpm executable version이나 installed dependency bytes는 snapshot하지 않는다. `.codex/config.toml`의 parse와 adapter 경로 존재는 확인했지만 새 target-scoped Codex task를 통한 role discovery는 실행하지 않았다.

## 증거 상한과 남은 판단

확인된 범위는 승인된 additive manifest의 설치, 기존 detailed canonical과 tracked 제품 파일 보존, 마지막 durable Harness `46/46`, ephemeral validation, Mock PG/in-memory API와 Checkout view-model Product Verify `9/9`, current receipt freshness와 independent review P1 해결이다.

Harness timing test의 매 실행 안정성, 실제 PG sandbox, 영속 DB·동시성·웹훅, Android WebView 앱 복귀, 실제 Checkout 브라우저 화면, 새 target-scoped Maintain role discovery, 사람 acceptance·commit·운영 효과, 서로 다른 Project portability는 증명하지 않는다. Target 설치물을 유지·commit·제거할지와 timing flake를 acceptance 전에 별도 수정할지는 사용자 판단으로 남긴다.
