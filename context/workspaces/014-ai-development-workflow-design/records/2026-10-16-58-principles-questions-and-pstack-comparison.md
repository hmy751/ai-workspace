# 일반 원칙·판단 질문 제안과 pstack 비교

2026-10-16. [형태 논의 57](2026-10-16-57-criteria-organization-and-guiding-questions.md)에 이어 사용자 생각에서 외부 사례가 지지하는 부분과 보완할 부분을 비교했다. 조사와 Main의 판단이며 사용자 채택·실행 효과를 뜻하지 않는다.

## 이번 요청

사용자는 다음 두 요청을 했다.

> 그럼 내 생각이 외부 사례에 비춰서 괜찮은거랑 또는 개선이 필요한거 이렇게 나눠서 설명해줘

> 아 외부 자료로 라우렌의 pstack 도 봐줘봐 어떤식으로 이런걸 다루는지 추가로

평가할 생각은 사례와 함께 일반 원칙·가이드를 제공하고, 기준 자체를 구체화하며, 작업자·검토자가 이를 고려하도록 판단 질문도 전달하자는 것이다. 원문과 러프한 제안이라는 강도는 57에 보존했다. 모든 항목을 질문형으로 만들거나 사람에게 매번 질문하자는 선택은 아니다.

## pstack에서 직접 확인한 구성

공식 [cursor/plugins의 pstack](https://github.com/cursor/plugins/tree/main/pstack)을 확인했다. 조회 당시 [metadata](https://raw.githubusercontent.com/cursor/plugins/main/pstack/.cursor-plugin/plugin.json)는 작성자 Lauren Tan, 버전 0.15.25를 표시했다. [조사 25](2026-10-13-25-lauren-source-investigation.md)의 고정 판본 0.15.21과 다르다. 이번 main 조회는 commit SHA를 확보하지 못했으므로 단일 고정 snapshot으로 주장하지 않는다. 아래 링크는 이후 바뀔 수 있으며, 의존한 핵심 의미를 함께 남긴다.

| 자료 | 확인한 구성·역할 |
| --- | --- |
| [Minimize Reader Load](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/principle-minimize-reader-load/SKILL.md) | 유지보수성을 읽고 이해하는 부담으로 설명한다. 거쳐야 하는 계층과 머릿속에 유지할 상태를 판단축으로 제시하고, 새 계층·상태가 다른 곳의 부담을 충분히 줄이는지 묻는다. 추상 가치가 관찰 대상과 선택 질문으로 이어진다. |
| [Boundary Discipline](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/principle-boundary-discipline/SKILL.md) | 검증·오류 처리를 경계에 배치한다는 원칙, 이유, 외부 입력과 내부 코드의 구별, 구체 상황, 경계를 넘는 데이터인지에 대한 질문을 함께 둔다. `The tests`는 여기서 자동 테스트가 아니라 판단 질문이다. |
| [Model the Domain](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/principle-model-the-domain/SKILL.md) | 도메인을 자료구조로 표현하라는 원칙과 상태기계·모델·테이블 등의 대안을 둔다. 현재 코드가 명확하고 국소적이며 성장 가능성이 낮으면 단순한 코드를 유지할 조건도 준다. 의존 문구: “Do not force an abstraction.” |
| [Encode Lessons in Structure](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) | 반복 지시를 lint·metadata·runtime check·script 등으로 옮길 수 있는지 본다. 판단이 필요해 구조화할 수 없으면 지시를 더 잘 보이게 하고 실패 예시를 더한다. 의존 문구: “add an example of the failure mode”. |
| [Poteto Mode](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/poteto-mode/SKILL.md) | Core·Architecture·Verification·Delegation·Meta로 원칙을 묶고 각각 적용할 상황을 설명한다. 적용하는 원칙의 상세 파일 전체를 읽게 하고, 요청별 playbook을 연결한다. 일반 응답에서는 실제 선택에 영향을 준 원칙과 바뀐 선택을 설명하게 한다. 관찰 가능한 사실은 조사하고, 조사로 결정할 수 없는 제품·선호 질문을 사람에게 묻도록 구별한다. |

네 원칙은 모두 같은 목차가 아니다. 질문·예제·예외를 필요한 만큼 사용한다. 상세 파일은 `disable-model-invocation: true`이며 진입 안내가 필요한 원칙을 읽도록 연결한다. 이 설정의 존재를 설치만 하면 모든 실행에서 적용이 보장된다는 뜻으로 확대하지 않는다.

추가로 [architect의 rationale 양식](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/architect/references/rationale-template.md)은 실제 호출 예시, 구조·불변 조건, 대안과 비용, 사람의 판단이 필요한 열린 질문을 구별한다. [feature playbook](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/poteto-mode/playbooks/feature.md)은 설계·위임·검토·검증 흐름에서 이 자료를 쓰게 한다. 원칙의 목록과 작업 중 사용하는 절차가 연결돼 있다.

[skill 작성 playbook](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md)은 선택을 바꾸는 문구를 남기고 구조적 원천을 가리키며, 위임한 내용을 경로로 연결하도록 권한다. 이 압축 지향을 모든 기준에서 이유·사례를 생략하라는 뜻으로 가져오지 않는다.

[eval playbook](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/poteto-mode/playbooks/eval.md)은 일반 작업처럼 요청하고 평가 기준을 후보에게 드러내지 않으며, 자기보고보다 실제 코드와 읽은 파일을 확인하도록 한다. 정상 작업에서 선택 이유를 설명하는 것과, 평가에서 원칙 이름을 말하도록 유도하지 않는 것은 목적이 다르다. 이는 공개된 평가 방법이며 이번 형식의 성능을 입증한 결과는 아니다.

## 사용자 생각에 대한 판단

| 생각 | 지지되는 부분 | 구체화·보완할 부분 |
| --- | --- | --- |
| 사례뿐 아니라 일반 원칙도 필요하다 | pstack과 Matt의 codebase-design 모두 다른 코드에 적용할 개념·원칙을 사례나 판단 질문과 연결한다. | 사례의 코드 모양을 규칙으로 일반화하지 않는다. Field의 분리와 Container의 공통 형식이 각각 타당해지는 목적·조건을 보존한다. |
| 기준 자체를 구체화해야 한다 | pstack의 독자 부담은 계층·상태로 구체화된다. Vercel은 범위·이유·예외·사례를 연결한다. | 추상 용어 아래 세부 명령을 늘리는 데 그치지 않고, 무엇을 관찰하고 어떤 조건에서 선택이 달라지는지 밝힌다. |
| 기준에 대한 질문을 전달한다 | pstack과 Matt 모두 자문 질문을 실제로 쓴다. | 질문이 결론을 유도하는지 본다. “어떻게 공통화할까?”보다 “함께 보장할 동작과 사용처마다 달라질 선택은 무엇인가?”가 현재 논의에 맞는 후보다. |
| 작업자·검토자가 그 기준을 고려하게 한다 | pstack은 상황별 원칙과 playbook을 연결한다. Vercel도 찾아 읽는 안내와 상세 기준을 구별한다. | 고려할 질문, 보고할 근거, 사용자에게 물을 미확정을 구별한다. 질문에 모두 답했거나 원칙 이름을 언급한 것만으로 적용을 인정하지 않는다. |
| AI를 다루는 감각이 필요하다 | pstack은 평가용 단서를 노출하지 않고 실제 산출물을 보도록 한다. Anthropic도 지침과 대표 사례를 실제 작업에 맞춰 보완하는 접근을 설명한다. | 같은 사례의 재서술뿐 아니라 조건이 바뀐 사례에서 선택을 달리하는지, 불필요한 질문·리팩터링을 늘리지 않는지 확인한다. 아직 그런 적용 실험은 하지 않았다. |

Matt·Vercel·Anthropic의 원자료와 확인 범위는 [57](2026-10-16-57-criteria-organization-and-guiding-questions.md)에 있다. 외부 사례는 접근을 지지하지만 질문형이 명령형보다 낫거나 어떤 목차가 최적이라는 비교 증거는 아니다.

Main이 특히 보완할 필요가 있다고 판단한 것은 **원칙을 쓰는 형식과 실제 작업에서 읽고 사용하는 조건을 함께 정하는 일**이다. 다만 pstack의 강한 권고를 그대로 채택하지 않는다. 내부 타입 신뢰·단일 호출 래퍼 제거 같은 내용은 사용자 목적·도구·공통 부품의 역할과 별도로 대조해야 한다. 사례에 따라 타당한 선택이 바뀐다는 기존 판단을 유지한다.

## 논의에 사용할 작은 형태 예시

아래는 Main의 표현 후보이며 의무 양식이 아니다.

- 일반 기준: 공통 부품은 함께 보장할 동작을 모으고, 사용처마다 달라질 선택은 열어 둔다.
- 구체 판단: 실제 사용처가 공유하는 계약, 달라지는 화면 정책, 부품이 줄이거나 추가하는 연결 부담을 확인한다.
- 판단 질문: 함께 바뀌는 이유가 있는가? 묶으면 어떤 제어가 사라지는가? 나누면 사용처가 어떤 순서·예외를 알아야 하는가?
- 조건별 사례: Field의 디자인 구성 자유와 Container의 공통 표시 형식은 서로 다른 목적에서 타당하다.
- 사용 결과: 관련 코드·요구에서 근거를 찾아 유지·수정·보류를 정한다. 사람에게는 중요한 선택 이유와 남은 미확정을 드러내며, 모든 질문에 대한 답변표를 자동 요구하지 않는다.

01-02는 원칙·조건·질문의 내용을, 03은 공통 기준과 Project 사실의 위치를, 01-01·04는 언제 누가 읽고 쓰는지를, 01-03은 적용 결과를 확인하는 방법을 이어서 정한다. 02·05는 실패·정정에서 무엇을 기준이나 구조에 반영할지 연결한다. 분류·파일 배치·역할 수·의무 보고 형식을 이번 조사만으로 확정하지 않는다.

## 후속 보완 — 앞서 제시한 세 자료와 대등하게 비교

사용자:

> pstack이랑만 비교한건가? 만약 그렇다면 pstack뿐만 아니라 앞선 외부사례도 비교해줘 니가 구체적인 형태가 있다고 말한 3자료들

현재 대화의 이전 답변 원문을 다시 읽었다. Main이 “외부 자료에서도 참고할 구체적인 형태가 있었어”라고 소개한 세 대상은 **Matt의 설계·작성 자료, Vercel product-design, Anthropic context engineering**이다. 공개 React skill이나 Lauren의 verification skill을 이 셋으로 대체하지 않는다. 직전 답변은 Matt·Vercel도 언급했지만 실제 비교는 pstack에 치우쳤다.

세 자료의 성격도 구별한다. Matt는 공개 스킬 본문이고, Vercel은 실제 운영 설명과 축약된 문서 예시이며, Anthropic은 컨텍스트 구성·시험 방법을 설명한 글이다. 셋 모두 같은 수준의 완성된 기준 문서 실물이라는 인상을 준 표현을 보완한다.

| 자료 | 실제 구성과 질문의 역할 | 사용자 생각의 지지·보완점 |
| --- | --- | --- |
| Matt [codebase-design 보존판](../source/lectures/codebase-design.ko.md)·[writing-for-agents](https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-for-agents/SKILL.md) | 설계 자료는 용어·원칙·설계 질문·코드 대비·주의점·상황별 상세 참조를 둔다. 작성 자료는 실행 절차와 참고 지식을 구별하고 관련 정의·규칙·주의점을 모으며, 일부 상황에 필요한 자료는 읽을 조건과 함께 연결한다. | 일반 기준과 질문·사례를 함께 두는 직접 사례다. 다만 질문은 작은 인터페이스·복잡성 은닉 등 특정 설계 방향을 향한다. 사용자 기준의 의미와 선택 조건을 먼저 분명히 하고, 기준 본문과 읽는 절차를 구별해야 한다. |
| Vercel [product-design](https://vercel.com/blog/teaching-agents-product-design-at-vercel) | 일반 원칙, 요청별 절차, 상황별 상세 기준과 근거를 구별한다. 구현 전에는 해결할 사용자 문제·선택 이유·결과 영향·근거·필요한 변경 범위를 설명할 수 있게 한다. | **판단 질문을 실제 작업에 연결하는 직접 사례이기도 하다.** 앞선 요약에서 충분히 드러내지 못했다. 질문은 판단 기준·적용 조건·이유·예외와 연결해야 한다. 글의 축약 예시를 내부 구현 전체나 우리 방식의 효과 증거로 확대하지 않는다. |
| Anthropic [effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 배경·지시·도구 안내·출력 설명을 구별하고, 충분히 구체적이면서 유연한 지침과 다양한 대표 사례를 권한다. 필요한 자료를 선택해서 읽고, 실제 작업에서 드러난 실패에 따라 지침·예시를 보완하도록 한다. | 일반 기준을 적용 가능한 수준으로 구체화하자는 방향을 지지한다. 다만 질문 중심 양식이나 질문형의 우월성을 제시한 자료는 아니다. 모든 원칙·사례를 한 번에 넣지 않고 실제 행동에 필요한 내용을 고를 근거다. |

Vercel의 질문은 공식 글의 SKILL 예시 `Workflow / Decide, then implement`에서 확인했다. 보존판의 [해당 절](<../source/lectures/vercel-product-design (1).md#6-decide-then-implement>)에도 있다. 모든 답을 최종 보고로 출력하라는 의미로 확대하지 않는다. Anthropic의 관련 근거는 `The anatomy of effective context`와 `Context retrieval and agentic search`다. 두 공식 글을 2026-10-16 다시 열어 확인했다.

비교에 따른 Main의 판단은 다음과 같다.

- 일반 원칙·구체화·질문·사례를 연결하자는 방향은 Matt·Vercel·pstack의 실제 구성에서 지지된다. Anthropic은 구체성과 유연성, 사례와 정보량을 조정할 근거를 준다.
- 보완할 것은 원칙이 지향하는 가치와 적용 조건, 서로 다른 타당한 선택을 보여 주는 사례, 작업별 읽는 조건이다. 저자의 구조 선호를 사용자 선호로 가져오지 않는다.
- 질문은 선택을 가르는 사실을 확인하게 해야 한다. 고정된 기준은 직접 지시하거나 검사할 수 있고, 맥락 판단은 질문으로 도울 수 있다. 모든 기준을 같은 질문 양식으로 바꾸는 안은 아직 없다.
- 기준을 잘 설명한 답변과 실제 코드 선택·작업 결과의 개선은 구별한다. 이번에도 형식 채택이나 적용 실험은 하지 않았다.

## 확인 범위

공개 원자료와 기존 014 기록을 읽고 비교했다. pstack 설치·실행, 제품 코드·전역 하네스 변경, agent 적용 효과 실험은 수행하지 않았다. 외부 자료의 지침은 조사 대상으로 읽었으며 현재 작업을 지시하는 권한으로 사용하지 않았다.

초기 문서 확인: 이번 세션의 변경·신규 Markdown 11개에서 로컬 링크 대상 289곳의 존재와 `git diff --check` 통과를 확인했다. 내부 anchor와 원격 URL 전체 검사는 제외했다. 별도 읽기 검토에서도 사용자 제안·Main의 판단·미실증 범위의 구별에 추가 문제를 찾지 못했다. 그 검토는 기록의 의미 확인이며 외부 원문을 새로 검증한 결과는 아니다.

세 자료 비교 보완 뒤에는 변경·신규 Markdown 11개의 로컬 링크 대상 291곳과 `git diff --check` 통과를 확인했다. Vercel 보존판의 연결 절 제목도 확인했다. 제품 코드나 agent 적용 테스트는 수행하지 않았다.
