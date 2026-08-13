# Project·Work context 상위 경계 재구성

날짜: `2026-08-13`
상태: 방향 수락, 구현·실제 순환 검증·commit 완료, 결과 검토 전
이전 기준 commit: `80635ad`
구현 commit: `2b110a3`

## 작업 배경

Harness의 `recover`와 `verify` 책임은 분리했지만, Project root에는 `docs/`, `harness/`, `workspaces/`가 형제처럼 놓여 있다. 이 배치는 다음 실제 관계를 충분히 드러내지 못한다.

- `docs/`의 PRD·architecture·공통 결정은 여러 작업이 공유하는 Project common context다.
- 각 Workspace는 특정 작업의 current와 records를 소유한다.
- Harness는 Project common context가 아니라 여러 Workspace를 선택·복구·검증하는 Work context의 공용 관리 장치다.

현재 코드는 `output/` 하나를 Project 문서·제품 코드·제품 테스트의 기준과 Workspace 상태·receipt의 기준으로 동시에 사용한다. 따라서 폴더만 이동하면 recover의 Project context 접근과 verify의 evidence·실행 cwd가 깨진다.

## 사용자가 수락한 방향

```text
output/
├── src/
├── tests/
└── context/
    ├── README.md
    ├── project/
    │   ├── README.md
    │   ├── prd.md
    │   ├── architecture.md
    │   └── decisions/
    └── work/
        ├── README.md
        ├── harness/
        └── workspaces/
```

- `context/README.md`는 Project context와 Work context의 관계를 정의한다.
- `context/project/`는 이 reference에서 여러 작업이 공유하는 Project common context를 소유한다.
- `context/work/`는 Harness와 Workspace collection의 관계를 정의한다.
- Harness는 개별 Workspace 안에 복제하지 않고 `workspaces/`와 형제로 둔다.
- `workspaces` 이름은 유지한다. 모호함의 원인은 이름보다 Project root에 평평하게 노출된 배치였다.
- 제품 구현과 제품 테스트는 context가 아니므로 `src/`, `tests/`에 유지한다.

## 구현에서 분리할 기준

- `project_root`: Project context, 제품 evidence, verify 명령의 실행 cwd 기준
- `work_root`: Workspace index, identity·책임별 계약, current, records, receipt 기준
- `harness_root`: 코드 위치이며 Project나 Workspace 의미의 canonical이 아님

Project context와 evidence 경로는 `../../../` 같은 물리적 탈출 경로가 아니라 계속 `project_root` 상대 경로로 표현한다. Workspace 상태 경로는 `work_root` 상대임을 packet과 status 계약에서 명확히 한다.

## 완료 기준

- 일반 진입점에서 Project context와 Work context의 정체성·관계·Owner를 찾을 수 있다.
- Harness를 제거해도 각 Workspace README와 current·records의 의미를 찾을 수 있다.
- recover는 `context/project/`의 선택된 문서만 Project context로 싣는다.
- verify는 Project root에서 제품 검증을 실행하고 Project-root 상대 evidence를 기록한다.
- Workspace index·status·receipt는 Work root 안에서만 해석하고 갱신한다.
- 전체 제품·Harness 테스트와 실제 `recover → verify → recover`가 통과한다.

## 범위 밖

- 다른 Project의 기존 문서를 강제로 `context/project/`로 옮기는 범용 migration
- Workspace 생성·전환·acceptance·완료·보관 lifecycle
- concurrent verify와 receipt/status 단일 transaction

## 구현 결과

- `output/context/README.md`가 Project context와 Work context의 관계를 정의한다.
- `output/context/project/`로 PRD·architecture·공통 결정을 이동하고 별도 진입점을 두었다.
- `output/context/work/`로 Harness와 `workspaces/`를 이동하고 둘의 상위 관계를 정의했다.
- 제품 구현과 제품 테스트는 `output/src/`, `output/tests/`에 유지했다.
- CLI를 `python3 -m context.work.harness`로 변경하고 `project_root`와 `work_root`를 분리했다.
- recover contract schema `2`, recovery packet schema `4`, status schema `2`로 경로 기준 변경을 명시했다.
- verify contract와 기존 receipt schema는 Project-root 상대 의미가 유지되어 올리지 않았다.
- 기존 receipt는 내용을 변경하지 않고 새 Work root 아래로 이동했다.

## 검증 결과

- recover 13개, verify 9개, 제품 7개를 합친 29개 unittest 통과
- 새 CLI help와 실제 active Workspace recover schema `4` 확인
- 실제 `recover → verify → recover` 통과
- 최종 pass receipt: `output/context/work/workspaces/001-default-timeout/records/verify-20260813T135739719409Z-2c773fcd8f4f4409b9a7c394194b3b13.json`
- 후속 recovery가 Work-root Workspace 자료와 Project-root `context/project/` 문서를 구분해 복구
- 사람용 Workspace `state/index.md` SHA-256 실행 전후 동일: `3360a031e6054e594d94ace6b4007dafad422e83883241017b94c1aacbe81ead`
- 독립 read-only 검토에서 처음 발견한 stale `context/current/state.md`와 이 record의 진행 상태를 최신 구현·검증 결과로 바로잡았다. 재검토 결과 여섯 검증 주장 모두 supported이며 남은 P1·P2·P3 결함은 없었다.
- 이동한 기존 receipt 5개는 `HEAD`의 이동 전 파일과 byte·SHA-256이 모두 일치했다.
- `output/` Markdown 로컬 링크 전수 검사에서 깨진 링크는 없었다.

Workspace 내부의 상세 증거는 [`Project·Work context 경계 이동 기록`](../../output/context/work/workspaces/001-default-timeout/records/2026-08-13-04-project-work-context-boundary-migration.md)에 있다.

## 검증 상한

이번 작업은 한 reference Project에서 두 root의 의미 분리, 새 위치의 실행 가능성, 기존 안전·상태 인계 동작 보존을 확인한다.

다른 실제 Project로의 이식, Project별 기존 문서 migration, Workspace 생성·전환·acceptance·완료·보관, concurrent verify와 receipt/status 단일 transaction은 구현하거나 증명하지 않았다. CLI가 `context/work/harness` 설치 위치에서 두 root를 유도하는 방식은 이 reference 배치에서만 확인했으며, 다른 배치나 이미 `context` Python package를 사용하는 Project와의 결합은 검증하지 않았다.
