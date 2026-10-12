# 핵심 개념·입출력 계약

`load_request_policy(config)`는 설정 dict를 검증해 요청 실행자가 사용할 불변 `RequestPolicy`를 반환한다. 지원 키는 `request_timeout_ms`이고 값의 단위는 밀리초다. 반환값에는 검증된 양의 정수 timeout이 있다.

현재 공개 함수는 dict가 아닌 입력과 boolean·정수가 아닌 timeout에 `TypeError`, 지원하지 않는 키와 0 이하 timeout에 `ValueError`를 발생시킨다. 부분 policy는 반환하지 않는다. 상세 함수와 타입의 Owner는 [config loader](../../../../../../../src/config_loader.py)다.

설정 검증 결과와 실제 요청 실행 결과는 다르다. 이 함수가 반환한 policy만으로 네트워크 요청이나 운영 환경의 동작을 확인했다고 할 수 없다.
