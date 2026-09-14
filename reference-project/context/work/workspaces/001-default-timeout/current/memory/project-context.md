# 선택한 Project 맥락

이번 Workspace는 상위 Project 문서 전체나 모든 물리 layer를 기본 입력으로 읽지 않는다.

- [`../../../../../project/README.md`](../../../../../project/README.md): Request policy config 작업의 주제별 진입, 물리 layer와 Owner 우선순위를 찾는 안정된 routing anchor
- [`../../../../../project/common/prd.md`](../../../../../project/common/prd.md): 이 goal에 지속해서 적용되는 사용자 장면, 제품 목적, timeout 입력 계약과 완료 기준
- [`../../../../../project/current/architecture.md`](../../../../../project/current/architecture.md): 현재 config loader의 지원 범위, 상세 코드·테스트 Owner와 검증의 증명 상한
- [`../../../../../project/decisions/0001-default-timeout.md`](../../../../../project/decisions/0001-default-timeout.md): 누락된 timeout의 canonical 기본값이 `5000`밀리초라는 결정

[`../../../../../project/guidance/README.md`](../../../../../project/guidance/README.md)는 설명 skill의 공통 기준을 안내하지만 이번 default-timeout 제품 goal에는 적용되지 않아 recovery context에 선택하지 않는다. Project의 [`MAINTENANCE.md`](../../../../../project/MAINTENANCE.md)와 [`REFERENCE/`](../../../../../project/REFERENCE/README.md)도 본문 갱신·구성·읽기 작업에서 직접 쓰는 관리 기준이므로 기본 packet에 넣지 않는다. Root README는 내용 선택을 대신하지 않으며, 실행 시 사용하는 정확한 선택 목록과 이유의 canonical 계약은 [`../../recover.json`](../../recover.json)의 `project_context`가 소유한다.
