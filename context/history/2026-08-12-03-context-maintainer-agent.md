# Context maintainer subagent 도입

날짜: `2026-08-12`

## 발단

active/history 지침만으로는 main이 긴 작업 중 context 갱신 시점을 놓칠 수 있어, 사용자가 context 유지 역할을 맡는 subagent 하나를 두자고 제안했다.

## 구현

- project-scoped custom agent: `.codex/agents/context-maintainer.toml`
- project-scoped role registration: `.codex/config.toml`
- 호출 routing: `AGENTS.md`
- 역할: 의미 있는 작업 경계에서 실제 변경·검증 결과와 active/history/source를 대조하고, 근거가 명확한 context 갱신만 수행

형식은 `2026-08-12`에 확인한 [OpenAI 공식 Subagents 문서](https://developers.openai.com/codex/multi-agent)와 [Codex configuration reference](https://developers.openai.com/codex/config-reference)를 따랐다. agent 지침은 `.codex/agents/*.toml`에 두고, 프로젝트 `.codex/config.toml`의 `[agents.context_maintainer]`에서 해당 파일을 명시적으로 등록한다.

## 호출 조건

- 목표·기준·제약·source 경계 변경
- 현재 문제·작업 커서·다음 행동 변경
- 의미 있는 결정·실패·blocker·검증 결과·완료·폐기
- active drift 가능성

단순 질의나 사소한 편집에는 호출하지 않아 history와 agent 비용이 불필요하게 늘지 않게 한다.

## 권한 경계

- 근거가 명확하면 `context/active/`와 `context/history/`를 갱신할 수 있다.
- `context/source/`, 제품 코드, 프로젝트 밖 파일은 수정하지 않는다.
- 사용자 목표·승인 결정·새 설계 기준을 대신 확정하지 않는다.
- 충돌 시 `needs_user_decision`으로 main에 반환한다.
- main이 변경 diff와 근거를 최종 검토한다.

## 제거 가능성

이 agent가 필요해진 전제는 main이 긴 작업 중 context 갱신 경계를 놓칠 수 있다는 점이다. 이후 같은 점검이 Codex 기본 기능으로 대체되거나 별도 maintainer가 불필요해지면 `.codex/config.toml`의 역할 등록, agent 파일, `AGENTS.md`의 routing만 제거할 수 있다. 현재 상태의 canonical인 `context/active/`, 근거 이력인 `context/history/`, 읽기 전용 원본인 `context/source/`, 그리고 main과 사용자의 최종 판단 책임은 그대로 남는다.

## 검증 결과

- 두 TOML 파일의 parse와 `git diff --check`를 통과했다.
- 프로젝트 `AGENTS.md`가 새 Codex 세션의 model-visible instruction에 포함되는 것을 확인했다.
- 첫 기본 호출은 프로젝트가 untrusted라 `.codex/config.toml`이 로드되지 않아 `unknown agent_type`으로 실패했다.
- Codex의 trust prompt로 `/Users/hammyeong-yeon/Desktop/context-harness`만 trusted project로 등록했다.
- ChatGPT 앱 번들에는 있지만 CLI 경로에 없던 `codex-code-mode-host`를 `/opt/homebrew/bin/codex-code-mode-host` symlink로 연결했다.
- 최종 read-only smoke test에서 `context_maintainer`가 named agent로 생성되고 `context/active/index.md`, `project.md`, `work.md`를 모두 읽었다. 수정 파일과 미해결 항목은 없었다.

## 검증 상한

등록·발견·active 진입 문서 소비까지는 확인했다. 새 agent가 이후 모든 의미 있는 작업 경계에서 빠짐없이 호출되고, 실제 변화에 맞게 active/history를 올바르게 갱신한다는 지속 효과는 후속 작업에서 확인해야 한다.
