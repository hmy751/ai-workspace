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

이 skill은 `reference-project/`를 범용 템플릿처럼 복사하지 않는다. 대상의 기존 canonical과 사용자 변경을 먼저 고정하고, `context/project/`에는 target 원자료가 지지하는 실제 Project common context를 구성한 뒤 Workspace·Harness와 `recover → verify → recover`를 durable receipt로 검증한다. 기존 문서를 복제하거나 링크만 모은 Project context는 완료로 보지 않는다. 브라우저·외부 시스템·사람 acceptance, target commit은 별도 승인 없이 완료 처리하지 않는다.

## Re-entry

지속 작업을 시작할 때는 `context/README.md`와 `context/workspaces/README.md`에서 Workspace를 선택한다. 사용자가 Workspace를 명시했다면 그 지시를 우선하고, 그렇지 않으면 active Workspace를 사용한다.

선택한 Workspace의 `README.md`, `current/index.md`, `current/memory.md`, `current/state.md`, `output/index.md`를 읽는다. 다른 Workspace의 current·output·records나 shared source 전체를 기본으로 읽지 않고, 현재 질문에 필요한 자료만 선택한다.

## Context maintenance routing

다음 중 하나가 생긴 작업은 자연스러운 종료 경계에서 `context_maintainer` subagent에게 대상 Workspace를 명시해 context 정합성 점검을 한 번 맡긴다.

- 계속 보존할 작업 문서·분석·중간 산출물·검증 기록이 생김
- 해당 Workspace의 목표·기준·제약, source 선택 또는 output 경계가 바뀜
- 현재 문제·상태·불확실성·작업 커서·다음 행동이 바뀜
- 결정, 실패, blocker, 검증, 완료, 폐기로 현재 영향이 달라짐
- 대상 Workspace의 `current/`가 실제 파일·Git 상태·test 결과·사용자 정정과 어긋날 가능성이 생김

일회성 탐색이나 임시 명령 출력을 매번 records로 만들지는 않는다. 다만 후속 작업에서 다시 사용할 분석이나 결과라면 상태 변화가 없어도 대상 Workspace의 records에 보존한다. 반복 개발 확인은 직접 test 명령을 우선하고, durable machine receipt는 상태 전환이나 인계에 필요한 검증에 사용한다.

`context_maintainer`는 지정한 Workspace만 갱신한다. 다른 Workspace의 current·records를 합치거나 active를 임의로 바꾸지 않는다. 사용자가 Workspace 전환을 결정한 경우에만 `context/workspaces/README.md`의 active 표기를 바꾼다.

`context_maintainer`가 수정한 diff와 근거는 main이 검토한다. 사용자 목표·승인 결정·새로운 설계 기준을 subagent가 대신 확정하게 하지 않는다. agent를 호출할 수 없는 환경이면 main이 같은 점검을 수행하고 그 사실을 보고한다.

## Source boundary

`context/source/`의 raw snapshot과 prior-work snapshot은 읽기 전용 원본으로 취급한다. 새 해석이나 현재 판단을 source에 쓰지 않는다. 사용자가 지정하지 않은 다른 Desktop 저장소로 조사 범위를 넓히지 않는다.
