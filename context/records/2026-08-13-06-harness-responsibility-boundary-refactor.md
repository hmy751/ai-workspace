# Harness 책임 경계 재구성

날짜: `2026-08-13`
상태: 구현·검증·사용자 수락·commit 완료
기준 commit: `80635ad`

## 작업 배경

사용자는 commit `df2ce77`의 Workspace current 폴더화와 사람용 `state/index.md`·기계용 `state/status.json` 분리를 수락했다.

다음 작업에서는 실제 workflow가 `recover`와 `verify`라는 책임을 중심으로 설명되지만, 구현·계약·테스트·운영 설명은 파일 종류와 저장 위치를 따라 흩어진 문제를 개선한다.

현재 확인된 구조적 결합은 다음과 같다.

- `harness/workspace.py` 한 파일이 Workspace 선택, recover, verify, receipt, 상태 갱신, CLI를 모두 구현한다.
- `tests/test_workspace_harness.py` 한 파일이 recover와 verify 계약을 함께 검증한다.
- `workspace.json` 한 파일과 `_load_manifest()`가 recover 전용 `project_context`와 verify 전용 `verification`·`next_actions`를 함께 검증한다.
- 그 결과 recover가 verify 전용 argv·timeout 오류로 실패하고, verify도 자신이 사용하지 않는 Project context 오류의 영향을 받는다.
- Harness 운영 설명이 `output/README.md`, `output/AGENTS.md`, Workspace README에 중복되어 각 책임의 canonical 진입점이 없다.

## 채택한 책임 경계

### Harness

Harness 상위 경계는 `recover`와 `verify`의 관계와 공통 진입 명령만 소유한다.

### Recover

Recover는 다음을 소유한다.

- active Workspace를 기준으로 복구 대상을 선택하는 흐름
- Workspace memory, 사람용 state, machine status, 선택된 Project context 로딩
- status가 연결한 verification receipt의 최소 정합성 확인
- JSON 또는 사람용 recovery packet 생성
- recover 전용 계약 검증과 테스트

### Verify

Verify는 다음을 소유한다.

- evidence 파일의 실행 전 snapshot
- Workspace가 고정한 argv의 제한된 실행
- stdout·stderr 상한, timeout, 로컬 경로 정규화
- append-only verification receipt 생성
- machine status의 검증 결과와 다음 행동 갱신
- verify 전용 계약 검증과 테스트

### Shared Workspace contract

두 책임이 실제로 공유하는 최소 기반만 Harness 상위에 둔다.

- Workspace id와 active Workspace 선택
- output root 안의 안전한 경로·JSON 접근
- machine status schema
- verify가 쓰고 recover가 확인하는 `status → receipt` 인계 필드

Project canonical 문서·제품 코드·제품 테스트와 Workspace의 `current/`·`records/`는 Harness 구현 아래로 옮기지 않는다. Recover와 verify는 이를 사용하지만 의미의 Owner가 아니다.

## 목표 구조

```text
output/
├── harness/
│   ├── README.md
│   ├── __main__.py
│   ├── workspace_contract.py
│   ├── recover/
│   │   ├── README.md
│   │   ├── operation.py
│   │   └── tests/
│   └── verify/
│       ├── README.md
│       ├── operation.py
│       └── tests/
└── workspaces/001-default-timeout/
    ├── workspace.json
    ├── recover.json
    ├── verify.json
    ├── current/
    └── records/
```

`workspace.json`은 Workspace 정체성만 소유하고, `recover.json`은 선택할 Project context, `verify.json`은 고정 검증과 pass/fail 다음 행동을 소유한다.

## 유지할 외부 경계

- Project 기준과 기본값 결정은 계속 `docs/`가 소유한다.
- 제품 구현과 제품 검증은 `src/`와 `tests/test_config_loader.py`가 소유한다.
- 계속 유효한 Work context는 Workspace `current/memory/`가 소유한다.
- 사람의 현재 문제와 해석은 `current/state/index.md`가 소유한다.
- 최근 machine 결과와 다음 행동은 `current/state/status.json`이 소유한다.
- 상세 작업 기록과 verification receipt는 Workspace `records/`에 남긴다.
- 검증 통과와 사람의 acceptance는 구분한다. Acceptance 기록과 완료 전이는 이번 책임 재구성에 섞지 않는다.

## 완료 기준

- Recover와 verify의 구현·전용 계약·테스트·설명을 각 책임 진입점에서 찾을 수 있다.
- Recover는 verify 전용 계약 오류 때문에 실패하지 않고, verify는 recover 전용 계약 오류 때문에 실패하지 않는다.
- 두 명령이 공유하는 코드는 Workspace 선택·안전한 접근·status 인계 계약으로 제한된다.
- 기존 선택적 복구, receipt 비노출, symlink/path 방어, bounded verification, fail/pass 상태 반영 동작이 유지된다.
- 제품 테스트와 Harness 책임별 테스트가 모두 통과한다.
- 실제 reference에서 `recover → verify → recover`를 다시 실행하고 최신 receipt와 상태를 확인한다.

## 구현 결과

- `harness/workspace.py`를 `workspace_contract.py`, `recover/`, `verify/`, thin CLI로 대체했다.
- 통합 Harness test를 각 책임 안의 테스트로 재배치했다.
- `workspace.json`은 identity만 소유하고 `recover.json`과 `verify.json`이 전용 계약을 각각 소유한다.
- recovery packet을 schema `3`으로 변경하고 verify 전용 argv·설정을 제거했다.
- malformed `verify.json`에서도 recover가 성공하고 malformed `recover.json`에서도 verify가 실행되는 독립성 테스트를 추가했다.
- Project canonical과 Workspace `current/records`는 기존 위치와 Owner를 유지했다.

## 검증 결과

- recover 11개, verify 8개, 제품 7개를 합친 26개 unittest 통과
- 실제 active Workspace의 `recover → verify → recover` 통과
- 최종 pass receipt: `output/context/work/workspaces/001-default-timeout/records/verify-20260813T125144640368Z-5dd549bd4b3244ba97787b7bdc80b503.json`
- 후속 recovery가 packet schema `3`, 최신 receipt, `verified_waiting_acceptance`를 복구
- 사람용 Workspace `state/index.md` SHA-256이 verify 전후 동일: `3360a031e6054e594d94ace6b4007dafad422e83883241017b94c1aacbe81ead`
- receipt evidence hash가 실제 source와 product test에 일치
- 독립 read-only 검토에서 P1·P2·P3 결함 없음

Workspace 내부의 상세 증거는 [`output Harness 책임 경계 기록`](../../output/context/work/workspaces/001-default-timeout/records/2026-08-13-03-harness-responsibility-boundary-refactor.md)에 있다.

## 검증 상한

이번 작업은 한 reference Project 내부의 책임 응집과 기존 동작 보존을 검증한다. Workspace 생성·전환·acceptance·완료·보관, Project canonical 반영, concurrent verify와 receipt/status transaction은 구현 범위에 포함하지 않는다.
