# SessionStart 재진입과 지침 소유권 정리

날짜: 2026-07-17

상태: **구현·구성요소 검증 완료 / 다음 main 작업 end-to-end 확인 남음**

## 계기

프로젝트는 `AGENTS.md → CLAUDE.md` 자동 로드와 `.codex/hooks.json`의 `SessionStart`를 함께 사용해 새 Codex 작업에서 현재 지도를 읽고 사용자와 위치를 맞춘다. 실제 사용에서는 대체로 작동했지만 다음 문제가 확인됐다.

- `CLAUDE.md`가 재진입 행동뿐 아니라 Goal·트랙·리서치 판단·현재 솔루션 상태를 다시 복제했다.
- `현재 작업의 고정 경계`에는 다른 문서가 소유하는 현재 결론과 이미 끝난 후보 탐색 단계의 교정 문구가 섞였다.
- 시작 문단과 문서 층위가 같은 네 문서의 역할을 반복 설명했다.
- SessionStart script가 `startup / resume / clear / compact`를 구분하지 않아 작업 중 자동 compact에도 `복기 후 정지` 계약이 다시 전달될 수 있었다.
- hook JSON·marker·symlink의 구성요소 검증은 있었지만, 실제 hook 호출 source와 당시 파일 상태를 나중에 확인할 실행 흔적은 없었다.
- `current.md`는 process/02에서 지도 중심으로 줄인 뒤 다시 세부 후보 이력을 품어 82줄까지 커졌다.

## 다시 잡은 소유권

`CLAUDE.md`는 다음만 직접 소유한다.

- 사용자와 직접 대화하는 main 작업의 재진입 행동
- 문서 층위와 각 소유 문서로 가는 입구
- 하위 context 문서가 대신할 수 없는 프로젝트 hook·로컬 로그·커밋 경계

프로젝트의 현재 사실과 판단은 기존 소유 문서가 계속 담당한다.

- Mission·Campaign Goal — `context/goal.md`
- 현재 위치·방향·단일 커서 — `context/current.md`
- 공식 요구사항 — `context/core/requirements.md`
- 지원 증거물 형태·증거 계약 — `context/core/support-evidence-artifact.md`
- Cofathon·Probe·FDE 출처 역할과 리서치 판단 — `context/research/00-current-synthesis.md`
- 선택한 제품 동작과 다시 열 조건 — `context/solution/00-selected-solution.md`
- 구현 Goal·loop 상태·검증 증거 — `context/engineering/`
- 프로젝트 전반의 개발·근거·검증 원칙 — `context/core/dev-principles.md`

따라서 `현재 작업의 고정 경계`는 다른 곳으로 복사하지 않고 제거한다. 이는 Goal이나 증거 계약을 바꾸는 일이 아니라 이미 존재하는 원본의 소유권을 회복하는 정리다.

## 사용자 재검토로 바로잡은 경계

첫 정리에서는 `support-evidence-artifact.md`를 여전히 세션 필수 선독에 따로 두고, `작업·검증 규칙`을 실행 전에 중요한 직접 규칙이라는 이유로 `CLAUDE.md`에 남겼다. 사용자는 문서 층위가 이미 해결하는 내용을 왜 다시 특별 취급하는지 재검토를 요청했다.

대조 결과 `core/README.md`가 지원 증거물 계약을 포함한 활성 core 문서의 색인과 읽는 경로를 이미 소유한다. `작업·검증 규칙`의 단계 경계·loop·개발 원칙·반복 공개 조사·브라우저 경계·Q1 재확인도 각각 `core/README.md`, 관련 core 문서와 단계별 README에 있었다. 독립적으로 `CLAUDE.md`만 소유해야 하는 규칙은 없었다.

따라서 세션 필수 선독은 `current.md`, `goal.md`, `core/README.md` 세 입구로 줄이고, 지원 증거물 계약은 core 색인과 현재 작업 관련성에 따라 읽는다. `작업·검증 규칙` 절은 제거하고 실제 규칙과 읽는 시점은 기존 소유 문서가 계속 담당한다.

## 재진입 동작

- `startup / resume / clear` — main은 필수 세 입구 문서를 읽고, 첫 final 응답에서 Mission·현재 커서·다음 판단을 복기한 뒤 사용자 확인 전까지 새 작업을 시작하지 않는다. 도구 사용 전 짧은 commentary는 허용한다.
- `compact` — 같은 문서를 최신 기준으로 다시 확인하되 진행 중인 작업을 보존하고, 시작 복기나 사용자 재확인을 새로 요구하지 않는다.
- subagent·guardian·독립 판별자 — main용 복기·정지 계약을 적용하지 않는다. 위임 범위와 독립성 계약을 따르고 결과를 부모에게 보고한다.

SessionStart hook은 stdin의 `source`를 읽어 main 재진입과 compact refresh를 다르게 전달한다. hook 호출 때 `session_id`, `source`, 재진입 원문과 실제 전달 context의 hash, 필수 파일 snapshot hash를 `logs/codex/session-start-hooks.jsonl`에 남긴다. 이 로그는 **hook이 실행되고 어떤 파일 상태를 가리켰는지**만 증명하며, 모델이 실제로 파일을 읽고 복기했다는 증거로 확대하지 않는다.

## current 정리 원칙

- Goal·공식 요구·트랙·지원 증거물·리서치·문제–솔루션·엔지니어링·제출의 전체 생애주기는 남긴다.
- 완료·철회된 세부 후보 이력은 현재 효력 한 줄과 상세 원본 링크만 남긴다.
- 현재 커서에서만 남은 상태와 다음 판단이 보이도록 깊어진다.
- Mission, 선택 솔루션, Loop 01 완료, 미검증 가치, 다음 loop 선택 전이라는 현재 의미는 바꾸지 않는다.

## 검증 계획

- `CLAUDE.md`에서 제거한 현재 결론이 각 소유 문서에 남아 있는지 확인한다.
- hook script를 `startup`, `resume`, `clear`, `compact`, 알 수 없는 source로 실행해 출력 모드를 확인한다.
- audit JSONL이 호출과 파일 snapshot을 남기며 hook 출력 JSON을 오염시키지 않는지 확인한다.
- `current.md`의 단일 커서와 활성 Goal·Loop 01 상태·남은 검증 부채가 유지되는지 확인한다.
- 실제 다음 main 작업에서는 필수 문서 선독과 첫 final 복기·정지를 사용자와 다시 확인한다. 이 마지막 항목은 구성요소 검증과 구분해 다음 작업의 end-to-end 확인으로 남긴다.

## 구현 결과

- `CLAUDE.md`의 `현재 작업의 고정 경계`와 중복 `작업·검증 규칙`을 제거하고, main 재진입·문서 층위의 입구와 하위 문서가 대신하지 않는 로컬 경계만 직접 소유하게 했다. 다른 곳에 이미 있는 현재 결론이나 운용 규칙을 새 문서로 옮겨 복제하지 않았다.
- LazyCodex와 개인 로그의 상세 runbook은 `tools/README.md`로 내리고, `CLAUDE.md`에는 실행 전 필요한 경계와 진입 링크만 남겼다.
- `codex-session-start.py`가 stdin의 `source`를 읽어 `startup / resume / clear`와 `compact`를 다른 developer context로 출력하게 했다. 알 수 없는 source는 계약 누락보다 안전한 main 재진입으로 처리한다.
- hook 호출의 `session_id`, `source`, 출력 mode, 재진입 원문·실제 전달 context hash, 필수 세 입구 문서의 byte·hash snapshot을 gitignored audit JSONL에 남긴다.
- `current.md`를 82줄·17,381 bytes에서 47줄·6,943 bytes로 줄였다. 전체 생애주기와 현재 결론은 유지하고, 완료된 후보 이력은 원본 링크로 접었으며 다음 loop 선택에만 깊이를 남겼다.
- source 분기와 audit snapshot을 고정하는 `tools/tests/test_codex_session_start.py`를 추가했다.

## 구성요소 검증 결과

- `startup / resume / clear` → `COFATHON_SESSION_START_V2`, `compact` → `COFATHON_CONTEXT_REFRESH_V2`, 알 수 없는 source → main 재진입으로 출력되는 것을 확인했다.
- 다섯 번의 실제 script 호출에서 audit에 source·mode와 세 대상 파일 hash가 기록되고, stdout의 hook JSON이 유효하게 유지됐다.
- `python3 -m unittest discover -s tools/tests -p 'test*.py' -q`의 9개 test가 통과했다.
- `.codex/hooks.json` JSON 검증, 변경 문서의 직접 링크 존재, `AGENTS.md → CLAUDE.md` symlink, `current.md`의 실제 커서 한 개, `git diff --check`를 확인했다.
- 이 검증은 hook 구성요소와 문서 일관성을 확인한 것이다. 실제 다음 main 작업에서 모델이 세 입구 문서를 읽고 첫 final 복기 뒤 멈추는 행동은 아직 증명하지 않았으며, 그때 사용자 관찰로 확인한다.
