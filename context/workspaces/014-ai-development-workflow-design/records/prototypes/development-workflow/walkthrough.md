# 로그인 완료 표현을 정리하는 한 작업

`loginAndRefresh`가 돌아왔을 때 인증만 끝났는지, 화면 데이터까지 준비됐는지를 호출자가 구별할 수 있게 만드는 예제다. 설명용 시작 조건을 바탕으로 새 실행 코드를 작성한 뒤, 그 코드에서 이름 유지와 개명을 비교한다. 실제 Noline의 이전 코드를 개명한 작업은 아니다.

## 완료 뒤에 누가 무엇을 하는가

[시작 입력](noline-demo/context/work/workspaces/001-login-completion-names/source/scenario-input.md)의 wrapper는 인증 서비스를 기다리고 조회 갱신을 요청한 뒤, 조회 결과를 기다리지 않고 `onCompleted`를 호출한다. Login은 이동하고 Reauth는 닫힌다. 두 소비자는 callback 안에서 최신 조회 값을 읽지 않는다. 외부에 공개된 API는 없고 내부 사용처 두 곳을 함께 변경할 수 있다고 가정한다.

이번 Work는 인증 적용 뒤의 비대기 완료, Promise로 전달되는 후속 조회 실패의 분리, 화면별 후속 행동을 새 실행 코드에서도 제공한다. 조회 요청 자체가 즉시 던지는 오류도 후속 실패로 분리하는 처리는 실행 예제를 만들면서 추가했다. 아래 이름 A/B는 이 추가 처리를 포함한 **현재의 같은 코드**를 비교하며, 시작 입력과 실제 제품의 동작이 모두 보존됐다는 검증은 아니다.

이때 Login의 ‘로그인과 화면 갱신 완료’ 안내는 실제 보장보다 넓다. 함수명은 그대로 둘 수도 있지만 이 안내는 어느 안에서도 ‘로그인 완료’로 바로잡아야 한다. 조회를 기다리는 동작을 새로 넣으면 이동·닫기 시점까지 달라진다.

## 판단 기준과 제품 계약을 함께 읽는다

| 필요한 판단 | 사용하는 본문 | 이번 작업에 가져오는 내용 |
| --- | --- | --- |
| 표현과 동작 중 무엇을 고칠지 | [Personal 이름·완료 기준](noline-demo/context/personal/development/naming-and-completion/index.md) | 소비자가 필요한 결과와 실제 보장을 대조한다. 가능한 한 코드 자체에서 의미를 읽을 수 있게 하고, 설명·개명·구성·동작 수정 중 필요한 조치를 고른다. |
| 인증 완료가 보장하는 상태 | [Project 인증 계약](noline-demo/context/project/guidance/authentication-and-session/index.md) | 기기 저장과 상태 적용은 완료한다. 후속 조회의 실패는 인증 저장 실패와 구별한다. |
| 이 제품에서 피해야 할 완료 표현 | [Project 가독성 가이드](noline-demo/context/project/guidance/code-readability/index.md) | 인증 적용·조회 요청·조회 결과·화면 준비를 섞지 않는다. |
| 이번 구현의 범위 | [Work Ticket](noline-demo/context/work/workspaces/001-login-completion-names/current/memory/tickets/01-authentication-completion.md) | 인증 적용 뒤 조회를 요청하고 기다리지 않는 완료 경계를 새 실행 예제로 구현한다. 두 소비자의 이동·닫기를 유지하며 이름과 완료 표현을 비교한다. |

Personal이 비교할 관점을 제공하고 Project가 제품의 약속을 정한다. Work는 이 둘을 현재 사용처에 대입해 선택한다. [개발 절차](noline-demo/context/work/DEVELOPMENT.md)는 입력 선택·전달·검토·갱신을 연결한다. 이 해설은 현재 문서를 이용한 설명이며 최초 전달 판본을 그대로 재현한 실험은 아니다.

## 같은 코드에 두 표현을 대입한다

| 이름 유지 + 설명 | 개명 + 같은 설명 |
| --- | --- |
| `loginAndRefresh` · `onCompleted` | `signInAndRequestRefresh` · `onSignedIn` |
| 가까운 설명을 읽으면 사용할 수 있지만 완료 범위를 설명에 의존한다. | 이름에서도 조회 요청과 인증 완료를 구별한다. 이 이름만으로 드러나지 않는 의미는 다른 코드의 타입·흐름과 별도 설명의 역할을 나눠 본다. |
| 참조를 바꾸지 않는다. | 내부 두 사용처의 참조를 함께 바꾼다. |

[전체 A/B 코드](noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-06-naming-alternatives.md)에서는 같은 주석·처리 순서·오류 전달·반환·사용자 안내를 두고 함수명과 callback명만 바꿨다. [비교 화면](viewer.html#naming)에서 나란히 볼 수 있다.

현재 예제는 가능한 한 설명 없이 코드에서 완료 의미를 읽게 하는 방향으로 개명안을 선택했다. 유지안을 사용할 수 있다는 것과 같은 수준의 명료함을 권한다는 것은 다르다. 공개 API 호환성이나 실제 변경 위험이 크면 이름을 유지하는 절충이 필요할 수 있다. 현재 비교는 이름 변경만 다루므로 타입·책임·제어 흐름까지 최선으로 구성했다고 확정하지 않는다.

최신 조회 결과를 바로 사용해야 하는 소비자가 생기면 이 선택을 그대로 반복하지 않는다. 해당 소비자만 기다릴지 공통 완료 계약을 바꿀지 판단해야 한다. 두 기존 소비자가 조회 결과를 필요로 하지 않는 현재 조건에서는 대기를 추가하지 않는다.

## 선택이 코드와 검사에 이어지는 지점

[인증 코드](noline-demo/examples/authentication/src/authentication.mjs)는 인증 적용을 기다리고 후속 조회 요청을 시도한 뒤 인증 완료를 통지한다. 조회 요청의 즉시 오류와 나중의 Promise 거부는 후속 오류로 전달한다. 즉시 오류의 분리는 실행 예제에서 추가한 처리이며 시작 입력에 이미 있었다고 가정하지 않는다.

[두 소비자](noline-demo/examples/authentication/src/consumers.mjs)는 Login의 이동과 Reauth의 닫기를 각각 소유한다. [동작 검사](noline-demo/examples/authentication/tests/authentication.test.mjs)는 저장 전 상태 보존, 조회가 미완료인 때의 인증 완료, 인증 실패와 후속 조회 실패의 분리를 확인한다. 메모리 기반 어댑터의 검사이며 실제 화면·DB·서버 통합을 확인하지는 않는다.

실제 수행한 실행과 초기 검토는 [Work 기록](noline-demo/context/work/workspaces/001-login-completion-names/records/README.md)에 있다. 선택·코드가 존재하는 것, 검사한 경계, 실제품 통합과 사용자 수락을 구별한다.

## 다음 변경은 달라진 내용을 소유한 곳에 남긴다

새 소비자가 최신 결과를 필요로 하면 Project의 완료 계약과 해당 Work의 요구를 함께 판단한다. 코드 연결만 바뀌면 [Project current](noline-demo/context/project/current/authentication-flow/index.md)를 맞춘다. 이번 선택과 확인·미확인은 [Work 상태](noline-demo/context/work/workspaces/001-login-completion-names/current/state/index.md)에 남기고, 결과 파일은 [output](noline-demo/context/work/workspaces/001-login-completion-names/output/index.md)에서 찾는다.

‘가능한 한 설명 없이 이해되는 코드’처럼 여러 작업에 가져갈 개인 판단은 Personal에서 관리한다. 그 기준이 바뀌면 이번 A/B 선택의 이유도 Work에서 다시 살핀다. 인증 완료의 보장이나 프로젝트의 공통 개발 규약이 달라진 것이 아니라면 Project 가이드를 함께 바꿀 필요는 없다. 이번 함수명을 새 공통 명명 규칙으로 등록하거나 모든 인증 작업에 조회 비대기를 강제하지 않는다.
