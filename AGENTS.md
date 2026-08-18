# context-harness local instructions

## Context contract

context 층의 canonical 역할은 `context/README.md`가 소유한다.

- `context/workspaces/`: 서로 다른 작업의 current, goal output, records를 Workspace별로 분리한다.
- 각 Workspace의 `README.md`: 해당 작업의 정체성·범위·재진입 순서를 정의한다.
- 각 Workspace의 `current/`: 다음 세션이 바로 행동하기 위해 읽는 현재 상태. 작업 단계가 바뀌어도 계속 유효한 `memory.md`와 빠르게 바뀌는 `state.md`로 나눈다.
- 각 Workspace의 `output/`: 해당 Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치를 찾는 층. 기존 Project 경로에 산출물이 있으면 복제하지 않고 `output/index.md`에서 가리킨다.
- 각 Workspace의 `records/`: 해당 작업에서 만든 지속 가능한 문서·분석·중간 산출물·검증 기록의 누적층. 사람이 읽는 날짜별 기록은 바로 아래에, 기계가 생성한 JSON 증거는 `records/receipts/<종류>/`에 분리한다. 여기에 있다는 이유만으로 현재 상태가 되지는 않는다.
- `context/source/`: 여러 Workspace가 필요할 때 선택해서 읽는 원자료와 provenance. 현재 판단이나 새 해석을 쓰지 않는다.
- 루트 `reference-project/`: 이 저장소가 만드는 실행 가능한 기준 Project. Workspace `output/`은 이를 복제하지 않고 goal과 실제 산출물의 선택 관계만 연결할 수 있다.
- `.agents/skills/`: 이 저장소에서 반복할 작업 절차. 실행 원형이나 실제 적용 기록을 복제하지 않는다.

## Repo-local skill routing

사용자가 대상 Project 경로와 함께 `reference-project/`의 context+harness 이식·적용, 실제 Project common context, Workspace current/source/output/records와 recover·verify 설치를 요청하면 [`.agents/skills/apply-context-harness/SKILL.md`](.agents/skills/apply-context-harness/SKILL.md)를 사용한다.

이 skill은 `reference-project/`를 범용 템플릿처럼 복사하지 않는다. 대상의 기존 canonical과 사용자 변경을 먼저 고정하고, `context/project/`에는 target 원자료가 지지하는 실제 Project common context를 구성한다. 이식 뒤에는 `recover → 실제 Owner의 direct test·eval·수동 확인 → 필요할 때만 Verify evidence 기록 → 다음 recover`를 구분해 검증한다. 기존 문서를 복제하거나 링크만 모은 Project context는 완료로 보지 않는다. 브라우저·외부 시스템·사람 acceptance, target commit은 별도 승인 없이 완료 처리하지 않는다.

## Re-entry

지속 작업을 시작할 때는 `context/README.md`와 `context/workspaces/README.md`에서 Workspace를 선택한다. 사용자가 Workspace를 명시했다면 그 지시를 우선하고, 그렇지 않으면 active Workspace를 사용한다.

선택한 Workspace의 `README.md`, `current/index.md`, `current/memory.md`, `current/state.md`, `output/index.md`를 읽는다. 다른 Workspace의 current·output·records나 shared source 전체를 기본으로 읽지 않고, 현재 질문에 필요한 자료만 선택한다.

## Context maintenance routing

자동 Maintain hook과 agent는 clean-room 재구현 동안 의도적으로 비활성이다. [`.codex/hooks.json`](.codex/hooks.json)은 빈 hook 집합만 가지며, [`.codex/config.toml`](.codex/config.toml)은 Maintainer를 등록하지 않는다. 삭제된 Reference runtime이나 이전 root Observe runtime을 임시로 다시 연결하지 않는다.

현재 clean-room 작업의 canonical은 [Workspace 007](context/workspaces/007-maintain-clean-room-reimplementation/)이다. Workspace 005와 006의 구현 topology는 새 설계를 자동으로 구속하지 않는다. 같은 구조를 유지하거나 피해야 할 의무 없이, 당시 근거·실패와 현재 Reference·host 조건에서 다시 판단한다.

그동안 main은 선택한 Workspace의 `README.md`, `current/`, `output/`, 필요한 `records/`를 직접 읽고 관리한다. 계속 보존할 판단·분석·검증이 생기거나 목표·현재 상태·다음 행동이 바뀌면 해당 Workspace 문서에 반영하되, 일회성 탐색 출력은 누적하지 않는다. 실제 파일·Git·test 결과와 대조하지 않은 상태를 fresh 또는 완료라고 기록하지 않는다.

새 Maintain 구현은 행동 계약과 책임 배치를 먼저 확정하고 실제 host에서 시작·연속 대화·response-end·실패 장면을 검증한 뒤에만 root에 다시 연결한다. Workspace 005의 구현 topology와 Workspace 006의 중단된 재구성은 active architecture도 금지 목록도 아닌 역사적 근거다.

## Source boundary

`context/source/`의 raw snapshot과 prior-work snapshot은 읽기 전용 원본으로 취급한다. 새 해석이나 현재 판단을 source에 쓰지 않는다. 사용자가 지정하지 않은 다른 Desktop 저장소로 조사 범위를 넓히지 않는다.
