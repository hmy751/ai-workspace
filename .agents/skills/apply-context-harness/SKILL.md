---
name: apply-context-harness
description: 기존 개발 Project 하나에 현재 reference-project가 소유한 Project common context, Workspace와 Harness 책임을 기존 canonical과 사용자 변경을 보존하며 이식한다. 사용자가 대상 경로와 함께 "context harness 이식/적용", "reference-project를 다른 프로젝트에 붙여줘", "Project context와 Workspace context harness를 설치해줘"라고 요청할 때 사용한다. 단순 기준 Project 수정, 구조 설명, 이미 설치된 Project의 브라우저 acceptance만 수행하는 요청에는 사용하지 않는다.
---

# Apply Context Harness

## 소유 경계

`reference-project/`는 현재 실행 계약과 책임 구조의 canonical이다. 이 skill은 target 조사, 충돌 보호, 책임 적응, 검증 선택과 결과 보고만 소유한다. Reference의 schema, status vocabulary, 내부 경로와 호환 이력을 이 문서에 다시 고정하지 않는다.

Sample Project 내용은 복제하지 않는다. 호출 시점에 commit과 clean/dirty provenance를 확인하고 사용이 승인된 Reference bytes와 target 원자료를 읽어 실제 Project common context, Workspace 내용과 Harness 연결을 구성한다.

## 시작

1. 대상 Project의 절대 경로, 허용 변경 범위와 첫 Workspace가 다룰 실제 작업 장면을 확인한다. 대상이 없으면 이 세 가지를 한 번에 묻고 멈춘다.
2. [`references/application-contract.md`](references/application-contract.md)를 끝까지 읽는다.
3. `git -C <skill-dir> rev-parse --show-toplevel`로 source root를 구하고 `reference-project/`의 존재를 확인한다. 상대 경로 단계 수로 추측하지 않는다.
4. Source commit과 `reference-project/`의 clean/dirty 상태를 확인한다. Dirty bytes를 쓰려면 path별 diff와 SHA-256을 먼저 제시해 승인을 받는다. 승인되지 않은 dirty Reference는 이식하지 않는다.
5. Live `reference-project/README.md`와 root `AGENTS.md`에서 시작해 Project·Work·Workspace·Harness canonical과 책임별 계약으로 이어지는 현재 routing을 읽는다. Target에 이식할 파일과 규칙은 이 live source에서 결정한다.

## 1. 변경 전 target을 고정한다

대상에 쓰기 전에 다음을 수행한다.

1. 대상 경로에 적용되는 `AGENTS.md`, `CLAUDE.md`와 도구별 Project 설정을 읽는다.
2. 대상 Git root, branch, HEAD, remote, tracked·staged·untracked 상태를 확인한다.
3. 다음 helper로 현재 변경과 instruction file의 관찰 receipt를 `/private/tmp`에 만든다.

```bash
python3 <skill-dir>/scripts/capture_target_state.py \
  --project-root <target-project-root> \
  --output-dir /private/tmp
```

4. Helper가 ignored 파일을 수집하지 않는다는 한계를 유지한다. Dry-run payload의 exact path와 ancestor는 실제 파일 존재 여부와 target ignore 규칙을 별도로 대조한다.
5. Target의 repo-local skill discovery 지원과 기존 `.agents/skills/create-context-workspace/`의 모든 exact path, root instruction routing을 별도로 확인한다. Helper receipt가 clean skill 파일 전체를 수집한다고 가정하지 않는다.
6. Receipt에서 사용자 변경, 삭제, untracked 파일과 instruction·skill 충돌을 보호 목록으로 만든다. Receipt는 저자나 변경 주체를 증명하지 않는다.

Dirty tree만으로 멈추지 않는다. Payload와 겹치거나 기존 canonical·설정·사용자 파일을 덮어쓸 가능성이 있을 때만 exact 충돌과 선택지를 제시한다.

## 2. Target Owner 지도를 만든다

원자료에서 다음을 확인한다.

- Project 공통 목표·구조·결정과 상세 사실의 현재 Owner
- 첫 Workspace의 목표, 지속 memory, 빠른 state, 선택 source, goal output과 records Owner
- 제품 검증의 실제 runtime, cwd, fresh-run 조건과 입력 범위
- 기존 context 경로, package, instruction, ignore와 도구 설정의 충돌
- Target의 repo-local skill discovery 경계, 기존 Workspace 생성 skill과 root routing Owner
- 자동 검증이 확인하지 못하는 외부 시스템과 사람 acceptance

Project common context는 live Reference가 요구하는 진입 책임을 target 사실로 채운다. 기존 상세 canonical은 그대로 유지하고, derived common context와 충돌하면 상세 Owner를 우선한다. Owner 자체의 이동은 별도 승인 없이는 수행하지 않는다. 기존 Owner의 경로만 연결하지 말고 여러 Workspace의 판단에 필요한 사실을 선별해 다시 서술한다. Target Owner에 제품 기준·구조·채택 결정처럼 서로 구분되는 공통 내용이 있으면 overview에 합치거나 생략하지 말고 대응하는 Project context 책임을 실제 내용으로 구성한다. 생략은 해당 책임에 독립된 공통 내용이 없음을 원자료에서 확인한 경우에만 허용한다.

## 3. Dry-run manifest를 먼저 제시한다

쓰기 전에 다음을 사용자에게 한 번에 제시한다.

- Source commit, Reference clean/dirty 상태와 읽은 canonical 진입점
- Target baseline receipt, 기존 Owner 지도와 보호 대상
- 새 파일, 수정 파일, 충돌 파일, 명시적 제외 파일
- 기존 Owner의 어떤 공통 사실을 Project context의 어느 책임·파일·문단에 어떻게 다시 서술할지, 각 선택 책임과 근거가 있는 생략 책임, 첫 Workspace에 넣을 목표·제약·state·source·output 내용
- Reference 책임별 `source Owner → target 배치 → 그대로 사용/적응/제외 → 이유` 매핑
- Repo-local Workspace 생성 skill과 root routing의 `install/adapt/exclude`, exact 충돌과 fallback
- Target instruction과 도구 설정에 추가할 routing, 수동 agent role, lifecycle hook, session별 explicit admission·activation 명령, wrapper, runtime ignore 또는 main fallback의 개별 설치·제외 판단
- Target의 Recover·Verify 계약과 제품 검증 입력을 live Reference에서 적응한 결과
- 변경 위험에 맞춘 Harness validation, product Verify와 review 계획
- 남는 proof ceiling, 사람 acceptance와 commit 경계

사용자가 manifest를 승인한 뒤 쓴다. Sample 문서·Workspace 내용·과거 receipt·sample 제품 코드와 테스트는 payload가 아니다. 기존 디렉터리에 broad recursive copy를 하지 않는다.

## 4. 책임 단위로 이식한다

1. 일반 진입점에 Project common과 Work context의 Owner routing을 additive하게 연결한다. 기존 instruction과 설정을 교체하지 않는다.
2. Project common context를 링크 목록이나 기존 문단 복사본이 아닌 target 사실로 구성한다. 상세 Owner, 충돌 우선순위와 갱신 조건을 함께 남기고, [`application-contract.md`](references/application-contract.md)의 내용 충족 검사를 통과시킨다.
3. Live Reference가 요구하는 Workspace 지속 층과 machine 계약을 첫 작업의 실제 목표·제약·source·output·검증으로 채운다. Sample 내용과 기존 Project 산출물을 복제하지 않는다.
4. Reference의 repo-local `create-context-workspace` skill과 root routing을 target 도구가 지원하면 기존 skill·instruction을 보존하며 설치하거나 좁게 적응한다. 최초 이식 중 첫 Workspace를 만들기 위해 아직 설치되지 않은 이 skill을 중첩 호출하지 않는다. 같은 이름의 기존 skill을 덮어쓰지 않으며, 지원하지 않거나 충돌을 해소할 수 없으면 제외 이유와 생성·전환 canonical을 main이 적용하는 fallback을 남긴다.
5. Harness runtime·계약·테스트는 승인된 source commit에서 가져오고, target package·경로·runtime과 충돌하는 부분만 좁게 적응한다. Reference 내부 계약을 skill 문장으로 재구현하지 않는다.
6. Live Reference의 tool-specific Maintain 연결을 target에서 쓸 수 있으면 기존 설정과 role 이름을 보존하며 수동 role, [session binding·lifecycle canonical](../../../reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md), lifecycle hook, schema v2 explicit admission config, session별 `status|activate|deactivate` wrapper와 ignored runtime을 하나의 Maintain 책임으로 설치·적응·제외한다. Project 공통 config, active index나 첫 prompt 의미를 새 session의 Workspace binding으로 사용하지 않는다. Schema v1 config와 runtime이 있으면 v2 adapter를 먼저 배치해 기존 session state를 generation 1로 읽게 하고 새 session 자동 binding은 즉시 중단한 뒤 config를 v2로 바꾼다. Existing runtime을 일괄 삭제·retarget하지 않는다. Role 발견 경로만 등록한 상태를 automatic Maintain 설치로 부르지 않는다. 설정 parse와 각 adapter path 해석은 확인하되 새 task의 실제 role·hook discovery와 lifecycle 장면을 실행하지 않았다면 증명했다고 쓰지 않는다. Project-local Codex hook은 이식 직후 기본 상태를 `activation_pending`으로 둔다. Target root의 Codex task에서 hook definition을 review/trust하고, 사용자가 Maintain을 원하는 session만 명시적으로 activate해 binding과 prompt/Stop runtime receipt를 확인한 뒤에만 `activated`라고 보고한다. Unbound 새 session은 정상 no-op이며 receipt를 만들지 않는다고 실패로 해석하지 않는다. 충돌하거나 discovery가 확인되지 않으면 덮어쓰지 않고 live Maintain 계약을 main이 수행하는 fallback과 미설치 범위를 기록한다.
7. Preflight receipt는 Workspace가 생긴 뒤 보존 위치로 exact copy하고 임시본과 SHA-256이 같은지 확인한다.

사용자가 직접 삭제·이동·승격한 파일은 그 주체와 결정을 기록한다. Harness가 하지 않은 행동을 Harness 효과로 서술하지 않는다.

## 5. 위험에 맞춰 검증한다

- 설명·링크·routing만 바뀌면 경로, local link, 설정 parse와 diff를 확인한다. 실행 의미가 바뀌지 않았다면 full suite, durable Verify와 독립 review를 자동으로 붙이지 않는다.
- Harness 코드·machine 계약·evidence 범위·path 방어·사용자 파일 보호가 바뀌면 관련 단위 테스트에서 시작해 target 전체 Harness tests와 ephemeral Harness validation으로 넓힌다.
- Target-specific Harness 변경의 지속 증거가 필요하면 다음 helper로 source snapshot과 test 결과를 별도 receipt에 남긴다. Product Verify receipt와 섞지 않는다.

```bash
python3 <skill-dir>/scripts/record_harness_tests.py \
  --project-root <target-project-root> \
  --source-root <target-harness-source-root> \
  --tests-start <target-tests-start> \
  --top-level <target-test-top-level> \
  --pattern 'test_*.py' \
  --records-dir <target-harness-test-receipts-dir> \
  --timeout-seconds 300
```

- 초기 이식 완료처럼 상태 전환·인계 증거가 필요한 경계에서만 live product Verify를 실행한다. 이후 Recover가 현재 machine result를 다시 연결하는지 확인한다. Ephemeral validation 결과, durable Harness test receipt와 Product Verify receipt를 서로 혼동하지 않는다.
- Context 의미가 바뀌면 명시한 Workspace만 Maintain하고 main이 근거와 diff를 검토한다. Verify pass를 사람용 완료나 acceptance로 바꾸지 않는다.
- Codex lifecycle hook 검증은 `installed`와 `activated`를 분리하고 live session lifecycle canonical의 runtime 저장 범위·권한 한계·actual-host proof ceiling을 함께 보존한다. `installed`는 target 파일, schema v2 설정 parse, wrapper import, unbound `status`와 bounded Recover가 통과한 상태다. `activated`는 target repo를 root로 하는 Codex task에서 project-local hook을 trust하고 사용자가 선택한 Workspace를 그 session에 명시적으로 activate한 뒤, persisted binding과 같은 generation의 prompt/Stop runtime receipt가 생긴 상태다. 현재 task가 target root가 아니거나 hook trust·explicit activation·event receipt 중 하나라도 없으면 activation을 완료로 쓰지 않는다. 다른 unbound session이 runtime이나 Workspace write를 만들지 않는지도 actual-host 격리 장면에서 확인한다.
- Workspace 생성 skill은 target 파일·frontmatter·canonical link와 root routing을 확인해 `installed` 또는 `adapted`를 판정한다. 같은 이식 session의 파일 존재만으로 실제 skill discovery나 implicit invocation을 증명하지 않고, 새 target-root session에서 확인하지 못했으면 그 한계를 남긴다.
- Project common context는 링크를 열지 않은 1차 읽기에서 Project 공통 판단에 필요한 내용을 설명할 수 있는지 검토하고, 그 뒤 상세 Owner를 열어 사실·범위·충돌 우선순위가 맞는지 대조한다.
- 신규 이식, 사용자 파일 충돌 또는 실행·안전 계약 변경은 구현자가 아닌 reviewer가 raw source, target 원자료, preflight와 실제 증거를 직접 대조한다. 낮은 위험의 설명·routing 변경은 main의 좁은 확인으로 끝낼 수 있다.

## 완료 조건

- 사용한 Reference commit과 책임별 target 매핑이 남아 있다.
- 기존 canonical과 사용자 변경이 보존되고 충돌 선택이 승인됐다.
- Project common context와 첫 Workspace가 target 사실을 담으며 실제 산출물을 복제하지 않고, Project context의 각 선택 문서가 링크 없이도 맡은 공통 책임을 설명한다.
- Target Owner에서 확인한 구분되는 공통 책임은 대응하는 Project context Owner가 맡고, 생략한 책임은 독립된 공통 내용이 없다는 근거가 남아 있다.
- 각 Reference 책임이 설치·적응됐거나 제외 이유와 fallback이 명시됐다.
- Repo-local Workspace 생성 skill과 root routing이 설치·적응됐거나, 제외 이유와 canonical을 main이 적용하는 fallback이 명시됐다.
- Project-local Maintain hook은 `installed`, `activation_pending`, `activated`, `excluded` 중 하나로 보고됐고, `activated`라고 쓰려면 target Codex task의 hook trust, session별 explicit activation과 같은 binding generation의 runtime event receipt가 확인됐다. 새 session이 기본 unbound라는 사실과 binding하지 않은 session의 무부작용을 별도로 보고한다.
- 변경 위험에 맞는 검증 결과와 proof ceiling이 남아 있다.
- Machine 결과, 사람용 Context, acceptance와 commit 권한이 분리돼 있다.
- 독립 review가 필요한 범위의 P1은 해결됐고 P2는 해결되거나 사용자가 영향을 보고 수용했다.

Target commit, acceptance, Project canonical 반영, Workspace 완료·보관은 별도 승인 없이 자동 수행하지 않는다. Staging이 필요하면 기존 사용자 변경과 이식 파일을 exact path로 분리한다.

## 보고

1. 어디에 어떤 Reference 책임을 이식·적응·제외했는가.
2. 기존 canonical과 사용자 변경을 어떻게 보존했는가.
3. 어떤 validation과 product Verify가 무엇을 실제로 확인했는가.
4. Receipt와 현재 재진입 위치는 어디인가.
5. Project-local Maintain hook의 상태가 installed, activation_pending, activated, excluded 중 무엇이며, default-unbound·session별 activation·trust와 runtime receipt가 어디까지 확인됐는가.
6. 아직 사람이나 실환경이 확인할 것은 무엇인가.
7. Commit 여부와 working tree 경계는 무엇인가.
