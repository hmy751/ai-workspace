# Noline 인증 흐름을 적용한 개발 프로토타입

인증을 기기에 저장하고 공개 상태를 바꾼 뒤 조회 갱신을 요청하는 작은 실행 예시다. Login과 Reauth는 함수로 된 두 사용처이며 UI는 만들지 않았다. context는 Personal·Project·Work를 나란히 두며, 실행 코드는 examples/authentication에 있다. 이 폴더의 코드와 문서는 함께 발전시키는 대상이다.

[Workspace 목록](context/work/workspaces/README.md)에서 지정 대상과 일반 재개의 기본 선택을 찾는다. [로그인 예제 Work](context/work/workspaces/001-login-completion-names/README.md)는 이 코드의 목표·선택 근거·실제 검사 결과를 담는다. 제품 의미나 개발 계약은 [Project context](context/project/README.md)가 소유하며, 한 작업에서 다른 입력을 함께 고른 이유는 Work 기록에 남긴다. 읽기·지속 본문 반영·요청된 Work 생성은 [context 진입](context/README.md)에서 각 방법으로 연결한다.

## 직접 실행한다

외부 패키지를 설치하지 않고 Node.js로 실행한다. 이번 확인 환경은 Node.js 24.16.0이다. 아래 명령의 기준 디렉터리는 이 `noline-demo/`다.

```bash
node examples/authentication/src/demo.mjs
node examples/authentication/src/demo.mjs --refresh-fails
node --test examples/authentication/tests/*.test.mjs
```

정상 예시는 저장 완료, 공개 상태 확인, Query 요청, 로그인 완료 안내, 이동 요청, 후속 조회 완료를 차례로 출력한다. 실패 예시는 인증 완료 안내 이후 조회 오류를 별도로 처리하고 `signed-in`과 보존한 여행 데이터가 남는 모습을 출력한다. 비밀 인증 정보는 출력하지 않는다.

| 바꿀 대상 | 담당 파일 |
| --- | --- |
| 계정 귀속 확인·저장 뒤 공개 상태 적용 | [기기 세션 Store](examples/authentication/src/device-session.mjs) |
| 로그인 대기 경계·조회 요청·완료 전달 | [인증 서비스와 wrapper](examples/authentication/src/authentication.mjs) |
| Login의 이동과 Reauth의 닫기·안내 | [두 소비자](examples/authentication/src/consumers.mjs) |
| 사람이 실행하는 메모리 기반 장면 | [실행 예시](examples/authentication/src/demo.mjs) |
| 비동기 순서·상태 보존·실패 경계 확인 | [동작 검사](examples/authentication/tests/authentication.test.mjs) |

## 실행 결과의 범위

이번에 새로 쓴 메모리 기반 코드다. 실제 Noline의 서버·기기 저장소·Query 라이브러리·화면에 연결하지 않았다. `waitForActiveWork`는 진행 중 작업의 종료를 기다릴 연결점이고, 실제 sync·cleanup·DB 조율기는 구현하지 않았다. DB·queue의 모든 귀속 검사, 동시 로그인·로그아웃 경쟁, 저장 도중 부분 실패, 프로세스 재시작 후 복구도 이번 예시에 포함하지 않는다.

저장 어댑터는 성공할 때 새 세션을 저장하고 실패할 때 이전 저장값을 유지한다고 가정한다. 완료·오류 callback은 정상 반환하는 소비자 계약이다. 이 가정 안에서 확인한 결과와 제품에 연결하기 전에 남은 확인은 [실행 기록](context/work/workspaces/001-login-completion-names/records/2026-10-19-03-execution.md)에 있다.

기존 문서 시안은 이 예시의 설계 입력이다. 거기에 서술된 가상 구현자·검토자 활동은 이번 실행 이력이 아니다. 새 코드와 파일 배치의 지위는 [작성 판단](context/work/workspaces/001-login-completion-names/records/2026-10-19-02-implementation.md)에서 구별한다.
