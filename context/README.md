# context

실제 개발 프로젝트에서 사람과 AI가 프로젝트 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 지속 상태에 다시 반영할 수 있게 하는 context+harness 운영 구조를 탐구하는 작업대다.

## 구성

- [`workspaces/`](./workspaces/): 서로 다른 작업의 현재 상태, goal 산출물, 누적 기록을 Workspace별로 분리한다.
- [`source/`](./source/): 여러 Workspace가 필요에 따라 선택해서 읽는 원본, 사용자 선택 발췌, AI 의견, 기존 작업 관찰 자료와 provenance다.

루트 [`../reference-project/`](../reference-project/)는 context 층이 아니라 이 저장소가 만드는 실행 가능한 기준 Project다. Workspace의 과정 분석·후보·결정·검증 기록은 해당 Workspace의 `records/`에 두고, goal을 위해 선택된 현재 산출물은 Workspace `output/index.md`에서 찾는다. 실제 산출물이 루트 `reference-project/`나 다른 canonical 경로에 있으면 Workspace 안에 복제하지 않는다.

## Workspace 경계

각 Workspace는 하나의 작업 맥락을 소유한다.

- `README.md`: 작업의 정체성·범위·사람이 읽는 순서
- `current/`: 다음 세션이 바로 행동하는 데 필요한 현재 상태
- `output/`: Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치의 진입점
- `records/`: 분석 초안·후보 비교·탈락 사유·결정 근거·시도·검증처럼 결과가 만들어진 과정의 지속 기록

지금까지의 source 정리와 실행 가능한 reference 구현은 [`001-reference-implementation`](./workspaces/001-reference-implementation/)에 보존한다. 새 적용 작업은 [`workspaces/`](./workspaces/)에서 서로 독립된 Workspace로 시작한다.

이 작업대에는 `reference-project/context/work`의 Harness, JSON 계약, machine status를 그대로 복제하지 않는다. 여러 작업의 현재 상태와 기록이 섞이지 않게 하는 Workspace 경계만 먼저 적용한다.

## 재진입

1. [`workspaces/README.md`](./workspaces/README.md)에서 active Workspace를 확인한다. 사용자가 Workspace를 명시했다면 그 지시를 우선한다.
2. 선택한 Workspace의 `README.md`와 `current/index.md`를 읽는다.
3. 선택한 Workspace의 `output/index.md`에서 현재 goal 산출물과 canonical 위치를 확인한다.
4. 현재 질문에 필요한 records만 선택해서 읽는다.
5. 판단 근거를 다시 확인해야 할 때만 [`source/`](./source/)를 연다.

다른 Workspace의 current, output, records는 비교·이관·검증에 필요하다고 명시된 경우에만 읽는다.
