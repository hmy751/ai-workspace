# Work Handoff: Reference Maintain clean-room 재구현

- transfer-status: prepared
- prepared-at: `2026-08-18T23:08:35+09:00`
- sender: current main agent
- intended-receiver: same-repository fresh agent in a new task
- workspace: 이 repository root에서 `context/workspaces/007-maintain-clean-room-reimplementation/`로 진입
- revision: 1

## 1. Purpose and done criteria

Workspace 005에서 합의한 Maintainer 경험을 글로벌 AI-system 책임 기준에서 다시 도출해 `reference-project/`에 구현한다. Workspace 005 final runtime이나 Workspace 006 diff를 축소·수정하는 작업이 아니다.

완료 조건은 다음과 같다.

- Bounded initial grounding, same-session warm understanding, every response-end check, no-change no-write/report, quiet/important/ambiguous 구분, Main 비차단과 false freshness 방지가 구조 독립적 acceptance와 연결돼 있다.
- 모델 판단, deterministic guard와 사람 권한의 배치 이유가 드러난다.
- 재사용 가능한 계약·구현·검증이 Reference의 책임 경계에서 함께 발견된다.
- Unit·filesystem proof와 actual host·semantic acceptance를 구분하고 실제 host 장면을 확인한다.
- Root는 acceptance 뒤 선택된 Reference를 부르는 얇은 연결만 가지며 semantic 구현을 복제하지 않는다.

## 2. Current state and last verified point

- verified: Workspace 006 중단 문서는 commit `0952b1d`에 보존됐다.
- verified: `9553d0a`의 live implementation·execution contract 45개 경로는 parent `2649e9b` 상태로 복원됐고 commit `b508d80`에 고정됐다.
- verified: Root automatic hooks와 Maintain agent·Workspace binding은 비활성이고 old Observe package는 복원되지 않았다.
- verified: 45개 manifest와 parent diff 없음, root JSON·TOML parse, `git diff --check`, Reference 전체 test 최종 `53/53` 통과.
- reported: Workspace 005 record 09의 Maintain `165/165`, Reference `223/223`와 006 중단 시점 `207/207`, `265/265`는 해당 역사적 구현의 기록이다. Receiver의 새 baseline 검증으로 재사용하지 않는다.
- unknown: 새 implementation topology, 실제 host response-end signal, warm continuity mechanism, UI 보고·질문 전달과 semantic update 품질.
- last verified point: `2026-08-18T23:12:26+09:00`, reset commit `b508d80`의 exact path 비교와 전체 Reference test 재실행 결과 `53/53`.

## 3. Sources of truth and artifacts

- project instructions: repository root `AGENTS.md`, `context/README.md`, `context/workspaces/README.md`, 이 Workspace `README.md`
- branch and HEAD: prepare 시 `main` at `b508d80`; 이 packet과 007 문서를 담는 후속 commit은 documentation/setup only이며 receiver는 현재 `git log -3`로 확인한다.
- dirty state: prepare 시 007 문서와 root active pointer가 tracked 변경으로 남아 있고 setup commit으로 묶을 예정이다. 사용자 소유 untracked `.DS_Store`는 계속 제외한다. Receiver가 시작할 때 기대 상태는 tracked-clean + `.DS_Store` only다.
- primary artifacts: [`current/memory.md`](../current/memory.md), [`current/state.md`](../current/state.md), [`behavior contract`](2026-08-18-01-clean-room-source-and-behavior-contract.md), [`reset baseline`](2026-08-18-02-code-reset-baseline-and-excluded-topologies.md), [`output/index.md`](../output/index.md)
- supporting evidence: [005 records 02–09](../../005-context-continuity-maintenance/records/), [006 self-check](../../006-maintain-behavior-responsibility-allocation/records/2026-08-18-03-self-check-and-purpose-first-reset.md), [006 clean-room decision](../../006-maintain-behavior-responsibility-allocation/records/2026-08-18-05-clean-room-restart-decision.md), commits `2649e9b`, `9553d0a`, `0952b1d`, `b508d80`

## 4. Decisions and rationale

- decision: Preserve Workspace 005 behavior, not Workspace 005 or 006 topology.
  rationale: 기존 구현을 개선 대상으로 고정하면 그 내부 상태를 위한 migration·compatibility·recovery가 다시 설계를 지배했다.
  evidence: [006 self-check](../../006-maintain-behavior-responsibility-allocation/records/2026-08-18-03-self-check-and-purpose-first-reset.md), [clean-room decision](../../006-maintain-behavior-responsibility-allocation/records/2026-08-18-05-clean-room-restart-decision.md)
- decision: Derive the whole behavior and responsibility allocation before selecting files or runtime state.
  rationale: 글로벌 behavior-responsibility reference는 구현 전에 해석·보장·권한·실행 책임과 더 단순한 보장 수단을 비교하게 한다.
  evidence: [`behavior contract`](2026-08-18-01-clean-room-source-and-behavior-contract.md), root `AGENTS.md` Shared reference routing
- decision: Reusable Maintain belongs in Reference; root remains inactive and thin.
  rationale: root-only Observe는 재사용 책임을 잘못 소유했고 live smoke에서 delivery가 실패했다. Adapter가 사라져도 Workspace 의미가 남아야 한다.
  evidence: [005 record 06](../../005-context-continuity-maintenance/records/2026-08-17-06-response-end-observe-runtime-and-live-smoke.md), [005 record 07](../../005-context-continuity-maintenance/records/2026-08-17-07-reference-ownership-correction-and-handoff.md), global responsibility cohesion·rippability references
- decision: Keep automatic Maintain disabled until actual host acceptance.
  rationale: unit·fake-process proof는 host delivery, warm continuity와 UI/semantic 품질을 증명하지 않는다.
  evidence: [`reset baseline`](2026-08-18-02-code-reset-baseline-and-excluded-topologies.md), [005 record 09 proof ceiling](../../005-context-continuity-maintenance/records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md)

## 5. Attempts ledger

### Succeeded

- 006의 self-check, stopped implementation과 clean-room 결정을 historical records로 보존했다.
- 005 final implementation의 exact live path를 parent로 복원하되 005·006 문서와 Git history를 보존했다.
- Parent Observe를 되살리지 않고 root hook·agent를 명시적으로 inactive 상태로 만들었다.
- 삭제된 Maintain module의 ignored bytecode cache를 exact directory 범위에서 제거했다.
- 최종 baseline에서 Reference test `53/53`, config parse와 diff 검사를 통과했다.
- 007에 직접 사용자 근거, 여섯 행동 장면, 책임 배치, reset manifest와 output gate를 구성했다.

### Failed

- Workspace 005 root Observe: actual host 종료 때 async Stop이 취소되고 repo-global FIFO gap이 생겼다. Unit protocol 수정을 반복하는 조건으로 retry하지 않는다.
- Workspace 005 final runtime: local test coverage는 넓었지만 recovery topology가 커졌고 actual warm resume·background·UI·semantic 품질은 미증명으로 남았다.
- Workspace 006 in-place improvement: completed-pair와 Workspace attention으로 일부 surface를 바꿨지만 migration·compatibility·delivery state가 다시 생겼다. 이 diff를 이어 고치지 않는다.
- Reset 뒤 첫 Reference test: Verify timeout timing test 1개가 한 번 실패했다. 단독과 전체 재실행은 통과했으며 reset path는 parent와 exact했다. 관련 process code를 다시 바꾸면 재확인한다.

### Not tried

- 새 behavior-to-acceptance matrix와 최소 vertical slice 설계
- 새 Maintain production code 또는 test 작성
- 실제 nested Codex, fresh hook trust, warm session, UI notice·question acceptance
- Root automatic hook·agent 재연결
- External push, deployment 또는 다른 Project 적용

## 6. Ownership and authority transferred

- receiver now owns: Workspace 007의 current·records·output, 새 Reference Maintain 구조·구현·검증과 proof ceiling 관리
- receiver may: 이 repository 안에서 007 source를 읽고 acceptance matrix를 작성하며, 근거가 연결된 최소 Reference vertical slice를 구현·검증하고 사용자 승인 범위에서 commit할 수 있다.
- receiver may not: 005·006 history 재작성, 006 diff 복원, global reference 수정, `.DS_Store` 변경, ignored historical Observe state 삭제·새 완료 상태로 재해석, history rewrite, external push·deployment, actual nested Codex 실행이나 root hook 활성화를 추가 승인·acceptance 없이 수행할 수 없다.
- completion reporting target: 사용자에게 관찰된 결과·검증 상한·남은 결정을 보고하고, 같은 내용을 007 `current/state.md`와 `output/index.md`에 반영

## 7. Open questions, approvals, and blockers

- Blocker는 없다. 첫 acceptance matrix와 구조 제안은 현재 source만으로 가능하다.
- Actual host의 response-end signal과 warm continuity mechanism은 조사·spike 뒤 선택해야 한다.
- Actual nested Codex 또는 fresh host acceptance가 외부 실행 권한을 요구하면 실행 전에 사용자에게 승인 범위를 확인한다.
- Root activation은 새 implementation의 actual acceptance 뒤 별도 결정이다.

## 8. External side effects

- already caused: local Git commits `0952b1d`, `b508d80`; live code와 root local automation state가 reset·inactive로 바뀜
- irreversible or costly actions: 없음. Git history는 보존됐고 reset은 새 commit으로 남았다.
- pending external actions: push, deployment, 다른 Project 적용, external message 모두 없음

## 9. Next atomic action

- action: 여섯 behavior scene을 `입력 → 모델 판단 → deterministic guard → 사람 권한 → 관찰 결과 → 실패 상태 → 검증`으로 펼친 acceptance matrix와 가장 작은 첫 vertical slice를 하나의 새 design record로 작성한다.
- working directory or target: `context/workspaces/007-maintain-clean-room-reimplementation/records/`
- expected result: 과거 runtime state name 없이 각 scene의 책임과 관찰을 비교할 수 있고, 첫 slice가 어떤 약속 하나를 end-to-end로 증명하는지 설명한다.
- stop condition: queue·ledger·intent·attention 같은 과거 topology를 이유 없이 전제하거나, actual host proof 전에 root activation을 요구하거나, 새 durable state가 어떤 사용자 장면을 지키는지 답하지 못하면 편집을 멈추고 사용자에게 판단 차이를 보고한다.

## 10. Do not repeat and recovery

- do not repeat: `git reset --hard`, `git revert 9553d0a`, 45개 manifest의 재복원, 006 code 복구, parent root Observe 활성화, `.DS_Store` stage·삭제, `.context-harness/runtime/context-maintainer/v1/`를 새 state로 해석하거나 승인 없이 지우는 일
- safe retry: 007 문서 재읽기, `git diff b508d80 -- <restored paths>` 비교, Reference 53-test suite와 JSON·TOML parse는 작업 상태를 바꾸지 않고 재실행 가능
- rollback or recovery: 006 docs는 `0952b1d`, reset baseline은 `b508d80`, 005 final implementation은 `9553d0a`, preimplementation content는 `2649e9b`에서 복구할 수 있다. 복구가 필요해도 broad reset 대신 exact path와 새 commit을 사용한다.

## 11. Verification receipt

- checked-at: `2026-08-18T23:16:28+09:00`
- check: exact 45-path parent diff, protected Workspace diff, old runtime absence, root JSON·TOML parse, `git diff --check`, Reference unittest discover, 73개 local Markdown link traversal, conversation context 없는 fresh-agent pre-commit rehearsal
- result: path/config/diff/link checks 통과, Reference 전체 최종 `53/53` 통과; 첫 test 실행의 timing failure는 attempts ledger에 보존. Fresh receiver는 목적·baseline·권한·첫 행동과 topology 비승계를 재현했지만 007이 아직 uncommitted라 `needs-input`으로 정확히 중단했다. Setup commit 뒤 다시 rehearsal한다.
- workspace before/after: before는 `b508d80` tracked-clean + user `.DS_Store`; after는 007 setup 문서와 active pointers만 tracked 변경 + 동일 `.DS_Store`. 검증 명령 자체는 파일을 바꾸지 않았다.
- not checked: setup commit 뒤의 fresh-agent handoff 재현, 새 implementation, actual Codex host와 semantic 품질.
