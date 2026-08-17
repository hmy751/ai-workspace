# Context continuity maintenance state

마지막 갱신: `2026-08-18`

## 현재 상태

Workspace 005에서 확정한 세션형 Maintain·축소 Verify 운영은 Reference-first 구조로 구현·재검증됐고 이번 변경 묶음으로 보존됐다. Cross-session에서 이전 worker가 시작되지 않거나 죽어도 가장 이른 queue를 복구하고 다음 session을 다시 깨우며, replay conflict와 checkpoint 뒤 raw cleanup도 false success 없이 복구한다. 현재 승인 범위에 남은 필수 구현은 없다.

## 구현된 현재 구조

- `reference-project/context/work/harness/maintain/`이 세션형 Maintain의 사람용 계약, hook controller, session runtime, warm Codex runner, decision schema·intent와 guarded writer, 수동 fallback agent 및 test를 함께 소유한다.
- Root `.codex/context-maintain.json`, `.codex/hooks.json`, `.codex/config.toml`과 agent config는 Workspace 005를 Reference runtime에 연결하는 얇은 설정이다. Root에 semantic prompt·writer·queue 코드를 복제하지 않는다.
- 이전 `.codex/context_maintainer/` Observe 구현과 그 전용 agent는 active 경로에서 제거했다. 당시 실패와 결함은 records 06–08과 Git 이력에 남긴다.
- 기존 Workspace의 `SessionStart`는 bounded initial grounding과 한 번의 짧은 시작 상태를 동기로 제공한다. 이후 `UserPromptSubmit`·`PostToolUse`·`Stop`은 bounded capture만 하고 response-end semantic 판단과 write는 detached worker가 수행한다.
- 같은 task·Workspace·worktree에서는 local Codex thread id를 저장해 warm resume한다. 잘못된 state, runner failure나 stale target은 외부 canonical에서 rebootstrap·re-grounding한다.
- Forming Workspace는 identity만 설정할 수 있지만 `README.md`, current와 output의 사람용 entrypoint가 생기기 전에는 semantic write를 금지한다.
- Decision은 `no_change`, 조용한 반영, 보고할 반영, `needs_decision`을 구분한다. 중요 보고와 ambiguity는 다음 safe hook에서 bounded 전달하고, ambiguity는 전달과 의미적 resolution을 분리한다.
- Session별 immutable response event와 checkpoint는 processing 순서를 보존한다. Workspace 수준 freshness·pending report 조회는 시간상 이전 session만 고려해 새 session handoff를 막거나 역방향 deadlock을 만들지 않게 한다.
- Writer는 Workspace 전체에서 하나의 lock·journal·completion namespace를 공유한다. Baseline hash, allowlist와 path·symlink·Markdown link 방어 뒤 multi-file replace를 수행하고, exact transaction marker로 crash 뒤 중복 판단과 lost update를 막는다.
- 누락 Stop gap은 자동 skip하지 않는다. 실제 higher sequence로 gap이 확정되고 사용자가 승인했을 때만 다음처럼 exact session·sequence·provenance로 repair한다.

```bash
python3 reference-project/context/work/harness/maintain/hook.py \
  --config .codex/context-maintain.json \
  repair-gap \
  --session-id <main-session-id> \
  --expected-sequence <sequence> \
  --approved-by <lowercase-provenance-code> \
  --reason <lowercase-provenance-code>
```

- `reference-project/context/work/harness/verify/`는 이미 수행된 test·eval·수동 확인의 evidence만 append-only로 기록한다. 제품 명령이나 machine status를 실행·전이하지 않고, legacy Verify receipt/status에 대한 Recover 읽기 호환을 보존한다.
- `apply-context-harness`는 target의 기존 canonical과 사용자 변경을 보존하면서 Maintain 실행 연결과 축소 Verify를 이식하고, live host를 실행하지 않은 범위를 acceptance로 주장하지 않도록 갱신했다.

## 남은 상태와 proof ceiling

- 이전 worker recovery, response replay conflict 차단, checkpoint-covered raw cleanup과 incomplete capture residue의 비차단·선별 경고를 포함한 Maintain test `165/165`, Reference 전체 test `223/223`, apply skill helper test `7/7`이 통과했다. Python compile, JSON·TOML parse, hook shell command 8개의 문법·동기 실행 조건과 root·Reference status 진입도 통과했다.
- 실제 nested `codex exec`와 같은 thread resume, fresh Codex host의 hook trust·SessionStart·background process·UI notice·semantic write 품질은 아직 live acceptance하지 않았다. 실행하려면 별도 Codex session에 선택한 fixture Context와 delta가 전달되는 외부 실행 경계를 승인받아야 한다.
- Writer baseline은 stale target overwrite를 막지만, 전달 evidence가 없는 외부 branch·worktree 전환과 conversation-only `no_change`를 자동 fingerprint로 판별하는 별도 장치는 이번 완료 범위에 넣지 않았다.
- Root `.DS_Store`는 이번 구현과 무관한 untracked 파일이다. Stage·commit에 포함하거나 되돌리지 않는다.

## 다음 행동

현재 승인 범위의 필수 후속 작업은 없다. 실제 nested `codex exec`와 fresh host acceptance는 사용자가 외부 실행을 별도로 승인할 때 임시 Reference fixture에서 proof ceiling을 좁히는 후속 검증으로 수행한다.
