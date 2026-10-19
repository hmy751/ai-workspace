# 인증 흐름의 현재 연결 — 예시 작업 후

> 가상 작업을 마친 시점의 Project 현황이다. 실제 Noline 코드·테스트를 대조한 결과가 아니다. 작업 전 이름과 동작은 [시작 입력](../../../../scenario-input.md)에 별도로 고정했다. 아래 최종 이름을 처음 구현자에게 이미 제공한 것으로 읽지 않는다.

## 현재 책임과 사용처

| 단위 | 이 예시에서 맡는 일 |
| --- | --- |
| `loginService.signIn` | 전체 세션 변경 서비스를 거쳐 진행 중 작업을 조율하고 계정·DB·queue 확인, 기기 저장, `signed-in` 적용을 마친다. Query 갱신은 이 함수에 들어 있지 않다. |
| `signInAndRequestRefresh` | 위 서비스를 기다린 뒤 Query 무효화를 요청하고 재조회를 기다리지 않은 채 `onSignedIn`을 부른다. |
| `LoginScreen` | `onSignedIn`에서 기존 화면으로 이동한다. 사용자에게는 ‘로그인 완료’라고 알리고 조회·화면 갱신까지 끝났다고 표현하지 않는다. `onRefreshError`에서 후속 조회 실패를 처리한다. |
| `ReauthDialog` | `onSignedIn`에서 재인증 모달을 닫는다. `onRefreshError`에서 후속 조회 실패를 처리한다. |

이 작업에서 wrapper와 callback의 이름·연결, LoginScreen의 과장된 완료 문구를 고쳤다고 가정한다. 위 두 내부 사용처의 화면 정책, 로그인·Query 대기 순서와 실패 분류는 유지했다. wrapper의 반환은 재조회 결과나 화면 반영 완료를 보장하지 않는다.

## 바뀐 표현과 유지한 계약

초기 이름 `loginAndRefresh`와 `onCompleted`를 각각 `signInAndRequestRefresh`, `onSignedIn`으로 바꿨다. 현재 이 예시에 그 외 공개 소비자는 없다. LoginScreen과 ReauthDialog 모두 같은 새 callback 키를 사용하는 것으로 연결했다.

Query는 무효화 요청 후 별도로 진행된다. Query 실패는 해당 Promise의 rejection으로 전달되고 `onRefreshError`가 처리하며 다시 던지지 않는다고 가정한다. `void` 자체가 오류를 처리하는 것은 아니다. 완료 callback도 정상 반환한다고 놓았다. 실제 제품으로 적용할 때는 라이브러리 설정·반환형·실패 전달과 화면별 처리를 확인해야 한다.

인증의 성공·실패와 후속 갱신을 구별하는 이유는 [인증 가이드](../guidance/authentication-and-session.md), 이름 선택의 기준은 [가독성 가이드](../guidance/code-readability.md)에 있다. 이번 작업 하나의 수정 과정은 이 현황에 누적하지 않는다.

## 증거 범위와 다시 볼 변화

위 내용은 설명용 코드 발췌와 가정한 사용처에 따른 최종 연결이다. 실제 제품 검사·화면 조작·OAuth·기기 저장소 확인은 하지 않았다. [구현 기록](../../work/workspaces/login-completion-names/records/implementation.md)과 [검토 기록](../../work/workspaces/login-completion-names/records/review.md)은 시안 속 판단과 예상 확인을 구별해 보존한다.

호출자가 늘거나 wrapper의 대기·오류·callback 시점을 바꾸면 변경 책임자가 이 관계와 인증 계약을 함께 대조한다. 이후 실제 코드가 생기면 여기의 가정을 그 코드·검사와 확인 범위로 대체해야 한다.
