# Noline demo Project context

이 층은 여러 작업에서 함께 사용할 **제품 의미·개발 계약·현재 구현 범위**를 소유한다. 현재 다루는 주제는 기기 인증을 복구하고 기존 로컬 작업을 이어 가는 인증 흐름이다. 한 작업의 목표·대안·진행·검사는 Work가 소유한다.

## 작업에서 필요한 본문

| 지금 필요한 판단 | 담당 본문 |
| --- | --- |
| 같은 계정으로 다시 로그인할 때 무엇을 보존하는가 | [기기 세션과 작업 연속성](common/device-session.md) |
| 언제 인증이 끝나며 후속 조회 실패를 어떻게 처리하는가 | [인증·세션 계약](guidance/authentication-and-session.md) |
| 함수·callback·안내가 같은 결과를 표현하는가 | [인증 코드의 가독성](guidance/code-readability.md) |
| 현재 구현과 검사가 어느 범위까지 이어지는가 | [현재 인증 흐름](current/authentication-flow.md) |

제품 의미는 [common](common/README.md), 구현·지원 현실은 [current](current/README.md), 관련 작업의 계약과 판단은 [guidance](guidance/README.md)가 맡는다. 세 층을 매번 순서대로 모두 읽지 않고 지금 질문에 맞게 고른다. 중요한 제품 선택의 근거는 [decisions](decisions/README.md)에서 찾는다.

## 구성과 관리

실제 Noline의 `context/project/` 구조를 따라 README, MAINTENANCE, REFERENCE와 common/current/guidance/decisions를 둔다. 이 demo에는 인증 관련 본문만 채웠다. 실제 Noline의 통화·날짜·API·동기화 전체가 들어 있다고 보지 않는다.

내용을 읽고 적용하는 기준은 [REFERENCE/reading.md](REFERENCE/reading.md), 본문을 나누고 구성하는 기준은 [REFERENCE/composition.md](REFERENCE/composition.md), 갱신 시점·권한·완료 확인은 [MAINTENANCE.md](MAINTENANCE.md)가 소유한다. 이 관리 문서들을 일반 인증 작업마다 기본 입력으로 붙이지 않는다.

이 Project 본문은 Noline의 보존된 제품 자료에서 가져온 계약과 이번 실행 예제에 맞춘 조건을 구별해 설명한다. 실제 제품 정본은 아니며 구현 사실은 [예제 코드](../../examples/authentication/README.md)에서 대조한다. 제품 계약의 변경과 현재 구현의 사실 정정은 다른 판단이다.

특정 Work의 함수명 선택과 대안·실행 이력은 [로그인 완료 표현 Work](../work/workspaces/001-login-completion-names/README.md)에 남긴다. 한 번의 선택을 제품 전체 의무로 자동 승격하지 않는다.
