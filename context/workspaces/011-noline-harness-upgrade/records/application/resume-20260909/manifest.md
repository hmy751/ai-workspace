# Noline 재이식 manifest

사용자가 승인한 동일 범위를 fresh preflight로 다시 고정했다. Source `87d2102` Reference clean, target `feat/noline-context-harness @ b4ed41f6`. Exact new/modify/remove-after-copy paths, old/new hashes, actual ancestor kind·ignore 확인은 paths.json이 소유한다. 보호 18개 entry와 payload 교집합은 없다. 기존 untracked 18개 entry를 유지한다. Session runtime은 양 host 모두 없다.

Source Work·Workspace·Recover·Maintain·Verify 계약 변경분은 동일 경계에 설치한다. 기존 Noline Claude 설명·role 이름·adapter·tests·settings·wrappers는 보존한다. 최신 Python runtime·tests는 원본과 동일하며 sample 제품·Workspace·receipt는 제외한다. Work 지침의 제품 경로·검증 명령만 Noline에 적응한다.

Project common/current/guidance와 Decision root는 설치·적응한다. common/product는 root guide·제품 README·Selective Activation 상세 Owner의 사용자 장면·데이터 불변식·범위를 재서술한다. current/architecture는 app/package 경계·Router/Sync/Policy 흐름·검증 상한을 재서술한다. guidance는 기존 rules/guards/runbooks Owner를 유지하고 공동 설명 기준을 조건부 설치한다. 본문이 없는 layer는 없다. 기존 flat 파일은 본문을 그대로 유지한 채 현재 authority에서 내렸음을 안내한다.

여섯 Reference skill은 `.claude/skills/<name>/`에 원본을 두고 `.agents/skills/<name>` 상대 bridge로 적응한다. 기존 create-context-workspace는 갱신하고 나머지 다섯을 추가한다. noline-work와 noline agents는 보존한다. Reference의 별도 `.codex/skills/` alias는 Noline discovery model과 중복되어 제외한다. 각 frontmatter/openai.yaml, root router·색인·canonical·공동 guidance 연결을 검사한다. 정적 설치를 실제 discovery·invocation으로 보고하지 않는다.

기존 active 001 이식 Workspace를 schema 6·Spec 다섯 파일·Ticket 하나로 적응한다. 이전 memory는 source/prior-memory에 원문 바이트를 보존하고 옛 current 세 파일만 내린다. Root README와 common/product·current/architecture·기존 Decision을 Recover에 선택한다. Guidance는 설명 스킬의 조건에서 선택하므로 기본 입력에서 제외한다. 제품 리팩토링은 계획하지 않는다. Machine preflight·path manifest·Harness tests는 records/receipts/<종류>에 둔다.

검사기는 새 skill 허용 목록·Project 진입과 Spec 계약을 맞추고 --no-git-diff를 추가한다. 기본 직접 검사는 동일 Git whitespace 확인을 유지한다. Verify는 regular 본문 closure를 선언하고 Git/index 검사만 직접 확인으로 분리한다. Symlink·directory membership·linked target 존재의 미래 동일성은 freshness가 증명하지 않는다는 ceiling을 claim과 기록에 둔다. 명령은 pnpm·lockfile·compiler나 제품 source를 실행하지 않는다.

검증은 관련 unit → 전체 Harness suite·ephemeral validation, local link lexical/resolved·semantic review, skill shape/bridge, all live consumer explicit/default Recover, Verify→Recover, 보존 hash 대조다. 신규 sample id/timeout residue는 test fixture 의미만 허용하고 live 내용에는 남기지 않는다. 과거 원문·기록 속 옛 Project 경로는 provenance로만 유지한다. 독립 review는 Main이 회수한다. Actual host trust/activation, 제품 acceptance, Workspace 완료·stage·commit은 범위 밖이다.

- write: `.agents/skills/README.md`
- symlink: `.agents/skills/explanation-recovery`
- symlink: `.agents/skills/reconsider-work`
- symlink: `.agents/skills/update-project-context`
- symlink: `.agents/skills/work-artifact-briefing`
- symlink: `.agents/skills/work-discussion`
- write: `.claude/decisions/2026-09-09-context-harness-upgrade.md`
- write: `.claude/harness/README.md`
- write: `.claude/skills/README.md`
- write: `.claude/skills/create-context-workspace/SKILL.md`
- write: `.claude/skills/create-context-workspace/agents/openai.yaml`
- write: `.claude/skills/explanation-recovery/SKILL.md`
- write: `.claude/skills/explanation-recovery/agents/openai.yaml`
- write: `.claude/skills/reconsider-work/SKILL.md`
- write: `.claude/skills/reconsider-work/agents/openai.yaml`
- write: `.claude/skills/update-project-context/SKILL.md`
- write: `.claude/skills/update-project-context/agents/openai.yaml`
- write: `.claude/skills/work-artifact-briefing/SKILL.md`
- write: `.claude/skills/work-artifact-briefing/agents/openai.yaml`
- write: `.claude/skills/work-discussion/SKILL.md`
- write: `.claude/skills/work-discussion/agents/openai.yaml`
- write: `CLAUDE.md`
- write: `context/README.md`
- write: `context/project/README.md`
- write: `context/project/architecture.md`
- write: `context/project/common/README.md`
- write: `context/project/common/product.md`
- write: `context/project/current/README.md`
- write: `context/project/current/architecture.md`
- write: `context/project/decisions/0001-selective-local-first.md`
- write: `context/project/decisions/README.md`
- write: `context/project/guidance/README.md`
- write: `context/project/guidance/explanation-and-evidence-criteria.md`
- write: `context/project/overview.md`
- write: `context/project/prd.md`
- write: `context/work/AGENTS.md`
- write: `context/work/README.md`
- write: `context/work/harness/maintain/README.md`
- write: `context/work/harness/maintain/codex_session.py`
- write: `context/work/harness/maintain/operation.py`
- write: `context/work/harness/maintain/tests/test_codex_session.py`
- write: `context/work/harness/maintain/tests/test_operation.py`
- write: `context/work/harness/maintain/workspace-context-maintainer.toml`
- write: `context/work/harness/recover/README.md`
- write: `context/work/harness/recover/operation.py`
- write: `context/work/harness/recover/tests/test_recover.py`
- write: `context/work/harness/testing.py`
- write: `context/work/harness/verify/README.md`
- write: `context/work/harness/verify/tests/test_verify.py`
- write: `context/work/workspaces/001-noline-context-harness-application/README.md`
- remove-after-byte-copy: `context/work/workspaces/001-noline-context-harness-application/current/memory/01-goal.md`
- remove-after-byte-copy: `context/work/workspaces/001-noline-context-harness-application/current/memory/02-constraints.md`
- remove-after-byte-copy: `context/work/workspaces/001-noline-context-harness-application/current/memory/03-project-context.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/index.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/project-context.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/spec/01-problem-goal-scope.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/spec/02-behavior-and-cases.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/spec/03-concepts-and-contracts.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/spec/04-quality-and-completion.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/spec/05-constraints-design-assumptions.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/tickets/001-upgrade.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/memory/tickets/index.md`
- write: `context/work/workspaces/001-noline-context-harness-application/current/state/index.md`
- write: `context/work/workspaces/001-noline-context-harness-application/output/index.md`
- write: `context/work/workspaces/001-noline-context-harness-application/records/2026-09-09-01-reference-upgrade.md`
- write: `context/work/workspaces/001-noline-context-harness-application/records/README.md`
- write: `context/work/workspaces/001-noline-context-harness-application/records/receipts/application/paths-20260909.json`
- write: `context/work/workspaces/001-noline-context-harness-application/records/receipts/harness-tests/README.md`
- write: `context/work/workspaces/001-noline-context-harness-application/records/receipts/preflight/preflight-20260909T140507056185Z-f1caf35fc6894327a7d811ffd7622f3c.json`
- write: `context/work/workspaces/001-noline-context-harness-application/recover.json`
- write: `context/work/workspaces/001-noline-context-harness-application/source/index.md`
- write: `context/work/workspaces/001-noline-context-harness-application/source/prior-memory/01-goal.md.txt`
- write: `context/work/workspaces/001-noline-context-harness-application/source/prior-memory/02-constraints.md.txt`
- write: `context/work/workspaces/001-noline-context-harness-application/source/prior-memory/03-project-context.md.txt`
- write: `context/work/workspaces/001-noline-context-harness-application/verify.json`
- write: `context/work/workspaces/CREATE-AND-TRANSITION.md`
- write: `context/work/workspaces/README.md`
- write: `context/work/workspaces/SPEC-AND-TICKETS.md`
- write: `scripts/check-harness.mjs`
