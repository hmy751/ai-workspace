# Workspace memory

## 목표

설정에 `request_timeout_ms`가 없을 때 request policy가 canonical 기본값 `5000`밀리초를 사용하게 한다.

## 완료 기준

- Project PRD가 정의한 유효 입력과 거부 입력을 구현한다.
- 누락된 timeout이 `5000`이 되는 동작을 실제 테스트로 검증한다.
- 검증 receipt와 현재 상태가 다음 재진입에서 복구된다.
- 검증 통과 뒤에도 사람의 명시적 수락 전에는 완료로 간주하지 않는다.

## 유지할 결정과 제약

- Python 표준 라이브러리만 사용한다.
- 기본 timeout의 canonical 결정은 Workspace가 아니라 Project 문서가 소유한다.
- 검증은 manifest에 고정된 argv만 사용한다.
- Workspace records는 실행 이력을 보존하지만 현재 상태를 대신하지 않는다.

## 선택한 Project 접근점

- `docs/prd.md`: timeout policy의 행위 완료 기준과 범위
- `docs/decisions/0001-default-timeout.md`: 기본값 `5000`밀리초의 canonical 결정

구현과 검증 대상 경로 및 실행 argv는 `workspace.json`에 고정한다.
