# Workspaces

하나의 Workspace는 하나의 작업 목표와 그 작업을 이어 갈 상태를 소유한다. 현재 적용 예시는 [001-login-completion-names](001-login-completion-names/README.md)다. 다른 Workspace의 current를 이어 읽어야만 이해할 수 있는 구조로 만들지 않는다.

| 위치 | 책임 |
| --- | --- |
| `README.md` | 작업의 정체성과 읽을 경로 |
| `current/memory/` | Work의 Spec 다섯 관점, Ticket 색인·본문, 선택한 Project·Personal 맥락 |
| `current/state/` | Workspace 전체 상황과 다음 행동 |
| `source/` | 이번 작업에 선택한 원자료·초기 입력과 provenance |
| `output/` | 현재 결과로 선택한 실제 코드·문서·검사의 위치. 복제본을 만들지 않는다. |
| `records/` | 선택 이유·작성·검사·검토의 지속 이력 |

Spec·Ticket 관계는 [작성·갱신 기준](spec-and-tickets/README.md)이, 실제 본문은 각 Workspace가 소유한다. Source의 입력과 records의 판단을 구별하며, 기록에 있다는 이유로 현재 요구가 되지는 않는다.

실제 Noline의 `workspace.json`, `recover.json`, `verify.json`, `current/state/status.json`은 설치된 Harness의 identity·선택·검증·결과 계약이다. 이 demo에서는 자동 실행을 연결하지 않았으므로 같은 이름의 임의 schema나 가짜 검증 상태를 만들지 않았다. 사람용 재진입은 각 Workspace README와 current에서 성립한다.
