# Goal output

이 파일은 `001-default-timeout` Workspace의 목표를 위해 선택된 현재 산출물의 지도다. `recover`는 이 index만 기본 context로 읽고, 연결된 산출물 본문은 필요할 때 사람이 선택해서 연다.

- [`src/config_loader.py`](../../../../../src/config_loader.py): 기본 timeout과 입력 검증을 구현한 제품 코드의 canonical

실제 산출물은 Project root에 있으므로 이 폴더에 복제하지 않는다. 제품 테스트는 Project root `tests/`에서 찾고, 이미 수행된 test·eval·수동 확인의 evidence receipt는 Workspace `records/receipts/verify/`에서 찾는다. Evidence receipt는 관찰된 결과와 미확인 범위를 보존할 뿐 이 지도에 포함된 산출물의 충분한 검증, 사람의 수락, Workspace 완료를 뜻하지 않는다.
