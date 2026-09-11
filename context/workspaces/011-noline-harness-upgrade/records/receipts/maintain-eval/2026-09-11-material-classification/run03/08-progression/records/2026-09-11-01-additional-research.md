# 추가 코드 조사와 Ticket 초안의 근거

## 입력과 확인 범위

대상 turn은 `01a08bdb-bab9-7580-a482-9451a899870b`다. 사용자 원문은 “추가로 또 조사해봐 합의한 내용 바탕으로 또 다른곳까지 있는지”다. Main 응답은 “작은 범위로 개선하고 전후 결과를 비교할 수 있는 곳”을 추가로 찾았으며 “제품 수정이나 동작 테스트는 아직 실행하지 않았습니다”라고 보고했다.

연결된 Main 문서는 Project root 기준 `eval-inputs/noline-002-additional-research-and-ticket-drafts-2026-09-11.md`다. Maintain이 읽은 파일의 SHA-256은 `f9656715bc0935258e664b189c412da4b2c04ca24cd4f2775c605eeb5134c1c4`다. 아래는 임시 전달 파일 없이도 선택과 한계를 다시 살필 수 있도록 보존한 핵심 내용이다. 제품 코드를 독립 확인하거나 검사를 실행한 결과가 아니라 Main의 조사 보고다.

문서의 핵심 원문: “아래 범위와 순서는 Main의 제안이며 사용자가 첫 구현 대상을 확정한 것은 아니다.” “아래 검증 사례는 실행 계획이다.” 문서는 앞선 사용자 요청을 “티켓 구성해보자”로 전달하지만 그 앞선 발화는 이번 delta의 직접 사용자 원문이 아니다.

Main은 branch `refactor/codebase`, HEAD `a612ba4c49b92b1193e75e1d56bdefcdcd86bbda`를 확인했고 시작·마지막 Git 확인의 미커밋 파일은 Workspace state뿐이었다고 보고했다. 기존 Spec·14개 후보·관련 guide와 대표 검색·날짜·통화·대표 여행·용량·인증·재시도·로그아웃·지도·query·schema·UI 구현과 사용처를 읽었다. 전체 파일 정독·앱 실행은 아니다. 제품 test/spec·runner 경로와 확인한 root/client/server scripts에서 제품 test 명령을 찾지 못했다고 보고했으며 저장소 밖의 검사 부재까지 입증하지 않는다. 과거 타입·린트 실패는 재실행하지 않았다.

## 추가 후보를 선택하거나 뒤로 둔 이유

파일 경로는 Project root 기준이다. 행 번호는 Main이 위 HEAD에서 보고한 위치다.

- `apps/client/src/features/trip/create-trip/geonames.api.ts:32`: `searchCities`의 요청 코드 목록(41행)과 응답 `allowedFCodes`(49행)가 중복된다. 55행의 인구 10,000 초과 또는 `PPLC` 예외를 독자가 해석해야 한다. `useSearchCities.ts`가 queryFn으로 사용한다. 코드 목록을 바꿀 두 위치라는 부담이 구체적이므로 Ticket으로 제안했다. 외부 문자열 좌표의 parseFloat와 실패 시 빈 배열은 필요한 계약이다.
- `apps/client/src/features/profile/hooks/useStorageStats.ts:22`: byte 표시 계산과 파일·지도 팩 집계가 있으며 성공 70행과 실패 78행이 같은 세 표시값을 조립한다. 파일 조회 중간 실패는 앞서 집계한 값을 남기고 지도 조회를 건너뛰며, 개별 지도 팩 실패는 다음 팩으로 계속한다. `screens/ProfileScreen.tsx:28,153`이 표시를 사용한다. 중복 조립과 부분 결과를 함께 확인할 수 있어 Ticket으로 제안했다.
- `apps/client/src/entities/trip/utils/selectMainTrip.ts:10`: 진행 중·미래·과거·날짜 없는 여행의 우선순위는 이미 단계별로 잘 보인다. 26·36·46행의 Date 변환과 날짜 존재 단언을 줄일 가능성은 있지만 간접 호출 증가가 개선을 상쇄할 수 있어 첫 다섯 범위 뒤 재검토하도록 제안했다. `TripSelector.tsx`, `screens/HomeScreen/TripsSection.tsx`, `app/_layout.tsx` 사용을 보고했다.
- `apps/client/src/screens/ExpenseDetailScreen.tsx:22,35`: 카테고리별 배경·글자색의 두 표는 함께 수정할 부담이 있다. `entities/expense/ui/ExpenseCard.tsx:26,38`의 유사 표는 `체험` 처리가 다르다. 실제 목록은 `shared/components/Card/ExpenseCard.tsx`를 사용하며 entity Card의 앱 호출은 검색에서 찾지 못했다. 상세 화면 안의 국소 개선과 다른 Card의 역할을 구분하고 자동 병합·삭제를 제안하지 않았다.
- `apps/client/src/shared/services/auth/auth-interceptor.ts:180,187`: sync helper의 토큰 갱신 설명과 401에서 만료 상태·AuthRequiredError를 만드는 본문이 다르다. setup 호출은 찾지 못했고 실행 중인 sync 클라이언트는 자체 인터셉터를 등록한다고 보고했다.
- `apps/client/src/shared/services/sync/api.ts:76`: “최대 3회, 2/4/8초 재시도” 설명과 `!originalRequest._retry` 조건, 첫 재시도 전 `_retry=true` 설정이 충돌하는 코드 경로를 보고했다. 같은 config 재실패가 이후 재시도를 막을 가능성을 실제 Axios config·요청 횟수로 확인해야 한다. 런타임 재현 결함으로 승격하지 않았고 3회가 되도록 수정하는 것은 별도 동작 수정 경계다.
- `apps/client/src/shared/services/auth/logout-service.ts`: 큐 삭제·DB reset·인증·캐시 정리는 반복되지만 로그아웃은 서버 실패 후에도 계속하고 계정 삭제는 바깥 catch로 끝난다. pending/inProgress는 hasPending에 포함되고 failed는 별도 반환된다. 옵션 많은 공통 절차보다 동일 로컬 책임의 범위를 후속 판단하도록 남겼다. 실제 삭제·reset은 실행하지 않았다.

## 기존 후보의 추가 경계와 제외한 통일

`ExpensesScreen.tsx:187`의 toFixed와 `shared/lib/currency.ts:115`의 천 단위 구분자는 출력이 다르므로 단순 helper 교체를 피한다. `currency.ts:69`의 “가장 많이 사용된 통화”와 명목 금액 정렬의 차이도 보고됐으나 앱 호출은 찾지 못했다. 빈도 정렬·환산을 추가할 근거로 삼지 않았다.

경비·일정 mutation의 캐시 대상은 다르고 일정 삭제는 경비 캐시도 갱신한다. 공통 hook이 이 차이를 없애면 보존에 실패한다. `shared/lib/datetime.ts:52`는 Date 입력을 직접 setHours로 변경하고 UTC ISO를 반환하며 offset·미래 상대 표현 예제도 실제 분기와 대조할 필요가 있다. 설명 정정과 날짜·입력 동작 변경은 나누었다.

UI Input·Checkbox·Switch는 짧고 명확해 범용 wrapper를 추가할 독립 개선 근거를 찾지 못했다고 보고했다. RadioGroup의 `as any`는 앱 사용처·prop 계약을 확인하기 전 첫 Ticket으로 올리지 않았다. 생성·수정 schedule schema는 필수성·허용 필드가 달라 단순 partial 통일을 채택하지 않았다.

## 작업 분해의 의미

다섯 초안은 경비 합계 규칙, 도시 검색, 저장 용량, 경비 API, 서버 일정 응답 변환이다. 각 범위가 실제 개선과 동작 보존 근거를 함께 만들도록 제안했으며 번호는 강한 기술 의존성이 아니다. 최소 검사 준비는 처음 필요한 Ticket에서 마련해 재사용하고 장기 기반 Ticket을 앞세우지 않는 제안이다. runner는 미선택이다.

폼·picker·날짜 그룹·저장 후 처리·공통 데이터 정리·완료 표현·설정·다른 서버 오류/변환은 후속 범위로 유지한다. 특히 Ticket 05의 일정 날짜 변환은 sync 단언·mutation any·중복 검증 전반을 해결하는 범위가 아니다. 현재 실행 정의와 검증 계획은 [Ticket 본문](../current/memory/tickets/index.md), 후보 관계는 [후보 목록](../current/memory/analysis-items.md)이 소유한다. 첫 추천은 경비 합계이며 사용자 채택이나 구현 착수로 해석하지 않는다.

## 함께 전달된 Evidence 사후 보존 보고

연결 문서는 앞선 Main이 자동 수집 전 대화 60개를 retrospective note로 보존하고 당시 bytes/hash 일치를 확인했다고 보고했음을 보충한다. 보고된 저장 경로는 `evidence-collector/store/recollections/846e3c64734effd3f30168c7ca0e341939c101f93d3e8f7124ab117f5a6e4466/20260910T135903.326183Z-b0d87f1f4f7e48518611b68b3a1a5261/note.md`다.

이번 조사나 Maintain 판단에서 그 메모를 읽거나 재검증하지 않았다. 실제 해시값과 원문 재현 범위는 제공되지 않았다. 사후 보존 보고는 자동 수집이 과거 구간까지 수행됐거나 response-end 처리가 모두 정상이라는 증거가 아니다.
