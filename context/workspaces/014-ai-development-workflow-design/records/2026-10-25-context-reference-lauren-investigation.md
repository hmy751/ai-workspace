# 04-03 — Lauren/pstack의 맥락 연결과 책임 구성 조사

2026-10-25. [조사 범위](2026-10-25-context-reference-investigation-scope.md)의 Lauren 부분을 조사했다. 하나의 context 스킬을 채택하는 근거로 미리 결론내리지 않았다. 이 기록은 원문 계약의 분석이며 스킬 설치·실행, source 수정, 최신 웹판 비교, 우리 실행 스킬 변경을 하지 않았다.

## 판단에 필요한 결론

**확인한 pstack은 전체 흐름, 질문별 조사, 실행 흔적과 재개, 프로젝트별 검증 지식, 경험 개선을 서로 다른 수행 단위로 나눈다.** 하나의 공통 context 관리자나 Personal·Project·Work와 동일한 소유 체계를 확인한 것은 아니다. 스킬이 직접 요청되기도 하고 상위 흐름 안에서 불리기도 하며, parent·담당 agent가 실제로 읽고 판단하고 쓴다. 스킬 파일 자체가 실행 주체인 것은 아니다.

차용할 만한 핵심은 파일 수가 아니라 **호출자가 왜·언제 요청하는지와 호출된 절차의 입력·수정 범위·반환 조건을 함께 정하는 방식**이다. 특히 `show-me-your-work`의 양식을 한곳에 맡기는 규정, 검증 스킬의 자기 디렉터리 한정 갱신, `reflect`의 후보 판단과 승인된 편집 분리는 실제 본문에서 확인된다. 반면 많은 필수 호출·다중 검토·새 agent 기본값과 외부 기록 권한은 우리 작업에 그대로 맞지 않는다.

여기서 ‘확인’은 보존 본문에 규정이 있다는 뜻이다. 실제 운영에서 그 규정을 지켰거나 품질·비용이 개선됐다는 뜻은 아니다. 아래 helper 코드는 정적으로 읽었으며 실행하지 않았다.

## 판본과 증거 범위

- 기준은 [보존 안내](../source/workflow-references/pstack/README.md) 63–75행의 commit `190d28736eff128ec94f502a22c7fe0c4b56cd37`, pstack **0.15.29**, 수집일 **2026-10-21 KST**다. 선택 사본의 원래 경로를 그대로 읽었다.
- 처음 선정에서 빠졌던 `recall`·`automate-me`는 Main이 공식 저장소의 같은 commit에서 확보한 [추가 사본](../source/workflow-reference-supplements/2026-10-25-pstack-context/README.md)을 직접 읽었다. 기존 보존본·manifest는 바꾸지 않았으며 최신판과 섞지 않았다.
- [기존 Lauren 조사25](2026-10-13-25-lauren-source-investigation.md)는 `997ffc7… / 0.15.21`과 강연 자료를 다뤘다. 확인할 질문을 찾는 데 재사용했으며 그때의 문장을 이번 판본의 직접 근거로 대체하지 않았다.
- 아래 경로의 `repository/`는 [pstack 원문 사본](../source/workflow-references/pstack/repository/)이다. 가이드, 실제 SKILL·agent·playbook, helper 코드, 실행 효과를 구별한다. Notes Feature Map은 설명용 예제다.

## 실제 책임·읽기·쓰기 관계

| 단위와 실제 수행자 | 읽고 판단하는 것 | 쓰기·반환·권한 경계와 직접 근거 |
| --- | --- | --- |
| `poteto-mode`를 받은 parent | 요청에 맞는 playbook, 호출할 전문 절차, 담당 배치와 종합을 결정한다. | [poteto-mode](../source/workflow-references/pstack/repository/skills/poteto-mode/SKILL.md) 93–101행: “The chat that receives `/poteto-mode` runs the playbook.” Routed `how`·`why`·`reflect` 등은 자기 agent 유형을 정한다. Parent는 diff를 읽고 자기 요약을 쓴다. 123행은 playbook 단계의 todo 복사와 생략 이유를 요구한다. |
| `poteto-agent` 담당자 | Parent의 한정된 과제와 poteto-mode 전체를 읽고, 적용할 원칙 leaf를 선택해 읽는다. | [agent](../source/workflow-references/pstack/repository/agents/poteto-agent.md) 3–9행: “You are one of its delegates.” 전체 흐름·todo·추가 Task는 parent 책임이다. [mode](../source/workflow-references/pstack/repository/skills/poteto-mode/SKILL.md) 11·40·95행의 절대 경로 전달·leaf 직접 읽기·file pointer 전달과 연결된다. 자료 접근 경로를 넘기는 것이 전체 Work 인수를 뜻하지 않는다. |
| `how`의 explorer·explainer | 현재 코드의 구성·실행·경계를 조사한다. 복잡하면 각도별 explorer 후 explainer, 단순해도 explainer 하나가 조사·설명한다. | [how](../source/workflow-references/pstack/repository/skills/how/SKILL.md) 11–36행은 read-only 조사와 설명 반환이다. [explorer prompt](../source/workflow-references/pstack/repository/skills/how/references/explorer-prompt.md) 7·25–35행은 맡은 각도·읽은 파일·공백을 반환한다. [explainer prompt](../source/workflow-references/pstack/repository/skills/how/references/explainer-prompt.md) 19–23행: “resolve contradictions by checking the code yourself.” 공유 current 갱신이나 문서 생성 단계는 없다. |
| `why`의 investigator·synthesizer | 코드가 하는 일과 만든 이유를 분리한다. Parent가 code anchor를 고정하고, 사용 가능한 출처 종류별 investigator가 원문·검색·반대 증거·공백을 모은다. | [why](../source/workflow-references/pstack/repository/skills/why/SKILL.md) 13·27–51·79–98행. MCP 접근 때문에 `readonly: false`이나 쓰기 권한 의도가 아니다. [synthesizer prompt](../source/workflow-references/pstack/repository/skills/why/references/synthesizer-prompt.md) 40–45행: “Do not write files, commit, or modify external state.” 출력은 근거·추론·미확인이며 변경 준비라면 Preserve/Change/Avoid/Risk 제약으로 연결된다. |
| `show-me-your-work`를 사용하는 실행자와 별도 trail 검토자 | 오래 걸리거나 사용자가 나중에 검토할 실행에서 선택·전환·검증 결과를 기록하고 대화 원문과 대조한다. | [skill](../source/workflow-references/pstack/repository/skills/show-me-your-work/SKILL.md) 40–67행: 기본은 미커밋 `decisions.tsv` 또는 `.audit/<task>.tsv`; append-only이며 잘못된 행도 덮지 않고 supersede한다. 82행: “let it own the format. Don't restate the columns.” 실행 흔적의 정본이지 제품 약속의 정본이라는 뜻은 아니다. |
| pause/pickup을 수행하는 parent | 중단 시 재개 단서를 남기고, 다음 실행에서 이전 trail·branch·diff·완료/남은 일을 대조한다. | [pause](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/pause-safely.md) 5–10행은 atom 마감·delegate 취소·WIP commit·resume note를 규정한다. compaction note는 `/tmp/<slug>-resume.md`. [pickup](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/session-pickup.md) 5–9행은 trail을 읽되 inherited claim을 원래 목표·실물과 검증하고, 재개 지점을 정한 뒤 맞는 playbook에 넘기고 종료한다. |
| `recall`의 parent·범위별 mining 담당자 | 주제·기간·Workspace를 먼저 고정하고 자신의 최근 대화와 같은 대상의 공유 기록을 복원한다. | [recall 추가 원문](../source/workflow-reference-supplements/2026-10-25-pstack-context/recall/SKILL.md) 17–22행: 특정 채팅 재개는 pickup, 습관의 skill화는 automate-me로 보낸다. “use it and skip the mining”처럼 이미 충분한 state capsule이면 탐색을 생략한다. 주제가 특정 feature/file/bug면 why의 출처별 investigator를 재사용하고 live Git·PR 상태를 대조한다. 출력은 28–35행의 capsule·thread 상태·반복 문제·다음 행동인 brief이며 지속 문서 작성 단계는 없다. |
| 검증 스킬 생성 담당자 | 실제 repo의 사용자 표면·실행·제어·관측·격리를 조사한다. | [create-verification-skill](../source/workflow-references/pstack/repository/skills/create-verification-skill/SKILL.md) 13–40행. `.cursor/skills/verify-<app>/`에 실행·doctor·drive·evidence·cleanup·helper와 features를 만든다. 한 mapped feature를 끝까지 실행하고 증거 보존을 확인해야 산출물이다. “A generated skill that was never executed is a draft.” 44행은 유지 절차를 안내하되 cadence는 사용자가 물을 때만 제안한다. |
| 검증 스킬 유지 coordinator와 feature reader | 모든 feature를 source에서 읽고, coordinator가 실제 앱에서 확인한다. Reader는 수정도 구동도 하지 않는다. | [maintain-verification-skill](../source/workflow-references/pstack/repository/skills/maintain-verification-skill/SKILL.md) 21·25–39행: “Only edit the verification skill's own directory.” 문서 drift·harness gap만 고치며 제품 regression은 보고한다. source가 깨끗해도 모든 feature live 확인을 요구한다. clean/blocked는 PR 없이, changed는 입증한 수정 한 PR. 실행 메모는 scratch에 두고 커밋하지 않는다. |
| `reflect`의 세 reviewer·별도 synthesizer·parent·사용자 | 현재 대화에서 지속할 학습을 찾고, 기존 스킬의 실제 결함·missed trigger·새 스킬 후보·구조적 수단을 구별한다. | [reflect](../source/workflow-references/pstack/repository/skills/reflect/SKILL.md) 11–58행. Reviewer와 synthesizer는 파일을 고치지 않는다. 47행: “wait for explicit approval before applying any Accepted edit.” 사용자가 subset·routing을 선택하면 parent가 사소한 편집, built-in create-skill이 실질 편집·trigger 최적화·신규 생성을 맡는다. Backlog는 승인 없이 외부 tracker에 올리라는 별도 권한 규정이 있다. |
| `automate-me`의 parent·mining 담당자·사용자 | 반복된 개인 작업 관례를 여러 대화에서 찾고 사용자에게 실제 의도를 확인한다. 기존 mode 갱신이면 마지막 수정 이후만 조사한다. | [automate-me 추가 원문](../source/workflow-reference-supplements/2026-10-25-pstack-context/automate-me/SKILL.md) 11·17–25·40–79행. Mine/create-skill/unslop을 순서대로 조율하고 개인 `-mode` 하나를 생성·갱신한다. 63행: “Don't copy its content.” Poteto 내용은 따라 쓰지 않으며 89행은 다른 skill과 별도 principle 문서를 경로로 참조한다. 사용자 초안 검토 뒤 worktree·commit·PR 경로가 79–83행에 있고, 일반 Project/Work current를 쓰는 절차는 아니다. |
| `correct`를 수행하는 실행자 | 최근 commit·revert·review·agent rule·workaround에서 두 번 이상 반복된 오류 유형을 찾는다. | [correct](../source/workflow-references/pstack/repository/skills/correct/SKILL.md) 15–30행은 architecture, types/lint, behavior test, 판단용 문서 순서로 repo를 실제 고친다. 과거 오류에서 새 검사가 실패함을 확인하고 rule–enforcement 표를 유지한다. “Drop a rule once its mistake can't happen.” `reflect`의 승인된 문장 편집과 같은 행위가 아니다. |
| 스킬 작성·평가를 맡은 parent | 스킬의 반복 가치와 호출 조건, 참조 경로, 실제 행동 변화 여부를 판단한다. | [authoring](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/authoring-a-skill.md) 5–10행: built-in create-skill, frontmatter·참조 검증, structural test, “Delegate to other skills by path. Don't restate.” [eval](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/eval.md) 17–25행은 격리된 동일 과제·가린 후보·별도 judge·실제 읽기 원문·parent 직접 대조로 승격 권고를 만든다. 일반적인 장기 효과 감시는 아니다. |

`how`와 `why`가 개발 중 호출된다고 해서 자기 수정 범위가 생기지는 않는다. [Investigation](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/investigation.md) 5–12행도 설명·권고를 산출물로 정하고 코드 변경이 이어지면 사용자에게 돌려준 뒤 Feature/Bug fix로 재배치한다. 반대로 `correct`는 실행을 요구하는 스킬이다. 이름이 ‘맥락 관련’이라는 이유로 서로 같은 읽기/갱신 권한을 부여할 수 없다.

## 두 대표 경로

### 1. 기존 기능을 바꾸다가 중단하고 이어 하는 경우

새 기능 변경 요청을 받은 parent는 [Feature](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/feature.md) 3–13행에 따라 설계·계획·검토·검증을 맡고, `how`로 영향받는 subsystem을 이해한다. 해당 코드와 기록에서 기존 이유가 쟁점이면 `why`의 근거·열린 판단이 변경 제약을 보충한다. 기능 playbook은 `architect` 뒤 파일 범위·data shape·성공 기준을 갖춰 구현을 위임한다. `poteto-agent`는 공통 mode와 적용 원칙을 직접 읽는다. Parent의 설명만 받은 채 원문 판단을 대신하는 구조는 아니다.

오래 걸리거나 사용자가 자리를 비운 작업이라는 조건이 있으면 mode 36행이 `show-me-your-work`를 호출한다. 다음 세션은 pickup 5–9행에 따라 해당 transcript·결정 기록·실제 branch 상태를 읽고, 이미 한 작업을 무조건 재수행하지 않으면서 현재 유효한 완료 주장인지 확인한다. 재개 지점을 정하면 pickup이 끝나고 남은 구현·버그 수정 등의 playbook이 다시 맡는다.

별도로 “지난주 이 기능 작업을 되짚어 달라”는 요청이면 `recall` 17–21행이 여러 최근 대화의 주제 맥락을 복원한다. 특정 한 채팅 인수가 아니므로 pickup과 구별하며, 충분한 현재 상태가 이미 제공됐다면 대화 mining을 생략한다. 이 경로가 모든 Feature 수행에 자동 삽입된다는 근거는 없다. 사용자 이력만으로 제품의 현재 상태를 확정하지 않도록 공유 기록과 live 상태를 추가하는 점은 우리 재개에서도 참고할 수 있다.

**우리에게 주는 판단:** 공통 읽기 절차의 끝을 ‘필요한 이해를 확보하고 본래 작업으로 돌아간다’로 놓는 것은 기존 [read-project-context](../source/ai-workspace-baseline/reference-project/.agents/skills/read-project-context/SKILL.md) 18–26행과도 맞는다. 그러나 pstack의 transcript·임시 resume note·기본 미커밋 TSV는 우리 Work의 목표·제약·상태·선택·지속 근거를 모두 대체하지 않는다. 현재 [Work 지침](prototypes/development-workflow/noline-demo/context/work/AGENTS.md) 3–11행은 Main의 일반 재개, 한정 담당의 읽기, Main의 의미 반영을 별도로 규정한다. **새 Work 생성에서 무엇을 계승할지는 이 pickup 계약이 답하지 않는다.** 원래 [Recover](../source/ai-workspace-baseline/reference-project/context/work/harness/recover/README.md) 3–18행도 기존 Workspace packet 재구성과 새 Workspace 계승 의미 선별을 구별한다.

### 2. 앱 변경 뒤 검증 문서가 어긋났고, 같은 오류가 반복되는 경우

검증 수단이 없는 Project에는 생성자가 repo에서 실제 실행 조건을 읽어 verify skill과 Feature Map을 만든다. 이후 maintainer는 그 skill 디렉터리를 대상으로 feature별 source reader를 붙이고 coordinator가 모든 feature를 직접 구동한다. map의 사용자 경로 설명이 틀렸다면 문서를, 정상 동작을 harness가 제어하지 못하면 harness를 고친다. 실제 제품이 약속된 동작을 잃었다면 제품 문제로 보고하고 이 유지 PR에서 제품 코드를 고치지 않는다. 이는 같은 ‘변화’여도 **증거의 종류·기존 약속·쓰기 Owner**에 따라 다른 결과를 고르는 실제 계약이다.

그 실행에서 반복된 작업 방식의 결함이 드러났다는 이유만으로 maintainer가 전역 스킬까지 고치지는 않는다. 별도로 호출한 `reflect`는 active transcript와 실제 사용된 스킬을 읽고 후보를 선별한다. [synthesizer](../source/workflow-references/pstack/repository/skills/reflect/references/synthesizer.md) 15–22행은 지속성·판단 변화·기존 home·실제 사용·이미 있는 지침을 대조한다. 이미 명료한 규칙을 실행자가 놓친 것이라면 중복 문장을 추가하지 않는다. 구조적 수단이면 Backlog, 승인된 문장 개선이면 해당 skill의 parent/create-skill 경로다. `correct`는 별도 요청에서 반복 오류를 repo 구조·검사로 막는다. **`reflect`가 자동으로 `correct`를 실행한다고 쓰여 있지는 않다.** [가이드](../source/workflow-references/pstack/repository/docs/guide/09-make-it-yours.md) 50행도 두 책임을 나눠 설명한다.

**우리에게 주는 판단:** 프로젝트 사실 갱신은 새 제품 약속 선택과 다르며, 개선 아이디어의 채택과 승인 범위 안의 편집도 구별할 수 있다. 현재 [Project 관리](prototypes/development-workflow/noline-demo/context/project/MAINTENANCE.md) 3–13행, [Personal 관리](prototypes/development-workflow/noline-demo/context/personal/README.md) 15–21행과 같은 구별이 필요하다. 다만 pstack의 검증 map은 사용자 경로를 실행할 지식이고 우리 Project 제품 계약 전체가 아니다. `reflect`의 skill-first 저장 위치를 Personal·Project·Work의 모든 학습에 적용하면 내용 Owner를 잃는다. 새 workflow의 05에서는 후보 선택·채택·반영 뒤 실제 효과 관찰까지 추가로 정해야 한다.

## 생성·유지·개선에서 확인한 경계

Feature Map은 [예제 README](../source/workflow-references/pstack/repository/skills/create-verification-skill/references/feature-map-example/README.md) 3·33–42행에서 verification의 maintained source로 선언된다. 읽을 때는 색인 다음 해당 feature를 보며, 내용은 사용자 진입·전제·명령·관측 proof다. [create-note 예제](../source/workflow-references/pstack/repository/skills/create-verification-skill/references/feature-map-example/create-note.md) 26–38행은 저장 알림만으로 통과시키지 않고 목록에서 다시 열어 영속성을 확인한다. 이것은 실물 판단에 필요한 맥락을 실행 수단 가까이에 둔 예제이며, Notes 제품·`control-notes` 구현·실제 유지 성과를 제공한 자료는 아니다.

반복 경험을 남기는 판단은 `reflect`의 synth 단계에 있다. 대상 스킬을 먼저 읽고, 이미 잘 있는 규칙이면 실행 문제로 기각하며, 재발 패턴에 적절한 기존 home이 없을 때만 새 skill을 제안한다. [judgment reviewer](../source/workflow-references/pstack/repository/skills/reflect/references/judgment-reviewer.md) 20–33행은 실제 사용된 skill/tool 또는 missed trigger에 한정한다. [tooling reviewer](../source/workflow-references/pstack/repository/skills/reflect/references/tooling-reviewer.md) 9–17행은 agent가 직접 얻을 수 있었던 자료를 사용자가 대신 전달한 순간을 그 workflow 소유 스킬의 개선 후보로 보낸다. 단순히 모든 발견을 중앙 memory에 축적하는 절차가 아니다.

개인 관례의 선택에는 별도 경로가 있다. `automate-me` 31–40행은 여러 대화 묶음에서 반복 근거를 대조하고, 42–48행은 아직 대화에 나타나지 않은 의도를 사용자에게 확인한다. 87–96행은 한 대화에 과적합하지 않고 비기본적인 개인 규칙만 남기며, 주관적인 mode를 일반 benchmark로 판정하지 않고 사용자에게 맞는지 검토받는다고 명시한다. 이것은 현재 [Personal](prototypes/development-workflow/noline-demo/context/personal/README.md)과 접점이 있지만 저장 대상이 개인 작업 방식의 실행 지침이라는 차이가 있다. 개인 판단 본문·제품 약속·특정 Work의 선택을 모두 mode에 흡수하는 근거는 아니다.

효과 확인은 범위가 다르다. 생성은 mapped feature 하나의 end-to-end 실행, 유지는 모든 feature의 source/live coverage, `correct`는 실제 과거 오류에 대한 새 장치의 실패 증명, `eval`은 동일 과제에서 후보 차이의 관측이다. `reflect` 자체는 승인된 편집·환경에 validator가 있으면 그 검사·결과 요약까지 규정하며, `automate-me`는 주관적 의도 부합 확인을 별도로 둔다. 모든 채택이 이후 다른 과제에서도 개선됐는지 추적하는 공통 장치는 이 범위에서 확인되지 않았다.

## 교체·제거를 실제 변경으로 대조한다

| 변경 사례 | 원문이 지지하는 조정 범위 | 남는 결합과 우리 적용 조건 |
| --- | --- | --- |
| 결정 기록 형식을 바꾼다 | `show-me-your-work`가 형식을 소유하고 다른 스킬은 위임한다. 따라서 그 본문·template·helper가 첫 변경 대상이다. | 그 trail을 읽는 pickup, transcript audit, cross-model 검토와 기존 기록의 읽기까지 확인해야 한다. [helper](../source/workflow-references/pstack/repository/skills/show-me-your-work/scripts/log.sh) 19–42행은 append·열 정리·수식 접두 방지 코드가 있으나 근거의 진실성, run 구별, 동시 쓰기를 보장하는 코드는 아니다. 문장과 기계 보장을 구별해야 한다. |
| 앱 실행 방식이나 selector가 바뀐다 | 생성된 project-local verify skill의 Launch/Drive/helpers/features와 유지 절차가 직접 범위다. [maintain](../source/workflow-references/pstack/repository/skills/maintain-verification-skill/SKILL.md) 33행은 앱의 Launch 모델을 유지자가 따르게 한다. | 일반 생성·유지 skill에 앱 세부를 복제할 필요는 없다. 다만 map의 설명이 오래됐는지 제품 regression인지 판단하려면 기존 사용자 약속의 근거가 필요하다. 폴더 한정은 그 의미 판단을 자동으로 해주지 않는다. |
| host나 모델 실행 환경이 바뀐다 | [Claude Code 안내](../source/workflow-references/pstack/repository/docs/harness/claude-code.md) 3·9–28·34–60행이 tool명, agent 유형, 모델, transcript 경로, 미지원 단계를 매핑한다. Model 선택은 [setup-pstack](../source/workflow-references/pstack/repository/skills/setup-pstack/SKILL.md) 18–39행의 별도 rule이며 실제 지원값을 확인한다. | `readonly`는 Explore로 바꿔도 Bash가 남아 행동 지시와 상태 확인을 더한다. Cloud를 worktree로 치환하고 미지원 기능은 건너뛰는 것은 같은 능력의 보장이 아니다. [저자 README](../source/workflow-references/pstack/repository/README.md) 30행은 generated tree와 CI 동기화를 설명하지만 생성기·CI는 이 사본에 없어 효과를 확인하지 않았다. 우리의 06 전환에서는 실제 대상 host의 권한·입력·생명주기로 다시 확인해야 한다. |

이 세 사례는 `어느 구현을 고치고 어느 소비자를 확인할지`를 보여 준다. 모든 skill을 자유롭게 뗄 수 있다는 증거는 아니다. `poteto-mode`는 many sibling skills와 원칙·host·외부 plugin을 명시적으로 호출한다. [migrate-callers 원칙](../source/workflow-references/pstack/repository/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) 11–14행도 외부 사용자가 없고 협조된 breaking change가 가능한 내부 API로 범위를 제한한다. 이를 모든 스킬 제거의 실증으로 일반화하지 않는다.

## 우리 구성 논의에서 가져올 후보와 조건

| 후보 원리 | 우리에게 연결할 책임 | 채택 전에 다르게 봐야 할 조건 |
| --- | --- | --- |
| 직접 요청과 흐름 중 호출이 같은 전문 절차를 사용하되 자기 종료 조건을 갖는다 | 개발 중 자료 선택·이해·적용, 직접 맥락 읽기 요청을 같은 실행 방법으로 연결할 수 있다. | `how` 같은 코드 조사와 Project 권위 읽기는 대상이 다르다. 하나의 context skill, read/write 분리, development 상세+공통 지침 중 어떤 포장이 적절한지는 이 자료만으로 정해지지 않는다. |
| 공통 절차를 경로로 호출하고 대상 지식을 복제하지 않는다 | 기존 read/update가 Project 읽기·관리 canonical을 실행하고, development는 역할·작업 연결을 소유하는 구분을 유지할 수 있다. | 기존 [update](../source/ai-workspace-baseline/reference-project/.agents/skills/update-project-context/SKILL.md) 8·19–25행은 이미 내용 Owner와 live consumer 영향을 다룬다. 새 이름을 만든다고 새 책임이 생기는 것은 아니다. |
| 재개 지점 복원과 수행을 분리한다 | 02의 Work 기록은 다음 Main·담당자가 목표·현재 사실·선택·실물 근거를 찾게 하고, 실행 책임은 development로 돌아간다. | pstack의 기본 로컬 trail보다 지속성이 필요하다. Work 생성과 계승 의미의 선택은 일반 재개에서 분리해야 한다. 기존 Maintain의 자동 response-end 구현은 [현재 prototype Work](prototypes/development-workflow/noline-demo/context/work/AGENTS.md) 13행에 연결되지 않았다. |
| 일상 drift 수정, 개선 선택, 허용된 반영을 나눈다 | Main의 Work 유지, Project 사실 정정, Personal 기준 채택, 05 경험 개선 후보·효과 관찰을 연결하되 각 권위를 보존한다. | `reflect`가 특정 조직의 모든 future agent를 이유로 승인받는 정책을 그대로 모든 로컬 수정에 적용할 필요는 없다. 기존 사용자 권한·관리 계약이 우선이며 외부 tracker 자동 작성은 차용 대상이 아니다. |
| 개인 실행 관례와 별도 판단 본문을 경로로 연결한다 | `automate-me`처럼 반복 패턴의 근거와 사용자 의도를 확인한 뒤 개인 실행 방식만 mode에 두고, 유지 중인 원칙 본문은 그 Owner에 남길 수 있다. | Personal의 모든 기준이 모드 스킬인 것은 아니다. 이 예는 개인 mode의 생성·증분 갱신이며 Personal/Project/Work 전체 동기화나 내용 승격 프로토콜은 제공하지 않는다. |
| 문장 추가 전에 기존 규칙·구조·실제 실패를 대조한다 | 반복 문제가 맥락 누락인지, 호출 실패인지, 불명확한 기준인지, 도구/구조 문제인지 구별하고 맞는 Owner에 개입한다. | [encode-lessons](../source/workflow-references/pstack/repository/skills/principle-encode-lessons-in-structure/SKILL.md) 9–11행은 판단이 필요한 경우 지침·실패 예를 인정한다. 모든 판단을 schema·lint로 만들거나 모든 경험을 skill로 만드는 근거가 아니다. |

## 반대 근거와 자료 공백

1. **가벼운 구성이 항상 아니다.** `how`는 단순 질문도 explainer를 쓰고, `why` 31–75행은 연결된 일곱 출처 종류의 완전 탐색을 기본으로 한다. `recall` 20행도 이름 붙은 대상이면 공유 기록 조사를 기본 의무로 둔다. `show-me-your-work` 67행은 별도 모델 계열 검토를 필수로 둔다. [setup guide](../source/workflow-references/pstack/repository/docs/guide/01-setup.md) 45–52행도 비용을 인정하고 작은 명백한 수정에서는 mode를 피하라고 한다. 반복 context 선택마다 이 구조를 붙일 근거가 없다.
2. **담당 재사용 정책이 우리와 다르다.** Mode 101행은 fix·follow-up도 새 agent를 기본으로 한다. 우리 [execution](prototypes/development-workflow/skills/development/references/execution.md) 19–25행은 원래 구현자와 좁은 후속 검증자를 이어 쓰는 것을 기본으로 한다. 어느 쪽이 더 효과적인지 자료만으로 확정할 수 없다.
3. **세부 절차가 상위 일반 문구를 한정한다.** Mode 99행의 parent 자체 요약과 how 32행의 explainer 결과 light edit, mode 149행의 매 playbook 뒤 PR과 Investigation 12행의 no PR을 단순히 합치면 잘못된 흐름이 된다. 적용할 절차의 구체 종료·반환 계약을 함께 읽어야 한다.
4. **권한과 기계 제한이 다르다.** Why/reflect의 agent mode는 MCP를 위해 쓰며 read-only 의미는 프롬프트에 있다. Claude adapter 21행도 Explore에 Bash가 남는다고 명시한다. Mode 83행의 외부 chat/ticket 허용, reflect 49행의 무승인 backlog 작성, pause 7행의 모든 미커밋 WIP commit은 우리 지시·사용자 권한과 별도로 대조할 정책이다.
5. **운영 효과는 미입증이다.** 저자 README 7–9행의 일상 사용·품질·병렬 신뢰 주장은 자기 설명이다. 실제 제품의 Feature Map, 유지 실행 diff·증거, 여러 과제의 비용/실패율, 조직 전체 skill 변경 뒤 효과는 이번 사본에 없다. 형식·helper가 있다는 사실을 의미 정확성이나 성공 보장으로 바꾸지 않는다.
6. **스킬 작성과 host 배포의 일부 원문은 없다.** Cursor built-in `create-skill`의 draft/test/description optimization 계약은 보존본 밖이다. `harness/pstack/`·`scripts/generate-pstack-harness-trees.mjs`·CI 원문도 없어 host generated copy의 정합성 보장은 안내상 주장에 한정한다. [manifest](../source/workflow-references/pstack/manifest.json) 402–410행에서 제외 경계를 확인했다.
7. **복원 brief와 지속 context의 연결은 별도 판단이다.** 누락됐던 recall·automate-me 원문은 같은 판본으로 추가 확보해 위 분석에 반영했다. 그 결과 recall의 주제 맥락 복원과 automate-me의 개인 mode 생성·갱신까지 확인했으나, brief를 Work current에 반영하는 규칙, 새 독립 Work의 생성·계승 계약, 제품 계약과 개인 기준의 최종 권위 체계는 이 원문들에 없다. 실제 private 대화·생성된 개인 mode·후속 사용 결과도 확인하지 않았다.

현재 근거가 지지하는 설계 결정의 단위는 **맥락 탐색, 작업 의미 유지, 대상별 사실 갱신, 경험 개선 선택, 허용된 실제 변경**이다. 이들을 한 스킬에 모을지 나눌지는 실제 호출자가 반복해서 필요로 하는 입력·권한·종료 조건과 변경 영향을 보고 정해야 한다. Lauren의 구성은 그 비교 사례이며 우리 새 구성을 결정하는 정답은 아니다.
