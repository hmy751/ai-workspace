Ticket 06의 **첫 네트워크 연결 범위 구현과 독립 검증을 마쳤습니다.** 품질 리뷰의 권고는 제가 티켓·9월 16일 합의와 대조해 채택 범위를 정했고, 워커 변경을 통합한 뒤 구현에 참여하지 않은 검증자가 최종 코드를 확인했습니다. 검증자는 이번 범위에서 남은 P1/P2 문제를 발견하지 못했습니다. 이 결과를 Ticket 06 전체 완료나 사용자 수락으로 확대하지는 않습니다.

핵심 변화는 네트워크 상태가 실제 동작에 쓰이는 경계를 맞춘 것입니다.

- [SyncProvider](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/services/sync/provider.tsx)는 DB 초기화 성공, 인증 준비·로그인, **실제** online, debug 강제 설정 해제를 함께 확인합니다. 로그인·연결 복구·강제 설정 해제 때 자동 sync가 시작될 수 있고, 동시에 들어온 자동·수동 호출은 진행 중인 한 작업을 함께 기다립니다. debug 화면의 수동 버튼도 이 경계를 사용해 차단·실패·engine 반환을 구별합니다. 여기서 `completed`는 queue 전체가 서버에 반영됐다는 뜻이 아닙니다.
- [Activation Router](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/services/offline-prep/router.ts)는 여행 목록, 새 여행 생성, 특정 여행의 조회·수정을 구별합니다. 활성 여행 A가 있어도 비활성 여행 B의 수정·삭제는 B의 `tripId`로 Remote 경로를 고릅니다. Schedule·Expense 수정·삭제도 이미 아는 `tripId`를 전달해 비활성 항목을 Local에서 먼저 찾던 의존을 제거했습니다. 실제 offline/unknown에서는 비활성 여행의 서버 요청을 열지 않고, 강제 설정 중에는 Local 쓰기까지 차단합니다.
- 일정·경비 목록과 상세 화면은 이전 서버 캐시를 지우지 않으면서 비활성 여행의 제한 내용을 가립니다. 같은 여행에서 실제 연결이 돌아오면 재조회가 성공한 뒤 내용을 다시 보이고, 실제 offline을 겪은 복구에만 안내를 표시합니다. 조회 실패·여행 선택 변경·초기 unknown 해소를 구별하며, 여러 화면이 같은 조회를 관찰할 때 진행 중 요청을 공유합니다. 작성 중인 폼 값과 여행 선택은 연결 변화나 저장 거부 때문에 초기화되지 않습니다. 저장·삭제 거부 이유는 기존 오류 안내에 전달됩니다.
- 장소 검색·길찾기와 Google 지도 마운트는 화면용 강제 online이 아니라 실제 관측 상태를 확인합니다. [Root](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/app/_layout.tsx)는 DB 준비 성공을 Splash 해제용 준비 종료와 구별하고, foreground 복귀 시 연결을 재확인합니다. 초기 unknown에서 실패한 여행 목록도 online 전환 뒤 다시 조회하며 기존 선택을 덮지 않습니다.

최종 client Jest는 **20개 suite·205개 test 모두 통과**했습니다. 독립 검증자는 그 직전 안정 소스에서 19개 suite·204개를 통과시키고 별도의 실제 React Query 검사로 다중 화면의 복구 요청 공유를 확인했습니다. 이후 그 사례를 영구 회귀 검사로 추가해 제가 최종 전체 검사를 실행한 결과가 205개입니다. 변경 파일 69개의 Prettier 검사, 변경 제품 코드 ESLint(오류 0·경고 6), `git diff --check`도 통과했습니다. Client typecheck는 기존 지도 관련 오류 3건 때문에 여전히 실패했고, 이번 변경 경로의 새 타입 오류는 확인되지 않았습니다.

실제 Expo·기기 NetInfo, SQLite transaction, 외부 지도·서버 요청과 navigation stack은 실행하지 않았습니다. DB/auth 실패 화면, 인증 route guard, 나머지 initializer·Splash 연결은 Ticket 06의 후속 범위입니다. transaction 원자성, sync queue별 결과·재시도, cleanup 보존도 각각 다른 티켓의 검증 책임으로 남습니다. 현재 제품 코드·테스트·관련 기록은 **미커밋**이며 커밋·push는 하지 않았습니다.
