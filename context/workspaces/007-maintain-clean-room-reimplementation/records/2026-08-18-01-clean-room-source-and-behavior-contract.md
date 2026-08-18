# Clean-room source와 Maintain behavior contract

날짜: `2026-08-18`

상태: **새 구현이 보존할 behavior 기준과 과거 topology의 비구속 경계**

## 이 기록의 역할

새 세션이 Workspace 005의 긴 대화나 006의 구현 diff에서 구조를 추측하지 않고, 사용자가 직접 확인한 경험과 글로벌 책임 기준에서 첫 구현을 도출하게 한다. 아래 인용은 판단 뉘앙스를 보존하는 최소 원문이고, 상세 맥락은 연결한 원래 record가 소유한다.

이 기록은 `005의 동작을 보존한다`는 뜻이지 `005의 구현을 복원한다`는 뜻이 아니다.

## 선택한 source와 역할

직접 행동 근거는 다음 네 기록이다.

- [005 record 02](../../005-context-continuity-maintenance/records/2026-08-17-02-context-continuity-and-background-maintenance-framing.md): current freshness가 Recover와 cross-session handoff보다 선행한다는 문제
- [005 record 03](../../005-context-continuity-maintenance/records/2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md): 매 response-end 점검, no-change no-write와 write 전 ambiguity
- [005 record 04](../../005-context-continuity-maintenance/records/2026-08-17-04-verify-evidence-recording-boundary.md): Verify를 제품 검증 주체가 아닌 선택적 증거 기록 보조로 낮춘 경계
- [005 record 08](../../005-context-continuity-maintenance/records/2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md): 세션형 Maintainer의 이해·비차단·보고·복구와 기술 후보가 자동 승계되지 않는 경계

다음은 보조 또는 반례 source다.

- [005 record 05](../../005-context-continuity-maintenance/records/2026-08-17-05-maintainer-retrieval-runtime-and-cursor-contract.md): bounded retrieval, 같은 세션의 이해 재사용과 no-change도 점검 완료라는 의미를 보조한다. 당시 cursor·event 형태는 architecture 요구가 아니다.
- [005 record 06](../../005-context-continuity-maintenance/records/2026-08-17-06-response-end-observe-runtime-and-live-smoke.md): async `Stop` 취소와 repo-global FIFO gap을 실제 host에서 재현한 negative evidence다.
- [005 record 09](../../005-context-continuity-maintenance/records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md): Reference/root 소유 결과와 로컬 proof ceiling을 우선 사용한다. 상세 recovery topology는 기본 architecture가 아니라 필요성을 다시 판단할 역사적 구현 근거다.
- [006 self-check](../../006-maintain-behavior-responsibility-allocation/records/2026-08-18-03-self-check-and-purpose-first-reset.md)와 [clean-room 결정](../../006-maintain-behavior-responsibility-allocation/records/2026-08-18-05-clean-room-restart-decision.md): 기존 구현을 보존한 채 줄이는 접근이 목적보다 compatibility를 키운 이유를 보존한다. 006 code name과 state shape에는 요구사항이나 금지 항목의 지위를 미리 부여하지 않는다.

## 사용자 발화의 최소 원문

### Freshness가 handoff보다 선행한다

사용자는 current 정합성에 관해 다음처럼 말했다.

> 이거 자체가 깨지면 다 깨지는 것 같아서

> 다른 세션이 들어오면 어느정도 유지는되어야 하지 않나

> 안 그럼 핸드오프가 안되잖아

따라서 Recover가 빠르다는 사실만으로 handoff가 성립하지 않는다. 다음 세션이 읽는 current가 실제 상태와 맞거나, 맞지 않음을 false success 없이 드러내야 한다.

### 매 응답 종료에 점검하되 변화가 없으면 지나간다

> 그래도 대화 응답 끝나면 점검하게 그래야 잘 유지될 것 같은데?

> 그러니까 매번 점검하는데 아까 나눈 기준들로 갱신하는거고 없으며 그냥 점검하고 지나가는거고 이게 맞는거 맞지?

점검 cadence와 persistent write cadence는 다르다. 매 response-end에 확인하지만 durable 변화가 없으면 write·record·report를 만들지 않는다.

### Maintainer는 전달 장치가 아니라 세션을 이해하는 agent다

> 받는다기보다 에이전트니까 알아서 가져가서 뭐 이해해야지

> 처음은 이해 갖춘뒤 해도 될 것 같아 싱크 맞출겸

> 새 작업 세션이면 메인테이너가 새로 이해해야지 그 세션에서 생기면서

새 세션은 외부 canonical에서 bounded grounding하고, 같은 세션에서는 이미 얻은 이해를 이어 쓴다. Queue나 cursor는 필요할 수 있는 adapter이지 이 경험의 정의가 아니다.

### Main 비차단과 판단·보고 경계

> 메인 세션이 최대한 방해 받지 않는 방향이었으면 좋겠어 그래야 메인이 안 기다리는데 기다리다보면 작업이 쓸데 없이 늦춰지는 것 같아서

> 뭐 사소한건 조용이하고 중요한 건데 작업 할만한거면 수정 후 보고 하면 되겠지? 애매한건 물어보고

Durability가 write 여부를 정하고, 사용자에게 알려야 할 중요도가 report 여부를 정한다. Ambiguity는 retry 대상이 아니라 관련 write 전 질문 대상이다.

### Verify는 실제 제품 검증을 대신하지 않는다

> 검증이나 test나 eval같은걸 잘 남겨서 context를 잘 유지하는데 도움을 주는거지 직접 코드 테스트 검증 평가를 책임지는게 아니라

Main·제품 Owner·CI·eval·사람이 실제 확인을 소유한다. Verify가 있다면 보존할 가치가 있는 이미 발생한 확인의 출처와 결과를 작게 기록하는 하위 장치다.

## 구조 독립적인 behavior contract

위 근거에서 새 구현이 보여야 할 장면은 여섯 가지다.

1. 기존 Workspace의 새 세션은 필요한 current만 bounded하게 읽고 시작 상태를 한 번 드러낸다.
2. 같은 세션의 후속 응답에서는 이미 이해한 맥락을 사용하고 넓은 재조사를 반복하지 않는다.
3. 모든 사용자 대상 Main response-end는 변화 여부를 점검한다.
4. Durable 변화가 없으면 persistent write와 report가 없다.
5. 명확한 변화는 기존 Owner에 반영하고 중요도에 따라 조용히 끝내거나 반영 뒤 보고한다. Ambiguity는 관련 write 전에 묻는다.
6. 초기 grounding 뒤 Main을 기다리게 하지 않고, 실패·지연·stale 상태를 fresh 또는 completed로 가장하지 않는다.

`bounded`, `warm`, `response-end`, `quiet`, `important`, `ambiguous`, `fresh`는 구현 enum 이름이 아니다. Acceptance는 실제 사용자 장면의 관찰로 연결해야 한다.

## 글로벌 reference를 적용한 책임 판단

Root [`AGENTS.md`](../../../../AGENTS.md)의 Shared reference routing에 따라 다음 다섯 기준을 직접 적용한다.

### `ai-system_behavior-responsibility-allocation.md`

먼저 운영상 하나인 Maintain 동작의 시작 조건, 입력·맥락, 결과·부작용, 비목표와 반드시 지킬 약속을 식별한다. 그 뒤 해석·선택, 보장·거부, 권한·승인, 실행·기록을 나눈다.

- 자연어 맥락을 종합해야 하는 durability·Owner·ambiguity·보고 중요도는 모델 판단에 남길 이유가 크다.
- 같은 상태에서 같은 거부가 필요하고 predicate로 표현 가능한 Workspace binding, write allowlist, path·symlink, stale baseline과 false success는 규칙 장치가 집행할 이유가 크다.
- Goal·정책·중요한 예외·되돌리기 어려운 권한·acceptance는 사람에게 남는다.
- 중요하다는 이유만으로 모든 의미 판단을 코드화하지 않고, 정확한 보장이 필요하다는 이유만으로 prompt 준수를 보장이라고 부르지 않는다.

새 장치를 제안할 때는 “이것이 없으면 여섯 장면 중 무엇이 깨지는가”, “더 단순한 platform 제약이나 schema·permission으로 같은 보장을 얻는가”, “새 상태·실패·복구·검증 책임의 비용은 무엇인가”를 함께 답한다.

### `ai-system_responsibility-cohesion.md`

하나의 책임으로 이해해야 하는 정의·구현·검증이 기술 계층별 파일에 흩어져 새 독자가 다시 조립하게 만들지 않는다. 반대로 등장한 state마다 별도 책임 경계를 만들지 않는다. Reference의 상위 Harness 경계는 하위 책임의 관계를 설명하고, Maintain은 자기 목적·규칙·구현·검증을 자기 진입점에서 찾게 한다.

### `ai-system_context-ownership-boundary.md`

Workspace README가 정체성·범위와 current·output·records 관계의 canonical이다. Current 내용, 실제 코드·Git·test 사실과 과거 근거의 Owner를 구분한다. Hook·agent·runtime은 갱신 장치일 수 있지만 Context Owner나 canonical이 되지 않는다.

### `ai-system_human-readable-structure.md`

사람은 machine state나 recovery code부터 역추적하지 않고 현재 문제, 유효한 상태, 결정할 사항, 상세 근거와 다음 지시 대상을 찾을 수 있어야 한다. 사람용 설명은 machine state를 복제하지 않고 의미와 실제 canonical을 연결한다.

### `ai-system_harness-rippability.md`

Hook·runtime·warm-session adapter를 제거해도 Workspace 의미, 관리 기준과 책임 관계가 남아야 한다. 현재 platform 전제를 보완하는 장치가 지속 의미를 독점하면 안 된다.

## 자동 승계하지 않는 과거 topology

[005 record 08](../../005-context-continuity-maintenance/records/2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md)은 특정 hook 조합, queue·locking·storage·transaction, session resume 명령, cursor 파일·schema, CLI·JSON, raw 보존과 UI 채널을 교체 가능한 기술 후보로 명시했다. 따라서 다음은 미리 승인된 요구사항도 금지된 구조도 아니며, 현재 조건에서 필요성과 대안을 다시 판단한다.

- UserPrompt에서 sequence를 먼저 예약하는 partial/orphan protocol
- Worktree 전체 FIFO와 missing-Stop gap repair
- Session별 report queue와 cross-session resolver
- `decision intent → writer journal → completion marker → checkpoint` lifecycle
- Workspace attention, legacy migration과 delivery cursor
- Unit/fake-process suite의 기존 test count

새 설계는 같은 장치든 다른 장치든 선택할 수 있다. 어떤 선택이든 여섯 장면과 직접 연결된 필요, 더 단순한 대안, 새 실패·복구 비용과 실제 acceptance를 현재 근거에서 설명해야 한다.

## 새 세션의 첫 산출물

코드를 고르기 전에 여섯 장면 각각을 다음 항목으로 펼친 작은 acceptance matrix를 만든다.

- 시작 조건과 필요한 입력
- 모델이 판단할 의미
- deterministic하게 거부·보장할 최소 경계
- 사람에게 남는 결정과 승인
- 사용자가 실제로 관찰할 결과
- 실패 시 false success 없이 드러날 상태
- 가장 작은 직접 검증과 actual host acceptance

Matrix가 과거 state 이름이나 파일 topology를 출발 전제로 삼는다면 그 필요와 대안을 명시적으로 비교한다. 현재 근거 없이 관성적으로 선택된 경우에만 이 behavior contract로 돌아와 다시 판단한다.
