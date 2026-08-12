# Cofathon 지원 작업 지침

Cofathon 참가자 선발을 준비하고, 선발 뒤 본선 과제까지 이어 가는 작업 저장소다. 새 문서와 메모의 설명 문장은 한국어로 쓰고, 코드·명령어·제품명·원문 인용은 자연스러우면 영어를 유지한다.

## 매 세션 시작 시 — main 재진입 계약

이 절의 복기·정지 계약은 사용자와 직접 대화하는 main 작업의 새 세션 시작과 재개에 적용한다. Codex SessionStart source로는 `startup`, `resume`, `clear`가 이에 해당한다. Codex의 도구 사용 전 짧은 진행 commentary는 허용하지만, 실질 작업보다 먼저 `context/current.md`, `context/goal.md`, `context/core/README.md`를 끝까지 읽는다. 읽은 뒤 첫 실질 사용자 응답(Codex에서는 첫 final 응답)에서 프로젝트의 Mission, `*-> 지금*` 커서가 가리키는 실제 진행 위치, 바로 다음 판단 또는 행동을 짧게 설명하고 멈춘다. 사용자가 지도를 바로잡거나 진행을 확인하기 전에는 새 작업을 시작하지 않는다.

자동 context compact 뒤에는 같은 문서로 기준을 복원하되 진행 중인 요청을 계속하고, 시작 복기나 사용자 재확인을 새로 요구하지 않는다. subagent·guardian·독립 판별자는 main용 복기·정지 계약을 적용하지 않고 위임 범위와 독립성 조건을 따른다.

`current.md`의 커서나 서술이 실제 파일·결정과 어긋나면 조용히 따라가지 않는다. 무엇이 어긋났는지 먼저 말하고 실제 상태를 확인한 뒤 지도를 고친다. 단계 선택·방향 전환·Goal 변경처럼 바깥 흐름을 바꾼 결정은 `context/process/`에 남긴다. 엔지니어링 loop 안의 구현 기록·검증 결과·반복 판정은 해당 loop 폴더에 남긴다. 기록 없이 다음 게이트를 완료로 표시하지 않는다.

아래 `@` 표기는 Claude Code의 자동 로드용이다. Codex에서는 `.codex/hooks.json`의 `SessionStart`가 이 절을 developer context로 다시 전달하고, agent가 파일을 직접 읽는다. hook script는 시작 source를 구분하며 실행 흔적은 `logs/codex/session-start-hooks.jsonl`에 남긴다. 새로 추가되거나 바뀐 hook 정의는 최초 실행 시 내용을 확인하고 신뢰 승인한다.

@context/current.md
@context/goal.md
@context/core/README.md

## 문서 층위

- `context/current.md` — 항상 먼저 보는 현재 지도. 완료된 가지도 남기되 세부 이력은 넣지 않는다. 커서는 `*-> 지금*` 하나만 둔다.
- `context/goal.md` — Mission과 Campaign Goal의 현재 원본. current는 짧은 요약과 링크만 유지한다.
- `context/core/` — 현재 커서와 무관하게 프로젝트 전반에서 계속 참조할 기준의 최신판. 불변은 아니지만 단계별 현재 판단을 미리 승격하지 않는다.
- `context/research/` — `00-current-synthesis.md`를 중앙판으로 두고, 첫 패스·표적 2차 패스·판단 보조에 상세 조사와 후보 발산·비교를 보존한다.
- `context/problem/` — 후보 방향을 고른 뒤 선택한 사용자·workflow·Problem Statement를 구체화하는 곳.
- `context/solution/` — 선택한 문제에 직접 작용하는 제품의 현재 정의·사용자 변화·핵심 workflow·출력·작동 경계와 다시 열 조건을 두는 곳. 구현 완료 상태와 기술 계약은 engineering이 소유한다.
- `context/engineering/` — 최상위 구현 Goal과 번호·주제가 붙은 loop 폴더를 두는 곳. 각 loop 폴더의 `goal.md`가 그 loop의 상태 변화·판정 기준·증거를 소유하고, 필요한 구현 기록과 검증 증거를 같은 폴더에서 연결한다. README가 현재 활성 문서와 기록 경계로 안내한다.
- `context/process/` — 단계 선택·방향 전환·공유 기준 승격·Goal 변경처럼 이후 흐름의 이유가 되는 결정을 시간순으로 쌓는 이력. 엔지니어링 loop 내부의 구현·검증·반복 판정은 해당 loop 폴더가 소유한다. 과거 기록을 현재 결론에 맞춰 고쳐 쓰지 않는다.
- `context/sources/` — 보존이 필요한 원문과 최소 발췌.
- `cofathon-main/`, `cofathon-apply/` — Cofathon 공식 페이지를 저장한 원본 bundle.

## 로컬 도구와 개인 로그

- LazyCodex/Insane Search의 격리 설치·사용, 대화 로그 hook·복구, SessionStart audit의 상세 절차는 [tools/README.md](./tools/README.md)를 따른다.
- `.lazycodex-home/`과 `logs/`는 커밋·공유하지 않는 로컬 자료다. 비밀정보가 로그에 남을 수 있으므로 API key·비밀번호·token을 대화에 넣지 않는다.

## 커밋 규칙

- 형식: `타입: 한국어 요약`. 본문은 필요할 때만 쓴다.
- `chore:` — 프로젝트 로컬 도구·훅·설정
- `context:` 또는 `context(scope):` — `context/` 문서 갱신
- `feat:` / `fix:` — 구현 코드
- 게이트를 완료로 기록할 때는 그 게이트의 소유 문서에 판정 근거가 먼저 있어야 한다. 엔지니어링 loop의 게이트는 해당 loop 폴더에 기록한다.
- 커밋 메시지에 AI 도구명·모델명·실행 환경 메타데이터를 남기지 않는다.
