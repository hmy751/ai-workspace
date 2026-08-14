# Project application state

마지막 갱신: `2026-08-14`

## 현재 문제

새 Project common context·recover 계약을 실제 target 내용으로 이식하고 검증할지는 아직 결정되지 않았다. 원본 target의 Harness 미설치 상태, 이전 계약의 blind 평가, 새 계약의 reference 검증을 서로 다른 증거로 유지해야 한다.

## 현재 상태

- 대상 Project는 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`다. 마지막 직접 확인 기준은 branch `feat/payment-recovery-mvp`, HEAD `9519a43`, clean working tree이며 이번 receipt 계약 변경에서는 target을 다시 열지 않았다.
- 기존 사용자 제품 변경 `App.tsx`, `styles.css`는 `527af89`에 별도로 커밋했다.
- 첫 Harness 적용 전체는 `eaacec7`에 snapshot으로 남겼다. 당시 Harness 계약 22개, 제품 Turbo 11개 task와 31개 test, Checkout build가 통과했고 상세 증거는 [적용·검증 기록](../records/2026-08-13-01-payment-recovery-project-application.md)에 있다.
- `git reset`을 사용하지 않고 `9519a43`에서 `eaacec7`을 revert했다. 마지막 직접 확인에서 target에는 `AGENTS.md`, `context/`, Harness용 `.gitignore` 변경이 없었다.
- 그때 HEAD tree는 Harness 적용 직전 제품 commit `527af89`와 완전히 같았고 `git diff --exit-code 527af89 HEAD`가 `0`을 반환했다.
- rollback 후 Harness 밖에서 동일한 `pnpm exec turbo run typecheck test build --force`를 실행해 cache 없이 11개 task, 31개 test, typecheck와 Checkout production build가 다시 통과했다.
- repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill과 [`reference-project/`](../../../../reference-project/)는 완료 target에 실제 내용의 `context/project/README.md`와 `overview.md`를 요구한다. 기존 README·STATUS·docs·코드·테스트는 상세 Owner로 보존하고, overview에 공통 맥락·Owner·충돌 우선순위를 실제 target 내용으로 구성한다.
- Fresh recover 계약은 schema `4`, `context/project/` 아래 regular Markdown-only, `overview.md` first다. Recovery packet shape는 그대로여서 packet schema `5`를 유지한다.
- 새 이식의 machine receipt는 `records/receipts/{preflight,harness-tests,verify}/`로 분리한다. 새 verify는 nested `verify/`에만 쓰고, 기존 flat `records/*.json`은 읽기 호환만 유지한다. Harness와 helper는 producer이고 receipt의 의미·수명주기 Owner는 target Workspace다.
- 격리 평가 target은 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`, branch `codex/context-harness-skill-test`, HEAD `527af89`다. 원본 002 current·records·output을 읽지 못하게 한 prompt에서 skill 이름·target 경로·첫 장면만 받고 별도 task `019ffec6-7cad-7120-b803-a6f4ef6787f3`가 이식을 수행했다.
- 격리 평가에서는 preflight·dry-run·target adaptation 뒤 첫 verify가 `node_modules` 부재로 실패했고, offline frozen install 후 verify 통과와 후속 recover까지 완료했다. 다만 이 평가는 schema `3`으로 루트 README·STATUS·docs를 직접 선택한 이전 계약의 결과다.
- 격리 target의 마지막 관찰에서는 `AGENTS.md`와 `context/` 44개 설치 파일이 untracked 상태였고 tracked diff와 staged diff는 없었다. Commit·staging·사람 acceptance는 수행하지 않았다.
- 이전 계약의 main 재검증은 preflight 원본·사본 SHA 일치, recover의 정확한 10개 경로, Harness source 14개와 test 28개의 receipt, 제품 evidence 36개 hash와 status linkage를 확인했다. direct Harness 28개 test와 제품 Turbo 11/11 task·31개 test·build도 cache `0`으로 통과했고 독립 review에서 P1·P2 문제는 없었다. ignored runtime artifact, transcript에 의존하는 실행 순서, 다른 ref에서 발견 가능한 과거 Harness commit, 선언과 다른 실제 pnpm 버전은 [blind 평가 기록](../records/2026-08-14-04-blind-apply-context-harness-skill-evaluation.md)의 상한으로 남겼다. 이 결과는 새 `context/project/`·schema `4` 계약을 검증하지 않는다.
- 새 계약은 source reference에서 전체 40개 unittest, 제품 테스트 7개를 nested 경로에 보존한 live verify receipt, 후속 recover의 packet schema `5`와 `overview.md` first 선택까지 확인했다. Skill helper 7개도 현재 Python `3.14.3`과 `/usr/bin` Python `3.9.6`에서 각각 통과했다. 상세 receipt 경계와 해석 상한은 [receipt 계약 기록](../records/2026-08-14-07-target-machine-receipt-boundary-contract.md)에 있다.
- source 기준 Project의 루트 이름은 Workspace `output/`과 책임을 구분하기 위해 `output/`에서 `reference-project/`로 바뀌었고, skill의 source lookup과 clean check도 새 경로를 사용한다. 이번 이름 변경에서는 Payment target을 열거나 재적용하지 않았으므로 target 검증 상태는 바뀌지 않았다. 상세 경계는 [이름 변경 기록](../records/2026-08-14-06-reference-project-root-rename.md)에 있다.
- 이번 receipt 계약 변경도 원본·격리 Payment target을 열거나 재이식하지 않았다. 첫 적용 snapshot과 blind 평가의 machine receipt는 당시 flat layout의 과거 증거로 유지되며 nested migration을 완료한 것으로 해석하지 않는다.

## 남은 불확실성

- 마지막 확인 상태의 원본 target에는 Harness가 없으므로 recover·verify·receipt 재진입을 실행할 수 없었다.
- Payment target 원자료에서 실제 `context/project/README.md`와 `overview.md` 내용을 구성하고 상세 Owner와 대조하는 작업은 하지 않았다.
- 새 schema `4` 계약은 실제 target이나 격리 target에 재적용하지 않았고 target별 `recover → verify → recover`와 독립 review도 수행하지 않았다.
- Nested receipt 계약은 실제 Payment target에서 검증하지 않았다. 기존 flat receipt 읽기 호환도 reference 회귀 테스트의 증거이며 target 자체를 다시 실행한 증거가 아니다.
- 외부 결제 화면의 승인·취소, focus 복귀, 모바일 표시, 실제 PG·영속 DB·Android WebView·웹훅·운영 효과와 사람 acceptance는 여전히 확인하지 않았다.
- 다른 실제 Project에 대한 portability도 검증하지 않았다.

## 다음 행동

원본 target은 사용자 결정 전까지 마지막 확인된 `9519a43`의 clean·Harness 미설치 상태를 전제로 보존한다. 재적용한다면 먼저 target을 새로 preflight하고 실제 Project 공통 맥락과 상세 Owner를 대조해 `context/project/README.md`와 `overview.md`를 작성한다. Machine receipt는 `records/receipts/{preflight,harness-tests,verify}/`에 새로 남기고 schema `4`의 `recover → verify → recover`와 독립 review를 수행한다. 기존 flat receipt의 migration, 격리 파일의 commit·제거, 원본 재적용과 사람 acceptance는 사용자가 각각 결정한다.
