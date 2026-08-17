# Harness validation

이 경계는 축소된 Verify evidence 기록을 Recover와 함께 사용해도 기존 Workspace 상태와 checked-in Reference 증거를 오염시키지 않는지 자체 검증한다.

## 소유 범위

- 임시 Project와 Workspace에서 첫 Recover packet을 만든다.
- 이미 수행된 확인을 나타내는 evidence payload를 `verify --input-json`으로 기록한다.
- 새 `evidence-*.json` receipt가 append-only로 생기고, 제품 명령은 실행되지 않으며 기존 status와 제품 파일이 byte 단위로 유지되는지 확인한다.
- 후속 Recover packet이 첫 packet과 같고 새 evidence receipt를 자동 입력이나 제품 verification status로 해석하지 않는지 확인한다.
- 실행 전후 checked-in sample Workspace의 status와 모든 machine receipt를 byte 단위로 비교한다.

Recover와 Verify 각각의 schema·안전 검증은 각 책임 경계의 단위 테스트가 소유한다. 이 경계는 입력 evidence의 진위나 충분성, 제품 test 실행, 사람 acceptance, Maintain, 실제 제품 Workspace의 durable 기록을 소유하지 않는다.

## 내부 구성

- [`tests/test_ephemeral_workspace_state_preservation.py`](tests/test_ephemeral_workspace_state_preservation.py): 임시 `Recover -> evidence 기록 -> Recover` 순환과 checked-in 기계 상태 보존을 검증한다.
- [`../testing.py`](../testing.py): Recover·Verify 단위 테스트도 함께 사용하는 최소 Project/Workspace fixture 지원이다. 공유 기반일 뿐 validation의 판단 계약을 소유하지 않는다.

## 실행

`reference-project/`에서 다음 명령을 실행한다.

```bash
python3 -m unittest \
  context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation \
  -v
```

이 검사가 통과하면 새 evidence 기록이 제품 명령·status·Recover 의미와 checked-in sample 상태에서 격리된다는 점은 확인된다. 입력 evidence 자체의 진위, 제품 claim의 충분성이나 실제 운영 환경의 성공까지 증명하지는 않는다.
