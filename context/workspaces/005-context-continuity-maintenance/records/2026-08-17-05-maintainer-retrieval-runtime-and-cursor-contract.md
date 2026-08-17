# Maintainer retrieval·runtime·processing cursor 계약

기록일: `2026-08-17`

## 이 기록의 경계

[응답 종료 Maintain 계약](2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md)과 [축소 Verify 경계](2026-08-17-04-verify-evidence-recording-boundary.md) 뒤, 매 response-end 점검을 실제로 운영할 때 무엇을 읽고 같은 Maintainer를 얼마나 재사용하며 event 처리 완료를 어떻게 구분할지 닫은 설계 판단을 보존한다. 매 응답마다 새 record를 만드는 예가 아니라 후속 구현에 필요한 여러 응답의 확정 결론을 한 사건으로 집계한 기록이다.

## AI 제안과 사용자 확정

Main은 records 전체를 기본 입력으로 읽는 방식 대신 current index가 필요한 canonical과 읽을 조건을 routing하고, 실제 파일 작업이 있을 때만 Git 범위를 좁게 대조하는 안을 제안했다. Git은 changed path, context write target의 stale·concurrent write, branch·HEAD·worktree 전환에 따른 rebootstrap 필요만 확인하는 용도였다. 사용자는 이 범위에 다음처럼 답했다.

> 그래 이정도 가 좋다고 봐

이어 Main은 다음을 하나의 구체 설계안으로 제시했다.

- 현재 conversation task, 활성 Workspace와 current worktree가 같은 동안 Maintainer 한 주체를 재사용한다.
- 사용자 대상 Main 응답이 확정되면 정확한 새 발화와 관련 접근점을 response-end event로 전달한다.
- Context나 records가 아닌 작은 runtime processing cursor로 no-change, write, ambiguity, processing과 failure를 구분한다.
- Maintainer 자기 restart·compaction이나 Workspace·worktree 전환, handoff, cursor gap, Owner·routing 변경 때 외부 canonical에서 rebootstrap한다.

사용자는 이 전체 구체화에 다음처럼 승인했다.

> 이정도로 하자

따라서 아래 내용은 AI 후보를 그대로 적은 것이 아니라 사용자 확인을 받은 설계 계약이다. 다만 runtime 구현과 효과 검증은 아직 없다.

## Retrieval과 외부 canonical

### 기본 조회 순서

Maintainer는 Workspace README와 `current/index`부터 읽고, index가 가리킨 현재 memory·state와 필요한 routing을 선택한다. Records 본문은 과거 이유, 상세 증거 또는 사용자 발화의 정확한 경계가 현재 판단에 필요하다고 index가 알려 줄 때만 연다. Records를 평소 넓게 읽는 방식은 기본값이 아니다.

외부 canonical은 사실의 종류에 따라 나뉜다.

- 판단·결정·제약: Workspace README, current index·memory·state와 필요한 routing
- 구현·실행 사실: 실제 파일, 관련 Git 상태와 test 결과
- 과거 이유·상세 근거: index 뒤 조건부로 읽는 records

Maintainer 내부 context는 빠른 연속 처리를 돕지만 위 canonical보다 우선하지 않는다.

### Delta는 전달 입력이다

Delta는 마지막 processing cursor 이후 생긴 정확한 새 사용자·Main 발화, 실제 작업과 관련 changed path, tool·Git·test 결과의 접근점을 담는다. Maintainer가 변화 후보를 빠르게 찾기 위한 일시적 event payload이며, 별도 durable 문서나 새로운 context 저장층으로 축적하지 않는다.

## Maintainer 수명과 rebootstrap

Maintainer 재사용 수명은 다음 세 경계가 모두 같은 동안이다.

- 현재 conversation task
- 활성 Workspace
- current worktree

같은 경계에서는 동일 Maintainer가 응답 사이에 대기하다 response-end event를 순서대로 처리한다. 다음 중 하나가 생기면 내부 기억을 전제로 계속하지 않고 외부 canonical에서 rebootstrap하거나 수명 경계를 reset한다.

- Workspace 또는 worktree 전환
- 대화 종료나 명시적 handoff
- Maintainer 프로세스 restart 또는 Maintainer 자기 context compaction
- Processing cursor gap
- Owner 또는 routing 구조 변경

Main의 context가 compact됐다는 이유만으로 살아 있는 Maintainer까지 자동 reset하지 않는다. 반대로 Maintainer 자신이 restart되거나 compact되면 내부 기억을 버리고 외부 canonical과 processing cursor에서 다시 시작한다.

## Response-end event

Response-end는 사용자에게 보낼 Main 응답 내용이 확정된 시점의 event다. Maintainer나 다른 subagent가 내부에서 만든 응답은 새 response-end trigger가 아니다.

Event가 임시로 전달할 최소 입력은 다음과 같다.

- thread id, response id와 Workspace id
- 정확한 새 사용자 발화와 사용자 대상 Main 발화
- 관련 changed path
- tool, Git과 test 결과의 접근점
- previous response id

처리는 main의 다음 작업을 막지 않는 background 실행을 목표로 한다. 같은 Maintainer에 전달된 event는 순서대로 직렬 처리해 두 응답 delta가 섞여 current를 덮어쓰지 않게 한다.

## Processing cursor

Processing cursor는 `context/`나 records가 아니라 runtime이 소유하는 작은 machine checkpoint다. 최소한 다음 의미를 구분한다.

- thread와 Workspace
- last completed response
- `no_change`, `updated`, `needs_decision`, `processing`, `failed` 상태
- Maintainer가 읽은 current revision의 최소 식별값

No-write는 아무 일도 없었다는 뜻이 아니라 event를 성공적으로 점검했고 durable 변화가 없었다는 완료 상태다. 따라서 `no_change`도 completed cursor를 전진시킨다. `updated`도 해당 response가 처리됐음을 남긴다. `needs_decision`이 completed cursor와 pending 반영을 어떻게 함께 표현할지는 구체 schema에서 정한다.

실패는 last completed response를 전진시키지 않아 같은 event를 replay할 수 있게 한다. Runtime은 cursor로 duplicate, missing gap, out-of-order, no-write 완료와 failure를 서로 구분해야 한다.

## 좁은 Git 대조

Git 대조의 목적은 다음 세 가지뿐이다.

1. 실제 changed path 확인
2. Context write target의 stale·concurrent write 확인
3. Branch·HEAD·worktree 전환 때문에 rebootstrap이나 수명 reset이 필요한지 확인

대화-only response라면 Git 조회를 생략한다. 파일 작업이 있었다면 event나 runtime이 알려 준 관련 경로만 status로 확인하고, context write 직전에 target 최신본과 revision을 다시 읽는다. Branch·HEAD·worktree 전환이나 전달 근거와 실제 상태의 모순이 발견될 때만 조회 범위를 넓힌다. 전체 repository review는 일상 response-end 점검의 기본 단계가 아니다.

## 구현 상태와 proof ceiling

이번 합의는 retrieval·runtime의 의미 계약이다. 다음 항목은 아직 구현하거나 시험하지 않았다.

- 실제 response-end hook과 event producer·delivery
- Processing cursor 파일 위치와 구체 schema
- Queue, locking과 background worker 수명
- Maintainer 자체 restart·compaction 감지와 Main compaction을 reset 사유에서 제외하는 runtime 판별
- Cursor gap·duplicate·out-of-order·failure replay 동작
- Target revision 표현과 concurrent write 방어

따라서 동일 Maintainer 재사용, main 비차단 처리, no-change cursor 전진과 failure replay가 실제 Codex runtime에서 가능하거나 latency·freshness를 개선한다고 아직 말할 수 없다.

## 다음 설계 커서

다음은 확정한 의미를 다시 논의하는 단계가 아니라 구현 전 기술 결정과 작은 protocol prototype 범위를 정하는 단계다. 먼저 실제 Codex 환경에서 사용할 수 있는 response-end signal, background subagent 수명과 context 밖 checkpoint 위치를 읽기 전용으로 확인한다. 그 근거로 event envelope와 cursor 최소 schema, 직렬 queue와 replay state machine을 제안한 뒤 구현 승인 경계를 구분한다.

현재 커서는 [current state](../current/state.md)에 둔다.
