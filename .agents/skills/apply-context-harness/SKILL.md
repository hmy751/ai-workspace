---
name: apply-context-harness
description: 기존 개발 Project 하나에 현재 reference-project의 Project context, Workspace 재개 안내와 기록·개발 스킬을 기존 canonical과 사용자 변경을 보존하며 이식한다. 대상 경로와 함께 context harness 이식·적용이나 reference-project 설치를 요청할 때 사용한다. 단순 기준 Project 수정, 구조 설명, 이미 설치된 Project의 브라우저 acceptance만 수행하는 요청에는 사용하지 않는다.
---

# Apply Context Harness

## 소유 경계

`reference-project/`는 현재 운영 계약과 책임 구조의 canonical이다. 이 skill은 target 조사, 충돌 보호, 책임 적응, 검증 선택과 결과 보고만 소유한다. Work 지침·Workspace 재개 안내·기록 스킬의 상세 기준은 live Reference에서 읽는다.

Sample Project 내용은 복제하지 않는다. 호출 시점에 commit과 clean/dirty provenance를 확인하고 사용이 승인된 Reference bytes와 target 원자료를 읽어 실제 layered Project context, Workspace 내용과 스킬 연결을 구성한다. 이름의 harness는 이전 호출과의 연속성을 위한 것이다. 아카이브한 Recover·Verify 실행기와 전용 machine 파일은 새 설치 payload가 아니다.

## 시작

1. 대상 Project의 절대 경로, 허용 변경 범위와 첫 Workspace가 다룰 실제 작업 장면을 확인한다. 대상이 없으면 이 세 가지를 한 번에 묻고 멈춘다.
2. [`references/application-contract.md`](references/application-contract.md)를 끝까지 읽는다.
3. `git -C <skill-dir> rev-parse --show-toplevel`로 source root를 구하고 `reference-project/`의 존재를 확인한다. 상대 경로 단계 수로 추측하지 않는다.
4. Source commit과 `reference-project/`의 clean/dirty 상태를 확인한다. Dirty bytes를 쓰려면 path별 diff와 SHA-256을 먼저 제시해 승인을 받는다. 승인되지 않은 dirty Reference는 이식하지 않는다.
5. Live `reference-project/README.md`와 root `AGENTS.md`에서 시작해 Project·Work·Workspace canonical과 [Project 작성·읽기 기준](../../../reference-project/context/project/REFERENCE/README.md), [Reference skill 색인](../../../reference-project/.agents/skills/README.md)을 읽는다. Target에 이식할 파일과 규칙, skill별 canonical·공통 기준·도구별 연결은 이 live source에서 결정한다. Archive의 과거 지침은 현재 설치 요구로 읽지 않는다.

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
5. Live Reference skill 색인에서 선택한 각 skill과 공통 기준의 target exact path·ancestor, 도구별 상대 symlink와 root instruction routing을 별도로 확인한다. Target의 discovery 지원과 이름이 달라도 같은 책임을 맡는 기존 skill·guidance Owner를 대조한다. Helper receipt가 clean·ignored skill과 공통 기준 파일 전체를 수집한다고 가정하지 않는다.
6. Receipt에서 사용자 변경, 삭제, untracked 파일과 instruction·skill 충돌을 보호 목록으로 만든다. Receipt는 저자나 변경 주체를 증명하지 않는다.

Dirty tree만으로 멈추지 않는다. Payload와 겹치거나 기존 canonical·설정·사용자 파일을 덮어쓸 가능성이 있을 때만 exact 충돌과 선택지를 제시한다.

## 2. Target Owner 지도를 만든다

원자료에서 다음을 확인한다.

- Project 공통 목표·구조·결정과 상세 사실의 현재 Owner, 주제별 유지·이동 승인 범위
- 첫 Workspace의 목표, 지속 memory, 빠른 state, 선택 source, goal output과 records Owner
- 제품 검증의 실제 runtime, cwd, fresh-run 조건과 입력 범위
- 기존 context 경로, package, instruction, ignore와 도구 설정의 충돌
- Target의 repo-local skill discovery 경계, 기존 관리·논의·재판단·설명 skill, 공통 guidance와 root routing Owner
- 자동 검증이 확인하지 못하는 외부 시스템과 사람 acceptance

Project context는 live Reference의 `context/project/README.md`, `MAINTENANCE.md`, `REFERENCE/`, `common/`, `current/`, `guidance/`, `decisions/` 물리 경계를 target에 구성하고 target 사실로 채운다. Root README는 작업·주제에서 실제 본문과 layer 책임을 찾는 안정된 routing anchor로 두며, 첫 Workspace는 README와 goal에 필요한 실제 본문을 따로 선택한다. Owner 이동이 승인되지 않은 target 상세 canonical은 유지하고 layered context와 충돌하면 상세 Owner를 대조한다. 사용자가 한정해 승인한 주제는 Project 내용 문서가 현재 의미의 canonical이 되도록 전환하되, 그 범위를 다른 상세 문서 전체로 넓히지 않는다.

- `common/`: 여러 Workspace에 지속되는 제품·사용자·domain 의미와 Project-wide 제약을 실제 내용으로 구성한다.
- `current/`: 현재 구현·지원·미지원 범위, 상세 Owner와 proof boundary를 다음 판단에 유용한 교체형 맥락으로 구성한다.
- `guidance/`: 관련 작업의 구체적인 계약·이유·적용·변경 판단·검증을 둔다. 조언이나 실행 순서에 한정하지 않는다.
- `decisions/`: 중요한 선택의 이유와 재검토 신호를 보존하며 현재 layer의 답을 기본적으로 대신하지 않는다.

세 책임 layer 자체는 생략하거나 overview 하나로 합치지 않는다. 기존 Owner의 경로만 연결하지 말고 여러 Workspace의 판단에 필요한 의미를 선별해 다시 서술한다. Ticket·Workspace·evidence 묶음은 조사 근거이지 문서 책임이 아니다. 다음 작업의 질문과 온전한 의미를 먼저 구성하고 주 책임 layer를 고르며, 원자료 수나 layer 수대로 문서를 쪼개지 않는다. 특정 layer에 README 외 실제 본문이 없을 수는 있지만, 그 경우 원자료에서 독립된 내용이 없다는 근거를 dry-run manifest와 적용 기록에 남긴다. 이식 범위의 기존 문서는 [기존 문서의 전환 기준](references/application-contract.md#기존-문서의-전환)에 따라 현재 역할을 판단하고, 내용의 귀속과 기존 파일의 처리를 함께 결정한다.

Live [`Project 관리 계약`](../../../reference-project/context/project/MAINTENANCE.md)과 [`REFERENCE`](../../../reference-project/context/project/REFERENCE/README.md)를 읽고 target의 같은 책임 위치에 적응한다. Root README는 주제별 진입과 권위 관계, 관리·작성·읽기 기준을 읽을 시점을 연결한다. 이식·갱신·읽기 주체가 필요한 작업에서 직접 읽도록 연결하며 일반 재개의 기본 자료로 자동 추가하지 않는다. 기준을 README나 관리 skill에 중복 정의하지 않고, 이번 이식에서 수행한 문서 전환·보존 결과는 적용 Workspace 기록에 남긴다.

## 3. Dry-run manifest를 먼저 제시한다

쓰기 전에 다음을 사용자에게 한 번에 제시한다.

- Source commit, Reference clean/dirty 상태와 읽은 canonical 진입점
- Target baseline receipt, 기존 Owner 지도와 보호 대상
- 새 파일, 수정·이동·제거할 파일, 충돌 파일과 명시적 제외 파일. 대체되는 문서는 유효한 내용의 반영 위치와 기존 경로의 처리 이유를 함께 제시한다.
- 기존 Owner의 어떤 주제를 유지하거나 승인된 범위에서 이동할지, 다음 작업의 어떤 질문으로 내용을 구성하고 주 책임 layer·본문을 고를지, 이전 canonical의 남은 역할과 처리, README 외 본문이 없는 layer와 그 근거, Decision 배치, 첫 Workspace에 넣을 목표·제약·state·source·output 내용
- Reference 책임별 `source Owner → target 배치 → 그대로 사용/적응/제외 → 이유` 매핑
- Live Reference의 각 repo-local skill, Project `REFERENCE`, 공통 기준·guidance 색인과 도구별 연결·root routing의 `install/adapt/exclude`, exact 충돌과 fallback
- Target instruction과 도구 설정에 추가할 routing, record-work의 원문 접근·서브 재사용 방식, 기존 자동 기록 장치의 중복 실행 방지·전환 범위와 fallback의 설치·제외 판단
- Target Work의 재개 안내·기록 연결과 실제 제품 검증 방법. 기존 Recover·Verify 등이 있으면 실제 소비자·보존할 계약/증거와 승인 범위 안의 유지·전환 계획
- Project path·책임·authority 변경에 영향받는 live consumer 목록과 각 consumer의 reconcile·전환·deactivation 계획
- Local link의 lexical/resolved target 검사와 semantic target review, source sample·rename 잔재의 residue 목록과 허용 근거
- 실제 검사 명령이 읽는 입력·환경과 보존할 판본/출력, 확인하지 못하는 범위
- 변경 위험에 맞춘 직접 검사, 재개·기록 수행 확인과 review 계획
- 남는 proof ceiling, 사람 acceptance와 commit 경계

사용자가 manifest를 승인한 뒤 쓴다. 이번 범위가 이미 승인돼 있으면 같은 승인을 반복해서 묻지 않는다. Sample 문서·Workspace 내용·과거 receipt·sample 제품 코드와 테스트, 아카이브한 runtime·machine 계약은 payload가 아니다. 기존 디렉터리에 broad recursive copy를 하지 않는다.

## 4. 책임 단위로 이식한다

1. 일반 진입점에 layered Project context와 Work context의 Owner routing을 additive하게 연결한다. 기존 instruction과 설정을 교체하지 않는다.
2. Project context의 root README, `MAINTENANCE.md`, `REFERENCE/`와 `common/current/guidance` layer README를 구성한다. Target의 실제 의미는 작성 기준에 따라 온전한 주제 본문으로 다시 서술하고, 관리 기준과 이번 적용 기록은 각 책임 위치에 둔다. 승인된 주제별 Owner 이동과 대체되는 기존 문서의 전환도 같은 변경 단위에서 수행한다. 각 본문에서 맡은 질문과 읽을 조건을 찾을 수 있게 하되 공통 목차나 모든 문서의 동일 메타데이터를 강제하지 않고, [`application-contract.md`](references/application-contract.md)의 문서 전환과 내용 충족 검사를 통과시킨다.
3. Live Work 지침에 따라 첫 Workspace의 README·`recover.md`·current·source·output·records를 실제 목표와 근거로 구성한다. 재개 안내는 현재 초점과 기본/조건부 읽기 대상·이유를 연결하고, 실제 상태·선택 이유·다음 행동은 기존 current가 소유하게 한다. 기본 Workspace 선택은 collection README에 연결한다. `index.json`·`workspace.json`·`recover.json`·`verify.json`·machine status를 새로 요구하지 않는다. 모든 Project layer를 기본 자료로 선택하거나 Sample 내용과 기존 Project 산출물을 복제하지 않는다.
4. [Reference skill 색인](../../../reference-project/.agents/skills/README.md)의 각 skill과 공통 기준을 [`application-contract.md`의 적용 기준](references/application-contract.md#repo-local-skills와-공통-기준)에 따라 설치·적응·제외한다. 기존 skill·guidance·instruction과 도구별 연결을 보존하고, 상세 호출·내용·유지 계약은 target의 실제 Owner로 이어지게 한다. 첫 Workspace는 이식 책임이 직접 만들며 아직 설치되지 않은 생성 skill을 중첩 호출하지 않는다. Skill 설치와 실제 원문 접근·서브 호출·문서 반영은 별도로 확인한다.
5. 재개 안내의 초기 구성과 실제 읽기 경로를 연결하고, 이후 방향·단계·읽기 대상이 바뀔 때 record-work가 안내를 갱신하도록 live Work 계약을 적응한다. 기존 target에 Recover·Verify runtime·machine 상태가 있으면 [기존 실행 장치 전환](references/application-contract.md#기존-실행-장치-전환)에 따라 실제 소비자와 증거를 먼저 확인한다. 승인된 전환 범위만 처리하고 사용 중인 대상 계약을 Reference의 변경만으로 일괄 삭제하지 않는다. 새 설치를 위해 옛 runtime이나 전용 schema를 복원하지 않는다.
6. [record-work](../../../reference-project/.agents/skills/record-work/SKILL.md)와 대상 Work 작성 기준을 함께 연결한다. 실제 host에서 Main 대화 원문 접근·서브 생성·후속 호출·쓰기 권한을 확인하고, 지원되지 않는 부분은 Main 또는 지정 담당의 동일 기준 수행으로 구별한다. Target에 옛 자동 Maintain이 있으면 진행 중 반영·미반영 내용과 사용자 설정을 먼저 확인하고 승인한 범위에서 hook·role·wrapper·전용 runtime 코드를 전환한다. 자동 기록과 새 담당자가 같은 문서를 중복 수정하게 두지 않는다. 기존 session 원문·실행 이력·Workspace 기록은 일괄 삭제하지 않는다. Live Reference에 없는 binding·activation·guarded apply를 다시 설치하지 않는다. 새 스킬 설치만으로 원문 판단·재사용·기록 효과를 확인했다고 보고하지 않는다.
7. Preflight receipt는 Workspace가 생긴 뒤 보존 위치로 exact copy하고 임시본과 SHA-256이 같은지 확인한다.

사용자가 직접 삭제·이동·승격한 파일은 그 주체와 결정을 기록한다. 문서·스킬의 지침과 도구가 실제로 제공한 보장을 구별한다.

## 5. 위험에 맞춰 검증한다

- 설명·링크·routing만 바뀌면 경로, local link, 설정 parse와 diff를 확인한다. 실행 의미가 바뀌지 않았다면 full suite나 독립 review를 자동으로 붙이지 않는다.
- 제품 동작이나 기존 실행 장치를 바꿨다면 해당 Owner의 직접 검사로 영향받는 계약과 실제 소비자를 확인한다. 신규 이식은 Work 지침·README·재개 안내에서 일반 재개와 한정 요청이 필요한 의미·근거·첫 행동을 복원하는지 확인한다. 읽기 안내가 있다는 사실만으로 이해나 읽기량 감소를 보장하지 않는다.
- 검증 결과는 사용한 명령·cwd·판본·조건과 성공/실패·미확인 범위를 연결해 필요한 Work 기록에 보존한다. 실제 실행 도구의 시간·출력 제한을 확인하며 반환 대기 시간을 강제 종료 제한으로 취급하지 않는다. 기존 Verify의 자동 snapshot·자식 프로세스 종료·receipt/status 보장을 새 흐름에도 있다고 주장하지 않는다.
- 아래 helper는 기존 대상의 Python Harness를 유지·수정하는 경우에만 선택할 수 있는 독립 도구다. 신규 이식의 필수 단계나 범용 제품 검사기로 사용하지 않는다. `harness_test` 형식과 Python 소스 수집 범위는 그대로이며 제품 검증 증거와 구별한다.

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

- 상태 전환·인계에 필요한 근거는 실제 제품 검사·eval·수동 확인에서 얻고 다음 재개가 그 결과와 한계를 찾는지 확인한다. 이전 증거 재사용은 관련 변경·입력·조건을 대조해 판단한다. 특정 receipt 형식이나 machine status 생성을 완료 조건으로 추가하지 않는다.
- Context 의미가 바뀌면 명시한 Workspace의 기록을 record-work로 반영하고 Main이 중요한 결과·미반영 사항을 확인한다. 검사 pass를 사람용 완료나 acceptance로 바꾸지 않는다.
- Record-work는 설치와 실제 수행을 구별한다. 원문 식별·접근, 기록 담당자 생성·같은 담당자 재호출, 지정 Work의 실제 반영, 중복 실행 부재와 미반영 사항 연결을 actual host에서 확인한 범위만 보고한다. 기존 자동 기록을 제거한 경우 남은 호출·설정·코드 의존과 진행 중 상태의 처리를 확인한다. 새로운 기계적 경로·동시성 보장을 스킬 지침만으로 주장하지 않는다.
- Repo-local skill은 각각 target 파일·frontmatter·호출 설정, canonical·Project `REFERENCE`·공통 기준 링크와 도구별 상대 연결·root routing을 확인해 `installed` 또는 `adapted`를 판정한다. 공통 기준의 조건부 consumer와 기존 guidance 색인이 보존됐는지 함께 확인한다. 실제 discovery·각 skill의 호출 방식, 본문 읽기·적용, Main 결과 전달·record-work 갱신은 파일 존재나 형식 검사로 증명하지 않으며 새 target-root session에서 관찰한 범위만 보고한다.
- Project context는 root README에서 주제별 진입과 세 물리 layer를 찾을 수 있는지 먼저 확인한다. 대표 관련 작업에서 필요한 본문을 선택하고, 상세 Owner나 작성자의 기억 없이 그 본문이 맡은 의미·계약·현재 차이와 열린 판단을 설명할 수 있는지 검토한다. 이어 실제 코드·상세 Owner를 열어 사실 범위와 authority를 대조한다. Project path·책임·authority가 바뀌면 [`application-contract.md`](references/application-contract.md)의 live consumer를 고정해 명시 Workspace와 collection의 기본 선택에서 README·재개 안내가 의도한 자료로 이어지는지 확인하고, Project README와 대표 기존 진입점이 같은 semantic Owner에 도달하는지 fresh reader가 대조한다.
- 변경한 Markdown의 local link는 경로 존재·root 경계를 기계적으로 확인한 뒤 설명과 실제 Owner가 맞는지 별도로 판정한다. Source sample·Workspace id와 rename·제거 path의 residue 목록을 검사하고, archive·source·records의 의도한 provenance hit만 exact allowlist로 남긴다.
- 직접 검사의 입력·환경·판본 범위는 [`검증 근거와 재사용`](references/application-contract.md#검증-근거와-재사용)을 따른다. 일부 파일 해시나 commit 하나를 전체 실행 환경의 증명으로 확대하지 않는다.
- 신규 이식, 사용자 파일 충돌 또는 실행·안전 계약 변경은 구현자가 아닌 reviewer가 raw source, target 원자료, preflight와 실제 증거를 직접 대조한다. 낮은 위험의 설명·routing 변경은 main의 좁은 확인으로 끝낼 수 있다.
- 큰 Project 내용 복원·책임 재구성은 구현 결론과 파일명 힌트를 주지 않은 cold/blind review artifact를 적용 기록에 보존한다.

## 완료 조건

- 사용한 Reference commit과 책임별 target 매핑이 남아 있다.
- 계속 유효한 canonical과 사용자 변경이 보존되고 충돌 선택이 승인됐다. 승인되어 이동한 주제는 Project 문서가 현재 의미의 canonical을 맡고 이전 문서와 경쟁하지 않는다. 이식으로 대체된 문서는 유효한 내용의 귀속과 기존 파일 처리가 끝났으며, 원래 경로에 남긴 문서에는 현재 역할이나 호환 필요가 있다.
- Project root README, `MAINTENANCE.md`, `REFERENCE/`와 `common/current/guidance` 물리 layer가 존재하고, 첫 Workspace가 target 사실을 담으며 실제 산출물을 복제하지 않는다. 재개 안내에서 goal에 필요한 실제 Project 본문과 진입점을 조건·이유에 따라 찾을 수 있고 각 선택 문서는 링크 없이도 맡은 책임을 설명한다.
- Target Owner에서 확인한 지속 의미·현재 현실·작업 기준은 대응하는 layer가 맡는다. README 외 본문이 없는 layer에는 독립된 내용이 없다는 근거와 새 항목을 만들 조건이 남아 있다.
- Project 관리·구성·읽기 기준이 target의 대응 위치에 있으며 README와 이식·갱신·읽기 절차에서 필요한 시점에 연결됐다. 이번 적용 결과는 Workspace 기록에서 찾는다.
- Project path·책임·authority 변경에 영향받는 live consumer가 reconcile·전환·deactivation됐고 명시 Workspace·기본 선택의 재개 경로와 semantic target review가 끝났다.
- Local link·residue·내용 Owner 설명과 실제 검사 입력·조건이 변경 범위에 맞게 판정됐으며, 자동으로 닫히지 않는 의미·외부 상태는 proof ceiling에 남아 있다.
- 기존 실행 장치를 전환했다면 소비자·호출 설정·보존한 계약과 증거·미전환 범위가 명시됐다. 아카이브한 Reference runtime과 machine 파일을 새로 설치하지 않았다.
- 각 Reference 책임이 설치·적응됐거나 제외 이유와 fallback이 명시됐다.
- Live Reference의 각 repo-local skill과 필요한 공통 기준·guidance 색인·도구별 연결·root routing이 설치·적응됐거나, 제외 이유와 해당 canonical을 적용하는 fallback이 명시됐다. 호출 조건과 문서 유지 경로가 실제 target 계약에 연결되며 discovery·실행·반영의 미확인 범위가 남아 있다.
- Record-work의 설치·적응·제외, 원문 접근·담당 재사용·직접 반영의 실제 확인과 미확인이 구별됐다. 기존 자동 기록 장치를 전환했다면 중복 실행 제거와 보존한 상태·미반영 책임이 남아 있다.
- 변경 위험에 맞는 검증 결과와 proof ceiling이 남아 있다.
- 실제 검사 결과, 사람용 Context, acceptance와 commit 권한이 분리돼 있다.
- 독립 review가 필요한 범위의 P1은 해결됐고 P2는 해결되거나 사용자가 영향을 보고 수용했다.

Target commit, acceptance, 승인 범위 밖의 Project canonical 변경, Workspace 완료·보관은 자동 수행하지 않는다. Staging이 필요하면 기존 사용자 변경과 이식 파일을 exact path로 분리한다.

## 보고

1. 어디에 어떤 Reference 책임을 이식·적응·제외했는가.
2. 기존 canonical과 사용자 변경을 어떻게 보존했는가.
3. 어떤 live consumer를 reconcile·전환·deactivation했고 명시 Workspace·기본 선택에서 어떤 재개 자료를 읽었는가.
4. Local link·semantic target·residue·내용 Owner 설명과 실제 검사 입력·조건을 어디까지 확인했는가.
5. 어떤 직접 검사·eval·수동 확인이 무엇을 실제로 확인했는가.
6. 보존한 근거와 현재 재진입 위치는 어디인가. 기존 실행 장치가 있다면 무엇을 전환·보존했고 무엇이 남았는가.
7. Record-work의 실제 원문 접근·담당자 재사용·문서 반영은 어디까지 확인했고, 기존 자동 기록의 전환과 미반영 내용은 어떻게 이어졌는가.
8. 아직 사람이나 실환경이 확인할 것은 무엇인가.
9. Commit 여부와 working tree 경계는 무엇인가.
10. 각 repo-local skill과 공통 기준·도구별 연결의 설치·적응·제외 결과, 실제 발견·호출과 문서 유지 흐름을 어디까지 확인했는가.
