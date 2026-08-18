# Code reset baseline과 과거 topology 근거

날짜: `2026-08-18`

상태: **실행·검증 완료**

## 결정과 commit 경계

기존 구현을 개선 대상으로 둔 채 단순화하면 그 구현이 만든 state·migration·compatibility를 계속 보존하게 된다는 사용자 정정에 따라, repository history를 rewrite하지 않고 live code만 구현 전 기준으로 복원했다.

- Workspace 005 최종 구현: `9553d0a85fe0c9187de1f5296033f1ee32d6aaf6` (`feat: implement session context maintenance`)
- 단일 부모와 새 code baseline: `2649e9bfaed79056e7117a33e716290ad19020c2`
- Workspace 006 중단 기록: `0952b1d` (`docs: record stopped maintain restructuring attempt`)
- Path-scoped code 복원과 root 비활성화: `b508d80` (`refactor: reset maintain implementation baseline`)

`git reset --hard`, `git revert 9553d0a`, repository 전체 restore는 사용하지 않았다. Workspace 005·006 문서와 후속 commit을 보존하면서 `9553d0a`가 변경한 live implementation·execution contract만 부모 상태로 맞췄다.

## 부모와 일치시킨 exact path manifest

다음 45개 경로를 `2649e9b`의 내용으로 복원했다. 현재 checkout에서 이 경로들에 대해 `git diff 2649e9b -- <paths>`는 차이가 없다.

```text
.agents/skills/apply-context-harness/SKILL.md
.agents/skills/apply-context-harness/references/application-contract.md
reference-project/.codex/context-maintain.json
reference-project/.codex/hooks.json
reference-project/.gitignore
reference-project/README.md
reference-project/context/work/AGENTS.md
reference-project/context/work/README.md
reference-project/context/work/harness/README.md
reference-project/context/work/harness/cli.py
reference-project/context/work/harness/maintain/README.md
reference-project/context/work/harness/maintain/__init__.py
reference-project/context/work/harness/maintain/config.py
reference-project/context/work/harness/maintain/controller.py
reference-project/context/work/harness/maintain/decision.schema.json
reference-project/context/work/harness/maintain/hook.py
reference-project/context/work/harness/maintain/intent.py
reference-project/context/work/harness/maintain/prompts.py
reference-project/context/work/harness/maintain/runner.py
reference-project/context/work/harness/maintain/runtime.py
reference-project/context/work/harness/maintain/tests/__init__.py
reference-project/context/work/harness/maintain/tests/test_config_forming.py
reference-project/context/work/harness/maintain/tests/test_controller.py
reference-project/context/work/harness/maintain/tests/test_hook.py
reference-project/context/work/harness/maintain/tests/test_prompts.py
reference-project/context/work/harness/maintain/tests/test_runner.py
reference-project/context/work/harness/maintain/tests/test_runtime.py
reference-project/context/work/harness/maintain/tests/test_writer.py
reference-project/context/work/harness/maintain/workspace-context-maintainer.toml
reference-project/context/work/harness/maintain/writer.py
reference-project/context/work/harness/recover/tests/test_recover.py
reference-project/context/work/harness/validation/README.md
reference-project/context/work/harness/validation/tests/test_ephemeral_workspace_state_preservation.py
reference-project/context/work/harness/verify/README.md
reference-project/context/work/harness/verify/__init__.py
reference-project/context/work/harness/verify/operation.py
reference-project/context/work/harness/verify/tests/test_verify.py
reference-project/context/work/workspaces/001-default-timeout/README.md
reference-project/context/work/workspaces/001-default-timeout/current/memory/01-goal.md
reference-project/context/work/workspaces/001-default-timeout/current/memory/02-constraints.md
reference-project/context/work/workspaces/001-default-timeout/current/state/index.md
reference-project/context/work/workspaces/001-default-timeout/output/index.md
reference-project/context/work/workspaces/001-default-timeout/records/README.md
reference-project/context/work/workspaces/001-default-timeout/records/receipts/README.md
reference-project/context/work/workspaces/README.md
```

Parent에 없던 005 final Maintain Python package와 test는 이 복원으로 삭제됐다. Workspace 006에서 새로 만든 untracked `attention.py`, `tests/test_attention.py`도 exact path로 삭제했다. 삭제된 module에서 남은 ignored `maintain/__pycache__/`와 `maintain/tests/__pycache__/`도 확인 뒤 해당 두 cache 경계만 제거했다.

## Root 연결은 부모 상태로 복원하지 않았다

`2649e9b`의 root에는 Workspace 005 Observe 실험이 있었다. 그 상태를 기계적으로 되살리면 [005 record 06](../../005-context-continuity-maintenance/records/2026-08-17-06-response-end-observe-runtime-and-live-smoke.md)에서 실제로 실패한 async `Stop --drain`과 repo-global FIFO를 새 007 세션에서 다시 실행하게 된다.

따라서 root는 다음과 같이 별도 정합화했다.

- `.codex/hooks.json`: 유효한 JSON이지만 `hooks: {}`인 명시적 inactive 설정
- `.codex/config.toml`: Maintain agent 등록 없음
- `.codex/context-maintain.json`: 삭제
- `.codex/workspace-context-maintainer.toml`: 삭제
- `.codex/context_maintainer/`: 부모의 Observe package를 복원하지 않음
- `.codex/agents/context-maintainer.toml`: 부모의 Observe agent를 복원하지 않음
- Root `AGENTS.md`, `README.md`: 자동 Maintain 비활성, 수동 Workspace 관리와 clean-room 경계를 설명

Root `.gitignore`의 `.context-harness/runtime/` ignore는 그대로 유지했다. 이 경로에는 과거 005 Observe와 중단된 006 실험의 runtime 잔재가 함께 남아 있지만 active 설정은 어느 것도 참조하지 않는다. 전체 ignored runtime을 새 설계의 source·canonical·완료 증거·migration 입력으로 재해석하거나 삭제하지 않았으며, 새 runtime 선택을 뜻하지도 않는다.

## 보존한 역사와 사용자 파일

다음 Workspace 005 경로는 `9553d0a` 시점으로도 되돌리지 않고 후속 종료 상태가 포함된 현재 버전을 그대로 보존했다.

```text
context/workspaces/005-context-continuity-maintenance/README.md
context/workspaces/005-context-continuity-maintenance/current/index.md
context/workspaces/005-context-continuity-maintenance/current/memory.md
context/workspaces/005-context-continuity-maintenance/current/state.md
context/workspaces/005-context-continuity-maintenance/output/index.md
context/workspaces/005-context-continuity-maintenance/records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md
context/workspaces/005-context-continuity-maintenance/records/README.md
```

Workspace 006의 README·current·output·records도 `0952b1d`에 먼저 보존하고 reset commit에서 수정하지 않았다. Root untracked `.DS_Store`는 사용자 소유로 판단해 stage·삭제·복원하지 않았다.

## 검증 결과

### Exact restoration과 비활성 경계

- 45개 path manifest와 `2649e9b` 비교: diff 없음
- Workspace 005·006에 대한 reset staged diff: 없음
- `.codex/context_maintainer/`, old root agent, active binding config와 Reference `maintain/hook.py`: 부재
- Root `.codex/hooks.json` JSON parse: 통과
- Root `.codex/config.toml` TOML parse: 통과
- `git diff --check`: 통과

### Reference test baseline

실행 명령:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=reference-project \
python3 -m unittest discover -s reference-project -t reference-project -p 'test_*.py' -q
```

전체 suite는 세 번 실행했다. 첫 실행과 007 setup 뒤 최종 실행에서는 기존 Verify의 `test_timeout_covers_descendant_after_group_leader_exits`가 descendant PID 파일을 0.3초 timeout 전에 만들지 못해 각각 53개 중 같은 1개가 실패했다. 그 사이 동일 test 단독 실행과 전체 suite 재실행은 각각 통과했다.

따라서 최종 판정은 `53/53 green`이 아니라 **52/53과 53/53 사이에서 흔들리는 parent baseline timing instability**다. 복원 path가 parent와 exact해 reset 회귀로 판정하지 않으며, 새 Maintain 구현과 섞어 고치지 않는다. Verify process handling을 변경할 작업이 생기면 이 test의 process scheduling 전제와 timeout을 별도 진단한다.

## 새 설계를 구속하지 않는 과거 topology 근거

### Root Observe

- UserPrompt와 async Stop을 partial pair로 모음
- repo-global sequence와 FIFO
- missing Stop 뒤 manual gap repair

실제 host exit에서 async Stop이 취소됐고 한 session의 gap이 다른 session을 막았다. 이는 이 구조를 금지한다는 뜻이 아니라, 같은 방식을 다시 선택한다면 host 종료 조건과 session 간 격리를 새 근거로 해결해야 한다는 negative acceptance다.

### Workspace 005 final runtime

- capture·pairing·queue·scheduler·session state·report·freshness·gap repair·metrics가 커진 runtime
- semantic intent, writer journal, stage, completion marker와 checkpoint의 다층 commit bridge
- session report delivery·resolution과 cross-session recovery protocol

Record 09의 Reference ownership 결과와 proof ceiling은 보존한다. 이 lifecycle은 미리 선택된 requirement도 금지된 option도 아니며 현재 필요성에서 다시 판단한다.

### Workspace 006 improvement attempt

- Stop 시점 completed pair ordering
- Workspace attention store
- legacy checkpoint migration·compatibility
- delivery cursor와 replay bridge

이 시도는 일부 active state를 없앴지만 새 store·migration·compatibility·delivery 복구를 만들었고, 기존 intent→journal→completion→checkpoint를 남겼다. 내부 test 통과만으로 새 architecture의 우선 후보가 되지는 않지만, 같은 아이디어가 현재 필요성에서 다시 도출되는 것을 막지는 않는다.

## 이 baseline이 의미하는 것

`b508d80`은 기능하는 새 Maintain이 아니라 선입견 없이 설계하기 위한 안전한 code baseline이다. Reference Maintain 디렉터리에는 부모 기준의 경계 문서와 adapter 정의만 남고, root 자동 실행은 없다.

새 세션의 첫 성공은 코드를 많이 만드는 것이 아니라, [behavior contract](2026-08-18-01-clean-room-source-and-behavior-contract.md)의 여섯 장면에서 최소 책임과 actual acceptance를 도출해 첫 vertical slice의 존재 이유를 설명하는 것이다.
