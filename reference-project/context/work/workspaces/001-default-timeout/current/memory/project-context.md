# 선택한 Project 맥락

이번 Workspace는 상위 Project 문서 전체나 모든 물리 layer를 기본 입력으로 읽지 않는다.

- [`../../../../../project/README.md`](../../../../../project/README.md): Request policy config 작업의 주제별 진입, 물리 layer와 Owner 우선순위를 찾는 안정된 routing anchor
- [`../../../../../project/common/prd.md`](../../../../../project/common/prd.md): 이 goal에 지속해서 적용되는 사용자 장면, 제품 목적, timeout 입력 계약과 완료 기준
- [`../../../../../project/current/architecture.md`](../../../../../project/current/architecture.md): 현재 config loader의 지원 범위, 상세 코드·테스트 Owner와 검증의 증명 상한
- [`../../../../../project/decisions/0001-default-timeout.md`](../../../../../project/decisions/0001-default-timeout.md): 누락된 timeout의 canonical 기본값이 `5000`밀리초라는 결정

[Project guidance](../../../../../project/guidance/README.md)의 설명 기준은 이 제품 goal의 기본 입력이 아니다. Project 관리·REFERENCE는 그 본문을 갱신하거나 읽기 기준을 재검토할 때 사용한다. 이 문서가 Project 선택과 이유를 소유하고, [재개 안내](../../recover.md)는 언제 이 선택을 읽을지 연결한다. Root README만으로 실제 내용 선택·이해를 대신하지 않는다.
