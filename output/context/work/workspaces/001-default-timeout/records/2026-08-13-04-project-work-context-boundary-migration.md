# Project context와 Work context 상위 경계 이동

날짜: `2026-08-13`

## 작업 목적

Project root에 형제로 놓였던 `docs/`, `harness/`, `workspaces/`를 실제 책임 관계에 맞게 재배치한다.

- Project common context는 `context/project/`에서 소유한다.
- Work context의 상위 경계는 `context/work/`에서 Harness와 Workspace collection의 관계를 정의한다.
- 제품 코드와 제품 테스트는 context 밖의 `src/`, `tests/`에 유지한다.

## 실제 변경

- `docs/`를 `context/project/`로 이동하고 Project context 진입 문서를 추가했다.
- `harness/`와 `workspaces/`를 `context/work/` 아래 형제로 이동하고 Work context 진입 문서를 추가했다.
- CLI를 `python3 -m context.work.harness`로 변경했다.
- 단일 root 계약을 다음처럼 분리했다.
  - `project_root`: `context/project/`, 제품 evidence, verify 명령의 실행 cwd
  - `work_root`: Workspace index·계약·current·records·receipt
- `recover.json`을 schema `2`로 올리고 Project context 경로를 `context/project/` 안의 Project-root 상대 경로로 바꿨다.
- recovery packet을 schema `4`로 올리고 각 경로에 `project_root` 또는 `work_root`라는 `path_base`를 명시했다.
- `status.json`을 schema `2`로 올려 receipt가 Work-root 상대 경로라는 의미를 고정했다.
- verify 계약과 receipt schema는 유지했다. 제품 evidence 경로와 검증 cwd의 기준은 이전과 같이 Project root이기 때문이다.
- 기존 receipt 파일은 당시 실행 증거이므로 내용은 다시 쓰지 않고 새 위치로 이동했다.

## 자동 테스트

Project root에서 다음 명령을 실행했다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

총 29개가 통과했다.

- recover 책임 테스트: 13개
- verify 책임 테스트: 9개
- 제품 config loader 테스트: 7개

추가된 root 분리 테스트는 Work root 안에 가짜 Project 문서·코드·테스트를 놓아도 recover와 verify가 이를 사용하지 않는지 확인한다. 기존 계약 오류 독립성, path traversal·절대경로·symlink 거부, evidence 선확보, timeout, 출력 상한, append-only receipt와 사람용 state 불변도 계속 통과했다.

## 실제 reference 순환

새 CLI로 active Workspace의 `recover → verify → recover`를 실행했다.

- 사전 recovery: packet schema `4`로 Work-root Workspace 경로와 Project-root Project context 경로를 구분해 복구
- verify: Project root에서 제품 unittest 7개 실행, exit `0`
- 새 receipt: [`verify-20260813T135739719409Z-2c773fcd8f4f4409b9a7c394194b3b13.json`](verify-20260813T135739719409Z-2c773fcd8f4f4409b9a7c394194b3b13.json)
- machine status: schema `2`, `verified_waiting_acceptance`, 최신 receipt를 Work-root 상대 경로로 연결
- 후속 recovery: 새 status와 receipt header, 선택된 `context/project/` 문서 두 개를 다시 복구
- 사람용 `current/state/index.md` SHA-256은 실행 전후 모두 `3360a031e6054e594d94ace6b4007dafad422e83883241017b94c1aacbe81ead`
- 독립 read-only 검토에서 Project/Work Owner, Harness 제거 가능성, 두 root의 실제 분리, schema·receipt 보존, 기존 안전 계약, 사람용 진입 경로를 확인했고 남은 P1·P2·P3 결함은 없었다.
- 기존 receipt 5개는 이동 전 `HEAD` 파일과 byte·SHA-256이 모두 일치했고, `output/` Markdown의 로컬 링크 검사에서 깨진 링크는 없었다.

## 검증 상한

이번 작업은 한 reference Project에서 두 root의 의미 분리, 새 위치의 실행 가능성, 기존 안전·상태 인계 동작 보존을 확인한다.

다른 실제 Project로의 이식, Project별 기존 문서 migration, Workspace 생성·전환·acceptance·완료·보관, concurrent verify와 receipt/status 단일 transaction은 구현하거나 증명하지 않았다.
