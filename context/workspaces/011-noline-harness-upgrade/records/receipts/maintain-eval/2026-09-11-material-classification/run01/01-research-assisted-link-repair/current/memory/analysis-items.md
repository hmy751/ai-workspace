# 리팩토링 후보 전체

기존 분석의 코드 표현·처리 방식 관찰에 추가로 확인한 폼·저장 결과·공통 구현의 조건을 합쳤다. 작은 요소부터 선택하며, 실제 결과가 바뀌는 부분은 버그 확인·수정과 구별한다.

아래는 실행 Ticket 목록이나 모든 항목을 무조건 변경하라는 결정이 아니다. 원래 관찰·현재 근거·검증 필요 여부를 보존한 후보이며, 채택할 때 해당 원문과 현재 코드를 직접 확인한다.

## 이름·주석·로그·catch

단순 API 처리에 조회 로그·오류 출력 후 재전파·코드 내용을 반복하는 주석이 겹친다. 함수 의도가 보이게 정리하고 기록할 오류의 책임을 확인한다. DELETE payload의 tripId처럼 이유를 설명하는 주석은 보존한다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 오류 전달과 표시 변화는 별도 판정.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/code-style.md), [대표 코드](../../../../../../apps/client/src/entities/expense/api/expenses.ts).

## 조건식과 표시 규칙

경비 화면의 첫 통화 비교와 소수 자릿수 규칙이 JSX 안에 반복된다. 의미 있는 이름과 작은 계산으로 의도를 드러낸다. outsideTripRange/insideTripRange는 보존할 기존 예시다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 통화별 금액·정렬·표시 결과 보존.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/code-style.md), [대표 코드](../../../../../../apps/client/src/screens/ExpensesScreen.tsx).

## 불필요한 값 변환과 기본값

number를 String 후 parseFloat로 되돌리는 표현, 미전달·null·빈 문자열의 의미를 흐리는 기본값을 확인한다. 좌표 0이 사라지는 동작 수정은 버그 Work에 분리한다.

근거 수준과 경계: 기존 분석·추가 코드 확인. ||를 일괄 교체하지 않는다.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/code-style.md), [대표 코드](../../../../../../apps/client/src/features/schedule/create-schedule/useCreateScheduleForm.ts).

## 타입으로 이어지는 검증 결과

normalizedTrips as never[], updateData: any, return updated!의 근거를 드러낸다. DB·API 경계에서 형태, 수정 가능 필드, 결과 존재를 확인한 사실을 이후 처리까지 전달한다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 단언 제거만 완료 기준으로 삼지 않는다.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/code-style.md), [대표 코드](../../../../../../apps/client/src/shared/services/sync/engine.ts).

## 중복 검증과 도달하지 않는 분기

목록의 entity를 검증한 뒤 같은 배열 응답을 다시 검증하는 처리, null을 허용하지 않는 여행 수정 schema 뒤의 null 분기를 검토한다. 요청과 응답 각각의 검증은 다른 경계다.

근거 수준과 경계: 기존 분석. 허용 입력·오류 계약을 유지하는 정리와 계약 변경을 구별.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/code-style.md), [대표 코드](../../../../../../apps/server/src/routes/trips.ts).

## 목록 계산과 useMemo

일정·경비 화면의 dateRange 배열이 매 렌더 새로 생성돼 useMemo가 계산을 재사용하지 못한다. 날짜별 그룹 계산과 반복되는 범위 생성을 읽기 쉽게 정리한다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 성능 장애나 최적화 효과를 측정한 것은 아니다.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/code-style.md), [대표 코드](../../../../../../apps/client/src/screens/ScheduleScreen.tsx).

## 폼 초기값·reset·값 변경 흐름

렌더 중 setValue, 장소 선택을 effect로 복사, 수정 Drawer의 ID 기준 초기화가 흩어져 있다. 취소·재열기·다른 항목·늦게 도착한 trip 데이터에 따른 기본 통화를 추적하기 쉽게 한다.

근거 수준과 경계: 기존 분석 + 비동기 기본 통화·동일 ID 재진입 추가 관찰. 의도 UX와 실제 영향 확인이 필요.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/components.md), [대표 코드](../../../../../../apps/client/src/features/expense/create-expense/useCreateExpenseForm.ts).

## picker callback 의미

선택 후 onClose 호출, onClose에 선택 handler 연결로 값 저장·검증·닫기가 겹친다. 각각의 책임과 이름을 맞춘다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 닫기·취소 결과가 달라지면 버그 확인 대상으로 분리.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/components.md), [대표 코드](../../../../../../apps/client/src/shared/components/TimePicker/TimePicker.tsx).

## 저장 성공 이후 처리

여행·경비·일정 생성의 이동 책임과 일정 수정의 후속 경로 준비가 다르다. 저장 결과, 캐시 반영, 이동, 백그라운드 준비의 책임을 읽을 수 있게 한다. 500ms 타이머의 필요는 먼저 확인한다.

근거 수준과 경계: 기존 분석 + 저장된 결과 활용·오래된 좌표 확인. 타이머·좌표 결과 변경은 동작 수정.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/components.md), [대표 코드](../../../../../../apps/client/src/features/schedule/update-schedule/UpdateScheduleDrawer.tsx).

## 생성·수정 컴포넌트의 반복과 차이

수정 Drawer에 조회·입력·저장·알림이 모여 있다. 경비의 연결 일정 선택, 공용 Input과 원시 TextInput 스타일, 날짜 그룹·메뉴 상태를 비교한다. 의도 UX는 보존하며 실제 공유 의미만 묶는다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 조회 정책·오류·loading 차이의 실제 영향은 버그 후보에도 남긴다.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/components.md), [대표 코드](../../../../../../apps/client/src/features/expense/update-expense/UpdateExpenseDrawer.tsx).

## 공통 데이터·경로·정리 구현

활성화와 일정 변경의 경로 다운로드, 활성화와 sync의 upsert, 즉시 비활성화와 지연 cleanup을 비교한다. 같은 생명주기 규칙을 수정할 위치를 줄이되 기존 경로 판별과 미전송 보존 조건의 차이를 먼저 해소한다.

근거 수준과 경계: 기존 분석 + 일정 ID/이동 수단만 보는 routeExists의 재계산 위험. 함수 호출로 단순 통일하면 안 된다.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/engine-data.md), [대표 코드](../../../../../../apps/client/src/shared/services/directions/route-downloader.ts).

## 완료 상태와 조율 책임 표현

활성화 hook의 서버·여러 테이블·이전 활성 해제·지도·경로·캐시 조율, online이라는 비활성 상태 이름, 지도만 보는 ready를 구별한다. 동기화 실행 종료·전체 반영·정리 가능 상태도 이름과 반환 의미를 분명히 한다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 완료/실패 의미 자체를 바꾸는 수정은 버그 Work.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/engine-data.md), [대표 코드](../../../../../../apps/client/src/shared/services/offline-prep/metadata.ts).

## 설정과 실제 사용처

policy syncStrategy의 선언과 동기화 실행 사용처가 이어지는지 판단한다. 공통 함수가 두 곳에서 사용된다는 주석도 실제 호출과 대조한다. 미사용 설정을 실제 기능 보장처럼 남기지 않는다.

근거 수준과 경계: 기존 분석. 미사용이라는 이유만으로 계획 기능 구현이나 삭제를 자동 결정하지 않는다.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/engine-data.md), [대표 코드](../../../../../../apps/client/src/shared/policy/constants.ts).

## 서버 변환·오류 처리 책임

CRUD·활성화·sync의 데이터 변환과 auth·helper·middleware의 오류 변환 위치를 읽기 쉽게 한다. 좌표·날짜·불리언과 오류 형태의 공유 계약은 실제 소비자와 확인한다.

근거 수준과 경계: 기존 분석·추가 코드 확인. 누락 필드·소유권·응답 불일치는 버그 Work, 공개 오류 계약 변경은 별도 기대 동작 확인.

출처: [보존한 분석의 해당 영역](../../source/codebase-analysis/server-contracts.md), [대표 코드](../../../../../../apps/server/src/utils/http-errors.ts).

## 2026-09-11 추가 조사와 1차 범위

아래는 Main의 [추가 조사와 Ticket 초안](../../../../../../eval-inputs/noline-002-additional-research-and-ticket-drafts-2026-09-11.md)에 보고된 관찰이다. Main이 확인했다고 밝힌 기준은 `refactor/codebase`, HEAD `a612ba4c49b92b1193e75e1d56bdefcdcd86bbda`다. 대표 구현·사용처를 읽은 결과이며 전체 파일 정독·앱·외부 API·DB·동작 테스트 실행 결과가 아니다. Maintain이 제품 코드를 독립 확인한 것으로 해석하지 않는다.

1차 범위는 [Ticket 색인](tickets/index.md)에 연결한다. 경비 표시 규칙은 Ticket 01, 신규 도시 검색은 02, 신규 저장 용량은 03, 경비 API는 04, 서버 일정 응답 변환은 05의 초안이다. 번호는 Main 추천이며 최종 처리 판정이나 사용자 확정이 아니다.

### 새 후보와 보존할 차이

- 도시 검색: `apps/client/src/features/trip/create-trip/geonames.api.ts`의 요청·응답에 허용 코드 네 개가 중복된다. 인구 10,000 초과 또는 수도 `PPLC` 조건을 읽히게 할 여지가 있다. 문자열 좌표 변환과 실패 시 빈 배열 반환은 보존한다. 상세 범위는 Ticket 02가 소유한다.
- 저장 용량: `apps/client/src/features/profile/hooks/useStorageStats.ts`의 성공·바깥 실패에서 같은 표시값을 조립한다. 파일 조회 중 실패하면 누적값을 남기고 지도 조회로 넘어가지 않는 흐름과 개별 지도 팩 실패 후 다음 팩을 계속 읽는 흐름을 구별한다. 상세 범위는 Ticket 03이 소유한다.
- 대표 여행 선택: `apps/client/src/entities/trip/utils/selectMainTrip.ts`에서 날짜 변환과 존재 단언이 반복된다. 진행 중·미래·과거·날짜 없는 여행의 우선순위는 이미 잘 보인다는 Main 판단으로 첫 다섯 Ticket 뒤 재검토한다. 고정 오늘·시간대, 동률·빈 목록·입력 순서 보존을 확인하고 날짜 없는 입력의 schema 허용 여부를 먼저 대조한다. 간접 호출만 늘리는 변경은 개선으로 보지 않는다.
- 카테고리 색상: `apps/client/src/screens/ExpenseDetailScreen.tsx`의 배경·글자색 표를 한 쌍으로 관리할 후보가 있다. `entities/expense/ui/ExpenseCard.tsx`와는 `체험` 처리가 다르고 실제 목록은 `shared/components/Card/ExpenseCard.tsx`를 사용한다는 Main 보고다. entity Card 호출을 검색에서 찾지 못한 것을 삭제 근거로 삼거나 서로 다른 색상을 통일하지 않는다.
- 로그아웃·계정 삭제: `apps/client/src/shared/services/auth/logout-service.ts`에 로컬 정리 단계가 반복되지만 서버 실패 뒤 계속 여부가 다르다. 동일 로컬 정리를 후속 검토하되 실행 순서·부분 실패·미전송 보존을 먼저 확인한다. `checkPendingSync`의 pending/inProgress와 별도 failed 반환을 지우는 통합을 하지 않는다. 실제 계정 삭제·DB reset을 실행한 증거는 없다.

### 설명 정정과 동작 확인을 구별할 후보

`apps/client/src/shared/services/sync/api.ts`는 최대 3회, 2/4/8초 재시도를 설명하지만 `!originalRequest._retry` 조건과 첫 재시도 전 `_retry=true` 설정이 충돌하는 경로가 보인다는 Main 보고다. 실제 Axios config 전달과 요청 횟수를 확인할 동작 후보이며 런타임 재현된 결함이 아니다. 설명만 바꾸어 닫거나 3회 재시도로 고치는 작업을 리팩토링에 포함하지 않는다.

`apps/client/src/shared/services/auth/auth-interceptor.ts`의 sync helper 설명은 토큰 갱신도 같다고 하지만 본문은 401에서 만료 상태와 `AuthRequiredError`를 처리한다고 보고됐다. 해당 helper의 setup 호출은 조사 범위에서 찾지 못했고 실행 중인 sync API는 자체 인터셉터를 등록한다는 설명이다. export 삭제나 기능 구현을 자동 결정하지 않는다.

`apps/client/src/shared/lib/datetime.ts`는 Date 입력을 직접 `setHours`로 바꾸고 UTC ISO를 반환하며 offset 예제·미래 상대 시간 예제가 구현과 맞지 않는 부분이 있다는 Main 보고다. 설명 정정과 입력 변경·시간대·미래 표시의 동작 수정을 분리한다.

### 기존 후보에서 추가로 확인한 경계와 후속 범위

- Ticket 01은 화면 `toFixed`와 currency helper의 천 단위 구분자 차이를 유지한다. `currency.ts`의 '가장 많이 사용된 통화' 설명과 명목 금액 내림차순 선택의 차이는 별도 후보이며 빈도 정렬·환산을 추가하지 않는다. 앱 호출을 찾지 못한 결과만으로 export를 삭제하지 않는다.
- Ticket 04 이후 auth wrapper·날짜 주석·미사용처럼 보이는 export는 후속 판단이다. 요청/응답 검증은 별개 경계로 유지한다.
- Ticket 05는 일정 CRUD 응답 변환만 다룬다. sync의 `as never[]`, mutation `any`, 중복 검증·도달하지 않는 분기, auth/places 오류와 activation/sync 변환은 해결한 것으로 처리하지 않는다.
- 일정 form의 number 왕복, 일정·경비의 날짜 범위/그룹, 폼 취소·재열기·다른 항목·늦은 기본값, picker와 호출부, 저장 후 캐시·이동·경로 준비는 후속 범위다. UTC/local date·기대 UX·500ms 타이머·오래된 좌표가 결과 차이로 이어지면 기대 동작을 먼저 확인한다.
- 생성·수정 컴포넌트는 위 폼 경계를 확인한 뒤 같은 입력 의미만 다룬다. expense/schedule mutation의 캐시 갱신 범위가 다르고 일정 삭제는 경비 캐시도 갱신한다는 추가 보고를 유지한다. 범용 mutation hook으로 차이를 지우지 않는다.
- route/upsert/cleanup과 로그아웃 정리는 직접 걸리는 데이터 보존 조건만 선행 확인한다. 활성화·동기화 완료 표현, policy `syncStrategy`의 실행 연결도 후속으로 남긴다.
- `packages/ui`의 Input·Checkbox·Switch는 짧고 명확해 범용 wrapper를 추가할 근거를 찾지 못했다는 Main 판단이다. RadioGroup의 `as any`는 앱 사용처와 primitive prop 계약 확인 전 첫 Ticket으로 올리지 않는다.
- `packages/schema/src/requests/schedule.ts`의 생성·수정은 필수성과 허용 필드가 달라 단순 partial 통일을 채택하지 않는다는 Main 판단이다.

이 연결은 후보 누락을 막기 위한 현재 분해다. 후속 후보를 완료·변경 불필요로 일괄 판정하지 않으며 다섯 Ticket의 작은 개선만으로 전체 목표 달성을 주장하지 않는다.
