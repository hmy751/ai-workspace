# Context continuity maintenance state

마지막 갱신: `2026-08-17`

## 현재 문제

Maintain의 의미 계약, 축소된 Verify 책임, retrieval·runtime·processing cursor의 동작 경계까지 정했다. 이제 이 설계 계약을 실제 hook·event delivery·checkpoint·queue로 옮기기 전에 남은 기술 선택과 최소 protocol prototype 범위를 정해야 한다.

## 확정된 사실

- 약 30분·26분의 긴 작업은 Recover나 Verify wrapper 자체보다 반복 이식, 중복 제품 검증, 순차·반복 Maintain, review와 timing flake rerun이 합쳐진 결과다.
- Maintain은 단순 record append가 아니라 `README/current/output/records` 사이의 의미 판단과 재작성이라 분 단위 비용이 실제로 발생했다. 같은 사건을 Workspace 002와 004에 반복 서술한 것도 비용을 키웠다.
- Timing flake는 실제 synchronization 결함이지만 20~30분의 근본 원인은 아니다.
- 매 응답 종료 점검, durable 변화가 없을 때 no-write, 명확한 변화의 allowlist 자동 반영, ambiguity 즉시 보고를 사용자가 선택했다.
- Memory 파일 수 자체는 제한하지 않는다. 장기 기준은 늘어날 수 있고, 향후 index routing으로 필요한 memory만 선택해 읽는다. 이 구조는 아직 구현하지 않았다.
- Recover는 현재 문제 없음으로 유지한다.
- Verify는 제품 검증 주체가 아니라 이미 일어난 test·eval·수동 확인의 최소 증거를 선택적으로 보존하는 기록 보조로 낮추기로 했다. 현재 Reference 구현과 schema는 아직 바꾸지 않았다.
- Records는 평소 넓게 읽지 않고 index가 지정한 조건에서만 선택한다. 판단·결정·제약은 Workspace README/current, 구현·실행 사실은 실제 파일·Git·test가 외부 canonical이다.
- Delta는 durable 저장층이 아닌 response-end의 일시적 전달 입력이다. 같은 conversation task·Workspace·worktree에서는 Maintainer를 재사용하고 event를 직렬 처리한다.
- Maintainer 자기 restart·compaction, Workspace·worktree 전환, 대화 종료·handoff, cursor gap이나 Owner·routing 구조 변경 때 rebootstrap한다. Main compaction만으로는 자동 reset하지 않는다.
- No-change와 성공 write는 processing cursor를 전진시키고, 실패는 completed cursor를 전진시키지 않아 replay 가능하게 한다.
- Git 대조는 event의 관련 경로와 write target freshness에 한정하며, branch·HEAD·worktree 전환이나 모순 때만 확장한다.

## 현재 설계 커서

다음 단계는 확정된 의미 계약을 바꾸는 토론이 아니라 구현 전 기술 결정과 protocol prototype 설계다.

1. 사용자 대상 Main 응답 확정을 어떤 hook 또는 runtime signal이 event로 만들지 정한다.
2. Event envelope와 processing cursor의 최소 schema·저장 위치를 정한다.
3. 같은 Maintainer의 직렬 queue, duplicate·gap·out-of-order·failure replay와 locking 방식을 정한다.
4. Rebootstrap 조건을 runtime이 어떻게 감지하고 외부 canonical을 다시 읽을지 정한다.
5. No-change, updated, needs-decision, failed 흐름을 파일 write 없이 먼저 검증할 최소 prototype을 설계한다.

Verify evidence helper는 갱신 workflow가 지속할 검증 증거를 발견했을 때 선택적으로 호출하는 하위 기록 장치다. 매 event의 필수 단계나 별도 제품 검증 gate가 아니다.

## 바로 이어서 확인할 질문

먼저 현재 Codex 환경에서 사용자 대상 Main 응답 확정을 관찰할 수 있는 hook·event producer와, context 밖 runtime checkpoint를 둘 수 있는 실제 위치를 조사한다. 그 근거로 event·cursor 최소 schema와 no-write prototype 범위를 제안하되 아직 runtime을 구현하지 않는다.

## 이후 미결정점

- Response-end를 발행할 실제 hook·runtime integration point
- Event delivery와 processing cursor의 구체 저장 위치·schema
- 같은 Maintainer를 재사용하는 queue·locking·restart 방식
- Maintainer compaction, cursor gap과 Owner·routing 변경의 감지 방법
- 향후 `memory/` 폴더와 index routing의 Owner 분리·선택 read 규칙
- Main과 maintainer가 동시에 쓸 때 target revision 표현과 stale-write 방어
- Ambiguity·실패 보고 채널과 replay 이후 중복 보고 방지
- 축소 Verify evidence의 선택 조건, 보존 형식과 retention
- Descendant timeout timing flake의 synchronization 수정
- 개선 효과를 판단할 latency, stale-context 발견, handoff 성공 지표

## 다음 행동

Codex의 실제 hook·subagent 수명·background 실행 가능 지점을 읽기 전용으로 확인한 뒤, event envelope와 processing cursor의 최소 기술안 및 prototype 범위를 제시한다. Runtime, cursor file, queue와 memory folder migration은 아직 만들지 않는다.
