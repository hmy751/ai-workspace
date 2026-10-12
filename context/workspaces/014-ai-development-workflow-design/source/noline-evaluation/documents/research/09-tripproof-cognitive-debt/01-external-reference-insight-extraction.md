# 외부 reference 재정독: 자료별 인사이트 추출

## 이 문서의 목적

현재 목표는 다음과 같다.

> **AI와 함께 작업하면서 사람이 필요한 이해와 판단을 유지하고, 나중에 다시 복구해야 할 인지부채를 줄이는 방법을 찾는다.**

이 문서는 이 목표와 [`세 사용 장면`](02-three-scenes-reference-synthesis.md)을 기준으로 외부 reference `01`·`02`·`03`·`04`·`06`·`08`의 원문을 다시 읽고, 실제로 재사용할 수 있는 내용을 자료별로 뽑은 분석이다. 자료의 원래 질문, 직접 주장과 관찰, 현재 적용을 위한 합성, 반대 근거와 한계를 함께 소유한다. 이해 복구 순서나 책임자 확인 강도처럼 이 문서에서 이미 도출한 내용도 있으며, 다음 문서가 모든 합성을 처음 만드는 것은 아니다.

이 재추출에서 세 장면은 내용을 적용해 보는 관찰 기준으로 사용했다. TripProof 자체를 분석한 `05`와 `07`은 외부 자료의 인사이트 추출 입력에 넣지 않았다. 그 자료가 제공하는 실제 문제 근거와 기존 Workspace·Project context 기반의 평가는 [`전체 인과와 해결 책임`](03-integrated-causal-map-and-solution-obligations.md)에서 다룬다. 장면별 결합·종료·전환 후보는 [`02`](02-three-scenes-reference-synthesis.md), 현재 채택한 설계와 실행 계약은 각각 [`05`](05-current-solution-design.md)과 [`v0`](v0/README.md)에 있다. 이 문서의 적용 후보 자체를 실행 지시로 사용하지 않는다.

## 읽고 뽑는 방법

기존 analysis부터 요약하면 이전 분석의 질문과 분류가 새 탐색을 미리 제한할 수 있다. 따라서 이번에는 각 source 원문을 먼저 읽고, 대응 analysis는 원문에서 놓친 조건과 과잉 해석을 확인하는 데 사용했다.

인사이트로 남기는 것은 다음 중 하나를 구체적으로 바꾸는 내용이다.

- AI가 먼저 확인할 정보와 사용자에게 물을 판단
- 이해를 위해 선택할 맥락과 근거
- 설명을 구성하고 필요한 부분으로 내려가는 순서
- 사실·해석·미확정·사람의 판단을 나누는 방식
- 사용하지 않아야 할 조건과 새로 생기는 비용

자료 하나를 장면 하나에 통째로 배정하지 않는다. 같은 내용이 여러 장면에 다르게 쓰일 수 있고, 어떤 장면에는 직접 쓸 내용이 없을 수도 있다. 자료마다 도움이 되는 장면과 줄이려는 부담, 보존해야 할 이해·판단, 새 질문·용어·문서·routing 비용, 기존 분석과의 중복·충돌과 비적용 조건을 함께 본다. 원문이 직접 말하거나 보여 준 내용과 현재 목표에 맞춰 도출한 적용은 구분한다. 어느 자료도 이 적용이 사람의 이해나 인지부채를 실제로 개선한다고 직접 비교 측정하지 않았다.

## 01 — 필요한 과거 정보를 고르는 문제

### 원래 질문

이 발표는 장기 실행 agent가 앞선 작업을 잊거나 반복하고 최초 질문에서 벗어나는 `context bloat`와 `context rot`를 다룬다. 핵심 실험은 필요한 정보가 현재 context 밖으로 밀려났을 때 어떤 recall 정책이 최종 답변의 정확도와 비용을 개선하는지 비교하는 것이다. 사람에게 설명하는 방법이나 요구사항 합의가 원래 질문은 아니다. [`01 원문`](../../source/01-yUjTWl7tOYc/translation.ko.md#L7)

### 뽑을 수 있는 내용

1. **필요한 정보가 이미 현재 context에 있으면 과거 자료를 더 불러오는 것이 이득이 아닐 수 있다.**

   원문에서는 문헌 검토에 필요한 모든 정보가 한 context에 들어온 조건에서 memory가 성능을 높이지 못하고 비용만 늘었다. 반대로 답에 필요한 124번째 step의 정보가 500번째 질문 시점에 context 밖으로 밀려난 조건에서는 recall이 필요했다. [`현재 context가 충분했던 조건`](../../source/01-yUjTWl7tOYc/translation.ko.md#L137), [`과거 정보가 필요했던 조건`](../../source/01-yUjTWl7tOYc/translation.ko.md#L181)

   현재 목표에는 다음처럼 적용할 수 있다. 작업 시점만 보고 과거 기록을 자동으로 불러오지 않고, 지금 이해하거나 결정할 질문에 필요한 정보가 실제로 빠졌는지 먼저 본다. 현재 대화와 현재 artifact로 답할 수 있다면 history를 추가하지 않는다. 이는 발표의 실험 결과를 대화의 정보 선택에 옮긴 도출이다.

2. **중요한 것은 memory 사용 여부보다 현재 질문에 맞는 정보를 우선해서 가져오는 일이다.**

   원문은 no-memory, vector RAG, turn별 decision ledger, 정답 memory를 알려 주는 oracle 등을 비교했고, 보존된 결과에서는 ranked ledger가 가장 좋았다고 보고한다. [`비교 조건`](../../source/01-yUjTWl7tOYc/translation.ko.md#L107), [`순위 기반 recall 결과`](../../source/01-yUjTWl7tOYc/translation.ko.md#L201)

   현재 장면에서는 단어가 비슷하거나 최근이라는 이유만으로 과거를 가져오기보다, 현재 질문을 구속하는 사용자 결정, 지금도 유효한 제약, 현재 결과를 직접 만든 전환점만 우선하는 근거가 된다. 이 우선순위 자체는 원문이 검증한 ranking 공식이 아니라 현재 목표에 맞춘 적용이다.

3. **정확한 정보를 찾은 것과 그 정보를 실제 답에 사용한 것은 다르다.**

   Oracle이 정확한 memory를 주어도 model이 무시하거나 다른 정보를 선택하거나 혼란스러워할 수 있었다. [`oracle의 한계`](../../source/01-yUjTWl7tOYc/translation.ko.md#L217) 따라서 과거 결정이나 코드 위치를 정확히 찾았다는 사실만으로 설명이 완성되지는 않는다. 현재 적용에서는 `확인한 사실 → 그 사실이 현재 상황에 미치는 의미 → 지금 질문에 대한 결론`을 이어 주어야 한다. 이 연결 방식은 원문에서 직접 제시한 설명 형식은 아니다.

4. **관련 없는 과거 정보는 중립적인 배경이 아니라 비용과 오판 원인이 될 수 있다.**

   발표자는 나쁜 memory가 token 비용을 늘리고 agent를 잘못된 방향으로 보낼 수 있다고 말한다. [`나쁜 memory의 비용`](../../source/01-yUjTWl7tOYc/translation.ko.md#L251) 사람의 이해를 돕겠다는 이유로 전체 대화, 모든 대안, 모든 파일을 먼저 보여 주면 현재 질문이 흐려질 수 있다는 경계로 사용할 수 있다.

### 세 장면에서의 쓰임

- **장면 1:** 이전 대화가 길 때 이미 확정된 결정과 아직 미정인 선택만 선별해 복구하는 데 조건부로 쓸 수 있다. 어떤 질문을 어떤 순서로 해야 하는지는 이 자료가 제공하지 않는다.
- **장면 2:** 이해가 끊긴 문장에 실제로 필요한 전제만 고르는 데 쓸 수 있다. 쉬운 설명이나 누락된 논리를 복구하는 방법은 제공하지 않는다.
- **장면 3:** 현재 구현은 현재 source에서 보고, 과거 결정은 “왜 이렇게 되었는가”에 필요할 때만 가져온다는 정보 선택 원리로 쓸 수 있다. 코드 구조 설명법 자체는 제공하지 않는다.

### 가져오지 않을 것과 한계

- Memory를 `쓰기 → 관리 → 읽기` loop로 본 설명은 유용하지만, 이번 작업에서 새 memory system이나 decision ledger를 만들 근거는 아니다. [`memory loop`](../../source/01-yUjTWl7tOYc/translation.ko.md#L67)
- 실제 비교에서 바꾼 것은 주로 recall block이며 write·manage 정책 전체, 최신성·충돌 관리의 효과를 검증한 것은 아니다. [`기존 분석의 한계`](../01-yUjTWl7tOYc.md#L119)
- 질문 수와 사용 model은 보고됐지만 raw score, 효과 크기와 통계적 유의성은 보존 자료에 없다.
- 정확한 recall이 사람의 이해·동의·판단을 만든다는 증거는 없다.

01은 사람의 인지부채보다 장기 agent recall이 중심이어서 직접 쓰임이 작다. 필요한 정보가 없어서 판단하지 못한 경우와 정보는 있지만 의미를 이해하거나 적용하지 못한 경우를 구분하는 데 쓰며, **현재 질문에 필요한 과거가 실제로 빠졌을 때만, 관련성이 높은 최소 정보부터 가져온다**는 제한된 원리를 남긴다.

## 02 — 모든 code line 대신 system의 의미와 근거를 보는 문제

### 원래 질문

발표는 code review를 하지 않고 여러 AI 작업을 병렬로 수행하면서도 쉽게 되돌릴 수 없는 programming language를 어떻게 안정적으로 만들 수 있는지 묻는다. 후반에는 모든 code를 읽지 않을 때 사람이 system을 어떻게 이해할 수 있는지로 질문을 옮긴다. [`발표의 출발점`](../../source/02-bKT2wOec_rg/translation.ko.md#L9), [`system 이해 질문`](../../source/02-bKT2wOec_rg/translation.ko.md#L373)

### 뽑을 수 있는 내용

1. **도구 사용법보다 오래 유지할 구조적 경계를 작게 둔다.**

   발표자의 `architecture.md`에는 특정 AI 도구 지침이 아니라 몇 달·몇 년 동안 바뀌지 않을 compiler layer와 허용된 통신 방향만 둔다. [`작은 장기 architecture`](../../source/02-bKT2wOec_rg/translation.ko.md#L77) 장면 1에서는 모든 내부 구조를 미리 정하는 대신 이번 작업이 넘으면 안 되는 경계나 반드시 지킬 조건만 확인하는 근거가 된다. 장면 3에서는 이 문서를 **의도된 안정 경계**로 읽되, 현재 component 관계와 실제 위반 여부는 dependency graph·현재 source·검사 결과에서 별도로 확인해야 한다. [`현재 관계와 위반 검사`](../../source/02-bKT2wOec_rg/translation.ko.md#L165)

2. **문서는 생성됐다는 사실보다 실제로 읽히고 판단에 사용되는지가 중요하다.**

   Design document 생성이 쉬워지자 하루에 여러 문서가 생겨 다시 읽히지 않는 자료가 되었고, 발표자는 배포 전에 다른 사람이 실제로 읽게 하는 조건을 붙였다고 말한다. [`문서 생성과 읽기`](../../source/02-bKT2wOec_rg/translation.ko.md#L101), [`읽히지 않는 문서 문제`](../../source/02-bKT2wOec_rg/translation.ko.md#L141) 따라서 작업 논의나 설명이 문서 자동 생성으로 끝나서는 안 되며, 이후 누가 읽고 어떤 판단에 쓸지 없는 문서는 오히려 새 부담이 될 수 있다.

3. **의미 구조에서 출발해 필요한 source로 선택적으로 내려간다.**

   원문 demo는 visualization에서 초기화, agent loop, component 관계 같은 큰 구조를 먼저 보여 준다. 사용자는 궁금한 부분만 펼치고 중요한 경우에만 연결된 정확한 code line으로 내려간다. [`semantic structure와 선택적 확장`](../../source/02-bKT2wOec_rg/translation.ko.md#L391) 모든 line을 같은 깊이로 읽기보다 사람의 현재 질문과 판단 지점에 주의를 배치하는 방식이다.

   원문이 직접 보여 주는 탐색 대상과 도구는 서로 나뉜다. Dependency graph에는 package와 semantic boundary가 나타나고, 별도의 function query는 설명·source·사용 위치를 함께 보여 주며, 다시 별도의 demo에서는 function을 독립 실행한다. [`dependency와 semantic boundary`](../../source/02-bKT2wOec_rg/translation.ko.md#L165), [`function 설명·source·사용 위치`](../../source/02-bKT2wOec_rg/translation.ko.md#L479), [`function 독립 실행`](../../source/02-bKT2wOec_rg/translation.ko.md#L537) 원문이 function을 하나의 `semantic unit`으로 정의하거나 이 속성을 하나의 계약으로 묶은 것은 아니다. `사용자 workflow`, `상태 변화`, `외부 effect`를 의미 단위로 삼는 것도 이 자료와 08을 현재 목표에 맞춰 합친 후속 도출이다.

4. **실제 동작에 관한 질문은 실행 근거로 내려간다.**

   발표자는 실행 trace로 어떤 경로가 지나갔고 어디에서 시간이 쓰였는지 본다. Function을 전체 application 없이 독립 실행하는 구상도 별도로 보여 준다. [`execution trace`](../../source/02-bKT2wOec_rg/translation.ko.md#L425), [`function 독립 실행`](../../source/02-bKT2wOec_rg/translation.ko.md#L537) 따라서 “무슨 code가 있는가”와 “이번 실행에서 실제로 무슨 일이 일어났는가”를 같은 설명으로 합치지 않는 근거가 된다.

5. **설계 의도, 현재 source, 관찰된 실행과 기계가 보장하는 조건은 서로 다른 근거다.**

   원문은 문서나 설명이 실제 code와 달라질 수 있다고 경고하고, error type 전파와 compiler의 미처리 오류 검사를 별도로 보여 준다. [`문서와 code의 차이`](../../source/02-bKT2wOec_rg/translation.ko.md#L505), [`compiler가 확인한 조건`](../../source/02-bKT2wOec_rg/translation.ko.md#L619) 이를 현재 설명에 적용하면 다음을 나눠야 한다.

   - 설계 문서에서 확인한 의도
   - source에서 확인한 현재 구현
   - trace·test에서 관찰한 특정 실행
   - compiler·rule check가 표현된 범위에서 보장하는 조건
   - AI가 위 자료를 연결해 도출한 해석

   이 구분은 여러 도구가 서로 다른 질문에 답한다는 원문을 바탕으로 만든 설명 방식이며, 발표자가 그대로 제시한 response template은 아니다.

6. **검토는 사라지는 것이 아니라 다른 위치로 이동한다.**

   Agent 실행 기록과 문제 후보는 다른 agent가 검토할 수 있지만, 사람과 agent가 함께 실제 문제·hallucination·taste 차이를 구분한다. 기능 대안은 tool call, error, 정확도 같은 선택된 지표로 비교한다. [`agent 결과와 사람의 구분`](../../source/02-bKT2wOec_rg/translation.ko.md#L217), [`A/B 비교`](../../source/02-bKT2wOec_rg/translation.ko.md#L251) 모든 code line 검토를 줄여도 구조·측정 기준·이상 징후에 대한 사람의 판단은 남는다는 근거다.

### 세 장면에서의 쓰임

- **장면 1:** 오래 유지할 경계, 되돌리기 어려운 설계와 무엇을 측정할지 정하는 작업에 제한적으로 쓸 수 있다. 모호한 사용자 의도를 질문으로 끌어내는 대화법은 없다.
- **장면 2:** 직접적인 이해 복구법은 없다. Code에 관한 응답이 이해되지 않는다면 표현만 바꾸지 말고 실제 source와 실행 근거로 내려가야 한다는 보조 원리만 제공한다.
- **장면 3:** 가장 직접적이다. 큰 의미 구조를 먼저 보고, 필요한 부분만 펼치고, source·사용 위치·실행 근거로 내려가며 각 근거가 말할 수 있는 범위를 분리하는 방식으로 쓸 수 있다.

### 설명 순서에 대해 직접 말할 수 있는 범위

원문이 하나의 demo 안에서 직접 연결해 보여 주는 탐색 이동은 다음까지다.

```text
큰 semantic structure
→ 궁금한 부분만 확장
→ 중요한 source line
```

Trace, 설명·source·사용 위치를 묶는 query, function 독립 실행은 각각 별도의 demo다. 이들을 위 이동 뒤에 놓아 하나의 설명 순서로 만드는 것부터 현재 합성이다. 발표자는 어느 조합도 AI가 사람에게 설명할 때 지켜야 하는 고정 목차로 규정하지 않는다. `사용자 흐름 → component 책임 → 상태 변화 → source → 실행 증거` 같은 구체적인 설명 순서는 02의 여러 demo와 08의 end-to-end 결과를 조합해 현재 작업에서 도출해야 한다.

### 가져오지 않을 것과 한계

- BAML이나 특정 visualization을 필수 해결책으로 채택하지 않는다. 의미 단위 설명이 code review를 대체하거나 없앤다는 효과도 이 자료로 입증되지 않는다.
- Visualization이 실제 code에 없는 의미 경계를 사후에 만들어 주지는 않는다. 구조가 흐리면 보기 좋은 그림이 오해를 강화할 수 있다.
- Trace는 실행된 경로를 보여 줄 뿐 실행되지 않은 모든 경로를 보장하지 않는다.
- Compiler 보장은 type system에 표현된 조건에 한정되며 제품 요구의 타당성을 입증하지 않는다.
- “Code가 진실의 원천”이라는 표현은 현재 구현을 확인하라는 강한 경계로는 쓸 수 있지만 runtime 설정, 외부 system, stale build까지 code 하나가 모두 설명한다는 뜻으로 확대하지 않는다.
- 보존 번역에는 화면에 나온 일부 TypeScript 예제와 BAML demo의 실제 code·결과가 빠져 있다. 현재 확인한 것은 발표자의 설명이며 visualization의 표현 충실도와 trace 결과를 독립 검증한 것이 아니다.
- 발표는 BAML 제작자의 팀 경험과 제품 demo다. Architecture 안정성, trace 비용과 생산성은 외부 비교가 없고 사람의 이해 복구 시간도 측정하지 않았다. [`기존 분석의 한계`](../02-bKT2wOec_rg.md#L148)

## 03 — 질문 순서와 이해 복구를 여러 작은 개입으로 나눈 사례

### 원래 질문

이 발표는 하나의 인지부채 해결법이 아니라 여러 AI coding skill의 release tour다. 작업 전 질문의 속도와 선후관계, AI 설명이 들어오지 않는 순간, 사람이 절차를 기억해야 하는 부담, 실제 답을 가진 사람이 현재 대화 상대가 아닌 상황을 서로 다른 개입으로 나눈다. [`작업 전 질문 문제`](../../source/03-sZrFaPMau6A/translation.ko.md#L219), [`설명 이해 실패`](../../source/03-sZrFaPMau6A/translation.ko.md#L121)

### 뽑을 수 있는 내용

1. **작업 논의는 spec보다 앞설 수 있고, 질문은 선행 결정이 끝난 것만 작은 묶음으로 묻는다.**

   소개된 흐름은 `Grill with Docs → Spec → Implement → Code Review`이며, 현재 답할 수 있는 여러 쉬운 질문은 함께 묻되 다음 질문을 좌우하는 핵심 질문은 먼저 하나만 물을 수 있다. [`논의가 spec보다 앞선 흐름`](../../source/03-sZrFaPMau6A/translation.ko.md#L27), [`질문 의존관계와 작은 round`](../../source/03-sZrFaPMau6A/translation.ko.md#L291) 번호와 추천안은 scanning과 음성 응답 비용을 줄이기 위한 장치다. [`응답 비용을 줄이는 형식`](../../source/03-sZrFaPMau6A/translation.ko.md#L317)

   대응 analysis는 여기서 codebase가 답할 사실은 AI가 조사하고, 선택과 trade-off만 사용자에게 묻는 역할 분리를 도출한다. [`사실 조사와 사용자 결정`](../03-sZrFaPMau6A.md#L93)

2. **이해 실패는 짧은 답을 요구하는 문제가 아니라 listener가 맥락을 놓쳤다는 신호다.**

   `Wait What`의 원 장면은 AI의 말이 중요해 보이지만 뜻을 모르겠는 상태다. 다시 설명할 때 Simplified Technical English뿐 아니라 앞선 논의에서 사용자가 만든 project language를 사용한다. [`이해하지 못한 상태`](../../source/03-sZrFaPMau6A/translation.ko.md#L141), [`명확한 문장과 기존 project language`](../../source/03-sZrFaPMau6A/translation.ko.md#L175)

   현재 적용에서는 이해가 공유됐던 마지막 지점까지 돌아가 새 용어, 빠진 전제, 논리 도약과 과잉 압축 가운데 막힘의 원인을 찾고, 사용자가 이미 아는 말로 전제와 결론의 연결을 복구하는 방식이 된다. **이 진단 순서 전체가 source 사례를 현재 장면에 맞춰 구체화한 도출**이며, source는 별도의 이해 확인 방법도 제시하지 않았다.

3. **답의 소유자가 누구인지에 따라 질문을 routing한다.**

   발표 원문은 외부 사람만 답할 수 있는 질문을 questionnaire로 보내는 사례를 보여 준다. [`외부 답변자가 필요한 상황`](../../source/03-sZrFaPMau6A/translation.ko.md#L523) Codebase·현재 환경이 답할 사실과 사용자가 정할 선택을 나누는 것은 이 사례와 각 skill 계약을 교차한 기존 analysis의 도출이다. [`사실·선택·외부 답변의 분리`](../03-sZrFaPMau6A.md#L93) 현재 장면에서는 설명을 반복하기 전에 실제 막힘이 표현 문제인지, 현재 code를 조사해야 하는지, 사용자나 다른 책임자의 선택이 필요한지 구분하는 근거로 쓴다.

4. **대화, 용어, 결정, 질문과 절차는 같은 수명과 저장 책임을 갖지 않는다.**

   대응 analysis는 여러 skill을 비교하면서 session 안의 이해 복구, 여러 단계가 참조할 용어·결정, 외부 답변을 기다리는 질문과 반복 절차를 한 덩어리로 저장하지 말아야 한다고 지적한다. [`context 수명과 artifact 경계`](../03-sZrFaPMau6A.md#L223) 이는 source의 개별 skill 구조를 함께 읽은 분석의 도출이며, 발표가 하나의 보편 저장 schema로 제안한 내용은 아니다.

### 세 장면에서의 쓰임

- **장면 1:** 강하다. 현재 답할 수 있는 결정만 작은 round로 묻고, 환경에서 확인할 사실과 사용자가 정할 trade-off를 나누는 근거를 제공한다.
- **장면 2:** 가장 강하다. 사용자의 기존 context와 project language에서 다시 출발하고 누락된 전제를 보충하는 직접 사례를 제공한다.
- **장면 3:** 구조 설명법은 제공하지 않는다. 실제 답이 codebase에 있으면 조사로 보내고, 조사한 설명이 어렵다면 장면 2로 복구한다는 경계만 제공한다.

### 가져오지 않을 것과 한계

- 추천 답변은 응답 비용을 낮추지만 AI 제안에 사용자를 고정할 수 있다.
- 중요하지 않은 작업까지 질문하면 작업 전 논의가 새 피로가 된다.
- 친숙한 용어로 재설명됐다고 설명 내용이 사실인 것은 아니다. 오래되거나 잘못된 project language는 오해를 더 자연스럽게 만들 수 있다.
- 반복 설명이 실패하면 문체가 아니라 용어 합의, 선행 결정 또는 문제 정의가 잘못됐을 수 있다.
- 질문·결정을 외부화하면 답변자·시점·불확실성이 전달 중 사라지거나, 저장된 내용을 필요한 순간에 발견하고 갱신하는 부담이 생길 수 있다. 자동 routing이나 파일 생성만으로 이 책임이 해결됐다고 보지 않는다.
- `Wait What` 뒤 실제 이해도가 좋아졌다는 측정은 없다. [`기존 분석의 증명 한계`](../03-sZrFaPMau6A.md#L248)

## 04 — Matt Pocock의 네 개별 skill 자료

### 자료의 지위

`teach`, `grill-with-docs`, `wait-what`은 사람용 설명 문서이고 `code-review`만 실제 `SKILL.md`로 보존됐다. 설명 문서에는 설계 의도, 사용자 보고와 미해결 문제가 함께 들어 있다. 네 자료는 하나의 인지부채 해결 세트가 아니라 서로 다른 목적의 도구다. [`자료의 provenance와 한계`](../04-matt-pocock-skills.md#L8)

### `grill-with-docs`: 작업 전 논의

1. **Spec은 선행조건이 아니라 가능한 후속 산출물이다.**

   이 도구는 change 시작 때 plan·design·용어가 흐린 상태를 사람과 AI의 shared understanding으로 만들고, 필요하면 이후 spec으로 넘긴다. 작은 change는 곧바로 구현할 수도 있다. [`원래 역할과 사용 범위`](../../source/04-matt-pocock-skills/original/grill-with-docs.md#L1), [`spec 또는 구현으로 이동`](../../source/04-matt-pocock-skills/original/grill-with-docs.md#L66)

   원문 범위는 사용자가 직접 호출하고 한 session 안에서 정할 수 있는 change다. 더 큰 effort는 별도 흐름으로 보낸다. [`호출과 규모의 전제`](../../source/04-matt-pocock-skills/original/grill-with-docs.md#L7) 장면 1을 더 넓은 작업 논의에 쓰는 것은 현재 합성의 확장이며, 사용자 발동을 기본으로 두는 편이 원문과 가깝다.

2. **Codebase가 답할 사실은 AI가 조사하고, 사용자는 선택과 trade-off를 판단한다.**

   원문은 code에서 답을 찾을 수 있는 질문을 사용자에게 되묻지 말라고 한다. [`codebase 사실 조사`](../../source/04-matt-pocock-skills/original/grill-with-docs.md#L72) 질문 의존관계를 AI가 추적하고 현재 답할 수 있는 결정만 작은 round로 묻는다면 사용자가 전체 질문 tree와 code 사실을 동시에 들고 있을 필요가 줄어든다.

3. **모든 대답을 지속 문서로 만들지 않는다.**

   Project term은 glossary, 맥락 없이 놀랍고 되돌리기 어려운 실제 trade-off는 ADR, 나머지는 conversation에 남긴다. [`선별 기록`](../../source/04-matt-pocock-skills/original/grill-with-docs.md#L29) 현재 작업에서는 이 구체적인 파일 구성을 그대로 복제하기보다, 나중에 다시 유도하는 비용이 큰 내용만 기존 Owner에 넘긴다는 원리로 사용할 수 있다.

4. **좋은 대화와 정확한 후속 전달은 별도 성공 조건이다.**

   원문에는 여러 writer가 동시에 쓰며 생긴 drift, dependency가 부분적으로만 load되어 interview는 됐지만 기록은 빠진 문제, ordering·negative·numeric 조건이 후속 spec에서 약해진 문제가 함께 보고된다. [`writer와 dependency 문제`](../../source/04-matt-pocock-skills/original/grill-with-docs.md#L43), [`후속 전달 손실`](../../source/04-matt-pocock-skills/original/grill-with-docs.md#L54) 대화가 잘 됐다는 사실이 다음 단계에 조건이 정확히 전달됐다는 뜻은 아니다.

### `wait-what`: AI 응답 이해 복구

1. **출력 길이 대신 listener의 상태를 알린다.**

   `concise`나 `tl;dr`처럼 출력을 지정하면 문맥까지 잘릴 수 있다. “당신이 나를 놓쳤다”는 신호는 AI가 무엇이 이해를 끊었는지 보고 필요한 만큼 뒤로 돌아가게 한다. [`listener 상태와 rewind`](../../source/04-matt-pocock-skills/original/wait-what.md#L13)

2. **쉬운 단어 치환이 아니라 빠진 context와 기존 project noun을 복구한다.**

   원문은 방금 말을 다시 pitch할 때 누락된 context를 더하고, plain language와 앞서 합의한 project vocabulary를 사용하라고 한다. [`핵심 동작`](../../source/04-matt-pocock-skills/original/wait-what.md#L1), [`설명 register와 project noun`](../../source/04-matt-pocock-skills/original/wait-what.md#L21)

3. **한 문단만 다시 쓰지 않고 실제로 사용자를 놓치게 한 범위까지 돌아간다.**

   대상은 last message의 고정 구간이 아니다. AI가 무엇이 listener를 잃게 했는지 보고 얼마나 뒤로 갈지 정한다. [`되돌아갈 범위`](../../source/04-matt-pocock-skills/original/wait-what.md#L19)

원문 skill은 장황함을 다시 만들지 않도록 핵심 지시를 일부러 세 줄로 유지한다. [`의도적으로 짧은 지시`](../../source/04-matt-pocock-skills/original/wait-what.md#L3) 현재 장면 2에는 `진행 중단 → 마지막으로 공유된 이해와 막힌 유형 확인 → 기존 용어로 대응 → 빠진 전제와 중간 논리 복원 → 남은 막힘 확인`으로 적용할 수 있지만, **이 전체 순서가 여러 자료를 합친 현재 도출**이다. 매번 사용자에게 긴 목차로 노출하지 않고 실제 막힘에 필요한 동작만 골라야 한다.

### `teach`: 지금 이해하는 것과 오래 학습하는 것의 경계

1. **읽는 순간 익숙하게 느끼는 것과 나중에 스스로 꺼내 쓰는 능력은 다르다.**

   `teach`는 learning 자체가 project일 때 실제 mission, resource, lesson, reference와 learning record를 여러 session에 유지한다. 한 번의 설명은 현재 session에서 묻고, 방금 message가 들어오지 않은 경우는 `Wait What`을 사용하라고 분리한다. [`학습 project와 일회성 설명의 구분`](../../source/04-matt-pocock-skills/original/teach.md#L1)

2. **처음 이해할 때와 이해한 뒤 연습할 때 필요한 난이도가 다르다.**

   원문은 처음 knowledge를 이해할 때 불필요한 difficulty를 낮추고, 이해한 뒤에는 retrieval practice와 feedback을 사용한다. [`이해와 연습의 순서`](../../source/04-matt-pocock-skills/original/teach.md#L40) 따라서 장면 2에 quiz와 장기 학습 구조를 기본으로 넣지 않는다. 반복 재설명이 실제 domain 학습 부족 때문에 실패할 때만 별도 학습으로 이동할 수 있다.

3. **장기 codebase orientation에는 조건부로 쓸 수 있다.**

   낯선 codebase를 여러 session에 걸쳐 실제로 익히는 사용례가 보고된다. [`codebase orientation`](../../source/04-matt-pocock-skills/original/teach.md#L76) 장면 3이 한 번의 구조 설명이 아니라 지속 학습을 명시적으로 요구할 때만 관련된다.

### `code-review`: 이해 설명과 적합성 판정을 나누는 경계

1. **먼저 비교할 fixed point와 diff 범위를 고정한다.**

   실제 skill은 ref가 resolve되고 diff가 비어 있지 않은지 확인한 뒤 review한다. [`review 범위 고정`](../../source/04-matt-pocock-skills/original/code-review.SKILL.md#L17)

2. **Repository 기준과 originating spec 충족을 별도 축으로 본다.**

   Spec이 없으면 `no spec available`을 남기며 pass로 추측하지 않고, 두 reviewer의 finding을 하나의 인상이나 ranking으로 합치지 않는다. [`spec 부재 처리`](../../source/04-matt-pocock-skills/original/code-review.SKILL.md#L25), [`판정축 분리`](../../source/04-matt-pocock-skills/original/code-review.SKILL.md#L74)

장면 3에서는 “무엇이 바뀌고 어떻게 작동하는가”를 이해하는 설명과 “요구·repository 기준에 맞는가”를 판단하는 review를 구분하는 경계만 가져온다. 이 skill 자체는 구조·흐름을 설명하는 도구가 아니다.

### 04 전체의 쓰임과 한계

- **장면 1:** `grill-with-docs`가 직접적이다. `teach`는 사용자가 결정할 문제가 아니라 먼저 배워야 할 지식 때문에 막혔는지 구분하는 데만 조건부로 쓴다.
- **장면 2:** `wait-what`이 직접적이다. `teach`는 즉시 이해와 지속 학습을 구분한다.
- **장면 3:** 전용 구조 설명기는 없다. `teach`의 장기 orientation, `code-review`의 범위·판정축 분리, `grill-with-docs`의 domain vocabulary만 조건부로 쓸 수 있다.

추천안은 anchoring을 만들 수 있고, glossary는 stale해질 수 있으며, 학습 workspace와 여러 artifact는 그 자체로 관리 비용을 만든다. Citation, quiz, 파일 생성과 reviewer 결과는 실제 학습·정확성·이해를 자동으로 증명하지 않는다. [`네 자료의 공통 증명 한계`](../04-matt-pocock-skills.md#L180)

## 06 — 실행을 위임하면서 사람의 판단을 유지하는 문제

### 원래 질문

발표는 AI가 실제 작업을 점점 더 많이 수행할 때 사람이 무엇을 계속 이해하고 판단해야 주도권을 잃지 않는지 묻는다. 선택 자료 중 인지부채의 상위 문제를 가장 직접적으로 다루므로 공통 판단축으로 사용한다. 사람의 역할을 모든 code를 직접 쓰고 읽는 것으로 두지 않고, 할 가치가 있는 일의 선택, 결과를 이해할 근거, 위험 수용과 방향 전환, 그 판단을 설명하고 결과에 답할 수 있는 상태에 둔다. [`사람에게 남는 역할`](../../source/06-wHePopfD6js/translation.ko.md#L13), [`quality·판단·설명 책임`](../../source/06-wHePopfD6js/translation.ko.md#L39)

### 뽑을 수 있는 내용

1. **Evidence와 사람의 최종 판단은 다른 산출물이다.**

   원문은 diff, test, log, reasoning, trace, trajectory와 screenshot을 판단에 필요한 evidence의 예로 들지만, 승인·차단·방향 전환과 위험 수용은 이후 사람의 outer loop에 남긴다. [`판단 근거의 예`](../../source/06-wHePopfD6js/translation.ko.md#L801)

   현재 설명에는 `확인된 사실`, `그 사실에서 AI가 도출한 해석`, `남은 미확정`, `판단 책임자가 실제로 정할 것`을 구분하는 방식으로 적용할 수 있다. 대화 중인 사용자가 그 판단의 책임자일 때만 마지막 선택을 사용자에게 올리고, team·기관·다른 담당자가 책임자라면 그 주체를 분명히 해야 한다. 원문도 결과 뒤의 책임 주체가 개인·team·기관일 수 있음을 전제한다. [`책임 주체의 범위`](../../source/06-wHePopfD6js/translation.ko.md#L663) 이 구분 형식은 원문이 제시한 template이 아니라 evidence와 verdict, 즉 사람의 최종 판단을 나눈 데서 도출한 것이다.

2. **사람을 모든 step에 넣기보다 판단 효과가 큰 시점에 둔다.**

   Harness와 반복 loop가 실행을 확장해도 production 결정은 사람이 하고, 사람의 판단을 leverage 높은 checkpoint로 옮기는 것이 이점이라고 말한다. Agent는 정한 policy 안에서 routing·merge·escalation을 할 수 있지만 실행과 책임은 구분된다. [`사람의 checkpoint`](../../source/06-wHePopfD6js/translation.ko.md#L113), [`실행과 책임`](../../source/06-wHePopfD6js/translation.ko.md#L685)

   장면 1에는 코드와 자료에서 확인할 사실까지 모두 묻지 않고, 결과를 실제로 갈라놓는 가치·위험·품질 선택만 **해당 판단의 책임자**에게 올리는 근거가 된다. 모든 turn에 이해 확인과 승인 절차를 붙이는 방식은 오히려 발표가 경고한 orchestration cost를 키울 수 있다.

   원문이 시간 면에서 직접 대비한 것은 작업 전·중·후가 아니라 30초짜리 interaction과 한 시간·하루짜리 workstream, 그리고 여러 병렬 workstream이다. [`짧은 interaction과 긴 workstream`](../../source/06-wHePopfD6js/translation.ko.md#L517) 세 장면에 checkpoint를 배치하는 것은 현재 도출이며, 확인 강도는 작업 지속시간·위임 깊이·병렬성에 따라 달라져야 한다.

3. **Build·test·merge된 결과도 사람이 이해하지 못한 채 다음 판단의 기반이 될 수 있다.**

   원문은 repository의 code와 사람이 실제로 이해할 수 있는 code 사이의 간극을 cognitive debt라고 부르고, 동작하는 PR이 있어도 팀이 배포 system을 설명할 능력을 잃을 수 있다고 말한다. [`성공한 결과에 남는 이해 간극`](../../source/06-wHePopfD6js/translation.ko.md#L487) 따라서 장면 3은 test pass를 반복하는 완료 보고가 아니라 결과의 목적·구조·동작·제약·확인 범위를 복구해야 한다.

4. **이해하지 못한 AI 결론을 그대로 자기 판단으로 받아들이지 않는다.**

   원문은 delegation을 “작업하고 내가 판단할 만큼 충분한 evidence를 보여 달라”는 상태로, cognitive surrender를 자기 의견을 만들기 전에 AI 답을 자기 답으로 받아들이는 상태로 구분한다. [`delegation과 cognitive surrender`](../../source/06-wHePopfD6js/translation.ko.md#L541) 장면 2에서 사용자가 이해를 요청한 순간에는 승인이나 다음 선택을 재촉하지 않고, 결론·근거·추론·미확정을 풀어 사용자가 별도 판단을 만들 수 있게 해야 한다.

5. **정성적 판단은 실제 critique와 example로 풀 수 있다.**

   발표자는 객관적 metric이 없는 상황의 판단을 신비한 직감으로 남기지 않고 critique와 example로 표현해야 다른 사람과 system이 배울 수 있다고 말한다. [`critique와 example`](../../source/06-wHePopfD6js/translation.ko.md#L331) 장면 1에서 사용자가 “이 느낌은 싫다”고 말하면 곧바로 추상 규칙으로 굳히기보다 실제 예시의 차이, 싫은 이유와 판단이 달라질 조건을 확인하는 방식으로 적용할 수 있다.

6. **설명할 수 있다는 것은 모든 line을 읽었다는 뜻이 아니다.**

   `Explain it or don't ship it`은 모든 line을 직접 작성하거나 읽으라는 뜻이 아니라 누군가 변경을 방어하고 설명할 만큼 충분히 이해해야 한다는 주장이다. [`설명 가능성과 line-by-line 검토의 차이`](../../source/06-wHePopfD6js/translation.ko.md#L873) 장면 3의 설명 깊이를 모든 구현 세부가 아니라 다음 판단의 영향과 실패 위험에 맞추는 근거로 쓸 수 있다.

### 세 장면에서의 쓰임

- **장면 1:** 할 가치, 품질 기준, 허용할 위험과 해당 책임자가 직접 정할 선택을 드러내는 데 강하다. 사용자가 그 책임자일 때만 사용자 질문으로 만든다.
- **장면 2:** Engineering 판단이 걸린 설명에서 결론·근거·AI 해석·미확정을 풀어 borrowed confidence를 막는 데 조건부로 강하다. 일반 대화 전체의 설명법을 제공하지는 않는다.
- **장면 3:** 가장 직접적이다. 결과를 설명할 수 있는 범위와 근거를 돌려주고, 이해와 최종 판단을 test pass나 AI 결론으로 대신하지 않게 한다.

### 가져오지 않을 것과 한계

- 06을 별도의 “최종 판단 장면”으로 만들지 않는다. 세 장면 안에서 설명과 근거가 사람의 판단으로 이어져야 하는 이유를 제공하는 공통 기준으로만 쓴다.
- 발표는 충분한 이해와 충분한 evidence의 깊이를 정하지 않는다. [`기존 분석이 확인한 빈칸`](../06-wHePopfD6js.md#L170)
- 사람이 마지막에 승인했다는 형식만으로 독립 판단이 생기지 않는다. AI가 고른 근거와 해석을 반복하면 이해 공백은 남을 수 있다.
- 발표가 인용한 조사 수치와 연구는 원 연구가 보존되지 않아 발표자의 소개 범위만 사용할 수 있다.
- 저위험·가역적 작업까지 같은 깊이로 설명하고 확인하면 검토 비용이 이득을 넘을 수 있다.

## 08 — 현재 일을 고르고, 전체를 넘기고, 한 조각을 실제로 보는 방법

이 source는 Shape Up Chapter 7·10·11의 제공된 한국어 번역이다. 영어 원문 snapshot과 번역 대조는 아직 없으므로 정확한 표현을 확정할 자료가 아니라 초기 reference로 사용한다. [`08 source 상태`](../../source/08-shape-up-chapters-ko/source.md#L10)

### Chapter 7: 현재 살아 있는 후보만 논의한다

1. **오래된 후보 전체를 계속 검토하는 일 자체가 집중과 인지 비용을 만든다.**

   원문은 처리할 수 없는 backlog를 보며 뒤처진 느낌을 받고, 오래된 아이디어를 재검토·정리·재우선순위화하느라 현재 project에 집중하지 못한다고 말한다. [`backlog의 부담`](../../source/08-shape-up-chapters-ko/chapter-07-bets-not-backlogs/translation.ko.md#L12)

2. **과거 아이디어는 목록에 남아 있다는 이유가 아니라 현재 맥락과 목적을 가진 사람이 다시 제기할 때 논의한다.**

   Betting table에는 최근 만들어진 소수의 shaped pitch나 누군가 의도적으로 다시 가져온 이전 pitch만 올라간다. [`소수의 현재 후보`](../../source/08-shape-up-chapters-ko/chapter-07-bets-not-backlogs/translation.ko.md#L26), [`현재 맥락을 가진 재등장`](../../source/08-shape-up-chapters-ko/chapter-07-bets-not-backlogs/translation.ko.md#L96)

   장면 1에서 여러 작업 후보를 고르는 경우 `왜 지금 이 작업인가`, `최근 어떤 문제나 근거 때문에 다시 살아났는가`, `이번에 실제로 선택할 후보가 무엇인가`를 확인하는 방식으로 적용할 수 있다. 이미 선택한 한 작업의 요구를 구체화하는 방법은 아니다.

3. **기록과 선택 책임을 한 중앙 목록으로 합치지 않는다.**

   Support·Product·developer가 각자의 문제와 아이디어를 관리하고, 각 목록이 자동으로 betting 입력이 되지는 않는다. [`분산된 목록과 선택`](../../source/08-shape-up-chapters-ko/chapter-07-bets-not-backlogs/translation.ko.md#L60) 현재 적용에서는 모든 과거 기록을 새 작업 논의의 입력으로 자동 승격하지 않는 경계가 된다.

중요한 문제가 반드시 반복해서 돌아온다는 주장은 보안·법적 의무·데이터 손실 가능성처럼 드물어도 큰 피해가 나는 항목에 일반화하면 안 된다. 이 예외 목록은 원문이 아니라 현재 적용을 위한 제한이다.

### Chapter 10: 전체 문제와 경계를 넘기고 구현 판단은 열어 둔다

1. **작업을 미리 task로 잘게 나누면 실행자가 전체 관계와 판단 책임을 잃을 수 있다.**

   원문은 project를 시작 전에 task로 쪼개면 각 사람이 연결되지 않은 조각만 받는다고 말한다. 대신 team이 전체 project를 맡고 정해진 경계 안에서 필요한 task와 구현 방식을 발견한다. [`task가 아니라 project 전체`](../../source/08-shape-up-chapters-ko/chapter-10-hand-over-responsibility/translation.ko.md#L8)

2. **자율성은 문제와 경계가 없는 상태가 아니다.**

   Shaping에서 해결할 문제의 형태와 경계를 정하되, 윤곽 안의 실제 설계와 구현은 작업자가 현실을 보며 채운다. [`정할 것과 열어 둘 것`](../../source/08-shape-up-chapters-ko/chapter-10-hand-over-responsibility/translation.ko.md#L40) 장면 1에는 전체 문제·원하는 결과·하지 않을 것까지 공유하고 내부 task·module 선택은 미리 닫지 않는 근거가 된다.

3. **작업 전 논의는 모든 질문을 끝내는 것이 아니라 시작하기에 충분한 이해를 만드는 데서 멈출 수 있다.**

   Kickoff는 문서만으로 명확하지 않은 중요한 질문을 하고 project에 대한 대략적인 이해가 생기면 일을 시작한다. [`kickoff의 질문과 종료`](../../source/08-shape-up-chapters-ko/chapter-10-hand-over-responsibility/translation.ko.md#L76)

4. **기존 system을 이해하고 시작점을 찾는 탐색은 실제 작업이다.**

   처음 며칠의 조용한 시간은 team이 기존 system과 관련 code를 이해하고 좋은 시작점을 찾는 과정이다. 예상한 task와 실제 구현 중 발견되는 task도 다르다. [`방향을 잡는 시간`](../../source/08-shape-up-chapters-ko/chapter-10-hand-over-responsibility/translation.ko.md#L90), [`예상 task와 발견되는 task`](../../source/08-shape-up-chapters-ko/chapter-10-hand-over-responsibility/translation.ko.md#L128) AI도 실제 code를 파악 중인 상태를 완성된 구조 설명처럼 포장하지 않아야 한다는 조건부 근거가 된다.

### Chapter 11: 작지만 실제로 동작하는 한 조각으로 이해와 판단을 구체화한다

1. **수평 layer의 진척보다 직접 써 볼 수 있는 작은 end-to-end 결과가 판단하기 쉽다.**

   원문은 frontend나 backend layer를 따로 완성하기보다 project의 작은 한 부분을 통합해 실제로 동작하는지, 원하는 방식인지 확인하고 틀리면 다시 생각하라고 한다. [`작은 통합 결과`](../../source/08-shape-up-chapters-ko/chapter-11-get-one-piece-done/translation.ko.md#L20)

   장면 1에서는 핵심 가정을 실제로 시험할 가장 작은 동작을 고르는 데 쓸 수 있다. 장면 3에서는 file·commit 수가 아니라 사용자가 수행할 수 있는 한 흐름을 따라 작업물을 설명하는 근거가 된다. 이 설명 방식은 원문을 현재 목표에 옮긴 도출이다.

2. **거친 표면에도 중요한 제품 결정이 들어 있을 수 있다.**

   원문은 UI의 field와 option이 가격·숙박·과정 단계 같은 깊은 결정을 반영할 수 있음을 보여 준다. [`표면 형태에 들어간 결정`](../../source/08-shape-up-chapters-ko/chapter-11-get-one-piece-done/translation.ko.md#L173) 장면 3에서는 보이는 화면이나 diff만 설명하지 않고, 그 형태가 어떤 결정과 제약을 구현하는지 연결하는 근거가 된다.

3. **핵심을 시험하기 위해 주변부를 의도적으로 불완전하게 둘 수 있지만 그 상태를 숨기면 안 된다.**

   Mock data, 임시 route와 hard-coded 인증으로 핵심 문제를 먼저 시험하는 사례가 나온다. [`전략적으로 불완전한 주변부`](../../source/08-shape-up-chapters-ko/chapter-11-get-one-piece-done/translation.ko.md#L229) 장면 3에서는 실제로 동작하는 구간, stub·mock·hard-coded인 구간과 아직 이 결과로 알 수 없는 부분을 나눠 설명해야 한다.

4. **첫 결과는 핵심이고, 작으며, 아직 검증하지 않은 부분을 우선할 수 있다.**

   보존 번역은 첫 조각이 project의 핵심이고 며칠 안에 의미 있게 끝낼 수 있어야 하며, 둘 다 만족하는 후보라면 이전에 해 보지 않은 쪽을 먼저 선택하라고 한다. [`첫 조각의 세 기준`](../../source/08-shape-up-chapters-ko/chapter-11-get-one-piece-done/translation.ko.md#L281) 장면 1에서 첫 실제 결과를 정해야 할 때만 쓸 수 있으며 모든 작업 논의의 필수 절차는 아니다.

### 08 전체의 쓰임과 한계

- **장면 1:** 현재 살아 있는 후보, 전체 문제와 경계, 구현 판단의 여지, 필요할 때 첫 작은 실제 결과를 고르는 데 강하다.
- **장면 2:** 직접적인 이해 복구법은 없다. Chapter 11의 “사용자가 이해할 수 있는가”는 제품 UI가 사용되는 장면이지 AI 설명법이 아니다.
- **장면 3:** Chapter 11의 end-to-end 결과와 불완전한 구간 구분을 코드·작업물 설명에 조건부로 적용할 수 있다. Chapter 10은 실제 repository 탐색이 선행돼야 한다는 근거만 준다.

작은 slice가 전체 feature 완료로 오해될 수 있고, stub이 핵심 자체를 대체하면 원래 취지와 반대가 된다. 눈으로 시연하기 쉬운 UI 작업에 편향되어 migration·보안·내부 기반 같은 비가시 작업을 저평가할 수도 있다. `vertical slice`와 일부 공식화는 기존 analysis의 재표현이며 보존 번역의 직접 용어로 취급하지 않는다. [`08 analysis의 사용 경계`](../08-shape-up-chapters-ko/README.md#L15)

## 자료별 재독에서 달라진 판단

- 01은 예상대로 세 장면의 직접 동작을 거의 제공하지 않는다. 다만 **필요한 과거가 빠졌을 때 관련성 높은 최소 정보만 가져온다**는 공통 정보 선택 원리는 남는다.
- 02의 의미 단위와 큰 구조에서 source·실행으로 내려가는 이동은 원문 근거가 강하다. 반면 `사용자 workflow → 책임 → 상태 변화`라는 완성된 설명 목차는 원문에 없으며 08과 함께 도출해야 한다.
- 장면 1의 구체적인 대화 진행은 03·04의 `Grill with Docs`가 가장 직접적이다. 08 Chapter 10은 무엇을 정하고 무엇을 열어 둘지 보완한다.
- 장면 2의 구체적인 이해 복구는 03·04의 `Wait What`이 가장 직접적이다. 02·08에는 이를 대신할 설명법이 없다.
- 장면 3의 중심 재료는 02의 semantic structure·source·trace 구분, 08 Chapter 11의 end-to-end 결과, 06의 설명 깊이와 근거·사람 판단 경계다.
- 06은 독립된 네 번째 장면이 아니라 세 장면에서 AI 설명과 evidence가 사람의 판단을 대신하지 않게 하는 공통 제한으로 쓰는 편이 맞다.

다음 문서에서는 이 자료별 결과를 source 단위로 합쳐 버리지 않고, 각 인사이트를 [`세 장면별 후보 동작`](02-three-scenes-reference-synthesis.md)으로 다시 배열한다.
