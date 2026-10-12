# 수집 방법 기록

2026-08-08, Claude Code 세션에서 두 라운드의 병렬 수집으로 만들었다. 이 문서는 다음 판단 세션이 "이 수집의 필터가 무엇을 걸렀는지"를 재검토할 수 있게 남기는 기록이다.

## 실행 구성

- 1차: 수집 agent 14개 (하네스 인벤토리 2, spec 대조 3, 기록 흔적 1, 로그 스캔 1, 발췌 5, 사용 흔적 1, 커버리지 점검 1).
- 2차 (1차 커버리지 점검이 찾은 구멍 보강): agent 8개 (미대조 spec 3, run 실물 대조 1, 영어 스캔 1, 누락 문서 3).
- 모델·추론 배치: 기계적 수집(인벤토리, grep, 발췌)은 Opus 중간 추론, 판정이 들어가는 사실 확정(spec-코드 대조, 사용 흔적 확정, run 대조, 커버리지 점검)은 Fable 높은~최상 추론. 문제 명명·원인 판단은 이 수집에서 하지 않았다.

## 모든 agent에 걸었던 공통 규칙

- 문제 명명, 원인 판단, 개선 제안, "~가 문제다", "~가 안 쓰였다" 결론 금지.
- 인용은 원문 그대로 + 위치(파일:줄).
- 각 산출물 끝에 "## 방법"(실행 명령·읽은 것·안 읽은 것)과 "## 예외"(예상 밖 충돌, 해석 없이) 기록.
- repo 수정 금지, 읽기 전용. 개인 식별 정보는 마스킹.

각 evidence 파일의 "## 방법"·"## 예외" 절이 그 파일의 1차 방법 기록이다. 이 문서는 파일들을 가로지르는 선별 기준과 노이즈만 모은다.

## 로그 스캔의 선별 기준 (재검토 지점)

스캔 대상: `archive/private/2026-08-04/.ai-conversation-logger/conversations/` 의 claude-code 21개 + codex 603개 = 624개 jsonl 전수. 각 줄을 json 디코드해 `role == "user"`의 `text`만 검색했다 (스크립트: `scripts/07-scan.py`, `scripts/14-scan-english.py`).

한국어 패턴 (07):
- friction: 그게 아니라 / 그런 뜻이 아니 / 아니 그 / 다시 해 / 다시해 / 왜 마음대로 / 하지 말 / 하지마 / 그만 / 되돌려 / 롤백 / 원래대로 / 내 말은 / 포인트가 아니 / 이상하 / 잘못됐 / 잘못된 / 틀렸
- cogdebt: 와닿 / 이해가 안 / 이해 안 / 무슨 소리 / 무슨소리 / 모르겠 / 헷갈 / 복잡해 / 복잡하 / 어렵 / 설명해 / 설명이 / 뭐가 뭔지 / 파악이 안
- spec: 스펙 / spec / 슬라이스 / slice / 계약

영어 패턴 (14): friction-en (no, / no. / wrong / that's not / stop / revert / undo / don't / not what i / incorrect / mistake 등), cogdebt-en (confus / don't understand / unclear / hard to follow / doesn't make sense / what do you mean).

발췌 컷라인:
- 매치 세션 527개 전량 집계는 `evidence/07-log-sweep.json` (total 내림차순).
- 구조화 반환에는 `total >= 7` 또는 `friction + cogdebt >= 3`인 210개만 담겼다 (출력 길이 한계 대응, 07-log-sweep-method.md에 자기 기록 있음).
- 장면 발췌는 total 상위 40개 세션만 (batch-1~5, 세션 8개씩). 매치됐지만 발췌 안 된 487개 세션은 JSON 집계로만 남았다.
- 영어 스캔은 46장면 전부 발췌 (컷 없음).

## 알려진 노이즈 (수치를 읽을 때 주의)

- spec 태그 4,922건에는 경로 문자열(`spec/`, `specs/`), skill 이름, 브랜치 이름 매치가 포함된다. 의미 구분을 하지 않았다.
- friction의 "그만"은 "그만큼", "그만두" 안에서도 매치된다. 영어 "stop"/"dont"/"no."도 hook 이름·경로·다른 어절 안에서 매치된다.
- codex 로그 13개 파일에는 "The following is the Codex agent history…"로 시작하는 승인 검토 envelope 246 레코드가 user role로 저장돼 있다. 07 전수 스캔은 이것을 통째로 user 텍스트로 집계했다 (14 영어 스캔만 내부 `[N] user:` 블록 337개를 분리 집계했다). batch-1이 2.8MB인 주된 이유가 이 envelope 원문 수록이다.
- 수치 단위 차이: 07-scan.py는 부분 문자열 출현 횟수(str.count), batch 문서들은 매치 턴/장면 수를 센다. 같은 세션의 두 수치는 단위가 다르다 (09-coverage-gaps.md 예외 절).
- batch별 장면 병합 기준이 조금씩 다르다 (batch-1·3·4: 매치 인덱스 간격 4 이하 병합, batch-2: 4/3, batch-5: 6 이하).
- claude-code `12e5d860` 세션에 동일 레코드 중복 저장, 4,932자 동일 발화가 codex 세션 14개에 반복 — 집계 부풀림 요인.

## 2차로 닫은 구멍 (09-coverage-gaps.md 기준)

- G-1 (spec 인용 run 실물 미대조) → 13. 이 대조로 04 문서 12항목, 05 문서 9항목의 [확인 불가]가 재판정 가능해졌다 (13에 목록, 04·05 본문은 수정하지 않음).
- G-2 (material-research 미열람) → 17.
- G-3·G-6 (prd/product-model/MANIFEST/spec-driven 원 문서 미열람) → 15.
- G-4 (spec 묶음 7개 중 5개 미대조) → 10·11·12.
- G-5 (폴더형 decisions 7개 누락) → 16.
- G-7 (영어 패턴 부재) → 14.
- G-11 (보조 스크립트 미기재) → scripts/ 폴더로 이동, 이 문서에 명시.

## 남은 구멍 (수집하지 않은 것과 이유)

- assistant 발화 (codex 12,684 + claude-code 2,218 레코드)의 패턴 스캔. user 발화의 마찰 장면이 우선이라 범위에서 제외했다. AI 쪽 서술(설명 방식)을 원문으로 보려면 이 스캔이 필요하다.
- 장면 발췌의 표본 한계: 한국어 상위 40 + 영어 32 세션. 나머지는 JSON 집계뿐.
- 테스트·서버·LLM·Supabase 실행 일체. spec의 "203 passed" 류 pytest 수치와 runtime AC는 실행 없이는 확정 불가라 [확인 불가]로 남겼다.
- git 브랜치별 이력·머지 구조·reflog·원격 상태 미조회 (커밋 제목 316건과 개별 git show 일부만 확인).
- 현재 코드 일부 미열람 영역: observations 모듈 대부분, client api/*.ts 일부, eval 스크립트 본문 일부, Supabase migration RPC 본문 45행 이후 등 (각 spec 대조 문서의 방법 절에 파일 단위로 기재).
- prd.md·product-model.md의 제품 기능 서술부 (프로세스 문장만 수집).

## 원자료 위치

- 하네스·문서 동결본: `~/Desktop/10_work/tripproof/archive/2026-08-04-pre-harness-reset/` (commit `ea97458` 기준, MANIFEST.md 참고)
- 대화 로그·run 실물·자료 조사: `~/Desktop/10_work/tripproof/archive/private/2026-08-04/` (gitignore 영역)
- 현재 코드 대조 기준: branch `chore/archive-project-harness`, HEAD `14628cf`, 2026-08-08 시점 working tree
