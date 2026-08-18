# Project context와 Work context reference

이미 존재하는 개발 Project에서 한 Workspace가 필요한 Project 맥락만 복구하고, 작업 중 의미 변화와 실제 검증 결과를 서로 다른 책임으로 유지한 뒤 다음 재진입 상태로 넘기는 실행 가능한 reference다.

이 reference는 Project context와 Work context를 상위 경계로 두고, 실제 제품과 관리 장치의 관계를 함께 보여 준다.

- **Project context**: [`context/project/`](context/project/)가 여러 작업이 공유하는 실제 제품 목적·구조·제약·채택 결정의 공통 맥락을 소유한다.
- **Work context**: [`context/work/`](context/work/)가 여러 Workspace와 공용 Harness의 운영 관계를 소유한다.
- **제품**: [`src/`](src/)와 [`tests/test_config_loader.py`](tests/test_config_loader.py)가 실제 구현과 제품 검증을 소유한다.

Harness는 Work context 안의 공용 관리 장치다. Project 기준이나 Workspace의 의미를 소유하지 않고, Recover·Maintain·Verify의 작업 책임과 Harness validation을 구조적으로 분리한다. 결정적 CLI는 Recover와 Verify가, 의미 갱신은 별도 Maintain 계약과 교체 가능한 agent/main adapter가, 관리 장치의 회귀는 임시 fixture validation이 맡는다.

## 시작점

전체 context 관계는 [context README](context/README.md), 사람이 현재 작업을 볼 때는 [active Workspace README](context/work/workspaces/001-default-timeout/README.md)에서 시작한다. Work·Harness의 AI 운영 지침은 [Work AGENTS](context/work/AGENTS.md), Harness 책임과 workflow는 [Harness README](context/work/harness/README.md)에서 시작한다.

실제 명령은 `reference-project/` root에서 실행한다.

```bash
python3 -m context.work.harness recover 001-default-timeout
python3 -m context.work.harness verify 001-default-timeout
python3 -m unittest discover -s . -p 'test_*.py' -v
```

- `recover`: 명시한 Workspace를 우선하고 id가 없을 때만 active 기본값을 사용해, 필요한 current와 선택된 Project context를 read-only recovery packet으로 만든다.
- `maintain`: Python 명령이 아니라 [`Maintain 계약`](context/work/harness/maintain/README.md)에 따라 명시한 Workspace의 의미 변화를 기존 Owner에 반영하고 main이 diff를 검토하는 agent/main 책임이다.
- `verify`: claim·canonical basis·evidence를 실행 전에 snapshot하고 고정 argv를 제한 안에서 실행한 뒤 receipt와 machine status만 갱신한다.
- 전체 test discovery: 제품 테스트와 임시 fixture에서 실행되는 Harness validation을 포함한 책임별 테스트를 실행한다. Active 제품 Workspace의 receipt와 status는 바꾸지 않는다.

## 구조

```text
.
├── .codex/
│   └── config.toml               # 하위 Maintain agent 발견 경로만 등록
├── AGENTS.md                     # 책임별 하위 지침을 찾는 최소 router
├── src/                          # 실제 제품 코드
├── tests/
│   └── test_config_loader.py     # 제품 동작 검증
└── context/
    ├── README.md                 # Project context와 Work context의 관계
    ├── project/                  # 실제 Project common context
    │   ├── README.md             # 책임·상세 Owner·충돌 우선순위
    │   ├── overview.md           # 여러 Workspace가 공유할 실제 맥락
    │   ├── prd.md
    │   ├── architecture.md
    │   └── decisions/
    └── work/
        ├── README.md             # Work context 운영 경계
        ├── AGENTS.md             # Work·Harness 운영과 Maintain agent routing
        ├── harness/              # 교체 가능한 Workspace 관리 장치
        │   ├── recover/          # 읽기 전용 재진입
        │   ├── maintain/         # 의미 갱신 책임과 실제 agent 정의
        │   ├── verify/           # durable 제품 검증 증거
        │   └── validation/       # 제품 상태를 보존하는 Harness 자체 검증
        └── workspaces/
            ├── README.md         # 지속 Workspace collection 경계
            ├── index.json        # active Workspace 선택
            └── 001-default-timeout/
                ├── README.md     # 사람용 Workspace 첫 화면
                ├── workspace.json
                ├── recover.json
                ├── verify.json
                ├── current/
                ├── source/
                ├── output/
                └── records/
                    ├── README.md
                    ├── YYYY-MM-DD-NN-*.md
                    └── receipts/
                        ├── README.md
                        └── verify/
```

각 Workspace는 `current/`, `source/`, `output/`, `records/`를 형제로 둔다. `current/memory/`의 `01-goal.md`, `02-constraints.md`, `03-project-context.md`는 최소 재진입 context이고, `source/`에는 해당 Workspace가 선택한 원문·snapshot·provenance만 둔다. 분석 메모·후보·비교·탈락안·선택 근거를 포함한 과정은 `records/` 바로 아래 날짜별 기록이 맡고, 기계가 생성한 검증 증거는 `records/receipts/<종류>/`에 분리한다. Goal을 위해 선택된 현재 산출물은 [`output/index.md`](context/work/workspaces/001-default-timeout/output/index.md)에서 찾게 한다. 이 sample의 실제 제품 구현은 Project root의 canonical을 연결하며 Workspace 안에 복제하지 않는다.

Project 문서 전체를 Workspace에 복사하지 않는다. 이 Workspace의 [`recover.json`](context/work/workspaces/001-default-timeout/recover.json)은 실제 공통 맥락인 [`overview`](context/project/overview.md)와 이번 작업에 직접 필요한 [`default timeout 결정`](context/project/decisions/0001-default-timeout.md)만 선택한다. 선택하지 않은 [`PRD`](context/project/prd.md)와 [`architecture`](context/project/architecture.md), Workspace `source/`와 `records/` 전체, Workspace `output/index.md`가 연결한 산출물 본문은 기본 recovery context에 들어가지 않는다.

## 실제 실행 증거

reference 순환을 확인하기 위해 기본 timeout 구현을 의도적으로 `3000`으로 어긋나게 한 뒤 같은 검증으로 실패시키고, canonical 값 `5000`으로 고쳐 다시 검증했다.

- [실패 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json): 제품 테스트 실패와 exit `1`
- [성공 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json): 같은 제품 테스트 통과와 exit `0`
- [사람용 현재 화면](context/work/workspaces/001-default-timeout/current/state/index.md)과 [machine status](context/work/workspaces/001-default-timeout/current/state/status.json): 현재 문제의 의미와 최근 검증 cursor 분리
- [goal output 지도](context/work/workspaces/001-default-timeout/output/index.md): 실제 제품 구현의 canonical 위치를 복제 없이 연결
- [검증 순환 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-01-default-timeout-verification-cycle.md)과 [current 폴더화 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-02-current-folder-migration.md): 당시 구현과 검증 범위
- [Harness 책임 경계 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-03-harness-responsibility-boundary-refactor.md): recover·verify 응집, 26개 테스트, 실제 새 CLI 재검증
- [책임 재구성 뒤 최종 성공 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260813T125144640368Z-5dd549bd4b3244ba97787b7bdc80b503.json): 제품 테스트 7개 통과, exit `0`, 실행 전 evidence hash
- [Project·Work context 경계 이동 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-04-project-work-context-boundary-migration.md): 두 root 분리, 29개 테스트, 새 위치의 실제 순환
- [경계 이동 뒤 성공 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260813T135739719409Z-2c773fcd8f4f4409b9a7c394194b3b13.json): Project root에서 제품 테스트 7개 통과, Work root에 결과 연결
- [Machine receipt 경계 기록](context/work/workspaces/001-default-timeout/records/2026-08-14-05-machine-receipt-boundary.md)과 [당시 nested receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json): 사람용 records와 종류별 기계 증거 분리, 이전 flat 경로 호환, 40개 테스트와 당시 실제 순환
- [책임 분리 뒤 제품 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T103703075846Z-a1cde45907164974a19c22564a956127.json): claim, canonical basis 3개와 evidence 2개의 실행 전 snapshot, bounded runtime, 제품 테스트 7개 통과, schema `3` machine-only status와 explicit Recover의 `fresh` 재확인

## 증명 범위

이 reference가 확인하는 것은 명시적 또는 active-default Workspace의 선택적 context 복구, Maintain 책임·Reference agent adapter의 구조적 연결, claim·canonical basis·evidence snapshot, 고정 검증 실행, 실패·성공 receipt 생성, machine-only status 갱신, 선언된 snapshot freshness의 재복구다. Harness 회귀 순환은 임시 fixture에서 실행해 active 제품 상태를 오염시키지 않는다.

정적 연결과 테스트는 Maintain agent가 실제 변화에서 어떤 의미를 남겨야 하는지 또는 작성 내용이 충분한지를 증명하지 않는다. 그 판단은 main의 evidence·diff 검토가 필요하다. Workspace 생성·전환·acceptance·완료·보관, Workspace 결과의 Project canonical 반영, concurrent Verify 조정, 실제 네트워크 요청과 운영 서비스 효과도 아직 구현하거나 증명하지 않았다. POSIX Verify timeout은 같은 process group의 일반 descendant까지 다루지만 스스로 새 session으로 분리한 process와 비-POSIX descendant 전체 종료는 보장하지 않는다. Harness 계약은 저장소가 신뢰하는 입력이며 악의적인 검증 프로그램을 격리하는 sandbox가 아니다. Receipt와 status는 각각 atomic하게 쓰지만 하나의 transaction으로 묶이지 않는다.
