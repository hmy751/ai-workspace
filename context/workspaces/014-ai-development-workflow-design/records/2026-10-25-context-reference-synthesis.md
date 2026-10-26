# 04-03 — Matt·Lauren 조사와 기존 시스템·새 개발 흐름의 종합

후속: [배치·사용 장면·파일 구성](2026-10-25-context-composition-walkthrough.md)을 제시한 뒤 사용자가 [이 정도 틀의 잠정 합의](2026-10-25-context-framework-provisional-agreement.md)를 요청했다. 참조와 스킬로 나뉘는 사용감에는 유보가 남아 있다. 아래는 조사 당시의 결과와 추천 이유이며 현재 합의·재개 범위는 후속 기록에서 읽는다.

2026-10-25. **조사 완료, 구성은 논의할 추천안이다.** 기존 read/update/create의 이름·개수를 유지하거나 하나의 context 스킬을 만들기로 확정하지 않았다. 실제 스킬·prototype·runtime은 이번 조사에서 수정·설치·실행하지 않았다.

## 먼저 판단할 내용

**개발 흐름이 맥락을 쓰고 유지할 시점을 연결하고, 반복되는 수행 방법은 재사용하되, Personal·Project·Work의 내용과 관리 책임은 각 영역에 남기는 구성을 권고한다.** 일상 읽기, 이번 Work 유지, 지속 기준의 변경, 경험 개선은 연관돼 있지만 시작 이유·수정 권한·끝나는 조건이 다르다. 이 차이가 실제 호출과 산출물에 이어져야 분리한 의미가 있다.

앞서 Main이 제안한 ‘선택·적용과 허용된 맥락 문서 반영을 하나의 context 스킬에 둔다’는 안은 **우선 추천에서 비교 후보로 내린다.** 이전 안도 내용 Owner와 Main·담당자를 구별했고, 경험 개선의 선택·코드 변경·새 Work 생성은 제외했다. 그 구분을 이번에 처음 발견한 것처럼 설명하지 않는다. 조정하는 것은 평상시 맥락 사용의 기본 진입을 새 스킬로 둘지다. 공유할 수 있는 방법이 있다는 사실만으로 한 스킬이 더 잘 발견되고 관리된다는 결론은 나오지 않는다. 이번 원문에는 일반 읽기에 별도 스킬 호출을 요구하지 않는 경우, 특정 내용의 능동적 구체화·유지만 맡는 스킬, 다른 절차를 조합하는 흐름, 일반 참조 파일이 함께 있다.

그렇다고 기존 세 스킬을 그대로 유지하거나 책임마다 새 스킬을 하나씩 만드는 것이 결론도 아니다. 현재 추천은 **일상 읽기는 workflow와 각 영역의 지침에서 직접 수행하고, 여러 호출자가 공유할 상세는 일반 참조로 두며, 능동적 관리·조사처럼 독립된 목적이 있는 과업만 필요에 따라 스킬화하는 것**이다. 직접 요청도 같은 방법을 쓰되, 개발 중 매번 사용자 호출·새 agent·별도 보고서·전체 재독을 요구하지 않는다. 이는 기존 문서 계약을 활용하는 설계 판단이며 세 방식의 실제 비용을 시험해 얻은 우열은 아니다.

## 요청과 조사 범위

사용자는 앞선 [조사 범위 제안](2026-10-25-context-reference-investigation-scope.md)을 보고 다음과 같이 요청했다.

> 좋아 그럼 그 방향으로 맷이랑 로렌 자료를 실제로 조사해봐. 지금 맥락 스킬 하나 만든다는 안에 맞추진 말고, 기존 시스템이랑 새 워크플로까지 같이 봐서 차용할 점이랑 우리한테 다르게 적용할 부분을 종합해줘

조사에는 기존 read의 의도와 반복 사용, 담당자 원문 읽기, Work current의 역할, 직접 요청과 개발 중 사용, 일상 유지와 개선 루프, 여러 영역에 걸친 책임·교체 가능성을 함께 포함했다. 앞선 [구성 비교](2026-10-25-context-responsibility-and-skill-architecture.md)와 [구체안](2026-10-25-context-responsibility-concrete-proposal.md)은 형성 근거이며 현재 결론으로 전제하지 않았다.

사용한 판본은 Matt **1.3.1 / `5beb35b…`**, Lauren의 pstack **0.15.29 / `190d287…`**다. 기존 보존 원문을 읽고, 선정에서 빠진 네 파일은 공식 저장소의 **동일 commit**에서 추가 확보했다. 최신판 전체를 조사한 것은 아니다. 상세 원문 위치·행·반대 근거는 [Matt 조사](2026-10-25-context-reference-matt-investigation.md)와 [Lauren 조사](2026-10-25-context-reference-lauren-investigation.md)에 있다. 추가 원문은 [Matt 관리 방침](../source/workflow-reference-supplements/2026-10-25-matt-maintenance/README.md), [pstack recall·automate-me](../source/workflow-reference-supplements/2026-10-25-pstack-context/README.md)에서 판본·URL·hash와 함께 찾는다.

## 원문에서 얻은 것과 우리 적용

| 조사 질문 | Matt에서 확인한 관계 | Lauren에서 확인한 관계 | 우리에게 차용할 점과 적용 차이 |
| --- | --- | --- | --- |
| 전체 흐름과 개별 절차를 어떻게 나누나 | `ask-matt`는 사람이 다음 스킬을 고르게 하는 안내다. 모델 호출 가능 스킬은 직접 요청과 다른 스킬의 수행 중 사용을 함께 지원한다. 공유 상세를 일반 파일로 두는 것도 허용한다. | `poteto-mode`의 parent가 playbook·배치를 맡고, 호출된 조사·검증 등의 절차는 자기 수행·반환을 맡는다. | development는 작업의 연결과 Main의 전체 판단을 맡고, 재사용 방법을 중복 정의하지 않는다. Matt의 안내 router를 우리의 실행 조정자로 보거나, Lauren의 모든 기본 호출을 그대로 옮기지 않는다. |
| 담당자는 무엇을 직접 읽나 | Project의 관련 glossary·ADR을 코드 탐색 때 읽는다. 기존 용어집을 읽는 것만으로 `domain-modeling`을 호출하지 않는다. | 담당자에게 mode 경로를 전달하고 적용할 원칙 leaf를 직접 읽게 한다. `how/why`는 맡은 질문의 원문과 반대 근거를 조사해 반환한다. | Main은 목표·범위·관련 접근점·판본을 전달하고 담당자는 필요한 원문을 읽어 적용한다. 질문이 바뀌면 추가로 선택한다. Lauren의 개인 mode 전체 상속을 Personal·Project·Work 전체 읽기로 확대하지 않는다. |
| 사용 중 갱신과 경험 개선은 어떤 관계인가 | 해결된 용어는 즉시 glossary에 반영한다. 별도 `retro`는 세션 근거에서 환경 개선 후보를 제시하고 끝난다. | 검증 지식 유지, `reflect`의 개선 후보·선택·편집, `correct`의 구조·검사 개선이 서로 다른 계약이다. | 현재 사실·진행을 맞추는 일은 05의 개선 채택을 기다리지 않는다. 경험에서 앞으로의 방식을 바꾸는 판단은 별도이며 결과가 문서일 필요도 없다. 두 자료 모두 우리의 채택 후 효과 관찰 전체를 제공하지 않는다. |
| 공통 방법과 대상 지식을 어디에 두나 | 일반 스킬은 Project 문서의 위치·읽는 조건을 연결하고, 제품 용어와 결정은 대상 Project가 보존한다. | 생성된 검증 스킬에는 앱별 실행·관측·Feature Map을 둔다. 유지자는 그 디렉터리만 고치고 제품 regression은 보고한다. | 공통 절차는 실제 내용·수정 기준의 위치를 따라간다. Project 제품 약속, Personal 판단, Work 선택을 실행 스킬 본문에 복제하지 않는다. 검증 map이 우리 Project 계약 전체와 같지는 않다. |
| 구성 요소를 바꾸거나 뺄 때 무엇을 관리하나 | 스킬 하나에도 문서·호출 관계·router·manifest 비용이 붙는다. 이름 변경도 참조와 사용자 진입에 영향을 준다. | 결정 trail 형식은 해당 스킬이 소유하고 다른 스킬은 그 형식을 재정의하지 않는다. host 차이는 별도 안내·adapter가 다룬다. | 단일 정본과 경로 참조만으로 교체가 끝나지는 않는다. 실제 읽는 곳·호출하는 곳·기존 기록·host를 함께 확인한다. 저자의 신규 기여 제한이나 내부 API 제거 조건을 보편 금지·보장으로 적용하지 않는다. |

주요 직접 근거: Matt의 [호출 규약](../source/workflow-references/matt-pocock/repository/.agents/invocation.md), [스킬 구성 기준](../source/workflow-references/matt-pocock/repository/skills/productivity/writing-for-agents/SKILL-MECHANICS.md), [Project 소비 지침 원형](../source/workflow-references/matt-pocock/repository/skills/engineering/setup-matt-pocock-skills/domain.md), [용어 구체화](../source/workflow-references/matt-pocock/repository/skills/engineering/domain-modeling/SKILL.md), [retro](../source/workflow-references/matt-pocock/repository/skills/engineering/retro/SKILL.md). Lauren의 [mode](../source/workflow-references/pstack/repository/skills/poteto-mode/SKILL.md), [검증 지식 유지](../source/workflow-references/pstack/repository/skills/maintain-verification-skill/SKILL.md), [reflect](../source/workflow-references/pstack/repository/skills/reflect/SKILL.md), [스킬 작성 playbook](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/authoring-a-skill.md).

## 기존 시스템에서 이미 있던 책임

이번 조사가 새로 발명한 것으로 설명해서는 안 되는 부분이 있다.

| 기존 요소 | 이미 소유한 의미 | 새 workflow에서 연결할 부분 |
| --- | --- | --- |
| [read-project-context](../source/ai-workspace-baseline/reference-project/.agents/skills/read-project-context/SKILL.md) | 질문에 따라 관련 Project 본문을 선택·이해·적용하고, 유효한 읽기는 재사용한다. 읽었다는 이유로 자동 기록하거나 Recover/Maintain을 다시 돌리지 않는다. | Project뿐 아니라 Personal·Work와 역할별 질문을 어떻게 선택하는지 연결한다. 일회성 수입만 하던 스킬로 단순화하지 않는다. |
| [update-project-context](../source/ai-workspace-baseline/reference-project/.agents/skills/update-project-context/SKILL.md) | 근거·권위·지속 범위·내용 Owner를 대조해 Project를 갱신하고 실제 소비 경로 영향을 확인한다. | 개발 중 발견한 사실, 새 제품 선택, 개인 기준 변화의 다른 권한을 보존한다. 모든 반영을 이 기존 Project 스킬의 책임으로 넓히지는 않는다. |
| [Recover](../source/ai-workspace-baseline/reference-project/context/work/harness/recover/README.md) | 기존 Workspace의 선택된 입력을 복원하는 기반 packet이다. 새 Work의 계승 의미 선택이나 실제 이해까지 보장하지 않는다. | 일반 재개와 한정 위임의 입력을 구별한다. 모든 담당자에게 같은 전체 인수를 강제하지 않는다. |
| [Maintain](../source/ai-workspace-baseline/reference-project/context/work/harness/maintain/README.md) | Work의 현재 의미와 지속 과정 근거를 구별해 유지한다. Project 승격·제품 결정·검증·작업 조정과 구별하며 의미 계약과 실행 adapter도 나눈다. | 현재 자동 runtime은 연결되지 않았고 Main이 관리한다. 이 의미 책임을 보존하면서 실제 기록 시점·Owner·연결은02와 구체화한다. |
| [create-context-workspace](../source/ai-workspace-baseline/reference-project/.agents/skills/create-context-workspace/SKILL.md) | 새 독립 Work 생성과 선택적 계승을 돕되, 생성 의미의 정본과 실행 도구를 구별한다. 생성과 activation도 다르다. | 이전 Recover/Verify/Maintain 설치를 전제로 한 부분을 현재 구조·대상 host와 대조한다. 단순 맥락 읽기나 채팅 재개로 흡수하지 않는다. |

우리 Work current에는 원문의 대체 복사본보다 **이번 목표에 어떤 기준을 적용했는지, 어떤 선택과 제한이 생겼는지, 현재 상태와 남은 판단이 무엇인지**가 필요하다. 그 선택이 중요한 이유와 원자료 접근점을 함께 남긴다. 담당자가 원문을 직접 읽는 것과 충돌하지 않는다. [현재 Work 지침](prototypes/development-workflow/noline-demo/context/work/AGENTS.md), [Project 관리](prototypes/development-workflow/noline-demo/context/project/MAINTENANCE.md), [Personal 관리](prototypes/development-workflow/noline-demo/context/personal/README.md)가 이미 가진 의미를 새 공통 스킬의 사유물로 옮기지 않는다.

Lauren의 `recall`은 최근 대화·공유 기록·실제 상태에서 요청별 맥락을 복원해 brief를 반환한다. 충분한 현재 상태가 있으면 mining을 생략한다. `automate-me`는 반복 관례와 사용자 의도를 확인해 개인 mode를 생성·갱신하고 다른 원칙을 경로로 참조한다. **두 절차 모두 우리 Work current의 지속 관리나 Personal 전체의 소유 체계를 대체하지 않는다.** Matt의 임시 handoff와 Lauren의 결정 TSV·resume note도 마찬가지다.

기존 Vercel 자료는 이 결론을 보조한다. [보존 article](<../source/lectures/vercel-product-design (1).md>)은 작업·표면에 따른 선택, 내용 정본 참조, 실행 지침과 관리 지침 구별, 근거 수집과 채택 판단의 분리를 설명한다. 다만 공개 article·발췌 예이지 전체 내부 시스템의 실행 증거는 아니다. 이 자료만으로 역할별 읽기 범위나 하나의 context 스킬 구성을 확정하지 않는다.

## 추천하는 실제 책임 연결

아래는 **책임 구분이지 새 스킬 여섯 개의 목록이 아니다.** 실제 행동자는 Main과 맡은 담당자이며 문서는 내용·관리 계약을, 스킬은 반복할 수행 방법을 제공한다.

| 책임 | 실제 수행과 끝나는 지점 | 유지할 위치·연결 |
| --- | --- | --- |
| 작업 연결 | Main이 목표·역할·범위·판본을 정하고, 새 정보가 기존 수행·검증에 미친 영향을 판단한다. | development가 조정한다. 공통 읽기·반영 알고리즘을 이곳에 모두 복제하지 않는다. |
| 필요한 맥락 사용 | 각 담당자가 현재 질문에 필요한 원문을 선택·확인·적용한다. 부족·충돌·선택 필요가 해결되거나 그 한계를 인계할 수 있으면 본래 과업으로 돌아간다. | 공통 읽기 방법과 각 영역의 진입점·읽기 기준을 사용한다. 단순한 유효 원문 재사용은 별도 관리 과업이 아니다. |
| 현재 Work 유지 | Main이 지속할 적용 이유·선택·상태·근거를 Work 계약에 맞게 남긴다. 담당자가 별도 기록 역할을 맡았으면 그 범위에서 수행한다. | Work current·records·output의 구별을 따른다. 담당자 반환을 공유 current의 무제한 수정권으로 바꾸지 않는다. |
| 지속 내용 반영 | 허용된 수행자가 사실 정정인지 새 기준·약속 선택인지 판단하고, 해당 영역의 관리 기준으로 필요한 본문·진입·소비 경로를 맞춘다. | Personal·Project·Work가 각 의미·권위를 소유한다. 공통 대조 방법을 재사용할 수 있지만 모든 영역의 결정을 대신하는 관리자는 두지 않는다. |
| 경험 개선 | 실제 장면에서 문제와 수단을 고르고, 채택된 코드·검사·도구·지침·역할 변경을 맞는 수행자에게 연결하고 이후 효과를 판단한다. |05가 선택·채택·관찰을 구체화한다. 문서 갱신은 가능한 결과 중 하나다. 매번 일상 유지를 이 루프에 통과시키지 않는다. |
| 새 Work·실행 환경 전환 | 독립 목표·계승할 의미를 정하고, 대상 host와 기존 canonical을 보존하며 실행 수단을 연결한다. | 새 Work 계약과06이 담당한다. 재개 brief 생성, 현재 Work 정리, 일반 읽기와 구별한다. |

예를 들어 로그인 흐름을 변경한다면 다음처럼 이어진다.

1. Main은 맡은 목표·변경 범위와 관련 Project 계약·Personal 기준·현재 Work 선택의 접근점을 준다. 담당자는 이를 직접 읽고, 구현 중 새 실패 조건을 만나면 관련 원문·코드를 추가 확인한다.
2. 담당자는 결과와 함께 판단을 바꾼 조건·충돌·남은 선택을 반환한다. Main은 이번 작업의 적용 의미가 달라졌다면 Work를 갱신한다. 매번 읽은 문서 목록이나 원문 전체를 current에 옮기지 않는다.
3. 허용된 기능 변경에 따라 Project의 현재 구현 설명이 오래됐다면 그 Owner의 관리 기준으로 맞춘다. 기존 제품 약속과 실제 동작이 충돌한다면 현 동작을 근거로 약속부터 바꾸지 않고, 요구·결함·새 선택 중 무엇인지 판단한다.
4. 여러 작업에서 같은 입력 누락이 드러나면05에서 그 원인이 문서 부재, 잘못된 읽기 조건, 실행 누락, 도구 문제 중 무엇인지 보고 개선 수단을 고른다. 이미 명료한 문장을 다시 추가하는 것으로 끝내지 않는다.
5. “지금 관련 맥락만 읽어줘”라는 직접 요청은1의 읽기 방법으로 끝날 수 있다. “확인한 변경을 Project에 반영해줘”는3의 관리 계약으로 들어간다. 같은 방법을 재사용한다고2~4까지 항상 실행할 이유는 없다.

## 스킬 구성 대안의 판단

| 구성 | 이점 | 이번 근거에서 남는 부담 | 현재 추천 |
| --- | --- | --- | --- |
| 하나의 context 스킬 안에 읽기와 허용된 맥락 문서 반영을 둔다 | 진입이 단순하고 공통 대조를 가까이 유지할 수 있다. | 읽기만 필요한 담당자에게 여러 영역의 관리·기록·권한 분기가 붙을 수 있다. 조건부 상세로 이를 막을 수 있다. 기존 제안도 Owner와 경험 개선의 경계를 구별했으므로 한 파일 자체가 책임 혼합이라는 뜻은 아니다. | 비교 후보로 유지한다. ‘같은 맥락’이라는 말만으로 우선 채택하지 않는다. |
| 읽기와 갱신을 독립 스킬로 나눈다 | 수정 유무와 반환 차이가 드러나고 직접 요청이 명료해질 수 있다. | 갱신 쪽이 여전히 Personal·Project·Work 전체의 권위를 떠맡으면 문제를 옮긴 셈이다. 반대로 작은 일마다 여러 호출을 강제해도 과하다. | 반복 호출·수정 범위가 실제로 독립하는 부분에 선택적으로 적용한다. 기존 이름을 그대로 유지할 의무는 없다. |
| 일상 읽기는 workflow·영역 지침에서 직접 수행하고, 공통 상세는 일반 참조로 두며, 능동적 과업만 필요에 따라 스킬화한다 | 이미 있는 읽기 경로를 사용하고, 조사·조정·반영처럼 별도 결과가 필요한 과업에는 적합한 실행 진입을 둘 수 있다. | 경로만 많고 읽을 조건이 없으면 찾기 어렵다. 직접 읽기로 충분한 경우와 재사용 절차가 필요한 경우를 구체화해야 한다. | **현재 추천이다.** 새 context 스킬을 모든 맥락 사용의 기본 진입으로 전제할 필요가 확인되지 않았기 때문이다. 독립 과업이 반복되는 곳은 새 스킬도 열어 둔다. |

세 안 모두 앞 절의 책임 경계를 지켜야 한다. 차이는 그 책임을 지키느냐가 아니라 **공통 방법을 어디에서 발견하고 어떤 경우 실행 절차로 들어가느냐**다. 일상 읽기·정리·반영의 대표 장면에서 실제 경로와 부담을 대조한 뒤 최종 포장을 선택한다.

독립 스킬 여부는 직접 요청 빈도 하나로 정하지 않는다. **독립해서 반복되는 목적이 있는지, 여러 호출자가 같은 입력·결과를 필요로 하는지, 수정 권한·종료 조건이 응집돼 있는지, 따로 변경할 이유가 있는지**를 함께 본다. 단순 공유 기준은 일반 참조로 충분할 수 있고, 여러 수행을 조합하는 목적이 반복되면 얇은 조합 스킬도 가능하다. 실제 host에서의 발견·호출 가능성은06에서 확인해야 한다.

## 유지·교체가 가능한지 확인할 장면

- **Work 기록 구조 변경:** Work 계약과 실제 기록·재개 소비자를 바꾼다. 일반 읽기 방법이 특정 current 파일 구조를 중복 정의했다면 그 결합을 줄여야 한다. Personal의 판단 본문이나 Project 제품 약속까지 같은 변경으로 고칠 이유는 없다.
- **공통 읽기 방법 교체:** workflow의 읽기 조건·호출 경로와 담당자 사용을 확인한다. 기존 정본·Work 적용 판단은 계속 남아 있어야 한다. 이름만 바꾸면 문서·metadata·설치·호출 안내도 영향을 받는다.
- **경험 개선 절차 비활성화:** 그동안 일상 개발·Work 유지·허용된 사실 정정은 계속돼야 한다. 개선 후보 선택을 멈춘 일이 현재 상태 기록까지 중단시키면 책임이 섞인 것이다.
- **host 전환:** 파일 경로·스킬 발견·호출·권한·agent 생명주기를 맞춘다. 원래 의미 계약까지 host 이름에 따라 재정의하지 않는다. adapter가 있다는 사실과 같은 행동을 재현했다는 것은 별도다.

이것은 후속 대조할 설계 장면이다. 실제 제거·교체 실험을 통과했다고 기록하지 않는다.

## 그대로 가져오지 않을 것과 남은 작업

Matt의 `CODING_STANDARDS.md`를 review에 배치하는 정책은 특정 코딩 기준의 소비 배치다. 우리의 Personal 기반 구현과 관련 기준을 공유하는 검토 합의를 뒤집는 근거가 아니다. Lauren의 mode 전체 상속·고정 모델·새 agent 기본값·매번 다중 조사도 우리 역할 재사용과 비용 판단에 맞게 다시 봐야 한다. 외부 tracker 자동 기록·WIP commit·PR 기본값은 저자의 권한 전제이며 이번 사용자 요청으로 차용되지 않는다.

02는 Work의 현재 의미·과정 근거와 관리 시점,05는 개선 선택·채택·효과·철회,06은 대상별 배치·새 Work·host 전환,07은 실제 연결의 확인을 계속 맡는다. 이번 연구가 이 Ticket들을 완료시키거나 실행 단계 이름으로 바꾸지는 않는다.04-03에서 먼저 구체화할 것은 **담당자의 평상시 읽기, 새 사실·선택의 Work/Project 반영, 직접 요청**이 위 책임 경계 안에서 어떻게 끝나는지다. 그 장면을 보고 공통 파일·기존 스킬 재구성·필요한 새 스킬의 실제 묶음을 정한다.

이번 결과는 보존 원문과 추가 공식 원문의 지시·책임·연결을 조사한 것이다. 실제 스킬 수행의 효과·비용·host 호환·장기 유지·제거 성공은 시험하지 않았다. 두 조사와 별도 원문 검토에서 주요 책임 해석을 대조했으며, 하나의 context 스킬에 대한 지지와 반증을 과장하지 않았다. 기록 링크·새 사본의 크기/hash·수정 범위는 별도 확인하고 결과를 아래에 남긴다.

## 보존 확인

종합·두 조사·세 source 안내의 Markdown 6개에서 로컬 링크112개가 존재하는 것을 확인했다. 새 raw 사본4개의 크기·SHA-256이 각 manifest와 일치했다. 이번 진입점 수정의 `git diff --check`는 통과했다. 기존 tracked source의 변경은 안내 README뿐이며 기존 raw·manifest는 수정하지 않았다. 스킬 실행·제품 검사·교체 실험은 수행하지 않았다.
