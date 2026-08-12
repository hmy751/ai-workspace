# Current memory

마지막 갱신: `2026-08-13`

## 목표

실제 개발 프로젝트에서 사람과 AI가 프로젝트의 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 다시 지속 상태에 반영할 수 있게 하는 context+harness 운영 구조를 만든다.

## 현재 정의된 context 역할

- **Project common context**: 장기간 유지되는 목표, 기준, 결정, 제약
- **Work context**: 특정 작업의 문제, 현재 상태, 근거, 불확실성, 다음 행동

Project common context처럼 작업이 바뀌어도 계속 유효한 내용은 이 파일이, 빠르게 바뀌는 Work context의 현재 상태는 [`state.md`](./state.md)가 소유한다. `current`, `records`, `source`는 이 context를 운영하는 저장 층위이며, 별도의 세 번째 context 역할로 간주하지 않는다.

## 만들려는 것

- 이미 개발 프로젝트가 있다고 가정하고 그 안에서 실제로 돌아가는 운영 구조
- 사람과 AI가 현재 상태를 복구하고, 필요한 context만 선택해 행동하는 구조
- 검증 결과가 일회성 출력으로 끝나지 않고 지속 상태에 다시 반영되는 구조
- work context의 층위와 이를 유지·보완하는 harness가 연결된 시스템

설치 패키지 자체가 목표는 아니다. 운영 흐름과 상태의 연결이 먼저 보여야 한다.

## 현재 채택한 운영 경계

- `context/current/`: 다음 세션이 바로 행동하는 데 필요한 현재 상태. 계속 유효한 `memory.md`와 빠르게 바뀌는 `state.md`로 나눈다.
- `context/records/`: 작업 중 만든 지속 가능한 문서·분석·중간 산출물·검증 기록의 누적층.
- `context/source/`: 원자료와 provenance의 읽기 전용 층.
- 루트 `output/`: 목표에 따른 실제 산출물. 분석 문서와 context 기록을 두지 않는다.

## output에 적용할 Project–Workspace 관계

- 이미 존재하는 개발 Project의 PRD, architecture, 공통 결정·제약은 상위 canonical 맥락이다.
- 실제 작업은 여러 Workspace 단위로 운영하며, 각 Workspace는 필요한 상위 Project 맥락만 선택해 접근점을 유지한다.
- Workspace의 `current`는 계속 유효한 `memory.md`와 빠르게 바뀌는 `state.md`로 나누고, 지속 가능한 작업 산출물은 `records/`에 누적한다.
- 상세 결과는 records, 현재 후속 행동은 state, 이후 작업에도 영향을 주는 효과는 memory에 반영한다.
- 상위 Project 자체의 폴더 구조, Workspace 결과를 상위 Project에 반영하는 규칙, Workspace 수명주기·구현 방식은 아직 정하지 않았다.

합의 과정과 미결정 범위는 [`Project–Workspace context 운영 구조 합의`](../records/2026-08-13-03-project-workspace-context-agreement.md)에 있다.

## 현재 context 유지 장치

- repo-local `context_maintainer` subagent가 자연스러운 작업 경계에서 records 누락과 current drift·비대화를 함께 점검한다.
- `AGENTS.md`가 호출 조건을 소유하고, main이 subagent 결과의 채택과 사용자 판단 경계를 소유한다.
- agent는 근거가 명확한 current/records만 갱신하며 source 원본이나 프로젝트 목표를 독자적으로 바꾸지 않는다.
- agent 정의·등록·routing은 이 저장소 안에서만 소유하며 전역 agent·skill·프로젝트 색인·runtime 설정으로 승격하지 않는다.

## source 경계

- Anthropic 공식 문서와 사용자가 선택한 발췌는 공식 참고 자료로 본다.
- 블로그 원문과 사용자가 선택한 발췌는 context+harness 관점을 구체화하는 참고 자료로 본다.
- 사용자가 공감해 가져온 Codex 의견은 설계 질문으로 보존하되, 사용자 승인 결정과 동일시하지 않는다.
- AX와 cofathon은 사용자가 실제로 작업한 방식을 관찰하는 자료이며 새 구조의 정답 원천은 아니다.
- 등록된 자료는 [`../source/manifest.json`](../source/manifest.json)에서 찾는다. 다른 Desktop 저장소는 source로 확장하지 않는다.
