워커 구현과 독립 코드 전문가의 검증까지 마쳤습니다. **Ticket 06의 첫 네트워크 연결 범위는 구현과 테스트 검증을 마쳤고, Ticket 06 전체는 아직 완료가 아닙니다.** 리뷰 권고는 [Ticket 06](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/06-app-startup-lifecycle.md)과 네트워크 정책 합의에 제가 대조해 채택한 범위로 적용했습니다.

핵심 변화는 네트워크 상태를 *표시할 때*와 실제 작업을 *시작할 때*의 판단을 각 소비 경로에 연결한 것입니다.

- [SyncProvider](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/services/sync/provider.tsx)는 DB 초기화 성공, 인증 준비와 로그인, **실제** online, debug 강제 설정 해제를 모두 만족할 때만 새 sync를 시작합니다. 실행 중 Promise를 화면용 `isSyncing`보다 먼저 보관하므로 같은 순간의 자동·수동 호출은 한 실행의 완료를 함께 기다립니다. debug 화면의 수동 버튼도 이 경계를 거치며 차단·실패·engine 반환을 구별해 안내합니다. 여기서 “완료”는 engine 반환이지 queue의 모든 항목이 서버에 반영됐다는 뜻은 아닙니다.
- [Router](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/services/offline-prep/router.ts)는 여행 목록, 새 여행 생성, 특정 여행의 조회·수정을 서로 다른 입력으로 구별합니다. 특정 여행은 그 `tripId`의 활성 여부로 Local 또는 Remote를 고릅니다. 일정·경비 수정·삭제도 알려진 `tripId`를 호출부에서 전달해, 온라인 비활성 여행의 항목이 Local에 없어서 서버 경로에 이르지 못하던 문제를 없앴습니다. Trip 수정 요청은 서버 계약에 맞게 PUT으로 연결했습니다. offline·unknown의 Remote 호출과 debug 강제 설정 중 쓰기는 Router에서 차단합니다.
- 일정·경비 목록과 상세는 이전 서버 캐시가 남아 있어도 비활성 여행의 내용을 제한 안내로 가립니다. 같은 여행을 계속 보고 있고 실제 연결이 돌아오면 재조회 **성공 후** 내용을 다시 엽니다. 여러 화면이 같은 조회를 관찰할 때는 진행 중 요청을 공유하며, 초기 unknown에서 실패한 여행 목록도 online 전환 후 다시 조회합니다. 여행 선택과 작성 중인 폼 값은 유지하고, 저장·삭제 차단의 구체적인 이유를 기존 오류 흐름에서 한 번 안내합니다.
- 장소 검색·길찾기·Google 지도 요청 경계는 화면에 강제로 표시한 상태가 아니라 실제 연결을 사용합니다. Network Store의 기존 관측·세션 구조는 유지했고, 화면 표시가 필요한 ScheduleCard만 구독형 상태로 연결했습니다. 이처럼 요청 판단과 화면 표시의 책임을 분리한 것이 이번 가독성 개선의 중심입니다.

독립 검증자는 구현 뒤 **제한 안내 중복, 초기 여행 목록의 복구 누락, 다른 여행 삭제의 오류 이유 누락, 복수 조회자가 복구 요청을 중복시키는 위험**을 발견했습니다. 모두 보완한 안정 소스를 다시 검토했고, 이번 범위에서 남은 조치 대상 P1/P2는 찾지 못했다고 판정했습니다.

최종 client Jest는 **20개 묶음, 205개 테스트 통과**입니다. 독립 검증자의 별도 실행은 보강 테스트 추가 전 **19개 묶음, 204개 통과**였고, 실제 React Query를 사용한 별도 검사에서 복수 조회자의 요청 공유와 초기 목록 복구도 확인했습니다. 변경 client 파일 69개의 Prettier 검사와 변경 제품 코드 ESLint는 통과했습니다. 전체 typecheck는 기존 지도 관련 오류 3개 때문에 실패했으며, 이번 변경 경로의 새 타입 오류는 확인되지 않았습니다.

실제 Expo·기기 NetInfo·SQLite transaction·외부 API·서버·navigation stack은 실행 검증하지 않았습니다. DB/auth 실패 화면, 인증 route guard, 나머지 초기화와 Splash 연결은 Ticket 06의 후속 범위입니다. transaction 원자성, sync queue 결과·재시도, cleanup도 각각 별도 티켓 범위에 남습니다. 제품 코드·테스트·관련 기록은 현재 `refactor/app-startup-lifecycle`의 `7cfa7db` 이후 **미커밋** 상태이며, 이번 작업에서 커밋·push나 실제 데이터 쓰기는 하지 않았습니다.
