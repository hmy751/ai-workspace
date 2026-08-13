# Workspaces

이 디렉터리는 [`Work context`](../README.md) 안에서 실제 작업을 복구하고 이어 가는 Workspace들의 지속 상태를 소유한다.

- [`index.json`](index.json): 기본 명령이 사용할 active Workspace를 선택한다.
- 각 Workspace 디렉터리: 하나의 작업 정체성, 책임별 실행 계약, 현재 context, 누적 기록을 함께 둔다.

각 Workspace의 내부 관계는 해당 `README.md`에서 시작한다. Harness는 이 자료를 읽고 갱신하는 관리 장치이며 Workspace의 목표, Project 기준, 사람의 판단을 소유하지 않는다.

## Workspace 내부 경계

- `workspace.json`: Workspace id와 schema를 가진 machine identity
- `recover.json` schema `2`: Project-root 상대 경로로 recover가 읽을 `context/project/` 문서와 선택 이유
- `verify.json`: verify가 실행할 고정 argv, evidence, 실행 제한, 결과별 다음 행동
- `current/`: 다음 작업자가 이어받을 현재 유효 context와 schema `2` machine status
- `records/`: 상세 작업 기록과 append-only verification receipt. `status.json`의 receipt 경로는 Work root 상대다.

Recover와 verify 구현의 목적·입력·출력은 각각 [`../harness/recover/`](../harness/recover/)와 [`../harness/verify/`](../harness/verify/)가 정의한다.
