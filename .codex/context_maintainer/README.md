# Workspace 005 context-maintainer observe runtime

이 패키지는 사용자 대상 Main 응답의 `UserPromptSubmit`과 `Stop`을 한 response-end event로 묶어 전달 경로만 시험한다. 현재 mode는 `observe`, 대상은 `005-context-continuity-maintenance`로 고정되어 있다. LLM·subagent를 실행하거나 Context 문서를 수정하지 않는다.

## Hook 흐름

- `UserPromptSubmit`: `session_id + turn_id` identity에 exact prompt와 pre-turn Git fingerprint를 partial로 저장하고 FIFO sequence를 예약한다.
- `Stop` (async): 같은 identity의 assistant message와 post-turn Git fingerprint를 합쳐 queue event를 atomic rename으로 게시한 뒤 준비된 event를 FIFO로 drain한다.
- `SessionStart`: `startup|resume|clear|compact` metadata만 기록한다.
- `CODEX_CONTEXT_MAINTAINER_CHILD`가 설정된 프로세스에서는 세 hook 모두 아무것도 기록하지 않는다.

모든 hook은 stdin의 Codex JSON payload를 읽고 stdout에 valid JSON을 한 번 출력한다. malformed payload와 내부 실패는 Main을 막지 않으며 raw prompt·assistant를 제외한 진단만 runtime status에 남긴다. Project hook은 최초 사용 및 정의 변경 후 Codex `/hooks`에서 trust해야 한다.

Sequence는 control을 먼저 올리지 않는다. Exact prompt partial을 atomic rename으로 저장하고 hash-only ledger를 만든 뒤에만 control의 `next_sequence`를 commit한다. Partial 저장 뒤 process가 끝나도 다음 `SessionStart`, `status`, `drain` 또는 hook이 partial에서 ledger와 control을 복구한다. 아무 event·partial·ledger도 없는 마지막 control 예약만 재사용하며, 뒤 sequence 증거가 있는 gap은 자동으로 메우거나 abandon하지 않는다.

같은 `session_id + turn_id`가 replay되면 prompt와 assistant hash를 기존 ledger와 비교한다. 내용이 같을 때만 duplicate로 처리한다. 다르면 raw 후보를 덮어쓰지 않고 conflict와 malformed 진단을 남기며, 해당 ledger의 queue는 conflict가 해소되지 않는 한 drain하지 않는다.

## Runtime protocol

Runtime root는 Git에서 제외된 `.context-harness/runtime/context-maintainer/v1/`이다. `.codex/`는 Codex가 읽는 tracked 설정층이므로 runtime write를 두지 않고, 저장소 루트의 별도 hidden boundary를 사용한다.

- `partials/`: 아직 Stop과 짝지어지지 않은 raw prompt
- `queue/`: atomic하게 완성된 raw response-end event
- `inflight/`: cursor commit 전에 atomic rename된 다음 delivery event
- `cursor.json`: 마지막으로 성공한 delivery sequence
- `ledger/`: drain 뒤에도 duplicate를 막는 identity와 content hash
- `orphans/`: UserPromptSubmit보다 먼저 도착한 Stop
- `sessions/`: session start/compact metadata
- `diagnostics.json`: raw content 없는 malformed, duplicate, failure, stop-before-user count

Drain은 `cursor + 1` 하나만 다음 event로 인정한다. gap·malformed event에서는 cursor를 전진시키지 않는다. Observe delivery가 성공하면 queue의 raw event를 삭제하고 cursor와 content-hash ledger만 남긴다. Maintenance outcome은 만들지 않는다.

`SessionStart`, `status`, `drain` 진입은 lock 안에서 crash residue를 재조정한다. Cursor 이하에 남은 queue/inflight raw는 이미 완료된 delivery로 보고 삭제하며 ledger를 `drained`로 맞춘다. Ledger가 이미 `queued`, `drained`, `abandoned`인 identity의 중복 partial raw도 삭제한다. Control만 예약되고 event·ledger가 없는 sequence는 완료로 추정하거나 건너뛰지 않는다.

## Commands

```bash
python3 .codex/context_maintainer/cli.py status
python3 .codex/context_maintainer/cli.py status --json
python3 .codex/context_maintainer/cli.py drain --once
python3 .codex/context_maintainer/cli.py drain
python3 -m unittest discover -s .codex/context_maintainer/tests -p 'test_*.py' -v
```

`status`는 mode/workspace, last enqueued/drained, queue count와 oldest age, missing pair, gap, malformed, duplicate, failure를 보여준다. Raw prompt와 assistant message는 출력하지 않는다.

## Observe proof ceiling

이 first slice는 한 repo worktree에 하나의 global FIFO와 cursor를 둔다. 따라서 어느 Codex session이든 먼저 예약한 sequence의 Stop이 영구히 누락되면 다른 session의 뒤 event도 drain되지 않는다. Status는 gap과 missing pair를 숨기지 않고 `queue_scope: repo_worktree_global`, `cross_session_gap_isolation: false`, `manual_gap_recovery: false`를 보고한다.

현재 CLI에는 gap skip·drop·수동 repair가 없다. Raw event를 보존한 채 거짓 cursor 전진을 막는 것이 observe 단계의 우선순위다. 여러 session을 동시에 무인 운영하거나 Context write mode로 확대하기 전에 queue/cursor를 session lifetime별로 격리하고 recovery 계약을 추가해야 한다.

후속 점검에서는 Git fingerprint 실패 오표시, queue publish와 ledger 갱신 사이 crash의 content 무결성, 잘못된 `next_sequence` 타입에서의 status crash, 대화-only event의 전체 repository Git scan도 확인됐다. 28개 unit test는 이 경로를 검출하지 못한다. 이 패키지는 Reference canonical이나 운영 acceptance가 아니라 결함을 포함한 Workspace 005 실험 기준선이며, 상세 정정과 다음 구현 계획은 [Workspace 005 record 08](../../context/workspaces/005-context-continuity-maintenance/records/2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md)를 따른다.
