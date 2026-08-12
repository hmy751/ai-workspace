# 마이리얼트립 제출 작업 지침

AX 인재전쟁 해커톤 마이리얼트립 제출물을 만드는 작업 레포다. 새 문서와 메모는 한국어로 쓰고, 코드·명령어·제품명·원문 인용은 영어를 그대로 둔다. 파일과 폴더 이름은 영어로 쓴다.

## 매 세션 시작 시 — 반드시 먼저 읽기

세션을 시작하면 다른 작업보다 먼저 `context/current.md`와 `context/core/README.md`를 읽는다. 아래 @표기는 Claude Code의 자동 로드용이고, Codex에서는 이 문단의 지시에 따라 직접 읽는다. `.codex/hooks.json`의 `SessionStart` 훅은 이 문단을 매 세션 developer context로 다시 전달한다. 이 문단의 지시나 읽기 목록을 바꾸면 다음 세션부터 자동으로 반영된다. 새로 추가되거나 바뀐 훅은 최초 실행 시 내용을 확인하고 신뢰 승인해야 한다.

첫 응답에서 프로젝트가 무엇인지, 지도 커서 기준 어디까지 왔는지, 다음 할 일이 무엇인지 설명하고 멈춘다. 사용자가 확인하기 전에는 작업을 시작하지 않는다.

작업 중 판단·기각·막힘이 생기면 그 자리에서 context/process/에 남긴다. 게이트 보고는 context/process/ 파일로 쓴다 — 기록 없이는 게이트를 넘지 않는다.

@context/current.md
@context/core/README.md

- `context/current.md` — 사용자의 현재 그림(위치·방향·생각 구조)과 AI의 싱크. 최신만 있고 이력이 없다.
- `context/core/` — 기준판: requirements(과제 요구사항·문항 기준), dev-principles(개발 원칙), 틀(loop·research). 거의 안 변한다. 유동적인 과제 기준·goal은 current.md에서 키운다.

## 문서 층위

- `context/` — 작업 컨텍스트 전체. 제출 형식 밖의 작업 문서는 여기 모은다.
  - `context/current.md` — 계속 변함 + 늘 곁에 둠. 덮어쓰기 전용. 이력은 남기지 않는다(이력은 context/process/).
  - `context/core/` — 현재 기준판 + 늘 곁에 둠. 바꿀 땐 조용히 바꾸지 않는다: 변경을 선언하고, 이유는 context/process/에 남기고, core 파일에는 최신 내용만 둔다.
  - `context/research/` — 조사 산출물(주장→근거 연결, 조사 정리). 리서치 루프가 갱신한다. 규칙은 context/core/research.md.
  - `context/problem/` — 문제 정의 산출물. 후보 비교판과 선택한 Problem Statement를 현재 상태로 다듬는다. 후보를 합치고·기각하고·선택한 이유는 context/process/에 남긴다.
  - `context/process/` — 매 대화 세션의 과정 기록(판단·결정·초안). 시간순으로 쌓이고, 과거 기록은 사후에 고쳐 쓰지 않는다.
  - `context/sources/` — 근거 원본. 무엇을 저장하고 무엇을 URL로만 남기는지는 context/core/research.md의 자료 보관 경계를 따른다.
- `src/` `logs/` `README.md` — 제출 형식(submission.zip = src/ + README.md + logs/).
- `samples/` — 검증용 샘플. zip에 넣으려면 src/ 안이어야 한다 — 위치는 구현 때 확정.

## 커밋 규칙

- 형식: `타입: 한국어 요약`. 본문은 필요할 때만.
- 타입:
  - `chore:` — 베이스라인, 도구·훅·설정
  - `context:` — context/ 문서 갱신. 하위 구분이 필요하면 scope로: `context(research):`, `context(sources):`, `context(process):`
  - `feat:` / `fix:` — src/ 플러그인 코드
  - `docs:` — README
  - `gate: [블록명] 통과` — 게이트 커밋. 본문에 해당 process 파일 경로를 한 줄 남긴다 (예: `process: context/process/02-problem-statement.md`). 게이트 커밋 = process 기록 존재 증명.
- 커밋 메시지에 AI 도구명·모델명 등 실행 환경 메타데이터를 남기지 않는다.

## 로그 규정 (제출용 — 어기면 실격 위험)

- 공식 log hooks가 설치되어 있다(`.claude/settings.json`, `.codex/hooks.json`, `tools/save_log.py`). Codex Desktop과 CLI는 신뢰 승인된 `Stop` 훅으로 매 turn 종료 시 `logs/codex/<session_id>.jsonl`을 자동 저장한다. `./tools/codex-start.sh`는 레포 루트에서 CLI를 여는 편의용이고, `./tools/codex-harvest.sh`는 훅 승인 전이나 훅 실패로 누락된 세션만 복구하는 비상용이다. 정상 작업 뒤에는 수동 수확이 필요 없다.
- `logs/`는 편집·발췌·삭제 금지. 사후 가공 시 실격.
- 대화에 API 키·비밀번호·토큰 등 비밀정보를 입력하지 않는다.
- 로그·플러그인·질문지·README의 정합성을 함께 평가한다 — 답변에 쓸 판단·기각·검증은 작업 중 대화에 실제로 남긴다.

## LazyCodex / Insane Search (로컬 전용)

- 전역 `~/.codex`에 설치하지 않는다. 루트 전용 홈 `.lazycodex-home/`에만 설치되어 있고, 실행은 `tools/lazycodex-local.sh` 래퍼로 한다 (래퍼가 HOME/CODEX_HOME을 격리한다).
- Insane Search는 omo 플러그인의 ultimate-browsing skill 안 Tier 1 엔진이다: `./tools/lazycodex-local.sh insane-search "<URL>" --json`
- 사용 기준: 일반 검색이나 평범한 fetch에는 쓰지 않는다. 403, WAF, JS 렌더링, YouTube 자막처럼 일반 접근이 막히거나 불안정한 자료만 escalation으로 쓴다.
- `.lazycodex-home/`은 커밋하지 않고, 제출물에도 포함하지 않는다.

## 제출 형식과 문항

- 상세 규정과 문항별 도움말(사실상 문항별 채점 기준)은 **context/core/requirements.md** — 까먹으면 안 되는 외부 제약의 정리판.
- 핵심만: submission.zip = `src/` + `README.md` + `logs/`. 문항3은 README.md와 일치. 근거는 AI가 확인 가능한 공개 자료만.
- 제출 전에 과제화면 원문을 다시 확인한다 — context/sources/ 캡처와 requirements.md는 확보 시점 기준이다.
