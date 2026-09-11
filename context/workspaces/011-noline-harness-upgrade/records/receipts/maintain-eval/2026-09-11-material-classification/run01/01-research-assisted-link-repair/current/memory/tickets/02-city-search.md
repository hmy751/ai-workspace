# 02 — 도시 검색의 선별 조건과 변환

## 맡은 결과와 범위

`apps/client/src/features/trip/create-trip/geonames.api.ts`의 요청 도시 코드와 응답 선별·City 변환을 명확히 한다. 같은 허용 도시 목록을 두 곳에서 맞춰야 하는 부담을 줄인다. query hook의 debounce·cache·오류 표시 정책은 바꾸지 않는다.

## 실행 맥락과 접근

[보존 계약](../spec/03-concepts-and-contracts.md)과 [품질 기준](../spec/04-quality-and-completion.md)을 적용한다. Main의 [조사 초안](../../../../../../../eval-inputs/noline-002-additional-research-and-ticket-drafts-2026-09-11.md)에 따르면 허용 도시 코드 네 개가 요청 `featureCode`와 응답 `allowedFCodes`에 반복된다. 인구가 10,000보다 크거나 수도 코드 `PPLC`인 조건도 식 안에 묶여 있다. `useSearchCities.ts`가 실제 queryFn으로 사용한다는 Main 보고다.

`searchCities`를 외부 호출 경계로 유지하며 허용 목록·수도 예외·필드 변환의 의미를 드러낸다. 외부 문자열 좌표의 `parseFloat`는 필요한 변환이므로 제거하지 않는다. 실패 시 빈 배열을 반환하는 catch는 단순 재전파 catch가 아니며 새 오류 throw로 바꾸지 않는다. Ticket 01과 기술적 의존성은 없다.

## 완료 조건과 확인 방법

수정 전 `searchCities`에 고정된 HTTP 응답을 공급하여 실제 요청 인자와 반환값을 확인하고, 수정 후 같은 검사를 실행한다.

- 허용/비허용 도시 코드, 이름/국가 누락을 구별한다.
- 인구 10,000과 10,001, 인구 기준에 미달하는 수도를 확인한다.
- 응답 순서, 숫자 문자열 좌표 변환, 요청 실패 시 빈 배열 반환을 보존한다.

허용 코드의 수정 위치가 하나로 모이고 선별 조건과 변환 이유를 가까운 코드에서 이해할 수 있어야 한다. 범용 검색 엔진을 도입한 것 자체는 개선이 아니다. 고정 HTTP 응답 검사는 실제 GeoNames 서비스 가용성을 증명하지 않는다.

## 현재 상태와 실제 결과

실행 전 초안이다. Main이 새 후보의 코드와 사용처를 확인했다고 보고했다. 외부 API 호출·제품 수정·제품 테스트 실행은 없으며 위 검사는 계획이다.
