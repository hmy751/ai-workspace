# Context Harness 이식 계약

이 문서는 `output/`의 실행 원형을 실제 기존 Project에 옮길 때 유지할 책임과 대상마다 다시 판단할 부분을 분리한다. 첫 적용의 상세 원자료는 [`002 Project application record`](../../../../context/workspaces/002-project-application/records/2026-08-13-01-payment-recovery-project-application.md)에 있다.

## 세 산출물의 역할

- `output/`: Project–Workspace–Harness 관계가 실제로 실행되는 reference. 복사 템플릿이나 설치 패키지가 아니다.
- `.agents/skills/apply-context-harness/`: target을 조사하고 reference 책임을 맞춰 옮기고 검증하는 반복 절차. Project 사실을 소유하지 않는다.
- target Project: 자신의 canonical, Workspace 내용, 제품 코드, verify 명령과 acceptance를 소유한다.

skill을 다듬을 때 `output/`과 target 내용을 assets로 중복시키지 않는다. 일반화할 판단 규칙은 이 skill에, 실행 책임 변경은 `output/`에, 적용 결과와 예외는 해당 application Workspace records에 남긴다.

## 유지할 책임과 바꿀 배치

| 구분 | 모든 이식에서 유지 | 대상마다 다시 결정 |
| --- | --- | --- |
| Owner | Project common, Workspace, Harness를 분리 | 기존 canonical 문서와 routing 위치 |
| Workspace | README, 최소 memory 3종, 빠른 state, 독립된 source, goal output index, 누적 records | ID, active 선택, 실제 목표·제약·Project 선택 경계·원자료·goal 산출물·다음 행동 |
| recover | current, output index와 선언된 Project 문서만 선택하고 source·records·output 본문 배제 | Project context root, schema version, 선택 문서 |
| path | Project root와 Work root 구분, absolute·traversal·symlink 거부 | Python package 충돌과 실제 상대 경로 |
| verify | shell 없는 고정 argv, evidence 선캡처, 성공·실패 receipt | runtime, cwd, timeout, cache bypass, evidence closure |
| status | machine 결과와 최신 receipt cursor 연결 | 사람용 상태 문구와 실제 acceptance 절차 |
| 제거 가능성 | Harness 제거 뒤에도 canonical과 Workspace 의미 유지 | repo-local routing과 ignore 규칙 |

`context/project/` 경로 자체는 invariant가 아니다. 기존 루트 README와 `docs/`가 canonical이면 그 Owner를 유지하고 recover 허용 경계만 명시적으로 바꾼다.

각 Workspace의 `current/`, `source/`, `output/`, `records/`는 형제 책임이다. `current/memory/`의 `01-goal.md`, `02-constraints.md`, `03-project-context.md`는 기본 재진입에 필요한 최소 구성이다. `source/index.md`는 source inventory의 최소 진입점이며, 실제 사용한 원문·변경하지 않은 snapshot·provenance만 연결한다. 별도 원자료가 없으면 없다고 적고 Project canonical을 복제하지 않는다. 해당 Workspace는 선택 범위·사용 시점·무결성·재접근 경로를 관리하며 원자료의 저자와 정본 권위는 원래 출처에 남는다. 현재 판단은 `current/`에 둔다.

`output/index.md`는 Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치의 최소 진입점이다. 실제 산출물이 Project 코드·문서·배포 위치에 있으면 복제하지 않는다. 분석 초안·후보 비교·탈락 사유·시행착오·선택 근거·교체된 이전 결과·검증 과정은 날짜가 있는 `records/`에 유지한다. 분석 문서도 goal 결과로 선택되면 output에서 찾게 하므로 파일 형식이 아니라 역할로 구분한다. Output 등재는 acceptance나 Workspace 완료를 뜻하지 않는다. Recover는 source를 검사하지 않고 output index만 기본 입력으로 읽으며 output artifact 본문과 records는 싣지 않는다.

## Preflight가 증명하는 것

`capture_target_state.py` receipt는 다음을 실행 전에 관찰한 사실로 고정한다.

- target Git root, branch, HEAD
- tracked worktree 변경, staged 변경, untracked 파일
- 각 dirty/untracked 파일의 현재 kind, byte size, SHA-256 또는 symlink target
- 적용 범위에서 발견한 `AGENTS.md`, `CLAUDE.md`의 위치와 hash
- 사람이 읽을 수 있는 porcelain status

이 receipt는 한 번의 local capture pass에서 순차 관찰한 결과이며 Git lock을 잡은 atomic snapshot이 아니다. 동시 writer가 있으면 status와 file hash가 서로 다른 순간을 반영할 수 있다. 또한 파일의 저자, 변경 이유, 삭제 주체, Git 밖의 과거 상태를 증명하지 않는다. 사용자 발화와 실제 이후 행동을 구분해서 기록한다. Hash 연속성은 "내용이 같음"을 지지할 뿐 "누가 만들었음"을 증명하지 않는다.

Receipt를 target 안에 바로 쓰면 그것도 working tree 변경이 되므로 기본 흐름은 `/private/tmp`에 먼저 쓰고, Workspace records 생성 후 exact copy하는 것이다. 복사 전후 SHA-256이 같은지 확인한다.

## 충돌과 dirty tree 처리

다음 순서로 보호한다.

1. preflight dirty path와 이식 manifest의 교집합을 계산한다.
2. 교집합이 없으면 exact file additions와 좁은 patch로 계속한다.
3. 교집합이 있으면 기존 Owner, 사용자가 기대한 내용, additive routing 가능성을 확인한다.
4. 의미를 바꾸는 선택이 남으면 사용자에게 충돌 파일과 선택지를 제시한다.
5. `git add context/`처럼 기존 untracked 파일까지 포함할 수 있는 broad staging을 금지한다.

기존 `context/` 디렉터리는 빈 설치 자리가 아니다. 개인 code map, 다른 도구 상태, 제품 runtime package가 먼저 존재할 수 있다. directory replace, broad recursive copy, 자동 이동·삭제를 하지 않는다.

## Recover adaptation의 최소 테스트

Project context 경계를 바꿨다면 적어도 다음을 target Harness tests에 둔다.

- 선택한 문서만 loaded 되고 순서가 계약과 같은 경우
- 최소 memory 세 파일 중 하나라도 없으면 실패하는 경우
- output index가 없거나 symlink·비정규 파일이면 실패하는 경우
- output index만 loaded 되고 output artifact 본문은 빠지는 경우
- 선택하지 않은 Project 문서, records, verify 계약이 빠지는 경우
- Workspace source inventory와 원문이 기본 recovery packet에서 빠지는 경우
- Project root와 Work root 상대 경로가 올바르게 분리되는 경우
- legacy schema 또는 지원하지 않는 schema 거부
- absolute path와 `..` traversal 거부
- 허용 root 밖의 undeclared path 거부
- non-Markdown 파일 거부
- symlink와 비정규 파일 거부

테스트 source 자체를 제품 verify evidence와 혼동하지 않는다. target-specific 변경의 현재 결과는 별도 Harness test receipt로 연결한다. Receipt helper는 임의 command를 받지 않고 현재 Python의 `unittest discover`만 실행해야 하며, timeout 때 같은 process group을 종료해야 한다. Test count가 0이거나 unittest 요약을 캡처하지 못하면 process exit가 0이어도 실패로 기록한다. stdout·stderr는 동시에 drain하되 설정한 byte prefix만 메모리에 보존한다. 새 session을 만들어 process group을 벗어난 descendant까지 격리하는 sandbox는 아니다.

## Verify evidence closure

Evidence 목록은 파일 수를 맞추는 일이 아니다. 고정 argv가 수행하는 task graph의 입력을 설명할 수 있어야 한다.

1. root argv가 호출하는 package manager, task runner, script를 펼친다.
2. root lockfile, workspace 선언, task runner 설정, 공통 compiler/build 설정을 찾는다.
3. 실제 실행 대상 package마다 tracked source, package manifest, package-local compiler/build/test 설정을 모은다.
4. runtime에서 읽는 fixture, scenario, schema, generated input이 있으면 포함한다.
5. 의도적으로 제외한 generated output, external service state, environment variable은 proof ceiling에 적는다.
6. evidence를 실행 전에 hash하고 그 뒤 같은 process에서 명령을 실행한다.

Cache hit 출력만으로 fresh pass를 선언하지 않는다. 도구가 제공하는 force/no-cache option을 고정 argv에 넣거나, cached validation이라는 한계를 명시한다. 전체 task 출력이 pass를 보고해도 evidence 목록이 입력을 닫지 못하면 "명령 출력상 통과"와 "어떤 tree가 검증됐는지"를 분리해서 말한다.

## 첫 적용에서 보존할 학습

첫 적용의 구체적인 시도·숫자·결과는 문서 첫머리의 application record 링크에서 읽는다. 이 skill에는 다음 일반화된 판단만 유지한다.

- 기존 canonical이 있으면 새 `context/project/`를 만들지 말고 recover 허용 경계를 대상에 맞춘다.
- 사용자 파일 보호를 사후 정황에 맡기지 말고 첫 쓰기 전에 preflight receipt를 만든다.
- runtime과 cache 의미를 미리 확인하고 fresh 실행이 아니면 그 한계를 숨기지 않는다.
- evidence는 중요 파일 표본이 아니라 실제 task graph의 입력을 설명하도록 닫는다.
- 제품 verify와 target-specific Harness test의 증거를 분리한다.
- typecheck, unit test와 build 결과를 브라우저·외부 시스템·사람 acceptance로 확장하지 않는다.

## 자동화하지 않을 판단

- 어떤 문서가 canonical인지와 누가 Owner인지
- 어떤 Workspace가 active여야 하는지
- 사용자 파일 삭제·이동·승격
- 임의 검증 명령의 신뢰 승인
- cache 결과를 fresh proof로 승격
- 일부 hash로 전체 task tree를 대표한다는 선언
- pass 뒤 acceptance, completion, canonical 반영, commit
- concurrent verify와 receipt/status transaction 보장

이 판단은 target 원자료, 사용자 권한, 실제 실행 결과를 함께 보고 main이 맡는다. helper script는 관찰과 기록만 결정적으로 만든다.

## Proof ceiling 문장 틀

다음 네 문장을 target 사실로 채워 migration record와 최종 보고에 남긴다.

1. "이번 recover는 Workspace current N개와 선택한 Project 문서 M개만 불러왔으며, 제외 목록 X는 포함하지 않았다."
2. "이번 verify receipt는 실행 전 evidence K개의 hash를 보존했고, 고정 argv의 종료 상태와 출력은 Y를 보고했다."
3. "이 결과는 A·B·C를 확인하지만, 외부 환경 D와 사람 acceptance E는 확인하지 않는다."
4. "Harness pass는 `verified_waiting_acceptance`이며 Project 완료나 사용자 수락을 뜻하지 않는다."
