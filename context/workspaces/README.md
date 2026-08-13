# Workspaces

이 디렉터리는 `context-harness` 저장소에서 서로 다른 작업의 현재 상태와 누적 기록을 분리한다. Workspace마다 자기 `README.md`, `current/`, `records/`를 소유하며 다른 Workspace의 상태를 이어 쓰지 않는다.

## Active Workspace

- active: [`002-project-application`](./002-project-application/)
- completed reference: [`001-reference-implementation`](./001-reference-implementation/)

사용자가 특정 Workspace를 지목하면 그 지시가 active 표기보다 우선한다. active 변경은 새 작업을 시작하거나 작업 책임을 명시적으로 전환할 때만 반영한다.

## 공통 규칙

- `current/memory.md`: 해당 Workspace 안에서 작업 단계가 바뀌어도 계속 유효한 목표·기준·결정·제약
- `current/state.md`: 지금의 문제·상태·근거·불확실성·다음 행동
- `records/`: 해당 Workspace에서 만든 지속 가능한 상세 기록
- 루트 [`../source/`](../source/): Workspace들이 필요할 때 선택해서 읽는 공유 원자료

완료된 Workspace의 상세 과정은 records에 남기고, 다른 Workspace로 통째로 복제하지 않는다. 새 Workspace는 이전 결과 중 지금 작업에 필요한 결론과 근거 접근점만 자기 current에 선택해 둔다.
