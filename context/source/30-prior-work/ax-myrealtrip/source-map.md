# Prior-work source map: AX MyRealTrip 작업본

- source ID: `prior-ax-myrealtrip-work`
- source class: 사용자의 기존 작업 방식 관찰 자료
- role in this project: 현재 context+harness 구조의 정답이 아니라, 실제 프로젝트에서 복구·선택·실행·검증·상태 반영을 어떻게 운영했는지 관찰하는 입력
- requested path: `/Users/hammyeong-yeon/Desktop/10_work/AX인재전쟁-해커톤/마이리얼트립제출/전체-작업본`
- resolved source root: `/Users/hammyeong-yeon/Desktop/10_work/AX인재전쟁-해커톤/10-마이리얼트립-제출/전체-작업본` (실제 파일시스템에서는 macOS NFD 한글 이름)
- snapshot date: `2026-08-12` (Asia/Seoul)
- Git branch: `main`
- Git HEAD: `7c1fa470e08cfb7fbc33cc4bcdbd26d764d6b95d`
- HEAD time: `2026-07-11T00:12:04+09:00`
- working tree at snapshot: clean
- preserved files: `snapshot/`
- byte manifest: `snapshot-manifest.tsv`
- verification ceiling: 파일 존재·내용·해시와 Git 상태를 확인했지만, 이 intake에서는 기록된 test·validator·ZIP 검증을 다시 실행하지 않음

## 관찰되는 연결

1. `CLAUDE.md`와 SessionStart hook이 새 세션에 진입 계약을 다시 주입하고, `current`와 `core`를 읽어 프로젝트·커서·다음 행동을 복구하게 한다.
2. `context/current.md`는 최신 지도, `context/core/*`는 안정 기준, `context/process/*`는 시간순 결정·기각·막힘·검증 기록을 서로 다른 파일이 소유한다.
3. `core/loop.md`는 goal → 구현 → 실제 입력과 fresh 판별 → 기준 승격을 연결하고, `core/research.md`는 원자료와 기존 후보판을 분리한 조사 방식을 고정한다.
4. process `09`, `14`, `26`, `27`은 사용자 정정, 기존 후보에서 독립된 2차 추출, 자체 fixture 통과와 실제 제품 통과의 분리, 판별 피드백의 계약 승격을 보여 준다.
5. process `30`, `31`은 0바이트 ZIP과 외부 업로드 실패를 성공 증거에서 제외하고 복구·대체 제출 상태로 남긴다.
6. `.codex/hooks.json`과 `tools/*`는 재진입·대화 보존·누락 세션 수확을 실행 경로로 만들고, `SKILL.md`·`state-contract.md`·test는 자연어 판단과 결정론적 상태 계약 및 검사를 연결한다.

## 중요한 drift

Git working tree가 clean이어도 모든 current-state 문서가 의미상 최신인 것은 아니다. `context/current.md`의 커서는 Loop 01에 남아 있지만, 더 늦게 작성된 process `30`과 `31`에는 최종 패키징과 업로드 실패가 기록되어 있다. 따라서 이 snapshot에서 `current.md`만 최종 상태로 인용하지 않고 HEAD와 후속 process를 함께 읽어야 한다.

## 보존한 대표 원본

- 재진입·상태 층위: `CLAUDE.md`, `context/current.md`, `context/core/loop.md`, `context/core/research.md`
- 시간순 판단과 correction: `context/process/README.md`, process `09`, `14`, `26`, `27`, `30`, `31`
- 실행 연결: `.codex/hooks.json`, `tools/codex-session-start.py`, `tools/save_log.py`, `tools/codex-harvest.sh`
- 실제 harness 계약과 검사: TripProof `SKILL.md`, `state-contract.md`, `test_tripproof.py`

## 의도적으로 복사하지 않은 자료

- `logs/codex/*.jsonl`: 직접 발화 원자료로서 강하지만 홈 절대경로와 session/task ID가 다수 포함된 비공개 자료라 별도 범위 승인 없이 복사하지 않음
- `.lazycodex-home/`: 약 737MB의 plugin·npm·venv·Library cache 중심 자료라 작업 방식 원자료로 취급하지 않음
- `.DS_Store`, `__pycache__`, `.pyc`, 설치 cache: 실행 부산물
- source 캡처 bundle과 과거 demo 전체: source 보존 방식이나 현재 계약을 증명해야 할 때만 원본·파생본 쌍으로 가져올 자료이며, 이번 대표 snapshot에서는 중복을 피함
- `src/` 전체: 이번 단계는 운영 방식 관찰이며 실행 가능한 TripProof 복사본을 만드는 단계가 아님
- 대화 로그가 가리키는 작업본 밖의 rollout·`/tmp` 상태: 이번 source 범위 밖이라 확인하지 않음

이 map의 설명은 원본 파일을 찾기 위한 파생 색인이다. 이후 설계에서 주장 근거가 필요하면 `snapshot/`의 해당 원본을 직접 확인한다.
