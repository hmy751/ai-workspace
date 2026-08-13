# 0001. 요청 timeout 기본값은 5000밀리초로 한다

- 상태: 채택
- 결정일: 2026-08-13

## 맥락

호출자가 `request_timeout_ms`를 생략해도 요청 실행 정책에는 확정된 timeout 값이 필요하다. 기본값이 코드 위치마다 암묵적으로 달라지면 같은 설정이 서로 다른 동작을 만들 수 있다.

## 결정

`request_timeout_ms`가 없을 때의 제품 기본값을 `5000`밀리초로 정한다. 명시값은 boolean이 아닌 양의 정수일 때만 그대로 사용한다.

이 문서가 기본값의 canonical 상위 맥락이다. [`src/config_loader.py`](../../src/config_loader.py)는 이 결정을 구현하고, [`tests/test_config_loader.py`](../../tests/test_config_loader.py)는 누락 시 실제 결과가 `5000`인지 검증한다.

## 결과

- 설정을 생략한 호출자도 동일한 timeout 정책을 받는다.
- 기본값을 변경하려면 이 결정, 제품 기준, 코드, 테스트의 정합성을 함께 검토해야 한다.
- 이 값은 config loader 동작의 기준이며, 실제 요청 성공 시간이나 외부 서비스의 응답 시간을 보장하지 않는다.

관련 제품 기준은 [PRD](../prd.md), 코드 구성과 실행 방법은 [architecture](../architecture.md)에 있다.
