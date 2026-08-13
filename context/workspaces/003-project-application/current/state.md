# Project application state

마지막 갱신: `2026-08-13`

## 현재 문제

첫 실제 적용 대상 Project와 그 안에서 검증할 작업 장면을 정해야 한다.

## 현재 상태

- 다음 적용 작업을 기존 reference 구현 작업과 섞지 않기 위해 이 Workspace를 만들었다.
- 기존 reference 구현과 검증은 [`001-reference-implementation`](../../001-reference-implementation/)에 보존되어 있다.
- 대상 Project 경로, 변경 범위, 검증할 첫 작업은 아직 지정되지 않았다.
- 따라서 다른 Desktop 저장소를 열거나 migration을 시작하지 않았다.

## 다음 행동

사용자가 대상 Project와 첫 적용 범위를 알려 주면, 그 Project의 기존 canonical·context·테스트 진입점을 먼저 확인하고 최소 migration 계획을 세운다.
