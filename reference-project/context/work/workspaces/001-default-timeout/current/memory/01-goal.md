# 목표와 완료 기준

## 목표

설정에 `request_timeout_ms`가 없을 때 request policy가 canonical 기본값 `5000`밀리초를 사용하게 한다.

## 완료 기준

- Project [`common/prd.md`](../../../../../project/common/prd.md)가 정의한 유효 입력과 거부 입력을 구현한다.
- 누락된 timeout이 `5000`이 되는 동작을 실제 테스트로 검증한다.
- 검증 receipt와 현재 상태가 다음 재진입에서 복구된다.
- 검증 통과 뒤에도 사람의 명시적 수락 전에는 완료로 간주하지 않는다.
