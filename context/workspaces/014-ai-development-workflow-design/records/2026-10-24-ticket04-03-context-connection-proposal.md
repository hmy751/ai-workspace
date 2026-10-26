# 04-03 — 개발 수행과 실제 context를 연결하는 안

2026-10-25 후속: 사용자는 세부화 전에 목적·범위와 전체 스킬 구성을 다시 보자고 요청했다. [종합 비교](2026-10-25-context-responsibility-and-skill-architecture.md)가 현재 논의 입력이다. 아래 read/update 독립 존속 추천은 보류하고 실제 경로 조사와 당시 제안은 형성 근거로 보존한다.

2026-10-24. **권고는 기존 읽기·갱신 책임을 유지하면서, 대상의 실제 진입점·역할 인수·변경 전달·다음 재개를 연결하는 것이다.** 현재 prototype에는 관련 본문과 기본 경로가 이미 있다. 모든 역할에게 같은 자료를 주거나 새 context 스킬 하나로 합치는 것이 필요한 상태는 아니다. 가장 큰 비호환은 기존 Workspace 생성 스킬이 현재 demo에 없는 Harness를 전제한다는 점이다.

이 문서는 [04-03](../current/tickets/04-skill-improvements/04-03-context-skills.md)의 첫 구체 연결안이다. 현재 본문에서 확인한 사실과 아래 보완 권고를 구별한다. **설계 논의용이며 실행 본문 반영·스킬 설치·새 Workspace 생성·전체 수행 시험은 하지 않았다.** 01-01·01-03의 역할·진행·인계 설계 마감은 유지한다.

## 출발점과 현재 판단

이번 요청은 다음과 같다.

> 014 current 읽고 04-03 context 연결부터 이어가자

[직전 재개 기록](2026-10-24-workflow-context-connection-checkpoint.md)에 보존된 “04-03은 스킬도 스킬이지만 어쨋든 구체적으로 이게 context과 어떻게 연결되는가도 맞을까?”를 범위로 이어받았다. 첫 결과는 시작·역할 수행·변화·완료/재개에서 어떤 내용이 실제 판단에 들어가고 어디로 돌아가는지의 제안이다. 사용자에게 남은 것은 연결안의 선택이며, 기존 역할 설계 전체를 다시 정하는 일이 아니다.

현재 [development](prototypes/development-workflow/skills/development/SKILL.md)는 필요한 맥락 선택·추가 탐색·역할 연결·Owner별 갱신을 이미 설명한다. [demo root](prototypes/development-workflow/noline-demo/AGENTS.md)는 일반 재개와 한정 위임을 구별하고, [context 입구](prototypes/development-workflow/noline-demo/context/README.md)는 Personal·Project·Work로 안내한다. [작업 해설](prototypes/development-workflow/walkthrough.md)에는 이름 선택과 제품 계약의 적용, 새 소비자 요구와 갱신 대상도 있다. 따라서 아래에서 구체화할 것은 이 경로의 조건·전달·예외이며, 읽기·갱신 원칙이 없다는 진단은 아니다.

## 실제 연결에서 각 문서가 맡는 일

| 담당 | 연결에서 맡을 일 | 기존 정본 |
| --- | --- | --- |
| 대상 root·context·Work 입구 | 어느 Project와 Workspace인지, 일반 재개인지 한정 위임인지 정하고 실제 본문으로 안내 | [root](prototypes/development-workflow/noline-demo/AGENTS.md), [context](prototypes/development-workflow/noline-demo/context/README.md), [Work 지침](prototypes/development-workflow/noline-demo/context/work/AGENTS.md) |
| development | 이번 질문에 필요한 Personal·Project·Work를 선택하고 적용·추가 탐색·결과 갱신을 조율 | [공통 수행 본문](prototypes/development-workflow/skills/development/SKILL.md) |
| 역할별 수행 상세 | 같은 자료를 어떤 질문으로 판단하고 무엇을 반환할지 정함 | [실행 배치](prototypes/development-workflow/skills/development/references/execution.md), [개선 검토](prototypes/development-workflow/skills/development/references/review.md), [검증](prototypes/development-workflow/skills/development/references/verification.md) |
| Personal·Project | 실제 판단 기준·이유·조건, 제품 약속·개발 규약·현재 구현 사실을 소유 | [Personal](prototypes/development-workflow/noline-demo/context/personal/README.md), [Project](prototypes/development-workflow/noline-demo/context/project/README.md) |
| Work | 이번 목표·선택·진행·근거·결과 위치를 이어감 | [001 Workspace](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/README.md) |

**대상 경로는 작업 대상의 root 지침에서 찾는다.** 현재 스킬은 `development-workflow/skills/`, 대상은 `development-workflow/noline-demo/`에 있다. source 스킬의 `../../../context/...`를 그대로 복사하면 이 배치의 context를 찾지 못한다. Git 저장소 최상위와 작업 대상 Project가 항상 같다는 전제도 이 nested demo에는 맞지 않는다. 대상 root·Workspace가 이미 지정됐으면 그 값을 사용하고, 불명확할 때 현재 경로·상위 지침·요청을 대조한다. 어떤 대상을 고르는지에 따라 결과가 달라지고 근거로 정할 수 없을 때만 확인한다.

이 경로 해석은 root와 스킬 진입의 보완 대상이다. Project의 제품 본문이나 Personal에 절대 경로 목록을 새로 관리시키지 않는다. 실제 host의 검색·bridge·배포는06에서 확인한다.

## 장면 1 — 기존 작업을 재개한다

예시는 “로그인 완료 표현 작업을 이어서 보자”다. 현재 일반 재개 경로는 다음과 같이 존재한다.

1. demo root와 Work 지침에서 [001 Workspace README](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/README.md)를 찾는다.
2. [memory](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/current/memory/index.md), [state](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/current/state/index.md), [output](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/output/index.md)에서 목표·현재 선택·확인 범위·남은 일과 실제 결과를 복원한다. 필요한 Spec·Ticket으로 내려간다.
3. 현재 쟁점에 따라 [Personal 선택](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/current/memory/personal-context.md)과 [Project 선택](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/current/memory/project-context.md)의 이유·본문을 사용한다. 이미 유효한 본문을 확보했다면 다시 전부 읽지 않는다.

이때 복원할 판단은 “개명을 택했고, 조회는 기다리지 않으며, 메모리 예제의 확인과 실제 제품 통합은 다르다”다. 파일 목록을 읽었다는 보고로 이 이해를 대신하지 않는다. 단순 표현 보완이면 이름 기준·해당 사용처에서 끝낼 수 있고, 최신 조회가 필요한 새 소비자라면 다음 장면처럼 선택을 바꾼다.

두 선택 문서는 **현재 적용할 내용과 이유**를 소유하며 최초 입력판의 사본이 아니라는 점도 이미 명시한다. 보완할 것은 이 구별을 실제 인수 예제에 연결하는 일이다. 현재 작업을 이어갈 때는 최신 본문을 사용하고, 과거 선택의 타당성을 따질 때는 당시 source·record·판본을 확인한다. 현재 설명이 과거 구현자의 입력이었다고 가정하지 않는다.

재개마다 Project의 모든 물리 layer·Personal 사례·형성 자료를 읽히거나, 선택 문서에 일반 기준 전문을 복제할 필요는 없다. 이번 선택이 달라졌을 때 해당 이유와 연결만 갱신한다.

## 장면 2 — 역할이 인수하고 새 질문을 발견한다

Main은 맡긴 결과·보존 조건·대상·판본·권한·중요한 공백을 직접 전달한다. 담당자는 적용 지침과 요구·관련 정본·실물을 직접 읽는다. 요약은 작업의 방향과 범위를 주고, 원문은 판단 근거를 제공한다. 자동 상속된 대화·지침도 실제 입력에 포함되므로 [execution](prototypes/development-workflow/skills/development/references/execution.md)의 인수 기준을 유지한다.

| 역할 | 로그인 예제에서 직접 판단할 연결 | Main에게 반환할 것 |
| --- | --- | --- |
| 구현자 | Ticket의 요구와 [인증 계약](prototypes/development-workflow/noline-demo/context/project/guidance/authentication-and-session/INDEX.md), [이름·완료 기준](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/INDEX.md)을 실제 호출자·반환·실패 처리에 적용 | 구현과 자기 확인, 선택 이유와 적용 조건, 현재 근거·미확인 |
| 개선 검토자 | 원래 요구·관련 기준과 실제 코드를 읽고, 현재 이름·책임·대기 방식과 대안의 이득·비용을 별도 판단 | 유지/변경 의견과 직접 근거. Main의 요약이나 기존 선택을 결론으로 받지 않음 |
| 검증자 | 요구·제품 계약·사용 조건에서 기대 결과를 만들고 현재 코드·검사의 충분성을 판단 | 요구별 근거·실패·미확인과 필요한 재현. 구현자가 골랐다는 이유만으로 기대값을 채택하지 않음 |

현재 runtime 본문에는 이 책임이 있다. **추가할 구체 장면은 새 질문 때문에 처음의 자료 선택이 달라지고 그 결과가 다음 담당자에게 이어지는 경우**다.

예를 들어 “새 화면은 로그인 뒤 최신 여행 목록을 바로 사용해야 한다”는 가상 요구가 들어왔다고 하자. 실제 구현 요청이나 관찰된 결함은 아니다.

- 출발점은 새 소비자의 요구와 코드다. 기존 [Project current](prototypes/development-workflow/noline-demo/context/project/current/authentication-flow/INDEX.md)가 설명하는 `signInAndRequestRefresh`는 조회 완료를 보장하지 않는다.
- [인증 계약의 대기 조건](prototypes/development-workflow/noline-demo/context/project/guidance/authentication-and-session/INDEX.md)과 Personal의 “실패 범위와 기다릴 범위는 별도”라는 판단을 함께 적용한다. 조회 실패가 인증을 취소하지 않는다는 이유만으로 비대기를 유지할 수 없다.
- 기존 Login·Reauth는 조회 결과를 즉시 쓰지 않는다. 새 소비자만 조회를 기다리는 방식과 공통 완료 경계를 바꾸는 방식의 영향·부담을 비교한다. 기존 계약으로 해결 가능하면 그 안에서 판단하고, 실제로 새 제품 약속을 결정해야 할 때만 해당 권한으로 연결한다.
- 담당자는 추가로 확인한 계약·실제 사용처, 선택이 바뀐 이유와 영향을 반환한다. Main은 관련 담당자의 입력과 필요한 재확인을 갱신한다. 모든 agent에게 전체 자료를 다시 배포할 필요는 없다.

판본이 바뀌면 변경된 코드·계약·가정에 걸린 이전 의견과 검사만 재평가한다. 커밋·미커밋 변경 또는 필요한 입력 사본 등 대상에 맞는 식별을 사용하며, 모든 본문 읽기에 해시·영구 로그를 요구하지 않는다. 접근하지 못한 자료는 그로 인해 남는 판단 공백으로 반환한다.

## 장면 3 — 바뀐 사실과 판단을 기록하고 정본에 반영한다

Main은 반환 내용을 “이번 선택인가, 제품이 계속 지킬 약속인가, 현재 구현 사실인가, 개인 기준의 의미 변화인가”로 판단한다. 기록 시점을 매 응답 종료로 고정하지 않고, 다음 수행이 달라질 결정·변경·중요한 확인·막힘이 생겼을 때 필요한 곳을 맞춘다. 대화 중 선택·실제 반영·검사 결과를 같은 완료 상태로 쓰지 않는다.

| 변화 | 실제 반환 위치와 다음 재개 |
| --- | --- |
| 새 소비자만 조회를 기다리기로 선택 | 해당 Work의 Ticket·필요한 Spec과 current에 요구·선택·남은 일을 남긴다. 대안 비교·확인은 records, 실제 결과 위치는 output에서 찾는다. 기존 공통 인증 약속이 그대로면 guidance의 계약을 바꾸지 않는다. |
| 구현·지원 경계가 실제로 바뀜 | 확인한 범위만 Project current에 반영한다. Work에는 이번 변경·근거·미확인을 남긴다. 다음 작업은 Project 입구에서 현재 지원 범위를, 해당 Work에서 선택·검사 경위를 찾는다. |
| 공통 완료 약속을 권한 있게 변경 | Project guidance의 계약과 필요한 설명·읽기 경로를 갱신한다. 관련 Work의 요구·선택·이전 검증 근거가 영향을 받는지 Main이 확인하고 담당자를 연결한다. 코드 관찰만으로 약속을 바꾸지 않는다. |
| 여러 작업에 적용할 개인 기준의 의미·조건을 변경 | Personal의 해당 본문과 필요한 형성 자료를 갱신하고 사용 중인 Work의 판단 영향을 살핀다. 제품 의미·규약이 바뀌지 않았다면 Project를 같이 고치지 않는다. |
| 국소 결함 수정·검증 실패·새 미확인 | Ticket/current에 상태·다음 행동을, 재현·중요한 비교 근거는 records에 남긴다. 지속 제품 사실이나 약속 변화가 없으면 Project 갱신 스킬을 호출하지 않는다. |

반영은 기존 [Project 관리](prototypes/development-workflow/noline-demo/context/project/MAINTENANCE.md), [Personal 관리](prototypes/development-workflow/noline-demo/context/personal/README.md), [Work 지침](prototypes/development-workflow/noline-demo/context/work/AGENTS.md)을 따른다. Personal·Project의 의미·조건 변경에는 [CONTENT-POLICY](prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)에 따라 관련 형성 자료도 확인한다. 일반 적용이나 뜻이 같은 문구 수정에서 전체 형성 자료를 읽지 않는다. Work의 새 `_background` 구성 보류는 유지한다.

**update-project-context의 쓰기 책임과 Main의 전체 갱신 책임은 구별한다.** 스킬은 Project 본문을 반영하고 관련 Work·코드·검사에 미칠 영향을 반환한다. Main이 그 영향을 실제 담당자와 연결해 현재 선택·상태·근거를 맞춘다. 스킬을 호출했다는 이유로 Work나 제품 코드의 수정 권한까지 얻지는 않는다. Main이 직접 모두 수행할 때도 어떤 책임으로 변경했는지 구별한다.

## 장면 4 — 완료 뒤 이어가거나 독립 작업을 만든다

같은 결과를 마무리하는 오류 수정·미확인 해소·설명 보완은 기존 Workspace에서 이어간다. 세션이 새로 열렸다는 이유로 Workspace를 새로 만들지 않는다. Main은 현재 상태에서 확인한 결과·남은 문제·다음 행동을, output에서 실제 산출물을, records에서 필요한 상세 근거를 찾게 한다. 새 후속 작업이 생겼다고 이전 Workspace의 미완료를 완료로 바꾸지 않는다.

사용자가 독립·후속 Workspace 생성을 요청하면 새 목표·범위·완료 장면에 필요한 현재 의미를 선별한다. 예를 들어 사용자가 “실제 기기 저장소 연결은 별도 작업으로 만들자”고 했다면, 새 Work에는 저장 전 공개 금지·같은 계정 데이터 보존과 현재 메모리 예제의 한계, 실제 어댑터의 부분 실패·복구라는 첫 판단을 직접 설명한다. 과거 이름 A/B의 전 과정을 기본 입력으로 복제할 필요는 없다. 이 예시는 생성된 Workspace나 승인된 제품 요구가 아니다.

현재 demo에는 생성·전환의 지속 계약과 Harness가 없다. 권고는 다음과 같다.

- Work의 생성·전환 계약에서 요청 조건, 새 목표에 필요한 의미 선별, current/source/output/records의 역할, 기존 작업과의 단방향 참조, 생성과 활성화의 구별을 설명한다. 실제 파일은 Work의 기존 구성 안에서 정하며 새 형성 자료 층을 도입하지 않는다.
- 현재 수동 prototype에서는 생성한 문서의 실제 진입점만으로 목표·제약·첫 판단·필수 원문을 복원하는지 확인할 수 있게 설계한다. 이런 읽기 대조를 Recover 실행이나 제품 Verify로 부르지 않는다. 실제 수행 시험은 후속 계획과 구별한다.
- Recover·Verify·Maintain이 설치된 대상의 machine schema·실행·활성화는 해당 runtime 계약으로 연결한다. 지금 없는 runtime이나 빈 JSON을 추가해 원형 스킬을 충족시키지 않는다. 수동 계약과 실제 대상 연결의 정합은02·06에서 함께 구체화한다.

**수동 demo의 기본 Workspace 선택은 기존 [Workspace 목록](prototypes/development-workflow/noline-demo/context/work/workspaces/README.md) 한곳이 맡도록 권고한다.** 현재 root·context 입구도001을 직접 안내하므로, 둘째 Workspace를 추가할 때에는 일반 재개 안내가 이 목록의 현재 선택을 따르게 맞춘다.001 링크는 이름을 명시한 예제 접근점으로 남길 수 있지만 별도의 현재 선택으로 관리하지 않는다. 새 JSON이나 세션 binding은 만들지 않는다.

사용자가 Workspace를 명시한 요청에서는 그 대상을 읽는다. 명시가 없을 때만 목록의 기본 선택을 사용한다. 생성만 요청했다면 새 Workspace를 목록에 등록하고 기본 선택은 유지한다. “그 작업으로 넘어가자”처럼 전환까지 요청했다면 새 진입점의 준비 상태와 넘길 의미를 확인한 뒤 Main이 목록의 선택을 바꾸고 실제 대화에서도 그 Work를 인수한다. 다음 일반 재개는 root에서 같은 선택에 도달해야 한다. 파일 선택 변경을 host activation 성공으로 보고하지 않는다. 이 수동 전환안은 현재의 빈 생성 계약을 구체화하는 후보이며 운영 host의 binding을 대체하기로 결정한 것이 아니다.

## 세 기존 스킬의 유지·보완 판단

비교 대상은 보존된 [Noline 스킬](../source/noline-baseline/.claude/skills/README.md)과 [Reference 스킬](../source/ai-workspace-baseline/reference-project/.agents/skills/README.md)이다. 현재 운영 저장소를 새로 조사한 결과가 아니다.

| 스킬 | 확인한 현재 계약·차이 | 이번 권고 |
| --- | --- | --- |
| [read-project-context](../source/ai-workspace-baseline/reference-project/.agents/skills/read-project-context/SKILL.md) | 두 판본의 핵심은 같다. 질문별 Project 본문 선택, 유효한 선행 읽기 재사용, 계약·예외·현재 차이의 실제 적용, 원래 작업 복귀. 기본 읽기 전용이며 영구 보고서·Recover 재실행을 요구하지 않는다. Noline은 실제 Owner 대조에 app/package guide도 명시한다. | Project 한정 역할 유지. 대상 경로를 찾는 방식을 현재 배치에 맞추고 development의 일반 재개·한정 위임·새 질문에서 필요한 때만 연결. Personal·Work 전체 읽기를 흡수하지 않음. |
| [update-project-context](../source/ai-workspace-baseline/reference-project/.agents/skills/update-project-context/SKILL.md) | 두 판본은 의미상 같다. 지속할 제품 의미·현재 사실·조건 변화와 누락 복원·승인된 Owner 이동을 다룬다. 쓰기 전 보존 의미·근거·미정·영향받는 진입점을 정하고 본문과 실제 소비 경로를 대조한다. | Project 한정 역할 유지. 기존 관리 계약을 실행하며 Main에게 관련 Work·검사·다음 읽기에 미치는 영향을 연결. 형성 자료 정책은 관리 문서에서 읽고 스킬에 복제하지 않음. |
| [create-context-workspace](../source/ai-workspace-baseline/reference-project/.agents/skills/create-context-workspace/SKILL.md) | 두 판본 모두 이미 설치된 Harness, machine identity·Recover/Verify 계약·bounded Recover·Maintain 활성화를 전제한다. Reference는 layer 순회에서 주제별 선택으로 개선했지만 세 물리 layer 부재를 repair로 보는 조건은 남아 있다. | 의미 선별·새 Work 구성·재진입 판단과 runtime 실행을 분리하는 안을 권고. 현재 demo용 생성·전환 계약을 먼저 구체화. 기존 스킬의 고정 경로·물리 구조·activation을 그대로 복사하지 않음. |

여섯 스킬 설정의 `allow_implicit_invocation: true`는 각 본문의 조건을 없애지 않는다. create는 새 Workspace 요청이 조건이고 단순 재개에는 비적용이다. 현재 prototype에 세 스킬의 실행 파일은 없으며 development는 설치·호환되는 스킬이 없으면 Main이 직접 수행하도록 이미 설명한다. 원형 보존과 실제 설치를 혼동하지 않는다.

스킬 색인의 자동 연결 부재 시 Maintain 수동 호출 안내도 현재의 Main 직접 문서 갱신과 다르다. Noline의 `.claude/skills` 원본·bridge와 Reference의 `.agents/skills` 원본·도구별 bridge 차이는06의 배치 입력으로 남긴다. 이 비교만으로 어느 쪽 배치를 채택하지 않는다.

## 어디를 구체화하고 어떤 비용을 피할 것인가

| 보완 위치 | 넣을 내용과 유지할 경계 |
| --- | --- |
| development의 기존 맥락 선택·관련 스킬·Owner 갱신 절 | 대상 root에서 시작하고, 현재 선택을 역할 입력으로 연결하며, 변화가 영향을 준 담당자·근거·기록으로 돌아가는 공통 관계. 제품 기준·Project 관리 정책 전문은 복제하지 않음. |
| execution·review·verification의 기존 인수 부분 | 현재판과 과거 입력판 구별, 변경된 가정·판본·읽기 공백의 전달을 기존 역할 질문에 대입. 동일한 context 목록을 세 상세에 각각 새로 만들지 않음. |
| walkthrough와 실제 Work 선택 문서 | 위 네 장면의 구체 경로·판단 차이·반환 예시. 실제 실행 이력과 가상 후속을 명시하고, 과거 기록을 새 역할의 실행 증거로 바꾸지 않음. |
| read/update 후보와 대상 진입 | 대상 경로 식별·조건부 연결. 이미 충분한 선행 읽기에서 재호출하거나 읽기마다 기록을 만들지 않음. |
| Work 생성·전환 계약과 create 후보 | 수동 의미 계약을 먼저 구성하고 runtime 의존을 명시. Work 전체 재편이나 Recover/Verify 제거·유지를 이 작업에서 일괄 확정하지 않음. |

추가 파일은 별도 적용 조건·변경 이유가 생기는지로 판단한다. 현재의 공통 연결은 development의 기존 절부터 고치는 편을 권고하며, 이번 제안만으로 별도 context 조율 스킬·전체 맥락 지도·새 상태 필드를 만들지 않는다. 독립·후속 Workspace 생성은 별도 발동·변경 범위가 있으므로 Work의 생성 계약으로 다룰 이유가 있다.

읽기 비용은 현재 질문을 바꿀 본문·실물만 선택하고 유효한 선행 읽기를 재사용해 제한한다. 기록 비용은 선택·근거·현재 상태의 각 역할에 맞는 내용을 남겨 제한하며, 기록을 줄이려는 이유로 중요한 대안·원문·실패 근거를 지우지 않는다. 실제 읽기량·재개 품질·수행 비용은 이 문서 대조로 측정한 것이 아니다.

## 이번 확인과 다음 판단

Main은 현재 root·context·Personal·Project의 읽기/관리·development·execution·작업 해설·실제 선택 문서와 원형 세 스킬을 대조했다. 두 읽기 전용 조사자가 Noline/Reference 차이와 Work의 실제 진입·갱신·생성 공백을 나누어 확인했다. 조사자는 기존 자료 비교 담당이며 새 역할 수행의 효과를 시험한 것이 아니다. 조사 시작 때 작업 트리는 깨끗했고 기준 HEAD는 `3c7a1e3`이었다.

부모 대화를 받지 않은 별도 읽기 전용 개선 리뷰에서, 새 Workspace 생성 뒤 기본 재개 대상이 root·context·목록의001 직접 링크 사이에 남는 공백을 지적했다. 이를 받아 장면4에 목록 한곳의 기본 선택·명시 요청 우선·생성과 전환의 차이·입구 갱신을 구체화했다. 이는 제안의 문서 대조이며 실제 생성·전환 성공을 확인한 시험이 아니다. 작업 중 별도 세션의04-02 변경이 추가됐으며 해당 내용은 이번04-03 변경과 구별해 보존한다.

리뷰의 핵심 반환은 다음과 같다.

> 생성만 하면 기존 선택 유지, 명시적인 전환 요청이면 어디의 현재 선택을 갱신하고 다른 입구가 이를 따르는지

다음 논의의 첫 선택은 **Main의 일반 재개와 한정 역할 인수를 위 경로로 구체화하고, Project 읽기·갱신을 각각 독립 수단으로 유지할지**다. 권고는 유지다. 이어서 변경 반환·다음 재개를 실제 본문에 통합하고, Work 생성·전환의 의미 계약과 기존 create의 runtime 의존을 나눈 후보를 다룬다. 세 스킬 통합이나 신설을 먼저 정할 근거는 현재 없다.

이번 결과는 04-03의 첫 연결안·현행 대조다. 실행 본문 수정·설치·새 수행 시험·Ticket 완료는 후속이며, 사용자 선택 없이 제안을 합의로 기록하지 않는다.

기록 확인: 새 연결안과 수정한 진입·상태 문서 총7개의 로컬 링크548개가 실제 대상에 연결됐다. `git diff --check`와 새 기록의 공백 검사를 통과했다. 이 확인은 파일·경로 정합에 대한 것이며, 위 문서 대조나 후속 실제 수행의 결과를 대신하지 않는다. 커밋은 만들지 않았다.
