# Spec·Ticket 작성 책임 독립 리뷰

날짜: 2026-09-08

상태: **독립 리뷰 회수와 Main의 평가, 후속 사용자 선택. Maintain의 기록·갱신과 Main의 작업 조율을 구분하며 실제 Reference 변경은 없다.**

## 리뷰를 요청한 대화

[Main·Maintain 책임 분석](2026-09-08-09-main-maintain-responsibility-analysis.md) 뒤 사용자는 기존 Maintain의 실제 동작을 다시 짚었다.

> 기존도 사실상 maintian이 나와 매인과의 대화를 보고 결정하고 알아서 수정한다 아니었나?

Main은 기존 Maintain이 대화를 이해하고 무엇을 남길지·어떻게 수정할지를 판단하며 명확한 변화를 자율 반영하던 구조임을 확인했다. ‘Main이 판단하고 Maintain이 반영한다’는 설명이 기존 Maintain의 의미 판단을 축소했다는 점을 정정했다. Spec도 기존 흐름을 이어받는 것이 자연스럽다는 제안과 별도 실행자의 결과 전달 문제를 설명했다.

> 그러게 새 서브나 세션이 문제네

Main은 결과가 Main에 돌아오는 subagent와 별도 독립 세션을 구별하고, 결과가 어디에 남으며 누가 전체 Workspace 관리에 이어 쓰는지가 쟁점이라고 설명했다. 이 설명도 아래 리뷰의 검토 대상이다.

> 흠 그냥 spec ticket 작성은 main이 해야하나? 아 어렵네 독립리뷰 시켜봐 이상황과 자료들 필요한거 주고

‘Main이 작성한다’는 문장은 사용자 선택이 아니라 리뷰가 필요한 후보·질문이다.

## 입력과 독립성

`subagent-delegation` skill과 독립 리뷰 기준을 적용해 대화 전체를 상속하지 않는 새 reviewer에게 읽기 전용 검토를 맡겼다. Main 전담, Maintain 확대 또는 특정 대안을 예상 결론으로 주지 않았다. ‘작성’이라는 질문의 의미와 Main의 직전 분석 자체도 기각할 수 있게 했다. 파일 수정·runtime 실행·추가 agent 생성은 맡기지 않았다.

사용자의 최근 원문과 가까운 교환, 채택한 구조의 위치, 실제 Maintain과 과거 선택 이유, 실패 연구 원자료의 접근점을 제공했다. 010 current/state와 기록 09는 Main의 해석을 포함한 검토 대상이며 확정안으로 읽지 않도록 했다. Spec 도입·구성·memory 배치를 다시 심사하거나 실행자 범위를 먼저 고정하는 리뷰로 확대하지 않았다.

주요 입력과 reviewer가 직접 확인했다고 보고한 근거:

- [010 memory](../current/memory.md), [Ticket 관리 결정](2026-09-08-07-memory-ticket-placement-decision.md), [전체 담당·실행자 구상과 범위 조정](2026-09-08-08-workspace-ticket-execution-direction.md), [Main 분석 09](2026-09-08-09-main-maintain-responsibility-analysis.md).
- [Spec 구성 이유](../output/spec-components-and-rationale.md), [예시 Spec](../output/spec-example-travel-answer.md).
- [현재 Maintain 계약](../../../../reference-project/context/work/harness/maintain/README.md), [agent 지침](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml), [로컬 읽기 범위](../../../../reference-project/context/work/harness/maintain/codex_session.py), [host 입력](../../../../reference-project/context/work/harness/maintain/host_adapter.py), [허용 경로·쓰기 검사](../../../../reference-project/context/work/harness/maintain/operation.py), [세션 귀속·비동기 동작](../../../../reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md).
- [007의 사용자 기대](../../007-maintain-clean-room-reimplementation/records/2026-08-18-01-clean-room-source-and-behavior-contract.md), [목적 재기준화와 입력·검증 범위](../../007-maintain-clean-room-reimplementation/records/2026-08-19-06-purpose-rebaseline-and-remaining-scope.md).
- [연구의 문제 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/01-problem-analysis.md), [트레이드오프 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md), [관점별 회고 원문](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-conceptual.md), [시간순 회고 원문](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-chronological.md).
- [기존 외부 용례 조사](2026-09-08-03-ticket-references-and-placement.md)가 연결한 Matt의 한국어 `to-tickets` 독해본. reviewer는 Context 수집·코드 조사·분해·본문 구성을 비교 자료로 읽었다고 보고했다. 이 skill을 실제 호출하거나 tracker에 게시하지 않았다.

Main은 병행해서 실제 host delta, 관련 로컬 파일을 추가로 읽을 수 있는 범위, 허용 경로·대상 파일 SHA 검사, 같은 세션의 event 처리 범위를 확인했다. 해당 코드 위치를 reviewer에게 전달했다. 중간 보고 뒤에는 ‘실행 전에 본문이 준비돼야 한다’는 조건을 Main 전용 작성자로 곧바로 연결하지 말고, 대화에서 내용이 충분한 경우와 추가 설계가 필요한 경우를 비교하도록 요청했다. 현재 비차단 구현을 변경 불가능한 제약으로 삼지 않도록 재확인했다.

## 회수한 리뷰 본문

아래는 reviewer의 최종 보고 본문이다. 마지막의 근거 링크 목록은 위 입력·근거 목록으로 모았으며, 권고는 사용자 결정이 아니다.

**Spec·Ticket의 작성자를 Main으로 독점 지정할 필요는 없습니다.** 권고는 **이미 대화에서 분명해진 내용을 문서로 만드는 일은 Maintain이 자율적으로 맡고, 아직 정해야 할 요구·설계·작업 분해는 현재 Workspace를 맡은 Main이 작업으로 진행하되 필요하면 작성 자체를 위임하는 것**입니다.

따라서 “신규 작성은 Main, 갱신은 Maintain”도 정확한 경계가 아닙니다. 대화가 충분하면 Maintain이 첫 Spec을 작성할 수 있습니다. 반대로 기존 Ticket 수정이라도 작업 범위와 선후관계를 새로 정해야 한다면 조사·설계·분해 작업이 필요합니다. 그 작업을 다른 주체가 수행해도 됩니다.

여기서 Main에게 남기는 책임은 모든 문장을 쓰거나 Maintain의 수정안을 재승인하는 일이 아닙니다. **다음 실행에 사용할 Spec·Ticket이 준비됐는지, 새 결과 때문에 작업 방향을 바꿔야 하는지를 실제 진행에 연결하는 책임**입니다. 현재 전체 Workspace를 맡은 세션을 기준으로 한 권고이며, 최초 Main 세션이 영구 담당이어야 한다는 뜻은 아닙니다.

현재 자료에서 확인한 사실은 다음과 같습니다.

- Maintain은 이미 대화의 의미, 남길 변화, 문서 위치, 모호함을 판단하고 명확한 변경을 별도 Main 승인 없이 반영합니다. 새 memory 문서의 생성도 기존 기능에 포함됩니다. 다만 현재 허용 경로에는 새 `memory/spec/`·`memory/tickets/` 하위 폴더가 포함되지 않습니다.
- 자동 Maintain은 사용자 prompt와 Main의 마지막 사용자 대상 응답을 받습니다. **Main이 subagent 결과를 받았다는 사실만으로 그 결과가 Maintain에도 전달되지는 않습니다.** 필요한 로컬 파일이나 diff가 해당 입력에 명시되면 제한적으로 읽을 수 있으므로, Main 응답에 모든 근거를 복사할 필요도 없습니다.
- 현재 자동 갱신은 응답 뒤 비동기로 처리됩니다. 접수됐다는 사실만으로 다음 실행자가 읽을 본문이 준비됐다고 볼 수 없습니다. 이것은 현재 방식의 비용이며, 다른 호출 방식으로 바꿀 수 없는 금지선은 아닙니다.

구체적인 작업 장면으로 보면 다음과 같습니다.

1. **처음 Spec과 Ticket을 만든다.**
   사용자와의 대화에서 목표·동작·완료 조건·설계가 충분히 정리됐다면 Maintain이 이를 Spec으로 구성할 수 있습니다. Main이 항목마다 “이 파일에 이 문장을 써라”라고 지시할 필요는 없습니다. 그러나 “실제 모델로 여행 질문에 답하게 하자” 정도만 있고 호출 계약이나 실행 순서가 열려 있다면, 자동 Maintain이 그 빈칸을 확정된 결정처럼 채우게 하지 않는 편이 좋습니다. Main이 직접 조사·설계하거나 다른 주체에게 작성 작업을 맡깁니다. 작성된 본문을 같은 응답 안에서 검토하거나 Ticket 실행에 바로 사용할 때는 그 시점까지 작성을 끝내는 호출 방식이 필요합니다. **이 조건을 충족하는 작성자가 Main일 필요는 없습니다.**

2. **사용자가 “확인한 부분은 답하고 나머지는 미해결로 남기자”고 요구를 명확히 바꾼다.**
   Maintain은 Spec의 요구 동작·출력 계약과 관련 Ticket을 스스로 대조해 분명한 변경을 반영할 수 있습니다. 어떤 Ticket을 더 나눠야 하는지까지 불분명하면, 그 불확실성을 남기고 필요한 판단을 드러냅니다. Main은 이미 실행 중인 작업이나 다음 실행에 이 변경이 영향을 주는지 처리합니다. 문서를 고쳤다는 사실만으로 실행 중인 다른 세션의 이해도 바뀌지는 않기 때문입니다. 이전 완료 결과가 새 기준에서도 유효한지는 필요한 범위에서 다시 확인하며, 그 확인 역시 위임할 수 있습니다.

3. **subagent가 “모델 인터페이스와 검증기는 완료했지만 실제 모델 호출은 확인하지 않았다”고 반환한다.**
   실행자는 수행 내용·확인 범위·남은 문제와 근거 위치를 반환합니다. Main은 다음 작업을 결정하는 데 필요한 의미를 소비하고, Maintain이 받을 응답에 해당 결과의 핵심과 정확한 근거 경로가 드러나게 합니다. Maintain은 이를 Ticket에 반영하고, Spec이 요구한 실제 모델의 답변까지 완료된 것으로 확대하지 않습니다. 이때 모든 Ticket 결과에 Main의 별도 승인 단계를 추가할 필요는 없습니다. 다만 Main이 마지막 응답을 “모두 완료했습니다”로 축약하면 Maintain에 필요한 차이가 사라집니다. **새 subagent 자체보다, 중요한 결과가 후속 입력에서 누락되는 것이 직접적인 문제입니다.**

4. **별도 세션이 작업한다.**
   그 세션이 Workspace 전체를 이어받았다면, 그 세션의 Main이 현재 문서를 읽고 전체 진행을 맡을 수 있습니다. 원래 Main 대화로 반드시 돌아올 이유는 없습니다. 일부 Ticket만 수행한다면 지정된 Ticket이나 records에 결과·근거·상위 기준에 영향을 주는 발견을 남기고, 현재 전체 담당 또는 다음 전체 담당이 그 결과를 읽도록 연결해야 합니다. 실행자가 자기 Ticket을 직접 갱신하는 방식도 타당한 대안입니다. 다만 기존 Maintain이 별도 세션의 대화를 자동으로 관찰하거나 여러 세션의 결정을 자동 조율하는 기능은 확인되지 않았습니다.

대안의 비용을 비교하면, **Main이 모두 직접 작성·갱신하는 방식**은 사용하는 기준을 한 대화에서 맞추기 쉽습니다. 대신 모든 결과를 Main이 재구성해야 하고, 기존 Maintain의 의미 판단·자율 반영을 줄이거나 중복 수정 문제를 처리해야 합니다. Main의 누락을 줄인다는 증거도 없습니다. 소규모 작업의 단순한 운영으로는 가능하지만, 영구적인 전용 작성 규칙으로 삼을 근거는 약합니다.

**Maintain이 작성·분해·재계획까지 모두 맡는 방식**도 원천적으로 불가능하지 않습니다. 다만 아직 없는 판단까지 만들어야 한다면 필요한 코드·자료 접근, 질문과 후속 조사, 결과를 사용할 시점, 실행 중 작업에 대한 전달까지 맡겨야 합니다. 기존 대화 유지보다 넓은 작업이 됩니다. 대화에서 충분히 정리된 내용을 첫 문서로 만드는 정도라면 이 확대가 필요하지 않습니다.

**권고한 조합**은 기존 Maintain을 유지하면서 새로운 설계·분해 작업을 상황에 맞게 배치할 수 있습니다. 대가는 작성 완료와 결과 전달을 실제 실행 시점에 연결해야 한다는 점입니다. 실행자의 Ticket 직접 갱신은 이 전달 부담을 줄일 수 있지만, 같은 Ticket을 여러 주체가 동시에 바꾸는 문제까지 기존 hash 검사로 해결됐다고 볼 수는 없습니다.

Main의 기록 09는 대체로 적절하지만 다음과 같이 보완하는 것이 좋습니다.

- **확인된 사실:** Maintain이 단순 저장 장치가 아니라 의미를 판단하고 자율 반영한다는 설명, 제품 검증을 기본 업무에서 뺀 것이 목적과 비용에 따른 선택이었다는 설명은 원자료와 맞습니다.
- **적절한 판단:** 중요도나 문서 이름만으로 Main 전용 책임을 정하지 않고, 필요한 근거와 맡은 작업을 보자는 방향은 타당합니다. 입력에서 드러나는 불일치를 Maintain도 식별할 수 있다는 판단도 적절합니다.
- **보완할 판단:** “입력만으로 유지 가능한가, 추가 작업이 필요한가”에 더해 **언제까지 문서가 준비돼야 하고 누가 실제 실행에 사용하는가**를 봐야 합니다. 추가 작업이 필요하다는 사실도 Main 전용 작성자를 뜻하지 않습니다.
- **좁혀 말할 부분:** “새 subagent·세션이 문제”만으로 설명하면 부족합니다. 기존에도 Main의 도구 실행 결과 전체가 자동 입력은 아니었습니다. 새 세션은 그 전달 문제를 더 뚜렷하게 만들고, 별도 세션의 변경과 기존 이해가 어긋날 가능성을 추가합니다.

과거 연구도 Main 전용 작성자를 지지하지는 않습니다. 직접 읽은 회고의 중심 문제는 **작업 문서가 없거나 작성자가 분산됐다는 것보다, 국소 완료가 전체 판단을 밀어내고 이전 선택이 재검토되지 않은 채 이어졌다는 것**입니다. Spec을 누가 타이핑하든, 결과가 기존 판단을 다시 열고 다음 작업을 바꾸는 데 사용되지 않으면 그 문제는 남습니다.

사용자가 지금 결정할 핵심은 두 가지로 줄일 수 있습니다.

1. **Spec·Ticket도 Maintain의 자율 문서화 대상에 포함한다.** 이미 분명한 내용은 신규 작성·갱신 모두 가능하게 하고, 새로운 설계·분해가 필요한 일은 명시적인 작업으로 진행한다는 방향입니다.
2. **실행 결과가 현재 Workspace에 돌아와 다음 작업에 사용될 책임을 둔다.** Main으로 반환하는 방식과 실행자의 Ticket 직접 갱신 중 하나를 모든 상황에 고정할 필요는 없습니다. “누가 파일을 쓰는가”보다 결과를 남길 위치와 다음 소비자가 끊기지 않게 정하는 것이 우선입니다.

이 결과는 읽기 전용 설계 권고입니다. 파일·권한·자동화를 변경하거나 런타임을 실행하지 않았으며, 어떤 배치가 실제로 더 효과적인지는 아직 비교 검증되지 않았습니다.

## Main의 대조와 현재 의견

**Main 전용 작성자를 정하지 않자는 권고에 동의한다.** 기존 Maintain의 의미 판단과 자율 반영을 유지하면서, 필요한 조사·설계·Ticket 분해를 실제 작업으로 수행할 수 있게 두는 편이 현재 사용자 의도와 맞는다. 그러나 이 동의를 사용자 채택으로 올리지 않는다.

이번 리뷰로 기록 09를 보완할 두 지점이 분명해졌다. 첫째, 문서 작성자뿐 아니라 다음 실행에서 읽을 본문이 실제로 준비됐는지가 중요하다. 둘째, Main이 결과를 받아도 현재 Maintain 입력에 그 의미가 전달되지 않을 수 있다. 새 subagent가 없는 일반 도구 실행에도 이 차이가 있었으므로 이를 새 세션만의 문제로 설명하지 않는다.

대화에 충분한 내용이 있으면 첫 Spec·Ticket도 Maintain이 문서화할 수 있다는 것은 앞으로 적용할 설계 권고다. 현재 코드가 새 하위 폴더를 이미 지원한다는 뜻이 아니다. 반대로 기존 Spec·Ticket 수정에도 새 조사나 실행 선택이 필요할 수 있으므로 최초 작성과 이후 갱신을 서로 다른 주체의 전용 업무로 고정하지 않는다.

Main이 병행해서 확인한 코드에서는 `host_adapter.py`의 `response_end`와 `drain`이 사용자 발화와 마지막 응답을 전달하고, `codex_session.py`의 `_decision_prompt`가 관련 Context Owner와 delta에 명시된 파일·diff의 제한적 열람을 허용한다. `operation.py`는 현재 쓰기 대상의 SHA를 검사하며, 전체 읽기 근거나 여러 세션의 판단 일치까지 보장하지 않는다. 새 세션·동시 수정의 모든 해결책을 지금 정해야 한다는 뜻은 아니다.

현재 논의는 ‘Spec·Ticket도 기존 Maintain의 자율 문서화 대상에 포함할지’와 ‘작성·결과 반영을 실제 다음 실행에 어떻게 연결할지’다. 정확한 실행자 읽기·쓰기 범위, 모든 결과의 Main 경유, 새 역할·승인 단계·동기화 runtime은 채택하지 않았다.

이 기록과 010의 현재 논의 지점·색인만 갱신했다. Reference·외부 연구 자료·전역 지침은 수정하지 않았다. 문서 링크와 diff 형식만 확인하며 제품·runtime 테스트는 수행하지 않는다.

## 후속 사용자 선택: Maintain은 기록·갱신, Main은 작업 조율

리뷰를 설명한 뒤 사용자는 다음과 같이 역할을 정리했다.

> 다만 기록만 maintain 이지 조율이랑 이런걸 맡기는건 안되규 main이 자연스레 할거고 뭐 돌아가겟네 잘

Maintain은 대화와 결과를 이해해 Spec·Ticket·state에 필요한 내용을 기록하고 갱신한다. 무엇을 남기고 어떻게 반영할지 판단하는 기존 동작은 이어간다. 여기서 기록은 `records/` 폴더에만 쓰는 의미가 아니라 Workspace 문서의 유지이며, 단순 받아쓰기 장치로 축소하는 뜻으로 해석하지 않는다.

작업을 설계·분해하거나 위임하고, 결과를 받아 다음 행동으로 연결하는 조율은 Main이 자연스럽게 맡는다. Maintain에는 실행자 배치·작업 지시·진행 조율을 맡기지 않는다. Spec·Ticket 작성 전체를 Main만 할 수 있다는 전용 규칙을 추가한 것도 아니다.

사용자 선택은 이 책임 방향이다. 모든 실행 결과가 특정 원래 Main 세션을 거쳐야 한다는 규칙, 실행자의 고정 입력·쓰기 범위, 새로운 승인 단계나 별도 조율 runtime까지 채택한 것은 아니다. 실제 운영 효과는 아직 검증하지 않았으며 Reference 구현 보류도 유지한다.

사용자는 이어 기존과 같은 역할임을 다시 확인했다.

> 그냥 이전과 같다고 보면되지? 어차피 그때고 기록을 맡은거엿잖아?

Main은 기존 Maintain도 대화를 이해해 기록을 판단·갱신했고 Main이 작업을 조율했으므로 역할 자체는 같다고 확인했다. 이번 설계는 그 기록 대상에 Spec·Ticket을 포함하는 것이며 새 책임 배분 체계를 만드는 것으로 설명하지 않는다.
