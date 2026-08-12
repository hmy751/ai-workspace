# Current work context

마지막 갱신: `2026-08-12`

## 현재 문제

source intake 이후 작업이 계속 쌓여도 현재 유효한 내용과 과거 작업 기록을 혼동하지 않도록 context 작업대의 상태 층위를 세운다.

## 현재 상태

- repo root는 `/Users/hammyeong-yeon/Desktop/context-harness`다.
- source는 원본·사용자 선택·AI 의견·기존 작업 관찰 자료로 분리되어 있다.
- context 아래에 `active`와 `history`를 분리했다.
- active의 현재 owner는 `project.md`와 `work.md`다.
- 작업 과정은 history에 남기고, 검증 후 현재도 유효한 내용만 active에 반영하는 흐름을 채택했다.
- `.codex/agents/context-maintainer.toml`에 repo-local maintainer를 두고, `.codex/config.toml`에 역할을 등록했으며, `AGENTS.md`에서 의미 있는 작업 경계의 호출 조건을 정했다.
- agent와 routing의 TOML·링크·지침 정합성을 검증했고, 저장소 밖에 남겼던 지원 설정은 모두 제거했다.

## 근거와 관련 기록

- source intake baseline: [`../history/2026-08-12-01-source-intake.md`](../history/2026-08-12-01-source-intake.md)
- active/history 층위 결정: [`../history/2026-08-12-02-active-history-separation.md`](../history/2026-08-12-02-active-history-separation.md)
- context maintainer 도입: [`../history/2026-08-12-03-context-maintainer-agent.md`](../history/2026-08-12-03-context-maintainer-agent.md)
- maintainer의 repo-local 범위 정정: [`../history/2026-08-12-04-context-maintainer-local-only.md`](../history/2026-08-12-04-context-maintainer-local-only.md)
- source 검증 보고: [`../source/VERIFICATION.md`](../source/VERIFICATION.md)

## 불확실성

- 사용자 원문에는 “context의 세 가지 역할”이라고 적혀 있지만 현재 이름과 설명이 제시된 역할은 Project common context와 Work context 두 가지다. 세 번째 역할은 아직 정하지 않는다.
- maintainer가 context 문서 정합성을 점검하는 경계는 정했지만, 제품 작업의 실제 검증 결과가 어떤 상태 전이로 project common context에 승격되는지는 아직 설계하지 않았다.
- Codex는 보안상 trusted project의 `.codex/config.toml`만 자동 로드한다. 이 저장소는 전역 trust를 미리 등록하지 않으므로, 실제 환경이 요구할 경우 trust 여부는 사용자가 그 환경에서 직접 선택한다.

## 다음 행동

source를 바탕으로 `복구 → 필요한 정보 선택 → 행동 → 검증 → active 반영`의 실제 운영 흐름과 각 상태 owner를 설계한다.
