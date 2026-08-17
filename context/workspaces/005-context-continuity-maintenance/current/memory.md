# Context continuity maintenance memory

마지막 갱신: `2026-08-17`

## 목표

Main과 사용자의 작업 흐름은 빠르게 유지하면서, 다음 세션이 낡은 `current`나 무관한 records 때문에 잘못 출발하지 않도록 지속 context의 freshness와 handoff 품질을 관리한다. 매 AI 응답 종료에 그 응답의 delta를 점검하되, durable 변화가 있을 때만 좁게 갱신하는 운영 모델을 만든다.

## 사용자 우선순위

- 현재 시스템의 가장 큰 우려는 **C와 E**다. 사용자의 설명에서 C는 `current/records` 자체가 깨지면 나머지 Recover·handoff도 함께 무너지는 기반 신뢰 문제이고, E는 다른 세션이 들어와 작업을 이어 갈 수 있어야 한다는 continuity 문제다.
- 평소 작업에서는 **A, B, C, E**가 모두 부담이다. A에 해당하는 재조사는 허용할 수 있지만 짧고 bounded해야 한다. B에 해당하는 완전한 상시 유지가 현실적으로 어렵다는 점은 인정하며, 중간의 의미 있는 변화와 대화·작업 종료 경계에서 적절히 갱신하는 방식은 받아들일 수 있다.
- Recover는 E를 일부 해결하지만 C를 대신하지 않는다. Recover는 선택된 `current`를 충실히 읽을 뿐, 그 내용이 stale하면 stale handoff를 더 정확히 재현한다. 따라서 `Maintain → trustworthy current → Recover → 다음 세션` 순서에서 C가 E의 선행 조건이다.
- 사용자는 Verify에 test가 계속 쌓이거나 Main이 이미 수행한 검증을 다시 맡아 관심사가 커지는 것을 우려한다. Verify는 제품 검증을 소유하지 않고, 이미 일어난 test·eval·수동 확인 중 나중에 다시 볼 가치가 있는 최소 증거만 보존한다.

## 유지할 역할 경계

- **Main/work**가 실제 변경과 반복 개발 판단을 수행하고 평소에는 제품의 direct test를 실행한다.
- **Recover**는 명시 Workspace의 필요한 current·output·Project context와 연결된 검증 근거를 read-only로 복구한다. 문서 의미를 고치지 않는다.
- **Verify**는 Main·제품 test·CI·eval·사람이 이미 수행한 확인의 최소 증거를 나중에 헷갈리지 않도록 보존하는 선택적 기록 보조다. test·eval 설계와 선택, 코드나 test 작성, 명령 재실행, coverage·충분성 판단, acceptance를 소유하지 않는다.
- **Maintain**은 매 AI 응답 종료에 활성화되어 그 응답에서 생긴 delta와 관련 Context Owner를 점검한다. 실제 작업·Git·test 결과와 대조해 durable 변화가 있을 때만 `current`, 필요한 record와 output routing을 의미적으로 갱신하며, 변화가 없으면 쓰지 않고 종료한다.
- **Harness validation**은 Recover와 증거 기록 helper 같은 Harness runtime의 schema·path 방어가 작동하는지 검사한다. 일상 제품 작업의 추가 제품 검증 단계가 아니다.
- 사람 acceptance와 제품 Owner 판단은 위 역할들이 대신하지 않는다.

## 선택된 Maintain 운영 기준

- 점검은 매 AI 응답 종료마다 실행한다. 매번 문서를 쓰거나 record를 만드는 규칙은 아니다. 이번 응답에 durable 변화가 없으면 아무것도 수정하지 않고 종료한다.
- 명확한 변화는 background maintainer가 다음 allowlist 안에서 자동 반영한다.
  - 지금의 문제·상태·다음 행동은 `current/state`
  - 작업 뒤에도 유지될 명시적 장기 기준은 memory
  - 판단 과정·근거를 다시 볼 필요가 있는 중요한 사건은 필요한 경우 하나로 집계한 record
  - 이미 선택이 확정된 산출물의 경로·상태는 `output/index`
- 애매한 후보는 쌓아두거나 추측해 쓰지 않고 즉시 짧게 보고하며, 해당 반영만 보류한다. 관련 없는 main 작업은 계속하고, 애매함이 현재 작업 방향을 바꿀 위험이 있을 때만 main도 멈춘다.
- Memory가 늘어나는 것 자체는 문제로 보지 않는다. 새로운 장기 기준은 추가할 수 있고, 기존 기준이 바뀌면 중복 append보다 현재 기준으로 교체·정합화한다. 판단 근거를 다시 볼 필요가 있으면 memory에서 record를 연결할 수 있지만 모든 memory에 record를 의무화하지 않는다.
- 향후 `memory/` 폴더와 index routing으로 책임별 문서를 연결하고, 재진입 때 필요한 memory만 선택해 읽는 방향을 채택했다. 현재 `current/memory.md`를 이 구조로 migration하거나 runtime을 구현한 것은 아니다.
- 실제 갱신 구현에는 `delta 분류 → Owner 선택 → 동시 수정·stale overwrite 확인 → write → 링크·상태 확인 → 보고` 순서를 포함한다.
- Recover는 현재 별도 문제나 변경 요구가 없다.

## 선택된 Maintain retrieval·runtime 기준

- 평소 bootstrap은 Workspace README와 `current/index`가 current canonical과 읽을 조건을 routing하는 데서 시작한다. Records 본문은 index를 읽은 뒤 과거 이유·상세 근거가 실제로 필요할 때만 선택한다.
- 판단·결정·제약의 외부 canonical은 Workspace README와 current의 index·memory·state 및 필요한 routing이다. 구현·실행 사실의 canonical은 실제 파일, Git과 test 결과다. Maintainer의 내부 기억은 이 외부 근거를 대신하지 않는다.
- Delta는 마지막 처리 cursor 이후의 정확한 새 사용자·Main 발화, 관련 changed path와 tool·Git·test 접근점을 담는 일시적 전달 입력이다. Delta 자체를 새 durable 문서나 context 저장층으로 관리하지 않는다.
- Maintainer는 현재 conversation task, 활성 Workspace와 current worktree가 같은 동안 한 주체를 살려 재사용한다. 응답 사이에는 대기하고, 같은 Maintainer의 response-end event는 순서대로 직렬 처리한다.
- 사용자 대상 Main 응답이 확정된 시점만 response-end event다. Maintainer나 다른 subagent의 내부 응답은 새 trigger가 아니다. Event는 main을 막지 않는 background 처리로 넘긴다.
- Workspace·worktree 전환, 대화 종료나 handoff, Maintainer restart·자기 context compaction, processing cursor gap, Owner·routing 구조 변경 시 외부 canonical에서 rebootstrap하거나 수명 경계를 reset한다. Main context compaction만으로 Maintainer reset을 자동 요구하지 않는다.
- Processing cursor는 context나 records가 아닌 runtime machine checkpoint다. No-change도 처리 완료로 전진하지만, 실패는 last completed response를 전진시키지 않아 replay할 수 있어야 한다.
- Git 대조는 전체 repository review가 아니다. 대화-only 응답이면 생략하고, 파일 작업이면 event가 알려준 관련 경로만 확인한다. Context write 직전에는 target 최신본과 revision을 다시 확인하며, branch·HEAD·worktree 전환이나 근거 모순이 있을 때만 범위를 넓힌다.

## 선택된 Verify 운영 기준

- Maintain이 실제 확인 결과를 관찰해 `current/records` 반영 필요성과 의미를 판단한다. Verify는 이 판단을 대신하지 않으며, 지속 가치가 있고 구조화가 자연스러운 증거가 필요할 때만 Maintain이 부르는 하위 기록 장치다.
- 최소 증거는 날짜·시각, producer 또는 출처, 무엇을 어떤 방법으로 확인했는지, 구체 결과, commit·CI·artifact·screenshot 같은 접근점, 남은 미확인 범위다.
- 기계 결과가 자연스럽게 있으면 JSON evidence로 보존할 수 있다. 수동 확인과 정성 평가는 Markdown 또는 원자료 링크로 충분하며, 모든 실행을 JSON으로 만들지 않는다. File path나 hash도 이미 결과에 있거나 증거 식별에 꼭 필요할 때만 둔다.
- Verify는 여러 test 파일을 일괄 snapshot·검사하거나 제품 명령을 다시 실행하지 않고, exit code만으로 `verification_passed`나 완료를 선언하지 않는다.
- 현재 Reference Verify 구현은 여전히 fixed argv 실행, basis/evidence snapshot, append-only receipt와 machine status 갱신 계약이다. 선택한 축소 경계로 코드·schema를 바꾸거나 과거 receipt를 migration하지 않았으며, 기존 receipt는 historical evidence로 보존한다.

## 증명 상한

이 Workspace는 현재 진단과 선택된 운영 기준만 소유한다. Background maintainer, response-end activation, memory index routing, event feed, 동시 쓰기 방어와 축소 Verify helper는 구현·실행·효과 측정을 하지 않았다. 기록된 유지 시간은 이번 대화의 task telemetry와 기존 records에 기반하며 일반 실행 시간 보장을 뜻하지 않는다.
