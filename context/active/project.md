# Project common context

마지막 갱신: `2026-08-12`

## 목표

실제 개발 프로젝트에서 사람과 AI가 프로젝트의 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 다시 지속 상태에 반영할 수 있게 하는 context+harness 운영 구조를 만든다.

## 현재 정의된 context 역할

- **Project common context**: 장기간 유지되는 목표, 기준, 결정, 제약
- **Work context**: 특정 작업의 문제, 현재 상태, 근거, 불확실성, 다음 행동

## 만들려는 것

- 이미 개발 프로젝트가 있다고 가정하고 그 안에서 실제로 돌아가는 운영 구조
- 사람과 AI가 현재 상태를 복구하고, 필요한 context만 선택해 행동하는 구조
- 검증 결과가 일회성 출력으로 끝나지 않고 지속 상태에 다시 반영되는 구조
- work context의 층위와 이를 유지·보완하는 harness가 연결된 시스템

설치 패키지 자체가 목표는 아니다. 운영 흐름과 상태의 연결이 먼저 보여야 한다.

## 현재 context 유지 장치

- repo-local `context_maintainer` subagent가 의미 있는 작업 경계에서 active의 drift와 history 누락을 점검한다.
- `AGENTS.md`가 호출 조건을 소유하고, main이 subagent 결과의 채택과 사용자 판단 경계를 소유한다.
- agent는 근거가 명확한 active/history만 갱신하며 source 원본이나 프로젝트 목표를 독자적으로 바꾸지 않는다.
- agent 정의·등록·routing은 이 저장소 안에서만 소유하며 전역 agent·skill·프로젝트 색인·runtime 설정으로 승격하지 않는다.

## source 경계

- Anthropic 공식 문서와 사용자가 선택한 발췌는 공식 참고 자료로 본다.
- 블로그 원문과 사용자가 선택한 발췌는 context+harness 관점을 구체화하는 참고 자료로 본다.
- 사용자가 공감해 가져온 Codex 의견은 설계 질문으로 보존하되, 사용자 승인 결정과 동일시하지 않는다.
- AX와 cofathon은 사용자가 실제로 작업한 방식을 관찰하는 자료이며 새 구조의 정답 원천은 아니다.
- 등록된 자료는 [`../source/manifest.json`](../source/manifest.json)에서 찾는다. 다른 Desktop 저장소는 source로 확장하지 않는다.
