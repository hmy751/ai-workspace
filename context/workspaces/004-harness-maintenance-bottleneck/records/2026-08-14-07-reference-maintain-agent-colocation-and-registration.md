# Reference Maintain agent 배치와 등록 결정

기록일: `2026-08-14`
상태: 사용자 구조 결정 반영, 정적 등록·회귀 검증 완료

## 사용자 결정

Reference의 실제 Maintain agent TOML을 Project root의 `.codex/agents/`에 두지 않고, Maintain 관심사를 소유한 `context/work/harness/maintain/` 아래에 둔다. Root에는 agent 내용을 복제하지 않고 Project-scoped role이 하위 정의를 찾는 등록만 남긴다.

## 반영된 책임 배치

- [`workspace-context-maintainer.toml`](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml): Maintain 계약을 수행하는 실제 Codex agent 정의
- [`.codex/config.toml`](../../../../reference-project/.codex/config.toml): `[agents.workspace_context_maintainer]`의 `config_file`로 하위 정의 경로만 등록
- [`context/work/AGENTS.md`](../../../../reference-project/context/work/AGENTS.md): Work·Harness 상세 운영 규칙, Maintain 호출 시점과 main 검토 routing
- [Root `AGENTS.md`](../../../../reference-project/AGENTS.md): 하위 책임별 지침으로 보내는 최소 router

이 배치는 agent 정의와 그 agent가 수행하는 Maintain 책임을 같은 경계에서 발견하게 한다. 동시에 Project root 설정은 Codex의 발견 장치, Work `AGENTS.md`는 운영 지침, Work·Workspace 문서는 지속 Context 의미의 canonical이라는 역할을 분리한다.

## 확인 결과와 범위

이번 변경은 agent 본문의 실행 의미, Recover·Verify 구현, schema와 제품 코드를 바꾸지 않는 경로·설명 재배치다. 다음 범위를 확인했다.

- `.codex/config.toml`과 하위 agent TOML parse, `config_file`의 실제 경로 해석 통과
- `reference-project/`와 Workspace 004 Markdown 로컬 링크 245개 검사에서 누락 0
- 최종 Reference 전체 suite 53/53 통과
- `git diff --check`와 `git diff --cached --check` 통과

첫 전체 suite에서는 timing-sensitive POSIX descendant-timeout test가 `descendant.pid`를 만들기 전에 끝나 1건 실패했다. 해당 test를 단독 재실행해 통과했고, 마지막 전체 suite도 53/53 통과했다. 이번 경로 재배치에서 Verify 코드는 수정하지 않았다.

이 검사는 등록 파일의 구조와 기존 회귀 동작을 확인하지만, 새 Codex session이 Project-scoped role을 실제로 발견해 agent를 호출하는 동작까지 증명하지 않는다.

## 남은 판단

사람 acceptance는 계속 열려 있다. 실제 Project-scoped agent 발견과 호출을 별도 runtime 검증할지는 main과 사용자가 변경 위험과 필요한 proof ceiling에 맞춰 결정한다.
