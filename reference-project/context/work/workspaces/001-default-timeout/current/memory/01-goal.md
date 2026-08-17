# 목표와 완료 기준

## 목표

설정에 `request_timeout_ms`가 없을 때 request policy가 canonical 기본값 `5000`밀리초를 사용하게 한다.

## 완료 기준

- Project PRD가 정의한 유효 입력과 거부 입력을 구현한다.
- 누락된 timeout이 `5000`이 되는 동작을 실제 테스트로 검증한다.
- 실제 테스트 결과와 확인하지 못한 범위가 evidence receipt로 보존된다.
- evidence 기록이나 과거 검증 통과 뒤에도 사람의 명시적 수락 전에는 완료로 간주하지 않는다.
