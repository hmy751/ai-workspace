# Root automatic Maintain 연결 경계

날짜: `2026-08-19`

상태: **Reference acceptance 완료 / outer root 적용은 별도 큰 범위**

## 이 기록의 역할

[Failure ordering과 semantic acceptance](2026-08-19-07-failure-ordering-and-semantic-acceptance.md) 뒤 outer `context-harness` root의 빈 hook을 Reference adapter에 다시 연결할 수 있는지 실제 경로를 대조한다. 단순 설정 활성화인지 기존 Context canonical을 바꾸는 별도 적용 작업인지 구분한다.

## 확인한 현재 구조

Outer root는 다음 구조를 canonical로 사용한다.

- Workspace: `context/workspaces/<workspace_id>/`
- 재진입 current: `current/memory.md`, `current/state.md`
- Root hook: `.codex/hooks.json`의 빈 hook 집합
- Root agent config: `.codex/config.toml`에 Maintainer 미등록

Reference adapter는 다음 구조를 전제로 구현됐다.

- Work root: `<project_root>/context/work`
- Workspace: `context/work/workspaces/<workspace_id>/`
- Identity와 Recover 계약: `workspace.json`, `recover.json`
- 재진입 current: `current/memory/index.md`와 direct-child memory Markdown, `current/state/index.md`
- Host adapter의 `work_root`: `project_root/context/work`로 고정
- Guard allowlist: 위 Reference Workspace Owner 경로

따라서 outer `.codex/hooks.json`과 `.codex/config.toml`에 Reference 설정만 복사하면 현재 Workspace 007을 grounding할 수 없다. 별도 `context/work/`를 만들면 기존 `context/workspaces/`와 두 Context canonical이 생겨 [root Context contract](../../../README.md)를 깨뜨린다.

## 필요한 별도 판단

Outer root에 적용하려면 최소한 다음 중 하나를 선택하고 실제 migration·fallback 범위를 설계해야 한다.

1. Outer Context를 Reference Work 구조로 이관한다.
2. Host adapter, Recover와 Guard가 outer root의 기존 Context 구조를 명시적으로 지원하는 별도 adapter를 만든다.
3. `apply-context-harness`의 target 적용으로 다루되, 기존 canonical을 보존하는 target-specific mapping을 먼저 확정한다.

세 선택 모두 기존 Workspace identity, current Owner, Recover 입력과 write allowlist에 영향을 주는 큰 범위다. Reference 구현을 root에 단순 등록하는 단계가 아니며, 사용자가 정한 gate에 따라 이번 slice에서 진행하지 않았다.

## 현재 판정

- `reference-project/` 안의 자동 lifecycle은 hook·binding·adapter까지 구현되고 실제 host acceptance를 통과했다.
- Outer root automatic Maintain은 계속 비활성이다.
- Workspace 007의 Reference clean-room 구현 목표는 완료로 판정할 수 있다.
- Outer root 적용은 기존 canonical 보존 방식을 먼저 결정해야 하는 별도 적용 작업이다.

Root 연결을 보류하는 이유는 Reference behavior나 failure ordering의 미완성이 아니라, target인 outer root의 Context 구조가 Reference와 다르기 때문이다.
