# Project common context 보정과 v3 forward test

## 정정 배경

V2 blind reapplication은 Harness 이식, selected output, Verify claim과 evidence closure를 만들었지만 사용자 검토에서 Project common context가 기존 PRD·architecture 링크형과 첫 Workspace 요약형에 가까워 완전한 적용 성공이 아니라는 결함이 확인됐다.

이 정정은 v2의 실행·검증 사건을 없애지 않는다. [v2 기록](2026-08-16-01-simplified-skill-blind-reapplication.md)은 당시 사실로 유지하고, common context 의미 충족 실패와 후속 보정은 이 기록에서 이어서 보존한다.

Main은 `apply-context-harness`에 링크 목록이나 Workspace 요약만으로 Project common context를 통과시키지 않는 내용 충족 검사를 추가했다. 요구한 내용은 여러 Workspace가 직접 판단할 사용자 장면, 현재 구현·미구현 범위, 공통 성공과 검증 경계, 구조·권한·흐름·불변성이다. 기존 canonical을 대체하거나 그대로 복제하지 않는 경계는 유지했다.

## 독립 forward test

- 독립 task thread: `01a009d3-5128-70a2-8ba3-591bcf62b1fe`
- 모델: `gpt-5.6-terra`
- Target: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3`
- Target branch: `codex/context-harness-skill-test-v3`
- Target baseline/HEAD: `527af898b114902ebc3f027c5bd09397949da1d3`
- Source Reference: `7793babc81f80562d677438a9190abebe182faed`

Terra에는 과거 application Workspace, v2 결과, 발견된 결함의 정답을 제공하지 않았다. 같은 Payment Project의 새 격리 사본에서 현재 skill과 live Reference를 사용해 적용하게 했다.

Target에는 root routing, Codex Maintain adapter, Project·Work context, 첫 Workspace와 Harness를 합쳐 non-ignored 파일 `55`개가 추가됐다. 모두 untracked이며 tracked·staged 제품 변경은 `0`이다. 기존 `README.md`, `STATUS.md`, `docs/`, `apps/`, `packages/`는 상세 canonical로 유지했다. Stage·commit·사람 acceptance는 수행하지 않았다.

Target 사람용 적용·검증 기록은 다음에 있다.

- `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3/context/work/workspaces/001-payment-result-recovery/records/2026-08-16-01-context-harness-application.md`
- `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3/context/work/workspaces/001-payment-result-recovery/records/2026-08-16-02-install-validation-and-verify.md`

## Project common context 결과

V3는 `context/project/`에 `README.md`, `overview.md`, `architecture.md`만 만들었다.

- `overview.md`: 외부 결제 앱 인증 뒤 승인 응답 유실·복귀 지연이라는 사용자 장면, 동일 `PaymentAttempt` 복구 목적, 현재 Node.js·pnpm local Mock PG MVP, 실제 PG·DB·webhook·Android WebView·배포의 미구현 범위, 자동 검증과 사람 acceptance 경계를 자체 내용으로 설명한다.
- `architecture.md`: Checkout·상점 API·PG·native host의 권한, `CONFIRMING → UNKNOWN → RECONCILING → PAID` 복구 흐름, package별 책임, transaction과 terminal-state 불변성, root Product Verify 경로와 증명 한계를 자체 내용으로 설명한다.
- 기존 docs를 내용 대신 가리키지 않고, 첫 Workspace의 일시 상태를 Project 전체 설명으로 올리지 않았다.

이 결과는 새 내용 충족 검사와 main의 source·target 대조를 통과했다. 다만 같은 Payment Project에서 만든 forward test이므로 모든 Project에서 의미 충족을 보장하지 않는다.

## 검증 결과

### Product Verify와 Recover

Terra가 durable Product Verify로 실행한 고정 argv는 다음과 같다.

`pnpm exec turbo run typecheck test build --force`

- Turbo task `11/11` 성공
- Receipt snapshot: canonical basis `2`개, evidence `33`개, 합계 `35`개
- 후속 Recover packet schema `6`
- Current status schema `3`, `verification_passed`
- Current receipt freshness `fresh`
- Snapshot changed·missing·unavailable 모두 `0`

Main의 direct Product task도 같은 argv에서 `11/11` 성공했다.

### Harness timing flake

- Terra 첫 full run: `45/46`, `test_timeout_covers_descendant_after_group_leader_exits` 실패
- Terra 두 번째 full run: `46/46` 통과
- Main 첫 direct full run: `45/46`, 같은 test 실패
- Main isolated 동일 범위: `5/5` 통과
- Main 두 번째 direct full run: `46/46` 통과

V2에 이어 v3에서도 두 실행 주체의 첫 full run이 같은 descendant timeout race로 실패했다. 마지막 green run은 사실이지만 안정적인 all-green이나 flake 해소를 뜻하지 않는다.

### Main과 independent review

Main은 target local link issue `0`, tracked·staged 제품 diff `0`, whitespace 검사를 확인했다. Independent review의 P1은 `0`이었다. Reference sample routing 문구가 남은 P2는 target Workspace와 Project root를 가리키도록 적응했다.

## 현재 해석과 proof ceiling

V3는 v2에서 빠졌던 Project common context 자체 내용을 현재 skill이 같은 Payment target에서 다시 구성하고, 기존 detailed canonical을 보존한 채 root Product task와 Recover freshness를 닫을 수 있음을 보여 준다.

다음은 아직 증명하지 않는다.

- descendant timeout test의 반복 안정성
- 서로 다른 구조와 canonical을 가진 Project에서의 portability
- 실제 PG sandbox, 영속 DB·동시성·webhook
- Android WebView 앱 복귀와 실제 browser 수동 흐름
- 사람 acceptance, commit, 운영 효과

따라서 현재 결과는 내용 보정 뒤 forward test 통과이지 범용 적용 완료나 target acceptance가 아니다.
