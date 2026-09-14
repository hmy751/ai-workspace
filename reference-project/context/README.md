# Project context와 Work context

이 디렉터리는 Project의 지속 맥락과 개별 작업의 지속 맥락을 서로 다른 책임으로 유지하면서, Work context가 필요한 Project 기준을 선택해 사용하는 관계를 정의한다.

- [`project/`](project/): 여러 작업에 지속되는 의미, 교체되는 현재 현실과 관련 작업의 판단 기준을 `common/`, `current/`, `guidance/` 물리 layer와 Owner 관계로 유지하는 Project-wide 판단 context. `decisions/`는 선택 이유를, `REFERENCE/`는 본문 구성·읽기 기준을 소유한다.
- [`work/`](work/): 여러 Workspace의 현재 상태·원자료·goal 산출물 지도·기록과 이를 복구·유지·검증하는 공용 Harness의 운영 경계

Project context는 기존 제품 문서의 복사본이나 링크 목록이 아니며 Workspace 안으로도 복제하지 않는다. [`project/README.md`](project/README.md)는 작업·주제에서 실제 본문과 물리 layer의 책임을 찾는 안정된 routing anchor이고, 각 Workspace는 이 anchor와 현재 작업에 필요한 본문의 경로·선택 이유를 계약에 남긴다. Harness는 두 경계를 연결하는 관리 장치이며 Project 기준이나 Workspace의 의미를 소유하지 않는다.

제품 구현과 제품 테스트는 context가 아니므로 각각 [`../src/`](../src/)와 [`../tests/`](../tests/)에 있다.

## 사람이 시작하는 위치

- 제품 기준과 현재 제약을 확인할 때: [`project/README.md`](project/README.md)의 주제별 진입에서 필요한 실제 본문
- 적용할 본문이 아직 없거나 현재 질문이 바뀌었을 때: [Project 읽기 기준](project/REFERENCE/reading.md)
- Project context를 작성·복원·갱신할 때: [`project/MAINTENANCE.md`](project/MAINTENANCE.md)와 [구성 기준](project/REFERENCE/composition.md)
- 현재 작업을 복구하거나 Work context 운영을 이해할 때: [`work/README.md`](work/README.md)
- 실제 제품 구현을 볼 때: [`../src/`](../src/)

Harness를 제거하거나 교체하더라도 `project/`의 기준과 각 Workspace의 README·`current/`·`source/`·`output/`·`records/` 의미는 남는다.
