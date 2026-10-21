# 날짜 차이·foreground 추가 확인 — 2026-10-04

기존 9/30 보고서에서 열린 날짜 원인과 foreground 갱신 주장을 추가 확인했다. 현재 날짜 차이는 실제 여행 원본과 시간대로 설명된다. foreground마다 최신 연결을 확인하는 별도 연결은 앱과 설치 NetInfo 모두에서 찾지 못했지만, 일반 native 관측과 반복 인터넷 도달 확인은 존재한다.

## 현재 날짜 차이: 원인 확인

현재 시뮬레이터 `D22939DA-F2A4-4F24-B286-197DC62F415C`, 앱 `com.noline.dev`의 `Documents/SQLite/noline.db`를 `sqlite3 -readonly`로 읽었다. user_id·인증·큐·다른 사용자 정보를 조회하지 않았다. 최소 SELECT는 `id,destination,start_date,end_date`만 대상으로 했다.

```sql
SELECT id,destination,start_date,end_date
FROM trips
WHERE deleted_at IS NULL AND (destination='파리' OR destination='Paris');
```

현재 메인 화면의 기간과 대응하는 파리 행:

```text
id: 01M3RVD3X9VSV0M44TET19H5DS
start_date: 2026-09-29T22:00:00.000Z
end_date: 2026-10-01T22:00:00.000Z
```

다른 파리 행은 `01KG727ZSTMBWMB6NEX3W6PM33`, 1/6~1/9 UTC 자정 기간이다. 화면에 보이는 두 여행 기간을 구별할 수 있다.

시뮬레이터에 `/bin/date '+%Y-%m-%d %H:%M:%S %Z %z'`를 읽기 전용으로 실행한 결과는 `2026-10-04 14:47:35 KST +0900`이다. `launchctl getenv TZ`는 빈값이어서 시간대 확정 근거로 사용하지 않았다.

현재 helper `getUTCDateRange`를 import하고 위 실제 원본 값으로 메모리 실행했다. `TZ=Asia/Seoul`에서 홈의 현지 getMonth/getDate 계산도 함께 실행했다. fixture가 아니다.

| 실제 원본의 해석 | 결과 |
| --- | --- |
| 현지 start | 2026-09-30 07:00 KST |
| 현지 end | 2026-10-02 07:00 KST |
| 홈 표시 계산 | 9월30일~10월2일 |
| 목록 helper 결과 | 2026-09-29, 2026-09-30, 2026-10-01 |

이는 [현재 화면 관찰](observations.md)의 홈 기간과 목록 첫·마지막 날짜에 정확히 대응한다. **현재 화면의 날짜 차이는 같은 timestamp를 홈은 현지 날짜, 목록은 UTC 날짜로 읽어서 발생한다.** 생성 경로나 원래 사용자 의도는 이번 조회로 확정하지 않는다. 과거 [9/30 증거](../ux-review-20260930/evidence.md:64)의 동일 모양도 이 계산으로 설명할 수 있지만 당시 DB snapshot·시간대가 없으므로 당시 원본까지 소급 확정하지 않는다.

코드와 현재 책임 근거:

- [홈 현지 표시](../../../apps/client/src/screens/HomeScreen/MainTripSection.tsx:33): new Date 후 getMonth/getDate.
- [일정 범위](../../../apps/client/src/screens/ScheduleScreen.tsx:91), [경비 범위](../../../apps/client/src/screens/ExpensesScreen.tsx:59): getUTCDateRange.
- [범위 helper](../../../apps/client/src/shared/lib/datetime.ts:81): UTC 자정·UTC 날짜 순회.
- [Trip 생성](../../../apps/client/src/features/trip/create-trip/useCreateTripForm.ts:80), [수정](../../../apps/client/src/features/trip/update-trip/EditTripDrawer.tsx:77): dateToISODateTime. [helper](../../../apps/client/src/shared/lib/datetime.ts:244)는 date-only를 UTC 자정으로 만들고 datetime은 동일 시점을 Z로 정규화한다. 현재 실제 행의 22:00이 이 date-only 경로로 만들어졌다고 주장하지 않는다.
- [공유 Trip 계약](../../../packages/schema/src/entities/trip.ts:31)은 offset 포함 ISO datetime이다.
- [현재 날짜 책임](../../../context/project/common/date-and-time.md:45)은 목록 UTC 범위와 기존 Trip 현지 표시를 유지하며, [51행](../../../context/project/common/date-and-time.md:51)은 Trip이 장기적으로 달력 날짜인지 시점인지 결정하지 않았다.

다음 판단: 날짜 차이를 원인 미상 항목으로 남길 필요는 없다. 해결하려면 여행의 시작일·종료일을 어떤 달력 날짜로 보여줄지 제품 기준을 정해야 한다. 홈만 UTC로 바꾸거나 목록만 현지로 바꾸는 선택은 Trip 입력·주요 여행 선택·활성 만료와 함께 판단한다. 이번 홈 제한 안내 수정과 분리할 수 있다.

## Foreground: 명시적 재확인과 일반 갱신을 구별

설치 버전은 [NetInfo package](../../../node_modules/@react-native-community/netinfo/package.json:3)의 11.4.1이다. 아래는 설치된 원본의 사실이며 native 통신 성공을 새로 검증한 결과가 아니다.

- 앱 [AppInitialization](../../../apps/client/src/application/AppInitialization.tsx:63)은 mount init / unmount cleanup이다. 앱 src·app·tests에서 AppState 연결을 찾지 못했다.
- 앱 [network refresh](../../../apps/client/src/shared/store/network.ts:112)는 명시적 요청을 공유하고 [370행](../../../apps/client/src/shared/store/network.ts:370)에서 NetInfo.refresh를 호출한다. [안내 버튼](../../../apps/client/src/shared/components/ErrorBoundary/PolicyErrorDisplay.tsx:96)은 이 refresh를 실행한다.
- 설치 iOS [RNCConnectionStateWatcher](../../../node_modules/@react-native-community/netinfo/ios/RNCConnectionStateWatcher.m:124)는 SCNetworkReachability callback을 main runloop에 연결하고 최초 flags를 읽는다. [RNCNetInfo](../../../node_modules/@react-native-community/netinfo/ios/RNCNetInfo.m:83)는 변경을 JS event로 전달한다. foreground notification을 받아 별도 조회하는 코드는 두 파일에서 발견하지 못했다.
- 설치 JS [State](../../../node_modules/@react-native-community/netinfo/src/internal/state.ts:29)는 native event를 구독하고 생성 때 current state를 읽는다. [명시적 refresh](../../../node_modules/@react-native-community/netinfo/src/index.ts:77)는 `_fetchCurrentState()`를 실행한다. 설치 src에서 AppState 연결을 찾지 못했다.
- iOS native 응답은 [type/isConnected/details](../../../node_modules/@react-native-community/netinfo/ios/RNCNetInfo.m:117)를 반환한다. [internetReachability](../../../node_modules/@react-native-community/netinfo/src/internal/internetReachability.ts:152)는 native boolean isInternetReachable이 없으면 JS 도달 확인을 사용한다. 연결이 예상되고 reachabilityShouldRun이 true이면 [HTTP 확인](../../../node_modules/@react-native-community/netinfo/src/internal/internetReachability.ts:56)을 시작하고, [결과 뒤 timer](../../../node_modules/@react-native-community/netinfo/src/internal/internetReachability.ts:109)로 반복한다. [설치 기본값](../../../node_modules/@react-native-community/netinfo/src/internal/defaultConfiguration.ts:9)은 실패 시 5초·성공 시 60초이며 앱의 NetInfo.configure는 찾지 못했다.
- [설치 README 461행](../../../node_modules/@react-native-community/netinfo/README.md:461)은 iOS background에서 Wi-Fi 변경 이벤트가 전달되지 않아 상태가 어긋날 수 있고, foreground 복귀마다 다시 읽으라고 안내한다. [457행](../../../node_modules/@react-native-community/netinfo/README.md:457)은 simulator의 host Wi-Fi 변경 알림 문제도 적는다.
- 앱 [SyncProvider](../../../apps/client/src/shared/services/sync/provider.tsx:45)는 인증·실제 네트워크·override·pause의 실행 가능 조건 전환으로 sync를 요청한다. foreground 자체는 별도 실행 원인이 아니다.

**확인된 결론:** 앱과 설치 라이브러리에는 foreground마다 즉시 재확인하도록 연결한 코드가 없다. 일반 관측·JS 반복 도달 확인으로 상태가 갱신될 수 있으므로 “복귀 뒤 아무 갱신도 없다”는 결론은 근거를 넘는다. 단순 복귀 화면이 온라인이었다는 사실은 foreground 전용 확인 호출이나 최신 상태 검증 성공을 증명하지 않는다.

기존 mock 테스트는 [init/listener](../../../apps/client/tests/shared/store/network.test.ts:104), [명시 refresh](../../../apps/client/tests/shared/store/network.test.ts:250), [실제 상태를 주입한 online 전환의 sync](../../../apps/client/tests/shared/services/sync/provider-network.test.tsx:256)를 다룬다. AppState/native foreground 검증을 찾지 못했다. 이번에 테스트 재실행·새 테스트를 하지 않았다.

다음 판단: 복귀 때 최신 확인을 즉시 시작한다는 보장이 필요하면 AppState 복귀→기존 network refresh 연결과 실제 기기 검증이 별도 후속 작업이다. 온라인 화면 정상 복귀 자체는 현재 관찰로 닫고, background 연결 변화 후 최신성 보장은 열린 항목으로 남긴다.

## 실행 경계

초기 sandbox simctl은 CoreSimulatorService 연결과 로그 파일 접근 제한으로 실패했다. 읽기 전용 list/get_app_container/spawn date를 승인된 escalation으로 재실행해 성공했다. DB는 -readonly로 조회했으며 앱·DB·기기 설정·제품 코드·Workspace 문서를 변경하지 않았다. UI 제어·Simulator 화면 조작·네트워크 변경을 하지 않았다. 이 추가 근거 파일만 생성했다.
