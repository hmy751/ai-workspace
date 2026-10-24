워커 구현과 독립 검증 결과가 모두 모였습니다. **최종 소스·검사 기록 기준으로, 합의한 네트워크 소비 연결 개선 범위는 충족됐고 독립 검증자가 남은 P1/P2 문제를 발견하지 못했습니다.** Ticket 06 전체 완료와 실기기 검증은 별도로 남아 있습니다.

이번 변경의 중심은 Network Store가 관측한 상태를 **실제 요청, 화면 안내, sync 실행이 각자의 책임에 맞게 소비하도록 연결한 것**입니다. 활성 여행은 이 기기의 SQLite를 사용하고, 비활성 여행은 서버를 사용한다는 기존 구조를 유지했습니다. 리뷰 권고의 적용 범위도 Ticket과 합의에 맞춰 제한됐습니다.

**sync는 자동 실행과 실제 debug 버튼이 같은 보호 경계를 사용합니다.**

이전에는 `isSyncing`이라는 React 표시 상태로 중복 실행까지 막으려 했습니다. 화면이 다시 그려지기 전 두 번 호출하면 두 호출 모두 실행될 수 있었고, debug 버튼은 Provider를 우회했습니다. 최종 [SyncProvider](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/services/sync/provider.tsx)는 DB 초기화 성공·인증 초기화 및 로그인·실제 online·override 해제를 시작 조건으로 확인하고, 진행 중 작업을 즉시 소유합니다.

```tsx
if (inFlightRef.current) {
  return inFlightRef.current;
}
```

뒤이어 새 실행의 Promise를 `inFlightRef.current`에 저장한 다음 `setIsSyncing(true)`를 호출합니다. 그래서 자동 시작과 수동 연타가 겹치면 engine을 한 번 실행하고, 후속 호출도 그 작업의 완료를 기다립니다. 화면 표시와 실행 소유권이 코드에서 구별됩니다. 실제 debug 버튼도 이 함수를 호출하며 `blocked`·`failed`·`completed`를 구분합니다. 여기서 `completed`는 engine이 반환됐다는 뜻이며, queue 전체가 서버에 반영됐다는 보장은 아닙니다.

Root도 Splash 해제용 준비 종료와 DB 준비 성공을 구별해 Provider에 전달합니다. 네트워크 확인 때문에 DB·인증 준비를 기다리게 하지 않고, background에서 돌아오면 연결을 재확인합니다. 기본 여행 선택은 이미 있는 사용자 선택을 덮지 않습니다.

**저장 위치는 수정하려는 여행을 기준으로 판단합니다.**

예를 들어 활성 여행 A가 있어도 비활성 여행 B의 경비를 수정하면 B의 서버 경로를 사용해야 합니다. 이전에는 대상 여행 대신 전역 활성 여부를 보거나, B의 경비를 먼저 Local에서 찾아야 해서 서버 요청 전에 실패할 수 있었습니다.

최종 [ExpenseRepository](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/entities/expense/repository/expense-repository.ts)의 수정 경계는 다음처럼 바뀌었습니다.

```ts
update: async (id: string, tripId: string, data: UpdateExpenseRequest): Promise<Expense> => {
  return await routeChildMutation(tripId, {
    local: () => ExpenseLocal.updateExpenseLocal(id, data),
    remote: () => ExpenseApi.fetchUpdateExpense(id, data),
  });
},
```

호출자가 이미 아는 `tripId`를 전달하고, [Router](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/services/offline-prep/router.ts)가 그 여행의 활성 여부와 실행 순간 네트워크를 판단합니다. 같은 연결이 Trip 단건 작업, Schedule·Expense 수정·삭제와 일정별 경비 조회까지 이어집니다. 정상 모드의 활성 여행은 unknown/offline에도 Local을 사용하고, 비활성 여행의 Remote 작업은 실제 online에서만 시작합니다. override 중에는 Router가 Local·Remote 쓰기를 모두 거부합니다.

전체 여행 목록의 기존 Local/Remote 분기는 유지했고, 새 여행은 서버에서 생성합니다. Trip 수정 요청은 기존 서버 계약에 맞춰 PUT으로 연결됐습니다. 이 변경으로 온라인 비활성 여행을 지원하면서도 Local 선조회가 필요하다는 숨은 전제가 제거됐습니다.

**화면은 캐시를 보존하면서 접근 제한과 복구를 구별합니다.**

비활성 여행 B의 내용을 보다가 연결이 끊겼다는 설명용 장면으로 보면, 최종 연결은 다음과 같습니다.

| 상황 | 화면과 요청의 결과 |
| --- | --- |
| offline 또는 unknown으로 바뀜 | 여행 선택·탭·기존 캐시는 유지하고 일정·경비 본문에 제한 안내 표시 |
| unknown이 10초 지속됨 | 확인 불가와 재확인 행동 표시. 전역 상태를 offline으로 바꾸는 시간 제한은 아님 |
| 같은 B를 보던 중 실제 online으로 돌아옴 | 내용을 재조회하고 성공 전까지 이전 캐시 본문을 숨김 |
| 복구 조회 성공 | 내용을 다시 열고, 실제 offline을 겪은 경우에만 복구 안내 표시 |
| 복구 실패 또는 다른 여행으로 이동 | 오류·재시도를 제공하거나 이전 여행의 늦은 완료를 무시함 |

이 흐름은 [useTripContentAccess](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/policy/useTripContentAccess.ts)와 실제 목록·상세 화면에 연결돼 있습니다. 초기 unknown 해소에는 복구 안내를 붙이지 않습니다. 여러 화면이 같은 조회를 관찰할 때는 `cancelRefetch: false`로 진행 중 요청을 공유합니다.

폼은 연결 변화나 Router 거부 때문에 닫거나 초기화하지 않고, 기존 오류 흐름에서 제한 이유를 안내합니다. 복구 뒤 저장을 자동 재실행하지 않습니다. 장소 검색·길찾기·Google 지도 마운트도 실제 관측을 사용하므로 화면을 강제 online으로 표시해도 실제 offline/unknown의 요청을 열지 않습니다.

독립 검증에서 발견한 **초기 unknown 뒤 여행 목록 미복구, Schedule 제한 안내 중복, Home 여행 삭제의 제한 이유 누락, 다중 화면 복구 조회의 중복 전송 위험**도 최종 상태에서 보완 확인됐습니다. Network Store의 기존 session·늦은 응답 보호 구조는 유지했고, 추가 파일 분할이나 범용 startup 체계는 도입하지 않았습니다.

검사 기록은 다음과 같습니다.

- **최종 전체 Jest: 20개 suite·205개 test 통과.** 앞서 안내된 19개·204개에 실제 React Query의 다중 소비자 회귀 검사가 추가된 결과입니다. 이 검사는 요청 1회 공유와 복구 성공 전 캐시 본문 숨김을 확인합니다.
- **독립 검증자:** 직전 안정 소스의 전체 204개 test와 별도 React Query 검사 2개를 직접 통과시켰습니다. 합의·수정 전 baseline·최종 소스·실제 호출부를 대조한 판정입니다.
- 변경 client source·test·설정 69개 파일의 형식 검사는 통과했습니다. 변경 제품 코드 ESLint는 오류 0개, 기존 경고 6개입니다. 기존 연동 문제로 Prettier 규칙은 ESLint에서 제외하고 별도 검사했습니다.
- **전체 typecheck는 기존 지도 오류 3개로 실패 상태입니다.** `shared/lib/mapbox.ts:61`과 `shared/services/offline-map/download.ts:165–166`이며, 변경 경로에서 새 타입 오류는 확인되지 않았습니다.

확인 범위는 코드와 hook/component 검사까지입니다. 실제 Expo·native NetInfo·지도 요청·SQLite transaction·서버·navigation stack, 기기에서의 연결 변동 빈도와 데이터 격리는 미확인입니다. override의 보호도 Router 쓰기와 새 sync에 대한 것이며, debug의 reset·직접 DB 도구 전체가 차단됐다는 뜻으로 확대할 수 없습니다.

[Ticket 06](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/06-app-startup-lifecycle.md)과 [개선 기록](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/records/2026-09-17-02-network-consumer-quality-improvements.md)에 결과와 한계가 반영돼 있습니다. 제품 코드·테스트·관련 문서는 미커밋입니다. Ticket 06의 후속 범위는 DB/auth 실패 화면·인증 route guard·나머지 initializer와 Splash 연결이며, SQLite 원자성은 14번, sync 내부 결과·재시도는 15번, cleanup은 16번에 남아 있습니다.
