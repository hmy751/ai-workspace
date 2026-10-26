# 04-03 — Matt 보존판의 스킬·맥락·관리 책임 조사

2026-10-25. **Matt의 보존판은 전체 작업을 안내하는 진입, 재사용 실행·참조 스킬, 프로젝트별 문서와 소비 지침을 함께 쓰는 혼합 구성이다.** 업무 흐름 안의 호출과 사용자의 직접 요청이 같은 스킬을 사용하는 실제 계약은 있다. 그러나 모든 읽기·현재 상태 유지·공통 반영을 하나의 context 스킬에 모은 구조는 아니다. 단순한 문서 소비와 내용을 다듬는 수행을 명시적으로 나누는 반대 사례도 있다.

이 기록은 [조사 범위](2026-10-25-context-reference-investigation-scope.md)의 Matt 담당 결과다. [현재 책임 구상](2026-10-25-context-responsibility-concrete-proposal.md)을 입증하려고 자료를 고르지 않았다. 하나의 맥락 스킬, 선택·반영의 분리, workflow와 공유 상세의 조합은 계속 비교 대상이다. 조사한 지시를 실행하거나 스킬을 설치·수정하지 않았다.

## 판본과 증거의 지위

- [보존 안내](../source/workflow-references/matt-pocock/README.md): `mattpocock/skills` 버전 **1.3.1**, Git `5beb35b040e3de97e54fa9e386d7e42d15c295c2`, 2026-10-21 로컬 클론에서 선택한 81개 파일이다. 최신 공개판과 비교하지 않았다.
- 후속으로 Main이 같은 commit의 공식 저장소에서 확보한 [관리 방침 두 문서](../source/workflow-reference-supplements/2026-10-25-matt-maintenance/README.md)를 직접 읽었다. 원 URL·commit·확보 시각·크기·hash는 해당 [manifest](../source/workflow-reference-supplements/2026-10-25-matt-maintenance/manifest.json)에 보존됐으며, 기존 81개 사본과 구별한다.
- `repository/skills/**/SKILL.md`와 같은 폴더의 참조 파일은 당시 실행 지침이다. `.agents/invocation.md`는 작성·호출 규약, setup의 `domain.md`는 대상 Project에 쓸 소비 지침의 원형이다. 이 파일들이 실제 제품에 설치·소비됐다는 증거와는 다르다.
- `repository/docs/`는 저자의 사용자용 설명이다. 실제 SKILL보다 의도·알려진 문제·사용 보고를 자세히 설명하지만, 인용한 사용자 사건의 원본 로그나 재현 결과는 이번 묶음에 없다. 저자가 전한 관찰과 직접 검증을 구별한다.
- 본문·참조·선택된 `agents/openai.yaml`을 읽어 계약과 선언된 연결을 대조했다. host 호출·본문 적용·새 역할 수행·수정 효과는 시험하지 않았다. 아래의 대표 경로는 **원문으로 추적한 수행 계약**이다.

## 확인한 구성과 책임

### 전체 진입은 실행 조정자와 같지 않다

[ask-matt](../source/workflow-references/matt-pocock/repository/skills/engineering/ask-matt/SKILL.md) L3–4·11–13은 직접 요청하는 router이며, 무엇을 권할지 판단하기 전에 해당 SKILL 본문을 읽도록 한다. L19–38은 설계·구현·review·retro의 흐름을 안내하지만 이 안내 자체가 다음 스킬들을 자동 실행하는 계약은 아니다.

[호출 규약](../source/workflow-references/matt-pocock/repository/.agents/invocation.md) L5–10·16–22는 다음을 나눈다.

| 형태 | 선언된 소비·호출 관계 | 직접 근거와 최소 발췌 |
| --- | --- | --- |
| 사용자 직접 호출 | 사용자가 이름을 입력한다. 다른 스킬이 자동으로 실행하지 않는다. Claude frontmatter와 Codex policy를 함께 맞춘다. | invocation L5·8·10: “only by the human typing its name” |
| 모델 또는 사용자 호출 | 모델의 자율 발견, 다른 스킬의 수행 중 호출, 사용자의 직접 요청을 모두 지원한다. | [SKILL-MECHANICS](../source/workflow-references/matt-pocock/repository/skills/productivity/writing-for-agents/SKILL-MECHANICS.md) L9: “model-invocation always _includes_ user reach” |
| router | 사람이 다음 스킬을 고르기 쉽게 알려 준다. 사용자 전용 스킬의 실행을 대신하지 않는다. | SKILL-MECHANICS L20–22: “It can only hint, never fire them” |
| 실제 실행 의존 | 실행 중 다른 스킬이 필요하면 명시적인 Skill 도구 호출로 연결한다. 단순한 이름 나열과 구별한다. | invocation L16·18·20–22: “operative” instructions와 router prose를 구별 |

`ask-matt`, `implement`, `retro`의 frontmatter와 Codex YAML은 사용자 직접 호출로 대응하고, `code-review`와 `domain-modeling`은 그 제한이 없는 선언을 확인했다. 실제 host가 이 차이를 어떻게 집행하는지는 이번 조사에서 확인하지 않았다. 특히 이 저장소가 전제하는 `Skill` 도구 호출 문장을 다른 host의 보편 인터페이스로 간주하지 않는다.

**우리 비교에 주는 의미:** workflow 안에서의 사용과 직접 요청은 독립된 두 구현을 요구하지 않는다. 동시에 사용자가 직접 고르는 router와 Main의 실행 조정을 같은 책임으로 묶을 근거도 없다. 기존 `development`의 Main 책임을 ask-matt의 안내 구조로 대체할 수는 없다.

### 스킬 본체·공유 참조·세부 자료를 함께 사용한다

[writing-for-agents](../source/workflow-references/matt-pocock/repository/skills/productivity/writing-for-agents/SKILL.md) L6–8은 skill·root 지침·연결된 문서에 공통 작성 기준을 적용하고, skill을 작성할 때만 `SKILL-MECHANICS.md`를 추가로 읽게 한다. L31–43은 본문 안 단계·본문 안 참조·조건부 외부 참조를 구별한다. 핵심은 어떤 판단 분기에서 실제 필요한가이지 파일 수를 줄이거나 늘리는 일이 아니다.

| 주장 | 직접 근거·발췌 | 이번 해석의 범위 |
| --- | --- | --- |
| 연결문에는 대상의 정체와 읽을 조건이 함께 있어야 한다. | writing-for-agents L12–17: “One trigger per branch.” | 현재 context 진입·workflow의 연결문을 검토할 후보 기준이다. 문구만으로 발견률을 보장한다는 뜻은 아니다. |
| 모두 필요한 내용과 일부 분기만 필요한 상세를 나눈다. | 같은 파일 L31–43: “inline what every branch needs” | 여러 영역을 다루는 공통 절차도 조건부 상세를 둘 수 있다. 이 원칙만으로 하나의 스킬이 최선이라고 결정하지 않는다. |
| 같은 의미는 한 정본이 소유하고 실제 환경에서 값싼 조회로 얻는 사실은 재서술을 줄인다. | 같은 파일 L78–81: “single source of truth”, “cache” | 우리 Work의 적용 판단을 없애라는 근거는 아니다. 원래 의미·그때의 적용 이유·현재 사실의 역할을 먼저 구별해야 한다. |
| 순서 분리와 호출 분리는 서로 다른 문제다. | 같은 파일 L49·54–59, SKILL-MECHANICS L16–18 | 내용이 여러 파일이라는 사실과 수행 중 문맥이 실제로 분리되는 사실을 구별한다. 인라인 스킬 호출은 앞선 context를 지우지 않는다. |
| 공유 참조를 반드시 독립 스킬로 만들지는 않는다. | SKILL-MECHANICS L14: “plain file outside the skill system” | 사용자 전용 스킬끼리 직접 호출할 수 없다는 저자의 호출 모델에서 공유 파일도 별도로 인정한다. |

[tdd](../source/workflow-references/matt-pocock/repository/skills/engineering/tdd/SKILL.md) L26은 인터페이스 형태가 쟁점일 때 `codebase-design`을 불러 공통 용어를 읽되 별도 세션 수행으로 취급하지 않는다. 같은 실행 주체가 참조 스킬을 적용할 수 있다는 직접 사례다. 코드 모듈 설계 원칙 자체를 스킬의 독립성·운영 성공 증거로 사용하지 않았다.

### 제품 내용은 대상 Project가 보존하고, 읽기와 능동적 내용 변경을 구별한다

[setup](../source/workflow-references/matt-pocock/repository/skills/engineering/setup-matt-pocock-skills/SKILL.md) L9–15는 tracker·domain 문서의 위치와 소비 규칙을 Project에 구성하는 prompt 기반 작업이다. L21–30에서 기존 상태를 탐색하고, L63–82에서 초안을 보여 준 뒤 기존 root 파일을 수정하며 주변 사용자 변경을 보존한다. L84–118은 root에 짧은 안내를 남기고 `docs/agents/`에 대상별 지침을 둔다. 사용자는 나중에 해당 파일을 직접 수정할 수 있으며 일상 수정마다 setup을 재실행할 필요는 없다고 설명한다.

`domain.md`의 내용은 실행 스킬에 제품 용어 자체를 넣는 대신, 대상 Project의 용어집·결정 문서를 읽게 하는 지침이다.

| 책임 | 실제 입력·수행·출력 | 직접 근거·최소 발췌 |
| --- | --- | --- |
| 일상 소비 | 코드 탐색 전에 관련 glossary와 ADR을 읽고, 산출물의 도메인 명칭에 사용한다. 여러 context이면 관련된 것만 고른다. | [domain 원형](../source/workflow-references/matt-pocock/repository/skills/engineering/setup-matt-pocock-skills/domain.md) L5–11·41–45: “Read each one relevant to the topic.” |
| 자료 부재 | 파일이 없으면 그대로 진행한다. 앞단에서 빈 용어집·결정 문서를 만들라고 요구하지 않는다. | 같은 파일 L11: “proceed silently” |
| 충돌 인식 | 기존 ADR과 반대되는 제안은 충돌임을 밝혀 다시 볼 이유를 설명한다. 조용히 덮어쓰지 않는다. | 같은 파일 L47–51: “surface it explicitly” |
| 내용 구체화·기록 | 모호한 말과 관계를 질문·구체 사례·코드로 대조하고, 용어가 정해지면 즉시 glossary를 갱신한다. | [domain-modeling](../source/workflow-references/matt-pocock/repository/skills/engineering/domain-modeling/SKILL.md) L42–62: “update `GLOSSARY.md` right there” |
| 내용 제한 | glossary는 용어 정의이며 구현 결정·작업 메모·Spec을 섞지 않는다. | 같은 파일 L64: “It is a glossary and nothing else.” |
| 결정 보존 | 되돌리기 어렵고, 맥락 없이 의외이며, 실제 대안을 비교한 결정일 때 ADR 작성을 제안한다. | 같은 파일 L66–74: “Only offer to create an ADR” |

[호출 규약](../source/workflow-references/matt-pocock/repository/.agents/invocation.md) L24–26과 domain-modeling L8은 **기존 glossary를 읽는 것에는 domain-modeling이 필요하지 않다**고 직접 명시한다. 내용의 능동적 구체화와 일상 소비를 갈라 놓은 사례다. 따라서 원문은 모든 읽기·갱신을 반드시 같은 스킬로 묶자는 결론의 반대 근거이기도 하다. 반대로 좁은 제품 용어 작업의 구분이므로 우리의 Personal·Project·Work 전체를 똑같이 나누라는 근거도 아니다.

내용 권위도 주의해야 한다. domain-modeling은 충돌하는 용어·사용자 설명·코드를 질문으로 드러내고, 연결되는 [grilling](../source/workflow-references/matt-pocock/repository/skills/productivity/grilling/SKILL.md) L28–30은 사실 조사는 agent, 결정은 사용자에게 둔다. 다만 모든 glossary 편집에 새 승인을 받으라는 문장은 없다. 용어가 해결됐을 때의 즉시 반영과 새 결정을 묻는 일을 구별한다. 우리의 기존 위임·Main 판단 범위는 이 인터뷰 전용 결정 배치로 대체하지 않는다.

### 작업별 인수·보고와 지속 Work 운영은 다르다

[implement-spec](../source/workflow-references/matt-pocock/repository/skills/engineering/implement-spec/SKILL.md) L15는 Spec·Ticket·조사 기록·commit을 가리키는 접근점으로 소통하고 이미 있는 정보를 복제하지 않게 한다. L23의 선택적 탐색자는 후속 구현자가 읽을 노트를 저장하며, L27–38의 구현·병합·최종 review와 수정은 상위 실행 흐름이 조정한다. 실행자가 자료를 찾을 수 있는 연결과 역할 인수가 실제로 있다.

[code-review](../source/workflow-references/matt-pocock/repository/skills/engineering/code-review/SKILL.md) L25–41·58–80은 기준점·diff·실제 요구 출처·저장소 기준을 선택해 두 검토자에게 나눠 제공한다. 저장소의 기준 목록은 경로로, 자체 smell 기준은 본문으로, Spec은 경로나 가져온 내용으로 전달한다. 모든 입력을 요약 하나로 통일하지 않는다. 검토 결과는 두 축을 병합·재정렬하지 않고 나란히 반환한다. 이는 우리의 Main이 개선 의견·검증 근거를 종합하고 적용을 판단하는 책임과 다르다.

[handoff](../source/workflow-references/matt-pocock/repository/skills/productivity/handoff/SKILL.md) L8–16은 다음 세션의 목적에 맞춘 이동용 Markdown을 OS 임시 폴더에 쓰고 기존 Spec·계획·ADR·issue·diff를 중복하지 않고 연결한다. “not the current workspace”가 명시돼 있다. [PHASE-BOUNDARIES](../source/workflow-references/matt-pocock/repository/skills/engineering/ask-matt/PHASE-BOUNDARIES.md) L21–40은 같은 세션 유지, clear, 이동용 handoff, subagent, compact를 서로 다른 이유로 고른다.

이들은 원문과 요약의 손실, 이동용 전달물, 기존 산출물 재사용을 판단할 자료다. 그러나 **우리의 지속 Work current·records·output 관리나 새 독립 Workspace 생성·activation을 제공하는 계약은 아니다.** 같은 이름의 handoff·context를 근거로 기존 Work 유지 책임을 없애거나 임시 파일을 지속 정본으로 삼으면 목적이 바뀐다.

### 일하는 동안의 갱신과 경험 개선은 다른 경로다

domain-modeling의 용어 갱신은 대화 중 내용이 해결될 때 일어난다. 이에 비해 [retro](../source/workflow-references/matt-pocock/repository/skills/engineering/retro/SKILL.md) L3–13·15–25는 사용자가 요청한 실제 세션을 읽고 agent 환경의 개선 후보를 제시하는 스킬이다. L17–23에서 탐색 경로, 자동 검사, 검토 기준, root 지침, 도구 비용, 정보 접근을 나눠 보며 문장 추가만을 결과로 삼지 않는다.

| 판단 | 직접 근거·최소 발췌 | 범위와 주의점 |
| --- | --- | --- |
| 경험 원문을 먼저 읽는다. | retro L13: “Read the primary sources” | 이번 세션 또는 지정한 세션이 입력이다. 모든 과거 작업을 자동 수집하는 계약은 아니다. |
| 기계적 오류는 검사, 해석이 필요한 판단은 prose 기준을 후보로 둔다. | retro L18–19: “Classify the violation first” | 기존 검사 명령·CI를 먼저 보고 미연결·고장을 새 검사 부재와 구별한다. |
| 결과는 후보 제시에서 끝난다. | retro L25, [사용 가이드](../source/workflow-references/matt-pocock/repository/docs/engineering/retro.md) L5·35: “It also only proposes.” | 채택 전 변경이나 자동 hook 설치를 수행하는 계약이 아니다. 이후 구현·반영의 세부 책임은 이 스킬 본문에 없다. |
| `CODING_STANDARDS.md`의 소비·코딩 기준 집행을 review에 배치한다. | retro L31–42 | 저자는 구현자의 문맥 부담을 이유로 이 문서는 review에서 읽고 기준 집행을 검토자가 맡도록 설명한다. 모든 기준·지침을 구현자 입력에서 배제한다는 계약은 아니다. |
| 장기 효과·철회는 완성돼 있지 않다. | retro 사용 가이드 L37–43: “You must still prune checks yourself.” | 한 세션 관찰로 기존 검사들의 장기 오탐·효용을 평가하지 못한다고 설명한다. 우리의05에서 채택 후 관찰·보류·철회를 별도로 설계할 이유가 남는다. |

사용 가이드 L51은 retro를 사건 기록 시스템으로 보지 않는다. 따라서 경험 개선이 있으니 Work 기록이 불필요하다거나, 일상 기록·사실 정정도 매번 retro를 통과해야 한다는 결론은 모두 원문과 다르다. 또한 retro의 환경 개선은 제품 코드 자체의 구조 개선과 구별된다(L57–59). 우리05는 코드·검사·도구·기준·역할 변경까지 열어 두므로 이 범위를 그대로 복사하면 좁아진다.

## 원문으로 따라간 대표 경로 두 개

### 경로 1 — 대화 중 용어를 정하고 후속 구현이 사용한다

| 지점 | 누가 어떤 지침으로 무엇을 하는가 | 실제 경계·근거 |
| --- | --- | --- |
| 대상 설정 | 사용자가 setup을 요청하면 수행자가 기존 root·문서·tracker를 탐색해 초안을 보여 주고 대상별 문서 위치·소비 규칙을 반영한다. | setup L15·21–30·63–82·106–118. 설치 실행은 이번에 하지 않았다. |
| 내용 대화 | 사용자가 `grill-with-docs`를 요청한다. 같은 수행자가 `grilling`과 `domain-modeling`을 각각 호출한다. | [grill-with-docs](../source/workflow-references/matt-pocock/repository/skills/engineering/grill-with-docs/SKILL.md) L7: “Call the Skill tool twice”. wrapper가 두 책임의 실행을 조합하는 실제 본문이다. |
| 사실과 결정 | agent는 필요한 사실을 조사하고, 사용자는 열린 선택을 답한다. 모호한 용어와 코드의 불일치를 구체 사례로 확인한다. | grilling L26–30, domain-modeling L46–58. |
| 즉시 유지 | 해결된 용어는 glossary에 반영하고, 특별히 보존할 결정만 ADR 작성을 제안한다. | domain-modeling L60–74. [ADR 형식](../source/workflow-references/matt-pocock/repository/skills/engineering/domain-modeling/ADR-FORMAT.md) L12–23은 짧은 맥락·결정·이유와 필요한 상태·대안·영향을 담는다. |
| 다음 수행의 소비 | 구현자가 implement를 사용하면 TDD를 호출하고, TDD는 코드 탐색 때 glossary와 해당 영역 ADR을 읽는다. 새 domain-modeling 호출을 전제하지 않는다. | [implement](../source/workflow-references/matt-pocock/repository/skills/engineering/implement/SKILL.md) L11, tdd L8–10. |

이 경로는 **작업 중 자연스러운 변경 → 지속 의미 보존 → 후속 실행의 직접 사용**을 보여 준다. 매번 읽은 것을 Work current에 복사하는 경로는 아니다. 동시에 새 작업에 필요한 선택·진행·미확인을 어디에 지속할지까지 정의하지 않으므로 우리 Work 운영 전체의 대안은 아니다.

### 경로 2 — 개발 결과 검토와 환경 개선 후보를 구별한다

| 지점 | 입력·실행·반환 | 실제 경계·근거 |
| --- | --- | --- |
| 개발 결과 | implement가 TDD·검사를 수행하고 code-review를 호출한다. 전체 병렬 구현의 경우 implement-spec이 통합 branch의 review와 수정을 연결한다. | implement L11–17, implement-spec L27–38. |
| 검토 입력 선택 | fixed point와 diff를 정하고 실제 요구 출처와 저장소의 코드 기준을 찾는다. | code-review L17–41. |
| 독립 축의 반환 | Standards와 Spec 검토가 다른 subagent에서 수행되고 근거가 있는 발견을 두 축으로 반환한다. | code-review L58–89. 합의된 우리의 개선 검토·행동 검증 역할과 동일하다고 보지 않는다. |
| 경험 질문 | 사용자가 해당 세션에서 또는 원문을 지정해 retro를 요청한다. 작성 기준을 읽고 실제 어려움·오류에서 환경 개선 후보를 만든다. | retro L11–25, ask-matt L34·38. 자동 후속 실행이라고 읽지 않는다. |
| 선택·반영 | 사용자가 후보를 선택한다. 실제 검사·문서·도구 변경은 그 선택과 별도 실행 범위에 달려 있다. | retro 사용 가이드 L5·35. SKILL 본문은 후보 제시에서 끝나므로 적용 완료를 추정하지 않는다. |
| 다음 소비 | 반영된 저장소 standards는 이후 code-review가 찾고, 자동 검사는 실제 실행 경로에서 쓰여야 한다. | code-review L34–41, retro L18–19. 채택 후 효과 추적의 정식 절차는 확인되지 않는다. |

이 연결에는 원문 자체가 알리는 공백도 있다. implement L15–17은 review 후 commit을 적지만 code-review L21은 `HEAD`까지의 diff를 사용한다. [code-review 사용 가이드](../source/workflow-references/matt-pocock/repository/docs/engineering/code-review.md) L79–81도 중간 commit이 없으면 미커밋 변경을 볼 수 없다고 설명한다. 이번에는 실제 실패를 재현하지 않았으며, **이름으로 연결됐다고 입력 시점·대상 판본까지 자동 정합하다고 할 수 없다는 반대 근거**로 남긴다.

## 차용 후보와 그대로 가져오지 않을 조건

| 차용 후보 | 우리 논의에서 확인할 지점 | 다른 적용 조건·비용 |
| --- | --- | --- |
| 같은 실행을 workflow와 직접 요청 양쪽에서 사용 | model-invoked reference·code-review·domain-modeling의 두 진입을 현재 공통 맥락 후보와 비교 | 같은 절차의 재사용을 지지하지만 읽기·반영을 하나로 합쳐야 한다는 근거는 아니다. 호출 설정은 실제 host에서 별도 확인해야 한다. |
| 경로뿐 아니라 적용 조건을 가진 연결문 | Main 인수·담당자의 추가 탐색·context 본문/상세/형성 자료 진입에서 질문과 연결 이유를 남김 | 모든 자료를 기본 입력에 싣지 않는다. 자료를 숨겨 필요한 판단이 누락되는지도 함께 본다. |
| 내용 소비와 능동적 의미 변경의 구별 | 단순 원문 이해·적용, Work의 적용 의미 유지, Personal·Project 기준 변경을 각각 판정 | Matt의 용어집 경계는 좁다. 우리의 Project 현재 사실·Work 선택·Personal 조건을 같은 쓰기 권한으로 다루지 않는다. |
| 공통 수행과 대상별 운영 지식의 분리 | workflow/맥락 절차는 방법을, context 진입·관리 지침은 대상의 내용·위치·권위를 소유하게 함 | setup의 고정 파일명을 우리 모든 Project에 강제하지 않는다. 대상별 지침을 읽는 실제 consumer 연결이 있어야 한다. |
| 경험을 문장 추가로 자동 해결하지 않음 | 05에서 기록·개선 선택·반영·효과 관찰을 나누고 코드·검사·도구·역할 변화 또는 유지 비교 | retro는 environment 후보 중심이며 제품 코드 개선과 장기 관찰은 부족하다. 구현자에게 Personal 기준을 주는 현재 합의는 유지한다. |
| 소비자와 실행을 실제로 따라가 교체 범위를 판단 | 06에서 callable 이름·참조 본문·target 지침·host 설정·현재 Work 접근점을 함께 대조 | 한 정본 원칙만으로 제거가 무영향해지지 않는다. 스킬 이름을 바꾸면 호출자·안내·metadata가 영향을 받는다. |

우리의 기존 read/update는 선택·이해와 지속 의미의 근거·권위·Owner를 이미 다뤘다. Matt가 같은 낱말을 쓴다는 이유로 새 필요를 입증하지 않는다. 기존 Recover는 정해진 Work와 Project 선택을 packet으로 제공했고 Maintain은 Work의 의미를 갱신했다. 이번 Matt 자료는 이에 대응하는 범용 current·Recover·Maintain 장치를 제시하지 않는다. 새 development는 역할별 원문 읽기·동적 탐색과 Main의 직접 기록·전체 판단을 소유하므로, 차용할 것은 그 연결을 더 분명하게 만드는 부분이다.

### 추가 원문이 설명하는 유지비용

[new-skills](../source/workflow-reference-supplements/2026-10-25-matt-maintenance/new-skills.md) L7–11은 스킬 하나를 “permanent maintenance surface”로 보고 다른 스킬·사용 가이드·ask-matt의 경로 안내·plugin manifest를 함께 맞춰야 한다고 설명한다. 기존 조합으로 되는 동작은 저자의 catalog에 새 스킬로 추가하지 않지만, 사용자별 조합은 각자의 prompt나 skill로 두라고 한다. **우리에게 적용할 것은 실제로 함께 유지해야 하는 연결을 세는 관점**이다. 새 구성의 필요성을 검토하는 이번 작업에 저자의 기여 제한을 신설 금지 규칙으로 올리지 않는다.

[harness-name-collisions](../source/workflow-reference-supplements/2026-10-25-matt-maintenance/harness-name-collisions.md) L7–20은 host의 내장 이름이 바뀔 때마다 스킬 이름을 변경하면 사용자 기억과 스킬 간 참조가 계속 깨진다고 설명한다. 저자는 host의 이름 해석과 스킬 본문을 구별하고 namespace 또는 사용자가 소유한 사본의 이름 변경으로 대응한다. 우리06에서는 **내용·책임 변경과 특정 host의 발견·호출 충돌을 구별하되, 실제 호출 가능성은 함께 확인**해야 한다. 이 방침을 현재 host의 충돌 해결 성공이나 이름 변경이 항상 부적절하다는 근거로 쓰지 않는다. 본문을 유지해도 설치 방식·호출자·사용자 진입을 조정할 비용은 남는다.

## 반대 근거와 자료 공백

1. **하나의 context 스킬이 정답이라는 근거가 아니다.** 공유 reference를 skill로 호출하는 경우와 일반 파일로 연결하는 경우가 함께 있고, passive glossary 소비는 별도 active 스킬을 부르지 않는다. 서로 다른 수행을 조합하는 얇은 wrapper도 있다. 현재 후보의 실행 분기를 대입해야 어느 포장이 적합한지 판단할 수 있다.
2. **스킬 호출과 agent·문맥 분리는 다르다.** writing-for-agents L49은 인라인 호출로 뒤 단계가 현재 문맥에서 사라지지 않는다고 설명한다. 독립 스킬마다 별도 agent·보고서·전체 재독이 생긴다고 가정하면 비교 비용이 왜곡된다.
3. **`CODING_STANDARDS.md`의 소비·집행 배치는 우리 기준 공유 합의와 대조해야 한다.** retro L31–35는 구현자의 탐색·작성·디버깅 부담을 이유로 coding standards 집행을 reviewer 책임으로 설명하고, L42는 해당 파일을 review에서 읽고 implementation에서는 읽지 않는다고 적는다. 그러나 실제 implement SKILL L7–17은 기준 파일을 읽지 말라는 제한을 별도로 두지 않는다. 호출하는 tdd L8–10은 반복 규칙과 glossary·관련 ADR을 읽게 하고, L26은 필요하면 codebase-design을 호출한다. retro L41도 root `CLAUDE.md`/`AGENTS.md`가 저장소에서 일하는 모든 agent에 입력된다고 명시한다. 따라서 ‘구현자는 모든 기준을 안 읽는다’, ‘root 지침도 받지 않는다’ 또는 실제 실행에서 기준이 노출되지 않았다는 주장으로 확대할 수 없다. 이 저자의 coding standards 배치를 근거로 우리의 Personal 기반 구현을 없애지 않는다. code-review 자체는 저장소 기준을 찾으므로 retro의 ‘review에는 탐색이 필요 없다’는 설명도 실제 자료 읽기 0회라는 뜻으로 해석하지 않는다.
4. **검토 결과의 독립성·종합 방식도 다르다.** code-review는 두 축의 출력을 병합·재정렬하지 않는다. 우리의 Main은 원래 목표·계약·근거에 다시 대조해 적용과 완료를 판단한다. 두 축 분리를 그대로 전체 의사결정 방식으로 가져오지 않는다.
5. **저자의 사용 가이드는 운영 한계를 인정한다.** code-review 가이드 L59–77은 재귀 위임, 근거 재검증 부재, 결과 수렴 부재에 관한 사용자 보고를 소개한다. 원본 로그·재현은 이번 자료에 없어 사실 강도는 저자 설명까지다. 이 자료를 안정적인 역할 운영의 실증으로 확대하지 않는다.
6. **이 조사 범위에서 장기 관리와 제거 시험은 확인되지 않았다.** retro 가이드 L37–43은 과거 생성한 검사들의 장기 효용·오탐 관찰과 정리를 맡지 않는다고 밝힌다. setup 문서는 대상 지침을 직접 고칠 수 있게 하지만, 재배포 충돌·rollback·모든 live consumer 갱신을 일반 계약으로 정의하지 않는다. 스킬을 제거한 뒤 업무가 어떻게 계속되는지 실행한 증거도 이 자료에는 없다.
7. **저장소 유지보수 방침은 보편 설계 기준이 아니다.** [SCOPE](../source/workflow-references/matt-pocock/repository/SCOPE.md) L9–18은 관찰된 실패와 저자의 철학에 맞는 이슈만 받으며 기존 스킬 조합으로 되는 새 스킬 제안을 받지 않는다. 이는 개인 라이브러리의 기여·관리 정책이지 우리에게 새 구성 제안을 금지하는 근거가 아니다.
8. **추가 확보와 남은 자료 공백:** 최초 snapshot에 없던 `.out-of-scope/new-skills.md`와 `harness-name-collisions.md`는 위 동일 commit 보충 원문으로 확보해 유지비용·이름 변경 방침을 확인했다. `subagent-recursion.md`와 `setup-skill-verify-mode.md`는 계속 미보존이다. 재귀 위임 대응이나 setup 검증 모드를 별도로 두지 않은 정확한 이유까지 판단할 때 필요하며, 현재 자료로 그 이유를 채우지 않는다.
9. **대상 Project와 실행 증거가 없다.** 실제 제품의 `docs/agents/domain.md`, glossary·ADR·standards의 변경 이력과 소비 로그는 보존하지 않았다. 선택·문서 존재·호출 선언과 실제 읽기·작업 적용·장기 효과를 나눠야 한다. ask-matt가 연결하는 일부 미보존 스킬은 이번 질문에 필요하지 않아 조사하지 않았다.

## 다음 종합에 남길 판단

Matt에서 직접 가져올 수 있는 유력한 관점은 **호출·참조·내용 소유를 구별하고, 실제 소비·쓰기 경로로 분리의 가치를 확인하는 방식**이다. 일반 읽기마다 독립 스킬을 요구하지 않으면서도 능동적 맥락 작업을 여러 workflow와 직접 요청이 함께 사용할 수 있다. 이 두 사실은 함께 성립한다.

따라서 현재 공통 맥락 후보에서는 ‘한 파일인가 둘인가’보다 **어떤 질문에서 어떤 정본을 읽고, 어떤 의미가 바뀌었을 때 누구의 권한으로 어디를 쓰며, 그 결과를 다음 담당자가 어떻게 다시 사용하는가**를 먼저 대조한다. 일상 유지와 경험 개선의 입력·종료가 다르다는 사실을 유지하고,02의 Work 구성·05의 개선 선택과 관찰·06의 실제 배치·07의 전체 연결에 필요한 차이를 넘긴다. 이번 연구는 차용·폐기·설치 결정을 확정하지 않는다.
