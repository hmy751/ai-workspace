# Context Harness의 Spec·Ticket 적용 — 연구 측에 전달할 맥락과 근거

작성일: 2026-09-08

대상: memory-harness-research에서 TripProof의 판단 연속성·Workspace·Project context 설계를 이어가는 주체

구현 기준: context-harness commit **`dcd3c6f` — `feat: integrate workspace spec and tickets`**

## 이번에 무엇이 달라졌는가

Context Harness의 실행 가능한 기준 Project인 `reference-project/`에 **Spec과 Ticket을 실제 개념·파일로 도입했다.** 기존 Workspace의 goal·constraints는 Spec이 대체하고, Ticket은 실행할 일의 정의와 진행을 함께 관리한다. Workspace는 이 작업의 기준·현재 판단·원자료·산출물·기록을 함께 유지하는 범위로 남는다.

Spec 도입 여부, 다섯 구성요소, memory 배치, goal·constraints 대체, Main·Maintain의 기존 역할 유지는 사용자와 논의해 정한 내용이다. 일반 Recover에 Ticket 색인까지만 넣고 필요한 본문을 추가로 읽는 방식은 그 합의 안에서 Main이 선택한 구현 기본값이다. 개별 실행자의 입력·쓰기 범위와 Ticket의 상세 형식은 열어 두었다.

이 문서는 **채택한 설계와 구현 상태를 연구에 되돌려 전달하는 문서**다. 연구 저장소의 기존 분석이나 실제 TripProof에 이 구성을 적용한 결과가 아니다. Context Harness root의 연구 Workspace도 기존 `current/memory.md`·`state.md` 형식을 유지한다. 자동 Maintain을 root에 다시 연결하지 않았다.

첫 독해는 이 문서로 충분하도록 선택 이유와 한계를 직접 적었다. 실제 운영 기준은 [Workspace의 Spec과 Ticket](../../../../reference-project/context/work/workspaces/SPEC-AND-TICKETS.md), 설명과 구체적인 예시는 [Spec 구성 이유](spec-components-and-rationale.md)와 [여행 질문 답변 예시](spec-example-travel-answer.md)에서 이어 읽을 수 있다.

## 출발점: 실행을 명확히 하면서 판단을 다시 할 수 있어야 했다

도입의 직접 계기는 스킬 작성·작업 분해·인계에서 “current를 바탕으로 작업한다”만으로는 정의할 대상과 실행 단위를 지칭하기 애매하다는 사용자 경험이었다. 외부 자료의 Spec·Ticket을 매번 자체 표현으로 바꾸는 일도 추가 해석·관리 비용이었다. 특정 spec-driven 체계를 통째로 가져오거나 익숙한 개념을 잘게 나눠 새 이름으로 대체하려는 요청은 아니었다. [첫 요청과 논의 기록](../records/2026-09-07-01-session-synthesis.md).

동시에 연구의 원래 문제를 유지했다. [01 문제 분석](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/01-problem-analysis.md)은 Spec·AC·테스트가 개별 작업을 이어 주었지만, 제품이 원래 문제를 풀고 있는지와 기존 구조가 다음 변경을 받을 수 있는지를 다시 판단하는 감각은 같은 강도로 이어지지 않았다고 진단했다.

[04 대화 장면 분석](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/04-conversation-scene-analysis.md)의 제품 사례에서는 실제 모델이 자료의 의미를 판단해야 한다는 합의를 반복해 확인했는데도, 구현에는 교체 가능한 interface와 검증기가 생기고 실제 모델 호출은 빠졌다. 기반 구조와 테스트의 완료가 기대한 수행의 완료처럼 보고됐다. 따라서 목표를 더 자세히 써 두는 것만으로 이 문제가 해결된다고 볼 수 없다.

이번 설계가 다루려는 것은 다음 관계다. **Spec으로 요구하는 결과를 명확히 하고 Ticket으로 실행할 일을 특정하되, 실행 결과를 근거로 현재 선택과 완료 판단을 다시 할 수 있어야 한다.** 과거 Spec이나 현재 코드에 적혀 있다는 사실만으로 그 선택을 계속 확정 전제로 받지 않는다. 반대로 구현이 빠졌다는 사실만으로 목표를 낮추거나 Spec을 현재 코드에 맞추지도 않는다.

이 원칙을 실제로 지키는지는 별도 확인 대상이다. 파일을 구성하고 입력에 포함한 결과를 행동 효과로 확대하지 않는다.

## Project·Work를 유지하면서 Spec·Ticket을 도입한 이유와 비용

논의에서 네 개념은 같은 자리를 놓고 경쟁하는 네 대안이 아니라고 정리했다. Spec은 이루려는 결과와 기준을 명시하고, Ticket은 실행할 일을 식별·배분·추적한다. 이 연구에서 Project는 여러 작업이 공유하는 맥락의 범위이고, Work와 그 Workspace는 한 목표를 추구하며 현재 판단과 진행을 이어가는 범위다.

따라서 별도 goal·constraints와 Spec에서 같은 요구를 각각 관리할 이유는 없었다. 겹치는 정의는 Spec으로 대체했다. 반면 현재 판단, 이전 결과의 의미, 어떤 원자료와 산출물을 선택했는지, 여러 작업에 계속 유효한 Project 맥락은 Spec·Ticket의 존재만으로 없어지지 않는다. 이 부분은 Workspace와 Project의 기존 책임으로 유지했다.

[06 트레이드오프 분석](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md)은 선택 조건과 비교 비용을 검토하는 근거로 읽었다. Spec 도입을 막거나 기존 Work-first를 보존하도록 강제하는 규칙으로 읽지 않았다. 후속 개념 리뷰에서는 “Spec은 판단이 끝난 뒤에만 만든다”, “Ticket은 반드시 한 세션 크기다” 같은 성질을 보편 정의로 확대하지 않았다. 판단의 재검토와 공통 맥락 관리도 Work라는 이름 없이 수행할 수 있다. [비교 질문 정정과 개념 리뷰](../records/2026-09-07-01-session-synthesis.md#9-최종-개념-리뷰와-main의-판단).

이 선택으로 기대하는 이득은 외부 스킬과 같은 개념으로 요구·실행을 전달하고, 실행 묶음이 바뀌어도 Workspace 안에서 전체 상황과 판단을 이어가는 것이다. 감수하는 비용은 Spec 작성·읽기·갱신, Ticket 상태 관리, 전체 state와의 중복 정리, 달라진 판단을 관련 문서와 실행자에게 전달하는 일이다. **충분히 관리되는 Spec-driven 운영보다 별도 Work가 실제로 더 낫다는 비교 증거는 아직 없다.**

특히 기본 Recover가 Spec 다섯 파일 전체를 읽으므로 기존의 짧은 goal·constraints보다 입력과 관리 비용이 늘 수 있다. Ticket 본문을 필요한 것만 읽게 해도 Spec 자체의 팽창 위험이 사라지지는 않는다. 구조가 생겼다는 사실보다 재설명·누락·재작업이 줄었는지를 실제 작업에서 봐야 한다.

## 채택한 파일 구성과 각 내용의 책임

실제 Reference의 Workspace current는 아래와 같다. Spec 하나를 구성한다는 전제로 시작하되, 하나만 허용하거나 새 Spec마다 새 Workspace를 강제하는 정책은 정하지 않았다.

```text
current/
├── memory/
│   ├── index.md
│   ├── spec/
│   │   ├── 01-problem-goal-scope.md
│   │   ├── 02-behavior-and-cases.md
│   │   ├── 03-concepts-and-contracts.md
│   │   ├── 04-quality-and-completion.md
│   │   └── 05-constraints-design-assumptions.md
│   ├── tickets/
│   │   ├── index.md
│   │   └── <ticket>.md
│   └── project-context.md
└── state/
    ├── index.md
    └── status.json
```

**Spec의 다섯 파일**은 다음 이유로 정했다.

1. **문제·목표·범위**는 왜 이 일을 하며 어디까지 이루려는지 정한다. 기반 작업이나 개별 Ticket을 끝낸 사실이 원래 기대한 기능의 완료로 바뀌지 않게 한다. 기존 Workspace goal의 책임을 이 부분이 맡는다.
2. **요구 동작과 대표 사례**는 제품에서 보존해야 할 의미를 구체화한다. 가능한 모든 경우를 나열하는 대신 비슷해 보여도 결과가 달라야 하는 사례를 둔다. 여행 답변 예시에서는 자료의 명시적 제한과 단순한 설명 부재, 답을 못 하는 경우와 처리 실패를 구별했다.
3. **핵심 개념·입출력 계약**은 일을 나누고 전달해도 같은 뜻으로 이해해야 할 대상과 정보의 관계를 정한다. 구체적인 출력 형식 때문에 제품 의미가 사라지지 않도록 한다. 모든 Spec에 JSON·내부 클래스·상세 저장 구조를 미리 요구하는 항목은 아니다.
4. **품질·완료 판단**은 어떤 실제 결과와 근거로 목표 달성을 판단할지 정한다. 연구의 ‘제품 원자료와 실제 동작의 비교’, ‘변경 전후 코드의 비교’를 이번 목표에 관련된 범위에서 적용한다. 개별 테스트가 통과했다는 사실과 확인하지 못한 핵심 수행을 함께 드러낸다.
5. **제약·현재 설계·가정**은 지켜야 할 조건, 현재 고른 방법과 이유, 아직 확인해야 할 전제를 구별한다. 다음 주체가 임시 내부 선택이나 미확인 가정을 모두 고정 제약으로 받지 않게 한다. 새로운 사실이 선택 이유를 흔들면 다시 판단할 수 있어야 한다.

구성과 분량은 다른 문제다. 실제 Recover는 이 다섯 경로를 요구하지만, 작은 작업의 본문까지 크게 만들거나 모르는 내용을 채워 확정하도록 요구하지 않는다. 실행에 필요한 구체성은 유지하고, 미확정은 가정·열린 부분으로 드러낸다. 최종 구성은 일반 Spec 자료와 연구 원문·분석, 확장한 예시 초안, 독립 개선 리뷰를 대조한 뒤 채택했다. [구성 결정의 상세 근거](../records/2026-09-08-01-spec-components-decision.md).

**기존 memory와의 중복**은 대체로 해결했다. `01-goal.md`와 작업별 `02-constraints.md`는 제거했다. 02에 함께 적혀 있던 source·records·output 관리 규칙은 Workspace 운영 문서가 계속 맡는다. Project 문서의 선택과 이유는 Spec의 책임이 아니므로 별도 파일로 유지했고, 옛 순서의 `03`을 없애 `project-context.md`로 이름을 바꿨다. Project 본문을 Spec 안에 복제하지 않는다.

**Ticket**은 `memory/tickets/`에 두고 제목·만들 동작·완료 조건·선행 작업·막힘·진행·결과를 필요에 맞게 함께 적는다. 개발자 Matt Pocock의 [to-tickets 스킬](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/skills/engineering/to-tickets/SKILL.md)을 참고하되 고정 필드·상태 이름·tracker는 채택하지 않았다. 완전한 Matt 운영 방식이나 모든 Ticket의 독립 세션 실행을 도입한 것도 아니다. [자료 비교](../records/2026-09-08-03-ticket-references-and-placement.md)와 [후속 사용자 선택](../records/2026-09-08-07-memory-ticket-placement-decision.md).

Ticket 배치 때문에 memory를 없애거나 정의·진행을 강제로 나눌지도 검토했지만, 최종적으로 memory를 유지하고 함께 읽어야 할 내용은 같은 Ticket에 남기기로 했다. **memory는 오직 잘 바뀌지 않는 문장만 담는다는 해석을 일부 조정한 선택**이다. state는 Workspace 전체의 현재 상황·판단·다음 행동을 맡고, Ticket별 상태를 별도의 정본으로 다시 관리하지 않는다. `status.json`은 기존 Verify의 기계 상태이며 Ticket tracker가 아니다.

**records와 스냅샷**의 경계도 유지한다. 완료한 Ticket은 자연스럽게 남길 수 있고, 상세 과정·변경 이유·보존할 근거는 필요하면 records에 둔다. 완료 때 자동 이동·삭제하거나 매 수정마다 불변 사본을 만들지는 않는다. Spec·Ticket은 해당 Workspace에서 필요하면 갱신하지만, 후속 Workspace와 자동 동기화하는 공유 Spec으로 만들지 않는다. 다른 Workspace에서 필요한 의미를 다시 구성해도 각 작업과 함께 남는 스냅샷 경계를 유지한다. 스냅샷은 작업 중 수정 금지를 뜻하지 않는다.

## 읽기·기록·실행은 어떻게 이어지는가

일반 Workspace 진입은 기존 current 전체를 읽던 흐름을 이어, Spec 전체·Project context 선택·Ticket 색인·전체 state·output 색인과 선택한 Project 본문을 읽는다. 실행을 정하거나 결과를 판단할 때 필요한 Ticket 본문을 추가로 읽는다. Ticket 색인은 제목·하는 일·본문 위치를 안내하며 별도 상태 정본은 만들지 않는다. 모든 Ticket 본문을 기본으로 넣지는 않는다.

**Main과 Maintain의 역할은 기존과 같다.** Main은 사용자와 필요한 설계·작업 분해·위임·결과 확인·다음 행동을 조율한다. Maintain은 대화와 결과를 이해해 무엇을 남길지 판단하고 Spec·Ticket·state와 필요한 records에 기록·갱신한다. ‘기록’은 records 작성이나 기계적 전사만 뜻하지 않는다. Main만 Spec·Ticket을 쓸 수 있다는 독점 규칙이나 Maintain이 일을 배분하는 절차를 추가하지 않았다. [작성 책임 독립 리뷰와 후속 확인](../records/2026-09-08-10-spec-ticket-authorship-independent-review.md).

다른 실행자의 결과가 Main에게 도착한 것과 Maintain 입력·실제 파일에 반영된 것은 다르다. Main은 판단에 필요한 결과·근거·미확인 범위나 정확한 결과 문서 위치를 대화에 연결하고, 실행자에게 문서를 읽힐 때 실제 내용이 준비됐는지 확인한다. 비동기 요청이 접수됐다는 사실만으로 파일 준비를 가정하지 않는다. 이 전달을 자동 수집하는 새 runtime은 만들지 않았다.

연구의 제품 사례에 적용하면 다음과 같다. 아래는 **운용을 설명하는 예시이며 실제 이번 실행 결과가 아니다.**

- 기반 연결과 검증 Ticket을 끝냈지만 실제 모델 판단이 빠졌고 다른 Ticket도 맡지 않는다면, 기반 완료는 유지하면서 빠진 수행을 다음 Ticket으로 다룬다. 전체 state에는 목표 달성에 남은 일을 적는다. 이 사실만으로 Spec의 목표를 기반 구축으로 낮추지 않는다.
- 새 근거가 기존 설계 가정의 부족을 드러낸다면 Spec에서 해당 가정·설계와 영향받는 동작·계약을 다시 판단한다. 그 가정을 실제로 사용한 Ticket과 결과부터 확인하고, 관련 없이 유효한 구현은 유지한다.
- 이번 작업을 넘어 제품 공통 의미가 바뀌었다면 기존 Project context Owner와 갱신 경로에서 다룬다. Spec 편집만으로 Project 전체 기준이 바뀌었다고 보지 않는다.

어느 경우인지 판단하고 실제 실행을 바꾸는 일은 파일 구조가 대신하지 않는다. 연구의 `reconsider-work`가 다루는 판단과 이 구조의 읽기·기록 위치는 연결될 수 있지만, 그 스킬을 설치하거나 실제 공동 운영을 검증한 상태는 아니다.

## 실제로 구현하고 확인한 범위

`dcd3c6f`에는 다음이 들어 있다.

- **샘플 Workspace**: 기존 default-timeout의 제품 기준·결정·코드·테스트에 맞춰 Spec 다섯 파일을 구성했다. Ticket이 없던 샘플에는 색인만 만들고 과거 실행 상태를 추정해 Ticket을 소급 생성하지 않았다. [실제 memory](../../../../reference-project/context/work/workspaces/001-default-timeout/current/memory/index.md).
- **Recover**: 새 필수 파일과 읽기 순서를 적용했다. 기존 packet 형태와 schema 6은 유지했다. 옛 goal·constraints 형식의 Workspace를 자동 변환하는 기능은 없다. [읽기 계약](../../../../reference-project/context/work/harness/recover/README.md).
- **Maintain**: Spec·Ticket 하위 Markdown을 guarded apply로 생성·갱신하게 했다. 새 Ticket은 Ticket 색인에서, 새 Spec·추가 memory는 memory 색인에서 찾을 수 있게 함께 연결한다. 기존 본문의 진행 수정만으로 state·색인을 의무 갱신하지 않는다. Spec·Ticket 운영 문서도 Maintain의 실제 규칙 입력에 넣었다. 파일별 기존 내용 확인은 여러 파일의 동시 갱신 전체나 복수 실행자의 일관성을 보장하지 않는다. [기록·갱신 계약](../../../../reference-project/context/work/harness/maintain/README.md).
- **생성·전환**: 새 Workspace를 구성하는 안내를 맞췄다. 생성·이식 스킬은 기존처럼 현재 canonical을 읽는 경로를 따른다. 제품 구현, Project 공통 내용, Verify 코드·계약·기존 receipt·machine status와 root 자동 Maintain 설정은 바꾸지 않았다. [생성·전환 기준](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md).

검증은 구현 경계와 실제 의미 판단을 구분한다.

- Recover·Maintain operation의 관련 테스트 **51개가 통과**했다. Spec 읽기, Ticket 생성·진행 갱신, 색인 연결, 잘못된 경로·symlink·오래된 파일 내용에 대한 거부를 포함한다.
- 파일명 정리 후 전체 제품·Harness 테스트는 **124개 중 123개 통과, Verify timeout 테스트 1개 실패**였다. 변경 전 `4fe8694`를 별도 임시 디렉터리에 추출해 실행한 전체 검사에서도 같은 테스트가 같은 지점에서 실패했다. 단독 실행은 통과했으며 근본 원인은 미해결이다. 전체 통과로 기록하지 않는다.
- 실제 샘플의 기본 Recover·Workspace를 지정한 Recover·Maintain bootstrap이 성공했고 새 파일 경로를 포함했다. 기존 receipt의 stale 상태를 그대로 읽었으며 제품 Verify를 새로 실행한 증거로 바꾸지 않았다. 변경 Markdown의 로컬 링크와 diff 형식을 확인했다.
- 실제 자동 Maintain이 적절한 문서를 골라 갱신하는지, Main·독립 실행자·다음 세션이 달라진 판단을 받아 실행하는지, 실제 TripProof에서 도움이 되는지는 확인하지 않았다.

상세 변경·테스트·기존 실패 재현은 [Reference 적용 기록](../records/2026-09-08-12-reference-spec-ticket-implementation.md), 파일명 정리 후 검증은 [후속 기록](../records/2026-09-08-13-project-context-filename-and-commit.md)에 있다. 12 기록의 미커밋 표기는 당시 경계이며 후속 사용자 요청에 따라 `dcd3c6f`로 보존했다.

## 연구 측에서 이번 결과를 어떻게 이어 읽으면 되는가

아래는 **연구 문서와 적용 경로를 대조할 지점에 대한 제안**이다. 해당 저장소 문서는 이번 작업에서 수정하지 않았다. 현재 파일 구조로 과거 분석·관찰을 소급해서 다시 쓰는 대신, 어떤 선택이 바뀌었고 무엇이 계속 유효한지 구별할 수 있다.

**01 문제 분석과 04 장면 분석**의 문제의식은 유지된다. 국소 완료가 전체 목표를 대신한 문제, 과거 선택을 확정 전제로 받은 문제는 이번 설계의 이유다. Spec에 관련 항목을 넣고 Recover로 읽힌 것은 대응 기반이며 해결의 행동 증거가 아니다.

**02 Workspace 방향**과는 실제 설계 차이가 있다. 기존 문서는 독립 Spec을 기본 작업 단위로 유지하지 않고, 상세 plan·task·AC를 기본 current에 두지 않는 방향이었다. 이번에는 Spec을 Workspace 내부의 작업 정의로 두고 다섯 파일 전체를 기본으로 읽는다. 따라서 “기존과 모두 같다”고 설명하면 안 된다. Spec·Ticket을 실제로 지칭하고 전달할 필요를 받아들여 내용·기본 읽기 범위를 바꾼 것이다. Workspace별 스냅샷, 선택한 Project context, current와 records의 구별은 유지한다.

**03 Project context foundation**의 공통 맥락과 작업별 맥락 구별도 유지된다. `project-context.md`는 선택과 이유를 안내하고, 정확한 기계 선택 목록은 기존 `recover.json`이 맡는다. 이번 Spec이 Project 공통 목적·기준이나 상세 제품 Owner를 대신하지 않는다. 선행 Project context 통합은 009의 작업이고, 이번 010의 성과로 합치지 않는다.

**05의 현재 판단 연속성 설계와 reconsider-work v0**에서는 “현재 작업 계획이나 current에 반영한다”는 말을 실제 적용 위치에 연결할 수 있게 됐다. 작업 목표·요구·설계는 Spec, 실행 정의·진행은 Ticket, 전체 상황·다음 행동은 state, 상세 판단 경위는 records, 여러 작업에 유효한 변화는 Project의 기존 Owner가 후보가 된다. 이 연결은 적용 시 확인할 위치이며 모든 사건마다 전부 갱신하라는 뜻은 아니다. [현재 v0 사용 안내](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/05-judgment-continuity-solution-direction/v0/README.md)가 요구하는 ‘실제 작업과 다음 실행까지 이어지는지’는 여전히 확인해야 한다. 이 전달을 위해 archive나 연결된 private JSONL을 읽지 않았다.

**06 트레이드오프 분석**의 “필요하면 일시적 실행 산출물로 Spec·Ticket을 사용할 수 있다”는 후보 관계는 Context Harness에서 더 구체화됐다. Spec은 기본 작업 정의이고 Ticket은 필요할 때 작성해 memory에 자연스럽게 유지한다. 반면 한 세션 크기·독립 구현 조각·상태 체계 등 Matt의 규율을 모두 채택한 것은 아니다. 비교 기준은 문서 수나 이름보다 실제 전달 정확성, 판단 갱신, 중복·팽창과 관리 비용에 계속 두어야 한다.

다음 실사용에서는 Ticket 완료 뒤 무엇이 가능해졌는지, 필요한 수행이 빠지면 목표를 유지하고 다음 일을 고치는지, 달라진 가정이 관련 Ticket과 다음 실행자에게 실제로 전달되는지를 볼 수 있다. Spec·Ticket·state를 관리하는 비용과 중복도 함께 관찰해야 한다. 이 확인은 새 고정 승인 절차나 모든 Ticket마다 전체 목표를 재평가하는 규칙이 아니다.

## 근거를 더 읽을 때

현재 결정을 재검토할 필요가 있을 때만 아래 자료를 선택해서 읽는다. 이 목록 전체를 수신 세션의 필수 입력으로 삼지 않는다.

- [010 current memory](../current/memory.md): 지금 유지할 합의와 열린 부분. 진행·검증은 [state](../current/state.md)가 소유한다.
- [첫 논의 종합](../records/2026-09-07-01-session-synthesis.md): 도입 이유, 공유 Spec 정정, memory/state 역사, 개념 트레이드오프와 초기 리뷰. 당시 미결정 표기는 후속 합의 이전의 상태다.
- [구성 결정 기록](../records/2026-09-08-01-spec-components-decision.md): 연구 01~04와 05의 현재 문서, 두 회고 원문, 외부 Spec 자료와 초안·리뷰를 대조한 경위. 원래 회고는 연구의 [conceptual 원문](../../../../../memory-harness-research/context/source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-conceptual.md)과 [chronological 원문](../../../../../memory-harness-research/context/source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-chronological.md)에서 찾는다.
- [Spec 범위·배치 결정](../records/2026-09-08-02-workspace-spec-scope.md), [Ticket 최종 배치 결정](../records/2026-09-08-07-memory-ticket-placement-decision.md), [Main·Maintain 역할 확인](../records/2026-09-08-10-spec-ticket-authorship-independent-review.md): 후보와 최종 사용자 선택을 구별하는 원문 근거.
- [구성 설명](spec-components-and-rationale.md)과 [구체적인 예시 Spec](spec-example-travel-answer.md): 본문과 이유를 따로 읽도록 채택한 두 산출물. 예시의 API·수치·정책은 실제 TripProof 계약이나 모든 Spec의 필수 조건이 아니다.

설계 기록 커밋은 `6982fbe`(구성요소·이유), `5320930`(배치·기존 current 대체), `4fe8694`(Ticket·역할 등 설계 종합)이고, 실제 Reference 적용 커밋은 `dcd3c6f`다. 연구 측 자료는 2026-09-08 접근한 본문을 기준으로 연결했으며 외부 자료의 최신 사양을 새로 조사한 보고서는 아니다. 로컬 링크는 같은 Desktop 아래의 두 저장소 배치를 기준으로 한다.
