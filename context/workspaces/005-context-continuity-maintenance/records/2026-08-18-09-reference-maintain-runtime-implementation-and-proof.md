# Reference 세션형 Maintain runtime 구현과 현재 proof

날짜: `2026-08-18`

## Trigger와 현재 결과

[세션형 Maintainer 동작과 Reference 구현 계획](2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md)을 코드와 Project 운영 계약으로 옮겼다. 이번 구현의 목표는 이전 root Observe queue를 다른 위치에 복사하는 것이 아니었다. 같은 작업 세션에서 이미 이해한 Maintainer가 그 이해를 유지하고, 매 Main response-end의 의미 변화만 background에서 판단해 기존 Context Owner를 신뢰 가능하게 유지하는 전체 동작을 Reference가 재사용 가능하게 소유하게 하는 것이었다.

현재 결과는 다음과 같다.

- `reference-project/`가 Maintain의 사람용 계약, semantic warm session, delivery·recovery runtime, guarded writer와 test를 소유한다.
- Verify는 제품 검증 실행기에서 이미 수행된 test·eval·수동 확인의 evidence recorder로 축소됐다.
- Root는 Workspace 005를 고르는 설정과 Reference hook·fallback agent를 발견하는 연결만 소유한다.
- 이전 root `.codex/context_maintainer/` Observe runtime과 전용 agent는 active 경로에서 제거했다. Records 06–08과 Git 이력은 당시 실험·실패 근거로 보존한다.
- Cross-session recovery wake와 incomplete capture residue의 비차단·선별 경고까지 구현했고 로컬 통합 재검증을 마쳤다. 실제 Codex host acceptance는 아래 proof ceiling로 분리한다.

## 보존한 사용자-facing 동작

### 처음에는 이해를 맞추고, 이후에는 이미 아는 상태를 쓴다

기존 Workspace의 새 Main 세션에서는 Maintainer가 Workspace README와 current index에서 필요한 current만 골라 bounded grounding한다. Records 전체나 repository 전체를 미리 읽지 않는다. 목표·현재 상태·다음 행동을 한 번 짧게 보여 준 뒤에는 같은 task·Workspace·worktree 동안 local Maintainer thread를 이어 쓴다.

따라서 두 번째 응답부터의 속도는 단순히 hook timeout을 줄여서 얻는 것이 아니다. 같은 agent가 대화와 작업을 따라가며 이미 얻은 이해를 재사용하고, 직전 완료 cursor 이후의 delta와 관련 evidence만 좁게 확인하는 데서 나온다. Main context compaction은 이 warm thread를 버리는 조건이 아니며, 새 Main 작업 세션은 이전 agent 기억이 아니라 외부 canonical에서 새로 grounding한다.

새 Workspace는 다른 동작을 한다. 안전한 identity binding은 둘 수 있지만 Workspace README, current와 output의 사람용 entrypoint가 생겨 identity·goal·Owner가 드러나기 전에는 persistent write를 금지한다. Maintainer는 대화를 따라 이해할 수 있지만 그 이해만으로 지속 구조를 추측해 만들 수 없다.

### Response-end는 Maintain 내부의 활동 시점이다

`SessionStart`는 처음 이해를 맞추는 bounded 동기 구간이다. `UserPromptSubmit`은 사용자 발화와 이전 background notice를 안전하게 전달하고, `PostToolUse`는 raw tool input·output 대신 관련 변경 path와 분류된 test·Git 결과 같은 좁은 evidence만 보강한다. `Stop`은 Main 응답을 같은 turn과 pair해 durable response event를 만든 뒤 detached worker를 시작한다.

Hook·queue·checkpoint는 별도 사용자-facing `Observe` 역할이 아니다. Maintainer가 매 response-end에 실제로 활동하게 만드는 Maintain 내부 실행 장치다. 동기 hook은 전달 자료를 안전하게 남길 때까지만 기다리고, semantic 판단·Context write·복구는 초기 grounding 뒤 Main 응답과 관련 없는 다음 작업을 막지 않는다.

### 판단과 보고는 네 장면을 구별한다

- Durable 변화가 없으면 write와 보고가 모두 없다.
- 사소하지만 명확한 durable 변화는 올바른 기존 Owner에 반영하고 조용히 끝낸다.
- 사용자가 알아야 할 중요한 명확 변화는 먼저 반영하고 짧게 결과를 보고한다.
- 의미·Owner·장기성·사용자 의도가 애매하면 해당 write 전에 질문하고, 관련 없는 Main 작업은 계속한다.

Background worker는 스스로 새 UI turn을 만들 수 없다. 중요한 반영과 질문은 다음 `UserPromptSubmit` safe point에서 길이·개수를 제한해 Main context에 전달한다. 화면에 한 번 보여 줬다는 사실과 질문이 해결됐다는 의미를 분리했다. `needs_decision`은 다른 세션에도 unresolved 상태로 이어지고, 뒤 response-end evidence가 그 exact 질문을 실제로 답하거나 대체했다고 semantic agent가 지정할 때만 제거한다.

## 소유권과 실제 배치

Reference의 `context/work/harness/maintain/` 안에는 의미 계약과 다음 실행 책임이 함께 있다.

- Host event를 받아 bounded capture와 detached worker를 연결하는 hook
- Initial grounding과 warm thread resume, response-end 판단, report reconciliation을 조율하는 controller
- Session event·checkpoint·freshness·report·gap repair를 durable하게 관리하는 runtime
- Read-only semantic agent의 decision을 엄격히 parse하는 prompt·schema·intent 경계
- 허용된 Workspace Markdown Owner만 deterministic하게 바꾸는 shared guarded writer
- 자동 hook이 없을 때 같은 의미 계약을 수행하는 수동 fallback agent

Root `.codex`에는 Workspace 005와 Work root, Reference contract path와 ignored runtime root를 고르는 값, Reference `hook.py`를 부르는 host 설정, fallback agent 발견 연결만 남겼다. 이 연결을 제거해도 Workspace README·current·source·output·records의 의미와 수동 Maintain 책임은 남는다. Global `ai-system_*` reference는 이 책임 응집, 사람용 진입과 제거 가능성을 점검하는 감사 기준으로만 사용했으며 global 파일은 바꾸지 않았다.

## Recovery invariant

이번 runtime은 성공 경로보다 “중간에 죽어도 무엇을 완료로 믿을 수 있는가”를 먼저 고정했다.

1. User capture와 대응하는 Stop이 pair되면 session별 immutable response event를 만든다. No-change도 처리 완료 cursor를 전진하지만, processor 실패나 손상은 완료로 기록하지 않는다. Processor 호출 전과 결과 commit 직전에 queue와 exact ledger가 여전히 같은 conflict-free event인지 다시 확인하므로 differing replay·malformed ledger는 cursor와 raw를 보존한 채 차단한다.
2. 한 processor call은 response event 하나만 처리한다. 남은 queue에는 successor worker가 필요하며, capture와 worker의 terminal unlock이 겹쳐도 durable queue generation을 다시 확인해 wake를 놓치지 않아야 한다. 이전 worker가 시작되지 않았거나 죽은 뒤 새 session이 열리면 가장 이른 안전한 queue를 먼저 깨우고, 그 완료 뒤 다음 session worker를 다시 깨운다.
3. Queue·checkpoint는 session별로 격리한다. 새 session은 시간상 자신보다 앞선 session의 freshness와 pending report만 확인한다. 나중 session 때문에 과거 session이 역으로 대기하는 대칭 deadlock은 허용하지 않는다.
4. 이전 session이 processing·retry 중이면 새 session은 stale Context를 fresh로 가장해 write하지 않는다. 이 대기는 새 session의 processor 실패 횟수를 소모하지 않는다. 완성된 response pair 없이 끝난 마지막 capture residue는 원자료를 보존하되 다음 session을 막지 않는다. UserPrompt 하나가 자기 Stop을 기다리는 정상 미완료 tail은 조용히 넘기지만, Stop-only·tool-evidence-only·혼합 residue는 전달 누락 가능성을 다음 safe point에서 content-free 경고한다.
5. Processor error는 같은 event를 먼저 조용히 replay하고, malformed state, content conflict, 확정된 gap 또는 반복 실패처럼 외부 canonical과 cursor의 신뢰를 자동 복구하지 못할 때만 짧게 경고한다.
6. Semantic decision은 event identity·content hash와 함께 durable intent가 된 뒤 writer에 들어간다. Agent는 직접 파일 권한을 갖지 않는다.
7. Writer lock·journal·stage·completion marker는 Main session별이 아니라 Workspace 전체가 공유한다. 따라서 서로 다른 session이 같은 Owner를 동시에 바꾸거나 오래된 baseline으로 나중 write를 덮어쓰지 못한다.
8. Multi-file replace 뒤 checkpoint 전 crash가 나도 exact transaction marker로 이미 적용된 write를 다시 의미 판단하지 않고 이어 간다. Checkpoint 뒤 cleanup 전 crash도 exact intent·marker를 reconcile한다. Completed event나 승인된 gap repair의 checkpoint 뒤 raw cleanup만 남은 경우에도 status가 이를 fresh로 숨기지 않고 recovery worker가 agent 재호출 없이 exact residue만 idempotent하게 정리한다. 다른 session의 별도 damaged journal이 있어도 이미 완료된 exact transaction의 acknowledgement는 막히지 않는다.
9. 판단 중 target baseline이 바뀌면 옛 intent를 영구 retry하지 않는다. 그 intent를 버리고 warm grounding을 invalidation한 뒤 최신 canonical에서 다시 이해하고 판단한다.
10. Important report는 stdout 전달 뒤에만 acknowledge한다. `updated_report`는 전달 뒤 끝나지만 `needs_decision`은 recipient별 전달 여부만 남기고 semantic resolution 전까지 보존한다.

누락 Stop은 higher sequence가 존재해 실제 gap으로 확정돼도 자동 skip하지 않는다. 사용자 승인을 받은 exact gap만 session id, expected sequence와 bounded provenance를 남겨 repair한다.

```bash
python3 reference-project/context/work/harness/maintain/hook.py \
  --config .codex/context-maintain.json \
  repair-gap \
  --session-id <main-session-id> \
  --expected-sequence <sequence> \
  --approved-by <lowercase-provenance-code> \
  --reason <lowercase-provenance-code>
```

이 명령은 일반 재시도 수단이 아니라, 자동 복구할 수 없는 exact missing-Stop abandonment를 사람이 승인했다는 provenance를 남기는 마지막 복구 경계다.

## 축소 Verify와 Recover 호환

새 Verify는 다음 사실만 입력받아 `records/receipts/verify/evidence-*.json`에 append-only로 기록한다.

- 누가 언제 무엇을 확인했는가
- 실제로 사용한 test·eval·수동 확인 방법은 무엇인가
- 생산자가 보고한 결과가 `pass`, `fail`, `partial` 중 무엇인가
- 원래 결과로 돌아갈 위치와 여전히 확인하지 않은 범위는 무엇인가

Verify는 제품 명령을 실행하지 않고 source reference를 열어 진위를 재판정하지 않는다. `pass` evidence를 기록한 exit `0`도 evidence 저장 성공일 뿐 제품 충분성, Workspace 완료나 사람 acceptance가 아니다. `verify.json`, legacy `verify-*.json`, `current/state/status.json`과 `recover.json`을 읽거나 수정하지 않는다.

과거 제품 Verify artifact는 migration하지 않았다. Recover는 status가 연결한 legacy receipt를 기존 규칙으로 계속 읽고, 새 evidence receipt를 제품 검증 cursor로 자동 선택하지 않는다. `apply-context-harness`도 이 경계를 따라 target의 기존 canonical·사용자 변경과 legacy artifact를 보존하고, Maintain hook·Verify recorder를 실제 target에 맞춰 배치하도록 갱신했다.

## 현재 검증과 proof ceiling

Fake Codex process와 임시 filesystem을 사용한 Maintain test `165/165`은 response pairing, session 격리, bounded grounding·warm resume command, forming→binding, no-change와 report·ambiguity, shared multi-owner write, stale baseline, crash replay, response replay conflict 차단, checkpoint-covered raw cleanup, 이전 worker recovery, incomplete capture residue의 비차단·선별 경고, gap·lease·malformed state를 다룬다. Verify·Recover·validation을 포함한 Reference 전체 test는 `223/223`, apply skill helper는 `7/7` 통과했다. Python compile, JSON 5개·TOML 4개 parse, root·Reference hook의 shell command 8개 문법과 동기 실행 조건, 두 status 진입도 확인했다.

다음은 아직 증명하지 않았다.

- 실제 nested `codex exec`가 선택한 Workspace를 읽고 별도 local thread를 만들며 이후 `resume`하는 동작
- Fresh Codex host가 새 hook을 신뢰·호출하고 SessionStart grounding을 Main context에 넣는 장면
- 실제 host process 종료·restart·Main compaction을 거친 background 비차단과 cross-session recovery
- Pending 중요 보고와 ambiguity가 실제 UI에서 짧게 보이고 사용자의 뒤 응답으로 해소되는 장면
- Semantic agent가 실제 Workspace 문서를 충분하고 정확하게 갱신하는 품질
- 전달 evidence 없이 외부에서 바뀐 branch·worktree와 그 상태에서의 conversation-only `no_change`를 자동 fingerprint로 감지하는 동작

실제 nested Codex 실행은 선택한 fixture Context와 response delta를 별도 Codex session으로 보내는 외부 실행 경계다. 사용자 승인이 없으면 정적·fake-process proof ceiling을 유지하고 live acceptance를 주장하지 않는다. Root의 untracked `.DS_Store`도 이번 구현·검증·commit 범위가 아니다.

## 다음 커서

이번 승인 범위의 Reference 구현, root 연결 설정, Workspace 005 문서는 한 변경 묶음으로 보존하고 push하지 않는다. 필수 구현 커서는 닫혔으며, 실제 nested Codex와 fresh hook acceptance는 외부 실행을 별도로 승인받은 뒤 임시 Reference fixture에서 proof ceiling을 좁히는 후속 검증으로 남긴다.
