# 선택한 Project 맥락

이번 Workspace는 상위 Project 문서 전체나 모든 물리 layer를 기본 입력으로 읽지 않는다.

- [`../../../../../project/README.md`](../../../../../project/README.md): `common/current/guidance` 물리 layer, 실제 문서 위치, Owner 우선순위와 선택적 읽기 계약을 찾는 안정된 routing anchor
- [`../../../../../project/common/prd.md`](../../../../../project/common/prd.md): 이 goal에 지속해서 적용되는 사용자 장면, 제품 목적, timeout 입력 계약과 완료 기준
- [`../../../../../project/current/architecture.md`](../../../../../project/current/architecture.md): 현재 config loader의 지원 범위, 상세 코드·테스트 Owner와 검증의 증명 상한
- [`../../../../../project/decisions/0001-default-timeout.md`](../../../../../project/decisions/0001-default-timeout.md): 누락된 timeout의 canonical 기본값이 `5000`밀리초라는 결정

[`../../../../../project/guidance/README.md`](../../../../../project/guidance/README.md)는 이 Project의 guidance 층이 현재 비어 있음을 설명하지만, 이번 goal에 적용할 실제 guidance가 없으므로 recovery context에는 선택하지 않는다. Root README는 내용 선택을 대신하지 않으며, 실행 시 사용하는 정확한 선택 목록과 이유의 canonical 계약은 [`../../recover.json`](../../recover.json)의 `project_context`가 소유한다.
