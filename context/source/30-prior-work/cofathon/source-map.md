# Prior-work source map: cofathon

- source ID: `prior-cofathon-work`
- source class: 사용자의 기존 작업 방식 관찰 자료
- role in this project: 현재 context+harness 구조의 정답이 아니라, 실제로 어떤 상태 소유·재진입·판단·검증 방식을 사용했는지 관찰하는 입력
- source root: `/Users/hammyeong-yeon/Desktop/10_work/cofathon`
- snapshot date: `2026-08-12` (Asia/Seoul)
- Git branch: `main`
- Git HEAD: `d99c7b95391849f0955fc20f97aa1a3b7988480c`
- snapshot basis: 현재 working tree
- working tree at snapshot: `context/current.md`, `context/process/README.md` 수정; `context/process/39-publish-sanitized-public-copy.md`, `q1-application/` untracked
- preserved files: `snapshot/`
- byte manifest: `snapshot-manifest.tsv`
- verification ceiling: 파일 존재·내용·해시와 Git 상태를 확인했지만, 이 intake에서는 test나 hook을 실행하지 않음

## 관찰되는 연결

1. `CLAUDE.md`가 새 세션과 compaction 뒤의 재진입 계약을 제공한다. 원본의 `AGENTS.md`는 이 파일을 가리키는 symlink라 중복 복사하지 않았다.
2. `context/goal.md`는 장기 목표와 완료 의미, `context/current.md`는 현재 지도와 단일 다음 커서, `context/core/*`는 단계가 바뀌어도 유지할 판단 기준과 loop를 소유한다.
3. `context/process/*`의 대표 기록은 현재 구조가 한 번에 정답으로 생긴 것이 아니라, current-map 우선, goal-loop 통합, 내부 평가 주기, 재진입 책임, 잘못된 산출물 폐기, 사용자 장면 기반 재선택으로 수정된 과정을 보여 준다.
4. `.codex/hooks.json` → `tools/codex-session-start.py` → `tools/tests/test_codex_session_start.py`는 재진입 지침이 문서에만 있지 않고 실행과 검증으로 연결된 예다.
5. `context/sources/README.md`는 raw source와 파생 표현의 경계를, `SKILL.md`와 `state-contract.md`는 자연어 지침과 결정론적 상태 계약의 연결을 보여 준다.

## 보존한 대표 원본

- 상태 소유: `CLAUDE.md`, `context/current.md`, `context/goal.md`, `context/core/README.md`, `context/core/loop.md`, `context/core/dev-principles.md`
- 판단 변화: process `02`, `27`, `31`, `34`, `36`, `38`
- 재진입 실행과 검증: `.codex/hooks.json`, `tools/codex-session-start.py`, 관련 test
- source 경계: `context/sources/README.md`
- 실제 harness 계약: tour-purchase-review의 `SKILL.md`, `state-contract.md`

## 의도적으로 복사하지 않은 자료

- `logs/codex/*.jsonl`: 실제 사용자·AI 발화와 민감정보 가능성이 있어, 별도 범위 승인 없이 복사하지 않음
- cache, `.lazycodex-home`, `__pycache__`: 이번 관찰 목적과 무관한 실행 부산물
- 대용량 test·fixture·host-smoke 상태: 실행 재현 단계가 아니므로 canonical 경로만 남기고 중복 복사하지 않음
- `q1-application/`과 process `39`: untracked 상태이며 현재 source snapshot의 대표 축으로 채택하지 않음
- 원본 페이지 bundle 전체: cofathon 내부에서도 raw와 파생본이 중복되므로, 이번에는 그 보존 규칙을 설명하는 README만 복사함

이 map의 설명은 원본 파일을 찾기 위한 파생 색인이다. 이후 설계에서 주장 근거가 필요하면 `snapshot/`의 해당 원본을 직접 확인한다.
