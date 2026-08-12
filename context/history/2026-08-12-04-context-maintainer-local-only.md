# Context maintainer를 repo-local 전용으로 정정

날짜: `2026-08-12`

## 사용자 정정

`context_maintainer`는 이 저장소에서만 사용해야 하며, 전역 agent나 전역 하네스 요소로 등록하지 않는다.

## 제거한 저장소 밖 변경

- `~/.codex/config.toml`의 `context-harness` project trust 항목
- `~/.claude/global-index/projects.md`의 `context-harness` 색인
- `~/.claude/global-index/runtime.md`의 `codex-code-mode-host` 설명
- `/opt/homebrew/bin/codex-code-mode-host` symlink

과거 전역 snapshot commit은 변경과 원복을 감사할 수 있는 이력이므로 다시 쓰거나 삭제하지 않고, 원복된 live 상태를 후속 snapshot으로 남긴다.

## 저장소에 남기는 canonical

- agent 역할과 권한: `.codex/agents/context-maintainer.toml`
- project-scoped 역할 등록: `.codex/config.toml`
- 호출 조건과 main 책임: `AGENTS.md`
- 현재 상태와 작업 이력: `context/active/`, `context/history/`

## 운영상 제한

Codex는 trusted project의 `.codex/config.toml`만 자동 로드한다. 이 프로젝트를 trust할지는 실행 환경의 사용자가 직접 선택하며, 저장소가 전역 trust를 대신 등록하지 않는다. trust 여부와 무관하게 agent의 의미·권한·routing 원천은 저장소 안에만 둔다.
