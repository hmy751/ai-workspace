# Workspaces

이 디렉터리는 [`Work context`](../README.md) 안에서 실제 작업을 복구하고 이어 가는 Workspace들의 지속 상태를 소유한다.

- [`index.json`](index.json): 기본 명령이 사용할 active Workspace를 선택한다.
- 각 Workspace 디렉터리: 하나의 작업 정체성, 책임별 실행 계약, 현재 context, 선택한 원자료, goal 산출물 지도, 누적 기록을 함께 둔다.

각 Workspace의 내부 관계는 해당 `README.md`에서 시작한다. Harness는 이 자료를 읽고 갱신하는 관리 장치이며 Workspace의 목표, Project 기준, 사람의 판단을 소유하지 않는다.

## Workspace 내부 경계

- `workspace.json`: Workspace id와 schema를 가진 machine identity
- `recover.json` schema `2`: Project-root 상대 경로로 recover가 읽을 `context/project/` 문서와 선택 이유
- `verify.json`: verify가 실행할 고정 argv, evidence, 실행 제한, 결과별 다음 행동
- `current/`: 다음 작업자가 이어받을 현재 유효 context와 schema `2` machine status. `current/memory/`는 `index.md`, `01-goal.md`, `02-constraints.md`, `03-project-context.md`를 최소 구성으로 가진다.
- `source/`: 이 Workspace가 작업 입력으로 선택한 원문, 변경하지 않은 snapshot, provenance를 분리·보존하는 층. `source/index.md`를 최소 inventory로 두며 별도 원자료가 없으면 그 사실과 Project canonical을 복제하지 않은 경계를 적는다. 원자료의 저자와 정본 권위는 원래 출처에 남으며, Workspace는 선택 범위·사용 시점·무결성·재접근 경로를 관리한다. 현재 판단, 분석, 결정, 실행·검증 기록은 두지 않는다.
- `output/`: Workspace goal을 위해 선택된 현재 산출물을 찾는 층. `output/index.md`를 최소 산출물 지도로 두고, 실제 산출물이 Project root의 코드·문서·테스트에 있으면 복제하지 않고 canonical 상대 경로를 연결한다. Workspace 안에서만 소유하는 goal 산출물은 이 폴더에 직접 둘 수 있다. 아직 선택된 산출물이 없으면 index에 없다고 명시한다.
- `records/`: source와 실제 작업을 바탕으로 만든 분석·결정·실행·검증 기록과 append-only verification receipt. 분석 메모·후보·비교·탈락안·선택 근거처럼 goal 산출물을 만들고 고른 과정도 여기에 날짜와 내용을 드러내어 누적한다. `status.json`의 receipt 경로는 Work root 상대다.

`source/`는 Project 전체가 공유하는 canonical인 [`context/project/`](../../project/)를 복제하는 곳이 아니다. 원자료를 다시 확인해야 할 때 사람이 필요한 항목만 선택해서 읽으며, `recover`는 `source/` 전체나 inventory를 기본 recovery packet에 싣지 않는다.

Source 항목에는 가능한 범위에서 원래 위치나 URL, 확보 시각과 방법, commit·version·SHA-256 같은 안정적인 식별 근거를 함께 둔다. 해석이나 결론이 생기면 source를 고치지 않고 `current/` 또는 `records/`에 분리한다.

`output/`은 `records/`에서 일부 파일을 자동 승격하거나 복제하는 archive가 아니다. 사람이 goal의 현재 결과로 선택한 산출물과 canonical 위치를 보여 주며, 선택 이유와 이전 후보는 `records/`에 남긴다. `output/`에 있다는 사실만으로 검증 통과, 사람의 수락, Workspace 완료가 되지 않는다. `recover`는 `output/index.md`만 기본 packet에 싣고 연결된 산출물 본문은 필요할 때 선택해서 읽게 한다.

Recover와 verify 구현의 목적·입력·출력은 각각 [`../harness/recover/`](../harness/recover/)와 [`../harness/verify/`](../harness/verify/)가 정의한다.
