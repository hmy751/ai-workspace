# Default timeout 검증 순환

날짜: `2026-08-13`

## 장면의 성격

context와 harness의 연결을 재현하기 위해 올바르게 작성된 `DEFAULT_REQUEST_TIMEOUT_MS = 5000`을 의도적으로 `3000`으로 바꿔 불일치를 만들었다. 따라서 이 실패는 자연 발생한 제품 장애가 아니라, 실패 상태가 지속 맥락에 반영되는지를 확인하기 위한 reference E2E다.

## 초기 복구

`python3 harness/workspace.py recover --json`은 active Workspace를 선택하기 위한 index와 manifest를 제어 정보로 읽었다. context 본문으로 읽은 경로는 다음 네 개였다.

- `workspaces/001-default-timeout/current/memory.md`
- `workspaces/001-default-timeout/current/state.md`
- `docs/prd.md`
- `docs/decisions/0001-default-timeout.md`

선택되지 않은 `docs/architecture.md`와 기존 records 전체는 context 본문에 포함되지 않았다.

## 실패와 반영

기본값을 `3000`으로 바꾼 상태에서 manifest의 고정 검증을 실행했다.

- 결과: exit `1`, `test_missing_timeout_uses_5000_ms` 1개 실패
- 실제 차이: `AssertionError: 3000 != 5000`
- receipt: [`verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json`](receipts/verify/verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json)
- 지속 상태: `verification_failed`
- 다음 행동: receipt에서 최초 실패를 확인하고 코드 또는 테스트를 수정한 뒤 같은 검증 재실행

receipt에는 실행 argv, exit code, 제한된 stdout·stderr와 실행 직전 코드·테스트의 SHA-256 및 byte size가 남았다. timeout·출력 상한과 truncation 여부도 기록하고, output root 절대경로는 `<OUTPUT_ROOT>`로 정규화한다.

## 수정과 성공

Project의 canonical 결정과 PRD에 맞춰 기본값을 `5000`으로 복원하고 같은 고정 검증을 다시 실행했다.

- 결과: 7개 제품 테스트 통과, exit `0`
- receipt: [`verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json`](receipts/verify/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json)
- 지속 상태: `verified_waiting_acceptance`
- 다음 행동: receipt와 선택한 Project 기준을 검토하고 사람의 수락 여부 결정

후속 `recover --json`은 성공 receipt와 `verified_waiting_acceptance`를 다시 복구했다. 검증 통과를 `completed`로 자동 승격하지 않았다.

## 증명 상한

이 기록은 한 reference Project에서 선택적 복구, 실제 테스트 실패·성공, receipt 누적, state 반영과 재진입이 연결됐음을 증명한다. 실제 사용자 Project 도입, 운영 서비스 동작, 사람의 최종 수락, Workspace 전체 수명주기는 증명하지 않는다.
