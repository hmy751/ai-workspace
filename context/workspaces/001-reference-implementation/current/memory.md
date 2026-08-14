# Current memory

마지막 갱신: `2026-08-14`

## 목표

실제 개발 프로젝트에서 사람과 AI가 프로젝트의 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 다시 지속 상태에 반영할 수 있게 하는 context+harness 운영 구조를 만든다.

## 현재 정의된 context 역할

- **Project common context**: 장기간 유지되는 목표, 기준, 결정, 제약
- **Work context**: 특정 작업의 문제, 현재 상태, 근거, 불확실성, 다음 행동

이 reference 구현 Workspace에서 작업 단계가 바뀌어도 계속 유효한 내용은 이 파일이, 빠르게 바뀌는 상태는 [`state.md`](./state.md)가 소유한다. `current`와 `records`는 context를 운영하고, `source`는 선택한 원자료를 분리하며, `output`은 goal을 위해 선택된 결과를 찾게 하는 저장 층위다. 이들은 Project common context나 Work context와 별개의 새 context 역할이 아니다.

## 만들려는 것

- 이미 개발 프로젝트가 있다고 가정하고 그 안에서 실제로 돌아가는 운영 구조
- 사람과 AI가 현재 상태를 복구하고, 필요한 context만 선택해 행동하는 구조
- 검증 결과가 일회성 출력으로 끝나지 않고 지속 상태에 다시 반영되는 구조
- work context의 층위와 이를 유지·보완하는 harness가 연결된 시스템

설치 패키지 자체가 목표는 아니다. 운영 흐름과 상태의 연결이 먼저 보여야 한다.

## 이 작업대에 채택한 운영 경계

- `context/workspaces/`: 서로 다른 작업의 current, goal output, records를 Workspace별로 분리한다.
- 이 Workspace의 `current/`: reference 구현 작업에서 계속 유효한 memory와 최종 state.
- 이 Workspace의 `output/`: 이 작업의 goal을 위해 선택된 현재 산출물과 실제 canonical 위치의 진입점. 실제 기준 Project는 루트 `reference-project/`에 두고 복제하지 않는다.
- 이 Workspace의 `records/`: reference 구현 중 만든 지속 가능한 문서·분석·중간 산출물·검증 기록.
- 루트 `context/source/`: 이 작업대의 Workspace들이 필요할 때 선택해서 읽는 reference 설계 원자료와 provenance의 읽기 전용 공유 층. `reference-project/`의 개별 Workspace source로 자동 복제하지 않는다.
- 루트 `reference-project/`: 이 Workspace가 만든 실행 가능한 기준 Project. 과정 분석이나 context 기록을 대신 보관하지 않는다.
- `reference-project/`라는 이름은 Workspace별 goal 결과 지도인 `output/`과 루트 기준 Project를 구분한다. 새 Project에 통째로 복사하는 starter kit가 아니라, 이식 뒤의 책임 구조와 실행 계약을 보여 주는 기준 구현이다.

## output에 적용할 Project–Workspace 관계

- 이미 존재하는 개발 Project의 PRD, architecture, 공통 결정·제약은 상위 canonical 맥락이다.
- 실제 작업은 여러 Workspace 단위로 운영하며, 각 Workspace는 필요한 상위 Project 맥락만 선택해 접근점을 유지한다.
- `reference-project/context/`는 Project context와 Work context의 관계를 묶는 상위 경계다. `context/project/`는 여러 작업이 공유하는 Project common context를, `context/work/`는 Harness와 Workspace collection이 함께 이루는 Work context 운영 경계를 소유한다.
- Harness는 개별 Workspace의 내용이 아니라 여러 Workspace가 공유하는 교체 가능한 관리 장치다. `context/work/` 안에서 `workspaces/`와 형제로 두되, 제거해도 각 Workspace의 의미·current·source·output·records를 이해할 수 있어야 한다.
- `workspaces/` 이름은 유지한다. 현재의 모호함은 이름보다 Project root에 독립 구성처럼 노출된 배치에서 생겼으며, `context/work/` 아래에서는 Workspace 인스턴스 collection이라는 역할이 분명하다.
- Workspace의 `current`는 `memory/`와 `state/` 폴더로 나눈다. `memory/index.md`와 주제별 문서는 계속 유효한 현재 맥락을, `state/index.md`는 사람이 읽는 현재 문제와 해석을, `state/status.json`은 harness가 갱신하는 최근 결과와 다음 행동을 소유한다.
- 각 Workspace는 `current/`, `source/`, `output/`, `records/`를 형제로 둔다. `source/index.md`는 해당 작업이 선택한 원문·변경하지 않은 snapshot·provenance를 찾는 최소 inventory이며, 현재 판단은 `current/`, goal을 위해 선택된 현재 산출물과 canonical 위치는 `output/index.md`, 분석·결정·실행·검증 기록은 `records/`에 둔다.
- 원자료의 저자와 정본 권위는 원래 출처에 남는다. Workspace는 선택 범위·사용 시점·snapshot 무결성·재접근 경로와 다른 층과의 분리를 책임진다.
- `current/memory/`의 `01-goal.md`, `02-constraints.md`, `03-project-context.md`는 최소 memory 계약이고, `output/index.md`는 필수 goal-output 지도다. Recover는 이 계약들의 존재를 검사하고 output index는 읽지만, Workspace `source/`나 index가 연결한 output artifact 본문은 검사하거나 기본 로드하지 않는다.
- 완료된 reference와 이식 target의 Project common context에는 `context/project/README.md`와 실제 내용의 `overview.md`가 필요하다. README는 책임·상세 Owner·충돌 우선순위·갱신 조건을, overview는 여러 Workspace가 공통으로 사용할 목적·범위·구조·제약·채택 결정·검증 경계와 근거를 소유한다. 기존 docs의 복제본이나 링크 목록만으로는 이 계약을 충족하지 않는다.
- Output과 records는 파일 형식이 아니라 Workspace goal에서 맡는 역할로 구분한다. Output은 선택된 현재 결과의 지도이고, 후보·탈락 사유·선택 근거·교체된 이전 결과와 검증 과정은 records에 남는다. Output 등재는 acceptance나 완료를 뜻하지 않는다.
- `records/` 바로 아래에는 날짜가 있는 사람이 읽는 기록을 두고, 기계 JSON은 `records/receipts/{verify,harness-tests,preflight}/`로 종류를 분리한다. Harness와 helper는 producer이고 receipt 의미·수명주기의 Owner는 해당 Workspace다. 이전 flat `records/*.json`은 읽기 호환만 유지한다.
- 반복 개발 확인은 직접 test 명령을 사용하고, product `verify`는 Workspace 상태 전환이나 다음 사람·세션에 근거를 인계할 때 durable receipt를 남기기 위해 사용한다. 실행된 receipt는 자동 삭제·병합하지 않으며 retention 자동화는 별도 문제다.
- memory 폴더에 과거를 누적하지 않는다. 지금도 유효하고 기본 재진입에 필요한 주제만 두며, 상세 과정과 이전 상태·검증 receipt는 `records/`에 누적한다.
- Workspace 루트 `README.md`를 사람의 첫 화면으로 두고, machine 계약과 raw receipt를 읽기 전에 현재 문서의 위치와 읽는 순서를 찾게 한다.
- `workspace.json`은 Workspace identity, `recover.json`은 Project context 선택, `verify.json`은 고정 검증과 결과별 다음 행동을 소유한다.
- Harness는 상위 경계 아래 `recover`와 `verify`의 정의·구현·테스트를 각각 묶고, 두 책임이 실제로 공유하는 Workspace 선택·안전한 접근·status/receipt 인계만 공통 계약으로 둔다.
- `context/project/`는 완료된 이식 결과가 가져야 할 Project common context의 고정 경계다. 기존 README·STATUS·docs·코드·테스트가 소유한 상세 사실은 원래 Owner에 남기고 derived overview가 충돌하면 상세 Owner를 우선한다. 기존 Owner 자체의 이동은 별도 승인된 migration이다.
- Recover contract schema `4`는 Project context 선택을 `context/project/` 아래 regular Markdown으로 제한하고 `overview.md`를 첫 항목으로 요구한다. 이전 reference schema `2`와 첫 실제 적용의 target-local schema `3`은 재사용하지 않으며, packet schema는 `5`를 유지한다.
- Workspace 결과를 Project canonical에 반영하는 규칙과 Workspace 생성·완료·보관 수명주기는 아직 정하지 않았다.

이식 skill은 이 구조의 별도 정본이나 복제본이 아니다. 실행 가능한 기준 Project는 `reference-project/`가 소유하고, repo-local `apply-context-harness` skill은 대상 Project의 기존 canonical과 실제 source에 맞춰 그 책임을 적용·검증하는 절차만 소유한다.

최초 합의와 미결정 범위는 [`Project–Workspace context 운영 구조 합의`](../records/2026-08-13-03-project-workspace-context-agreement.md), 사람용·기계용 current 분리는 [`Workspace current 폴더화`](../records/2026-08-13-05-workspace-current-folder-migration.md), 수락된 Harness 책임 배치는 [`Harness 책임 경계 재구성`](../records/2026-08-13-06-harness-responsibility-boundary-refactor.md), Project context와 Work context의 물리적 상위 경계 결정은 [`Project·Work context 상위 경계 재구성`](../records/2026-08-13-07-project-work-context-boundary.md), Workspace source와 최소 memory 계약은 [`Workspace source 층과 최소 memory 계약`](../records/2026-08-14-01-workspace-source-layer-and-minimum-memory.md), goal output 지도와 records 경계는 [`Workspace output 층과 records 경계`](../records/2026-08-14-02-workspace-output-layer-and-record-boundary.md), 실제 Project overview와 recover 계약은 [`실제 Project overview와 recover 계약`](../records/2026-08-14-03-project-overview-and-recover-contract.md), 루트 이름 변경과 재검증은 [`기준 Project 루트 이름 변경`](../records/2026-08-14-04-reference-project-root-rename.md), machine receipt 배치와 durable verify 운용은 [`Machine receipt 경계와 durable verify 운용`](../records/2026-08-14-05-machine-receipt-boundary-and-durable-verify.md)에 있다.

## 현재 context 유지 장치

- repo-local `context_maintainer` subagent가 자연스러운 작업 경계에서 records 누락과 current drift·비대화를 함께 점검한다.
- `AGENTS.md`가 호출 조건을 소유하고, main이 subagent 결과의 채택과 사용자 판단 경계를 소유한다.
- agent는 근거가 명확한 current/records만 갱신하며 source 원본이나 프로젝트 목표를 독자적으로 바꾸지 않는다.
- agent 정의·등록·routing은 이 저장소 안에서만 소유하며 전역 agent·skill·프로젝트 색인·runtime 설정으로 승격하지 않는다.

## source 경계

아래 항목은 이 작업대의 공유 `context/source/`에 대한 권위 구분이다. `reference-project/`의 Workspace별 `source/`는 각 작업이 실제로 선택한 원자료 snapshot과 provenance만 분리·관리한다.

- Anthropic 공식 문서와 사용자가 선택한 발췌는 공식 참고 자료로 본다.
- 블로그 원문과 사용자가 선택한 발췌는 context+harness 관점을 구체화하는 참고 자료로 본다.
- 사용자가 공감해 가져온 Codex 의견은 설계 질문으로 보존하되, 사용자 승인 결정과 동일시하지 않는다.
- AX와 cofathon은 사용자가 실제로 작업한 방식을 관찰하는 자료이며 새 구조의 정답 원천은 아니다.
- 등록된 자료는 [`../../../source/manifest.json`](../../../source/manifest.json)에서 찾는다. 다른 Desktop 저장소는 source로 확장하지 않는다.
