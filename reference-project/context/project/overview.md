# Request policy config Project overview

이 문서는 여러 Workspace가 공통으로 알아야 하는 Project 맥락을 실제 내용으로 압축한다. 상세 제품 기준을 복사한 snapshot이나 링크 목록이 아니라, 작업을 다시 시작할 때 판단을 바꾸는 제품 목적·구조·제약·검증 경계를 한곳에서 읽게 한다.

## 사용자 장면과 제품 목적

호출자는 요청 실행 정책을 만들 때 `request_timeout_ms`를 명시할 수도 있고 생략할 수도 있다. Project는 이 입력을 검증해 모든 호출자가 동일하게 해석하는 불변 `RequestPolicy`를 제공한다. 설정이 잘못되면 임의 보정하지 않고 즉시 거부해 오타나 타입 오류가 실행 단계까지 퍼지지 않게 한다.

## Project 공통 범위

- 설정이 없으면 채택된 기본 timeout `5000`밀리초를 사용한다.
- 명시값은 boolean이 아닌 양의 정수만 허용한다.
- 지원하지 않는 키와 잘못된 타입·범위는 거부한다.
- 검증 결과는 생성 후 바꿀 수 없는 policy 객체다.
- 파일 파싱, 환경 변수 병합, 실제 네트워크 요청 실행은 제품 범위 밖이다.
- Workspace 복구와 receipt 생성·status 연결은 제품 코드가 아니라 제거 가능한 Work Harness가 맡고, 생성된 receipt의 의미와 보존 수명주기는 해당 Workspace가 소유한다.

## 주요 실행 구조

[`src/config_loader.py`](../../src/config_loader.py)의 `load_request_policy(config)`가 입력 형태, 허용 키, 기본값 또는 명시값, 값 범위를 순서대로 검증하고 `RequestPolicy`를 만든다. [`tests/test_config_loader.py`](../../tests/test_config_loader.py)는 기본값·명시값·거부 조건·불변성을 외부 동작으로 확인한다.

기본값 `5000`밀리초는 코드 안의 우연한 상수가 아니라 채택된 Project 결정이다. 이를 바꾸려면 제품 기준, 결정, 코드와 테스트를 함께 검토해야 한다.

## 검증과 acceptance 경계

표준 라이브러리 기반 제품 테스트의 통과는 현재 config loader가 선언된 행위를 구현한다는 근거다. 실제 네트워크 요청, 외부 서비스 응답 시간, 운영 환경 적용과 사람의 acceptance는 증명하지 않는다. Harness의 `verification_passed`도 Project 완료를 뜻하지 않는다.

## 상세 Owner와 정합성

- 목적·완료 기준·범위: [`prd.md`](prd.md)
- 구현 구조와 검증 경로: [`architecture.md`](architecture.md)
- 기본 timeout 채택 결정: [`decisions/0001-default-timeout.md`](decisions/0001-default-timeout.md)
- 실제 제품 행위: [`src/config_loader.py`](../../src/config_loader.py)와 [`tests/test_config_loader.py`](../../tests/test_config_loader.py)

이 overview는 위 Owner들에서 여러 Workspace에 계속 필요한 맥락을 선택해 설명하는 Project common context의 진입점이다. 상세 Owner와 충돌하면 overview를 최신 사실로 간주하지 않고 해당 Owner를 기준으로 다시 대조해 갱신한다.
