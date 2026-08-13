# Project context와 Work context reference

이미 존재하는 개발 Project에서 한 Workspace가 필요한 Project 맥락만 복구하고, 실제 변경의 검증 결과를 다음 재진입 상태로 돌려보내는 실행 가능한 reference다.

이 reference는 Project context와 Work context를 상위 경계로 두고, 실제 제품과 관리 장치의 관계를 함께 보여 준다.

- **Project context**: [`context/project/`](context/project/)가 여러 작업이 공유하는 제품 기준·구조·결정을 소유한다.
- **Work context**: [`context/work/`](context/work/)가 여러 Workspace와 공용 Harness의 운영 관계를 소유한다.
- **제품**: [`src/`](src/)와 [`tests/test_config_loader.py`](tests/test_config_loader.py)가 실제 구현과 제품 검증을 소유한다.

Harness는 Work context 안의 공용 관리 장치다. Project 기준이나 Workspace의 의미를 소유하지 않고, 두 경계의 canonical을 읽어 검증 결과를 연결한다.

## 시작점

전체 context 관계는 [context README](context/README.md), 사람이 현재 작업을 볼 때는 [active Workspace README](context/work/workspaces/001-default-timeout/README.md)에서 시작한다. Harness의 책임과 workflow를 변경할 때는 [Harness README](context/work/harness/README.md)에서 시작한다.

실제 명령은 `output/` root에서 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness verify
python3 -m unittest discover -s . -p 'test_*.py' -v
```

- `recover`: active Workspace와 recover 전용 계약을 읽어 필요한 current와 선택된 Project context만 recovery packet으로 만든다.
- `verify`: verify 전용 계약의 고정 argv를 제한 안에서 실행하고 receipt와 machine status를 갱신한다.
- 전체 test discovery: 제품 테스트와 각 Harness 책임 안에 함께 둔 테스트를 모두 실행한다.

## 구조

```text
.
├── src/                          # 실제 제품 코드
├── tests/
│   └── test_config_loader.py     # 제품 동작 검증
└── context/
    ├── README.md                 # Project context와 Work context의 관계
    ├── project/                  # 공유 Project 기준과 결정
    └── work/
        ├── README.md             # Work context 운영 경계
        ├── harness/              # 공용 recover·verify 관리 장치
        └── workspaces/
            ├── README.md         # 지속 Workspace collection 경계
            ├── index.json        # active Workspace 선택
            └── 001-default-timeout/
                ├── README.md     # 사람용 Workspace 첫 화면
                ├── workspace.json
                ├── recover.json
                ├── verify.json
                ├── current/
                └── records/
```

Project 문서 전체를 Workspace에 복사하지 않는다. 이 Workspace의 [`recover.json`](context/work/workspaces/001-default-timeout/recover.json)은 [`PRD`](context/project/prd.md)와 [`default timeout 결정`](context/project/decisions/0001-default-timeout.md)만 선택한다. 선택하지 않은 [`architecture`](context/project/architecture.md)와 `records/` 전체는 기본 recovery context에 들어가지 않는다.

## 실제 실행 증거

reference 순환을 확인하기 위해 기본 timeout 구현을 의도적으로 `3000`으로 어긋나게 한 뒤 같은 검증으로 실패시키고, canonical 값 `5000`으로 고쳐 다시 검증했다.

- [실패 receipt](context/work/workspaces/001-default-timeout/records/verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json): 제품 테스트 실패와 exit `1`
- [성공 receipt](context/work/workspaces/001-default-timeout/records/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json): 같은 제품 테스트 통과와 exit `0`
- [사람용 현재 화면](context/work/workspaces/001-default-timeout/current/state/index.md)과 [machine status](context/work/workspaces/001-default-timeout/current/state/status.json): 현재 문제의 의미와 최근 검증 cursor 분리
- [검증 순환 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-01-default-timeout-verification-cycle.md)과 [current 폴더화 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-02-current-folder-migration.md): 당시 구현과 검증 범위
- [Harness 책임 경계 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-03-harness-responsibility-boundary-refactor.md): recover·verify 응집, 26개 테스트, 실제 새 CLI 재검증
- [책임 재구성 뒤 최종 성공 receipt](context/work/workspaces/001-default-timeout/records/verify-20260813T125144640368Z-5dd549bd4b3244ba97787b7bdc80b503.json): 제품 테스트 7개 통과, exit `0`, 실행 전 evidence hash
- [Project·Work context 경계 이동 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-04-project-work-context-boundary-migration.md): 두 root 분리, 29개 테스트, 새 위치의 실제 순환
- [경계 이동 뒤 성공 receipt](context/work/workspaces/001-default-timeout/records/verify-20260813T135739719409Z-2c773fcd8f4f4409b9a7c394194b3b13.json): Project root에서 제품 테스트 7개 통과, Work root에 결과 연결

## 증명 범위

이 reference가 확인하는 것은 선택적 context 복구, 고정 검증 실행, 실패·성공 receipt 생성, machine status 갱신, 갱신 상태의 재복구다.

Workspace 생성·전환·acceptance·완료·보관, Workspace 결과의 Project canonical 반영, concurrent verify 조정, 실제 네트워크 요청과 운영 서비스 효과는 아직 구현하거나 증명하지 않았다. Harness 계약은 저장소가 신뢰하는 입력이며 악의적인 검증 프로그램을 격리하는 sandbox가 아니다. Receipt와 status는 각각 atomic하게 쓰지만 하나의 transaction으로 묶이지 않는다.
