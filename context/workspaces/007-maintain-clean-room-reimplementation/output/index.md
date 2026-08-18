# Maintain clean-room reimplementation output

마지막 갱신: `2026-08-18`

## Workspace goal

Workspace 005의 사용자-facing Maintain 동작을 글로벌 책임 배치 기준에서 다시 도출해 `reference-project/`가 소유하는 재사용 가능한 구현과 검증으로 만든다.

## 현재 선택된 구현

없다.

현재 [`Reference Maintain 경계 문서`](../../../../reference-project/context/work/harness/maintain/README.md)는 code baseline의 진입점일 뿐 새 architecture나 완료된 output이 아니다. Root automatic hook과 agent도 비활성이다.

## 현재 선택된 설계 입력

- [`Clean-room source와 behavior contract`](../records/2026-08-18-01-clean-room-source-and-behavior-contract.md)
- [`Code reset baseline과 제외 topology`](../records/2026-08-18-02-code-reset-baseline-and-excluded-topologies.md)
- [`Clean-room implementation handoff`](../records/2026-08-18-03-clean-room-implementation-handoff.md)

## Output 선택 gate

1. 여섯 사용자 장면이 구조 독립적인 acceptance로 표현됨
2. 각 책임의 모델 판단·deterministic guard·사람 권한 배치 이유가 드러남
3. 가장 작은 vertical slice가 하나의 실제 사용자 장면을 end-to-end로 보임
4. Unit·filesystem proof와 actual host·semantic acceptance의 상한을 구분함
5. 재사용 가능한 계약·구현·검증이 Reference 책임 경계에서 함께 발견됨
6. Root 연결은 실제 host acceptance 뒤에만 얇게 추가됨

005의 final runtime과 006의 attention 기반 diff는 현재 output 후보가 아니다.
