# Workspaces

하나의 Workspace는 하나의 작업 목표와 그 작업을 이어 갈 상태를 소유한다. 다른 Workspace의 current를 이어 읽어야만 이해할 수 있는 구조로 만들지 않는다. 이 목록은 작업의 위치와 일반 재개의 기본 선택을 소유하고, 각 Workspace는 자기 현재 의미와 상태를 소유한다.

## 기본 선택과 작업 목록

**일반 재개의 기본 선택: [001-login-completion-names](001-login-completion-names/README.md).** 사용자 지정 Work가 우선하며, 특정 Work를 읽거나 수행하라는 요청만으로 이 기본 선택을 바꾸지 않는다. root·context·Work의 일반 재개는 여기의 선택을 따른다.

| Workspace | 맡은 목표 |
| --- | --- |
| [001-login-completion-names](001-login-completion-names/README.md) | 로그인 완료의 표현과 실행 경계. 실제 결과·미확인은 해당 Work에서 확인한다. |

같은 목표의 재개는 [Work 지침](../AGENTS.md)을 따른다. 독립 목표 생성이나 지속 전환이 요청되면 [생성과 전환 계약](CREATE-AND-TRANSITION.md)을 사용한다. 생성만 마친 Work는 목록에 연결하되 위 기본 선택은 유지한다. 이 목록의 선택은 수동 재개 기준이며 host binding을 만들지 않는다.

## Workspace 내부의 책임

| 위치 | 책임 |
| --- | --- |
| `README.md` | 작업의 정체성과 구성, `recover.md`로 이어지는 진입 |
| `recover.md` | 현재 재개의 초점과 기본·조건부 읽기 대상, 선택 이유와 필요한 절·구간 |
| `current/memory/` | Work의 Spec 다섯 관점, Ticket 색인·본문, 선택한 Project·Personal 맥락 |
| `current/state/` | Workspace 전체 상황과 다음 행동 |
| `source/` | 이번 작업에 선택한 원자료·초기 입력과 provenance |
| `output/` | 현재 결과로 선택한 실제 코드·문서·검사의 위치. 복제본을 만들지 않는다. |
| `records/` | 선택 이유·작성·검사·검토의 지속 이력 |

사람용 문서를 쓰거나 고칠 때는 [문서 작성과 갱신](DOCUMENT-WRITING.md)을 적용한다. 기존 날짜별 record와 raw source는 보존하며 후속 보완은 새 record와 색인에 연결한다.

Spec·Ticket 관계는 [작성·갱신 기준](spec-and-tickets/README.md)이, 실제 본문은 각 Workspace가 소유한다. Source의 입력과 records의 판단을 구별하며, 기록에 있다는 이유로 현재 요구가 되지는 않는다.

`recover.md`의 작성·읽기·갱신 기준은 [Work 지침](../AGENTS.md#재개-안내를-구성하고-갱신한다)이 소유한다. 현재 의미는 current에서, 상세 과정은 records에서 유지하며 안내에 별도 상태 정본을 만들지 않는다.

이 demo는 사람용 재개 안내와 직접 검사를 사용하며 machine identity·검증 상태 JSON을 생성하지 않는다. 기존 Harness 계약과 과거 receipt가 있는 다른 대상에서는 실제 소비 경로와 증거 접근을 보존하며 전환해야 한다. 이 prototype의 문서 적용만으로 해당 대상의 실행기가 아카이빙된 것은 아니다.
