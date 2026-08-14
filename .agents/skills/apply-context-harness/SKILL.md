---
name: apply-context-harness
description: 기존 개발 Project 하나에 context harness를 기존 canonical과 사용자 변경을 보존하며 최소 이식하고 recover, fixed verify, receipt, 재진입까지 실제 검증한다. 사용자가 대상 경로와 함께 "context harness 이식/적용", "output을 다른 프로젝트에 붙여줘", "Workspace current/source/output/records와 recover/verify를 설치해줘"라고 요청할 때 사용한다. 단순 output 수정, 구조 설명, 이미 설치된 Project의 브라우저 acceptance만 수행하는 요청에는 사용하지 않는다.
---

# Apply Context Harness

## 목적

이 저장소의 `output/`에서 검증한 책임을 대상 Project의 기존 소유 구조에 맞춰 이식한다. 폴더 모양을 복제하는 대신 Project common, Workspace, Harness의 Owner 관계와 `recover → verify → recover` 순환을 실제 증거로 복원한다.

`output/`은 실행 가능한 원형이고 이 skill은 이식 절차다. `output/`을 skill assets로 복제하지 말고, 호출 시점의 live source와 commit을 읽어 사용한다.

## 시작 조건

1. 대상 Project의 절대 경로와 사용자가 허용한 변경 범위를 확인한다.
2. 대상이 지정되지 않았으면 경로와 첫 Workspace로 다룰 작업 장면을 한 번에 묻고 멈춘다.
3. 대상이 지정됐으면 인접 저장소를 열지 말고 바로 preflight를 시작한다.
4. 이 skill의 [`references/application-contract.md`](references/application-contract.md)를 끝까지 읽는다.
5. `git -C <skill-dir> rev-parse --show-toplevel`로 source repository root를 구하고 `output/`의 존재를 확인한다. 상대 경로 단계 수로 repository root를 추측하지 않는다.
6. `git -C <source-root> status --short -- output`으로 source bytes가 source commit과 같은지 확인한다. `output/`이 dirty면 commit만 기록하고 진행하지 않는다. 현재 dirty bytes를 이식할지 먼저 사용자에게 알리고, 승인되면 dirty path 전체의 diff와 SHA-256을 manifest에 넣는다. 아니면 source 변경을 별도 작업으로 먼저 확정한다.

## 1. 변경 전 상태를 고정한다

대상에 어떤 파일도 만들거나 고치기 전에 다음을 수행한다.

1. 대상 경로에 적용되는 `AGENTS.md`, `CLAUDE.md`와 그 밖의 로컬 지침을 읽는다.
2. 대상 Git root, branch, HEAD, remote 유무, tracked·untracked·ignored 상태를 확인한다.
3. 다음 helper로 dirty/untracked 파일의 현재 hash와 적용 지침을 임시 append-only receipt로 캡처한다.

```bash
python3 <skill-dir>/scripts/capture_target_state.py \
  --project-root <target-project-root> \
  --output-dir /private/tmp
```

4. receipt를 읽어 사용자 변경, 삭제 상태, untracked 파일, 같은 이름의 기존 `context/`·`AGENTS.md`를 보호 목록으로 만든다.
5. 이 receipt는 내용 저자나 변경 주체를 증명하지 않는다. "이식 직전 관찰한 상태"로만 사용하고, Workspace records가 생기면 바이트를 바꾸지 않은 채 그곳에 보존한다.

기존 dirty tree가 있다는 이유로 멈추지 않는다. 다만 이식 파일과 경로가 겹치거나 사용자 변경을 덮어쓸 수 있으면 충돌 파일과 선택지를 제시하고 사용자 판단을 받는다.

## 2. 대상의 Owner 지도를 만든다

다음을 원자료에서 확인하고 migration record에 명시한다.

- Project 공통 목표·구조·결정·공개 상태를 현재 어느 문서가 소유하는가.
- 진행 중인 첫 작업의 정체성, 계속 유효한 memory, 빠르게 바뀌는 state, 작업이 직접 선택한 source, goal 산출물과 canonical 위치, records를 어디에 둘 것인가.
- 제품 검증의 기존 명령, runtime, cwd, timeout, cache 의미와 실제 입력 범위는 무엇인가.
- 기존 `context/`, Python package, `.gitignore`, instruction file과 어떤 충돌이 있는가.
- 자동 검증이 증명하지 못하는 브라우저·외부 시스템·사람 판단은 무엇인가.

기존 Project canonical이 이미 있으면 그대로 Owner로 유지한다. `output/context/project/`가 있다는 이유로 `context/project/` 복제본을 만들지 않는다. Owner가 불명확해 recover 허용 경계나 상태 책임이 달라질 수 있을 때만 사용자에게 결정 질문을 한다.

## 3. dry-run manifest를 먼저 만든다

파일을 합치기 전에 대화나 작업 기록에 다음 manifest를 제시한다.

- source commit, `output/` clean/dirty 상태와 dirty source를 쓸 때의 path별 hash·diff
- 새 파일, 수정 파일, 충돌 파일, 명시적 제외 파일
- Project canonical routing
- Workspace ID와 active 선택
- 첫 Workspace의 최소 memory인 `01-goal.md`, `02-constraints.md`, `03-project-context.md`에 둘 실제 내용
- 첫 Workspace가 작업 입력으로 보존할 원문·snapshot·provenance, `source/index.md` inventory, `source/`에서 명시적으로 제외할 현재 판단·분석·실행 기록
- `output/index.md`에서 연결할 goal 산출물, 실제 canonical 위치, 현재 상태와 proof ceiling. 대상 Project에 이미 산출물이 있으면 복제하지 않는다.
- `recover.json`이 선택할 정확한 Project 문서와 선택 이유
- `verify.json`의 고정 argv, cwd, timeout, output limit, fresh-run 방법
- 검증 명령이 실제 읽는 source·manifest·설정 전체를 대표하는 evidence 목록
- 남을 proof ceiling과 사람 acceptance 지점

샘플 Project 문서, sample Workspace 내용, 과거 receipt, `output/src`, `output/tests`, `__pycache__`는 payload에 포함하지 않는다. 기존 디렉터리 위에 광범위한 recursive copy를 하지 않는다.

## 4. 책임 단위로 이식한다

대상에 필요한 최소 산출물을 additive하게 만든다.

1. 일반 진입점에서 Project common과 Work context의 Owner 관계를 찾게 한다. 기존 `AGENTS.md`나 context index가 있으면 교체하지 말고 충돌 없는 routing만 추가한다.
2. `context/work/workspaces/` 아래에 Workspace collection, active index, 첫 Workspace의 README·계약·`current/`·`source/`·`output/`·`records/`를 만든다. `current/memory/`에는 최소한 `01-goal.md`, `02-constraints.md`, `03-project-context.md`를 둔다. `source/index.md`를 source inventory의 최소 진입점으로 만들고, 실제 사용한 원문·변경하지 않은 snapshot·provenance만 연결한다. 별도 원자료가 없으면 없다고 적고 Project canonical을 복제하지 않는다. 원자료의 저자와 정본 권위는 원래 출처에 남긴다. 현재 판단·분석·결정·실행·검증 기록은 source에 섞지 않는다.
3. `output/index.md`를 Workspace goal을 위해 선택된 현재 산출물의 최소 진입점으로 만든다. 실제 산출물이 Project의 기존 코드·문서·배포 위치에 있으면 복제하지 않고 canonical 경로를 연결한다. Output에는 선택된 결과와 상태·proof ceiling만 두고, 분석 초안·후보 비교·탈락 사유·시행착오·선택 근거·교체된 이전 결과는 날짜가 있는 records에 남긴다. 파일 형식이 아니라 Workspace goal에서 맡는 역할로 둘을 구분하며, output 등재를 acceptance나 완료로 해석하지 않는다.
4. `context/work/harness/`에는 `output/context/work/harness/`의 실행 책임만 옮긴다. Harness가 Project 기준이나 사람 판단을 소유하게 하지 않는다.
5. 대상 Project canonical의 실제 위치에 맞춰 recover schema와 허용 경계를 바꾼다. 이 변경은 target-specific 코드 변경이므로 absolute path, traversal, undeclared path, non-Markdown, symlink와 records 유입 거부 테스트를 함께 고친다.
6. verify는 shell 없는 고정 argv를 사용하고, 실행 전에 evidence를 hash하며, 성공과 실패를 모두 새 receipt로 남기고 machine status만 atomic하게 갱신하게 한다.
7. cache replay가 가능한 도구는 fresh 실행 option을 계약에 고정하거나, fresh가 아님을 proof ceiling에 명시한다.
8. preflight receipt를 첫 Workspace `records/`에 그대로 복사하고 migration record에서 연결한다.

사용자가 직접 삭제·이동·승격한 파일은 그 주체와 결정을 기록한다. Harness가 하지 않은 행동을 Harness의 효과나 손실로 서술하지 않는다.

## 5. Harness 자체를 별도로 검증한다

target-specific 변경이 들어간 Harness의 테스트를 제품 verify와 분리한다. target root에서 `python3 -B`로 전체 Harness test discovery를 실행하고, 다음 helper로 실행 전 Python source hash와 결과를 durable receipt로 남긴다.

```bash
python3 <skill-dir>/scripts/record_harness_tests.py \
  --project-root <target-project-root> \
  --source-root context/work/harness \
  --tests-start context/work/harness \
  --top-level . \
  --pattern 'test_*.py' \
  --records-dir context/work/workspaces/<workspace-id>/records \
  --timeout-seconds 300
```

실제 target test layout에 맞춰 `--tests-start`, `--top-level`, `--pattern`만 명시적으로 조정한다. helper는 임의 argv나 shell을 받지 않고 현재 Python으로 `unittest discover`만 실행하며, timeout이면 같은 process group을 종료하고 실패 receipt를 남긴다. 단순 사람 기록만으로 "Harness tests pass"를 선언하지 않는다.

## 6. 전체 순환을 검증한다

다음 순서를 바꾸지 않는다.

1. `recover`: Workspace current, `output/index.md`, 선택한 Project 문서만 loaded 되었는지 exact set으로 확인한다. 최소 memory 세 파일이나 output index가 없으면 실패하는지, 선택하지 않은 문서, Workspace source 전체, output artifact 본문, records, verify 계약이 빠졌는지도 확인한다.
2. `verify`: 계약의 고정 명령을 실행한다. receipt가 evidence를 실행 전에 캡처했는지, cache가 실제 우회됐는지, exit·timeout·stdout/stderr truncation과 task/test/build 범위를 확인한다.
3. `recover`: 새 machine status와 최신 receipt header가 다시 연결되는지 확인한다. receipt 본문 전체가 recovery context로 들어가면 안 된다.
4. 사람용 state가 자동으로 완료 처리되지 않았는지 확인한다. pass는 `verified_waiting_acceptance`이며 acceptance나 Workspace 완료가 아니다.

제품 verify의 evidence는 "중요해 보이는 파일" 몇 개가 아니라 고정 argv가 실제 실행하는 task graph의 입력을 닫아야 한다. root 실행 설정과 각 대상 package의 tracked source·manifest·compiler/build 설정을 포함하고, 포함하지 못한 입력은 정확히 적는다.

## 7. 독립 검토와 정합성 유지

구현자가 아닌 reviewer에게 source `output/`, target 원자료, preflight, Harness receipt, product receipt, status를 직접 보게 한다. 다음 주장을 각각 supported, unsupported, contradicted로 판정하게 한다.

- 기존 canonical과 사용자 변경을 보존했는가.
- recover가 선언된 최소 context만 싣는가.
- target-specific Harness 변경이 현재 green인가.
- 최종 evidence가 고정 검증 입력을 실제로 대표하는가.
- 자동 검증과 사람 acceptance가 분리됐는가.
- Harness를 제거해도 Project와 Workspace 의미가 남는가.

현재 repository에 Project application Workspace와 context maintainer routing이 있으면 자연스러운 종료 경계에서 그 Workspace만 정합성 점검한다. active Workspace를 임의로 바꾸거나 다른 Workspace records를 합치지 않는다.

## 완료 조건

다음을 모두 만족할 때 구조 이식을 완료로 보고한다.

- preflight receipt와 보호 대상이 남아 있다.
- Project canonical Owner와 target별 adaptation이 문서화됐다.
- 첫 Workspace가 최소 memory 세 파일, `source/index.md`, `output/index.md`, 독립된 `source/`·`output/`·`records/` 경계를 가진다. Recover에는 output index만 들어오고 source와 output artifact 본문은 들어오지 않는다.
- Harness test receipt가 source hash와 현재 pass/fail을 연결한다.
- `recover → verify → recover`가 live target에서 실행됐다.
- product receipt와 status가 같은 최종 실행을 가리킨다.
- 증명한 범위와 브라우저·외부 시스템·사람 acceptance의 미검증 범위를 분리했다.
- 독립 검토의 P1/P2가 해결됐거나 unresolved로 명시됐다.

대상 커밋, acceptance, Project canonical 반영, Workspace 완료·보관은 사용자가 별도로 승인하지 않으면 자동 수행하지 않는다. staging이 필요하면 기존 사용자 변경과 이식 파일을 exact path로 분리한다.

## 보고 형식

결과를 다음 순서로 짧게 보고한다.

1. 어디에 무엇을 이식했는가.
2. 기존 canonical과 사용자 변경을 어떻게 보존했는가.
3. Harness test와 product verify가 무엇을 실제로 통과했는가.
4. receipt와 current 재진입 위치는 어디인가.
5. 아직 사람이나 실환경이 확인해야 할 것은 무엇인가.
6. commit 여부와 working tree 경계는 무엇인가.
