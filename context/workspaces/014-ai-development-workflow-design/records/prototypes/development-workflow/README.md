# 개발 판단을 코드와 한 작업에 적용하기

공통화할 범위, 신뢰할 계약, 이름과 완료 표현을 **코드와 사용 조건으로 판단하는 개발 프로토타입**이다. 개인의 일반 기준과 사례를 읽고, Noline 인증 예제에서 제품 계약과 함께 적용한 선택·코드·검사 결과를 확인할 수 있다.

[폴더와 본문 열기](viewer.html) · [이름 유지·개명 나란히 보기](viewer.html#naming) · [로그인 작업 따라가기](walkthrough.md)

## 지금 궁금한 것에서 시작한다

| 보고 싶은 것 | 시작점 | 여기서 이해할 차이 |
| --- | --- | --- |
| 공통으로 묶을 범위와 사용처에 남길 선택 | [공통 제공과 사용처 선택](noline-demo/context/personal/development/shared-boundaries/INDEX.md) · [코드 사례](noline-demo/context/personal/development/shared-boundaries/INDEX.cases.md) | Field의 배치·입력 교체, Container의 오류 표시, 같은 주문 API와 같은 구매 흐름의 차이 |
| 공통 오류와 시간·자원의 의미 | [계약과 수명](noline-demo/context/personal/development/contracts-and-lifetime/INDEX.md) · [코드 사례](noline-demo/context/personal/development/contracts-and-lifetime/INDEX.cases.md) | 파싱 실패·HTTP 상태, 옵션의 적용 순서, Toast의 3초가 시작되는 시점 |
| 이름을 유지할지, 바꿀지, 동작을 고칠지 | [이름과 완료](noline-demo/context/personal/development/naming-and-completion/INDEX.md) · [판단 사례](noline-demo/context/personal/development/naming-and-completion/INDEX.cases.md) | 같은 코드의 이름 유지·개명 비용과 이득, 설명만으로 해결할 수 없는 완료 요구 |
| 이름 기준이 왜 이렇게 만들어졌고 어떻게 고칠지 | [형성 자료 안내](noline-demo/context/personal/development/naming-and-completion/_background/README.md) | 현재 맥락, 당시 선택·정정 기록, 발화 근거를 질문에 따라 찾는 경로 |
| 체계 지침의 본체·진입과 상세 분할을 어떻게 구별할지 | [체계 지침의 역할과 구성](noline-demo/context/SYSTEM-GUIDANCE.md) | 일반 내용의 기준과 체계를 다루는 지침, 진입 본문·상세·형성 자료의 책임 |
| 기준을 실제 작업에서 어떻게 사용하는지 | [로그인 완료 표현을 정리하는 작업](walkthrough.md) | Personal의 판단 관점, Project의 계약, Work의 선택이 코드에 연결되는 과정 |
| 작업 정의가 충분한지, 무엇을 더 구체화할지 | [작업 논의 스킬](skills/work-discussion/SKILL.md) · [스킬 안내](skills/README.md) | 기존 정의와 보완 후보의 대조, 충분성 판단과 필요한 구체화에 맞춘 반환 |
| 실행 코드와 확인 범위 | [Noline demo](noline-demo/README.md) | 저장·인증 적용 뒤 조회를 요청하되 결과는 기다리지 않는 완료 경계 |

일반 기준은 다른 작업에도 적용할 판단과 조건을 설명한다. 사례는 그 기준으로 선택이 갈리는 코드를 보여 준다. 전체 사례를 순서대로 읽는 대신 이번 쟁점에 맞는 본문을 고른다.

## Personal·Project·Work가 맡는 내용

세 층은 [noline-demo/context](noline-demo/context/README.md) 아래에 있다. 서로의 본문을 복제하지 않고, 한 작업에서 필요한 내용을 함께 선택한다.

| 위치 | 소유하는 내용 | 이번 인증 예제에서의 역할 |
| --- | --- | --- |
| [Personal](noline-demo/context/personal/README.md) | 개인의 판단 기준·이유·조건과 사례 | 이름 유지·설명·개명·동작 수정 중 필요한 조치를 판단한다. |
| [Project](noline-demo/context/project/README.md) | 제품의 의미·개발 계약·현재 구현 | 인증 적용과 조회 완료를 구별하고 실패 때 보존할 상태를 정한다. |
| [Work](noline-demo/context/work/README.md) | 이번 요구·선택·상태·입력·결과·기록 | 내부 두 소비자의 완료 표현을 정리하고 코드와 확인 결과를 연결한다. |

Work의 [개발 절차](noline-demo/context/work/DEVELOPMENT.md)는 이 입력을 고르고 구현·검토·갱신으로 연결하는 방법을 설명한다. Project가 개인 기준의 채택 목록을 관리하지 않으며, 이번 Work에서 고른 함수명을 모든 작업의 규칙으로 올리지 않는다.

## 직접 확인할 수 있는 범위

[인증 예제](noline-demo/examples/authentication/README.md)는 Node.js로 실행하는 메모리 기반 코드다. Login은 완료 뒤 이동을, Reauth는 닫기를 시작하며 실제 화면은 구현하지 않았다. 서버·DB·실제 기기 저장소와 운영 Harness도 연결하지 않았다. 실행 방법은 [demo 안내](noline-demo/README.md#직접-실행한다), 결과와 남은 조건은 [Work 상태](noline-demo/context/work/workspaces/001-login-completion-names/current/state/index.md)에서 읽는다.

현재 선택된 인증 이름과 같은 동작의 유지 대안은 [두 코드 비교](noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-06-naming-alternatives.md)에 있다. 사례의 설명용 API나 조건부 권고를 제품에 이미 구현한 것으로 읽지 않는다. 역할 겸임·검토 생략 조건과 자동 스킬 연결은 아직 정하지 않은 운영 범위다.

본문과 실행 코드가 정본이며 `viewer.html`은 이를 담은 열람 화면이다. 수정한 뒤에는 [화면 생성 안내](viewer/README.md)에 따라 표시 내용을 갱신한다.
