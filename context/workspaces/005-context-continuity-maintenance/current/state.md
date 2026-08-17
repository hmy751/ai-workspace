# Context continuity maintenance state

마지막 갱신: `2026-08-17`

## 현재 문제

현재 outer `context_maintainer`는 의미 있는 변화 뒤 여러 Owner 문서를 넓게 다시 읽고 고치는 LLM 작업이라, 파일 쓰기나 Recover·Verify runtime보다 훨씬 오래 걸린다. 이를 매번 동기식 종료 gate로 붙이면 continuity를 지키려는 장치가 main과 사용자의 대화를 막는다. 반대로 maintenance를 늦추기만 하면 `current`가 stale해져 다음 Recover와 handoff가 잘못 출발할 수 있다.

## 확정된 사실

- 약 30분·26분의 긴 작업은 Recover나 Verify wrapper 자체보다 반복 이식, 중복 제품 검증, 순차·반복 Maintain, review와 timing flake rerun이 합쳐진 결과다.
- Durable Verify의 기록 동작은 짧을 수 있지만 실행하는 제품 argv가 길면 Verify 전체 시간은 길어진다. 따라서 wrapper 비용과 제품 test graph 비용을 구분해야 한다.
- Maintain은 단순 record append가 아니라 `README/current/output/records` 사이의 의미 판단과 재작성이라 분 단위 비용이 실제로 발생했다. 같은 사건을 Workspace 002와 004에 반복 서술한 것도 비용을 키웠다.
- Timing flake는 실제 synchronization 결함이지만 20~30분의 근본 원인은 아니다.
- 명확한 current state 변화는 background에서 직접 반영하는 방향을 사용자가 선택했다. Memory 자동 반영은 축적 방지 조건을 먼저 정해야 한다.

## 현재 설계 커서

Background maintainer가 후보를 다음처럼 분류하는 최소 모델을 검토 중이다.

1. 일시적 대화·명령 출력: durable write 없음
2. 명확한 현재 상태 변화: `current/state` 직접 갱신
3. 명시적이고 장기적인 사용자 결정: memory 승격 조건을 통과할 때 기존 항목을 교체·압축
4. 재사용할 결정·실패·검증 사건: 자연스러운 경계에서 하나의 record로 집계
5. 의미나 권한이 애매한 후보: 보류 후 보고

이 분류는 제안이며 구현 계약으로 채택되지 않았다.

## 바로 이어서 확인할 질문

애매한 후보의 보고 cadence를 다음처럼 둘지 사용자에게 확인한다.

- 지금 작업 방향이 틀릴 위험이 있을 때만 즉시 보고한다.
- 그 밖의 애매한 후보는 대화 종료, handoff, commit 전처럼 자연스러운 경계에서 한 번에 묶는다.
- 자동으로 반영한 명확한 변경도 같은 경계에서 짧게 요약한다.

## 이후 미결정점

- `current/state`, `memory`, records, output 중 background direct-write allowlist
- Memory 승격의 장기성·명시성·중복·Owner·길이 조건과 replace/delete 규칙
- Main과 maintainer가 동시에 쓸 때 baseline hash, 재확인, stale-write 방어
- 자연스러운 경계의 trigger와 실패·지연 시 fallback
- Verify가 제품 test를 참조하는 방식, durable 실행 조건과 receipt retention
- Descendant timeout timing flake의 synchronization 수정
- 개선 효과를 판단할 latency, stale-context 발견, handoff 성공 지표

## 다음 행동

위 보고 cadence 한 가지를 먼저 사용자와 확정한다. 그다음 최소 자동 쓰기 allowlist와 memory 축적 방지 조건을 정한다. 이 두 결정 전에는 background runtime을 구현하지 않는다.
