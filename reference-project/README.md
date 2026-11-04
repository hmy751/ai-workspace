# Personal·Project·Work context reference

이미 존재하는 개발 Project에서 한 Workspace가 필요한 Project 맥락만 복구하고, 작업 중 의미 변화와 실제 검증 결과를 서로 다른 책임으로 유지한 뒤 다음 재진입 상태로 넘기는 실행 가능한 reference다.

이 reference는 Personal·Project·Work context를 상위 경계로 두고, 실제 제품과 관리 장치의 관계를 함께 보여 준다.

- **Personal context**: [개인 기준과 경험](context/personal/README.md)이 여러 작업에 적용할 관점·조건과 협업 경험·열린 후보를 구별해 소유한다.
- **Project context**: [`context/project/`](context/project/)가 여러 작업이 공유하는 의미, 교체되는 현재 현실과 관련 작업의 계약·판단 기준을 `common/current/guidance` 물리 layer로 나눠 소유한다. `REFERENCE/`는 본문 구성·읽기 기준을 소유한다.
- **Work context**: [`context/work/`](context/work/)가 여러 Workspace와 공용 Harness의 운영 관계를 소유한다.
- **제품**: [`src/`](src/)와 [`tests/test_config_loader.py`](tests/test_config_loader.py)가 실제 구현과 제품 검증을 소유한다.

Harness는 Work 안에서 Recover의 읽기 전용 복구와 Verify의 제품 증거 기록을 맡는다. 작업 중 의미·과정의 기록은 [record-work](.agents/skills/record-work/SKILL.md)의 서브가 원문을 읽고 직접 수행한다. 필요할 때 호출하고 같은 대화에서 재사용하며 기존 자동 Maintain과 hook·binding·guarded apply는 제거했다.

## 시작점

전체 context 관계는 [context README](context/README.md), 사람이 현재 작업을 볼 때는 [active Workspace README](context/work/workspaces/001-default-timeout/README.md)에서 시작한다. 새 Workspace를 만드는 사람은 [생성·전환 canonical](context/work/workspaces/CREATE-AND-TRANSITION.md), 실행하는 AI는 repo-local [Workspace 생성 skill](.agents/skills/create-context-workspace/SKILL.md)에서 시작한다. Work·Harness의 AI 운영 지침은 [Work AGENTS](context/work/AGENTS.md), Harness 책임과 workflow는 [Harness README](context/work/harness/README.md)에서 시작한다.

필요한 맥락은 [USAGE](context/USAGE.md)의 선택·대조·재사용 방법으로 읽고, 제품별 판단은 [Project 읽기 기준](context/project/REFERENCE/reading.md)을 따른다. Personal·Project의 허용된 갱신·누락 복원에는 [context-update](.agents/skills/context-update/SKILL.md)와 해당 영역의 관리 계약을 사용한다. Work 기록은 record-work와 대상 작성 기준을, 생성·전환은 해당 Work 계약을 따른다.

Work를 구체화하거나 실제 결과에 따라 판단을 다시 보고, 코드·작업물·앞선 설명을 이해할 때는 [스킬 색인](.agents/skills/README.md)에서 해당 역할과 호출 조건을 찾는다. `work-discussion`의 명시 호출 조건과 `reconsider-work`의 기존 역할을 유지하며, 설명은 `explain`으로 연결한다. [공통 설명과 근거 기준](.agents/skills/shared/explanation-and-evidence-criteria.md)은 `work-discussion`과 `explain`이 필요한 때 읽는다.

실제 명령은 `reference-project/` root에서 실행한다.

```bash
python3 -m context.work.harness recover 001-default-timeout
python3 -m context.work.harness verify 001-default-timeout
python3 -m unittest discover -s . -p 'test_*.py' -v
```

- `recover`: 명시한 Workspace를 우선하고 id가 없을 때만 active 기본값을 사용해, 필요한 current와 선택된 Project context를 read-only recovery packet으로 만든다.
- `verify`: claim·canonical basis·evidence를 실행 전에 snapshot하고 고정 argv를 제한 안에서 실행한 뒤 receipt와 machine status만 갱신한다.
- 전체 test discovery: 제품 테스트와 임시 fixture에서 실행되는 Harness validation을 포함한 책임별 테스트를 실행한다. Active 제품 Workspace의 receipt와 status는 바꾸지 않는다.

## 구조

```text
.
├── .agents/
│   └── skills/
│       ├── README.md                 # 설치 스킬의 역할·canonical·연결 색인
│       ├── create-context-workspace/ # 설치 뒤 새 Workspace 생성·재진입 검토
│       ├── record-work/             # 필요 시 원문 판단·Work 직접 기록
│       ├── context-update/          # Personal·Project의 한정 반영
│       ├── work-discussion/          # 명시 호출로 Work 구체화
│       ├── reconsider-work/          # 실제 결과에 따른 재판단
│       ├── explain/                 # 뜻·동작·선택 이유와 앞선 말 설명
│       ├── shared/                  # 소비자가 선택하는 공통 설명 기준
│       └── SKILLS-CONTENT-POLICY.md  # 스킬 본문·형성 자료 관리
├── .claude/skills/               # 설치 스킬 원본의 상대 연결
├── .codex/
│   ├── skills/                  # 같은 스킬 원본으로 상대 연결
│   ├── config.toml               # 전용 Maintain agent 등록 없음
│   ├── hooks.json                # 빈 자동 hook 집합
├── AGENTS.md                     # 책임별 하위 지침을 찾는 최소 router
├── src/                          # 실제 제품 코드
├── tests/
│   └── test_config_loader.py     # 제품 동작 검증
└── context/
    ├── README.md                 # Personal·Project·Work의 관계
    ├── USAGE.md                  # 질문별 읽기·대조·재사용
    ├── CONTENT-POLICY.md         # Personal·Project 본문·형성 자료 관리
    ├── SYSTEM-GUIDANCE.md        # 체계 지침의 역할·진입·분할
    ├── _background/             # 공통 지침의 형성 근거
    ├── personal/                # 개인 판단·사례·협업 경험
    ├── project/                  # 실제 Project-wide 판단 context
    │   ├── README.md             # 물리 layer·Owner routing anchor
    │   ├── REFERENCE/            # 본문 구성·읽기 판단 기준
    │   ├── common/               # 지속되는 제품·domain 의미
    │   │   ├── README.md
    │   │   └── prd.md
    │   ├── current/              # 교체되는 구현·지원·proof 경계
    │   │   ├── README.md
    │   │   └── architecture.md
    │   ├── guidance/             # 조건부 Project-wide 판단 기준
    │   │   └── README.md
    │   └── decisions/            # 선택 이유와 재검토 신호
    │       ├── README.md
    │       └── 0001-default-timeout.md
    └── work/
        ├── README.md             # Work context 운영 경계
        ├── AGENTS.md             # Work·Harness 운영과 기록 담당 연결
        ├── harness/              # 교체 가능한 Workspace 관리 장치
        │   ├── recover/          # 읽기 전용 재진입
        │   ├── verify/           # durable 제품 검증 증거
        │   └── validation/       # 제품 상태를 보존하는 Harness 자체 검증
        └── workspaces/
            ├── README.md         # 지속 Workspace collection 경계
            ├── CREATE-AND-TRANSITION.md # 생성·전환 end-to-end canonical
            ├── SPEC-AND-TICKETS.md # 이전 링크를 새 canonical로 연결하는 안내
            ├── spec-and-tickets/   # 실행·Spec·Ticket·갱신 기준과 선택 이력
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

각 Workspace는 `current/`, `source/`, `output/`, `records/`를 형제로 둔다. `current/memory/`에는 [Spec 다섯 파일·Ticket·Project context 선택](context/work/workspaces/spec-and-tickets/README.md)을 두고, state는 전체 상황·판단·다음 행동을 맡는다. `source/`에는 해당 Workspace가 선택한 원문·snapshot·provenance만 둔다. 분석 메모·후보·비교·탈락안·선택 근거를 포함한 과정은 `records/` 바로 아래 날짜별 기록이 맡고, 기계가 생성한 검증 증거는 `records/receipts/<종류>/`에 분리한다. Goal을 위해 선택된 현재 산출물은 [`output/index.md`](context/work/workspaces/001-default-timeout/output/index.md)에서 찾게 한다. 이 sample의 실제 제품 구현은 Project root의 canonical을 연결하며 Workspace 안에 복제하지 않는다.

Project 문서 전체를 Workspace에 복사하지 않는다. 이 Workspace의 [`recover.json`](context/work/workspaces/001-default-timeout/recover.json)은 안정된 [`Project routing anchor`](context/project/README.md), goal에 지속해서 적용되는 [`제품 기준`](context/project/common/prd.md), 지금의 구현·검증 경계를 보여 주는 [`architecture`](context/project/current/architecture.md), 직접 적용할 [`default timeout 결정`](context/project/decisions/0001-default-timeout.md)을 이유와 함께 선택한다. 현재 default-timeout 제품 작업은 설명 스킬의 공통 기준을 기본 입력으로 요구하지 않으므로 [`guidance`](context/project/guidance/README.md)를 recovery context에는 선택하지 않는다. Workspace `source/`와 `records/` 전체, Workspace `output/index.md`가 연결한 산출물 본문도 기본 recovery context에 들어가지 않는다. README는 문서 위치를 찾게 할 뿐 실제 내용 선택을 대신하지 않는다.

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

이 reference의 결정적 실행 장치는 명시 또는 active-default Workspace의 선택적 복구와 claim·canonical basis·evidence snapshot, 고정 검증 실행, receipt·machine status·선언된 snapshot freshness의 재복구를 다룬다. 임시 fixture 회귀는 active 제품 상태를 바꾸지 않는다.

record-work는 원문 해석·문서 수정·같은 서브 재사용의 실행 지침이다. 기존 guarded apply의 경로·preimage·schema 거부 보장을 그대로 제공하지 않으며 지침과 host의 실제 권한으로 범위를 지킨다. 설치·정적 검사·unit test만으로 실제 host의 발견·호출·서브 재사용·기록 품질·재개 효과를 증명하지 않는다. 기존 자동 Maintain의 코드는 Git 이력에서 복구할 수 있고 현재 실행 목록에는 두지 않는다.

Workspace 생성의 의미 충분성·사람 수락·전체 완료, concurrent Verify 조정·실제 네트워크·운영 서비스 효과는 별도다. POSIX Verify timeout은 같은 process group의 일반 descendant를 다루지만 스스로 새 session으로 분리한 process와 비-POSIX descendant 전체 종료를 보장하지 않는다. Harness 입력은 신뢰된 계약이며 악의적인 프로그램을 격리하는 sandbox가 아니다. Receipt와 status는 각각 atomic하지만 하나의 transaction은 아니다.

Project·Personal의 반영은 context-update와 해당 Owner의 관리 계약을 적용한다. Work 결과를 자동 승격하지 않으며 기록 반영·제품 검증·다음 실제 사용 효과를 구별한다.
