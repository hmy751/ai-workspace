# 네트워크 관측과 화면 접근의 현재 연결

연결 상태가 바뀔 때 어떤 여행 내용과 입력을 계속 사용할 수 있는지, 화면 제한과 실제 요청이 어디까지 함께 동작하는지 확인할 때 읽는다. [여행 접근의 제품 의미](../common/travel-access.md)와 [Network·Policy 변경 가이드](../guidance/network-and-policy.md)를 현재 Store·Router·조회 hook·화면에 연결하는 본문이다.

**이 브랜치의 제품 기준은 `759cba3`이다.** 아래 기본 연결은 2026-09-25의 코드·검사 기록 대조를 바탕으로 한다. 활성 상태 최초 확인(1-A)은 당시 `refactor/app-startup-lifecycle` 미커밋 변경의 관찰이며 이 브랜치에 포함되지 않았다. 별도 작업의 이후 진척은 여기서 확인하지 않았다.

- 구현됨: 관측과 Debug 표시 구별, Router 실행 검사, 세 화면의 read 제한과 두 수정 Drawer의 기존 값 보존.
- 합의했지만 연결이 남음: 오프라인 새 여행 선택 거절, 복구 재조회·1회 안내, foreground·unknown 안내 끝단, 직접 Places 요청의 실제 online 검사.
- 열린 제품 판단: 경비 날짜 변경 뒤 기존 일정 연결을 유지·해제·재선택하는 UX.

10월 1일 문서 수정은 코드 대조이며 새 제품 실행 검증이 아니다.

## 앱 진입과 실제 요청은 다른 조건을 사용한다

[AppInitialization](../../../apps/client/src/application/AppInitialization.tsx)은 DB를 준비하고 Auth Store 복원 시도가 끝나면 앱을 연결한다. DB 실패는 삭제 없는 재시도, 인증 복원 실패는 로그인 화면의 restore-failed로 이어진다. 네트워크 unknown도 진입할 수 있으므로 앱 화면 진입이 서버 연결·로그인 성공을 뜻하지 않는다.

| 소비자 | 사용하는 조건 | 현재 보장 |
| --- | --- | --- |
| [Network Store](../../../apps/client/src/shared/store/network.ts) | NetInfo의 연결·도달성 신호 | 실제 online/offline/unknown을 유지한다. Noline 서버 가용성을 판정하지 않는다. |
| [Policy](../../../apps/client/src/shared/policy/useAppPolicy.ts)·[상태 표시](../../../apps/client/src/shared/components/Navigation/NetworkStatusIndicator.tsx) | `useDisplayNetworkStatus`의 실제 상태 또는 override | 화면 실험용 상태를 사용할 수 있다. Unknown에서는 offline 권한표를 쓰되 실제 관측은 유지한다. |
| [Activation Router](../../../apps/client/src/shared/services/offline-prep/router.ts) | Local 계정·대상 활성 여부, Remote의 인증·실제 online | 실행 출처를 고르고 override 동안 Local·Remote mutation을 거절한다. |
| [sync lifecycle](../../../apps/client/src/shared/services/sync/lifecycle.ts) | DB 준비·인증·실제 online·override·종료 pause | 표시만 online으로 바꿔도 새 sync는 열리지 않는다. |

지도·경로·activation의 직접 write와 모든 Service 요청까지 동일한 override 차단을 거친다는 보장은 확인하지 않았다. Local 계정과 실제 저장의 연결은 [세션 현황](session-and-local-data.md)에 있다.

## 현재 화면은 캐시 보유와 접근 허용을 구별한다

`useAppPolicy`는 Schedule·Expense CRUD의 허용 여부와 Service 선택을 제공한다. Local session이 없으면 Entity 작업을 막고, 재인증이 필요한 상태에서는 활성 여행의 Local 작업을 유지하며 비활성 여행의 Entity 작업을 막는다. Service는 별도의 네트워크·활성 상태 표를 사용하므로 인증 만료만으로 전체 서비스를 offline으로 만들지 않는다.

[ScheduleScreen](../../../apps/client/src/screens/ScheduleScreen.tsx), [ExpensesScreen](../../../apps/client/src/screens/ExpensesScreen.tsx), [ExpenseDetailScreen](../../../apps/client/src/screens/ExpenseDetailScreen.tsx)은 read 정책이 허용하지 않으면 남은 Query 데이터 대신 제한을 표시한다. 두 목록의 수정 Drawer는 내용 제한 분기 밖에 있어 제한이 생겼다는 이유만으로 form state를 버리지 않는다. 이 세 화면의 연결을 Schedule 상세나 모든 화면의 접근 제어 완료로 확대하지 않는다. Schedule 목록에는 헤더와 본문 양쪽의 제한 표시가 있어 전체 안내 중복까지 정리된 상태도 아니다.

수정 form에서도 서비스 제한과 기존 값의 보존을 구별한다. [일정 수정](../../../apps/client/src/features/schedule/update-schedule/UpdateScheduleDrawer.tsx)은 새 장소를 선택하지 않으면 장소·좌표 필드를 payload에서 생략하고, [경비 수정](../../../apps/client/src/features/expense/update-expense/UpdateExpenseDrawer.tsx)은 manual-only에서도 기존 일정 연결을 표시하고 저장한다. 이 적용은 [Drawer 검사](../../../apps/client/tests/features/edit/offline-values.test.tsx)가 다루는 기존 값·연결·제한 복귀 범위다. 새 장소 선택 뒤 연결 전환이나 모든 form의 native 입력 보존까지 확인한 것은 아니다.

### 활성 여부 최초 확인의 후속 구현

`759cba3`에서는 활성 조회의 결과 부재를 비활성 기본값으로 사용했다. 9월 25일 원래 작업 트리에서 확인한 `useAppPolicy`는 [useGetTripActivation](../../../apps/client/src/entities/trip/data/useGetTripActivation.ts)의 `undefined`와 `null`을 구별한다. 아직 성공 결과가 없는 undefined에서는 CRUD를 확인 중 또는 최초 조회 실패로 표시하고, 성공 후 기록 없음인 null은 비활성 정책에 맡긴다. 기존 결과가 있으면 background 재조회 중·실패 뒤에도 그 결과를 유지한다. Local session이 없으면 로그인 안내를 먼저 적용한다.

원래 작업 트리의 `PolicyErrorDisplay`는 `pending`을 진행 표시로 표현하며 기존 목록·상세·수정 form은 같은 정책 소비를 재사용한다. 활성 조회 전용 재시도 버튼을 새로 제공한 것은 아니다. 활성 조회 hook 검사와 화면 검사는 제어 가능한 DB/조회 응답으로 최초 대기·실패·기록 부재·기존 결과 유지·대상 변경을 다룬다. 이 제품 코드·검사는 이 브랜치에 포함하지 않았으며, 파일 위치와 당시 Ticket 06 실행 보고는 [분리 시점의 1-A 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-28-01-project-context-branch-separation.md#제품-작업-1-a의-분리-시점-기록)에 보존했다. 이 변경은 대조 시점에 미커밋이며 native SQLite·실기기 화면 검증이나 전체 네트워크 안내 완료를 뜻하지 않는다.

## 선택 보존과 복구 조회는 별도로 연결해야 한다

**목록 결과 때문에 선택을 지우는 경우는 보호돼 있다.** [TripRepository](../../../apps/client/src/entities/trip/repository/trip-repository.ts)와 [useGetTrips](../../../apps/client/src/entities/trip/data/useGetTrips.ts)가 목록의 Local/Remote 출처를 전달한다. [useTripSelection](../../../apps/client/src/entities/trip/data/useTripSelection.ts)은 성공·종료한 Remote 목록과 실제 online을 모두 확인한 뒤 선택한 여행의 제거를 판단한다. 선택이 없으면 대표 여행 또는 첫 항목을 고른다.

아래는 이 연결만으로 해결되지 않은 부분이다.

| 남은 연결 | 현재 근거와 영향 |
| --- | --- |
| Offline에서 새 비활성 여행 선택 거절 | [TripSelector](../../../apps/client/src/entities/trip/ui/TripSelector.tsx)의 `handleTripChange`는 연결·활성 조건을 검사하지 않고 선택을 바꾼다. 2026-10-01 코드 대조에서 확인했다. 목록에 후보가 남아 있으면 합의한 선택 보존을 이 handler가 보장하지 않는다. |
| 같은 비활성 여행의 복구 재조회·성공 1회 안내 | [Query 설정](../../../apps/client/src/shared/lib/queryClient.ts)은 reconnect refetch를 끈다. 활성 여행 sync/pull은 이 재조회를 대신하지 않는다. 캐시 재표시도 조회 성공이 아니다. |
| Foreground 재확인·unknown 안내 끝단 | 확인 중·확인 불가·재확인 행동과 초기 unknown 해소/장애 복구 구별의 화면 연결이 남아 있다. |
| 공개 Places 실행 전 실제 online 검사 | [장소 검색 hook](../../../apps/client/src/features/schedule/create-schedule/useLocationSearch.ts)의 enabled는 검색어 조건이다. 검색·상세 요청마다 최신 실제 네트워크를 확인하는 guard는 없다. |

이 항목들은 [여행 이용](../common/travel-access.md)의 합의와 구현 사이의 간격이다. 공개 Places에는 보호 API interceptor가 없어 재인증 자체가 보호 요청 오류를 만들지는 않는다. 공개/보호 client의 실제 구분은 [API 가이드](../guidance/api-contracts.md)에서 확인한다.

## 근거의 범위와 갱신 시점

[Store 검사](../../../apps/client/tests/shared/store/network.test.ts), [Router 검사](../../../apps/client/tests/shared/services/offline-prep/router-network.test.ts), [선택 검사](../../../apps/client/tests/entities/trip/data/useTripSelection.test.tsx), 화면·Drawer 검사는 관측값·호출 경로·component 상태의 근거다. 실제 NetInfo 전환 빈도, Expo 진입, 외부 Places, native Drawer와 전체 navigation 경험은 이 근거로 입증되지 않는다. 과거 소비 확대 구현의 철회와 최종 검사 대상은 [현재 제품 저장·검증 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-22-02-five-stage-commits-and-verification.md)에서 구별한다.

관측·표시 selector, Router 실행 조건, 활성 조회의 반환 의미, 화면 read/Drawer 배치, query 재조회 또는 Service 호출부가 바뀌면 그 변경 책임자가 이 연결과 검사를 다시 대조한다. 특히 별도 제품 브랜치의 활성 확인 변경을 통합하거나 복구 안내를 연결할 때에는 이 본문의 지원 범위와 남은 간격을 함께 갱신한다.
