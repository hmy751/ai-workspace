# 인증 완료 경계의 실행 예제

메모리 저장 뒤 인증 상태를 적용하고 Query 갱신을 요청하는 작은 Node.js 예제다. 실제 Noline 앱의 디렉터리나 제품 코드를 대체하지 않으며, context에서 설명하는 완료·실패 경계를 실행으로 대조하는 역할을 맡는다.

- [기기 세션 저장과 상태 적용](src/device-session.mjs)
- [인증 서비스와 조회 요청 wrapper](src/authentication.mjs)
- [Login·Reauth 소비자](src/consumers.mjs)
- [정상·실패 실행 장면](src/demo.mjs)
- [완료·실패 경계 검사](tests/authentication.test.mjs)

실행 기준 디렉터리와 명령은 [프로젝트 README](../../README.md#직접-실행한다)에 있다. 제품 계약은 [인증 가이드](../../context/project/guidance/authentication-and-session/index.md)가, 이 예제를 결과로 선택한 이유와 검사는 [Work](../../context/work/workspaces/001-login-completion-names/README.md)가 맡는다.
