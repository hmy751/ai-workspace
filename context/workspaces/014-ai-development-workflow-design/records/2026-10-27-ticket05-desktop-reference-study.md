# 05 — Desktop 외부 원문 조사와 기존 체계에 가져올 후보

후속 상태: 사용자가 전반 조사의 부족을 지적해 [외부 접근 전반의 재조사](2026-10-27-ticket05-broader-reference-investigation.md)로 이어졌다. 아래는 첫 조사로 보존한다. 개별 자료의 사실은 재사용하되, 이 범위로 조사가 충분하다는 판단과 곧바로 운영 절차를 구체화한다는 안내는 후속 기록으로 대체한다.

2026-10-27. **Matt의 환경 개선 관점, pstack의 경험 해석·후보 선별, Vercel의 반영 대상 선택·효과 확인을 함께 비교할 근거를 마련했다.** 세 자료는 서로 다른 범위를 맡으며 우리05의 전체 운영안을 대신하지 않는다. 아래 가져올 방향은 Main의 조사 권고이고 단계·담당·호출·스킬의 채택안은 아니다.

## 요청과 조사 범위

사용자 원문:

> 좋아 그럼 외부 레퍼런스 자료를 Desktop에서 찾아서 봐봐 그래서 우리가 한 기존 시스템이랑 논의들 등등을 보고 어떻게 가져올지 좀 보게 일단 여기에 필요한 외부 레퍼를 잘 봐봐

Desktop의 외부 원본과05에 직접 필요한 연결 자료를 읽었다. Matt와 pstack은 각 담당에게 원문 조사를 나눴고, 별도 담당은 자동 학습 plugin의 실제 코드·지시 책임을 확인했다. Main은 Vercel 원문, reflect의 본체·네 역할 지침, 우리05·04-03 실행 본문과 관련 논의를 대조해 종합했다. 새 설계안의 독립 개선 리뷰나 이들 스킬의 실제 수행은 아니다.

| 원본 | 이번에 확인한 판본과 원자료 관계 |
| --- | --- |
| `/Users/hammyeong-yeon/Desktop/skills` | Matt skills 1.3.1, `5beb35b040e3de97e54fa9e386d7e42d15c295c2`, clean. 핵심·직접 연결 원문10개가 기존 [보존판](../source/workflow-references/matt-pocock/README.md)과 바이트·SHA-256 일치. |
| `/Users/hammyeong-yeon/Desktop/plugins/pstack` | pstack 0.15.29, `190d28736eff128ec94f502a22c7fe0c4b56cd37`, clean. reflect·네 역할·구조 원칙·recall·automate-me·검증 유지9개가 기존 source 또는10/25 보충판과 일치. |
| `Desktop/강연_관련_스킬_번역본/vercel-product-design (1).md` | John Phamous의2026-06-25 글. 기존 [원문](<../source/lectures/vercel-product-design (1).md>)과 바이트·SHA-256 일치. 내부 전체 구현·운영 기록이 아닌 설명 글과 축약 지침이다. |
| `Desktop/plugins/continual-learning` | 같은 plugins commit의 plugin 1.0.0. 기존 보존 범위 밖이어서 [별도 원문 묶음](../source/workflow-reference-supplements/2026-10-27-continual-learning/README.md)에7개 파일을 보존했다. |

Desktop의 `agent-scripts`와 관련 외부 저장소에서 이름을 탐색했으나 무관한 개인 프로젝트로 조사하지 않았다. `teaching/skills/run-learning-retrospective`는 학습자의 개념 이해·진도·연습 계획을 조정하는 짧은 절차라 이번 agent 작업 방식 개선의 주 근거에서는 제외했다. 로컬 원본을 새로 열어 확인한 결과이지 인터넷 최신판 조사나 설치 확인은 아니다.

## Matt: 대화에서 드러난 작업 환경의 개선 기회를 찾는다

현재 [retro 본체](../source/workflow-references/matt-pocock/repository/skills/engineering/retro/SKILL.md) 7~25행과 [사용 설명](../source/workflow-references/matt-pocock/repository/docs/engineering/retro.md)을 함께 읽어야 한다. 사용자 호출을 받아 지정 세션의 원자료를 읽고, 지정이 없으면 현재 세션을 대상으로 삼는다. 탐색 경로·자동 검사·코딩 기준·큰 진입 지침·도구 비용·효과 없는 지시·정보 접근에서 개선 후보를 찾아 심각도 순으로 제시한다.

본문의 “Default to building the check over writing the rule.”는 기계가 판별할 실패라면 반복 지시보다 검사를 먼저 보라는 방향이다. 기존 저장소에 있는 검사·CI가 빠져 있거나 고장 났는지도 먼저 확인한다. 도구나 지침을 새로 만드는 것뿐 아니라 기존 연결 복구·정리·삭제도 후보가 된다.

사용 설명의 “Discard any candidate you can't trace to a specific moment.”는 추상적인 모범 답안을 후보로 만들지 않도록 한다. 한 세션에서 눈에 띈 문제의 심각도를 과대평가할 수 있고, 지난달 추가한 lint·hook·CI의 과잉 동작을 장기 감사하는 방법은 이 스킬이 해결하지 못한다고 설명한다. 끝나는 결과는 사용자가 고를 후보이며 실제 편집·후속 효과 확인까지 닫힌 절차가 아니다.

우리에게 유용한 것은 **어떤 환경이 다음 수행을 달라지게 할지** 보는 질문이다. 재개에서 자료를 찾지 못했는지, 이미 읽은 자료의 중심을 잘못 판단했는지에 따라 개선 대상이 달라진다. 후보가 특정 장면·실제 비용과 연결돼야 한다는 점도05에 맞는다.

다만 Matt는 코딩 기준을 reviewer 중심으로 두고 어려운 세션을 주 대상으로 설명한다. 우리는 관련 Personal 기준을 구현자와 검토자가 함께 사용하고, 잘된 경험과 유지할 선택도05에서 다룬다. 기준을 reviewer에게만 보내거나 성공 사례를 제외하는 배치는 가져오지 않는다. [domain-modeling](../source/workflow-references/matt-pocock/repository/skills/engineering/domain-modeling/SKILL.md) 60~74행은 확정 용어를 즉시 기록하므로, Matt에서도 일상적인 의미 반영을 retro까지 미루는 것은 아니다.

## pstack: 경험의 해석을 나누고 실제 행동을 바꿀 후보만 남긴다

[reflect](../source/workflow-references/pstack/repository/skills/reflect/SKILL.md)는 현재 대화의 원문을 식별한 뒤 세 관점으로 후보를 찾고 별도 종합자가 정리한다. 원문이 없으면 요약을 쓸 수 있지만, 이는 정확한 발화·시점·누락을 판정할 때 근거 상한을 낮춘다. 다른 workspace 대화를 임의로 찾는 것은 명시적으로 제한한다.

| 실제 역할 원문 | 질문의 차이와 우리에게 유용한 점 |
| --- | --- |
| [Judgment](../source/workflow-references/pstack/repository/skills/reflect/references/judgment-reviewer.md) | 실수·교정·선호·결정 이유에서 다음 판단에 남길 내용을 찾는다. 사건 요약을 지속할 판단으로 옮기는 역할이다. |
| [Tooling](../source/workflow-references/pstack/repository/skills/reflect/references/tooling-reviewer.md) | 도구·명령·실행 진입의 재탐색 비용과 AI가 직접 가져올 수 있었던 자료를 사용자가 대신 제공한 장면을 찾는다. 우리에게는 실제 접근 권한·요청 의도를 확인한 뒤 자료 연결의 개선 기회로 사용한다. 사용자의 모든 자료 제공을 실패로 세지는 않는다. |
| [Divergent](../source/workflow-references/pstack/repository/skills/reflect/references/divergent-reviewer.md) | 놓친 후속 영향, 우연히 통과한 성공, 실행하지 않은 대안·검증을 살핀다. 같은 사건의 겉보기 교훈을 다시 판단하게 한다. 억지 반대 의견을 만드는 것이 목적이 되어서는 안 된다. |
| [Synthesizer](../source/workflow-references/pstack/repository/skills/reflect/references/synthesizer.md) | 지속성·구체성·미래 행동 차이·기존 수신 스킬·기계적 해결 가능성을 대조한다. 대상 본문을 읽어 중복인지 실제 빈틈인지 판정하고 Accepted/Rejected/Backlog로 나눈다. |

특히 종합자의 “a future agent does something different”와 “because the issue is execution, not the skill”가 중요하다. 명확하고 적절한 위치에 이미 있는 지시라면 다시 덧붙이지 않는다. 지시가 묻혔거나 약하다면 중복 조항 추가 대신 표현·배치를 바꾼다. 스킬을 부르지 못한 문제는 본문 내용과 따로 다룬다.04-02에서 이미 요구한 기준의 미수행과 문구 개선의 한계를 본 경험에 직접 연결된다.

Main의 적용 판단: 이 기각은 해당 스킬 문구를 더하지 않는다는 판단이지 실제 마찰이 해결됐다는 뜻이 아니다. 우리05에서는 남은 문제를 수행 시점·맥락 적용·검사·역할 배치 등 적합한 책임으로 이어갈 수 있어야 한다. 또한 [전체 Spec](../current/spec.md)의 후보 범위는 이미 겪은 실패에만 한정되지 않는다. 기존 장면의 교훈을 주장할 때의 증거 조건과 외부 자료에서 얻은 새 개선안을 비교하는 일을 구별한다.

[구조에 교훈을 반영하는 원칙](../source/workflow-references/pstack/repository/skills/principle-encode-lessons-in-structure/SKILL.md)과 reflect의4번은 검사·스크립트·메타데이터·실행 장치가 더 잘 처리할 후보를 별도로 보낸다. 단순히 스킬 문구로 다시 쓰는 것을 개선의 끝으로 삼지 않는다는 점을 가져올 수 있다. 우리에서는 장치의 실제 정확도·오탐·유지비와 필요한 판단을 함께 비교해야 한다.

원형은 조직 전체 스킬 변경을 대상으로 사용자 승인을 받은 뒤 작은 편집은 parent가 직접, 큰 수정·새 스킬·발동 조정은 Cursor 내장 작성 절차로 연결한다. Backlog는 외부 tracker에 곧바로 등록한다. 이 흐름의 `Accepted`도 실제 사용자 채택·반영 완료와 같은 상태가 아니다.

우리에게 그대로 맞지 않는 값도 있다. 스킬 중심 수신 대상, 단발 사건의 일괄 제외, 항상 세 검토자와 종합자, 모든 편집 항목의 별도 승인, 약10행 기준, 외부 backlog 자동 등록이다. 여러 검토자가 동의해도 독립된 성공 사례가 늘어난 것은 아니다. 의미 있는 관점 분리와 원문 대조는 참고하되, 호출 수·승인·보존 위치는 기존 권한과 비용에 맞춰 정해야 한다.

참고 범위도 구별한다. [recall](../source/workflow-reference-supplements/2026-10-25-pstack-context/recall/SKILL.md)의 기존 요약 재사용·현재 사실 확인은 입력 비용에 참고할 수 있다. [automate-me](../source/workflow-reference-supplements/2026-10-25-pstack-context/automate-me/SKILL.md)는 개인 방식의 포착을 사용자 적합성 확인으로 마치며, [maintain-verification-skill](../source/workflow-references/pstack/repository/skills/maintain-verification-skill/SKILL.md)은 자기 문서·도구를 실제 기능과 대조하는 한정 유지다. 모두 같은 효과 시험을 요구하는 자료는 아니다. Cursor 내장 create-skill의 본문은 이 저장소에 없어 내부 시험 방법·효과까지 확인하지 않았다.

## Vercel: 근거의 검토와 반영할 위치·수단·효과를 잇는다

[제품 설계 원문](<../source/lectures/vercel-product-design (1).md>) 335~351행은 주간 근거 수집, 수집자와 판단자, 후보·기각·추가 확인·근거 공백을 포함한 검토 묶음을 설명한다. 수집자는 규칙을 제안하지 않고, 판단자는 출처와 범위를 대조한다. 숙련자의 의견도 근거 없이 규칙이 되지 않으며 후보는 사람이 선택하기 전까지 미채택이다.

핵심은 결과를 지침·참고자료·사례·lint·평가·미확인 항목·변경 없음 중에서 고른다는 점이다. 채택하면 가장 좁은 관련 정본에 반영한다.325~333·437~479행은 기대 수정을 숨긴 다른 사례와 스킬 없는 실행의 비교, 지침 적합성과 이미 출시된 코드와의 유사성 구별, 호출 실패와 읽은 뒤 적용 실패의 분리, 도움이 사라진 규칙의 제거를 설명한다.

우리의 Personal·Project·Work와 코드·검사·스킬의 책임 구분에 맞춰 **무엇을 학습했는지와 어디를 바꾸는지를 따로 판단하는 방법**, 후속에 관찰할 행동·결과를 함께 정하는 방법을 가져올 수 있다. 이미04-03에서 구현한 한정 반영 방법을 다시 만들 필요는 없다.

주간 주기·Slack/Figma/GitHub 수집·두 역할 고정·모든 변경의 새 승인 절차는 이 조직의 운영값이다. 공개 평가 범위도 copywriting과 인터페이스 언어이며 전체 개발 workflow가 아니다. 실제 수집 코드·누락 탐지·검토 묶음·승인 이력·효과 수치는 확보한 글에 없다. 설명된 절차를 우리 환경에서 검증된 운영 결과로 쓰지 않는다.

## 자동 처리의 보조 대조: Continual Learning

[보존한 원문·코드](../source/workflow-reference-supplements/2026-10-27-continual-learning/README.md)를 보면 종료 hook은 응답 횟수·시간 간격·대화 파일 수정 시각·같은 generation의 중복을 제한한다. 스킬은 단일 갱신 담당에게 맡기고, 그 담당이 바뀐 대화를 읽어 반복 선호·지속 사실을 기존 항목에 통합한다. 의미 있는 변경이 없으면 본문을 그대로 두도록 한다.

증분 입력과 의미 중복 정리는 비용을 줄일 아이디어다. 그러나 어떤 경험이 지속할지, 의미상 중복인지, 실제 갱신과 처리 index가 맞는지는 LLM의 판단 지시이고 hook이 보장하지 않는다. hook은 갱신 성공을 확인하기 전에 실행 상태를 기록한다. 호출됐다는 사실을 반영 완료로 해석할 수 없다.

단일 담당이 발견·채택·직접 편집을 수행하며 결과는 선호와 workspace 사실 두 절이다. 근거·선택 이유·미채택·후속 효과를 관리하는05와 범위가 다르다. README의 시험 모드 활성 설명과 실제 설정·코드 기본값도 달라, 안내만으로 활성 상태를 판정할 수 없었다. 자동 종료 호출·메모리 갱신을 도입하는 근거로 삼지 않으며 필요한 시점에 자동화의 책임을 비교할 보조 자료로 둔다. 실제 대화·사용자 메모리는 열람하거나 변경하지 않았다.

## 기존 시스템과 연결해 가져올 방향

현재 기준은 [05](../current/tickets/05-learning-loop.md), [대화 기준 루프의 직접 발화](2026-10-26-context-03-goal-improvement-review.md#사용자-후속--project-내용-선별과-대화-기준-루프), [담당자 제안의 재사용](2026-10-26-context-proposal-review-apply-design.md), [실행된 context-update](prototypes/development-workflow/skills/context-update/SKILL.md), [04-02 마감](2026-10-26-ticket04-02-closeout-and-followups.md)이다. 아래는 이 계약에 비춘 Main의 권고다.

| 가져올 판단 | 기존 관계와 실제 의미 |
| --- | --- |
| 경험의 근거와 해석을 구별한다 | 기존 제안·원문·실제 결과를 재사용하되, 원인과 개선안은 별도 판단한다. 전체 대화 재수집이나 원 구현자 재호출을 기본으로 만들지 않는다. |
| 다음 행동을 달라지게 할 지점을 찾는다 | 실행 누락·기준 부족·찾기 어려운 배치·도구 접근·구조의 문제를 구별한다.04-02의 추가 문구 이득 미확인을 곧 스킬 전체 실패나 기준 추가 사유로 바꾸지 않는다. |
| 유지·변경·보류를 모두 실제 결과로 다룬다 | 성공한 조건과 현재 방식을 유지할 이유도 남길 수 있다. 스킬 편집을 매 회고의 필수 산출물로 만들지 않으며, 보류에는 다시 볼 조건을 연결한다. |
| 반영할 대상과 권한을 기존 체계에서 찾는다 | Personal은 여러 작업의 개인 판단, Project는 제품 공통 의미·계약·제약, Work는 이번 선택·진행·근거를 맡는다. 채택 결과가 코드·검사·도구이면 그 수행으로, 지정된 지속 본문이면 context-update로 잇는다. |
| 실제 반영과 이후 효과를 구별한다 | 형식·링크 확인, 지침의 실제 사용, 개발 결과, 사용자 부담을 같은 성공으로 묶지 않는다. 다음 유사 상황에서 관찰할 차이와 수정·철회 조건을07과 연결한다. |

예를 들어 기록을 읽었는데 우선순위를 잘못 잡은 재개는 기록 시점·양만 늘릴 근거가 아니다. 실제로 읽은 내용과 현재 선택을 적용한 판단을 봐야 한다. 보고서 재작성과 중요한 DB·인증 질문도 같은 교정 실패로 묶지 않는다. 반면 좋은 문서 개선 사례는 어떤 기준·자료·수행 조건이 도움이 됐는지 살펴 유지할 후보가 될 수 있다. 이들은 [기존 평가](2026-10-12-01-background-and-evaluation.md)의 확인 범위에서 사용할 설계 입력이며 새로운 실행 결과가 아니다.

다음 구체화에서는 대화와 사건의 경계, 검토할 시점, Main과 별도 판단자의 배치, 이미 처리한 후보의 재사용, 사람에게 남길 선택, 효과 관찰의 수신을 실제 사례에서 비교한다. 이 조사로 정해진 것은 참고할 내용과 조정할 지점이며, 단계 수·역할 수·스킬 형태·자동 발동은 아직 정하지 않았다.

## 확인과 보존

- Desktop 두 Git checkout은 위 commit과 clean 상태를 직접 확인했다. 기존 원문10개·9개의 일치는 각 조사 담당이 바이트·해시로 대조했다. Main은 Vercel과 retro 번역본의 기존 사본 일치를 직접 확인했다.
- 기존 snapshot·manifest는 변경하지 않았다. 새 Continual Learning 원문7개는 Main이 복사 후 바이트·해시를 대조했고 출처 manifest를 남겼다.
- 문서 계약·코드 정적 대조의 결과다. 실제 회고 스킬·hook·개선 루프를 실행하지 않았고 반복 효과·새 운영안의 품질을 입증한 것은 아니다.
- 이번 산출물은 이 조사 기록과 원자료 접근점이다. 기존 실행 prototype·전역 지침·설치·제품 코드는 변경하지 않는다.
