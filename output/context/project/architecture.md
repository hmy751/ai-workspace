# Request policy config 구조

## 구성 요소

- [`src/config_loader.py`](../../src/config_loader.py)는 입력 dict의 키, 타입, 값 범위를 확인하고 `RequestPolicy`를 만든다.
- `RequestPolicy`는 frozen dataclass이며, 검증이 끝난 `request_timeout_ms`를 불변 값으로 보유한다.
- [`tests/test_config_loader.py`](../../tests/test_config_loader.py)는 기본값, 명시값, 거부 조건, 불변성을 외부 동작으로 검증한다.

## 실행 경로

`load_request_policy(config)`는 다음 순서로 동작한다.

1. 입력이 dict인지 확인한다.
2. 지원하지 않는 키가 있는지 확인한다.
3. `request_timeout_ms`가 없으면 제품 기본값을 선택하고, 있으면 입력값을 선택한다.
4. 선택한 값이 boolean이 아닌 양의 정수인지 확인한다.
5. 검증된 값으로 불변 `RequestPolicy`를 반환한다.

기본값 `5000`밀리초의 소유 결정은 코드 설명이 아니라 [default timeout 결정](decisions/0001-default-timeout.md)에 있다.

## 검증 경로

`output/`을 현재 디렉터리로 두고 다음 명령을 실행한다.

```sh
python3 -m unittest tests.test_config_loader -v
```

프로세스 종료 코드 `0`과 모든 test case의 `ok`를 성공 조건으로 사용한다. 이 검증은 config loader의 동작을 증명하지만, 실제 네트워크 요청이나 운영 환경 적용까지 증명하지는 않는다.
