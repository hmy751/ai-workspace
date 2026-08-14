# Project context와 Work context

이 디렉터리는 Project의 지속 맥락과 개별 작업의 지속 맥락을 서로 다른 책임으로 유지하면서, Work context가 필요한 Project 기준을 선택해 사용하는 관계를 정의한다.

- [`project/`](project/): 여러 작업에 걸쳐 공유되는 제품 목표, 구조, 결정과 제약의 canonical
- [`work/`](work/): 여러 Workspace의 현재 상태·원자료·goal 산출물 지도·기록과 이를 복구·검증하는 공용 Harness의 운영 경계

Project context는 Workspace 안으로 복제하지 않는다. 각 Workspace는 현재 작업에 필요한 Project 문서의 경로와 선택 이유만 계약에 남긴다. Harness는 두 경계를 연결하는 관리 장치이며 Project 기준이나 Workspace의 의미를 소유하지 않는다.

제품 구현과 제품 테스트는 context가 아니므로 각각 [`../src/`](../src/)와 [`../tests/`](../tests/)에 있다.

## 사람이 시작하는 위치

- 제품의 장기 기준을 확인하거나 바꿀 때: [`project/README.md`](project/README.md)
- 현재 작업을 복구하거나 Work context 운영을 이해할 때: [`work/README.md`](work/README.md)
- 실제 제품 구현을 볼 때: [`../src/`](../src/)

Harness를 제거하거나 교체하더라도 `project/`의 기준과 각 Workspace의 README·`current/`·`source/`·`output/`·`records/` 의미는 남는다.
