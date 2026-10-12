# Work-first와 Spec/Ticket-first 트레이드오프 분석

> **후속 결과 — 2026-09-08:** 아래 비교는 당시 Work-first의 기본값과 Matt의 특정 Spec/Ticket 운영을 대조한 분석이다. 이후 Context Harness Reference에서는 Spec을 기본 작업 정의로, Ticket을 필요할 때 작성해 memory에서 유지하는 실행 단위로 채택·구현했다. 현재 결과는 [Spec·Ticket 통합 분석](07-context-harness-spec-ticket-integration.md)에서 먼저 확인한다. 아래의 조건부 도입 관계나 특정 실행 규율을 새 Reference의 확정 규칙으로 적용하지 않는다. 실제 효과와 비용의 검증 필요성은 유지된다.

## 문서의 지위

이 문서는 [`01-problem-analysis.md`](01-problem-analysis.md)에서 출발해 채택한 [`Workspace 기반 연속성`](02-workspace-based-continuity-direction.md)과 [`Project context foundation`](03-project-context-foundation-direction.md)을, Matt Pocock의 Spec/Ticket 흐름과 과거 TripProof spec-driven 운영에 대조해 설계상의 교환관계를 정리한다.

목적은 Work가 더 우월하거나 새롭다고 주장하는 것이 아니다. 두 운영 방식이 무엇을 최적화하고 무엇을 대가로 치르는지 분명히 해, Work가 단순 재명명인지 조건이 있는 합리적 설계 선택인지 이후 논의할 기준을 남기는 것이다.

현재 TripProof의 Project/Work 구조는 실제 제품 작업에 적용하기 전이다. 따라서 이 문서는 구조와 기존 근거로 설명할 수 있는 **설계 가설과 선택 조건**까지만 소유한다. 실제 효과, 사람 acceptance와 일반적인 우월성은 주장하지 않는다.

## 현재 결론

Work-first와 Spec/Ticket-first는 일부 정보를 공유하지만 운영 기본값이 다르다.

- **Work-first**는 판단과 상태가 구현 중에도 바뀔 수 있다고 보고, 살아 있는 Work current를 해당 Work의 현재 재진입·조율 표면으로 둔다. Project의 상세 현재 사실은 각 실제 Owner를 따르고, 여러 Work에 계속 유효한 의미만 Project context 반영 후보로 올린다. 일회성 실행 산출물을 어떤 형식으로 파생할지는 작업 조건에 따라 정한다.
- **Spec/Ticket-first**는 판단이 충분히 닫힌 변경에서 Spec을 결정 snapshot으로 만들고, 이를 fresh context 하나가 수행·검증할 Ticket으로 나눠 정확한 실행과 분배를 우선한다. 다만 plan이나 현재 대화가 충분하면 별도 Spec 없이 곧바로 Ticket을 만들 수도 있다.

따라서 Work의 가장 강한 설명은 Spec/Ticket의 대체재나 개선판이 아니라, **실행 전후에 변하는 판단·현재 권위·근거와 역사의 수명을 다루는 continuity envelope**라는 것이다. 판단이 안정된 구현 단계에서는 Work 안에서 Spec이나 Ticket에 해당하는 일시적 실행 산출물을 사용할 수 있다는 것이 현재 후보 관계다.

명확한 트레이드오프는 이 구조가 시험할 가치가 있는 합리적 선택이라는 점을 방어한다. TripProof에 실제로 더 적합했다는 주장은 운용 증거가 있어야 한다.

## 비교 단위와 공정성

### 파일 이름이 아니라 운영 기본값을 비교한다

`Work 대 Spec`을 포함 필드나 파일 수로 비교하면 목표·범위·완료 조건·현재 상태가 겹치므로 재명명처럼 보인다. 실제 비교 대상은 다음과 같다.

```text
Work-first
현재 판단과 상태를 계속 교체할 수 있는 Work-local 재진입·조율 표면
→ 필요하면 현재 행동이나 한 session용 실행 산출물 구성
→ 결과를 근거로 current와 관련 판단 재검토

Spec/Ticket-first
결정이 끝난 목적지를 필요하면 Spec snapshot으로 고정
→ Spec·plan·현재 대화에서 한 fresh context 크기의 Ticket들로 분해
→ Ticket별 구현·검증·종료
```

### Matt의 흐름을 허수아비로 만들지 않는다

Matt의 [`to-spec`](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/docs/engineering/to-spec.md)은 Spec을 영구 Project 정본으로 보지 않는다. 구현이 새 사실을 가르치면 stale해질 수 있고, 작업 뒤에는 버리며, 오래 유지할 의미와 결정은 `CONTEXT.md`와 ADR에 두라고 한다. [`to-tickets`](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/docs/engineering/to-tickets.md)도 모든 작업에 Ticket을 요구하지 않고 한 context에 끝나는 변경은 곧바로 구현하도록 한다. Ticket은 Spec뿐 아니라 plan이나 현재 대화에서도 직접 만들 수 있다.

따라서 과거 TripProof 문제를 `Spec-driven 개발 일반의 본질적 실패`라고 표현하면 안 된다. 현재 근거가 지지하는 더 좁은 진단은 다음과 같다.

- 과거 TripProof의 Spec·AC·test·eval은 한 slice의 계약, 구현과 검증에는 강했다.
- 여러 작업이 누적되면서 당시 Spec과 코드 구조가 다시 검토할 선택보다 현재의 확정 전제처럼 작용했다.
- 제품 전체 방향, 코드 성장성, 판단 재개방과 과거 결과의 현재 권위를 다루는 상위 시간축은 상대적으로 약했다.
- Work는 이 상위 시간축과 정보 수명을 별도 책임으로 다루려는 설계다.

과거 강점과 한계의 해석·요약은 [`05-tripproof-harness-retro.md`](../05-tripproof-harness-retro.md)와 [`01-problem-analysis.md`](01-problem-analysis.md)가 소유하고, 원문과 provenance는 각 문서가 가리키는 `context/source/`가 소유한다.

## 실제 중복과 실제 차이

### 겹치는 책임

- Work goal·완료 장면·범위·비범위는 Spec의 목적지·scope·out-of-scope와 겹친다.
- Work constraints와 current judgment는 Spec의 결정·제약과 겹칠 수 있다.
- 004에서 사용한 Work의 bounded brief는 Ticket의 fresh-context handoff와 일부 겹친다.
- records의 판단 이유와 결과는 Spec reasoning, ADR, issue history와 겹친다.
- Project context는 일반적인 project docs, `CONTEXT.md`, ADR과 상당 부분 겹친다.

그러므로 Work를 완전히 새로운 정보 primitive로 설명하지 않는다. 익숙한 요소를 TripProof의 수명·권위·재진입 문제에 맞게 다시 배치한 구조에 가깝다.

### Work 쪽에 남는 고유한 운영 책임

- 살아 있는 현재 답과 당시에는 합리적이었던 history를 명시적으로 분리한다.
- Work 안에서 강했던 지시·결과가 이후 Project 전체의 권위를 자동으로 얻지 못하게 한다.
- 여러 Work에 계속 유효한 변화만 실제 Project Owner에 반영할 후보로 올린다.
- Workspace마다 필요한 Project context를 이유와 함께 선택해 bounded recovery한다.
- 기능 구현뿐 아니라 조사·결정·architecture 재검토처럼 판단 자체가 움직이는 작업을 같은 시간 경계에서 다룬다.
- 새 결과가 기존 판단을 바꾸면 그 판단에 의존한 선택과 결과를 다시 보는 방향을 목표로 삼는다. 다만 이 마지막 항목은 아직 004의 미채택 가설이며 실제 효과가 아니다.

### Spec/Ticket 쪽에 남는 고유한 실행 책임

- 결정된 목적지와 test seam을 구현 전에 명확히 고정한다.
- 각 Ticket을 fresh context 하나에 들어가는 크기로 제한한다.
- schema·API·UI·test를 관통하는 좁지만 완전한 vertical slice를 요구한다.
- 각 조각이 독립적으로 demo·검증할 수 있게 한다.
- blocker graph와 실행 가능한 frontier를 통해 순차·병렬 실행을 조율한다.
- issue tracker에서 dependency와 실행 상태를 표현할 수 있다. 다만 실제 dispatch, assignee와 closure의 정확성은 tracker와 사람의 별도 관리에 의존한다.

현재 Work의 current와 004에서 제한적으로 사용한 bounded brief가 이 내용을 표현할 수는 있지만, 같은 분해 규율과 반복 실행성을 기본으로 제공한다고 입증되지는 않았다.

## 핵심 트레이드오프

| 판단축 | Work-first의 기본값 | Spec/Ticket-first의 기본값 | 실제로 치르는 대가 |
| --- | --- | --- | --- |
| 중심 문제 | 변하는 판단의 현재성·권위·재진입 | 결정된 변경의 정확한 실행·분배 | 적응성 대 실행 특화 |
| 활성 작업 기준 | Work-local `current`를 갱신하고 Project 상세 사실은 실제 Owner를 따른다 | Spec은 결정 snapshot, Ticket은 현재 실행 기준 | live 조율 표면 대 안정된 실행 baseline |
| 구현 중 학습 | upstream을 갱신할 표면은 있지만 brief·기존 결과로의 전파 방식과 효과는 미검증이다 | pivot 시 Spec snapshot을 다시 발행하거나 영향받는 Ticket을 폐기·재분해한다 | 지속 갱신·전파 비용 대 명시적 재발행 비용 |
| 실행 분해 | 상세 plan·모든 AC·blocker는 조건부 | seam·vertical slice·blocker가 핵심 계약 | 유연성 대 독립 검증·병렬성 |
| fresh context | 선택한 current와 Project context로 재진입하며, 004에서는 필요할 때 bounded brief를 사용했다 | self-contained Ticket 하나를 실행 | 공통 판단 탐색·보존 대 좁고 즉각적인 실행성 |
| 완료 의미 | session 또는 조건부 brief 완료와 Work·제품 판단 완료를 분리 | Ticket별 demo·AC와 closure를 강하게 표현 | 상위 판단 보존 대 국소 완료 선명성 |
| 장기 권위 | Work-local 결과를 Project 정본과 분리하고 선택적으로 반영 | durable 판단은 별도 Context·ADR로 옮기고 Spec/Ticket은 폐기 | 지속적인 권위 관리 대 별도 승격·폐기 작업 |
| 감사 관점 | 왜 판단이 바뀌었고 현재 무엇이 유효한지 추적 | Spec의 결정 snapshot과 Ticket dependency·실행 순서를 추적하되 실제 assignee·closure는 별도 관리 | 살아 있는 판단 history 대 결정·실행 snapshot |
| 유지비 | current·Owner·routing의 정확성을 계속 관리 | 작성·분해·tracker 관리 비용을 작업 기간에 지불 | 지속 관리비 대 일시적 실행 관리비 |

## Work-first가 강한 조건

- 구현하면서 제품 의미, 책임 배치나 architecture 판단 자체가 바뀔 가능성이 크다.
- 이전 판단을 다시 열고 그 판단에 의존한 기존 선택이나 결과도 다시 볼 필요가 있다.
- 조사·결정·prototype·구조 개선·구현처럼 성격이 다른 활동이 하나의 목표 안에서 이어진다.
- Project-wide 의미, 현재 구현 상태, Work-local 판단의 수명과 권위를 구분해야 한다.
- 긴 공백이나 session 교체 뒤에도 전체 history가 아니라 작은 current와 선택한 근거로 재진입해야 한다.
- 한 실행 조각의 통과를 상위 제품·코드 판단의 완료와 구분하는 것이 중요하다.

이 조건에서도 Work가 자동으로 우세하다는 뜻은 아니다. 실제 consumer가 current를 읽고, 새 근거에 따라 갱신하며, records를 현재 지시로 오인하지 않아야 구조상의 차이가 행동 차이가 된다.

## Spec/Ticket-first가 강한 조건

- 요구와 해결 방향이 이미 안정됐다.
- 한 변경을 여러 session이나 여러 실행자가 나눠 구현한다.
- 독립적으로 시연·검증할 vertical slice가 둘 이상이다.
- blocker와 병렬 실행 순서가 중요하다.
- 각 조각의 acceptance criteria와 test seam을 강하게 고정해야 한다.
- 판단의 재구성보다 정해진 내용을 빠짐없이 구현하는 것이 중심 문제다.
- dependency와 실행 상태를 tracker에서 공유하고, 별도 운영으로 assignee와 closure를 관리해야 한다.

이 조건에서 Work의 current와 brief만 고집하면 세부 범위 재구성, 숨은 blocker, 중복 수행과 통합 재작업 비용이 커질 수 있다.

모든 경우에 별도 Spec이 필요한 것은 아니다. 이미 정리된 plan이나 현재 대화가 충분하고 장기 decision snapshot이 추가 가치를 주지 않으면 Ticket으로 바로 분해해 Spec 합성 비용을 피할 수 있다. 반대로 Spec을 만들면 결정 압축 과정의 변형 가능성, dense한 문서의 사람 검토 비용과 tracker 재조회·잘림 비용도 함께 감수한다.

## 각 방식이 부당해지는 조건

### Work-first가 부당해지는 경우

- 단지 여러 session이 필요하다는 이유만으로 모든 작업에 Work를 만든다.
- 작은 수정에도 Workspace·current·records·Harness 절차를 의무화한다.
- 기존 issue·Spec·ADR의 내용을 이름만 바꿔 여러 Owner에 중복 기록한다.
- 결정이 끝난 병렬 구현에서도 Ticket·dependency graph 같은 실행 장치를 원칙적으로 거부한다.
- current를 갱신하고 실제 행동에서 소비할 주체가 없다.
- 기록 위치를 만들었다는 사실을 판단 연속성이나 제품 수렴의 효과로 주장한다.
- bounded current가 이론·역사·상태를 계속 흡수해 또 하나의 장기 Spec으로 팽창한다.

### Spec/Ticket-first가 부당해지는 경우

- 아직 핵심 책임과 해결 방향이 정해지지 않았는데 Spec으로 조기 고정한다.
- 구현이 알려 줄 핵심 불확실성을 문서 논의만으로 닫는다.
- Ticket을 layer별 또는 지나치게 작은 단위로 나눠 독립적인 사용자 결과가 사라진다.
- 각 Ticket의 AC 통과를 제품 전체 수렴이나 코드 성장성의 근거로 확대한다.
- 공통 판단과 재개방 조건을 Ticket마다 복제해 서로 다른 현재 답을 만든다.
- 새 근거가 upstream 판단을 무효화해도 이미 닫은 Spec과 Ticket을 계속 집행한다.

## Ticket과 bounded brief의 현재 관계

현재 004에는 다음과 같은 제한된 fresh-context 수행 사례가 있다.

```text
Work current
→ records의 변경하지 않는 bounded brief
→ fresh context의 독립 수행
→ records의 result
→ Main의 채택·기각 판단
→ current/state 반영
```

이 사례는 `Ticket이라는 새 영구 계층이 없으면 fresh-context 작업이 불가능하다`는 해석을 반박한다. records의 brief는 발행 시점의 입력 snapshot, result는 반환된 결과와 근거이며, current는 진행 여부와 채택된 현재 답을 소유할 수 있다.

하지만 이 제한된 004 사례를 일반 구현 Work의 기본 흐름으로 채택하지 않았다. Matt식 Ticket의 vertical slice, falsifiable acceptance, blocker graph, frontier와 tracker accountability까지 자동으로 대신하지도 않는다. 순차적인 판단·조사 작업에서는 충분할 수 있고, 반복 병렬 실행·복잡한 dependency·여러 실행 가능 조각이 나타나면 별도 Ticket 목록이나 issue tracker가 더 적합할 수 있다는 것이 현재 가설이다.

따라서 현재 열린 질문은 Ticket이라는 이름이나 디렉터리를 추가할지 여부가 아니라 다음과 같다.

> 어느 조건에서 Work의 다음 행동과 bounded brief만으로 충분하며, 어느 조건에서 fresh-context 실행 단위를 독립된 Ticket으로 관리해야 하는가?

## 가장 강한 반론과 현재 답

### “익숙한 요소를 이름만 바꿔 다시 만들었다”

개별 정보 요소 수준에서는 상당 부분 맞다. 목표·scope·current·history·decision·task는 기존에도 있었다. 방어 가능한 차이는 새로운 파일 유형이 아니라 현재 답과 history, Work-local과 Project-wide 권위, 기본 읽기 범위와 갱신 정책이 실제 행동을 다르게 만드는 데 있다.

이 차이가 운용에서 나타나지 않으면 Work는 재명명에 그친다.

### “핵심 판단 연속성을 해결하지 않고 저장 위치만 늘렸다”

현재로서는 맞다. Workspace와 Project context는 판단을 찾고 보존할 기반이며, 그 판단이 작업 선택·미룸·구현·근거 해석·완료를 실제로 통제하는지는 004의 남은 문제다. Work를 판단 연속성의 완성된 해결책으로 설명하지 않는다.

### “결국 Spec과 Ticket을 다시 쓰면 Work는 불필요한 wrapper다”

판단이 이미 안정된 유한 build만 본다면 이 반론이 성립할 수 있다. 반대로 판단이 움직이는 장기 작업에서 Spec/Ticket의 실행 권위를 어느 시간과 범위 안에 제한하고, 결과를 현재 판단과 Project 정본에 다시 연결해야 한다면 Work envelope의 별도 책임이 남는다.

Work 안에서 Spec/Ticket을 사용한다는 사실 자체는 실패가 아니다. Work가 맡은 수명·권위·재진입 책임 없이도 같은 결과를 더 단순하게 얻을 수 있다면 그때 wrapper 비용이 정당화되지 않는다.

### “living current도 결국 더 큰 stale 문서가 된다”

가능한 핵심 위험이다. current가 작고 현재 답만 소유하는지, 갱신 trigger와 consumer가 있는지, history가 records로 실제 강등되는지를 시험해야 한다. 문서 이름만 `current`라고 해서 최신성이 보장되지 않는다.

## 설계 선택과 포트폴리오 설명의 상한

현재 근거로 방어 가능한 설명은 다음과 같다.

> Spec과 Ticket은 결정된 변경을 여러 실행 session에 정확히 분배하는 데 강하다. Work는 그 실행보다 앞뒤에서 변하는 Work-local 판단, Project의 실제 Owner, 근거와 역사의 수명을 연결하는 데 초점을 둔다. 판단이 열려 있는 동안에는 Work current를 재진입·조율 표면으로 사용하고, 실행 경계가 안정되면 필요에 따라 Spec이나 Ticket에 해당하는 일시적 산출물을 사용할 수 있다. 그 대가로 지속적인 current 관리 비용과 약한 기본 실행 분해를 감수한다.

이 설명은 Work가 모든 상황에서 낫다는 주장이 아니라, 어떤 조건에서 어떤 이득을 위해 어떤 비용을 선택했는지 보여 준다. 따라서 설계가 모순이 아니며 시험할 가치가 있다는 점은 설명할 수 있다.

아직 말할 수 없는 것은 다음과 같다.

- Work가 일반적인 Spec/Ticket 개발보다 우월하다.
- 실제 TripProof에서 재진입 비용과 판단 누락을 줄였다.
- bounded brief가 구현 Ticket을 항상 대신할 수 있다.
- Project/Work 구조가 제품 수렴이나 코드 성장성을 해결했다.
- 추가 Harness의 지속 비용보다 얻는 효과가 크다.

포트폴리오에서는 현재 구조를 `검증된 더 나은 개발법`이 아니라, 과거 관찰에서 나온 **명시적인 trade-off를 가진 설계와 시험 가능한 prototype**으로 표현해야 한다.

## 실제 운용에서 확인할 증거

### Work의 목표와 직접 연결된 증거

- fresh session이 작은 current와 선택한 Project context만으로 목표·현재 상태·열린 판단·다음 행동을 복원하는가.
- 과거 brief·Spec·record가 현재 지시처럼 작동하지 않는가.
- 구현의 새 사실이 현재 판단과 필요한 의존 결과를 실제로 다시 열게 하는가.
- 한 session의 국소 완료가 더 넓은 제품·코드 판단으로 부당하게 승격되지 않는가.
- 여러 Work에 계속 유효한 변화만 Project context의 적절한 Owner에 반영되는가.

### 비교 비용과 손실

- 사용자의 재설명과 scope correction이 얼마나 필요한가.
- current가 stale하거나 팽창하는가.
- 같은 의미가 current·record·Project context에 중복되는가.
- Work를 유지하는 시간·주의·문서 변경량이 얼마나 드는가.
- Ticket을 사용하지 않아 blocker 누락, 중복 수행이나 통합 재작업이 발생하는가.
- Ticket을 사용할 때 과분해, 국소 완료 편향이나 upstream 판단 손실이 발생하는가.

### 비교가 필요한 대표 작업

- 요구가 안정된 multi-session feature
- 판단과 책임 배치가 구현 중 바뀌는 architecture 또는 제품 작업
- 순차적으로 근거를 보며 다음 행동을 바꾸는 작업
- 여러 fresh agent가 병렬로 구현하는 작업
- 맥락을 따로 복구할 필요가 없는 작은 수정

작은 수정에서 Work를 건너뛸 수 있는지, 안정된 병렬 구현에서 Spec/Ticket을 채택할 수 있는지도 설계의 성공 조건에 포함한다.

## 이후 논의할 열린 질문

- Work의 stable contract와 mutable state 사이에서 같은 판단을 중복하지 않을 canonical Owner는 무엇인가.
- current가 bounded surface로 남기 위한 크기·갱신·축소 조건은 무엇인가.
- 어느 시점에 판단이 충분히 안정되어 Spec 또는 Ticket으로 닫아도 되는가.
- 구현의 어떤 사건이 닫힌 Spec·Ticket과 upstream 판단을 다시 열어야 하는가.
- bounded brief에 부모 Work의 어떤 판단·책임·관찰·권한을 반드시 운반해야 하는가.
- 순차 brief에서 독립 Ticket 관리로 전환할 실제 trigger는 무엇인가.
- 판단이 바뀌었을 때 어떤 unfinished·completed 실행 결과까지 재판정해야 하는가.
- Work를 사용하지 않거나 제거해야 하는 조건은 무엇인가.

이 질문들은 새 구조나 파일을 지금 추가하라는 요구가 아니다. 실제 TripProof 적용 전에 비교 기준을 더 구체화하고, 적용 중 관찰할 증거를 정하기 위한 후속 논의 항목이다.

## 주요 근거

- [`01-problem-analysis.md`](01-problem-analysis.md): 과거 Spec의 강점, 판단 연속성의 공백과 원래 해결 질문
- [`02-workspace-based-continuity-direction.md`](02-workspace-based-continuity-direction.md): Work current·records·Project context의 수명과 책임 경계
- [`03-project-context-foundation-direction.md`](03-project-context-foundation-direction.md): Work-local 실행 권위와 Project-wide 현재 판단의 관계
- [`01-current-direction.md`](05-judgment-continuity-solution-direction/archive/2026-09-06-before-reassessment/01-current-direction.md): Work 기반 위에도 남은 판단 연속성 목표와 증거 상한
- [`../05-tripproof-harness-retro.md`](../05-tripproof-harness-retro.md): 과거 TripProof spec-driven 운영의 확인된 강점과 longitudinal 공백
- [`Matt to-spec`](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/docs/engineering/to-spec.md): 결정 snapshot, multi-session trigger, stale·폐기와 durable context 경계
- [`Matt to-tickets`](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/docs/engineering/to-tickets.md): fresh-context vertical slice, blocker·frontier와 알려진 실패·운영 비용

Matt 자료는 2026-09-03에 clean 상태의 로컬 clone `/Users/hammyeong-yeon/Desktop/skills`에서 commit `068b6e0c62393147daf03530149cdce209c93da8`을 읽었다. 위 링크는 같은 commit의 원문으로 고정했다. 기존 [`context/source/04-matt-pocock-skills`](../../source/04-matt-pocock-skills/source.md)의 보존 범위에는 이 두 문서가 포함되지 않으므로, 그 과거 source record가 이번 비교의 직접 원문을 보존한 것처럼 소급해 표현하지 않는다.
