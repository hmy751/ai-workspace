# Current와 records로 context 층위 정리

날짜: `2026-08-13`

## 사용자 결정

누적된 작업과 현재 상태를 혼동하지 않도록 기존 `active`와 `history` 이름을 다음처럼 바꾼다.

- `current`: 지금 유효하고 다음 세션의 행동에 필요한 현재 상태
- `records`: 작업 중 만든 지속 가능한 문서·분석·중간 산출물·검증 기록의 누적층

current 내부에서는 다음 두 context 역할을 계속 분리한다.

- `project.md`: 여러 작업을 지나도 유지되는 목표·기준·결정·제약·지속 효과
- `work.md`: 지금 이어갈 문제·현재 상태·근거 접근점·불확실성·다음 행동

## 완료 상태를 다루는 기준

완료 여부만으로 current와 records를 나누지 않는다.

- 완료 과정과 상세 결과는 records에 남긴다.
- 완료 뒤에도 이후 행동에 영향을 주는 효과·제약은 current/project에 남긴다.
- 완료 뒤 후속 작업이 있으면 current/work에 남긴다.
- 여전히 사실이어도 다음 행동에 영향을 주지 않으면 current에서 내리고 records에서 찾게 한다.
- 미확인 상태나 사용자 판단 대기도 현재 행동에 필요하면 상태를 명시해 current/work에 둔다.

## 반영한 변경

- `context/active/`를 `context/current/`로 변경했다.
- `context/history/`를 `context/records/`로 변경했다.
- 루트와 context 안내, 재진입 지침, current 유지 규칙을 새 의미에 맞췄다.
- repo-local `context_maintainer`가 records 누적과 current 갱신·정리를 함께 점검하도록 역할과 routing을 바꿨다.
- `output/`에 잘못 두었던 source 분석 문서를 records로 옮기고, 사용자 승인 결정이 아닌 AI 분석·제안임을 표시했다.
- `output/`은 실제 목표 산출물 자리로 비워 두었다.

## 과거 records의 이름

`2026-08-12` records 안의 `active/history` 표현은 당시 사용한 이름과 그 시점의 결정을 보여 주므로 현재 용어로 소급해 다시 쓰지 않는다. 이 record가 `current/records`로 바뀐 후속 결정을 소유한다.

## 검증

변경 뒤 다음을 확인했다.

- prior-work 대표 snapshot 내부의 의도적 미보존 링크를 제외한 로컬 Markdown 링크 34개가 모두 유효하다.
- `.codex/config.toml`과 `.codex/agents/context-maintainer.toml`이 Python `tomllib` parse를 통과했다.
- AX와 cofathon의 보존 snapshot 36개가 각 manifest의 SHA-256과 byte size에 그대로 일치했다.
- staged·unstaged 변경 모두 `git diff --check`를 통과했고 `context/source/` 변경은 없다.
- 현재 운영 문서에는 옛 `context/active/`나 `context/history/` 경로가 남지 않았다. 과거 records와 이 migration record의 옛 이름은 당시 상태와 이름 변경을 설명하는 기록이다.
- `output/`에는 자리 유지를 위한 `.gitkeep`만 있고 실제 산출물은 아직 없다.
- 별도 read-only verifier가 current/records 역할, 완료 처리, AI 제안의 미승격, proof ceiling을 대조해 `context_status: current`로 판정했다.

repo-local custom agent를 이름으로 직접 생성하는 시도는 현재 런타임에서 `unknown agent_type 'context_maintainer'`로 거절됐다. 전역 trust나 agent 등록은 추가하지 않았고, 같은 저장소의 agent 지침을 읽은 독립 subagent로 정합성만 검증했다. 따라서 agent 파일·routing 계약의 정적 정합성은 확인했지만, named agent 자동 로드와 지속적인 행동 효과는 아직 증명하지 않았다.
