# Workspaces

이 디렉터리는 `context-harness` 저장소에서 서로 다른 작업의 현재 상태, goal 산출물, 누적 기록을 분리한다. Workspace마다 자기 `README.md`, `current/`, `output/`, `records/`를 소유하며 다른 Workspace의 상태를 이어 쓰지 않는다.

## Active Workspace

- active: [`006-maintain-behavior-responsibility-allocation`](./006-maintain-behavior-responsibility-allocation/)
- completed maintain implementation: [`005-context-continuity-maintenance`](./005-context-continuity-maintenance/)
- paused maintenance implementation: [`004-harness-maintenance-bottleneck`](./004-harness-maintenance-bottleneck/)
- paused application: [`002-project-application`](./002-project-application/)
- ready: [`003-project-application`](./003-project-application/)
- completed reference: [`001-reference-implementation`](./001-reference-implementation/)

사용자가 특정 Workspace를 지목하면 그 지시가 active 표기보다 우선한다. active 변경은 새 작업을 시작하거나 작업 책임을 명시적으로 전환할 때만 반영한다.

## 공통 규칙

- `current/memory.md`: 해당 Workspace 안에서 작업 단계가 바뀌어도 계속 유효한 목표·기준·결정·제약
- `current/state.md`: 지금의 문제·상태·근거·불확실성·다음 행동
- `output/index.md`: Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치. 기존 Project 경로에 산출물이 있으면 복제하지 않고 가리킨다.
- `records/`: 분석 초안, 후보 비교, 탈락 사유, 시행착오, 결정 근거, 중간 산출물, 검증처럼 결과가 만들어진 과정의 지속 기록. 사람이 읽는 날짜별 기록은 바로 아래에 두고, 기계 JSON은 `records/receipts/<종류>/`에 격리한다.
- 루트 [`../source/`](../source/): Workspace들이 필요할 때 선택해서 읽는 공유 원자료

파일 형식만으로 output과 records를 나누지 않는다. 분석 문서라도 Workspace goal의 결과로 선택됐으면 output에서 찾게 하고, 선택 전 후보·선택 이유·교체된 이전 결과는 records에 남긴다. Output에 있다는 사실만으로 acceptance나 완료가 되지는 않으며 상태와 검증 상한은 current와 output index에서 구분한다.

완료된 Workspace의 상세 과정은 records에 남기고, 다른 Workspace로 통째로 복제하지 않는다. 새 Workspace는 이전 결과 중 지금 작업에 필요한 결론과 근거 접근점만 자기 current에 선택해 둔다.

기계 receipt를 만드는 Harness나 helper는 생성 주체일 뿐 보존 Owner가 아니다. Receipt가 증명하는 작업과 수명주기는 해당 Workspace가 소유한다. 반복 개발 확인은 직접 test 명령을 사용하고, 상태 전환·인계에 필요한 실행만 durable receipt로 남긴다.
