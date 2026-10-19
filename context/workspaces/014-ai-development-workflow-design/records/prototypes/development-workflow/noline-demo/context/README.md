# Noline demo context

이 context는 개인이 가져오는 판단 기준, 제품이 계속 지킬 의미, 한 작업의 현재 상태를 구별해 제공한다. 이번에는 **로그인 함수·완료 알림이 인증 완료와 조회 갱신 완료를 혼동시키지 않게 하는 작업**에 적용한다.

| 필요한 것 | 시작점 | 담당하는 내용 |
| --- | --- | --- |
| 개인의 개발 판단 | [personal](personal/README.md) | 목적·사용처·비용에 따른 판단, 이름과 실제 책임·완료 범위, 판단을 다시 볼 사례·대화 |
| Noline demo의 제품 맥락 | [project](project/README.md) | 기기 세션의 의미, 인증 적용·조회 후속 실패 계약, 현재 예제의 구현 경계 |
| 이번 작업을 이어 가기 | [work](work/README.md) | 작업의 Spec·Ticket·현재 상태와 입력·결과·기록 |

Personal과 Project는 자기 내용만으로 담당 의미를 설명한다. 어느 개인 기준과 제품 계약을 이번 작업에 함께 적용할지는 Work의 [개발 절차](work/DEVELOPMENT.md)가 선택한다. Project가 개인 기준의 채택 목록을 관리하거나 개인 원문을 알아야 제품 계약을 이해할 수 있게 만들지 않는다.

현재 작업은 [001 로그인 완료 표현](work/workspaces/001-login-completion-names/README.md)이다. 같은 프로젝트에서 다른 작업을 시작하면 별도 Workspace가 그 목표와 상태를 맡으며, 이번 작업의 함수명 선택을 다른 작업의 고정 규칙으로 올리지 않는다.

Project·Work의 책임과 계층은 실제 Noline에서 확인한 구조를 따른다. Personal은 사용자가 이번 설계에서 context 아래에 두도록 정한 추가 층이다. 운영 Harness·자동 hook은 이 demo에 연결하지 않았다. 문서와 코드가 갱신되면 각 Owner를 직접 맞춘다.
