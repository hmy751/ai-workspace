# 본문과 형성 맥락을 함께 관리하는 외부 사례 조사

후속: 사용자 적용 요청에 따른 실제 이름 기준 묶음과 변경 실험은 [107](2026-10-20-107-naming-context-pilot-and-maintenance-trials.md)에서 읽는다. 아래의 미적용·제안 표기는 이 기록을 작성한 당시 상태다.

2026-10-20 KST. Karpathy의 LLM Wiki 원문을 반복하는 대신 Lauren Tan과 다른 실무자의 공개 원자료·실제 문서 구성을 조사했다. 대상은 [105에서 확인한 요청](2026-10-20-105-adjacent-formation-context.md), 즉 현재 쓰는 본문 옆에 그 본문을 형성한 의도·배경·판단과 필요한 과정·원문을 재구성한 자료를 두는 구상이다. 아래 적용 판단은 Main의 제안이며 형식 채택이나 데모 반영 결과가 아니다.

## 조사에서 얻은 판단

**우선 참고할 자료는 Lauren의 설계와 rationale 관계, Gwern의 현재 설계와 별도 설계 회고, Ryan Lopopolo의 논지·보조 자료·원자료 구성이다.** 각각 ‘무엇을 담을지’, ‘현재 설명과 형성 과정을 어떻게 연결할지’, ‘해석과 근거를 어떻게 관리할지’에 구체적인 실물을 제공한다. Andy Matuschak은 원자료를 자기 판단으로 재구성하는 방법에, ADR은 바뀐 결정의 당시 이유를 보존하는 방법에 보조 근거가 된다.

이 자료들이 공통으로 `context.md`라는 이름이나 같은 폴더 배치를 요구하는 것은 아니다. 같은 폴더에 두려는 방향은 사용자의 요구이며, 조사에서 검토할 대상은 그 안의 내용·연결·갱신 방식이다. 공개 지식 사이트, 에이전트 실행 문서, 설계 이유 문서, 결정 이력을 하나의 ‘LLM 위키 방식’으로 묶지 않는다.

| 자료 | 직접 확인한 구성 | 이번 구상에 가져올 부분 | 적용의 한계 |
| --- | --- | --- | --- |
| Lauren / pstack architect | 타입·구조 스케치와 함께 한 페이지 rationale | 목적·제약·선택·감수한 비용·대안·열린 질문 | 영구 위키나 원문 보존 체계는 아니다. |
| Gwern.net | 현재 설계 문서에서 별도 Design Graveyard로 연결 | 현재 결과에 도달한 과정과 포기·변경 이유를 다시 읽을 수 있게 한다. | 실패 중심의 문서를 모든 맥락의 형식으로 쓰지는 않는다. |
| Ryan / harness-engineering | 논지별 본문·보조 문서와 별도 source library | 판단을 재구성하고 근거를 그 판단에 연결한다. | 공개 구성의 실물이며 장기 자동 유지 효과의 증거는 아니다. |
| Andy Matuschak | 개념 중심의 지속 노트와 자료별 노트를 구별 | 자신의 해석과 원자료를 구별하고 연결·수정한다. | 한 본문 옆에 맥락 문서를 붙이는 구조와는 다르다. |
| Nygard / Fowler의 ADR | 맥락·결정·결과와 변경된 결정의 연결 | 당시 이유와 현재 상태, 재검토할 조건을 구별한다. | 문서 하나의 전체 형성 맥락을 결정 하나로 축소하지 않는다. |

## Lauren: 결과와 이유를 함께 두되 자료의 용도를 구별한다

Lauren Tan은 `poteto` 계정의 실무자이며 pstack 공개 플러그인의 저자다. 기존 [조사25](2026-10-13-25-lauren-source-investigation.md)와 같은 저자를 대상으로 최신 공개 자료를 다시 확인했다. 기준판은 `cursor/plugins` commit `ddf824aff1e55ba14bd666b30bce3fc69962abe6`, pstack `0.15.28`이다. GitHub API에서 확인한 HEAD 시각은 2026-10-19 22:39:26 UTC다. 검색 캐시의 이전 버전과 구별했다.

### 가장 직접적인 자료: architect의 rationale

[rationale template 고정판](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills/architect/references/rationale-template.md)은 타입·구조 설계에 함께 붙는 짧은 이유 문서다. 문서의 첫 설명은 다음과 같다.

> The prose that ships alongside the type sketch. One page.

Problem, Usage, Shape, Synthesis decision, Tradeoffs accepted, Alternatives considered, Open questions and risks, Next implementation step으로 구성한다. 특히 기존 제약 때문에 선택이 자명하지 않았던 이유, 무엇을 기반으로 삼고 무엇을 버렸는지, 미래 독자가 누락으로 오인할 수 있는 의도적인 절충을 설명한다. [architect 본문](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills/architect/SKILL.md)은 구현 중 설계와의 차이를 드러내고 반복되는 마찰이 생기면 설계를 다시 조사하게 한다.

**이번 적용 판단:** 기준 본문 옆 맥락 자료에도 단순한 배경 소개를 넘어, 왜 현재 선택이 나왔는지와 어떤 손해·범위를 의식적으로 받아들였는지 담을 가치가 있다. 다만 타입 설계용 Usage·Shape·다음 구현 단계를 그대로 복제할 필요는 없다. 이 템플릿은 저장 경로·옛 rationale 보존·원문 snapshot 방법까지 정하지 않는다.

### 위키에 대한 직접 설명: 기능 지도의 목적

Lauren 본인 계정의 [verification-skill-example](https://github.com/poteto/verification-skill-example/blob/d5abe70d0d8c671672b6cef4069363f26c488feb/README.md#why-not-a-wiki)은 `Why not a wiki?`에서 사람이 읽는 위키의 가치를 인정하면서, 에이전트 검증에는 기능별로 좁혀 읽는 자료를 제안한다. `SKILL.md`는 실행 절차, `references/features/README.md`는 색인·전체 점검 순서, 각 기능 파일은 동작·진입·구동·함정을 맡는다. UI 변경과 같은 PR 또는 유지 점검에서 문서와 실제 동작의 차이를 고친다.

이는 **자료를 어느 때 얼마나 읽을지 용도로 나누는 근거**다. 의도·배경의 맥락 문서를 실행 절차로 바꾸라는 근거는 아니다. 이 저장소는 2026-07-30 commit `d5abe70d0d8c671672b6cef4069363f26c488feb`의 가공 예제다. Atlas·Harbor Labs·control-atlas는 실제 제품이 아니고 driver도 생략돼 있다. Lauren의 개인 위키 운영이나 실서비스 검증 결과로 소개하지 않는다.

### 과정 선별과 과거 의도의 재구성

[show-me-your-work](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills/show-me-your-work/SKILL.md)는 선택·이유·증거·결과를 결정 지점별로 남긴다. 모든 행동을 적는 방식은 아니며, 방향 전환·되돌림과 그 계기 등을 선별한다. 이 기록은 기본적으로 임시 작업 자료이고 검토에 필요한 경우에만 커밋하므로, 전 과정을 영구 저장하자는 근거로 쓰지 않는다.

[why의 근거 판단](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills/why/references/epistemics.md)은 당시 직접 진술, 간접 근거, 현재 추론, 추측, 미확인을 구별한다. 현재 결과가 그럴듯하다는 이유로 과거 의도를 역으로 꾸미지 않게 한다. **105의 맥락 문서에서도 실제 발언과 Main이 뒤에 구성한 해설의 차이는 유지할 필요가 있다.**

공식 pstack 관련 Markdown·JSON·TSV와 제한된 공개 검색에서는 Lauren의 지속 지식 위키 운영까지 확인하지 못했다. 이 한계를 ‘Lauren은 위키를 쓰지 않는다’로 확대하지 않는다. 검색된 다른 저자의 `pkstack`은 Lauren의 pstack과 구별했다.

## Gwern: 현재 설계와 그 설계를 형성한 시행착오를 연결한다

Gwern Branwen은 장기간 갱신하는 에세이·자료 사이트 Gwern.net의 저자·운영자다. [현재 설계 설명](https://gwern.net/design)은 목적·설계 원칙·기능·도구를 설명하며, `Abandoned` 절에서 별도의 [Design Graveyard](https://gwern.net/design-graveyard)로 직접 연결한다. 확인 위치: design의 `Abandoned`, design-graveyard의 도입부·`Popup Annotations`·`RSS Feed`.

Design Graveyard는 실패하거나 여러 번 고친 설계의 회고를 재구성한다. 팝업 주석의 변천에서는 링크만 있던 때의 문제, 원문에 접근하기 쉽게 만들려는 의도, 시도한 대안과 구현 비용을 설명한다. 현재 구현만 읽어서는 알기 어려운 선택 이유를 별도 문서에서 복원하는 실제 사례다.

작은 편집마다 보내던 RSS는 잡음이 커서 없앴다는 경험도 남아 있다. 모든 변경 내역의 보존·노출과 독자가 필요한 형성 맥락은 다를 수 있다는 근거다. 월별 변경 목록도 어떤 독자에게 너무 성기다는 한계를 인정한다.

**이번 적용 판단:** 가장 직접적인 문서 관계의 예다. 본문은 현재 기준을 설명하고, 그 자리에서 연결되는 별도 맥락 자료는 이 기준을 낳은 목적·경험·대안·변경 이유를 설명할 수 있다. 단, 우리의 자료에는 긍정적 지향과 받아들인 판단도 있으므로 ‘실패 기록’만으로 구성하지 않는다. 이 사례는 같은 물리적 폴더 배치나 고정 목차를 증명하지 않는다.

## Ryan Lopopolo: 논지·보조 자료·원자료를 구별하면서 연결한다

Ryan Lopopolo의 공개 [harness-engineering 저장소](https://github.com/lopopolo/harness-engineering/tree/226c8d35fb6ea3ed55467753dba6dea2b5fd5778)는 글·강연·사례를 사람과 에이전트가 활용할 자료로 재구성한 산출물이다. 2026-07-18 공개 commit `226c8d35fb6ea3ed55467753dba6dea2b5fd5778`을 기준으로 확인했다. 아래는 개인 공개 저장소의 구조이며 OpenAI 전체의 운영 표준으로 귀속하지 않는다.

[ARCHITECTURE](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/ARCHITECTURE.md)는 `docs/<thesis>/`의 논지·사례·적용과 `sources/`의 원자료·출처 정보를 구별한다. 평소에는 현재 판단에 필요한 논지를 읽고, 정확한 말과 맥락이 판단을 바꿀 때 원자료로 내려간다. 원자료 하나가 여러 논지를 지지할 수 있다.

[본문 작성 지침](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/AGENTS.md)은 주장을 설명하는 문단에 근거를 연결하고, 사용하지 않은 자료는 출처 색인에 남기게 한다. 보조 문서는 기존 본문을 반복하지 않고 새로 필요한 사례·조건을 발전시킨다. [원자료 관리 지침](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/sources/AGENTS.md)은 원문을 문장 개선 목적으로 고치지 않고 해석은 설명 문서에 두며, 원 URL·검토일과 보존본의 버전을 관리한다.

**이번 적용 판단:** 맥락 문서도 실제 판단을 재구성한 글이어야 한다. 근거는 그 글의 특정 판단을 뒷받침하는 위치에 연결하고, 원문과 재구성한 설명의 갱신 방식을 구별한다. 자료마다 문서를 만들거나 대화 순서를 그대로 따를 필요는 없다. 저장소의 `sources/` 구조를 데모에 통째로 가져오려는 제안은 아니다.

공개 이력은 같은 날의 두 커밋이며 실질 내용이 한 번에 공개됐다. 장기 자동 유지가 검증된 위키로 평가할 근거는 부족하다. 일부 context sidecar 설명 역시 제안이므로 실제 동작으로 올리지 않는다. 강점은 확인 가능한 편집 구조와 출처 관계다.

## 보조 레퍼런스: 해석·근거·변경을 다루는 방법

### Andy Matuschak: 원자료를 자기 판단으로 재구성한다

사고·학습 인터페이스 연구자 Andy Matuschak의 [Literature notes are secondary and separate](https://notes.andymatuschak.org/Literature_notes_are_secondary_and_separate)는 자료별 노트와 자신이 소화한 개념 노트를 구별한다. [실제 독서 노트](https://notes.andymatuschak.org/How_to_Take_Smart_Notes_-_Ahrens)에서는 발췌·서지정보와 관련 판단 노트가 연결되고, [갱신 설명](https://notes.andymatuschak.org/How_to_process_reading_annotations_into_evergreen_notes)은 기존 노트를 찾아 연결·병합·수정하고 상위 설명도 다시 고치는 과정을 제시한다.

**이번 적용 판단:** 발췌를 모은 파일만으로 맥락을 보존했다고 하지 않는다. 어떤 발언·경험이 어떤 판단으로 이어졌는지 자신의 설명으로 연결하고 필요한 원문을 뒷받침으로 둔다. 그의 개념 노트망은 본문별 맥락 문서 구조와는 다르므로 구조 전체를 옮길 이유는 없다.

### Nygard와 Fowler: 당시 결정과 현재 유효성을 구별한다

Michael Nygard의 [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)(2011-11-15)는 당시의 제약·결정·상태·긍정과 부정의 결과를 짧게 남긴다. 바뀐 결정도 대체됐다는 표시와 함께 보존한다. Martin Fowler의 [Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)(2026-03-24)는 결정에 기여한 조언을 요약하고 상세를 별도로 둘 수 있으며, 불확실성과 다시 검토할 조건도 남기도록 설명한다.

**이번 적용 판단:** 현재 맥락 문서는 계속 더 잘 설명하도록 고칠 수 있다. 다만 당시 발언·결정이 바뀐 것처럼 과거 근거까지 덮어쓰지 않고, 변화의 이유와 현재 지위를 구별한다. ADR은 중요한 결정 하나의 기록이므로, 문서의 의도·경험·형성 배경 전체를 ADR 몇 개로 대체하지 않는다. 이 자료는 위키 운영 사례가 아닌 인접한 문서 관리 방식이다.

### 더 살펴봤지만 주된 형식으로 삼지 않을 자료

- Maggie Appleton의 [Colophon](https://maggieappleton.com/colophon): 아이디어를 개인 노트에서 발전시킨 뒤 공개 글로 편집하고, 글의 성숙도를 표시하며 나중에 다시 다듬는다. 의도·판단 과정을 담는 형식보다 문서의 현재 상태를 드러내는 보조 근거다. 과거 Roam 소개를 현재 운영으로 쓰지 않았다.
- Simon Willison의 [비동기 코드 조사](https://simonwillison.net/2025/Nov/6/async-code-research/)(2025-11-06): 질문별 폴더에 코드와 보고서를 남기고 프롬프트·일부 대화 기록을 연결한다. 재확인 가능한 실험 근거의 사례다. 본인이 보고서를 상세히 검토하지 않았다고 밝혔으므로 신뢰할 기준 본문의 완성 사례로 쓰지 않는다.

## 105의 구체화에 주는 영향

아래는 자료에서 얻은 Main의 판단이다. 문서 형식을 새로 확정하지 않는다.

1. **본문 옆 맥락 자료라는 구상을 유지할 근거는 있다.** 특히 Lauren의 rationale과 Gwern의 문서 관계가 직접적이다. 중요한 것은 위치만이 아니라, 현재 결과만 읽어서는 복원하기 어려운 의도·제약·선택 이유를 담는 것이다.
2. **105의 다섯 부분은 작성 질문으로 사용하고 고정 양식으로 굳히지 않는 편이 낫다.** 실제 내용에서는 목적·배경이 한 설명으로 연결될 수도 있다. 대안이나 의도적인 절충이 중요한 본문에는 그 부분을 더 자세히 쓴다.
3. **현재 맥락 설명과 당시 원문은 다르게 관리한다.** 앞쪽 설명은 새 이해에 맞춰 고치되, 필요한 발췌에는 당시 말과 시점을 남긴다. 현재 해석이 달라졌다고 당시 발언을 함께 바꾸지 않는다. 긴 근거가 있을 때만 별도 자료로 분리한다.
4. **실패와 정정만 모으지 않는다.** 처음 무엇을 이루려 했는지, 어떤 가치와 비용을 중요하게 봤는지, 잘 작동해 유지한 판단도 포함한다.105의 이름 기준에서는 코드 자체로 의도를 읽게 하려는 지향과 개인 판단의 역할이 중심이고, A/B 설명의 정정은 그 지향을 명료하게 한 과정이다.
5. **기준을 적용하는 읽기와 기준을 고치는 읽기를 구별한다.** 현재 판단에 필요한 본문은 바로 쓸 수 있어야 한다. 의미가 모호하거나 수정 방향을 정할 때 형성 맥락을 읽고, 그 해석을 확인해야 할 때 원문까지 읽을 수 있게 연결한다. 주변 자료 전체를 매번 읽는 절차는 이 조사에서 도출되지 않는다.

다음에는105의 이름 기준 맥락 초안을 이 관점에서 다듬어, 본문·맥락 설명·필요한 원문의 실제 관계를 한 묶음으로 비교할 수 있다. 이는 후속 추천이며 이번 조사에서 데모를 바꾼 것은 아니다.

## 후속 질문: 이 관계를 실제로 유지할 수 있는가

사용자는 다음을 물었다.

> 하나 더 궁금한게 이런식으로 할때 정말 이 관계나 시스템이 유지 되는것도 중요할텐데 가능할까?

Main의 판단은 **작은 범위에서 운영 가능한 구성이지만, 본문 옆에 자료를 놓는 것만으로 유지가 보장되지는 않는다**는 것이다. 지금 데모에는 형성 맥락 자료가 아직 없으며 장기 유지 효과도 확인하지 않았다. 이 질문을 자동화 구현이나 새 운영 규칙의 채택으로 해석하지 않는다.

### 현재 있는 기반과 없는 부분

[Personal 입구](prototypes/development-workflow/noline-demo/context/personal/README.md)는 개인 기준을 고친 뒤 사용 중인 Work의 영향을 살피고, 제품 요구·작업 비용의 변화는 Project·Work가 맡도록 설명한다. [DEVELOPMENT의 결과 갱신](prototypes/development-workflow/noline-demo/context/work/DEVELOPMENT.md)은 변경 담당자와 Main의 연결 책임을, [Project 관리](prototypes/development-workflow/noline-demo/context/project/MAINTENANCE.md)는 의미가 바뀐 본문과 관련 진입 경로를 대조하는 수동 관리를 이미 둔다. Project 관리 문서를 Personal 전체의 관리자로 확대하지 않는다.

[열람 화면의 검사](prototypes/development-workflow/viewer/README.md)는 원문과 화면의 일치·파일·링크·앵커를 확인하는 범위다. 새 본문–형성 맥락 관계의 누락이나 의미 모순을 이미 검사한다고 볼 수 없다. 현재 없는 것은 그 관계의 명시, 변경 때 읽을 조건, 내용 대조, 실제 변경 상황에서의 운영 확인이다.

### 최소한으로 제안할 유지 방식

| 상황 | 같이 확인할 것 | 고치지 않고 보존할 것 |
| --- | --- | --- |
| 본문의 의도·적용 조건·판단이 달라짐 | 변경 담당자가 관련 맥락을 읽고 새 판단과 예전 이유의 관계를 정리한다. 달라진 현재 설명·사례·진입 경로만 맞춘다. | 당시 발언·근거를 새 결론에 맞춰 고쳐 쓰지 않는다. |
| 새 근거가 기존 이유와 충돌함 | 근거를 지우거나 결론을 자동 변경하지 않고, 실제로 어떤 판단을 다시 검토해야 하는지 드러낸다. | 확인되지 않은 과거 의도를 그럴듯한 설명으로 채우지 않는다. |
| 오탈자·문장 표현만 보완함 | 의미 변화가 있는지만 본다. | 변경 시각을 맞추기 위해 맥락·근거를 일괄 수정하지 않는다. |
| 특정 Project·Work의 조건만 달라짐 | 해당 제품 계약이나 작업 선택을 고치고 Personal의 일반 기준에 영향이 있는지 구별한다. | 개인 기준이나 다른 Project에 자동 전파하지 않는다. |
| 파일 이름·위치가 달라짐 | 본문과 관련 맥락을 찾는 연결 및 화면을 확인한다. | 내용 변경이 없는데 새 결정 이력을 만들지 않는다. |

본문에서 관련 맥락을 찾을 수 있고, 맥락에서 어떤 본문·판단을 설명하는지 알 수 있어야 한다. 처음부터 별도 관계 데이터베이스를 만들기보다 이 작은 연결을 분명히 하는 것을 기본 후보로 삼는다. 본문을 수정한 주체가 같은 작업 안에서 영향도 확인을 맡고, 기존 검토 단계에서 의도와 범위가 보존됐는지 대조한다. 매번 모든 자료를 읽거나 모두 수정하는 절차는 제안하지 않는다.

도구는 끊어진 링크, 이동 뒤 남은 참조, 화면과 원문 불일치 같은 구조 문제를 확인할 수 있다. 본문이 바뀌었는데 관련 맥락을 검토하지 않았을 가능성도 알릴 수 있지만, 이것만으로 맥락이 틀렸다고 판정할 수는 없다. 의미가 여전히 맞는지와 당시 이유를 정확히 복원했는지는 근거를 읽는 판단이 필요하다. 무인 자동 갱신의 정확성을 보장한다고 말하지 않는다.

외부 근거에서도 생성과 유지의 책임이 구별된다. Lauren의 [maintain-verification-skill](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills/maintain-verification-skill/SKILL.md)은 색인·소스·실제 동작을 대조하고, 문서가 틀린 경우와 제품 동작이 잘못된 경우를 구별한다. 그 실제 앱 검증 절차를 글에 그대로 옮길 수는 없지만, 현재 설명과 실제 대상을 다시 대조하는 유지 작업이 필요하다는 참고다. Ryan의 [구조 원칙](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/ARCHITECTURE.md)도 용어 반복보다 실제 판단 변화와 구성의 적정 규모를 요구한다.

### 유지 가능성을 확인할 다음 실험

한 본문 묶음에서 의미 변경, 표현만 변경, 원래 이유와 충돌하는 근거 추가를 각각 가정해 보는 것이 Main의 추천이다. 이전 대화를 모르는 작업자가 관련 맥락을 찾아 필요한 부분만 바꾸는지, 과거 원문을 보존하는지, 불필요하게 Project까지 바꾸지 않는지 확인한다. 본문과 맥락을 일부러 어긋나게 둔 경우도 실제로 발견할 수 있어야 한다. 이는 관계를 유지할 수 있는지에 대한 초기 확인이며 장기 효과의 증거는 아니다.

현재는 이러한 읽기·갱신·확인 조건을 문서 구성과 함께 구체화할 단계다. 자동 hook, 스킬 연결, 정기 점검 실행은 후속 워크플로 작업에서 판단하며 이번 질문으로 구현하지 않았다.

## 확인 범위

세 조사자가 Lauren, 공개 지식 사이트, AI 실무자의 지속 자료 운영을 나눠 조사했다. Main은 핵심 원문의 문서 관계·형식·한계를 다시 읽고 위 적합성을 판단했다. 외부 스킬은 조사 자료로만 읽었으며 실행·설치하지 않았다. pstack과 Ryan 저장소는 고정판을 확인했고, Gwern·Andy·Maggie의 웹 문서는 2026-10-20 열람 상태로 다뤘다. 장기 운영 성과를 별도 실험으로 확인하지 않았다.

이번에는 조사 기록과014의 재진입 안내를 갱신했다.105의 사용자 의도와 제안 지위는 유지한다. 데모 본문·viewer·실행 코드·source·운영 스킬은 변경하지 않았고 추가 커밋도 하지 않았다.
