# Project application state

마지막 갱신: `2026-08-14`

## 현재 문제

원본 target은 Harness 미설치 상태로 보존하면서, 격리 사본에서 완료한 blind skill 평가의 상한과 아직 필요한 사람 판단을 분리해야 한다.

## 현재 상태

- 대상 Project는 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`, branch는 `feat/payment-recovery-mvp`, 현재 HEAD는 `9519a43`이고 working tree는 clean이다.
- 기존 사용자 제품 변경 `App.tsx`, `styles.css`는 `527af89`에 별도로 커밋했다.
- 첫 Harness 적용 전체는 `eaacec7`에 snapshot으로 남겼다. 당시 Harness 계약 22개, 제품 Turbo 11개 task와 31개 test, Checkout build가 통과했고 상세 증거는 [적용·검증 기록](../records/2026-08-13-01-payment-recovery-project-application.md)에 있다.
- `git reset`을 사용하지 않고 `9519a43`에서 `eaacec7`을 revert했다. 현재 target에는 `AGENTS.md`, `context/`, Harness용 `.gitignore` 변경이 없다.
- 현재 HEAD의 tree는 Harness 적용 직전 제품 commit `527af89`와 완전히 같다. `git diff --exit-code 527af89 HEAD`가 `0`을 반환했다.
- rollback 후 Harness 밖에서 동일한 `pnpm exec turbo run typecheck test build --force`를 실행해 cache 없이 11개 task, 31개 test, typecheck와 Checkout production build가 다시 통과했다.
- 첫 적용에서 승격한 repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill에는 이후 Workspace source/output/minimum-memory 계약도 반영됐지만, 이 최신 계약은 현재 target에 아직 재적용하지 않았다.
- 격리 평가 target은 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`, branch `codex/context-harness-skill-test`, HEAD `527af89`다. 원본 002 current·records·output을 읽지 못하게 한 prompt에서 skill 이름·target 경로·첫 장면만 받고 별도 task `019ffec6-7cad-7120-b803-a6f4ef6787f3`가 이식을 수행했다.
- 격리 평가에서는 preflight·dry-run·target adaptation 뒤 첫 verify가 `node_modules` 부재로 실패했고, offline frozen install 후 verify 통과와 후속 recover까지 완료했다. 별도 독립 review와 main 재검증도 통과했다.
- 격리 target에는 `AGENTS.md`와 `context/` 44개 설치 파일이 untracked 상태로 남아 있다. tracked diff와 staged diff는 없고 commit·staging·사람 acceptance는 수행하지 않았다.
- main 재검증은 preflight 원본·사본 SHA 일치, recover의 정확한 10개 경로, Harness source 14개와 test 28개의 receipt, 제품 evidence 36개 hash와 status linkage를 확인했다. direct Harness 28개 test와 제품 Turbo 11/11 task·31개 test·build도 cache `0`으로 통과했고 독립 review에서 P1·P2 문제는 없었다. ignored runtime artifact, transcript에 의존하는 실행 순서, 다른 ref에서 발견 가능한 과거 Harness commit, 선언과 다른 실제 pnpm 버전은 [blind 평가 기록](../records/2026-08-14-04-blind-apply-context-harness-skill-evaluation.md)의 상한으로 남겼다.

## 남은 불확실성

- 현재 target에는 Harness가 없으므로 recover·verify·receipt 재진입을 실행할 수 없다.
- 최신 source/output/minimum-memory 계약은 격리 사본에서 검증했지만 원본 target에는 설치하지 않았다.
- 외부 결제 화면의 승인·취소, focus 복귀, 모바일 표시, 실제 PG·영속 DB·Android WebView·웹훅·운영 효과와 사람 acceptance는 여전히 확인하지 않았다.
- 다른 실제 Project에 대한 portability도 검증하지 않았다.

## 다음 행동

원본 target `9519a43`은 clean·Harness 미설치 상태로 유지한다. 격리 평가 결과의 acceptance, 격리 파일의 commit 또는 제거, 원본 재적용은 사용자가 각각 결정해야 하며 자동 검증만으로 대신 확정하지 않는다.
