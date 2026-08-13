# Project Workspace Context Harness

이미 존재하는 개발 Project에서 한 Workspace가 필요한 Project 맥락만 복구하고, 실제 변경의 검증 결과를 다음 재진입 상태로 돌려보내는 실행 가능한 reference다.

이 reference는 세 경계를 함께 보여 준다.

- **Project**: [`docs/`](docs/), [`src/`](src/), [`tests/test_config_loader.py`](tests/test_config_loader.py)가 제품 기준·구현·검증을 소유한다.
- **Workspaces**: [`workspaces/`](workspaces/)가 작업별 선택 계약, 현재 context, machine status, 누적 기록을 소유한다.
- **Harness**: [`harness/`](harness/)가 Workspace를 대상으로 `recover`와 `verify`를 실행한다.

Harness는 Project 기준이나 Workspace의 의미를 소유하지 않는다. 두 경계의 canonical을 읽고 검증 결과를 연결하는 관리 장치다.

## 시작점

사람이 현재 작업을 볼 때는 [active Workspace README](workspaces/001-default-timeout/README.md)에서 시작한다. Harness의 책임과 workflow를 변경할 때는 [Harness README](harness/README.md)에서 시작한다.

실제 명령은 `output/` root에서 실행한다.

```bash
python3 -m harness recover
python3 -m harness verify
python3 -m unittest discover -s . -p 'test_*.py' -v
```

- `recover`: active Workspace와 recover 전용 계약을 읽어 필요한 current와 선택된 Project context만 recovery packet으로 만든다.
- `verify`: verify 전용 계약의 고정 argv를 제한 안에서 실행하고 receipt와 machine status를 갱신한다.
- 전체 test discovery: 제품 테스트와 각 Harness 책임 안에 함께 둔 테스트를 모두 실행한다.

## 구조

```text
.
├── docs/                         # Project canonical 기준과 결정
├── src/                          # 실제 제품 코드
├── tests/
│   └── test_config_loader.py     # 제품 동작 검증
├── harness/
│   ├── README.md                 # Harness와 두 책임의 관계
│   ├── workspace_contract.py     # 두 책임이 공유하는 최소 인계 계약
│   ├── recover/                  # 복구 정의·구현·테스트
│   └── verify/                   # 검증 정의·구현·테스트
└── workspaces/
    ├── README.md                 # 지속 Workspace 경계
    ├── index.json                # active Workspace 선택
    └── 001-default-timeout/
        ├── README.md             # 사람용 Workspace 첫 화면
        ├── workspace.json        # Workspace identity
        ├── recover.json          # Project context 선택 계약
        ├── verify.json           # 고정 검증 계약
        ├── current/              # 현재 memory, 사람용 state, machine status
        └── records/              # 상세 작업 기록과 verification receipt
```

Project 문서 전체를 Workspace에 복사하지 않는다. 이 Workspace의 [`recover.json`](workspaces/001-default-timeout/recover.json)은 [`PRD`](docs/prd.md)와 [`default timeout 결정`](docs/decisions/0001-default-timeout.md)만 선택한다. 선택하지 않은 [`architecture`](docs/architecture.md)와 `records/` 전체는 기본 recovery context에 들어가지 않는다.

## 실제 실행 증거

reference 순환을 확인하기 위해 기본 timeout 구현을 의도적으로 `3000`으로 어긋나게 한 뒤 같은 검증으로 실패시키고, canonical 값 `5000`으로 고쳐 다시 검증했다.

- [실패 receipt](workspaces/001-default-timeout/records/verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json): 제품 테스트 실패와 exit `1`
- [성공 receipt](workspaces/001-default-timeout/records/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json): 같은 제품 테스트 통과와 exit `0`
- [사람용 현재 화면](workspaces/001-default-timeout/current/state/index.md)과 [machine status](workspaces/001-default-timeout/current/state/status.json): 현재 문제의 의미와 최근 검증 cursor 분리
- [검증 순환 기록](workspaces/001-default-timeout/records/2026-08-13-01-default-timeout-verification-cycle.md)과 [current 폴더화 기록](workspaces/001-default-timeout/records/2026-08-13-02-current-folder-migration.md): 당시 구현과 검증 범위
- [Harness 책임 경계 기록](workspaces/001-default-timeout/records/2026-08-13-03-harness-responsibility-boundary-refactor.md): recover·verify 응집, 26개 테스트, 실제 새 CLI 재검증
- [책임 재구성 뒤 최종 성공 receipt](workspaces/001-default-timeout/records/verify-20260813T125144640368Z-5dd549bd4b3244ba97787b7bdc80b503.json): 제품 테스트 7개 통과, exit `0`, 실행 전 evidence hash

## 증명 범위

이 reference가 확인하는 것은 선택적 context 복구, 고정 검증 실행, 실패·성공 receipt 생성, machine status 갱신, 갱신 상태의 재복구다.

Workspace 생성·전환·acceptance·완료·보관, Workspace 결과의 Project canonical 반영, concurrent verify 조정, 실제 네트워크 요청과 운영 서비스 효과는 아직 구현하거나 증명하지 않았다. Harness 계약은 저장소가 신뢰하는 입력이며 악의적인 검증 프로그램을 격리하는 sandbox가 아니다. Receipt와 status는 각각 atomic하게 쓰지만 하나의 transaction으로 묶이지 않는다.
