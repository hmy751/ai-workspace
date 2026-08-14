# Project application state

마지막 갱신: `2026-08-14`

## 현재 문제

첫 적용의 브라우저 acceptance를 확인하는 일과, 승격한 반복 절차를 두 번째 실제 Project에서 검증하는 일이 남아 있다.

## 현재 상태

- 대상 Project는 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`, 기준 branch는 `feat/payment-recovery-mvp`, Harness 적용 전·현재 HEAD는 `76d8e2f`다.
- Project canonical을 복제하지 않고 `AGENTS.md`, `context/README.md`, `context/work/harness/`, `context/work/workspaces/001-payment-recovery-mvp/`를 적용했다.
- Harness 계약 테스트는 recover 13개와 verify 9개, 총 22개가 통과했다. 실행 전 Harness source 14개의 hash·size와 exit `0`은 별도 durable receipt에 보존됐다.
- live recover는 Workspace current 6개와 선택한 Project canonical 3개만 불러오고 최종 receipt와 `verified_waiting_acceptance` 상태를 연결했다.
- 네 번째 최종 고정 verify는 실제 Turbo 대상 5개 package를 포괄하는 40개 evidence를 실행 전에 보존하고, cache 없이 11개 task를 모두 실행해 통과했다. 5개 test file의 31개 test, typecheck와 Checkout production build가 통과했으며 상세 결과는 [적용·검증 기록](../records/2026-08-13-01-payment-recovery-project-application.md)에 있다.
- 대상 working tree에서 Harness 적용분인 `.gitignore` 수정과 새 `AGENTS.md`, `context/`는 아직 커밋되지 않았다. 적용 전 사용자 변경 `App.tsx`, `styles.css`도 미커밋 상태이며 수정하지 않았다. 적용 전 untracked였던 `context/code-map.md`는 사용자가 직접 삭제했고 현재 없다.
- 첫 적용의 반복 절차를 repo-local `apply-context-harness` skill로 승격했다. helper unit 7개는 Python 3.14.3과 `/usr/bin/python3` 3.9.6에서 각각 통과했고, skill validator·YAML·discovery/trigger 검증과 독립 리뷰도 통과했다. 상세 근거는 [승격 기록](../records/2026-08-14-01-apply-context-harness-skill-promotion.md)에 있다.
- 이후 `2026-08-14` 원형과 skill에 추가한 Workspace `source/`, `output/index.md`, 최소 memory 세 파일 계약은 기존 payment target에 자동 적용하지 않았고 다시 검증하지 않았다. 현재 target 상태와 새 이식 계약을 같은 버전으로 해석하지 않는다.

## 남은 불확실성

- 외부 결제 화면의 승인·취소, focus 복귀, 모바일 표시와 승인 응답 유실 자동 복구를 실제 브라우저에서 확인하지 않았다.
- 실제 PG, 영속 DB, Android WebView, 웹훅, 운영 서비스 효과는 검증하지 않았다.
- 사람의 acceptance와 이후 commit·Project canonical 반영 여부는 결정되지 않았다.
- 두 번째 실제 Project에는 아직 이식하지 않았다. 따라서 skill의 portability와 다른 canonical·runtime·test graph에 대한 generalization은 검증되지 않았다.
- 기존 payment target의 source/output/minimum-memory 후속 migration 여부도 아직 결정하지 않았다.

## 다음 행동

첫 적용은 최종 receipt의 evidence 범위를 확인한 뒤 실제 브라우저 동작을 실행해 사용자가 acceptance를 결정한다. portability는 사용자가 두 번째 대상 Project와 변경 범위를 지정한 뒤 repo-local skill로 실제 이식을 끝까지 수행해 검증한다. 그전에는 첫 적용을 완료로 바꾸거나 반복 절차를 범용으로 입증됐다고 쓰지 않는다.
