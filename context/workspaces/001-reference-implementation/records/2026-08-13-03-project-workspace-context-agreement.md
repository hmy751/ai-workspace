# Project–Workspace context 운영 구조 합의

날짜: `2026-08-13`

## 이 기록의 역할

`output/`에 실제 산출물을 만들기 전에, 상위 Project와 개별 Workspace의 관계 및 Workspace 내부 context 경계를 대화에서 확정한 결과를 보존한다. 이 문서는 논의 결과와 아직 정하지 않은 범위를 함께 남기는 record이며, 현재 유효한 결론은 [`../current/memory.md`](../current/memory.md)에 압축한다.

## 합의한 구조

### 1. Project와 Workspace는 다른 층위다

- 이미 존재하는 개발 Project의 상위 맥락에는 PRD, architecture, 공통 결정과 제약처럼 여러 작업에 걸쳐 공유되는 canonical 문서가 있다.
- 실제 작업은 여러 Workspace 단위로 쌓인다. 하나의 Workspace는 하나의 작업 맥락을 복구하고 이어 가는 운영 단위다.
- Workspace는 상위 Project 문서 전체를 복사하거나 매번 전부 읽지 않는다. 현재 작업에 필요한 문서만 선택해 접근점을 유지한다.
- 상위 Project 자체의 폴더 구조나 `current/records` 적용 여부는 이번 합의에 포함하지 않는다.

### 2. Workspace의 current는 memory와 state로 나눈다

- `current/memory.md`: 작업 단계가 바뀌어도 계속 유효한 현재 맥락. Workspace의 목표·기준·유지되는 결정과 제약·계속 영향을 주는 결과·선택한 상위 Project 맥락을 소유한다.
- `current/state.md`: 빠르게 바뀌는 현재 작업 상태. 지금의 문제·진행 상태·근거·불확실성·최근 검증 결과·다음 행동을 소유한다.
- `memory`는 모든 과거를 쌓는 저장소가 아니다. 지금도 유효하고, 다음 세션이 모르면 판단이나 행동이 달라지는 내용만 유지한다.
- `state`에는 완료 과정이나 긴 분석을 누적하지 않는다. 지금 이어 갈 커서만 유지한다.

### 3. records는 Workspace에서 생긴 지속 가능한 작업 산출물의 누적층이다

- 분석, 설계, 시도, 결정, 구현 기록, 실패, 검증 결과처럼 후속 작업에서 다시 사용할 산출물을 누적한다.
- records에 있다는 사실만으로 현재 유효하거나 채택되었다는 뜻은 아니다.
- 상세 과정과 근거는 records에 남기고, 그중 계속 유효한 효과만 memory에, 현재 후속 행동만 state에 압축한다.

## 재진입과 반영 흐름

1. Workspace의 `current/memory.md`에서 계속 유효한 맥락과 선택된 상위 Project 접근점을 읽는다.
2. `current/state.md`에서 지금 상태와 다음 행동을 복구한다.
3. 현재 판단에 필요한 상위 Project 문서와 records만 선택해 읽는다.
4. 실제 프로젝트 산출물에 행동하고 기존 test·검증 수단으로 결과를 확인한다.
5. 상세 결과는 records에 남기고 state를 갱신한다.
6. 이후 작업에도 계속 영향을 주는 결과만 memory에 반영한다.

## 이름을 이렇게 정한 이유

- `scope.md`는 범위만 강조해 목표·결정·제약·지속 효과까지 맡는 역할보다 좁다.
- `brief.md`는 작업 정의 산출물의 의미가 강해, 계속 유지되는 현재 메모리와 다르다.
- `workspace.md`는 Workspace 폴더 안에서 이름이 중첩되고 파일의 역할을 설명하지 못한다.
- `project.md`와 `work.md`는 상위 Project와 Workspace라는 구조적 층위와 혼동된다.
- 따라서 역할을 직접 드러내는 `memory.md`와 `state.md`를 사용한다.

## 이 작업대에 적용한 변경

- `context/current/project.md`를 `context/current/memory.md`로 바꿨다.
- `context/current/work.md`를 `context/current/state.md`로 바꿨다.
- live 진입 문서와 repo-local maintainer의 참조를 새 이름에 맞췄다.
- 날짜가 붙은 과거 records와 `context/source/`의 보존 자료는 당시 맥락을 유지하기 위해 다시 쓰지 않았다.

## 아직 정하지 않은 것

- 상위 Project context의 구체적인 디렉터리 구조와 owner별 파일 형식
- Workspace 생성·완료·보관 수명주기와 식별 방식
- 선택한 상위 context와 선택 이유를 표현하는 구체적인 링크·manifest 형식
- Workspace의 결과를 상위 Project canonical context에 반영하는 owner·승인 규칙
- context를 읽고 검증 결과를 반영하게 할 harness의 구체적인 hook·CLI·agent 동작
- `output/`에서 먼저 구현하고 검증할 실제 작업 장면
