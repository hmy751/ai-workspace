# 작업물 이해 브리핑의 구조 시각화 보완 분석

## 이 문서의 상태와 질문

이 문서는 Source 02의 영상 reference와 이 폴더의 01·02 분석에서 도출한 합성을 구분해, **어떤 상황에서 어떤 구조 표현이 이해를 도울 수 있고, 어떤 규칙이 새 인지피로와 오해를 만들 수 있는지** 판단하는 연구 근거다.

원자료가 직접 보여 준 것, 이 연구에서 도출한 조건과 반대 설명을 재검토할 때 읽는다. 현재 선택은 [현재 설계](05-current-solution-design.md)가, 실행 계약과 검토 예시는 [v0](v0/README.md)가 소유한다. 아래 분석의 질문·표를 모든 응답에서 수행할 별도 checklist로 적용하지 않는다.

중심 질문은 “작업물 이해 브리핑에 다이어그램을 넣을 것인가”보다 다음에 가깝다.

> 사용자가 현재 질문에서 이해해야 하는 관계를 어떤 경우에 외부 구조로 보여 주고, 그 구조가 실제 source와 근거보다 강한 의미를 만들지 않게 하려면 무엇을 판단해야 하는가?

## 먼저 내리는 결론

구조 시각화는 `work-artifact-briefing`에만 조건부로 보완할 가치가 있다. 하지만 “복잡하면 다이어그램을 넣는다”는 규칙으로는 부족하다.

보완해야 할 것은 다음 세 가지다.

1. **선택 조건:** 문장만으로 관계·분기·상태 변화를 계속 되짚어야 하고, 그 관계를 놓치면 답의 의미가 달라질 때만 구조 표현을 사용한다.
2. **표현의 근거:** 그림의 node뿐 아니라 화살표, 묶음, 방향과 위치도 호출·의존·시간·데이터 이동·소유 관계에 관한 주장으로 취급한다.
3. **선택적 확장:** 전체 architecture를 한 번에 그리지 않고 현재 질문에 필요한 부분 구조에서 시작해, 중요한 부분만 정확한 source·wiring·실행 근거로 내려간다.

따라서 목표는 그림을 더 많이 만드는 것이 아니다. **현재 질문에 필요한 관계만 근거에 맞게 외부화하고, 사용자가 필요한 부분을 선택해 더 확인할 수 있게 하는 것**이다.

## Source 02가 직접 제공하는 재료

### Dependency graph: 표시된 의존 관계와 경계를 보는 지도

발표자는 내부와 일부 외부 dependency를 시각화하고 package와 semantic boundary를 표시하는 도구를 보여 준다고 설명한다. 이 graph를 통해 codebase가 어떻게 변하는지 관찰한다고 말한다. [`dependency graph와 semantic boundary`](../../source/02-bKT2wOec_rg/translation.ko.md#L165)

직접 확인되는 범위는 graph가 표시된 dependency, package, semantic boundary와 그 변화를 보이게 한다는 데까지다. 이 표시를 보고 사람이 더 확인할 관계를 고를 수 있다는 것은 현재 적용을 위한 해석이다. 금지된 dependency를 막고 어디에서 구조가 깨졌는지 찾는 책임은 graph 자체가 아니라 별도의 CLI, CI/CD와 commit history에 있으며, 구조 조건의 기계적 보장도 이 장치들이 맡는다.

발표자가 이 방식으로 architecture가 수렴했고 최근 3~4개월 동안 바뀌지 않았다고 말한 것은 팀의 자기보고다. 이것만으로 좋은 architecture나 사람의 이해 비용 감소가 입증되지는 않는다.

### Code visualization: 의미 구조에서 source로 내려가는 확대 경로

후반 demo에서 발표자는 raw code 대신 시각화된 결과를 보고, 더 넓은 구조를 펼치거나 궁금한 부분만 선택하며, 중요한 경우 연결된 정확한 code line으로 이동한다고 설명한다. 초기화, agent loop와 component 관계 같은 큰 단위를 먼저 알아볼 수 있다는 예를 든다. [`큰 구조·선택적 확장·정확한 code line`](../../source/02-bKT2wOec_rg/translation.ko.md#L391)

이 장면이 직접 제공하는 이동은 다음까지다.

```text
큰 semantic structure
→ 궁금한 부분만 확장
→ 중요한 source line
```

이는 모든 code를 한 깊이로 읽지 않고 사람의 현재 질문에 주의를 배치하는 탐색 방식이다. 현재 01 분석도 이 범위를 direct reference로 남기고 있다. [`직접 말할 수 있는 설명 순서`](01-external-reference-insight-extraction.md#설명-순서에-대해-직접-말할-수-있는-범위)

### Execution trace와 semantic query: 구조 그림과 다른 질문

Execution trace는 특정 실행이 어떤 경로를 지났고 어디에 시간이 쓰였는지를 보여 주는 별도 demo다. [`execution trace`](../../source/02-bKT2wOec_rg/translation.ko.md#L425) Function 설명, source와 사용 위치를 한 번에 제공하는 semantic query도 다시 별도의 demo다. [`설명·source·사용 위치`](../../source/02-bKT2wOec_rg/translation.ko.md#L479)

현재 설명과 근거 기준으로 각 demo의 역할을 해석하면 구조도, source 연결과 실행 trace는 서로 대체할 수 없다.

- 구조도는 표시된 범위의 관계를 보고 더 확인할 부분을 고르게 한다.
- Source와 사용 위치는 그 관계가 현재 code 어디에 있는지 확인하게 한다.
- Trace·log는 특정 조건의 실행에서 실제로 지난 경로를 보여 준다.
- Test는 작성하고 실행한 사례의 결과를, compiler·rule은 표현된 조건의 보장 범위를 보여 준다.

이들을 하나의 AI 응답 순서로 결합하는 것은 영상의 고정 template이 아니라 현재 Workspace의 합성이다. 이 폴더의 02 분석도 `사용자·제품에서의 역할 → 대표 흐름 → component 책임 → source → 실행 근거 → 미완성`이라는 전체 순서를 Source 02·06·08을 함께 사용한 도출로 제한한다. [`장면 3의 근거 강도`](02-three-scenes-reference-synthesis.md#이-설명-순서의-근거-강도)

### 영상에서 직접 가져올 수 없는 것

Source 02는 다음을 직접 입증하거나 규칙으로 제시하지 않는다.

- 모든 AI 브리핑에 다이어그램을 넣으면 이해가 쉬워진다는 보편 효과
- 정적인 Markdown 구조도가 영상의 interactive visualization과 같은 효과를 낸다는 것
- Flow, tree, map과 table을 상황별로 고르는 response 규칙
- 시각화가 실제 이해 시간이나 인지피로를 얼마나 줄였는지에 관한 측정
- BAML 전용 click·zoom UI, typed CLI와 모든 function 독립 실행을 일반 AI 설명에 그대로 옮길 수 있다는 것
- 구조 그림이 현재 runtime 수행이나 invariant 준수를 증명한다는 것

보존된 source에는 한국어 번역문은 있지만 영상 화면 snapshot과 demo의 실제 code·결과가 없다. 따라서 현재 확인한 것은 발표자가 설명한 demo 동작이며, 화면 표현의 충실도나 이해 효과를 독립 검증한 것은 아니다. [`Source 보존 상태`](../../source/02-bKT2wOec_rg/source.md), [`기존 분석의 증거 한계`](../02-bKT2wOec_rg.md#이-영상과-분석의-한계)

## 현재 작업에 옮길 때의 이해 기능

Source 02의 제품 UI를 그대로 흉내 내는 대신, 그 탐색 원리를 대화형 브리핑으로 옮긴다면 다음 순서가 된다.

```text
한 문장 결론과 전체 역할
→ 관계를 놓치기 쉬운 경우에만 질문에 필요한 부분 구조
→ 사용자가 궁금해하는 부분을 선택적으로 확장
→ exact source·사용 위치·wiring
→ 실제 수행이 질문일 때 trace·log·test로 별도 확인
```

`구조를 먼저 보여 준다`는 말은 응답 첫 줄부터 그림을 놓는다는 뜻이 아니다. 현재 skill의 결론 우선 원칙을 유지하고, 결론과 전체 역할 다음에 관계를 설명하는 첫 형상으로 구조를 사용할 수 있다는 뜻이다.

이 구조가 줄일 수 있는 부담은 syntax나 file 이름을 하나씩 기억하는 일이 아니라, 여러 문장을 읽으며 **구성요소 사이의 관계를 사용자가 머릿속에서 다시 조립하는 일**이다. 다만 이것은 Source 02에서 효과가 측정된 결론이 아니라, demo의 탐색 방식과 현재 인지부채 목표를 연결한 작업 가설이다.

## 상황별 선택 판단

구조 표현의 종류는 작업물 종류가 아니라 사용자가 지금 이해해야 하는 관계에 따라 달라진다. 아래 형식 선택은 영상의 직접 규칙이 아니라 현재 적용을 위한 조건부 판단 도움이다.

| 상황 | 구조 표현이 실제로 보여 줄 것 | 사용할 만한 경우 | 피해야 할 오해와 과잉 |
| --- | --- | --- | --- |
| 현재 runtime 흐름 | 입력이 component와 상태 변환을 거쳐 결과·외부 effect가 되는 과정 | 여러 subsystem, 분기, fallback이나 중요한 상태 전환을 문장만으로 되짚어야 할 때 | Source상 가능한 경로를 관찰된 실행으로 보이게 하거나 모든 예외를 한 그림에 넣지 않는다. 대표 wiring인지 trace로 본 실행인지 구분한다. |
| Component·dependency 구조 | 책임 경계, 호출·소비 방향, interface와 실제 provider 관계 | 소유·의존·경계가 질문의 중심일 때 | File tree를 architecture처럼 제시하거나, 많은 edge가 얽힌 전체 graph를 만들거나, source에 없는 layer를 발명하지 않는다. Edge가 call·import·data flow·ownership 중 무엇인지 알 수 있어야 한다. |
| 변경 전후 | 어떤 책임, edge, state나 consumer가 바뀌었는지 | 변경이 한 값이나 이름이 아니라 흐름·책임·연결 구조를 바꿨을 때 | 전체 구조 두 장에서 사용자가 차이를 다시 찾게 하지 않는다. Base·target을 고정하고 유지된 구조보다 바뀐 node·edge를 우선한다. |
| 역사적 작업물 | 당시 의도와 당시 구현의 차이 또는 여러 시점 사이의 변화 | 합의한 흐름과 구현이 갈라졌거나 여러 시점을 구분해야 할 때 | 현재 source·현재 해석을 과거 사실과 합치거나, 보존되지 않은 간극을 선으로 메우지 않는다. 한 시점만 설명하면 timeline을 만들 필요가 없다. |
| 문서·분석·review 결과 | 질문, finding, 근거, 해석과 열린 판단의 관계 | 여러 주장이 서로 의존·반박하거나 여러 Owner의 자료를 함께 봐야 할 때 | 인용을 인과로, reviewer 해석을 확인 사실이나 acceptance로 보이게 하지 않는다. 단순 요약은 짧은 문장이나 표가 더 낫다. |

실행·상태 변화에는 flow, 책임·소유·의존에는 작은 tree나 map, 전후 차이와 정확한 대응에는 delta 표현이나 table을 고려할 수 있다. 이것은 고정 mapping이 아니다. 문장이나 짧은 목록이 더 명확하면 구조도를 만들지 않는다.

## 구조 표현을 선택하기 전에 답해야 할 질문

실제 skill에는 긴 checklist를 출력하게 하지 않되, 다음 판단이 행동 안에 있어야 한다.

1. 사용자가 이해해야 하는 핵심이 개별 사실인가, 여러 요소 사이의 관계인가?
2. 그 관계를 문장으로만 설명하면 사용자가 앞 문장으로 돌아가 구조를 다시 조립해야 하는가?
3. 지금 보여 줘야 하는 관계는 실행 순서, dependency, ownership, 상태 변화, 시간 차이, 주장과 근거 중 무엇인가?
4. 각 화살표와 묶음은 실제로 어떤 관계를 뜻하며 무엇이 이를 뒷받침하는가?
5. 질문에 필요한 부분만 그렸을 때 전체 구조를 다 보여 준 것처럼 오해할 가능성이 있는가?
6. 관계가 명시된 design, current source와 runtime observation 중 무엇으로 확인됐는지 또는 AI가 도출한 grouping인지가 결론을 바꾸는가? 그렇다면 확인 근거와 AI 도출을 구분했는가?
7. 경로가 기본, opt-in, disabled, stub·test-only 중 무엇인지가 결론을 바꾸는가? 그렇다면 활성·완성 상태를 구분하고, 미확인은 근거 한계로 따로 두었는가?
8. 이 구조가 설명을 줄이는가, 아니면 새 기호와 범례를 해독하는 일을 더 만드는가?

한 구조에는 한 관계 질문을 우선한다. 실행 순서, dependency, 역사와 evidence 강도를 한 그림에 모두 담으면 구조화가 아니라 새로운 해독 과제가 된다.

## 그림도 근거가 필요한 주장이다

구조도는 단순한 장식이나 이미 확인된 설명의 중립적 요약이 아니다.

- 화살표는 호출, 시간 순서, 데이터 이동, dependency나 인과를 암시한다.
- 박스 묶음은 responsibility, ownership, layer나 semantic boundary를 암시한다.
- 위아래와 좌우 배치는 선후 관계나 중요도를 암시할 수 있다.
- 빠진 branch는 존재하지 않거나 중요하지 않다는 인상을 줄 수 있다.
- 하나의 직선 흐름은 조건부·비활성·fallback 경로가 없는 것처럼 보일 수 있다.

따라서 node·edge·grouping은 현재 질문의 Owner인 current source·configuration·wiring, runtime observation, 당시 artifact, 명시된 design·decision이나 review evidence처럼 대상에 맞는 원자료에 근거해야 한다. 설명 편의를 위해 AI가 연결하거나 묶은 부분은 확인된 architecture나 관찰 사실처럼 제시하지 않는다. 관련 branch만 보였다면 `현재 질문에 필요한 대표 경로만 표시`처럼 범위를 밝힌다.

설계 의도, current source, runtime observation, test 보장은 기존 공통 기준이 이미 구분한다. 경로의 기본·opt-in·disabled·stub 같은 활성·완성 상태는 이와 다른 축이고, 미확인은 다시 근거 한계다. 시각화 규칙은 이 내용을 모두 범례로 늘어놓지 않고, 어느 차이가 현재 결론의 의미를 바꿀 때만 해당 축을 그림이나 가까운 설명에서 구분해야 한다.

## 대표 형상을 비교한 설계 근거

이 분석 당시 `OUTPUT-PREVIEW.md`의 작업물 이해 브리핑은 `ChatWorkspace`부터 다시 `ChatWorkspace`의 출력까지 13단계를 직선 화살표로 연결했다.

이 흐름은 entry에서 결과까지의 방향을 한 번에 표시하려는 형상이다. 실제로 이해를 더 빠르게 했는지는 확인하지 않았다. 동시에 다음 문제가 있다.

- UI entry, HTTP boundary, use case, retrieval 내부 절차, domain 중간값, certification, API projection과 UI rendering이 같은 크기의 단계로 평평해진다.
- 화살표가 call, data 변환과 시간 순서 중 무엇을 뜻하는지 구분되지 않는다.
- 실제 runtime을 관찰한 trace가 아니라 source와 configuration을 조사한 대표 경로인데, 하나의 실행을 그대로 관찰한 것처럼 보일 수 있다.
- 기본 disabled인 `EntailmentVerdict` 경로는 본문에만 나오므로 기본 흐름과 조건부 경로의 관계를 한눈에 구분하기 어렵다.

분석에서는 먼저 `질문 접수 → 근거 context 구성 → 답변 후보 생성 → 검증과 사용자 상태 확정 → API·UI 표시`처럼 의미 단계 중심의 작은 대표 흐름을 보여 주고, 그 뒤 현재 질문에 중요한 retrieval이나 certification만 source와 함께 펼치는 방향을 제안했다.

당시 반영한 preview는 그림 가까이에 `current source와 기본 configuration에서 확인한 대표 wiring이며 live trace는 아님`이라는 효력 범위를 두었다. Disabled·opt-in 경로는 기본 직선에 섞지 않고 가까운 설명에서 상태를 분리했다. [`반영된 preview`](v0/OUTPUT-PREVIEW.md)

이 대비는 어떤 정보가 첫 구조에 남고 어떤 부분이 상세 설명으로 내려가야 하는지 판단하는 설계 근거다. 현재 preview의 모든 표현이 당시와 같다는 주장이나 실제 사용자 이해 개선을 확인한 결과가 아니다.

## 현재 선택과 과정 기록의 위치

현재는 `work-artifact-briefing`에만 조건부 구조 표현을 두며, 공통 guidance와 다른 두 skill로 확대하지 않는다. 실행 기준은 [브리핑 skill](v0/payload/.agents/skills/work-artifact-briefing/SKILL.md)의 `관계를 구조로 보여 줄 때`가 소유하고, 이름·호출·다른 책임과의 경계는 [현재 설계](05-current-solution-design.md)에서 함께 읽는다. 이 분석 전체를 runtime 입력으로 복제하지 않는다.

사용자의 2026-09-04 반영 결정, 당시 바꾼 대상·유지한 경계와 검사 보고는 [005 품질 검토·수정 경위](../../../workspaces/005-tripproof-cognitive-debt-skill/records/2026-09-06-01-package-quality-review-and-revision-history.md)에 보존한다. 정리 전 이 문서의 상세 변경 경위는 commit `7ece5f407ede82d0955a44f7eac15c0e67ba0162`의 원래 경로 `context/analysis/09-tripproof-cognitive-debt/12-work-artifact-briefing-visual-structure-analysis.md`에서 확인할 수 있다.

구조 표현을 채택했다는 사실과 실제 효과는 다르다. 문서 검사나 작성한 예시만으로 사용자 이해 개선·인지피로 감소를 증명할 수 없으며, 실제 설치·사용 검증은 별도 범위다.
