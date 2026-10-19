# 로그인 완료 표현을 정리하는 한 작업

**문서만 따로 읽는 대신, 한 작업이 어떤 입력·선택·구현·기록으로 이어지는지 따라간다.** 초기 문제와 두 소비자는 이 프로토타입에 부여한 가정이다. 현재 파일과 실행 가능한 데모 코드는 실제로 작성했으며, 수행한 확인은 [Work 상태](noline-demo/context/work/workspaces/001-login-completion-names/current/state/index.md)에서 구별한다. 아래 예시 의뢰를 실제 사용자의 제품 수정 요청으로 취급하지 않는다.

## 1. 맡은 문제와 보존할 동작

예시 의뢰:

> `loginAndRefresh`와 완료 callback을 보면 화면 데이터까지 다 바뀐 것처럼 읽힌다. 실제로 보장하는 책임과 완료 범위에 맞게 이름과 완료 표현을 정리한다. 실행 순서, 실패 처리, 화면별 이동 정책은 유지한다.

[초기 입력](noline-demo/context/work/workspaces/001-login-completion-names/source/scenario-input.md)의 wrapper는 인증 서비스를 기다리고, 조회 갱신을 요청한 뒤 조회 완료를 기다리지 않고 `onCompleted`를 부른다. 내부 소비자는 LoginScreen과 ReauthDialog 두 곳이며, LoginScreen에는 `로그인과 화면 갱신 완료`라는 문구가 있다. 외부에 공개한 API는 없다고 가정한다.

이 초기 코드는 실제 Noline의 과거 버전이 아니다. [이번 Ticket](noline-demo/context/work/workspaces/001-login-completion-names/current/memory/tickets/01-authentication-completion.md)은 이 예시에서 고칠 표현과 보존할 동작을 고정한다.

## 2. 판단에 필요했던 입력과 현재 읽기 경로를 구별한다

[Noline 진입 안내](noline-demo/AGENTS.md)에서 같은 프로젝트의 [context 입구](noline-demo/context/README.md)로 들어간다. Main은 Work의 [개발 절차](noline-demo/context/work/DEVELOPMENT.md)에 따라 personal·project를 따로 선택한다. 선택한 제품 계약과 개인 주제는 Work의 current/memory에, 목표는 Spec에, 실행 범위는 Ticket에 남는다.

아래는 보존된 시나리오와 당시 선택 기록을 바탕으로 **초기 판단에 필요했던 사실을 재구성한 해설**이다. 당시 전달 문장의 그대로인 복원본이나 새 작업자에게 시행한 재실험이 아니다. 현재 문서에는 그 뒤 보완된 설명도 있으므로, 지금의 링크를 최초 입력과 동일하게 취급하지 않는다.

> 초기 wrapper는 인증 서비스를 기다린 뒤 조회 요청을 시도하고, 조회 완료를 기다리지 않고 callback을 호출한다. LoginScreen은 이동하고 ReauthDialog는 닫힌다. 두 callback은 최신 조회 값을 소비하지 않는다. 이번 요구는 이 시점과 화면별 후속 행동을 보존하면서, 이름과 문구가 보장 이상의 완료를 암시하지 않게 하는 것이다. 두 소비자는 내부 코드이고 공개 API 호환 요구는 없다. 기기 저장·인증 적용과 후속 조회 실패는 구별한다. 최종 함수명과 callback명은 아직 주지 않고, 유지·설명 보완·개명 중 선택할 근거를 비교한다.

이 재구성의 실패 보존 범위는 초기 가정에 적힌 Promise 거부다. 조회 요청 자체의 동기 오류를 후속 실패로 분리한 처리는 실행 가능한 데모를 만들 때 추가했다. 과거부터 모든 실패 처리가 같았다고 주장하지 않는다.

| 현재 찾아 읽는 본문 | 판단에 쓰는 내용과 지위 |
| --- | --- |
| [개인 개발 공통](noline-demo/context/personal/development/README.md) | 기준을 채택했더라도 목적·사용처·비용으로 적용한다. 예시와 코드 모양이 다르다는 이유만으로 고치지 않는다. |
| [이름·책임·완료 일반 기준](noline-demo/context/personal/development/naming-and-completion.md) | 호출자가 기대하는 결과와 실제 보장을 대조한다. 개명·가까운 설명·동작 수정 중 무엇이 필요한지 비교한다. 사례별 조건이 필요하면 별도 사례 파일의 해당 절로 내려간다. |
| [Project 인증 계약](noline-demo/context/project/guidance/authentication-and-session.md) | 기기 저장과 상태 적용, 후속 조회, 인증 실패와 후속 실패를 구별한다. |
| [Project 가독성 가이드](noline-demo/context/project/guidance/code-readability.md) | 이 제품에서 이름·완료 알림·사용자 문구가 어떤 보장을 표현해야 하는지 확인한다. |
| [이번 Work](noline-demo/context/work/workspaces/001-login-completion-names/README.md) | source는 부여한 시작 상황, current와 records는 선택·구현·검사의 현재 설명과 이력이다. 선택 후 이름과 결과를 초기 판단 조건에 섞지 않는다. |

일반 기준의 판단 차이를 더 볼 때 [상세 사례](noline-demo/context/personal/development/cases/naming-and-completion.md)를 선택하고, 당시 의미·채택 범위를 재판단할 때 그 사례의 원기록으로 내려간다. 원자료 전체를 매 작업마다 읽지 않는다. Project 본문에는 개인 기준 경로를 추가하지 않았으며, 이번 작업에서 무엇을 사용했는지는 Work에 남긴다.

새 작업자에게 처음부터 다시 적용시켜 보는 실험에서 입력 판본을 어떻게 고정·전달할지는 미정이다. 이 해설과 현재 화면은 그 실험의 성공 증거가 아니다.

## 3. 같은 계약 안에서 가능한 선택을 비교한다

Project가 정하는 완료의 의미는 인증 적용까지다. 조회 요청·조회 완료·화면 렌더 완료는 구별한다. 개인 기준은 그 의미를 전달할 수단과 변경 비용을 판단하게 한다. 따라서 특정 이름이 기준 파일에 있다는 이유로 바로 복사하지 않는다.

| 선택 | 이 예시에서의 판단 |
| --- | --- |
| 기존 이름 유지 + 가까운 설명 보완 | 호환 변경이 적고 가능한 선택이다. 다만 초기에는 계약 설명이 없고 이미 화면 갱신 완료로 읽히는 표현이 있어, 이번에는 이름에서도 차이를 드러낼 이득을 본다. |
| 개명 + 짧은 계약 설명 | 내부 두 사용처를 함께 바꿀 수 있고 공개 호환 계약이 없으므로 비용이 제한적이다. 이 프로토타입에서는 이 방향으로 구현한다. 이름만으로 모든 단계와 실패 조건을 나열하지 않는다. |
| 조회 완료를 기다리도록 변경 | 완료 알림·이동·닫기 시점을 늦춘다. 두 callback은 최신 결과를 소비하지 않고 이번 요구는 그 시점을 보존하므로 대기를 추가하지 않는다. 기다리더라도 조회 실패와 인증 실패는 분리할 수 있다. 최신 결과가 필요한 소비자가 생기면 그 소비자만 기다릴지 공통 완료 계약을 바꿀지 다시 판단한다. |

이 선택은 이번 작업의 조건에 따른 Main·구현자의 구체화다. 모든 Project에서 같은 이름을 쓰라는 사용자 결정으로 올리지 않는다. 널리 쓰이는 공개 API라면 설명 보완이나 전환 기간을 포함해 비용을 다시 비교한다.

## 4. 코드와 검사에서 완료 경계를 확인한다

[현재 데모 소스](noline-demo/examples/authentication/src/authentication.mjs)는 저장·상태 적용, 조회 요청, 완료 알림과 두 소비자의 처리를 읽을 수 있게 구성한다. 실제 저장소·서버 대신 이 경계를 확인할 수 있는 작은 구현과 의존성을 사용한다. 전체 앱·실제 UI를 재현하는 범위는 아니다.

[테스트](noline-demo/examples/authentication/tests/authentication.test.mjs)에서는 조회가 아직 끝나지 않은 때의 인증 완료, 인증 실패와 후속 조회 실패가 서로 다른 경로로 전달되는지를 대조한다. 테스트가 확인하는 정확한 항목과 이번 실행 결과는 [구현 기록](noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-02-implementation.md)에서 읽는다. 초기 가정 코드와 실제 제품의 회귀를 확인했다는 뜻은 아니다.

검토는 의뢰·선택한 개인 본문·Project 계약·현재 코드·검사 결과를 함께 받아 수행한다. 특정 결함이나 이름을 답으로 주입하지 않는다. 초기판에서 수행한 검토·발견·수정·한계는 [검토 기록](noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-04-review.md)에 남긴다. 과거 시안에서 검토자가 문구를 고쳤다고 가정한 대화를 이번 실행 기록으로 복사하지 않는다.

## 5. 결과를 담당 위치에 남긴다

| 남는 내용 | 실제 위치 |
| --- | --- |
| 제품의 현재 함수·완료·소비자 연결 | [Project current](noline-demo/context/project/current/authentication-flow.md). 현재 코드를 기준으로 설명한다. |
| 이번 입력·대안·선택·구현·검사·미확인 | [Work 상태와 기록](noline-demo/context/work/workspaces/001-login-completion-names/current/state/index.md). 단일 작업의 결과를 제품 정책이나 개인 공통 의무로 자동 추가하지 않는다. |
| 개인 판단의 뜻·조건·근거 | [Personal](noline-demo/context/personal/README.md). 이번 함수명을 새 공통 명명 규칙으로 등록하지 않는다. |
| 다음 작업자가 읽고 전달하는 절차 | [workflow](noline-demo/context/work/DEVELOPMENT.md). 기준 내용을 복제하지 않고 필요한 본문·담당·반환 경로를 유지한다. |

다음에는 새로운 날짜 폴더를 만들지 않고 이 프로토타입에서 필요한 책임의 본문·코드·장면을 고친다. 제품 작업이 새로 생기면 해당 Project 안에 별도 Work를 추가하고 현재 Project와 개인 기준은 자기 의미가 바뀔 때 갱신한다. 이 프로토타입을 설계하는 바깥 작업의 판단·변경 이유는 Workspace 014에 남긴다.


구조 정정 뒤에는 [Work의 source](noline-demo/context/work/workspaces/001-login-completion-names/source/index.md)에서 원래 입력을, [output](noline-demo/context/work/workspaces/001-login-completion-names/output/index.md)에서 실제 결과를 찾는다. Main이 직접 다시 확인한 경로와 실행 범위는 [후속 확인](noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-05-context-layout-check.md)에 있다. 과거 내용 검토 통과가 context 배치의 적절성까지 증명한 것으로 읽지 않는다.
