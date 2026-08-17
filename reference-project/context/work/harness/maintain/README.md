# Maintain

Maintain은 Main 작업 세션 동안 선택한 Workspace를 이해하고, 작업 중 생긴 durable 의미 변화를 기존 Context Owner에 반영하는 Harness 관리 책임이다. Context의 의미나 책임 Owner를 새로 정하지 않으며, [`Work context`](../../README.md), [`Workspace collection`](../../workspaces/README.md), 선택한 Workspace의 README가 소유한 경계를 적용한다.

Maintainer는 event를 저장하는 기계 장치가 아니라 세션의 대화와 작업을 함께 이해하는 agent다. 매 사용자 대상 Main 응답 종료는 그동안의 변화를 점검하는 Maintain 활동 시점이다. Hook, event 전달, queue, checkpoint, agent resume와 reporting은 이 책임 안에서 교체할 수 있는 runtime adapter이며 별도 사용자-facing 역할이 아니다.

현재 자동 경로는 이 디렉터리의 [`hook.py`](hook.py), [`controller.py`](controller.py), [`runtime.py`](runtime.py), [`runner.py`](runner.py), [`intent.py`](intent.py), [`writer.py`](writer.py), prompt와 decision schema가 함께 구현한다. [`workspace-context-maintainer.toml`](workspace-context-maintainer.toml)은 Project root [`.codex/config.toml`](../../../../.codex/config.toml)이 등록하는 수동 fallback agent다. 수동 fallback은 같은 의미 계약을 따르지만 자동 경로의 read-only semantic agent와 deterministic guarded writer 분리를 증명하지는 않는다.

## 세션 시작과 수명

Main 작업 세션마다 그 세션 전용 Maintainer 하나를 둔다.

기존 Workspace를 선택한 새 세션에서는 첫 작업 전에 다음 순서로 bounded grounding한다.

1. 대상 Workspace README와 `current/`의 index를 읽는다.
2. Index가 가리키는 현재 목표·제약·상태·다음 행동 중 이번 작업에 필요한 문서만 읽는다.
3. 과거 이유나 정확한 근거가 실제로 필요할 때만 관련 records 또는 Project canonical을 추가로 읽는다.
4. 목표, 현재 상태, 바로 다음 행동을 한 번 짧게 보여 Main과 사용자가 시작점을 확인할 수 있게 한다.

이 초기 grounding은 이해를 맞추기 위해 Main 시작을 잠시 기다리게 할 수 있다. 새 Workspace에는 미리 읽을 Context가 없으므로 Maintainer가 세션 대화를 따라가며 이해를 형성한다. Config에 안전한 소문자 `workspace_id`는 명시하되 대상 디렉터리가 아직 없어도 시작할 수 있다. Workspace README와 지원하는 구조의 current 목표·상태·output 사람용 진입점이 모두 regular file로 형성되기 전에는 unbound 상태로 유지하고 어떤 지속 write도 허용하지 않는다. 이 진입점이 Main과 사용자 대화에서 형성되면 같은 warm Maintainer가 bounded binding grounding을 한 뒤 기존 Owner 관리를 시작한다.

같은 conversation task·Workspace·worktree에서는 같은 Maintainer가 이미 얻은 이해를 유지한다. Main context가 compact됐다는 이유만으로 살아 있는 Maintainer를 초기화하거나 전체 history·records·repository를 다시 읽지 않는다. 새 작업 세션에서는 새 Maintainer가 외부 canonical과 실제 작업 상태에서 다시 grounding하며, 이전 Maintainer의 내부 기억을 세션 사이 durable truth로 사용하지 않는다.

## 응답 종료 활동과 Main 비차단

초기 grounding 뒤에는 매 사용자 대상 Main 응답 종료에서 직전 점검 이후의 대화·작업 delta만 판단한다. Maintainer의 점검·쓰기·복구가 Main 응답 전송이나 관련 없는 다음 작업을 기다리게 해서는 안 된다.

Maintainer는 Main이 매번 완성된 evidence 묶음을 포장해 주기를 기다리지 않는다. 세션에서 이미 이해한 사용자 결정과 작업 흐름을 이어 쓰고, 판단에 필요한 대상 Workspace 문서, 관련 Project canonical, 실제 diff·파일·Git 상태, test 또는 Verify 결과를 스스로 좁게 대조한다. 다른 Workspace, active index, 저장소 전체와 records 전체를 기본 탐색하지 않는다.

Runtime adapter가 필요한 대화나 근거를 전달하지 못했거나 processing gap이 생겼다면, 추측으로 이해를 메우지 않고 [실패와 복구](#실패와-복구) 기준을 적용한다.

## 현재 Codex 실행 연결

Project root의 `.codex/context-maintain.json`이 한 Workspace, Work root, 이 계약과 ignored runtime root를 명시한다. `.codex/hooks.json`은 다음 경계를 잇는다.

- `SessionStart`: 기존 Workspace 또는 forming 상태를 한 번 동기로 grounding하고 짧은 시작 상태를 Main context에 넣는다. Host 실행이 실패하면 Main이 직접 bounded grounding하도록 `additionalContext`를 반환한다.
- `UserPromptSubmit`: 사용자 발화를 session·turn identity에 연결하고, 이전 background 결과 중 사용자에게 보여야 할 항목만 bounded notice로 전달한 뒤 worker를 시작한다.
- `PostToolUse`: raw input·output을 보존하지 않고 allowlisted 변경 경로, 명시 path, 안전하게 분류한 test·Git 결과와 hash만 turn evidence로 보강한다. 이 hook만으로 semantic worker를 시작하지 않는다.
- `Stop`: Main 응답을 같은 turn과 pair한 뒤 detached worker를 시작한다. 동기 구간은 durable capture까지만 기다리고 semantic 판단과 write를 기다리지 않는다.

Runtime은 Workspace와 Main session별 namespace, immutable response event, FIFO checkpoint, pending report, process lease와 content-free status를 소유한다. 완성된 response pair가 없는 마지막 capture residue는 원자료를 보존하되 다음 session을 막지 않는다. UserPrompt 하나만 Stop을 기다리는 경우는 정상적인 미완료 응답일 수 있어 조용히 넘기고, Stop만 있거나 tool evidence가 홀로 남은 경우와 혼합 residue는 전달 누락 가능성을 다음 safe point에서 content-free 경고한다. 이후 sequence가 존재해 실제 gap이 확정되면 조용히 건너뛰지 않고 freshness를 신뢰 불가로 표시한다. 이미 checkpoint에 포함된 completed event나 승인된 gap repair의 raw cleanup만 남은 경우에는 agent를 다시 부르지 않고 recovery worker가 그 residue만 idempotent하게 정리한다. V1 Observe 파일은 읽거나 완료 처리하지 않는다.

Worker 하나는 response event 하나만 처리한다. 다음 queue가 남거나 세 번 미만의 일시 실패가 있으면 가장 이른 안전한 session worker 하나를 다시 깨운다. 이전 session worker가 시작되지 않았거나 중간에 죽은 채 새 session이 열려도 새 session의 retry budget을 소모하지 않고 이전 queue를 먼저 복구한 뒤 다음 session을 깨운다. Processing 중인 worker, 확정 gap, malformed·conflict 또는 세 번 실패한 session은 자동 우회하거나 무한 재실행하지 않는다.

Semantic runner는 prompt를 command argument가 아니라 stdin으로 전달하고, 한 호출을 host의 120초 SessionStart 제한보다 짧은 90초로 끝낸다. 처음에는 bounded canonical grounding을 하고 이후에는 같은 local Codex thread id를 `codex exec resume`으로 이어 delta만 판단한다. Main compaction은 이 thread를 버리는 신호가 아니다.

Agent 결정은 바로 파일 권한이 되지 않는다. Decision intent를 event hash와 함께 먼저 durable하게 기록하고, writer가 allowlist·baseline hash·symlink·Markdown link를 검사한 뒤 전체 파일을 교체한다. Processor 호출 전과 결과 commit 직전에 queue와 exact ledger가 여전히 같은 conflict-free event인지 확인하므로, differing replay나 malformed ledger를 Context 반영·cursor 전진으로 잘못 완료하지 않는다. Cursor와 사용자 보고는 같은 event checkpoint에 함께 commit하며, 그 전 crash는 저장한 intent와 write journal로 같은 판단을 재실행 없이 완결한다. 기존 Markdown mode를 보존하고 새 Markdown은 `0644`로 만든다.

상태는 다음처럼 확인한다.

```bash
python3 context/work/harness/maintain/hook.py \
  --config .codex/context-maintain.json status
```

Higher sequence로 missing Stop gap이 확정된 경우에는 사용자 승인과 이유를 받아 exact session·sequence 하나만 복구한다.

```bash
python3 context/work/harness/maintain/hook.py \
  --config .codex/context-maintain.json repair-gap \
  --session-id <session-id> \
  --expected-sequence <sequence> \
  --approved-by <provenance-code> \
  --reason <reason-code>
```

Reference가 상위 repository의 하위 디렉터리에 있을 때는 실제 Project root에 맞는 hook path를 사용한다. 현재 실행 연결은 Python 3.10 이상과 POSIX file lock·shell을 사용하며 Windows 실행은 지원 범위가 아니다.

## 판단·쓰기·보고

각 활동 시점에는 다음 순서로 판단한다.

- Durable 변화가 없으면 아무것도 쓰지 않고 보고도 하지 않는다.
- 명확한 durable 변화는 아래 allowlist의 올바른 기존 Owner에 반영한다.
- 사소하고 명확한 반영은 조용히 처리한다.
- 사용자가 알아야 할 중요한 명확한 반영은 먼저 수정하고 결과만 짧게 보고한다.
- 의미, Owner, 장기성, 사용자 의도가 애매하면 추측해 쓰지 않고 즉시 질문한다. 해당 반영만 보류하고 관련 없는 Main 작업은 계속한다. 현재 방향을 바꿀 ambiguity일 때만 관련 Main 작업도 답을 기다린다.

`사소함`은 write 여부의 기준이 아니다. Write 여부는 durability로, 보고 여부는 사용자가 알아야 할 중요도로 판단한다. Semantic ambiguity는 runtime 실패가 아니므로 retry나 다음 세션으로 미루지 않는다.

## 읽기와 갱신 경계

변경이 필요한 의미만 다음 기존 Owner에 한 번 반영한다.

- `current/`: 지금도 유효하여 다음 행동에 필요한 목표·제약·현재 상태·불확실성·cursor를 해당 memory 또는 state 문서에 둔다. 끝난 과정과 상세 증거를 누적하지 않는다.
- `records/`: 이후 다시 판단할 가치가 있는 분석·결정·실패·검증 해석을 사람이 읽는 날짜별 기록으로 남긴다. Verify receipt를 만들거나 고치지 않는다.
- `source/`의 provenance와 index: 선택한 원자료의 범위·출처·시점·무결성·재접근 경로만 갱신한다. 보존한 raw snapshot의 본문은 절대 다시 쓰지 않는다.
- `output/index.md`: 현재 goal을 위해 선택된 산출물과 실제 canonical 위치만 연결한다. 산출물을 복제하거나 선택을 acceptance로 해석하지 않는다.

모든 층을 매번 수정하지 않는다. 같은 사실을 여러 층에 반복하지 않고 상세 근거는 records나 실제 canonical을 연결한다. 각 층의 세부 의미와 내부 관계는 [`Workspace collection`](../../workspaces/README.md)과 선택한 Workspace README에서 확인한다.

## 실패와 복구

일시적 runtime 실패, 처리 지연 또는 Maintainer restart가 생기면 실행 연결은 먼저 retry·replay·rebootstrap으로 이해와 processing 위치를 복구해야 한다. 복구 중에는 completed 또는 fresh 상태를 가장하지 않는다.

자동 복구 뒤에도 외부 canonical과 실제 작업 상태를 대조해 신뢰할 수 있는 freshness를 다시 세울 수 없을 때만 사용자에게 짧게 경고하고 필요한 부분을 묻는다. 현재 구현은 ordinary processor failure를 같은 event에서 세 번까지 조용히 replay하고, 세 번째 실패나 content conflict·malformed checkpoint·확정된 sequence gap처럼 구조적 신뢰가 깨진 경우에만 warning을 올린다. Queue, checkpoint, lease, journal과 경고 채널은 이 의미를 수행하는 교체 가능한 장치이며 Workspace의 durable truth가 아니다.

## 소유하지 않는 것

Maintain은 다음을 수행하거나 결정하지 않는다.

- Project 제품 코드·제품 문서·제품 test 수정
- `workspace.json`, `recover.json`, `verify.json` 같은 machine 실행 계약 변경
- Verify receipt 또는 `current/state/status.json` 생성·수정·삭제
- `workspaces/index.json`의 active 선택·변경
- 사용자 대신 목표·source 권위·설계 기준·acceptance·완료를 결정하는 일
- 파일 stage, commit, push 또는 외부 쓰기

새 Workspace의 생성·선택 자체는 Maintainer가 추측하지 않는다. 세션에서 identity·goal·Owner가 형성되고 대상이 명확해진 뒤 위 allowlist의 지속 관리를 시작한다. 허용 범위 밖의 변경이 필요해 보이면 그 필요와 근거만 사용자 또는 main에 올린다.

## 결과와 검토

Maintainer의 결과는 매번 정해진 status message로 노출하지 않는다. No-change와 사소한 명확 반영은 조용히 끝내고, 중요한 반영·ambiguity·복구 불가능한 freshness에만 [판단·쓰기·보고](#판단쓰기보고)와 [실패와 복구](#실패와-복구) 기준으로 짧게 알린다.

Background worker는 새 UI turn을 스스로 만들 수 없다. 중요한 반영과 ambiguity가 response-end 뒤에 확정되면 다음 `UserPromptSubmit` safe point에서 Main context에 넣고, Main은 관련 write나 방향 진행 전에 바로 보여 주거나 질문한다. Pending notice는 개수와 전체 길이를 제한하고 실제 출력한 report만 stdout flush 뒤 acknowledge한다.

변경이 생기면 실제 수정 파일과 근거가 나중에 대조 가능해야 한다. Main은 사용자 결정, 실제 evidence와 diff를 검토하되 이 검토가 매 응답의 선행 병목이 되게 하지 않는다. Agent 보고나 정적 설정 검사는 acceptance가 아니며, 작성 내용의 충분성도 자동으로 증명하지 않는다.

## 교체와 제거

Maintain의 지속 기준과 Workspace의 의미는 runtime 구현이나 agent 내부 기억에 있지 않다. 실행 연결을 제거하거나 다른 사람·AI·도구로 교체해도 이 README에서 시작해 Work·Workspace canonical을 적용하면 같은 책임을 수행할 수 있다. 따라서 실행 연결 교체를 위해 Context 구조나 각 Workspace의 의미를 다시 만들 필요가 없다.

Runtime 구현은 이 `maintain/` 책임 아래에서 계약·설정·코드·검증과 함께 발견되어야 한다. Project root 설정에는 발견에 필요한 얇은 연결만 두고, 다른 Project에서 같은 구현을 복제하지 않는다.

Repo-local queue의 raw 사용자·assistant text는 checkpoint 성공 전 replay를 위해 보존하고 성공 뒤 삭제한다. Tool raw input·output은 저장하지 않는다. Decision intent와 staged Markdown은 commit 또는 명시적 복구가 끝날 때까지 ignored runtime에 남는다. Warm continuity를 위해 만든 Codex thread는 Codex의 local session store에 지속되며, prompt와 response delta가 그 thread 기록에 포함될 수 있다. Maintain은 이 host-owned 기록을 자동 삭제하지 않고 새 Main session에서 재사용하지도 않는다. 따라서 “raw cleanup” 증거는 repo-local runtime에만 적용되며 Codex 자체 보존 정책까지 뜻하지 않는다.

자동 실행 연결을 제거할 때 Project root의 Maintain hook/config/agent 연결과 ignored runtime을 함께 제거할 수 있다. 그러더라도 Workspace README, current, source, output, records의 의미와 수동 Maintain 책임은 그대로 남는다.

현재 unit·filesystem integration은 pairing, session 격리, warm resume command, forming→binding, guarded multi-owner write, crash replay, 이전 worker recovery, gap·lease·malformed state와 reporting을 fake process로 검증한다. 실제 Codex host의 hook trust, 별도 Codex session, background process kill, UI/model context 전달을 연결한 fresh-task acceptance는 별도 실행 전까지 증명되지 않는다. Writer의 target baseline은 stale overwrite를 막지만, 전달 evidence가 전혀 없는 외부 branch·worktree 전환과 conversation-only `no_change` 판단을 자동 fingerprint로 검출하는 동작도 이번 검증 범위가 아니다.
