# 형식 후보를 만들기 전에 참고할 외부 자료와 비교 항목

2026-10-17. [개선 조언 59](2026-10-16-59-format-design-objectives-advisor.md) 이후 Main이 같은 내용으로 두 형식을 비교하자고 제안했다. 사용자는 형식 제작보다 앞서 어떤 외부 자료의 무엇을 참고할지 명확히 하도록 물었다. 이 기록은 참고 범위와 도출 방법에 대한 Main의 제안이며, 형식·규칙 채택은 아니다.

## 사용자 요청과 순서 보완

> 근데 그전에 그럼 형식 만들고 외부 레퍼 참고한다는건가?
> 근데 그전에 어떤 외부 레퍼를 어떤걸 구체적으로 참고할건지 이런건 어덯게 돼?

앞선 답변은 형식 후보 제작을 먼저 설명하고 레퍼런스 사용을 뒤에서 짧게 언급했다. 기존 조사는 이미 했지만, 그 자료의 구체 부분과 이번 설계 선택의 연결을 충분히 보여 주지 못했다.

현재 해야 할 일은 **우리 문제에 대응하는 외부 구성의 구체 부분을 대조하고, 가져올 요소·조정할 조건·보류할 요소와 이유를 제시하는 것**이다. 그 결과를 근거로 형식 후보를 만든다. 앞서 제안한 ‘판단 주제에서 출발’과 ‘작업 상황에서 출발’도 아직 두 최종 후보로 고정하지 않는다. 목표·비교 기준 역시 잠정안이며 자료를 대조하면서 놓친 문제나 비용이 보이면 보완한다.

## 우선 참고할 구체 범위

| 우리 쪽에서 결정할 것 | 읽을 자료의 구체 부분 | 비교해서 얻을 판단 |
| --- | --- | --- |
| 기준 하나를 얼마나 설명하고 어떤 요소를 함께 둘지 | [Matt codebase-design](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design/SKILL.md)의 용어·원칙·질문·코드 대비, [pstack Boundary Discipline](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/principle-boundary-discipline/SKILL.md)의 이유·적용 위치·질문 | 새로운 개념을 설명해야 하는 기준과 익숙한 개념을 적용시키는 기준의 구성 차이. 공통 항목을 어느 정도 두고 기준별 설명 차이를 어디까지 허용할지. |
| 상황에 따라 다른 선택을 어떻게 전달할지 | Matt의 설계 질문과 대비 예시, [pstack Model the Domain](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/principle-model-the-domain/SKILL.md)의 대안·적용하지 않을 조건, [Vercel](https://vercel.com/blog/teaching-agents-product-design-at-vercel)의 reference 예시 중 범위·이유·예외·사례 | 질문·대비 사례·예외가 각각 필요한 경우. Field와 Container처럼 조건이 달라지면 다른 선택이 성립하는 판단을 보존할 방법. |
| 무엇을 묶고 나누며 언제 찾아 읽게 할지 | [Matt writing-for-agents](https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-for-agents/SKILL.md)의 `Context pointers`·`Information hierarchy`·`When to split`, [pstack Poteto Mode](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/poteto-mode/SKILL.md)의 `Principles`, Vercel의 `How the skill routes` | 항상 필요한 내용과 특정 상황의 내용, 주제 분류와 읽는 조건, 본문과 별도 참조의 관계. 파일·skill 수와 읽기 부담도 함께 비교한다. |
| 구현자·검토자가 기준을 실제 선택에 어떻게 쓸지 | Vercel의 SKILL 예시 `Workflow / Decide, then implement`·`Review Output`, pstack Poteto Mode의 적용한 원칙과 작업별 playbook 연결 | 기준을 읽게 하는 시점, 확인할 근거, 결과에 남길 정보. 외부의 보고·수정 권한을 그대로 채택하지 않고 현재 B 방향과 연결한다. |
| 설명·질문·사례의 양과 보완 방법을 어떻게 정할지 | [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)의 `The anatomy of effective context`·`Context retrieval and agentic search`, Matt 작성 지침의 `Pruning` | 구체성과 유연성, 대표 사례와 불필요한 나열, 처음 제공할 정보와 필요시 읽을 정보의 균형. 효과는 실제 적용 뒤 별도로 확인한다. |

같은 형식 결정에 여러 자료를 함께 대조한다. 한 저자에게 한 기능을 고정 배정해 조각을 합치거나 모든 참고 요소를 반드시 넣는 방식으로 다루지 않는다. Anthropic은 완성된 기준 문서 양식이 아니라 구성·정보량·시험 방법을 판단할 보조 근거다. Vercel의 공개 구조는 축약 예시이며 내부 전체 구현과 구별한다. Matt의 고정 설계 판본과 현재 작성 지침, pstack main 조회도 동일 판본으로 묶지 않는다.

## 비교가 실제 선택으로 이어지는 예

Matt의 설계 자료는 공통 용어와 관계를 설명하며 여러 원칙·질문·코드 대비를 연결한다. pstack은 원칙별 상세 파일에 필요한 이유·행동·질문·예외를 다르게 배치한다. Vercel의 reference 예시는 범위·규칙·이유·예외·출처를 명시한다. 여기서 우리가 고를 것은 저자 이름이 아니라 **공통으로 필요한 정보, 함께 읽어야 하는 정보, 기준마다 달라질 설명의 양과 형태**다.

Matt의 용어 체계를 통째로 들이면 사용자 관점과 다른 설계 방향이 강해질 수 있다. 압축된 pstack 원칙을 그대로 가져오면 적용 조건이 충분히 전달되지 않을 수 있다. 규칙마다 모든 항목을 강제하면 짧은 기준까지 작성·갱신 비용이 커질 수 있다. 이 비용과 59의 목표·비교 기준을 대조해 선택 이유를 제시한다. 아직 어느 방식이 우리 환경에서 가장 효과적인지 확인한 것은 아니다.

## 다음 산출물의 범위

다음에는 위 각 결정에 대해 외부 자료의 구성 차이와 우리 쪽에서 가져올 것·조정할 것·보류할 것 및 이유를 짧게 비교한다. 확인된 근거로 의미 있는 형식 후보가 드러나면 작은 초안을 만든다. 형식 후보의 수나 첫 진입 방식을 먼저 고정하지 않는다. 내용 예시는 이미 논의한 기준 중 형식의 차이를 드러내는 데 필요한 만큼만 사용한다.

이번 연결은 01-02의 표현과 03의 배치, 01-01·04의 사용, 01-03의 확인, 02·05의 갱신 접점을 보기 위한 것이다. 각 Ticket의 전체 구현·역할 수·권한을 이 단계에서 확정하지 않는다.

## 확인 범위

59·state와 기존 조사 근거를 읽고, Matt 작성 지침·pstack 독자 부담 원칙·Vercel·Anthropic 공식 자료를 2026-10-17 다시 조회했다. 다른 세부 구성은 이번 세션에서 확인한 57·58의 원자료와 조사자의 후속 비교를 사용했다. 공개 지침은 분석 대상으로 읽었으며 현재 작업에 설치·실행하지 않았다. 제품·전역 하네스·source 사본 변경이나 적용 실험은 없다.
