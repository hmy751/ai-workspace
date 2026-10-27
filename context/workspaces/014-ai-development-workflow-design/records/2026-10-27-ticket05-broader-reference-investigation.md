# 05 — 외부 접근 전반의 재조사와 학습 대상의 재검토

2026-10-27. **05에서 무엇을 살필지 자체를 다시 판단할 수 있도록 외부 자료의 전체 구성에서 관련 접근을 선별하고 본문·연결 자료를 대조했다.** 앞선 조사는 경험에서 개선 후보를 골라 반영하는 절차에 치우쳤다. 이번 조사는 기존 컨텍스트와 기준의 적절성, 실제 협업 방식, 대화에서 생긴 이해·목표의 변화, 환경의 수행 능력, 기록의 신뢰성과 개선 확인 방법까지 펼친다. 아래는 조사 결과와 Main의 적용 제안이며 고정 검토 항목·단계·역할·스킬을 채택한 설계가 아니다.

## 사용자 요청과 이전 조사와의 관계

사용자 원문:

> 그러니까 뭔가 많이 고려해야되는게 뭐 러프하게 말하자면 기존 컨텍스트들이 잘 구성되어 있나 부터 뭐 기준이나 내용 들 뭐 그리고 대화 에서 나오는 것들 도 있거든 그런것도 있어서
> 그리고 pstack에 더 좋은 관점들도 있던데? 내가 AI와 대화하면서 어떤식으로 일했는지 등도 루프 돌리는게 있고 아무튼 좀 더 자세히 조사해서 설명해봐

Main은 이에 “특히 pstack의 `automate-me`가 실제로 일해 온 방식에서 개인 작업 절차를 만드는 기능입니다. 이를 중심으로” 조사하겠다고 답했다. 사용자는 다시 정정했다.

> 그러니까 `automate-me` 만 찾으라는게 아니라 전반적으로 조사가 부족한것 같다 이게 포인트인건 알지?

사용자가 든 항목은 탐색의 단서이며 닫힌 요구 목록이 아니다. 별도 self-check에서도 기존의 경험 선택·후보 반영 구도를 외부 자료를 분류하는 고정 틀로 삼지 말고, 무엇을 문제로 보며 무엇을 관찰·변경·확인하는지를 먼저 조사하라는 기준을 회수했다. 감사자는 압축 이전의 전체 응답 원문을 볼 수 없어 최초 축소의 문장별 원인까지 확정하지 않았다.

[첫 조사](2026-10-27-ticket05-desktop-reference-study.md)의 retro·reflect·Vercel·자동 처리에 관한 사실은 계속 사용할 수 있다. 다만 그 묶음으로 외부 조사가 충분하다고 보거나 바로 운영 단계·담당을 정할 상태라는 안내는 이번 재조사로 대체한다. `automate-me`를 상세히 추가하는 것만으로 정정이 반영되지 않는다.

## 어떻게 범위를 살폈는가

| 자료군 | 탐색과 본문 확인 | 이번 질문에 중요한 이유 |
| --- | --- | --- |
| Desktop pstack | README의 전체 skill·23 playbook·24 principle 지도와 guide 목차에서 선별. reflect·automate-me뿐 아니라 how/why, 결정 기록, 문서 작성, 검증 지식 유지, 가설·평가, 개인 작업 방식·협업 안내를 읽었다. | 현재 이해·기록·기준·실제 수행·개선 확인이 어떻게 연결되는지 비교할 수 있다. |
| Desktop Matt skills | 실제 38개 skill의 설명과 분류별 카탈로그를 함께 확인. 기존 retro·domain-modeling·writing-for-agents 외에 wayfinder, teach, chief-of-staff, grilling, questionnaire, loop-me, research·prototype·글 구성·전환 관련 본문을 선별했다. | 실패 교정 이전의 목표·질문·이해, 사람과 AI의 책임, 기존 지식의 갱신을 볼 수 있다. |
| Vercel 제품 설계 글 | 보존한 486행 전체를 다시 읽고 판단 근거·문서 구성·수집/채택·평가·삭제와 비교했다. | 현재 결과를 닮는 것과 적절한 기준으로 판단하는 것의 차이, 기준의 이유·범위·예외를 다룬다. |
| Lauren의 Agent 신뢰 강연 | Desktop 전체 번역의 실제 검증·기능 지도·환경·기존 패턴 확산 부분을 읽었다. | AI에게 공급되는 지식뿐 아니라 직접 관찰·수행할 능력과 주변 산출물의 영향도 개선 대상이다. |
| plugins의 인접 도구와 agent-scripts | 카탈로그에서 workflow-from-chats, verify-this, agent-compatibility, skill-cleaner, docs-list를 선별해 본문을 읽었다. 마지막 두 항목은 실제 구현의 관찰 범위도 확인했다. | 대화의 작업 방식을 구조화하는 다른 접근, 실제 문서 사용과 검증 비용, 공급·사용·중복 관찰을 보완한다. |

다른 Desktop 개인 프로젝트로 범위를 넓히지 않았다. Git·PR 실무 자동화, 특정 테스트 도구 설치, 성과 요약, 화면 표시용 scaffold는 목적을 확인한 뒤 05의 중심 근거로 확장하지 않았다. 실행 반복 장치인 ralph-loop와 경험으로 방식을 재판단하는 루프도 구별했다. 이름만 발견하고 본문을 찾지 못한 agent-scripts의 `/different`·`/improve`는 구현된 회고 방법으로 인용하지 않는다.

판본은 pstack·인접 plugins가 `cursor/plugins@190d28736eff128ec94f502a22c7fe0c4b56cd37`, Matt가 `mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`, agent-scripts가 `16a71932d9e8de8285c79f3c1969ab74eff64db7`이다. 인터넷 최신판을 확인한 조사는 아니다. 기존 보존판과 일치하는 파일은 재사용하고, 새 핵심 자료 22개는 [추가 원문 묶음](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/README.md)에 보존했다. 모든 기능의 모든 참조·내부 코드를 전수 검증한 것은 아니다.

## 기존 컨텍스트와 기준 자체를 검토한다

pstack의 [technical-writing](../source/workflow-references/pstack/repository/skills/technical-writing/SKILL.md)은 문서의 독자가 하려는 일·알아야 하는 질문에 따라 내용과 구성을 판단한다. 실행 방법, 조회할 사실, 선택의 이유는 필요한 설명이 다르다. 주체·조건·용어·제약·이유가 드러나는지 볼 수 있으나, 명료한 문장만으로 사실의 정확성이나 기준의 적절성이 증명되지는 않는다.

[maintain-verification-skill](../source/workflow-references/pstack/repository/skills/maintain-verification-skill/SKILL.md)은 기능 지도와 코드를 대조하고 실제 기능도 실행한다. 낡은 문서, 기능을 다룰 수 없는 도구, 제품 결함을 구별한다. 제품이 잘못됐는데 문서를 그 결과에 맞춰 고치는 것을 금한다. [정형 검증 유지](../source/workflow-references/pstack/repository/skills/maintain-formal-verification-skill/SKILL.md)도 옛 검사가 계속 통과하더라도 이미 바뀐 시스템을 설명할 수 있다는 문제를 다룬다.

Matt의 [chief-of-staff](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/skills/skills/in-progress/chief-of-staff/SKILL.md)는 새로운 정보가 영향을 주는 기존 페이지를 함께 갱신하고, 판단 전에 관련 지식을 읽으며, 모순·고아·빠진 연결·새 근거에 밀린 주장을 점검한다. 원형은 날짜와 commit을 붙인 역사적 wiki이므로 현재 상태를 소유하는 우리의 current를 그대로 대체할 수는 없다.

[문서 신뢰성 검토](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/plugins/agent-compatibility/agents/docs-reliability-review.md)는 문서의 절차를 실제 따라가며 틀림·누락·오도와 그 영향을 확인한다. [작은 변경의 검증 검토](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/plugins/agent-compatibility/agents/validation-review.md)는 정상 경로를 찾는 추측, 실제 신호, 비용을 본다. 고정 점수와 가중치는 원형의 선택일 뿐 우리 합격 기준으로 삼지 않는다.

Main의 적용 제안: Personal·Project·Work의 구성과 본문을 **검토의 대상**으로도 본다. 필요한 내용이 있는지, 현재 사실·목표·기준과 맞는지, 다음 독자가 찾고 이해하고 판단에 쓸 수 있는지를 구별한다. 지침의 형식·링크, 의미의 충분성, 실제 사용 결과는 서로 다른 근거로 확인해야 한다. 모든 문서에 같은 목차나 매 대화 전수 감사를 강제할 이유는 없다.

## 사람과 AI가 일한 방식과 새로 생긴 이해를 본다

pstack의 [automate-me](../source/workflow-reference-supplements/2026-10-25-pstack-context/automate-me/SKILL.md)는 여러 대화에서 응답 형식 외에도 자율성, 조사와 질문, 위임, 검증 완료 기준, 코드·글 품질, 작업 절차를 찾는다. 기존 개인 스킬을 증분 갱신하고 대화에 나오지 않은 의도를 사용자에게 보충받는다. 평가는 주로 사용자에게 맞는지 확인하는 것이며 더 좋은 결과를 냈다는 효과 입증은 아니다.

추가로 찾은 [workflow-from-chats](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/plugins/cursor-team-kit/skills/workflow-from-chats/SKILL.md)는 대화별 요약 대신 **발동 조건·작업 단계·판단 규칙·품질 기준·중단 조건·근거·확신도**를 추출하고 작업 형태별로 묶는다. AI가 혼자 선택한 행동에 피드백이 없으면 약한 근거로 본다. 결과는 스킬·규칙·작업 문서 또는 산출물 없음이며, 채택 후보·고려·기각을 구별한다. 기본 조사 기간·확신도 분류는 운영 예시이고 장기 효과 재확인은 구체화돼 있지 않다.

Matt의 [학습 기록](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/skills/skills/productivity/teach/LEARNING-RECORD-FORMAT.md)은 설명한 주제와 실제 이해의 증거를 구별한다. 기존 지식을 밝힌 경우, 오해가 교정된 경우, 이해가 깊어져 목적이 달라진 경우가 이후 활동을 바꾼다. “Coverage is not learning. Wait for evidence.”라는 원문이 이 차이를 드러낸다. 다만 [사용 설명](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/skills/docs/productivity/teach.md)은 초기 수준과 종료 판단의 부족도 밝힌다.

Main의 적용 제안: 사용자가 어느 선택에 참여하려 했고 AI가 어디까지 조사·판단했는지, 무엇이 이해를 도왔고 무엇이 불필요한 보완 노동이었는지 살핀다. 예컨대 긴 배경을 매번 제공한 행동은 선호일 수도, 자료 접근의 부족을 보완한 행동일 수도 있다. 반복했다는 사실만으로 좋은 방식으로 고정하지 않는다. 대화에서 드러난 새 이해·기준은 근거가 있을 때 다음 설명·위임·의사결정의 조건을 바꿀 수 있다. 개발 대화를 수업으로 바꾸거나 사용자의 이해 수준을 추정해 저장하자는 뜻은 아니다.

## 현재 질문·기준·선택의 이유를 다시 검토한다

pstack의 [why 근거 판단](../source/workflow-references/pstack/repository/skills/why/references/epistemics.md)은 현재 코드의 형태만으로 과거 의도를 만들어내지 않는다. 직접 발화·간접 증거·추론·경쟁 가설·미확인을 구별하고 모순되는 근거를 함께 남긴다. 현재의 모양을 합리화하는 설명과 실제 선택 이유를 구별할 수 있다.

Matt의 [wayfinder](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/skills/skills/engineering/wayfinder/SKILL.md)는 열린 결정을 먼저 펼치고, 아직 질문으로 만들 수 없는 불확실성과 범위 밖을 구별한다. 한 결정이 다른 질문을 무효화하면 지도도 갱신한다. [운영 설명](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/skills/docs/engineering/wayfinder.md)은 과도한 사전 계획·질문 피로와 닫힌 결정 재검토 절차의 부족을 보고한다. 이 티켓 체계를 가져오는 대신, 지금 검토 중인 문제 정의와 질문의 빠짐도 다시 볼 수 있다는 관점을 취한다.

[Vercel 원문](<../source/lectures/vercel-product-design (1).md>)은 현재 출시 결과에도 결함이 있을 수 있으므로 규칙 준수와 출시 결과 유사도를 따로 평가한다. 결정에는 이유·범위·예외·근거·사례·가정·열린 선택을 연결하고, 검사로 다룰 수 없어진 규칙은 판단 지침으로 되돌리거나 유용성이 사라지면 제거한다.

Main의 적용 제안: 기존 기준을 지켰는지와 그 기준이 지금 목표에 적절한지를 모두 물을 수 있어야 한다. 새로운 사용자 정정이 기존 규칙의 표현을 보완하는 것인지, 목표·문제 정의·판단 기준을 바꾸는 것인지 구별한다. 기존 Owner는 채택된 변경의 책임을 찾는 데 쓰며 개선 대상을 탐색하는 범위를 닫는 근거로 쓰지 않는다.

## 다음 작업의 수행 능력과 주변 환경을 개선한다

[Lauren 강연의 원문 번역](../source/lectures/03_Agent_신뢰_강연_전체번역.md)은 AI가 직접 앱을 제어·관찰하는 도구와 제품의 기능·접근 방법을 설명하는 지식을 함께 발전시킨 사례다. 반복해서 새 스크립트를 만드는 비용, 사람만 할 수 있었던 확인, 기존 코드의 나쁜 패턴이 이후 작업에 복제되는 문제를 다룬다. 이 관점은 첫 조사에서 본 Matt retro·pstack correct의 구조 개선과 연결된다.

agent-scripts의 [skill-cleaner](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/agent-scripts/skills/skill-cleaner/SKILL.md)는 설치된 파일과 실제 모델에게 공급되는 목록을 구별하고 사용 흔적·중복·길이를 관찰한다. [구현](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/agent-scripts/skills/skill-cleaner/scripts/skill-cleaner.ts)의 사용 집계와 본문 유사도는 휴리스틱이다. 미사용 흔적은 불필요함을, 열람 흔적은 실제 적용을 증명하지 않는다. [docs-list](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/agent-scripts/scripts/docs-list.ts)는 읽을 조건을 보여 주지만 본문 타당성까지 보장하지 않는다.

Main의 적용 제안: 새 지식이나 문구뿐 아니라 어떤 자료·관찰·실행 능력을 갖추면 다음 작업이 나아질지 찾는다. 필요한 입력이 반복해서 빠지는지, 좋은 예제가 실제로 쓰이는지, 중복 지시와 낡은 예제가 방해하는지 확인한다. 명백한 문제 예방 외에 잘된 방법을 재사용 가능한 도구·사례·절차로 만드는 기회도 포함한다.

## 경험의 기록과 개선됐다는 주장도 검토한다

pstack의 [show-me-your-work](../source/workflow-references/pstack/repository/skills/show-me-your-work/SKILL.md)는 중요한 선택·이유·근거·결과를 남기고, 작업 종료에 그 기록을 해당 대화와 대조한다. 실제로 한 결정인지, 근거가 주장을 뒷받침하는지, 빠진 전환·철회가 있는지 본다. 기존 기록 재사용은 유효하지만 기록이 정확하다는 자동 보장은 아니다. TSV·매 종료 감사·다른 모델 고정은 별도 운영값이다.

[attack-the-premise](../source/workflow-references/pstack/repository/skills/principle-attack-the-premise/SKILL.md)는 같은 전제를 둔 개선이 실패하면 그 전제를 직접 확인할 관찰을 찾는다. [hillclimb](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/hillclimb.md)은 문제를 재현할 조건·측정 민감도·기준 상태를 먼저 확보하고 가설별로 유지·철회를 판단한다. [verify-this](../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/plugins/cursor-team-kit/skills/verify-this/SKILL.md)는 동일 조건의 전후 증거를 비교하고 유효한 비교가 없으면 미확인으로 남긴다.

Main의 적용 제안: 규칙을 읽음, 지침에 맞게 행동함, 제품 결과가 나아짐, 사람의 판단·이해·부담이 나아짐을 구별한다. 질문 수·문서 길이·한 번의 점수로 전체 협업 품질을 대신 평가하지 않는다. 효과가 없으면 문구만 계속 보강하기 전에 개선 가설과 확인 방법을 다시 본다. 좋은 조건을 유지하거나 불필요한 장치를 줄이는 것도 결과다.

## 기존 014의 사례에 대입하면 달라지는 검토

| 확인된 사례 | 조사 결과를 바탕으로 추가로 물을 것 |
| --- | --- |
| 문서별로 사례 또는 핵심 설명이 필요하다는 사용자 판단과 실제 문서 재편집 뒤의 긍정적 반응 | 어떤 독자의 질문과 내용 배치가 맞았는가. 현재 다른 문서도 자기 역할에 필요한 내용·조건·이유를 갖추는가. [원문과 실제 변경](../source/noline-evaluation/reviews/document-guidance-followup.md). |
| 이름 비교에서 설명이 필요 없는 코드를 지향한다는 기준이 명확해지고, Personal·Project 관리 방법도 다시 논의함 | 어떤 대안·질문이 기준의 의미를 드러냈는가. 기존 기준이 새로운 조건에서도 선택을 가르는가. [기준 형성](2026-10-19-101-self-explanatory-code-priority.md), [관리 판단](2026-10-19-102-personal-project-update-ownership.md). |
| access 질문은 먼저 이유와 적절성의 판단을 원했고, DB·인증 질문은 중요한 이해·선택의 과정이었음 | AI의 자율 판단, 사용자 참여, 설명과 선택의 준비가 적절했는가. 반복 질문을 모두 줄여야 할 교정으로 보지 않는다. [사용자 인터뷰](../source/noline-evaluation/reviews/interview-20261012.md). |
| 재설명 부담은 전체적으로 줄었으나 기록을 읽고도 중심을 다시 잡아준 장면이 남음 | 내용·발견 경로·실제 열람·판단 적용 중 무엇이 영향을 주었는가. 잘 복구한 조건도 볼 수 있는가. [재개 후속 비교](../source/noline-evaluation/reviews/record-timing-followup.md). |
| 04-02 보완의 일부 확인은 좋아졌지만 전체 추가 이득은 뚜렷하지 않았음 | 문구 추가 가설이 맞는지, 필요한 수행을 측정했는지, 국소 변화가 전체 사용 경험에 의미가 있는지. [마감과 후속](2026-10-26-ticket04-02-closeout-and-followups.md). |

이는 기존 사례의 새 조사 질문이며 실제 원인을 새로 입증한 결과는 아니다. [전체 Spec](../current/spec.md)은 이미 과거 실패만으로 개선 후보를 제한하지 않는다. 문제 보고가 없는 구성도 더 나은 외부 대안과 비교할 수 있다. 03·04의 설계 완료는 해당 결과를 영구 고정하는 뜻이 아니지만, 완료된 모든 항목을 자동으로 다시 열 필요도 없다.

## 현재 판단과 남은 구체화

05의 설계는 대화를 중요한 관찰 단위로 삼되, **대화·실제 산출물·현재 체계·형성 근거·외부 대안을 함께 보고 무엇을 배우고 유지하거나 바꿀지 판단하는 방법**을 구체화할 필요가 있다. 여기서 제시한 관점은 매회 수행할 전수 체크리스트가 아니다. 사건 하나의 교훈, 여러 대화에 걸친 방식, 기존 지식의 현실 대조, 효과 시험은 필요한 근거 범위와 비용이 서로 다르다.

현재 체계에는 이미 Personal·Project·Work의 본문과 형성 자료, 읽기·갱신 책임, 채택된 의미를 반영하는 context-update, 일부 실제 수행 비교가 있다. 이를 입력으로 재사용하면서 검토 대상 자체의 적절성과 새 개선 기회를 살핀다. 이미 확정된 사실의 일상 갱신은 이 루프를 기다리지 않는다.

다음 논의는 스킬 이름이나 역할 수를 먼저 정하기보다 서로 다른 실제 사례에서 무엇을 살피면 유용한지, 어떤 근거가 필요하고 무엇을 결과로 남길지를 비교하는 것이다. 그 뒤 대화의 경계·호출 시점·Main과 별도 판단자의 배치·사용자에게 남길 선택·반영과 효과 관찰을 구체화한다. 현재는 외부 접근과 기존 사례의 연결을 설명할 근거를 확장한 상태이며 운영안 채택·설치·실제 루프 수행은 하지 않았다.

## 확인 범위

문서·연결 원문과 일부 도구 구현의 정적 조사다. 원형의 실행 계약과 우리에게 가져올 제안을 구별했다. Matt의 in-progress 자료와 사용 설명의 자기평가는 검증된 일반 효과가 아니며 Vercel의 공개 eval도 copywriting 범위다. 실제 개인 채팅 수집, 외부 스킬 실행, 설치·자동화·제품 변경·운영 효과 시험은 없다. 신규 원자료는 원본과 바이트·해시를 대조하고 기존 snapshot은 유지했다.
