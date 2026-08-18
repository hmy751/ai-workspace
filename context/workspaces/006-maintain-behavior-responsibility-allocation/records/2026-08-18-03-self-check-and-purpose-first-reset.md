# Self-check와 목적 우선 재정렬

날짜: `2026-08-18`

## Trigger

사용자는 006의 current 목표와 실제 작업 결과 사이에 괴리가 있다고 지적했다. 글로벌 reference와 Workspace 005의 이유를 제대로 적용했다면 개별 runtime 결함보다 파일 구성, 과도한 설계와 Maintainer의 목적·흐름·mental model부터 의심했어야 하는데, 기존 기능을 유지한다는 이유로 test와 국소 guard만 점검한 것 같다는 정정이었다.

`ai-self-check`의 fresh auditor는 이 지적이 타당하다고 판정했다. Main은 “Workspace 005의 사용자 목적과 경험을 보존한다”를 현재 구현 방식까지 보존하는 조건으로 넓혔고, 글로벌 reference를 목적에서 구조를 다시 도출하는 기준보다 기존 파일에 역할을 붙이는 분류표처럼 사용했다. 따라서 fail-closed resolver는 잘못된 수정이라고 단정할 수는 없지만 006의 본래 구조 개선으로 승격할 근거가 없었다.

## Workspace 005 records에서 다시 복원한 흐름

이번 판단은 Workspace 005 records 01–09를 시간순으로 직접 읽어 다시 세웠다.

- Record 01의 시작 문제는 Harness wrapper 자체보다 넓은 Maintain, Main의 중복 test, review와 재정합화가 한 turn 뒤에 이어져 20–30분짜리 tail을 만든 것이었다.
- Record 02는 `current` freshness가 깨지면 Recover와 handoff도 무너진다는 우려, Main을 막지 않는 background Maintainer 방향과 함께 역할 구분과 현재 저장소의 고정 topology를 같게 보지 말라고 명시했다.
- Record 03은 매 사용자 대상 응답 종료마다 점검하되 no-change이면 쓰거나 보고하지 않고, 명확한 변화는 기존 Owner에 반영하며, ambiguity는 write 전에 즉시 묻는 사용자 장면을 확정했다.
- Record 04는 Main과 겹치던 Verify를 제품 검증 주체에서 이미 수행된 확인의 선택적 증거 기록 보조로 낮췄다.
- Record 05는 같은 세션의 Maintainer 이해 재사용, bounded retrieval와 작은 processing cursor를 합의했다. Delta는 별도 지속 문서가 아닌 일시적 전달 입력이다.
- Record 06의 root Observe는 partial·queue·ledger·cursor를 구현하고 unit test를 통과했지만 실제 Codex smoke에서 `async Stop`이 취소돼 sequence gap을 남겼고, 한 session 누락이 worktree 전체 FIFO를 막았다.
- Record 07은 root-only Observe가 최종 architecture가 아니며 재사용 가능한 책임은 Reference가 소유해야 한다고 정정했다.
- Record 08은 Maintainer의 본질을 event 운반 장치가 아니라 세션을 따라 이미 얻은 이해를 이어 쓰는 agent로 다시 고정했다. Hook 조합, queue·locking·storage·transaction, cursor schema, CLI·JSON, raw 보존과 UI 채널은 승인된 architecture가 아닌 교체 가능한 기술 후보라고 명시했다.
- Record 09의 최종 구현은 사용자 계약을 코드화했지만 `runtime.py` 4,603줄을 포함한 약 8,800줄의 production Python과 다층 crash protocol을 만들었다. 실제 nested Codex warm resume, background 비차단, UI notice와 semantic 문서 갱신 품질은 여전히 proof ceiling 밖이다.

## 보존할 사용자 mental model

보존 기준은 다음 여섯 장면이다.

1. 기존 Workspace의 새 세션은 필요한 current만 짧게 읽고 목표·현재 상태·다음 행동을 한 번 맞춘다.
2. 같은 세션에서는 같은 Maintainer가 이미 얻은 이해를 이어 쓴다.
3. 매 Main response-end를 점검하지만 durable 변화가 없으면 write·보고가 모두 없다.
4. 명확한 변화는 올바른 기존 Context Owner에 반영하고, 사소하면 조용히 끝내며 중요하면 반영 뒤 짧게 알린다.
5. 의미·Owner·장기성·사용자 의도가 애매하면 쓰기 전에 묻고 관련 없는 Main 작업은 계속한다.
6. 초기 grounding 뒤 Main은 Maintain을 기다리지 않으며, 다음 세션은 stale current를 fresh로 오해하지 않는다.

Queue, ledger, journal, completion marker, report acknowledgement와 repair CLI는 이 mental model 자체가 아니다.

## 목적에서 다시 배치한 최소 책임

- 모델은 durability, 올바른 기존 Owner, ambiguity와 사용자에게 보고할 중요도를 판단한다.
- 규칙 기반 장치는 명시된 Workspace와 허용 Markdown Owner 밖의 write, path traversal·symlink, stale baseline과 실패의 false success를 반복 가능하게 거부한다.
- 사람은 Workspace 선택, goal·정책·중요한 예외·acceptance와 자동 복원할 수 없는 누락의 의미를 결정한다.
- Main과 제품 Owner는 실제 변경과 test·eval을 수행한다. Verify는 보존 가치 있는 기존 증거를 기록할 뿐 이를 대신하지 않는다.
- Host hook과 runtime은 Maintainer를 깨우고 이어 주는 제거 가능한 adapter이며 Workspace 의미의 정본이 아니다.

지속 의미의 source of truth는 Workspace README·current·records와 실제 파일·Git·test 결과다. Warm Maintainer thread는 속도를 위한 cache다. Runtime에는 처리하지 않은 bounded response delta, warm thread cursor, `clean | pending | processing | failed` 수준의 freshness와 다음 safe point에 전할 notice·question보다 더 많은 의미를 기본 전제로 두지 않는다.

## 현재 구조에서 먼저 의심할 부분

현재 `runtime.py`는 capture·pairing, queue·sequencing, worker scheduling, session metadata, report delivery·resolution, freshness, gap repair, metrics와 tool evidence를 함께 소유한다. 반대로 하나의 Context 반영 commit은 `controller.py`, `intent.py`, `writer.py`, `runtime.py`에 나뉘어 있다. 나눠야 할 host delivery 책임은 한 파일에 모였고, 하나여야 할 apply 책임은 여러 상태와 파일에 흩어졌다.

우선 대조할 제거·통합 후보는 다음과 같다.

- UserPrompt 시 sequence를 미리 예약하면서 생긴 `partial/orphan/queue/ledger/control/gap-repair` 다층 상태
- session checkpoint마다 들어 있는 pending report와 Workspace 전체 session scan
- `decision intent → writer journal → stage → completion marker → checkpoint`의 중복 crash bridge
- `writes[].path`에서 파생 가능한 `changed_paths`, 사용되지 않는 `evidence_paths`, semantic outcome에 섞인 runtime `freshness_failed`
- session 간 scheduler·wake 전파와 protocol 내부 상태를 지키기 위해 생긴 metrics·status schema

다만 read-only semantic agent, Workspace allowlist, path traversal·symlink 거부, 최신 baseline 확인, 처리 성공 전 bounded response replay, warm thread id와 새 session grounding은 사용자 약속과 직접 연결되므로 단순화를 이유로 없애지 않는다.

## 이전 diff의 현재 지위

- Root Workspace ID를 `005`로 고정한 portable Reference test assertion 제거는 가변 root 선택과 Reference invariant를 분리하므로 유지 가치가 있다.
- Fail-closed report resolver와 관련 test는 현재 session checkpoint report topology 안에서 유효한 correctness 발견이다.
- 그러나 resolver 자체와 cross-session report scan이 남아야 하는지 아직 증명하지 않았으므로 선택된 개선 결과가 아니다. 새 구조가 pending semantic state를 Workspace 한 곳으로 옮기거나 report lifecycle을 단순화하면 이 diff는 함께 사라질 수 있다.

## 다음 작업 기준

기존 protocol state를 하나씩 보존하며 축소하지 않는다. 먼저 위 여섯 사용자 장면을 구조 독립적인 acceptance로 고정한 뒤, `semantic session`, `completed-response delivery`, `guarded apply` 세 책임과 작은 freshness cursor로 새 vertical path를 설계한다.

실제 host transcript를 안정적인 원자료로 쓸 수 있는지는 live acceptance 전에는 가정하지 않는다. 우선 현재 확인된 동기 capture 경계에서 완성된 user·assistant pair만 처리 대상으로 만드는 작은 outbox를 기준으로 삼고, 한 session 누락이 다른 session이나 관련 없는 Main 작업을 막지 않게 한다. Multi-file exact-once transaction이 아니라 최신 canonical을 다시 읽어 수렴하는 semantic reconciliation로 false freshness를 막을 수 있는지도 먼저 검증한다.
