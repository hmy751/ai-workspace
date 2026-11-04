# Default timeout 작업 재개

현재 제품의 timeout 계약과 확인 범위를 이어받는 안내다. 구현 변경인지 당시 선택·검증 설명인지 먼저 구별하고, 현재 결과와 다음 판단은 아래 state에서 확인한다. 이 파일은 상세 상태나 검사 결과의 두 번째 정본이 아니다.

## 기본 읽기

| 자료 | 읽는 이유와 범위 |
| --- | --- |
| [문제·목표·범위](current/memory/spec/01-problem-goal-scope.md) | 누락된 timeout의 기본값과 포함·제외한 작업을 이해한다. |
| [현재 상태](current/state/index.md) | 지금 확인된 결과·한계와 다음 판단을 이어받는다. 과거 Verify 성공을 현재 수락으로 읽지 않는다. |
| [산출물 지도](output/index.md) | 실제 구현·검사의 위치를 찾는다. 연결된 전체 본문을 항상 읽지는 않는다. |

## 요청에 따라 추가로 읽기

| 요청·판단 | 자료와 필요한 범위 |
| --- | --- |
| 기본값·거부 입력·반환값을 설명하거나 수정한다 | [Project 맥락 선택](current/memory/project-context.md)의 해당 기준·결정·현재 구조. [요구 동작](current/memory/spec/02-behavior-and-cases.md)과 [입출력 계약](current/memory/spec/03-concepts-and-contracts.md)을 실제 코드와 대조한다. |
| 왜 `5000`인지, 현재 구현 방식을 유지할지 판단한다 | Project 선택 문서의 default-timeout 결정과 [제약·설계·가정](current/memory/spec/05-constraints-design-assumptions.md). 개인 취향과 제품의 채택 계약을 구별한다. |
| 구현·검사를 수행하거나 완료를 판단한다 | [품질·완료 기준](current/memory/spec/04-quality-and-completion.md), [Ticket 색인](current/memory/tickets/index.md)의 해당 실행과 [제품 검사 안내](../../../../README.md#직접-실행한다). 실행 조건·대상·결과와 미확인을 남긴다. |
| 앞선 검증을 다시 근거로 사용한다 | [기록 색인](records/README.md)에서 해당 실행·receipt를 선택한다. 당시 claim·입력·판본·결과와 지금의 코드·기준을 대조하며 옛 hash나 성공만으로 현재 효과를 추정하지 않는다. |
| 재개 방식·기계 상태가 바뀐 이유를 확인한다 | [전환 기록](records/2026-11-04-recovery-guide-transition.md). 이전 구현 자체를 재검토할 때만 archive를 연다. |
| 입력 원문을 다시 대조한다 | [source inventory](source/index.md)의 실제 선택과 출처를 확인한다. 다른 Workspace 전체를 기본 입력에 더하지 않는다. |

맡은 범위의 목표·이유·조건·확정과 미정·다음 행동이 설명되면 과업으로 돌아간다. 공백이 있으면 [Work 재개 기준](../../AGENTS.md#요청에-맞춰-재개한다)에 따라 필요한 본문·원문을 더 읽는다.
