# Goal output

이 파일은 `001-default-timeout` Workspace의 목표를 위해 선택된 현재 산출물의 지도다. [재개 안내](../recover.md)에서 이 지도를 연결하며, 산출물 본문은 요청에 필요할 때 선택해서 연다.

- [`src/config_loader.py`](../../../../../src/config_loader.py): 기본 timeout과 입력 검증을 구현한 제품 코드의 canonical
- [`tests/test_config_loader.py`](../../../../../tests/test_config_loader.py): 입력·반환 계약을 직접 확인하는 제품 검사

실제 산출물은 Project root에 있으므로 이 폴더에 복제하지 않는다. 직접 검사 기록은 [records](../records/README.md), 과거 Verify 증거는 `records/receipts/verify/`에서 찾는다. 이 지도에 포함되었다는 사실은 검증 통과, 사람의 수락, Workspace 완료를 뜻하지 않는다.
