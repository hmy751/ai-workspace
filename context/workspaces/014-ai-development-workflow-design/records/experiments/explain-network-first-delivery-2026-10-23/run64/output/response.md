워커 구현과 독립 검증을 마쳤습니다. **Ticket 06의 첫 네트워크 연결 범위는 코드와 자동 검사 기준으로 충족**했습니다. 독립 검증자는 티켓·합의 기록을 수정 전 코드와 최종 코드에 대조해 남은 P1/P2 문제를 발견하지 못했습니다. 이는 Ticket 06 전체 완료나 실기기 동작의 수락 판정은 아닙니다.

이번 변경의 중심은 네트워크 상태를 실제 요청과 화면 표시가 각자 올바르게 쓰도록 연결한 것입니다. sync는 DB 초기화 성공·인증 완료·실제 online·debug 강제 설정 해제를 확인한 뒤 시작합니다. 자동 시작과 수동 버튼이 같은 실행 경계를 사용하며, 동시에 눌러도 진행 중인 한 작업을 함께 기다립니다. 따라서 debug 버튼이 보호 조건을 우회하던 문제와 같은 순간 sync가 두 번 실행되던 문제를 해결했습니다. 앱이 다시 foreground로 오면 연결을 재확인하고, 여행 목록이 회복돼도 사용자가 고른 여행은 덮어쓰지 않습니다.

여행 데이터는 **대상 여행의 활성 여부**로 분기합니다. 활성 여행 A가 있어도 비활성 여행 B의 수정·삭제는 실제 online에서 서버 경로로 가며, 일정·경비가 기기 DB에 없다는 이유로 그 경로가 막히지 않도록 Local 선조회를 제거했습니다. offline·unknown에서는 비활성 여행의 서버 요청을 시작하지 않고, debug 강제 설정 중 쓰기도 차단합니다. Trip 수정 요청 방식도 서버의 PUT 계약에 맞췄습니다.

일정·경비 목록과 상세 화면은 이전 서버 응답이 캐시에 남아 있어도 제한 상태에서는 내용을 가리고 이유를 안내합니다. 같은 비활성 여행이 실제 online으로 돌아오면 재조회가 성공한 뒤 내용을 다시 보여 줍니다. 여러 화면이 같은 조회를 기다릴 때 요청을 공유하도록 보완했고, 폼 입력은 연결 변화나 저장 거부 뒤에도 유지됩니다. 장소 검색·길찾기·온라인 지도는 화면의 강제 online 표시가 아니라 실측 연결을 따릅니다.

독립 검증에서 일정 화면의 중복 안내, 초기 unknown 뒤 여행 목록의 회복 누락, 다른 여행 삭제 시 제한 이유가 일반 오류로 덮이는 문제, 다중 조회자가 복구 요청을 중복 전송할 위험을 찾았고 모두 보완했습니다. 최종 client Jest는 **20개 묶음·205개 테스트 통과**, 변경된 69개 client 파일의 형식 검사와 변경 제품 코드의 ESLint는 오류 없이 통과했습니다. 타입 검사는 기존 지도 코드 오류 3개 때문에 여전히 실패하며, 이번 변경 경로의 새 타입 오류는 보고되지 않았습니다.

실제 Expo·native NetInfo·SQLite transaction·외부 API·서버·navigation stack은 실행하지 않았습니다. DB/auth 실패 화면, 인증 route guard, 나머지 Splash·initializer 연결은 Ticket 06의 후속 범위이고, transaction 원자성·sync 내부 재시도·cleanup은 각각 다른 티켓의 책임으로 남습니다. 제품 코드·테스트·관련 기록은 현재 `refactor/app-startup-lifecycle`의 `7cfa7db` 이후 **미커밋** 상태입니다. 세부 근거와 검증 경계는 [Ticket 06](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/06-app-startup-lifecycle.md)과 [품질 개선 기록](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/records/2026-09-17-02-network-consumer-quality-improvements.md)에 반영돼 있습니다.
