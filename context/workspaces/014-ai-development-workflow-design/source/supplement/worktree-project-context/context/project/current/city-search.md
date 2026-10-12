# 도시 검색의 현재 선별·실패 경계

여행 생성의 도시 검색 요청, GeoNames 응답 선별이나 `City` 변환을 수정할 때 읽는다. 이 본문은 2026-09-14 현재 `searchCities`가 보존하는 여러 조건과 확인 범위를 함께 설명한다. 검색 debounce·cache·화면 오류 경험이나 외부 검색 공급자 선택은 소유하지 않는다.

## 요청과 응답은 같은 도시 범위를 사용한다

**요청한 도시 범위와 응답에서 허용하는 범위를 함께 유지한다.** [GeoNames client](../../../apps/client/src/features/trip/create-trip/geonames.api.ts)는 이름 접두어 검색에 한국어·인구순·최대 10건을 요청하며, 요청과 응답 필터가 같은 feature code 목록을 사용한다.

| 판단 | 현재 기준 |
| --- | --- |
| 허용 code | `PPLC`, `PPLA`, `PPLA2`, `PPL` |
| 공통 필수값 | 이름과 국가명이 비어 있으면 제외 |
| 수도 `PPLC` | 필수값·허용 code 조건을 통과하면 인구와 무관하게 포함 |
| 그 밖의 허용 도시 | 인구가 10,000보다 커야 함. 10,000은 제외, 10,001은 포함 |
| 결과 변환 | 공급자 순서를 유지하고 lat·lng 문자열을 숫자로 바꿔 City 반환 |

**요청 실패도 현재는 빈 배열로 반환된다.** 오류를 기록한 뒤 반환하므로 호출부는 검색 결과 없음과 실패를 같은 값으로 받는다. Throw나 별도 상태로 바꾸려면 query hook·화면의 오류 경험까지 정해야 하며, 동작 보존 리팩터링으로 처리하지 않는다.

## 확인 범위와 다시 볼 신호

Ticket 02에서는 고정 Axios adapter로 요청 parameter, 허용·비허용 code, 빈 필드, 인구 10,000/10,001, 저인구 수도, 좌표 변환, 순서와 실패 반환을 변경 전후 대조했다. 영구 자동 검사 파일은 남기지 않았고 실제 Axios 네트워크 직렬화, GeoNames 가용성, 전체 화면은 확인하지 않았다.

Feature code, 인구 경계, 실패 표현, GeoNames request 또는 query consumer가 바뀌면 이 본문과 실제 서비스 경계를 다시 대조한다. 완료와 근거의 상세는 Workspace 002 [Ticket 02](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/02-city-search.md)가 소유한다. 2026-10-01 편집에서는 그 Ticket과 이 브랜치의 GeoNames client를 다시 대조했으며 외부 요청이나 제품 검사를 새로 실행하지 않았다.
