# 선택한 Project 맥락

이번 Workspace는 상위 Project 문서 전체를 기본 입력으로 읽지 않는다.

- [`../../../../../project/overview.md`](../../../../../project/overview.md): 여러 Workspace가 공유하는 제품 목적, 구조, 제약과 검증 경계
- [`../../../../../project/decisions/0001-default-timeout.md`](../../../../../project/decisions/0001-default-timeout.md): 누락된 timeout의 canonical 기본값이 `5000`밀리초라는 결정

선택하지 않은 [`../../../../../project/prd.md`](../../../../../project/prd.md)와 [`../../../../../project/architecture.md`](../../../../../project/architecture.md)는 필요할 때 사람이 열 수 있지만 기본 recovery context에는 들어가지 않는다. 실행 시 사용하는 정확한 선택 목록과 선택 이유의 canonical 계약은 [`../../recover.json`](../../recover.json)의 `project_context`가 소유한다.
