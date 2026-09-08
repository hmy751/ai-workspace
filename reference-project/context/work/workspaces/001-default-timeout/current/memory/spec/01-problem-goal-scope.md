# 문제·목표·범위

설정에 `request_timeout_ms`가 없을 때 호출자마다 기본값을 다르게 해석하지 않도록 request policy가 Project의 canonical 기본값 `5000`밀리초를 사용하게 한다.

이번 작업은 누락된 timeout의 기본값, 명시한 값의 유지, 잘못된 입력의 거부와 불변 policy 반환을 구현·확인하는 범위다. 실제 테스트와 검증 기록을 다음 재진입에서 찾을 수 있어야 한다. 파일 형식 파싱, 환경 변수 병합과 네트워크 요청 실행은 포함하지 않는다.

기준은 Project [제품 요구](../../../../../../project/common/prd.md)와 [default timeout 결정](../../../../../../project/decisions/0001-default-timeout.md)이다. 이 Spec은 이번 작업에 적용할 의미를 담으며 기본값의 Project 정본을 대신하지 않는다.
