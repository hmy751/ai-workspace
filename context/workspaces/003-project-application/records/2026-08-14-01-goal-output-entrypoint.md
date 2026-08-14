# Goal output 진입점 추가

날짜: `2026-08-14`

## 배경

Workspace 공통 계약은 goal을 위해 선택된 현재 산출물과 실제 canonical 위치를 `output/index.md`에서 찾게 한다. 이 Workspace에는 그 진입점이 없었지만, 대상 Project와 첫 적용 범위도 아직 정해지지 않은 ready 상태다.

## 판단

- [`output/index.md`](../output/index.md)를 goal 산출물의 진입점으로 추가한다.
- 아직 선택된 산출물과 canonical 위치가 없다는 상태를 그대로 기록한다.
- 현재 루트 [`reference-project/README.md`](../../../../reference-project/README.md)는 적용에 사용하는 기준 Project이며, 대상 Project 적용 결과로 간주하지 않는다.
- 향후 결과가 선택되면 실제 canonical 위치와 검증 상한을 output index에서 가리키고, 후보·선택 근거·검증 상세는 records에 남긴다.

## 현재 영향

재진입 순서에 output index가 추가되었다. 대상 Project 미지정, migration 미착수, 선택된 결과 없음이라는 현재 상태는 바뀌지 않았다.
