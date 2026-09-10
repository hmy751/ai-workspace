# Project context와 Work context

이 디렉터리는 Project의 지속 맥락과 개별 작업의 지속 맥락을 서로 다른 책임으로 유지하면서, Work context가 필요한 Project 기준을 선택해 사용하는 관계를 정의한다.

- [`project/`](project/): 여러 작업에 지속되는 의미, 교체되는 현재 현실과 조건부 판단 기준을 각각 `common/`, `current/`, `guidance/` 물리 layer와 Owner 관계로 유지하는 Project-wide 판단 context. `decisions/`는 선택 이유와 재검토 신호를 보존한다.
- [`work/`](work/): 여러 Workspace의 현재 상태·원자료·goal 산출물 지도·기록과 이를 복구·유지·검증하는 공용 Harness의 운영 경계

Project context는 기존 제품 문서의 복사본이나 링크 목록이 아니며 Workspace 안으로도 복제하지 않는다. [`project/README.md`](project/README.md)는 물리 layer의 책임과 실제 내용 위치를 찾는 안정된 routing anchor이고, 각 Workspace는 이 anchor와 현재 작업에 필요한 layer 문서의 경로·선택 이유를 계약에 남긴다. Harness는 두 경계를 연결하는 관리 장치이며 Project 기준이나 Workspace의 의미를 소유하지 않는다.

제품 구현과 제품 테스트는 context가 아니므로 각각 [`../src/`](../src/)와 [`../tests/`](../tests/)에 있다.

## 사람이 시작하는 위치

- 제품의 장기 기준을 확인하거나 바꿀 때: [`project/README.md`](project/README.md)에서 책임 layer를 고른 뒤 해당 `common/`, `current/`, `guidance/` 문서
- Project context를 작성·복원·갱신할 때: [`project/MAINTENANCE.md`](project/MAINTENANCE.md)의 내용 충분성·변경·관리 기준
- 현재 작업을 복구하거나 Work context 운영을 이해할 때: [`work/README.md`](work/README.md)
- 실제 제품 구현을 볼 때: [`../src/`](../src/)

Harness를 제거하거나 교체하더라도 `project/`의 기준과 각 Workspace의 README·`current/`·`source/`·`output/`·`records/` 의미는 남는다.
