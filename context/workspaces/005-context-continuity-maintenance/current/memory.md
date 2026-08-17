# Context continuity maintenance memory

마지막 갱신: `2026-08-17`

## 목표

Main과 사용자의 작업 흐름은 빠르게 유지하면서, 다음 세션이 낡은 `current`나 무관한 records 때문에 잘못 출발하지 않도록 지속 context의 freshness와 handoff 품질을 관리한다. 완벽한 실시간 동기화가 아니라, 위험한 stale state를 우선 막고 자연스러운 경계에서 압축·정합화하는 운영 모델을 만든다.

## 사용자 우선순위

- 현재 시스템의 가장 큰 우려는 **C와 E**다. 사용자의 설명에서 C는 `current/records` 자체가 깨지면 나머지 Recover·handoff도 함께 무너지는 기반 신뢰 문제이고, E는 다른 세션이 들어와 작업을 이어 갈 수 있어야 한다는 continuity 문제다.
- 평소 작업에서는 **A, B, C, E**가 모두 부담이다. A에 해당하는 재조사는 허용할 수 있지만 짧고 bounded해야 한다. B에 해당하는 완전한 상시 유지가 현실적으로 어렵다는 점은 인정하며, 중간의 의미 있는 변화와 대화·작업 종료 경계에서 적절히 갱신하는 방식은 받아들일 수 있다.
- Recover는 E를 일부 해결하지만 C를 대신하지 않는다. Recover는 선택된 `current`를 충실히 읽을 뿐, 그 내용이 stale하면 stale handoff를 더 정확히 재현한다. 따라서 `Maintain → trustworthy current → Recover → 다음 세션` 순서에서 C가 E의 선행 조건이다.
- 사용자는 Verify에 test가 계속 쌓여 관심사가 커지는 것도 우려한다. Verify는 제품이 이미 소유한 검증 명령과 근거를 실행·추적해야 하며, 자체적으로 큰 test catalog를 소유하는 방향은 피한다.

## 유지할 역할 경계

- **Main/work**가 실제 변경과 반복 개발 판단을 수행하고 평소에는 제품의 direct test를 실행한다.
- **Recover**는 명시 Workspace의 필요한 current·output·Project context와 마지막 Verify freshness를 read-only로 복구한다. 문서 의미를 고치지 않는다.
- **Verify**는 상태 전환·handoff에 필요한 고정 제품 명령을 실행하고 입력 snapshot, receipt와 machine status를 남긴다. 코드 변화와 context 문서가 의미상 일치하는지를 스스로 해석하지 않는다.
- **Maintain**은 실제 작업·Git·test 결과와 Context Owner를 대조해 `current`, 필요한 record와 output routing을 의미적으로 정합화한다. 매 test나 매 발화 뒤 실행하지 않는다.
- **Harness validation**은 Recover·Verify runtime과 schema·path 방어가 작동하는지 검사한다. 일상 제품 작업의 네 번째 workflow 단계가 아니다.
- 사람 acceptance와 제품 Owner 판단은 위 역할들이 대신하지 않는다.

## 지금까지 선택된 방향

- 역할은 없애지 않는다. 평소 direct test, 상태 전환이나 인계 시 durable Verify, 의미 변화가 안정된 자연스러운 경계에서 Maintain을 실행한다.
- 명확한 state 변화는 background maintainer가 `current/state`와 짧은 event record를 직접 갱신하고 main 작업을 막지 않는 **A 방향**을 사용자가 선택했다. 자동 변경은 자연스러운 경계에서 묶어 알린다.
- 명시적인 장기 사용자 결정도 자동 `memory` 반영 쪽에 가깝지만, “막 쌓이면 안 된다”는 조건이 붙었다. 따라서 append가 기본이 아니며, 기존 항목의 교체·압축과 승격 조건이 먼저 필요하다.
- 애매한 후보는 durable context에 바로 쓰지 않는다. 현재 작업 방향을 잘못 만들 위험이 있을 때만 즉시 보고하고, 그 밖에는 자연스러운 경계에서 묶어 보고하는 안이 현재 유력하지만 아직 사용자 확인 전이다.

## 증명 상한

이 Workspace는 현재 진단과 설계 framing만 소유한다. Background maintainer, event feed, 동시 쓰기 방어, 자동 압축이나 report batching은 구현·실행·효과 측정을 하지 않았다. 기록된 유지 시간은 이번 대화의 task telemetry와 기존 records에 기반하며 일반 실행 시간 보장을 뜻하지 않는다.
