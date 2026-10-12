# Request policy config 제품 기준

이 문서는 여러 Work에 지속되는 제품 목적·사용자 장면·완료 기준·범위의 normative Owner다. 제품 goal이나 acceptance를 정할 때 읽고, 사용자 또는 제품 책임자가 의미를 바꿀 때 갱신한다. 현재 코드가 이 기준과 충돌한다는 사실만으로 기준을 구현 상태에 맞춰 자동 변경하지 않는다.

## 사용자 장면

호출자는 요청 실행 정책을 만들 때 `request_timeout_ms`를 명시할 수도 있고 생략할 수도 있다. Project는 입력을 검증해 모든 호출자가 동일하게 해석하는 불변 `RequestPolicy`를 제공한다. 설정이 잘못되면 임의 보정하지 않고 즉시 거부해 오타나 타입 오류가 실행 단계까지 퍼지지 않게 한다.

## 목적

요청 실행기가 사용할 timeout 정책을 하나의 검증된 값으로 제공한다. 호출자는 설정에 `request_timeout_ms`를 명시할 수도 있고, 생략해 제품 기본값을 사용할 수도 있다.

## 완료 기준

- `request_timeout_ms`가 없으면 `5000`밀리초를 사용한다.
- 양의 정수로 명시한 `request_timeout_ms`는 바꾸지 않고 유지한다.
- Python의 boolean, `0`, 음수, 정수가 아닌 값은 유효한 timeout으로 받아들이지 않는다.
- 지원하지 않는 설정 키는 오타로 간주해 거부한다.
- 검증 결과는 생성 이후 값을 바꿀 수 없는 policy 객체로 반환한다.
- Python 표준 라이브러리만으로 실행하고 검증할 수 있다.

## 범위 밖

파일 형식 파싱, 환경 변수 병합, 네트워크 요청 실행은 이 Project의 범위가 아니다. Workspace 복구와 검증 기록 보존은 Project 코드가 아니라 별도 harness가 맡는다.

현재 구현 구조와 검증 명령은 [architecture](../current/architecture.md), 기본값의 결정 근거는 [default timeout 결정](../decisions/0001-default-timeout.md)에 둔다.
