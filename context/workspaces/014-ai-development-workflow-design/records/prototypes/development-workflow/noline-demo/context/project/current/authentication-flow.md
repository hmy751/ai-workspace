# 현재 실행되는 인증 흐름

현재 이 폴더에서 실행할 수 있는 것은 메모리 기반 Node.js 예시다. 전체 세션 서비스의 경계를 두고 저장·상태 공개 뒤 Query를 요청하며 조회 완료를 기다리지 않고 인증 완료를 전달한다.

| 책임 | 현재 구현 | 끝날 때 보장하는 것 |
| --- | --- | --- |
| 계정 귀속·기기 저장·상태 공개 | [device-session.mjs](../../../examples/authentication/src/device-session.mjs)의 `applyAuthentication` | 이 예시의 계정·여행 목록 확인과 저장 후 공개 상태 반영 |
| 인증 응답과 진행 작업 대기 연결 | [authentication.mjs](../../../examples/authentication/src/authentication.mjs)의 `signIn` | 인증 응답, 주어진 대기 함수, Store 적용 완료 |
| 후속 Query와 인증 완료 전달 | 같은 파일의 `signInAndRequestRefresh` | Query 요청 시도 후 `onSignedIn` 호출. Query 오류는 `onRefreshError`로 전달 |
| Login | [consumers.mjs](../../../examples/authentication/src/consumers.mjs)의 `submitLogin` | ‘로그인 완료’ 안내와 이동 함수 호출 |
| Reauth | 같은 파일의 `submitReauthentication` | ‘인증을 복구했어요’ 안내와 닫기 함수 호출 |

조회 요청 시점에는 기기 저장값과 공개 세션이 이미 새 인증으로 바뀌어 있다. 조회 Promise가 계속 대기 중이어도 Login·Reauth의 인증 완료 처리는 진행한다. 소비자의 이동·닫기 함수 호출은 실제 화면 전환 완료를 뜻하지 않는다.

여기서 Query는 주입한 비동기 함수이며 실제 Query 라이브러리는 연결하지 않았다. 진행 작업 종료 역시 주입한 대기 함수만 실행한다. 제품의 DB·queue 귀속 검사와 조율, UI·네트워크·디스크 저장까지 확인한 상태가 아니다.

[동작 검사](../../../examples/authentication/tests/authentication.test.mjs)는 제어 가능한 대기로 저장 전 공개 여부, 저장 실패 보존, Query 비대기 완료와 후속 오류 분리를 확인한다. [이번 실행 기록](../../work/workspaces/001-login-completion-names/records/2026-10-19-03-execution.md)에 실제 실행 명령·결과·한계가 있다. 계약 의미는 [인증 가이드](../guidance/authentication-and-session.md)가 소유하고 이 문서는 현재 연결만 갱신한다.
