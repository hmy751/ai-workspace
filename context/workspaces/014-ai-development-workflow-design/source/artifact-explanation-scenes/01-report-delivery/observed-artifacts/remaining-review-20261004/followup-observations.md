# 제한·복귀·picker 추가 관찰 — 2026-10-04

이전 묶음은 정상 목록·상세·폼만 관찰하여 비활성 목록이 제한되고 돌아오는 흐름과 picker 취소 후 초안 상태를 확인하지 못했다. 이번에는 기존 비활성 여행을 조회 선택하고 Debug 상태를 바꿔 대표 흐름을 직접 관찰했다. 원인·수락·우선순위는 판단하지 않는다.

## 기존 여행 online → unknown → offline → null

시작은 활성 파리9/30~10/2, 온라인, override null. 일정 TripSelector에서 두번째 기존 파리를 선택했다. 일정·경비 선택이 동일 비활성 파리1/6~1/9로 이어졌다. 여행 활성화·해제나 데이터 변경은 하지 않았다. 실제 네트워크는 Debug에서 계속 online, 변경한 것은 강제설정 unknown/offline이다.

| 파일 | 실제 보이는 상태 |
| --- | --- |
| 09-inactive-schedule-online.jpg | 파리 선택에 메인/활성화 표식 없음. 온라인,1/6~1/9 각0개와 추가 동작. |
| 10-inactive-expense-online.jpg | 같은 여행,온라인,EUR7.00,1/6의 기존 Expense remote1002 recovered 카드1개. |
| 11-inactive-expense-unknown.jpg | 상단 확인불가,여행선택 유지. 정상 합계·날짜·카드 대신 작업을수행할수없습니다/인터넷연결을확인할수없어요./다시확인 버튼1개. |
| 12-inactive-schedule-unknown.jpg | 확인불가,같은여행. 정상 날짜목록 대신 동일 제목·설명·다시확인 버튼1개. |
| 13-inactive-schedule-offline.jpg | 오프라인,같은여행. 작업을수행할수없습니다/인터넷에연결되어있지않아요.오프라인에서는활성여행을선택해주세요. 재시도버튼 없음. |
| 14-inactive-expense-offline.jpg | 오프라인,같은여행. 같은 제한 제목·설명,합계·경비카드 가림. 재시도버튼 없음. |
| 15-inactive-expense-restored.jpg | Debug 실제 버튼으로 override null 확인 후 경비탭복귀. 온라인,같은 비활성선택,EUR7.00와 기존 경비카드1개 재표시. |
| 16-inactive-expense-detail.jpg | 복귀한 기존 경비 클릭. EUR7.00,Expense remote1002 recovered,기타,1/6,영수증없음. 연결된일정 영역 없음. |
| 17-inactive-schedule-restored.jpg | 같은 비활성선택의 일정탭복귀. 온라인,1/6~1/9 각0개 다시 표시. |

unknown에서 다시확인 버튼은 누르지 않았다. 실제단절·서버강제실패·다시확인 성공을 검증한 흐름은 아니다. 비활성 여행 일정0개이므로 기존 일정상세 제한 대조는 없다. 경비수정 진입·연결변경은 추가하지 않았고 연결조건을 만들기 위해 새 데이터를 생성하지 않았다.

## 일정 추가 picker와 저장 없는 초안

원래 메인/활성화 여행을 다시 선택한 후9/30 추가→장소직접입력→제목 REPORT-1004 입력. 날짜와 시간을 열고 값선택/확인을 누르지 않은 채 backdrop으로 닫았다.

- 18-schedule-date-picker.jpg: 제목 REPORT-1004 뒤에 날짜선택 bottom sheet,10월2026 달력,확인 버튼. 열기 전 폼 날짜는2026-09-30이었다. OS-native 여부는 화면만으로 판정하지 않는다.
- 19-schedule-time-picker.jpg: 같은 제목 뒤 시간선택 bottom sheet,표시00:00,확인 버튼. 열기 전 폼 시간은09:00이었다.
- 20-schedule-draft-preserved.jpg: 두 picker 닫기후 제목 REPORT-1004,날짜2026-09-30,시간09:00 유지. 확인·날짜/시간 선택·저장은 누르지 않았다. 최종 취소해 목록으로 복귀했다.

같은 열린 폼의 unknown 왕복은 여전히 미수집: 폼에 하단탭/Debug진입이 없고 기존Debug로 가려면 폼을 떠나야 한다. 새 runtime 계측이나 bridge를 넣지 않았다. 이 picker 초안 보존을 네트워크 전환 초안 보존으로 확장하지 않는다.

## 도구 제약과 복원

여행 선택 sheet는 Native AX에 전체element만 노출하여 둘째행을 screenshot 좌표로 누르려 했다. CUA noWindowsAvailable이 재연결후에도 발생했다. Simulator 창 자체 AX클릭으로 입력대상을 활성화한 후 같은 기존행 좌표선택이 성공했다. MobileBuild tap API는 elementRef만 지원했고 sheet개별행 target이 없어 좌표대안으로 쓰지 않았다.

최종 override null/실제online, 원래 메인활성여행 선택 복원. 초안 취소 후 홈에서 파리9/30~10/2,준비완료,일정2개/EUR56.00 확인. 계정·데이터·설정·소스 변경 없음. 기존 Metro 유지,시뮬레이터 조작 종료/제어 반환.
