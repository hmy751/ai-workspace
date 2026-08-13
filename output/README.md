# Project Workspace Context Harness

이미 개발 Project가 존재한다고 가정하고, 하나의 Workspace가 필요한 상위 맥락만 선택해 실제 코드 작업과 검증 결과를 지속 상태로 연결하는 실행 가능한 reference다.

## 실행

사람이 파일을 둘러볼 때는 먼저 [active Workspace README](workspaces/001-default-timeout/README.md)에서 읽는 순서를 확인한다. 실제 재진입과 검증은 이 디렉터리에서 다음 명령으로 실행한다.

```bash
python3 harness/workspace.py recover
python3 harness/workspace.py verify
python3 -m unittest discover -s tests -v
```

- `recover`는 active Workspace를 찾기 위한 index와 manifest를 제어 정보로 읽고, state status가 receipt를 가리키면 그 파일의 존재와 status 정합성을 함께 확인한다.
- context 본문으로는 Workspace의 `memory/index.md`와 주제별 memory 문서, 사람이 읽는 `state/index.md`, 기계 상태인 `state/status.json`, manifest가 선택한 Project 문서만 싣는다.
- `verify`는 manifest에 고정된 argv를 timeout과 출력 상한 안에서 실행하고, 실행 직전 evidence의 SHA-256과 byte size, exit code, 제한된 stdout·stderr를 JSON receipt로 남긴다. timeout은 exit `124`의 실패 결과로 기록하며, 출력의 output root 절대경로는 `<OUTPUT_ROOT>`로 바꾼다.
- 검증 결과는 `state/status.json`에 반영되어 다음 `recover`에서 복구된다. 사람이 읽는 `state/index.md`는 harness가 덮어쓰지 않는다.
- 검증 통과는 `verified_waiting_acceptance`이며 사람의 수락이나 작업 완료를 뜻하지 않는다.

## 구조

```text
.
├── docs/                         # Project의 canonical PRD, architecture, 결정
├── src/                          # 실제 제품 코드
├── tests/                        # 제품과 harness의 실행 테스트
├── workspaces/
│   ├── index.json                # active Workspace 선택
│   └── 001-default-timeout/
│       ├── README.md             # 사람용 Workspace 첫 화면
│       ├── workspace.json        # 선택한 Project context와 고정 검증 계약
│       ├── current/
│       │   ├── memory/           # 계속 유효한 현재 맥락의 주제별 문서
│       │   │   ├── index.md      # memory 지도
│       │   │   ├── 01-goal.md
│       │   │   ├── 02-constraints.md
│       │   │   └── 03-project-context.md
│       │   └── state/
│       │       ├── index.md      # 사람용 현재 문제와 해석 경계
│       │       └── status.json   # harness가 갱신하는 최근 결과와 다음 행동
│       └── records/              # append-only 검증 receipt와 작업 기록
└── harness/workspace.py          # recover와 verify 연결
```

Project 문서 전체를 Workspace에 복사하지 않는다. 이 예시의 Workspace는 [`PRD`](docs/prd.md)와 [`default timeout 결정`](docs/decisions/0001-default-timeout.md)만 선택하고, 선택하지 않은 [`architecture`](docs/architecture.md)는 기본 recovery context에 싣지 않는다.

## 실제 실행 증거

reference 순환을 확인하기 위해 기본 timeout 구현을 의도적으로 `3000`으로 어긋나게 한 뒤 같은 검증 명령으로 실패시키고, canonical 값 `5000`으로 고쳐 다시 검증했다.

- [실패 receipt](workspaces/001-default-timeout/records/verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json): 7개 제품 테스트 중 기본값 테스트 1개 실패, exit `1`
- [성공 receipt](workspaces/001-default-timeout/records/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json): 같은 7개 제품 테스트 통과, exit `0`
- [사람용 현재 화면](workspaces/001-default-timeout/current/state/index.md)과 [기계 상태](workspaces/001-default-timeout/current/state/status.json): 현재 문제와 `verified_waiting_acceptance`, 성공 receipt, 다음 행동을 분리해 보존
- [실행 기록](workspaces/001-default-timeout/records/2026-08-13-01-default-timeout-verification-cycle.md): 의도적으로 만든 장면과 증거 범위를 구분
- [current 폴더화 기록](workspaces/001-default-timeout/records/2026-08-13-02-current-folder-migration.md): 사람용 index와 machine status 분리, 22개 테스트와 post-migration 재검증을 보존

## 증명 범위

이 reference가 실제로 확인한 것은 선택적 context 복구, 고정된 테스트 실행, 실패와 성공 receipt 생성, state 갱신, 갱신된 상태의 재복구다.

아직 구현하거나 증명하지 않은 것은 Workspace 생성·전환·완료·보관, 사람의 acceptance 기록, Workspace 결과의 Project canonical 반영, 동시 검증 조정, 실제 네트워크 요청과 운영 서비스 적용이다. manifest는 저장소가 신뢰하는 운영 계약이며, 이 harness는 악의적인 manifest를 격리하는 sandbox가 아니다. recovery는 연결 receipt의 schema·Workspace·result·finished_at을 state status와 대조하지만 argv·evidence·exit code까지 전체 의미를 재검산하지는 않는다. `status.json` 하나의 교체는 atomic하지만 receipt와 status를 하나의 transaction으로 묶지는 않는다.
