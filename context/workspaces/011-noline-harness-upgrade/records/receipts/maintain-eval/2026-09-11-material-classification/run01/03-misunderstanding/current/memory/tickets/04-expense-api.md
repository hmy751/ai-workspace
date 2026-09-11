# 04 — 경비 API의 요청·검증·반환 흐름

## 맡은 결과와 범위

`apps/client/src/entities/expense/api/expenses.ts`의 다섯 remote 함수를 다룬다. 재전파 catch·반복 주석·로그가 작은 본문을 가리는 부담을 줄인다. repository/router, schema 계약, 전역 fetcher의 오류 변환은 바꾸지 않는다.

## 실행 맥락과 접근

[대표 사례](../spec/02-behavior-and-cases.md), [보존 계약](../spec/03-concepts-and-contracts.md), [품질 기준](../spec/04-quality-and-completion.md)을 적용한다. 기존 후보를 좁힌 범위이며 Main의 [조사 초안](../../../../../../../eval-inputs/noline-002-additional-research-and-ticket-drafts-2026-09-11.md)에 정의되어 있다.

요청 검증과 응답 검증은 서로 다른 경계이므로 중복으로 삭제하지 않는다. 삭제할 출력과 남아야 할 실패 기록의 책임을 먼저 확인한다. DELETE payload의 tripId처럼 이유를 설명하는 주석은 유지한다. 사용자 오류 표시·오류 종류·fallback을 바꾸지 않는다.

## 완료 조건과 확인 방법

수정 전 기존 API export를 호출하는 검사를 구성하고 수정 후 같은 검사로 비교한다.

- 정상 요청·반환, 삭제 반환과 HTTP 호출 횟수를 확인한다.
- 잘못된 요청은 HTTP 전에 실패하고 잘못된 응답은 검증에 실패해야 한다.
- 네트워크 실패는 같은 오류로 호출부에 전달되어야 한다.

진단 로그 정리는 변경 내용과 남은 기록 책임을 따로 설명한다. 데이터·오류 계약 변경과 혼합하지 않는다. 실제 요청·검증·반환 흐름이 직접 보이고 재전파를 읽기 위한 부수 코드가 줄었는지 비교한다. 한 함수를 위한 범용 API framework를 만드는 것은 완료 기준이 아니다.

## 현재 상태와 실제 결과

실행 전 초안이다. Main은 기존 후보의 구체적 소스 범위를 확인했다고 보고했다. 제품 수정·동작 테스트 실행 및 검증 결과는 없으며 위 검사는 계획이다.
