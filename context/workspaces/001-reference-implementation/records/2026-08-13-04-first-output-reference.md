# 첫 실행 가능한 output reference 구현과 검증

날짜: `2026-08-13`

## 목표

합의한 Project–Workspace와 `memory/state/records` 경계를 문서 제안으로 끝내지 않고, 실제 코드 작업 한 건이 다음 순환을 통과하는 산출물로 구현한다.

`복구 → 필요한 상위 맥락 선택 → 실제 코드 작업 → 고정 검증 → records/state 반영 → 다음 재진입`

## 구현한 Project

당시 [`output/`](../../../../reference-project/)에 request policy config를 다루는 작은 Python Project를 만들었다. 현재 경로는 `reference-project/`다.

- Project canonical context: PRD, architecture, default-timeout 결정
- 실제 제품 코드: `src/config_loader.py`
- 제품 검증: `tests/test_config_loader.py`
- 핵심 기준: `request_timeout_ms` 누락 시 `5000`밀리초, 잘못된 타입·범위·키 거부, 불변 결과

이 Project는 stdlib-only로 실행되며 파일 파싱, 실제 네트워크 요청, 운영 서비스 적용은 범위 밖이다.

## 구현한 Workspace와 harness

- `workspaces/index.json`: active Workspace 선택
- `workspaces/001-default-timeout/workspace.json`: 선택한 Project context, 선택 이유, 검증 argv와 evidence 경로, 결과별 다음 행동
- `current/memory.md`: 작업 단계가 바뀌어도 계속 유효한 목표·완료 기준·제약·선택한 Project 접근점
- `current/state.md`: machine-owned marker가 최근 결과·receipt·다음 행동을 소유
- `records/`: 실패·성공 receipt와 실행 기록 누적
- `harness/workspace.py recover`: index와 manifest를 제어 정보로 읽고, context 본문은 memory→state→선택된 Project 문서만 반환
- `harness/workspace.py verify`: manifest의 고정 argv를 `shell=False`로 실행하고, 실행 직전 evidence hash·실행 결과를 receipt에 남긴 뒤 state를 갱신

성공은 `verified_waiting_acceptance`, 실패는 `verification_failed`다. 성공도 `completed`로 자동 승격하지 않는다.

## 실제 E2E

### 선택적 복구

초기 `recover --json`이 context 본문으로 읽은 것은 다음 네 경로였다.

- `workspaces/001-default-timeout/current/memory.md`
- `workspaces/001-default-timeout/current/state.md`
- `docs/prd.md`
- `docs/decisions/0001-default-timeout.md`

active Workspace와 선택 목록을 정하기 위해 `workspaces/index.json`과 `workspace.json`도 제어 정보로 읽었으며 recovery packet의 `control_paths`에 별도로 공개한다. 선택하지 않은 architecture와 기존 records 전체는 context 본문에 포함하지 않았다.

### 실패 반영

올바른 기본값 `5000`을 의도적으로 `3000`으로 바꿔 같은 고정 검증을 실행했다.

- 제품 test 7개 중 default-timeout test 1개 실패
- exit code: `1`
- 실제 오류: `AssertionError: 3000 != 5000`
- output receipt: [`fail`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json)
- 지속 상태: `verification_failed`

이는 자연 발생한 장애가 아니라 상태 반영을 검증하기 위해 의도적으로 만든 reference 장면이다.

### 수정·성공·재진입

Project canonical 기준대로 기본값을 `5000`으로 복원하고 같은 검증을 다시 실행했다.

- 제품 test 7개 통과
- exit code: `0`
- output receipt: [`pass`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json)
- 지속 상태: `verified_waiting_acceptance`
- 후속 recovery가 성공 receipt와 사용자 수락이라는 다음 행동을 복구

fixture 기반 harness test 10개는 선택되지 않은 context·records 비노출, path/schema/marker/shell 입력 거부, 연결 receipt 정합성, fail→pass receipt/state 전이, timeout, 출력 상한·경로 정규화, pass가 completed가 아님을 검증한다. 제품 test와 합치면 총 17개 unittest가 통과했다.

## 독립 리뷰에서 잡아 반영한 결함

- records symlink를 통해 선택 경계를 우회할 수 있던 문제
- 검증 명령이 evidence를 삭제하면 receipt 자체가 남지 않던 문제
- 잘못된 marker 타입이 계약 오류가 아니라 Python 예외를 만들던 문제
- marker 밖 state 설명이 검증 후 낡을 수 있던 문제
- index와 manifest도 읽으면서 context 네 경로만 읽었다고 보일 수 있던 provenance 표현
- state가 가리키는 receipt가 없거나 내용이 어긋나도 recovery가 성공하던 문제
- 검증 subprocess의 timeout·출력 상한이 없어 지속 상태 반영 전에 멈출 수 있던 문제
- receipt traceback에 로컬 output 절대경로가 남던 문제

## 증명 상한과 미구현

확인한 것은 한 로컬 reference Project에서 선택적 복구, 실제 unittest 실패와 성공, receipt 누적, state 갱신, 갱신 상태 재복구다.

확인하거나 구현하지 않은 것은 다음과 같다.

- 실제 사용자 Project 채택과 실제 운영 서비스 효과
- Workspace 생성·전환·acceptance·완료·보관
- Workspace 결과를 Project canonical context에 반영하는 owner·승인 흐름
- 동시 verify 조정과 receipt/state의 단일 transaction
- recovery 시 receipt의 argv·evidence·exit code까지 포함한 전체 의미 재검산
- 악의적인 manifest나 검증 프로그램을 격리하는 sandbox

현재 output Workspace는 사용자 수락 전이며 `verified_waiting_acceptance`를 유지한다.
