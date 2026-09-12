# Noline Spec·Ticket 실행 기준의 Reference 역반영

날짜: 2026-09-12
Noline source: `d7223b7b6622f625e26f7e7457f6eb1373cf91d9` (`feat(harness): Spec·Ticket 실행 기준 강화`)
Reference preimage: `af42b5ba2a858e1b5492e057b65851dc236ca964`

외부 Noline 저장소가 없어져도 이 판단을 재검토할 수 있도록, 실제로 의존한 최소 원문·원출처 blob·후보 판본·fresh-Main 검토 결과는 Reference 폴더의 [내부 근거 snapshot](../../../../reference-project/context/work/workspaces/spec-and-tickets/2026-09-12-NOLINE-EVIDENCE.md)에 함께 보존한다. 위 commit은 provenance와 원본 대조점이며 유일한 근거 접근 경로가 아니다.

## 요청과 판단

사용자는 Noline의 지정 커밋을 면밀히 살펴 `spec-and-tickets` 관련 근거와 이유를 확인하고 이 source Project에 반영하도록 요청했다. Noline 커밋은 제품 코드 변경 하나가 아니라, `002-code-readability-refactoring`의 Ticket 실행이 작은 수정 목록을 마친 뒤 넓은 Spec의 개선 기대를 충분히 이어 가지 못한 사례에서 출발했다.

최초 Ticket 03 결과는 helper 추출과 상태 조립 중복 제거를 실제로 수행했지만 SQLite·Mapbox 처리, 실패 경계와 React 상태 연결은 다루지 않은 채 Ticket 범위를 완료했다고 보고했다. 사용자의 후속 정정 뒤에야 처리 흐름과 책임을 더 넓게 보았다. 기존 Spec에는 이미 넓은 품질 기대가 있었으므로 문제를 Spec 이름이나 Ticket 크기 자체로 보지 않고, Ticket 초안의 수정 방법을 결과의 상한으로 삼은 실행·완료 판단의 연결 문제로 보았다.

채택한 기준은 다음과 같다.

- 수정 내용이 명시된 작은 요청과, 기능 완성·문제 해결·전반 개선처럼 결과 달성을 맡긴 요청을 구별한다.
- 결과 달성을 맡기면 필요한 일을 찾는 책임도 포함하며, 분석 예시나 초안의 수정 목록을 검토 범위 전체로 취급하지 않는다.
- Ticket은 수정 방법보다 맡은 결과·필요한 범위·완료 근거를 먼저 정하고, 일부만 맡길 때 실제 제공 결과와 남은 책임을 드러낸다.
- 실행 중 확인한 근거로 잠정 접근과 파일 범위를 발전시키되, 조사 범위와 실제 변경 권한은 구별한다.
- 테스트 통과나 목록 소진이 맡은 결과를 입증하는지 대조하고, 미검토·미완료를 전체 완료로 바꾸지 않는다.

이 기준은 리팩토링 전용으로 두지 않았다. Noline에서 기능 완성, 결함 수정, 코드 개선, 오탈자 수정과 API 자체 납품 사례로 일반화한 후보를 원대화 없는 새 Main들이 계획하게 하고, 목표 해석·필요 작업 발견·국소 범위 준수·완료 근거 구별을 독립 검토했다. 확인 범위는 계획 수립이며 실제 구현과 반복 실행의 신뢰성을 보장하지 않는다.

## Reference에 반영한 범위

기존 단일 `SPEC-AND-TICKETS.md`의 부모 판본은 Reference와 Noline에서 같은 Git blob `66e82b290fe668df5effe4a485a78c96db524457`였다. 따라서 Noline 제품별 내용을 복사하지 않고 공통 계약의 후속 구조를 Reference에 적용했다.

- `reference-project/context/work/workspaces/spec-and-tickets/`를 만들고 진입, 실행 기준, Spec 작성, Ticket 작성, 갱신, 선택 이력을 책임별로 분리했다.
- 기존 `SPEC-AND-TICKETS.md`는 과거 링크를 새 canonical로 연결하는 안내만 남겼다.
- Reference root·Work·Workspace·skill 진입 링크와 sample Workspace 링크를 새 경로로 맞췄다.
- Maintain의 수동 role과 계약은 분리된 기준 전체를 적용하도록 바꾸고, 자동 Codex session은 `README.md`, `EXECUTION-CRITERIA.md`, `SPEC.md`, `TICKET.md`, `MAINTENANCE.md` 본문을 최초 grounding과 후속 판단에 함께 제공한다.
- 회귀 테스트와 공용 fixture는 단일 파일이 아니라 다섯 정본 디렉터리를 사용하도록 바꿨다.

Noline의 `002-code-readability-refactoring` Spec·Ticket·state·output·records, 제품 검증 계약과 receipt는 target 작업의 canonical이므로 Reference에 복제하지 않았다. Noline root의 `.claude/decisions`와 project-specific checker도 Reference의 다른 구조를 덮지 않았다.

다만 공통 기준의 선택 이유를 제품 저장소 링크에만 맡기지 않았다. Ticket 03의 최초 완료 판단과 사용자 정정, reviewer 지적, 일반화 후보의 판본 식별자와 계획 검토 결과는 [Reference 내부 근거 snapshot](../../../../reference-project/context/work/workspaces/spec-and-tickets/2026-09-12-NOLINE-EVIDENCE.md)으로 옮겼다. 제품 현재 상태는 복제하지 않으면서도 공통 판단은 Reference만으로 재검토할 수 있는 경계다.

문서 분리는 적용 시점과 책임이 다른 판단을 가까이 모으고 일반 진입점에서 전체 관계를 찾게 한다. 실행 의미는 Workspace canonical이 소유하고 Maintainer·Recover는 이를 소비하므로, adapter가 사라져도 기준은 남는다. `ai-system_instruction-clarity.md: 적용`, `ai-system_context-ownership-boundary.md: 적용`, `ai-system_responsibility-cohesion.md: 적용`, `ai-system_behavior-responsibility-allocation.md: 적용`, `ai-system_human-readable-structure.md: 적용`, `ai-system_harness-rippability.md: 적용`.

## 확인 결과와 한계

Reference root에서 다음을 확인했다.

- 첫 전체 `python3 -B -m unittest discover -s . -p 'test_*.py' -v`: 126개 중 125개 통과. Noline 기록에도 남아 있는 기존 descendant timeout timing 시험 한 건이 실패했다.
- 해당 timeout 시험 단독 재실행: 통과.
- 전체 동일 검사 재실행: 126개 통과.
- 명시적 `001-default-timeout` Recover와 active 기본 Recover: 모두 성공하며 같은 Workspace를 복구했다.
- Reference Markdown 57개 local link 검사: 깨진 링크 0개.
- 변경 diff whitespace 검사: 이상 없음.

이 검사는 문서 발견, Maintainer 입력, fixture와 기존 Harness 회귀를 확인한다. 새로운 실제 제품 Ticket을 이 기준으로 끝까지 구현했을 때의 품질, 실제 host Maintain의 semantic apply, Noline 제품 acceptance를 새로 증명하지 않는다. Noline 커밋에서 확인한 계획 검토의 입증 범위를 Reference의 실제 실행 효과로 확대하지 않는다.
