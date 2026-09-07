# Spec 도입의 개발 영향 분석

확인일: 2026-09-07. 코드 기준: `5e45310`의 live `reference-project/`. 이전 조사 기록·Workspace 문서만 working tree에서 변경된 상태였다. 이번에는 Reference 코드·설정·기존 계약을 변경하지 않았다.

## 분석 질문과 전제

사용자는 current가 이미 spec에 해당하는지 다시 물은 뒤, “spec 도입이면 어느 부분이 개발적으로 영향이 가는지”, “만약 recover가 goal을 건드린다면 그건 범위잖아”라고 요청했다. 따라서 개념을 권장하는 데서 멈추지 않고 goal·요구·완료 기준을 읽고, 수정하고, 검증에 연결하고, 새 작업에 구성하는 실제 경로를 추적했다.

앞선 [09 비교](2026-09-07-09-spec-ticket-current-assessment.md)의 ‘별도 spec 도입을 우선 권장’하는 의견을 확정 방향으로 사용하지 않는다. 현재 goal·제약·완료 기준은 이미 명세 역할 일부를 수행한다. 이번에는 (a) 같은 current 안에서 명세를 구체화하는 경우, (b) 별도 spec이 상세 요구의 정본을 맡는 경우, (c) goal의 파일·필수 계약을 대체하는 경우, (d) 여러 Workspace가 공유하는 경우를 구분했다. 특정 배치나 도입은 아직 합의되지 않았다. Ticket 체계 구현은 이번 분석에 포함하지 않는다.

## 확인한 전체 관계

Recover는 goal을 필수 파일로 검사하고 본문을 packet에 담는다. Maintain은 그 packet으로 최초 맥락을 구성한 뒤 대화의 명확한 변화를 goal을 포함한 허용 문서에 반영한다. Verify는 goal을 직접 읽지 않고 별도의 `verify.json`이 지정한 기준 문서와 제품 입력을 snapshot한다. 다음 Recover는 그 receipt에 기록된 파일만 현재 내용과 대조한다.

따라서 개발 영향은 **요구의 소유 문서, 읽기 선택, 변경 반영, 검증 기준, 검증 기록의 유효성, 생성·전환·이식, 이를 증명하는 테스트**에 걸친다. 영향 범위라는 사실이 모든 경우의 Python 수정이나 schema 변경을 뜻하지는 않는다.

## 1. Workspace goal·current의 계약

현재 [Workspace 구성](../../../../reference-project/context/work/workspaces/README.md)의 15행은 `current/memory/index.md`, `01-goal.md`, `02-constraints.md`, `03-project-context.md`를 최소 구성으로 정한다. [생성·전환 계약](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)의 20~23행은 goal·완료 장면·범위를 구성하고 필수 현재 의미를 current Owner에 직접 서술하도록 한다.

- 현재 파일 안에서 요구를 구체화하면 파일 계약을 유지할 수 있다. 요구·사용 시나리오·수락 기준이 충분한지에 대한 작성·검토 기준은 영향받는다.
- 별도 spec으로 상세 요구를 옮기면 Work goal에 남는 책임 범위와 완료 판단, spec에서 읽을 상세 조건을 구분해야 한다. 링크만 남겨 독립 재진입 의미를 잃거나, 두 문서에서 같은 요구를 독립 수정하는 결과를 피해야 한다.
- goal 파일을 없애거나 이름을 바꾸면 Workspace 최소 구성, 생성 계약, sample, Recover와 fixture를 함께 바꿔야 한다.

코드가 Markdown 문장을 파싱하지 않는다는 사실은 문서·agent 행동 계약의 변경이 없다는 뜻이 아니다.

## 2. Recover: 필수 파일·선택 경로·packet

[Recover operation](../../../../reference-project/context/work/harness/recover/operation.py)의 39행은 필수 memory 파일을 고정하고, 134행은 memory 바로 아래 Markdown을 전부 읽는다. [공통 파일 읽기](../../../../reference-project/context/work/harness/workspace_contract.py)의 202행은 UTF-8 원문을 반환할 뿐 목표·요구·완료 기준을 파싱하지 않는다. Recover는 읽기 전용이다.

- `01-goal.md` 본문만 명세로 강화: Python·JSON shape 변경 없이 본문을 공급할 수 있다.
- `current/memory/04-spec.md` 추가: 현재 loader로 자동 포함된다. index 링크가 선택 목록은 아니므로 해당 spec 전체가 매 재진입 입력이 된다.
- `current/memory/specs/`, Workspace `specs/`, `output/spec.md`, `docs/specs/`에 배치: 링크만으로 본문을 자동 읽지 않는다. Source도 기본 입력이 아니다.
- 공유 spec이 `context/project/common/specs/feature.md`처럼 기존 허용 layer 아래에 있으면 각 `recover.json`에서 선택할 수 있다. `context/project/specs/`나 `docs/specs/`를 현재 `project_context`에 지정하면 거부된다. 위치가 허용된다는 사실과 그 문서가 Project common에 속한다는 의미 판단은 별개다.
- 별도 spec 선택 항목을 새로 도입하면 59행의 exact keys, 95행의 경로 검증, 필요한 loader가 범위다. Packet에 새 필드를 만들면 470행의 packet, 499행의 사람용 renderer, JSON·텍스트 출력 테스트와 schema 호환 정책을 함께 검토한다. 모든 경로 조정이 packet shape 변경을 요구하지는 않는다.

`workspace.json`에 `spec_id`를 넣는 설계도 [공통 계약](../../../../reference-project/context/work/harness/workspace_contract.py) 268행의 id/schema 한정 identity와 충돌한다. 단순 spec 파일 도입에 ID가 필수인 것은 아니다.

## 3. Maintain: 최초 읽기·수정 Owner·쓰기 경계

[Maintain operation](../../../../reference-project/context/work/harness/maintain/operation.py) 67행의 bootstrap은 Recover packet을 사용한다. [Codex session](../../../../reference-project/context/work/harness/maintain/codex_session.py) 198행은 최초 grounding에서 제공된 bootstrap만 읽게 한다. Spec 본문이 packet에 없으면 링크만으로 Maintainer가 명세를 알고 있다고 볼 수 없다.

Maintain은 실제 goal writer다. Operation 222행은 `current/memory/` 바로 아래 Markdown을 허용하며, [기존 테스트](../../../../reference-project/context/work/harness/maintain/tests/test_operation.py) 104행이 `01-goal.md`의 실제 수정 성공을 확인한다.

- 기존 goal이나 memory 직접 자식 spec: 현재 write 경로를 사용할 수 있다. 새 memory 파일을 만들 때에는 operation 447행의 index 동시 갱신 조건도 적용된다.
- 별도 spec 정본: 요구 변화는 어디에 쓰고 Work 범위·진행 해석은 어디에 쓸지 [Maintain 계약](../../../../reference-project/context/work/harness/maintain/README.md)과 [수동 role](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml), 의미 평가 사례를 함께 바꿔야 한다. Python의 hash·path guard는 이 의미 배치를 판정하지 않는다.
- 자동 경로는 수동 TOML role 자체를 실행하지 않고 Codex session 258행에서 Maintain README를 prompt에 넣는다. TOML만 고치는 것으로 자동 경로의 행동 변경을 완료할 수 없다.
- 새 `specs/` 폴더를 Maintain 수정 대상으로 삼으면 write allowlist·index 관계·경로 검사·테스트가 범위다. 별도 spec을 읽기만 하고 다른 Owner가 수정한다면 쓰기 범위를 넓힐 필요는 없다.
- 여러 Work 공유 Project spec은 현재 Workspace Maintain의 쓰기 범위 밖이다. 이를 자동 수정하게 하면 한 Workspace만 관리한다는 책임 자체가 달라진다.

현재 decision은 path·content·기존 hash 형태여서 Markdown spec 도입만으로 schema 변경이 필수는 아니다. `grounding.schema.json`은 입력 packet이 아니라 agent가 반환하는 결과 schema다. Spec ID·revision·승인 상태·의존 입력을 기계적으로 추가할 때 해당 schema 변경을 검토한다.

## 4. 살아 있는 Maintain session과 spec 변경

[Host adapter](../../../../reference-project/context/work/harness/maintain/host_adapter.py) 544행은 같은 Workspace 재activation을 `already_active`로 반환한다. 1551행의 후속 의미 입력은 Workspace·turn id와 사용자 발화·Main 응답이다. 외부에서 바뀐 shared spec을 매 turn 자동 수집하지 않는다.

또한 [guarded apply](../../../../reference-project/context/work/harness/maintain/operation.py) 398·548행의 hash는 수정할 파일의 기존 내용만 확인한다. 다른 spec의 최신 내용을 근거로 goal 요약을 쓴다는 관계까지 보호하지 않는다.

따라서 ‘공유 명세가 바뀌면 연결된 모든 current도 최신 명세를 반영한다’를 도입 요건으로 잡으면 변경 전달·선택적 재읽기·재grounding·입력 revision 검사 중 무엇을 책임질지 추가 설계해야 한다. Spec을 담는 문서 하나를 만드는 것만으로 이 보장은 생기지 않는다. 현재 시스템의 결함으로 단정하거나 새 자동 동기화를 도입한 것으로 기록하지 않는다.

## 5. Verify와 receipt freshness

[Verify operation](../../../../reference-project/context/work/harness/verify/operation.py) 121행은 `verify.json`의 claim·canonical_basis·verification을 읽는다. 213행은 Project-root 아래 안전한 regular file 경로를 허용하고, 624행은 기준 문서와 evidence를 실행 전에 snapshot한다. Goal이나 Recover 입력을 자동으로 검증 기준으로 승격하지 않는다.

- 별도 spec이 실제 요구의 정본을 맡으면 각 `verify.json`의 `canonical_basis`, 검증할 claim, 고정 argv와 evidence 입력을 새 정본과 대조해야 한다.
- spec을 basis에 지정해 hash를 남기는 것 자체는 현재 schema 2로 가능하다. Verify의 basis 경로는 Recover의 Project layer 제한보다 넓다. `docs/specs/feature.md`도 기존 Verify로 처리할 수 있다.
- 문서를 snapshot한 사실은 그 문서의 모든 요구를 테스트했다는 뜻이 아니다. 요구별 test·eval·사람 확인의 관계는 실제 제품 검증과 이를 정한 Owner가 설명해야 한다. 현재 Verify에는 요구 ID별 coverage·충족 상태 집계가 없다. 이를 자동화하기로 할 때 새 계약·receipt·표현·검증이 개발 범위가 된다.
- [Recover freshness](../../../../reference-project/context/work/harness/recover/operation.py) 264행은 receipt의 선언된 basis/evidence 파일만 대조한다. 기본 sample처럼 goal을 basis에 넣지 않았다면 goal 요구가 달라져도 `fresh`가 유지될 수 있다. 현재 `verify.json`의 claim·argv 변화도 자동 비교하지 않는다.
- 상태 JSON의 `verification_passed`는 최근 명령 실행 결과이며 spec 전체 성립·사람 수락·Workspace 완료가 아니다. Spec 도입만으로 이를 다른 의미로 바꾸지 않는다.

## 6. Spec 소유 위치·공유·새 Workspace 생성

[Project 제품 기준](../../../../reference-project/context/project/common/prd.md)은 이미 여러 Work에 지속되는 요구·완료 기준을 소유한다. [Project 계약](../../../../reference-project/context/project/README.md) 74행부터의 실제 Owner 우선순위를 대조해 기존 PRD·spec과 중복 권위를 만들지 않아야 한다. Workspace 전용 변경 제안을 바로 Project 전체의 합의된 요구로 올리지 않는다.

작성하고 계속 수정하는 spec은 읽기 전용 원자료인 `source/`와 다르다. 명세 자체가 해당 Work의 목표 산출물이면 `output/`에 둘 수 있지만, 기본 packet이 본문을 읽지 않고 현재 Maintain도 output 본문을 수정하지 않는다는 소비·관리 경계를 같이 고려해야 한다.

[생성·전환 계약](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)과 [생성 skill](../../../../reference-project/.agents/skills/create-context-workspace/SKILL.md)은 새 Work의 goal·제약·선택 context·첫 판단을 구성한다. 별도 spec 도입 시 적용할 명세와 이번 Work 범위, shared current 정본과 과거 snapshot 중 무엇을 사용하는지, predecessor current를 계속 읽지 않고 재진입할 수 있는지가 범위다. 현재 생성은 별도 deterministic generator가 아니라 canonical과 skill을 따르는 작업이다.

Project spec의 위치·권위가 크게 바뀌면 [live consumer 계약](../../../../reference-project/context/work/workspaces/README.md) 31행에 따라 active/default와 실제 연결된 Workspace의 선택·current·output도 대조한다. [Project 갱신 skill](../../../../reference-project/.agents/skills/update-project-context/SKILL.md)은 이 Project 책임의 실행 경로이며 Workspace Maintain과 별개다. 모든 내용 편집마다 전 Workspace를 자동 동기화하는 규칙은 현재 없다.

## 7. 이식·fixture·테스트·host 배선

[이식 skill](../../../../.agents/skills/apply-context-harness/SKILL.md) 46행의 Owner 지도와 71행의 target 배치, [application contract](../../../../.agents/skills/apply-context-harness/references/application-contract.md)를 통해 기존 target PRD·spec 보존, 첫 Workspace의 명세 선택, 새 입력·검증 기준, migration 이후 재진입을 반영해야 한다. 기존 helper는 goal/spec을 하드코딩하지 않으므로 이름 도입만으로 helper Python 변경이 필수는 아니다.

[공통 fixture](../../../../reference-project/context/work/harness/testing.py) 202행은 goal 파일을 고정 생성한다. 입력 배치가 바뀌면 Recover 포함·제외, goal 필수·구버전 호환, Maintain 수정 위치·index 연결, Spec 기준 hash·실제 test 범위, 새 Workspace의 명세 선택을 검증해야 한다. Spec·goal·state에 올바른 의미를 배치하는지는 경로 unit test와 별도 의미 검토가 필요하다.

Reference의 `.codex/config.toml`, hook JSON과 wrapper는 role 발견·host routing을 맡으며 goal 본문을 해석하지 않는다. 단순 문서 추가만으로 hook 수정이 필요한 것은 아니다. 새로운 lifecycle 보장을 선택할 때 host adapter 변경과 실제 host acceptance가 범위가 된다. 이 저장소 root의 [.codex/hooks.json](../../../../.codex/hooks.json)은 빈 hook이며 root Maintain는 비활성이다. Reference 개선을 root 자동 운영의 변경으로 간주하지 않는다.

## 도입 형태에 따른 변경 규모

위 접점을 기준으로 직접 수정과 계약·입력 검토를 구분하면 다음과 같다.

| 도입 형태 | 기존 코드로 가능한 부분 | 실제로 추가되는 개발 범위 |
|---|---|---|
| 현재 goal·constraints를 명세 수준으로 구체화 | Recover 읽기, Maintain 기존 경로 쓰기 | 작성·Owner·의미 검토 기준, 필요 시 Verify basis·claim·제품 test 정합성 |
| Goal 유지, memory 직접 자식 spec 추가 | 자동 Recover·기존 Maintain guard | goal/spec 중복 제거 계약, 최초 생성과 index, 입력 크기, 검증 연결 |
| Goal 유지, 기존 허용 Project layer의 공유 spec 선택 | recover.json 선택, verify.json basis | Project 권위·갱신 Owner, 각 Work 범위·선택, 필요 시 살아 있는 session의 변경 전달 |
| 별도 specs 경계를 기본 읽기·수정 대상으로 도입 | Verify 파일 snapshot은 재사용 가능 | Recover 선택·loader·필요 시 packet, Maintain 입력·선택한 쓰기 권한, 생성·이식·test |
| Goal 파일 자체 대체 | 일부 일반 파일 읽기·쓰기 재사용 | 최소 Workspace·Recover 필수 목록·migration·sample·fixture·생성 계약 |
| 요구별 충족 집계·task 생성·spec 변경 자동 전파까지 요구 | 기존 Harness는 이 전체 workflow를 제공하지 않음 | 별도 기능·책임·schema·평가 설계. 단순 spec 도입과 구분해 범위를 결정 |

## 실제 확인한 동작

기존 `WorkspaceFixture`가 만든 임시 Project에서 검증·재진입을 실행했다. 임시 receipt/status는 cleanup됐고 실제 sample의 receipt/status는 수정하지 않았다. 제품 값은 fixture test가 통과하는 `expected`로 맞췄다.

| 조작 | 관찰 결과 | 의미 |
|---|---|---|
| 기본 Verify 뒤 Recover | `fresh` | 초기 비교 기준 |
| basis 미등록 goal 본문만 변경 | `fresh` | goal 변화는 자동으로 검증 결과를 무효화하지 않음 |
| goal에서 `docs/specs/feature.md`로 링크 | spec 본문 packet 미포함 | 링크가 자동 읽기 선택은 아님 |
| 해당 spec을 `canonical_basis`로 지정해 Verify | exit 0, `fresh` | 기존 Verify는 별도 spec 경로 snapshot을 지원 |
| 등록한 spec 본문 변경 | `stale` | 선언된 spec 변경은 기존 freshness로 탐지 |
| 다시 Verify 후 `verify.json`의 claim만 변경 | `fresh` | freshness는 현재 claim 계약 비교가 아님 |

위 조작은 `context.work.harness.testing.WorkspaceFixture`의 `setUp`/`tearDown` 사이에서 `verify_workspace`와 `build_recovery_packet`을 호출했다. 임시 spec은 어떤 실제 제품 요구도 대표하지 않는다. 이 결과는 현재 코드의 입력·hash 범위에 대한 근거이며 새 Spec 설계의 효과나 실제 host 행동 검증이 아니다.

추가로 기존의 다음 5개 회귀 검사를 실행해 모두 통과했다. 실행 위치는 `reference-project/`, 명령은 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest <아래 각 fully-qualified test> -v`다.

- `context.work.harness.recover.tests.test_recover.RecoverTests.test_requires_minimum_memory_files`
- `context.work.harness.recover.tests.test_recover.RecoverTests.test_does_not_require_or_inspect_workspace_output_artifacts`
- `context.work.harness.recover.tests.test_recover.RecoverTests.test_accepts_nested_markdown_from_each_project_layer`
- `context.work.harness.maintain.tests.test_operation.MaintainOperationTests.test_allowed_existing_update_requires_and_matches_preimage`
- `context.work.harness.verify.tests.test_verify.VerifyTests.test_canonical_basis_is_not_limited_to_recover_project_layers`

## 다음 설계 판단

구현 범위를 확정하려면 spec이 기존 current 안의 내용에 붙이는 이름인지 별도 정본인지, 별도 정본이라면 누가 갱신하고 각 Workspace가 무엇을 읽는지, spec 변경 시 기존 작업 판단·검증 결과에 어떤 보장을 제공할지 결정해야 한다. 채택 형태에 따라 위 실제 접점에서 수정 범위를 정할 수 있다. 이번에는 영향 분석을 완료했으며 도입 형태를 선택하거나 구현하지 않았다.
