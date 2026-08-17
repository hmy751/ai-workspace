# 세션형 Maintainer 동작 확정과 Reference 전체 구현 계획

날짜: `2026-08-17`

## Trigger

[Reference 소유권 정정](2026-08-17-07-reference-ownership-correction-and-handoff.md) 뒤 계획을 다시 세우는 과정에서 다음 혼동이 반복됐다.

- response-end 전달 장치를 Maintain과 나란한 별도 책임처럼 설명했다.
- 빠름을 hook·queue 지연 중심으로 설명하고, 같은 Maintainer가 이미 이해한 상태를 유지하는 의미를 뒤로 밀었다.
- SQLite, CLI, schema, session resume 방식과 성능 수치를 합의된 계약처럼 앞서 확정했다.
- 이를 고치면서 이번에는 Reference canonical 수정 자체를 이해 확인 뒤로 미뤘다.

사용자는 최종 재사용 구현 전체가 `reference-project/`에 있어야 한다는 범위를 다시 고정하고, 이미 records에 확정된 Maintain 판단을 다시 질문하지 말라고 정정했다. 이 기록은 그 뒤 실제 세션 동작과 구현 순서를 다시 맞춘 결과를 보존한다.

## 최소 사용자 발화 근거

Maintainer가 event 입력을 받는 기계 장치보다 세션에서 자연스럽게 이해를 이어 가는 agent라는 의미는 다음 발화에서 분명해졌다.

> 그냥 매 세션마다 활동하는게 기본인거지 hook으로 정하든 발동을 정하든 바로하고 간단하면 자연스레 수정을 안하던가 하겠지

> 받는다기보다 에이전트니까 알아서 가져가서 뭐 이해해야지

속도는 Main 비차단과 Maintainer의 지속 이해를 함께 뜻한다.

> 메인 세션이 최대한 방해 받지 않는 방향이었으면 좋겠어 그래야 메인이 안 기다리는데 기다리다보면 작업이 쓸데 없이 늦춰지는 것 같아서

기존 Workspace로 시작하는 새 세션의 첫 grounding과 이후 세션 경계는 다음처럼 정했다.

> 처음은 이해 갖춘뒤 해도 될 것 같아 싱크 맞출겸

> 새 작업 세션이면 메인테이너가 새로 이해해야지 그 세션에서 생기면서

자동 반영과 보고 경계는 다음 발화로 닫았다.

> 뭐 사소한건 조용이하고 중요한 건데 작업 할만한거면 수정 후 보고 하면 되겠지? 애매한건 물어보고

실패 자체보다 복구 뒤 freshness가 기준이라는 점도 확인했다.

> 믿기 어려워질 때 짧게? 어쨋든 복구하려고 할거고 복구가 불가능한건 아닐거잖아?

## 확정한 실제 동작

### 세션 시작과 수명

- Main 작업 세션마다 그 세션 전용 Maintainer가 생긴다.
- 기존 Workspace라면 첫 작업 전에 Workspace README와 `current/index` 중심으로 필요한 current를 선택해 짧게 grounding한다. Records 본문은 과거 이유나 정확한 근거가 실제로 필요할 때만 연다.
- 초기 grounding이 끝나면 목표·현재 상태·다음 행동을 한 번 짧게 보여 줘 Main과 사용자에게 시작점이 맞는지 확인 가능하게 한다.
- 새 Workspace는 미리 읽을 Context가 없다. Maintainer는 세션 대화를 함께 따라가되, identity·goal·Owner가 형성되기 전에 지속 문서를 추측해 만들지 않는다.
- 같은 conversation task·Workspace·worktree에서는 같은 Maintainer의 이해를 유지한다. Main context compaction만으로 살아 있는 Maintainer를 초기화하지 않는다.
- 새 작업 세션에서는 새 Maintainer가 외부 canonical에서 다시 이해한다. 이전 Maintainer의 내부 기억을 세션 사이 durable truth로 보존하지 않는다.

### 응답 종료 활동과 Main 비차단

- Maintainer는 세션의 대화와 작업을 계속 이해하는 agent다. 사용자·Main 발화나 관련 근거를 event payload로 옮기는 것은 필요할 수 있는 adapter 구현이지 Maintainer 역할의 사용자-facing 정의가 아니다.
- 매 사용자 대상 Main 응답 종료는 Maintainer가 그동안 생긴 변화를 점검하는 활동 시점이다.
- 초기 grounding 뒤 Maintainer의 점검·갱신·복구 때문에 Main 응답이나 관련 없는 다음 작업을 기다리게 하지 않는다.
- 같은 Maintainer가 이미 가진 이해를 재사용하고, 두 번째 응답부터 전체 history·records·repository를 다시 조사하지 않는다.

### 판단·쓰기·보고

- Durable 변화가 없으면 아무것도 쓰지 않고 보고도 하지 않는다.
- 명확한 durable 변화는 기존 allowlist의 올바른 Owner에 반영한다.
- 사소하고 명확한 반영은 조용히 처리한다. 중요한 명확한 반영은 먼저 수정하고 짧게 결과를 보고한다.
- 의미·Owner·장기성·사용자 의도가 애매하면 추측해 쓰지 않고 즉시 질문한다. 해당 반영만 보류하고 관련 없는 Main 작업은 계속하며, 현재 방향을 바꿀 ambiguity일 때만 관련 Main 작업도 멈춘다.
- `사소함`은 write 여부의 기준이 아니다. Write 여부는 durability로, 보고 여부는 사용자가 알아야 할 중요도로 판단한다.

### 실패와 복구

- 일시적 runtime 실패, 뒤처진 처리와 Maintainer restart는 먼저 자동 retry·replay·rebootstrap으로 복구한다.
- 복구 중에는 성공한 것처럼 completed 상태나 fresh Context를 가장하지 않는다.
- 자동 복구 뒤에도 외부 canonical과 실제 상태를 대조해 freshness를 다시 세울 수 없을 때만 사용자에게 짧게 경고하고 필요한 부분을 묻는다.
- Semantic ambiguity는 runtime 실패가 아니므로 반복 retry로 미루지 않고 위 ambiguity 규칙대로 바로 올린다.

## Reference 소유권과 구현 계획

최종 목표는 root Observe를 옮기는 데서 끝나지 않는다. Workspace 005에서 합의한 Maintain·Verify 운영 전체의 재사용 가능한 구현은 `reference-project/`가 소유하고, root는 이를 Workspace 005에서 실행하는 얇은 dogfood adapter만 소유한다.

구현 순서는 다음과 같이 확정했다.

1. Reference Harness·Maintain의 사람용 진입 문서와 계약을 위 세션형 Maintainer 의미로 수정한다.
2. 별도 root 실험이 아니라 Reference Maintain 구현 안에서 session lifetime, background 비차단, 보고와 restart 복구 가능성을 time-boxed spike로 확인한다.
3. Spike 근거로 trigger, agent continuity, processing checkpoint, retry와 reporting adapter의 최소 구조를 결정한다.
4. Reference에 initial sync, warm continuity, no-change, 좁은 `current/state` 반영, 중요 반영 보고, ambiguity 질문과 자동 복구의 첫 vertical slice를 구현한다.
5. Root를 Reference를 호출하는 thin adapter로 전환하고 실제 여러 turn·Main compaction·Maintainer restart·failure를 dogfood한다.
6. Reference write 범위를 memory와 index, 집계 records, 확정 output routing 순서로 확장한다.
7. 축소 Verify를 선택적 증거 기록 도구로 구현하고 기존 Verify·Recover 호환을 확인한다. Dogfood에서 Maintain freshness를 Recover에 연결할 필요가 있는지 확인하되, 실제 결함 근거가 있을 때만 Recover를 최소 변경한다.
8. 마지막으로 `apply-context-harness`를 새 Reference 구현에 맞게 갱신하고 root 중복 runtime을 정리한 뒤 전체 validation과 fresh-task acceptance를 수행한다.

첫 vertical slice는 중간 milestone이며 전체 완료가 아니다. Memory·records·output, 축소 Verify, Recover 호환, 이식 skill까지 끝나야 Reference 전체 구현 목표가 완료된다.

## 구현 후보로 내린 항목

다음은 목표를 만족시키기 위한 교체 가능한 기술 후보이며 현재 승인된 architecture가 아니다.

- 특정 hook 조합과 sync·async capture 방식
- Queue, locking, storage와 transaction 방식
- Maintainer session을 이어 쓰는 정확한 Codex 명령이나 adapter
- Processing cursor의 파일 위치와 구체 schema
- CLI 이름, enum과 JSON 형태
- Raw 대화의 durable 보존·삭제 방식
- 중요 반영·ambiguity·복구 경고를 보여 줄 정확한 UI·hook 채널
- 측정 전의 고정 latency 횟수와 수치

Global `ai-system_*` shared reference는 책임 응집, 사람용 진입과 하네스 제거 가능성을 확인하는 감사 기준으로만 적용한다. 이 구현의 목표나 별도 산출물이 아니며 global reference 파일은 수정하지 않는다.

## 기존 Observe에서 이어 갈 회귀 입력

현재 root Observe는 최종 architecture가 아닌 실험 근거다. 28개 unit test가 통과했어도 추가 점검에서 다음 결함이 확인됐으므로 proof ceiling을 넓히지 않는다.

- Git fingerprint 명령 실패를 `available: true`로 표시하면서 `head`와 `branch`를 `null`로 남긴다.
- Queue publish와 ledger 갱신 사이 crash에서 content 무결성과 duplicate·conflict 판정이 어긋날 수 있다.
- Valid JSON이지만 `next_sequence` 타입이 잘못된 control에서 `status`가 `ValueError`로 종료된다.
- 대화-only event에도 매번 전체 repository의 untracked 변경까지 Git scan한다.

Reference에서 선택한 새 구현은 이 네 항목을 회귀 조건으로 다룬다. V1 raw runtime state는 새 구현이 자동으로 완료 처리하거나 의미를 재해석하지 않는다.

## 성공 기준

- 기존 Workspace의 새 세션은 bounded grounding 뒤 짧은 상태를 보여 주고 시작한다.
- 두 번째 응답부터 같은 Maintainer 이해를 재사용해 넓은 재조사를 반복하지 않는다.
- Main 응답은 background Maintain 완료를 기다리지 않는다.
- No-change, 조용한 명확 반영, 중요한 반영 후 보고와 write 전 ambiguity 질문이 실제 사용자 장면에서 구별된다.
- 자동 복구 가능한 실패는 사용자 작업을 방해하지 않고, freshness를 복원하지 못했을 때만 false success 없이 경고한다.
- 작업 종료에 수분짜리 Maintain tail을 다시 만들지 않는다.
- 다음 세션은 stale `current`를 정상 상태로 오해하지 않고 전체 records 재독 없이 handoff를 시작한다.
- 재사용 가능한 코드·계약·검증은 Reference에서 함께 발견되고, root에는 같은 구현을 복제하지 않는다.

## 다음 커서

이 문서 갱신과 현재 미커밋 Workspace 005 작업을 검증·commit한 뒤, Reference Harness·Maintain 계약 수정부터 시작한다. 새 기술안을 먼저 확정하거나 root Observe 결함만 고치는 것으로 돌아가지 않는다.
