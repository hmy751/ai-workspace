# Response-end Observe runtime과 live smoke

날짜: `2026-08-17`

## Trigger

Workspace 005에서 정한 response-end 유지 계약을 곧바로 Context 자동 갱신으로 확대하지 않고, 실제 Codex hook이 event를 빠뜨리지 않고 전달할 수 있는지 먼저 확인하기로 했다. 첫 구현 범위는 이 저장소와 Workspace 005에 한정한 **Observe protocol**이다.

## 구현한 범위

- [`.codex/hooks.json`](../../../../.codex/hooks.json)이 `UserPromptSubmit`, `Stop`, `SessionStart`를 repo-local runtime으로 전달한다.
- [`.codex/context_maintainer/`](../../../../.codex/context_maintainer/)가 `session_id + turn_id`를 한 response identity로 사용해 partial, queue, inflight, cursor와 hash ledger를 관리한다.
- `status`는 raw 사용자·assistant 본문을 출력하지 않고 queue, missing pair, gap, duplicate, failure와 proof ceiling을 사람과 JSON 형식으로 보여 준다.
- `drain`은 완성된 event만 FIFO로 처리하고, 성공 뒤 raw event를 지운다. Observe 결과로 `no_change`, `updated` 같은 의미 판정을 만들지 않는다.
- runtime state는 tracked `.codex/`가 아니라 Git에서 제외된 `.context-harness/runtime/context-maintainer/v1/`에 둔다. 처음 후보였던 `.codex/runtime/`은 실제 sandbox 쓰기에서 `PermissionError`가 발생해 사용하지 않았다.
- 현재 구현은 LLM이나 subagent를 실행하지 않고 Context 문서를 쓰지 않는다. 기존 수동 `context_maintainer` routing도 대체하지 않는다.

Reference Project, `apply-context-harness` skill, 축소 Verify, `memory/` migration은 이번 구현 범위에 포함하지 않았다.

## 내부 검증

다음 28개 unit test가 통과했다.

```bash
python3 -m unittest discover -s .codex/context_maintainer/tests -p 'test_*.py' -v
```

검사 범위는 정상 pairing, duplicate와 out-of-order, missing pair와 gap, 동시 enqueue, malformed partial·queue·ledger, user-first·stop-first crash residue, partial-first sequence commit, 동일 identity의 content conflict, raw cleanup, status redaction, recursion guard, config·ignore·hook 구조다. Python 3.9 compile, hook stdout JSON, `git diff --check`도 통과했다.

독립 검토에서 발견한 sequence 예약 직후 crash window는 partial-first commit과 reconciliation으로 닫았다. 동일 identity에 다른 prompt·assistant content가 replay되면 benign duplicate로 넘기지 않고 conflict를 봉인해 drain을 막도록 보정했다. 이 두 변경의 회귀 test까지 통과했지만 실제 async Stop 취소와는 별개의 내부 protocol 보정이다.

## 실제 Codex hook smoke

read-only Codex task를 Terra 모델로 한 번 실행해 `hook-smoke-ok`만 답하게 했다. 실제 결과는 다음과 같았다.

1. `SessionStart`와 `UserPromptSubmit`은 runtime에 도달했다.
2. User event가 sequence 1을 예약하고 partial을 만들었다.
3. `Stop`은 `async: true`였고, `codex exec` session 종료 때 background hook이 끝나기 전에 취소됐다.
4. 따라서 sequence 1은 `waiting_stop`, cursor는 미생성, 뒤 event는 global FIFO gap에 막히는 상태로 남았다.

이는 [OpenAI Hooks 문서](https://learn.chatgpt.com/docs/hooks)가 설명하는 “background hooks는 session 종료 시 unfinished process가 취소될 수 있다”는 한계를 실제로 재현한 것이다. `async` 설정 존재나 unit test만으로 response-end delivery를 증명할 수 없다는 점도 확인했다.

## 판정과 증명 상한

- **통과**: payload 두 개가 runtime에 도달한 뒤의 identity, FIFO, duplicate, crash residue와 raw cleanup 동작
- **실패**: 실제 Main 응답마다 `Stop`이 durable하게 도달한다는 end-to-end pairing
- **미증명**: fresh Desktop task의 project hook trust, global hook과 장기 공존, 여러 session 격리, 자동 background Maintainer, Context conditional write

현재 queue는 repo worktree 전체가 공유한다. 한 session의 누락 Stop이 다른 session의 뒤 event도 막는다. 수동 gap repair나 session 격리도 아직 없다. 그러므로 Observe runtime은 구현됐지만 운영 acceptance나 `state-only` write 단계로 넘어갈 수 없다.

## 다음 결정

실제 결함을 고치려면 다음 두 권한을 사용자와 먼저 정해야 한다.

1. `Stop`의 **작은 deterministic capture와 enqueue까지만 synchronous**로 바꿔 응답 종료에 짧은 지연을 허용할지. 이후 의미 판단·Maintainer 처리는 계속 background에 둔다.
2. 현재처럼 Stop이 영구 누락된 exact expected sequence를 사람이 reason과 함께 **abandoned 처리**하고 raw partial을 지우며 FIFO를 복구하는 좁은 명령을 허용할지.

두 항목은 각각 응답 지연과 관찰 증거 폐기 권한을 새로 만든다. 따라서 내부 crash cleanup과 달리 묵시적으로 채택하지 않았다.

## 후속 정정

이 기록 뒤 추가 점검에서 Git fingerprint 실패 오표시, queue·ledger crash window의 content 무결성, 잘못된 `next_sequence` 타입의 status crash와 대화-only event의 전체 repository Git scan이 확인됐다. 따라서 위 28개 test의 proof ceiling은 더 좁다. 또한 sync capture·manual repair부터 결정하는 커서는 최종 계획이 아니다. 현재 판정과 Reference 전체 구현 순서는 [세션형 Maintainer 동작과 Reference 구현 계획](2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md)을 따른다.
