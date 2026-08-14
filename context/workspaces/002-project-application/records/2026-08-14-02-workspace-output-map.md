# Workspace goal output 지도 도입

날짜: `2026-08-14`

## 배경

공통 Workspace 계약은 `output/index.md`를 goal을 위해 선택된 현재 산출물과 실제 canonical 위치의 진입점으로 둔다. 이 Workspace는 실제 적용물, 반복 적용 절차, 실행 원형의 위치를 current와 records에 각각 보존하고 있었지만 이를 한 번에 찾는 output 진입점은 없었다.

## 결정

- `output/index.md`는 산출물 복제본이 아니라 위치와 역할을 연결하는 selector로 둔다.
- 첫 실제 적용물의 canonical은 대상 Project의 `AGENTS.md`와 적용된 Workspace에 그대로 둔다.
- 반복 적용 절차의 canonical은 이 저장소의 repo-local `apply-context-harness` skill에 둔다.
- 루트 `output/`은 적용 입력인 실행 원형으로 구분하며, 대상 Project에 배치된 goal 산출물로 바꾸어 쓰지 않는다.
- output에 노출되었다는 이유로 Workspace 완료, 사람의 acceptance, target commit 또는 portability 입증을 추론하지 않는다.

## 현재 영향

재진입 순서는 current에서 목표·상태를 확인한 뒤 output 지도에서 현재 산출물의 canonical을 찾고, 상세 근거가 필요할 때 records를 읽는 흐름이 됐다. 기존 적용 상태와 다음 행동은 바뀌지 않았으므로 `current/memory.md`와 `current/state.md`의 내용은 유지한다.

## 근거와 검증 상한

이 결정은 `2026-08-14` 시점의 이 Workspace `README.md`, `current/memory.md`, `current/state.md`, 기존 두 records가 이미 구분한 책임과 위치를 사용했다. 이번 구조 보정에서는 대상 Project를 다시 열거나 live 상태를 재검증하지 않았으므로, 외부 canonical의 최신 검증 상태는 기존 적용 기록과 current가 밝힌 상한을 넘지 않는다.
