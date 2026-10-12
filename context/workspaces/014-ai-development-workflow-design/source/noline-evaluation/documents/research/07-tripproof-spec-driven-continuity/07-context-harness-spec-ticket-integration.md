# Context Harness의 Spec·Ticket 통합 결과와 연구 후속 기준

작성·확인일: 2026-09-08

## 현재 결과와 이 문서의 역할

Context Harness의 실행 가능한 기준 Project인 `reference-project/`에 **Spec과 Ticket을 실제 개념·파일로 도입했다.** Spec은 기존 Workspace의 goal·작업별 constraints를 대체하고, Ticket은 실행할 일의 정의와 진행·결과를 함께 관리한다. Workspace는 이 작업의 기준·현재 판단·원자료·산출물·기록을 함께 유지하는 범위로 남는다.

이 문서는 context-harness에서 마친 설계·구현을 이 연구의 기존 분석과 연결한다. 다음 세션은 여기서 채택한 내용, 이전 방향과 달라진 부분, 구현·검증 범위와 열린 사항을 파악한 뒤 필요한 원자료만 추가로 읽을 수 있다. Spec·Ticket을 다시 자체 용어로 바꾸거나 도입 여부부터 재논의하는 것을 기본으로 삼지 않는다.

채택·구현된 곳과 아직 적용하지 않은 곳을 구별한다.

- **Context Harness Reference:** 합의한 구조, Recover의 읽기, Maintain의 기록·갱신, 생성·전환 안내를 구현했다. 구현 커밋은 `dcd3c6f`다.
- **Context Harness root의 연구 Workspace:** 기존 `current/memory.md`·`state.md` 형식을 유지한다. 이번에 root 자동 Maintain을 다시 연결하지 않았다.
- **memory-harness-research와 실제 TripProof:** 이 구성을 이식한 상태가 아니다. 이 연구에 분석을 보존한 것과 Workspace·Harness를 변경한 것은 다르다.

실제 Reference 운영 기준은 context-harness의 [Workspace의 Spec과 Ticket](../../../../context-harness/reference-project/context/work/workspaces/SPEC-AND-TICKETS.md)이 소유한다. 이 문서는 해당 기준의 두 번째 운영 정본이나 자동 동기화 대상이 아니다. 아래 내용은 확인일과 구현 커밋을 기준으로 한 연구 분석이다.

## 도입 이유와 기존 비교에서 달라진 전제

직접적인 도입 이유는 스킬 작성·작업 분해·인계에서 작업 정의와 실행 단위를 명확하게 지칭할 필요였다. “current를 바탕으로 작업한다”만으로는 어떤 요구를 정리하고 어떤 실행을 맡기는지 표현하기 어려웠다. 외부 개발 자료가 사용하는 Spec·Ticket을 매번 자체 표현으로 바꾸는 것도 해석·관리 비용이었다.

따라서 이번 선택은 익숙한 Spec·Ticket을 사용하면서 기존 Workspace 구조를 수정하는 방향이다. 특정 spec-driven 체계 전체를 그대로 가져오거나, Spec·Ticket의 역할을 잘게 나눠 다른 이름의 대체물을 만드는 방향은 아니다.

[06 트레이드오프 분석](06-work-first-spec-ticket-tradeoff-analysis.md)은 선택 이유와 비용을 검토하는 배경이었다. 독립 Spec을 기본으로 두지 않던 과거 Work-first를 보존하도록 강제하는 규칙으로 사용하지 않았다. 또한 Matt의 특정 운영 방식에서 확인한 다음 성질을 보편적인 정의로 확대하지 않았다.

- Spec을 반드시 모든 판단이 끝난 뒤에만 작성한다는 조건
- Ticket이 반드시 한 세션 크기이며 독립된 구현 조각이어야 한다는 조건
- 판단 재검토와 공통 맥락 관리를 Work라는 이름만의 고유 기능으로 보는 해석

Spec은 요구하는 결과와 기준을 명시하고, Ticket은 실행할 일을 식별·배분·추적한다. Project는 여러 작업이 공유하는 맥락의 범위이고, Work와 그 Workspace는 한 목표를 추구하며 판단과 진행을 이어가는 범위다. 충분히 관리되는 Spec-driven 운영보다 별도 Work를 두는 편이 실제로 더 낫다는 비교 증거는 아직 없다.

## 채택한 current 구성

Reference의 구성은 다음과 같다. 우선 Spec 하나를 구성하는 형태를 사용하지만, Workspace마다 하나만 허용하거나 새 Spec마다 새 Workspace를 강제하는 정책은 정하지 않았다.

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

### Spec이 맡는 내용과 다섯 파일의 이유

**문제·목표·범위**는 해결할 문제, 사용자가 얻을 결과, 포함·제외 범위와 중요한 선행 조건을 정한다. 기존 Workspace goal의 책임을 맡는다. 일부 Ticket이나 연결 기반의 완료가 원래 기대한 기능의 완료로 바뀌지 않도록 실제 목적을 드러낸다.

**요구 동작과 대표 사례**는 제품에서 보존해야 할 의미를 구체화한다. 가능한 모든 상황을 열거하기보다 비슷해 보여도 결과가 달라야 하는 사례를 둔다. 예를 들어 자료의 명시적 제한과 단순한 설명 부재는 다른 결론으로 이어져야 한다. 사례는 의미를 구별하는 기준이며 단순한 장식이 아니다.

**핵심 개념·입출력 계약**은 일을 나누고 전달해도 같은 뜻으로 다뤄야 할 대상과 정보의 관계를 정한다. 필요한 부분 결과와 오류의 의미도 표현한다. 모든 Spec에 JSON, 내부 클래스나 상세 저장 구조를 미리 요구하는 항목은 아니다.

**품질·완료 판단**은 어떤 실제 결과와 근거로 목표 달성을 판단할지 정한다. 기존 연구의 ‘제품 원자료와 실제 동작의 비교’, ‘변경 전후 코드의 비교’를 이번 목표에 관련된 범위에서 적용한다. 테스트가 확인한 범위와 미확인 핵심 수행을 구별하며, 모든 Ticket마다 제품 전체를 재검토하는 의무로 만들지 않는다.

**제약·현재 설계·가정**은 지켜야 할 조건, 현재 선택한 방법과 이유, 아직 확인해야 할 전제를 구별한다. 다음 실행자가 임시 내부 선택이나 가정까지 고정 제약으로 받아들이지 않게 한다. 구현이 빠졌다면 구현을 고칠 문제일 수 있고, 요구대로 구현해도 의도한 결과를 얻지 못했다면 요구나 설계 가정을 다시 볼 수 있다. 결과가 부족하다는 이유만으로 목표를 낮추거나 현재 코드에 Spec을 맞추지 않는다.

다섯 파일의 구성과 분량은 별개다. Recover는 다섯 경로를 필수로 요구하지만, 작은 작업까지 긴 본문으로 채우거나 모르는 내용을 확정하도록 요구하지 않는다. 실행에 필요한 구체성은 유지하고 미확정은 가정·열린 부분으로 표현한다.

### 기존 memory와 Ticket·state의 관계

기존 `01-goal.md`와 작업별 `02-constraints.md`는 Spec으로 대체했다. 같은 작업 정의를 별도로 유지하지 않는다. 옛 constraints에 함께 있던 source·records·output 관리 규칙은 Workspace 운영 문서가 계속 맡는다. Project 문서의 선택과 이유는 Spec의 책임이 아니므로 별도 `project-context.md`로 유지하며, Project 본문을 Spec에 복제하지 않는다.

Ticket은 `memory/tickets/`에 두고 제목·만들 동작·완료 조건·선행 작업·막힘·진행·결과를 필요한 만큼 함께 적는다. Matt의 `to-tickets`를 참고하되 고정 필드·상태 이름·tracker를 채택하지 않았다. **Ticket의 정의와 진행을 같은 본문에 두는 것은 사용자와 논의해 정한 선택**이다. memory가 잘 바뀌지 않는 내용만 담아야 한다는 해석 때문에 함께 읽을 내용을 분리하지 않는다.

`state/index.md`는 Workspace 전체의 현재 상황·판단·다음 행동을 맡는다. 필요한 Ticket 상황을 종합할 수 있지만, 개별 상태의 두 번째 정본으로 관리하지 않는다. Ticket 색인도 제목·하는 일·본문 위치를 안내하며 별도 상태 장부가 아니다. `status.json`은 기존 Verify의 기계 상태이며 Ticket tracker가 아니다.

완료한 Ticket은 자연스럽게 남길 수 있다. 상세 과정·변경 이유·근거를 보존할 필요가 있으면 records를 사용한다. 완료 때 자동 이동·삭제하거나 매 수정마다 불변 사본을 만들지는 않는다.

### Workspace별 스냅샷의 의미

Spec·Ticket은 해당 Workspace 안에서 필요하면 수정한다. 작업과 함께 남으며, 후속 Workspace나 Project의 변화에 맞춰 과거 작업 문서를 계속 최신화할 의무는 없다. 다른 Workspace에서 필요한 의미를 새로 구성하더라도 공유 Spec으로 자동 전파·상호 갱신하지 않는다.

이 스냅샷 경계는 작업 중 수정을 금지하는 불변성 규칙이 아니다. 현재 판단을 수정할 수 있다는 사실과 모든 과거 Workspace를 계속 현재 상태로 유지한다는 정책은 구별한다.

## 읽기·기록·실행에 적용한 방식

### 기본 재진입과 개별 실행

일반 Recover는 memory 색인, Spec 전체, Project context 선택과 추가 memory, Ticket 색인, 전체 state, output 색인과 선택한 Project 본문을 읽는다. 실행할 Ticket을 정하거나 결과를 판단할 때 필요한 본문을 작업 주체가 추가로 읽는다. 모든 Ticket 본문을 기본 입력에 넣거나 자동 선택하는 장치를 만든 것은 아니다.

Spec 전체를 기본 재진입에 포함하는 방향은 사용자와 정했다. Ticket 색인까지만 기본 packet에 넣는 세부 방식은 그 합의 안에서 Main이 선택한 구현 기본값이다. 개별 실행자에게 Spec 전체나 일부 중 무엇을 읽힐지, 무엇을 직접 쓰게 할지는 실제 위임에 맞게 정할 수 있다. 모든 Ticket의 위임·새 세션 실행은 의무가 아니다.

### Main과 Maintain

Main은 사용자와 설계·작업 분해·위임·결과 확인·다음 행동을 조율한다. Maintain은 대화와 결과를 이해해 무엇을 남길지 판단하고 Spec·Ticket·state와 필요한 records를 기록·갱신한다. 기록은 단순 전사나 records 작성만을 뜻하지 않는다. Main만 Spec·Ticket을 작성할 수 있다는 규칙도 추가하지 않았다.

구현에서는 Maintain의 허용 경로에 `memory/spec/`와 `memory/tickets/` 바로 아래 Markdown을 추가했다. 새 Ticket은 Ticket 색인에, 새 Spec·추가 memory는 memory 색인에 같은 변경 제안으로 연결한다. 기존 Ticket 본문의 진행 수정만으로 색인과 전체 state의 동시 갱신을 강제하지 않는다. Spec·Ticket 운영 기준도 Maintain의 실제 규칙 입력에 포함했다.

파일별 기존 내용 확인과 경로 검사는 여러 파일이 한꺼번에 갱신되거나 복수 실행자가 함께 수정할 때의 일관성까지 보장하지 않는다. 개별 실행자의 쓰기 범위와 결과 반영 방식은 실제 적용에서 확인해야 한다.

다른 실행자의 결과가 Main에게 도착한 것과 Maintain 입력·실제 파일에 반영된 것은 다르다. Main은 다음 판단에 필요한 결과·출처·미확인 범위나 정확한 결과 문서 위치를 대화에 연결하고, 실행자에게 문서를 읽히기 전에 필요한 내용이 실제로 준비됐는지 확인한다. 비동기 요청의 접수를 파일 준비로 간주하지 않는다. 결과 자동 수집이나 새로운 조율 runtime을 만든 것은 아니다.

### 실행 결과에 따른 판단과 반영

아래는 채택한 운영을 설명하는 사례이며 이번 Reference에서 실제 수행한 제품 작업의 증거는 아니다.

- 연결 기반과 검증 Ticket을 끝냈지만 실제 모델 판단이 빠졌고 다른 Ticket도 맡지 않는다면, 기반의 완료는 유지하면서 빠진 수행을 다음 Ticket으로 다룬다. 전체 state에는 목표 달성에 남은 일을 적는다. Spec의 목표를 기반 구축으로 낮추지 않는다.
- 새 근거가 설계 가정의 부족을 드러낸다면 Spec의 해당 가정·설계와 영향받는 동작·계약을 다시 판단한다. 그 가정을 실제로 사용한 Ticket과 결과부터 확인하며, 관련 없이 유효한 구현은 유지한다.
- 여러 작업에 유효한 제품 의미가 바뀌면 기존 Project 담당 위치와 갱신 경로에서 다룬다. 작업별 Spec 편집만으로 Project 전체 기준이 바뀐 것은 아니다.

이는 [판단 연속성 설계](05-judgment-continuity-solution-direction/04-solution-direction.md)가 요구한 판단·행동·기존 결과의 연결을 표현할 위치를 제공한다. 어떤 상황인지 판단하고 실제 실행을 바꾸는 능력까지 파일 구조가 보장하지는 않는다.

## 구현과 검증의 확인 범위

Reference 샘플 `001-default-timeout`은 기존 제품 기준·결정·코드·테스트를 바탕으로 Spec 다섯 파일을 구성했다. 여행 답변 예시를 샘플 제품 계약으로 복사하지 않았다. 샘플에는 Ticket 색인만 있고, 과거 실행을 추정해 Ticket을 소급 작성하지 않았다.

Recover는 새 필수 파일과 읽기 순서를 적용했고 packet schema 6을 유지했다. 옛 goal·constraints 형식의 Workspace를 자동 변환하는 기능은 없다. Maintain의 경로·색인 연결과 생성·전환 안내도 맞췄다. 제품 코드·Project 공통 내용·Verify 코드·계약·기존 receipt·machine status와 root 자동 Maintain 설정은 이번 변경에서 바꾸지 않았다.

검증 기록이 보고한 결과는 다음과 같다. 이 연구에서 테스트를 새로 실행한 결과가 아니다.

- Recover·Maintain operation 관련 **51개 테스트 통과**. Spec 읽기, Ticket 생성·진행 갱신, 색인 연결, 잘못된 경로·symlink·오래된 파일 내용 거부를 포함한다.
- 전체 제품·Harness 테스트 **124개 중 123개 통과, Verify timeout 테스트 1개 실패**. 변경 전 `4fe8694`의 전체 119개 검사에서도 같은 테스트가 같은 지점에서 실패했고, 단독 실행은 통과했다. 근본 원인은 미해결이며 전체 통과로 기록하지 않는다.
- 실제 샘플의 기본·명시 Workspace Recover와 Maintain bootstrap 성공을 기록했다. 기존 receipt의 stale 상태는 그대로 읽었으며, 제품 Verify를 새로 실행한 증거로 바꾸지 않았다.
- 수정 Markdown의 로컬 링크와 diff 형식을 확인했다고 보고했다.

수신 시점에는 구현 커밋의 존재, 현재 Reference와 해당 커밋 사이에 구현 차이가 없다는 점, 새 Recover 필수 입력, Maintain의 허용 경로·색인 연결, Verify 등 비변경 범위를 코드·기록으로 대조했다. 중요한 전달문–실체 불일치는 확인하지 못했다.

아직 확인하지 않은 것은 자동 Maintain이 적절한 내용을 선택해 갱신하는지, Main·독립 실행자·다음 세션이 달라진 판단을 실제로 인수하고 실행하는지, TripProof에서 재설명·누락·재작업이 줄어드는지다. 관련 스킬의 설치나 공동 운영 효과도 이번 구조 구현으로 검증한 것이 아니다.

## 기존 연구에 유지할 것과 바뀐 것

**01 문제 분석과 04 장면 분석의 문제의식은 유지한다.** 개별 완료가 전체 목표를 대신하거나 과거 선택이 확정 전제가 되는 문제는 이번 설계의 이유다. 관련 내용을 Spec에 넣고 기본으로 읽혔다는 사실은 대응 기반이며 해결 효과가 아니다.

**02 Workspace 방향에는 실제 변경이 생겼다.** [당시 채택 방향](02-workspace-based-continuity-direction.md)은 독립 Spec을 기본으로 유지하지 않고 상세 plan·task·AC를 기본 current에서 제외했다. 이번 Reference는 Spec을 내부 작업 정의로 두고 다섯 파일 전체를 기본으로 읽는다. 기존과 모두 같다고 설명하거나 옛 기본값을 현재 Reference의 규칙으로 적용하면 안 된다. Workspace별 스냅샷, 선택한 Project context, current와 records의 구별은 유지한다.

**03 Project context foundation의 경계는 유지한다.** [Project 공통 맥락과 작업별 맥락](03-project-context-foundation-direction.md)은 계속 구별된다. `project-context.md`는 선택과 이유를, `recover.json`은 정확한 기계 선택 목록을 맡는다. Spec이 Project 공통 목적·기준이나 상세 제품 담당 위치를 대신하지 않는다. 선행 Project context 통합은 context-harness의 별도 작업이며 이번 통합의 성과로 합치지 않는다.

**05의 판단 반영 위치는 더 구체화됐다.** [현재 판단 연속성 설계와 v0](05-judgment-continuity-solution-direction/README.md)의 작업 목표·요구·설계는 Spec, 실행 정의·진행은 Ticket, 전체 상황·다음 행동은 state, 상세 판단 경위는 records, 여러 작업에 유효한 변화는 Project의 기존 담당 위치에 연결할 수 있다. 모든 사건마다 전부 갱신하라는 뜻은 아니다. 실제 적용 때 읽기·쓰기 위치와 후속 실행까지 이어지는지 확인해야 한다.

**06 트레이드오프 분석의 후보 관계는 Reference에서 구체화됐다.** [비교 분석](06-work-first-spec-ticket-tradeoff-analysis.md)의 “필요하면 일시적 실행 산출물로 Spec·Ticket을 사용할 수 있다”에서, Spec은 기본 작업 정의이고 Ticket은 필요할 때 작성해 memory에 유지하는 구조로 바뀌었다. Matt의 모든 실행 규율을 함께 채택한 것은 아니다. 과거 분석은 당시 비교의 근거로 보존하고 이 후속 결과와 구별해 읽는다.

[판단 연속성과 이해 지원의 공동 적용 준비본](06-judgment-and-understanding-application/README.md)은 별도 산출물이다. 준비본의 존재와 이번 Reference 통합을 합쳐 설치·공동 운영 완료로 주장하지 않는다. 실제 대상에 적용할 때 현재 실행 지침과 이 구조의 관계를 대조한다.

## 다음 세션에서 이어갈 기준

Spec·Ticket 도입, 다섯 Spec 구성, memory 유지, goal·constraints 대체와 Main·Maintain의 기존 역할은 Reference에서 채택한 내용으로 이어받는다. Ticket 상세 형식·상태 체계, 개별 실행자의 입력·쓰기 범위, 엄격한 Spec 개수 제한은 결정하지 않은 상태로 둔다.

연구를 이어갈 때는 이 결과가 어떤 기존 설명을 바꾸는지 먼저 대조한다. 실제 이식을 요청받았다면 대상의 현재 구조와 운영 기준을 확인하고 적용 범위를 정한다. 이번 분석 보존만으로 이식·Workspace 전환·스킬 설치를 수행하거나 완료한 것으로 취급하지 않는다.

실사용에서는 Ticket 완료로 무엇이 가능해졌는지, 핵심 수행이 빠지면 목표를 유지하고 다음 일을 고치는지, 달라진 가정이 관련 Ticket과 다음 실행자에게 전달되는지를 볼 수 있다. Spec 전체를 읽고 관리하는 부담, Ticket·state의 중복과 반영 지연도 함께 관찰해야 한다. Spec 다섯 파일이 기본 입력이 되었으므로 기존의 짧은 goal·constraints보다 입력·갱신 비용이 늘 수 있다. Ticket 본문을 선택해 읽는 것만으로 Spec 팽창 위험이 없어지지는 않는다.

이 관찰은 모든 Ticket마다 고정 리뷰나 승인 절차를 추가하는 요구가 아니다. 실제 작업 선택·근거 해석·후속 행동이 달라지는지 확인하기 위한 판단 기준이다.

## 근거와 재접근

원자료는 별도 `context-harness` 저장소에 있다. 아래 링크는 두 저장소가 같은 상위 디렉터리에 있는 배치를 기준으로 하며, 다른 배치에서는 해당 checkout의 저장소 상대 경로로 찾는다. 본문의 판단을 이해하기 위해 연결된 records 전체를 읽을 필요는 없다.

- **주 전달문:** `context-harness`의 `context/workspaces/010-spec-ticket-workspace-design/output/research-feedback-spec-ticket-integration.md`. [전달문](../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/output/research-feedback-spec-ticket-integration.md)은 `9505bf31521ec40e09a9608c815566f2d89e3dc1`에 보존됐다.
- **실제 구현 기준:** `dcd3c6fa957102894bc6e4629923bc90fca5aefc` — `feat: integrate workspace spec and tickets`. [Spec·Ticket 운영 기준](../../../../context-harness/reference-project/context/work/workspaces/SPEC-AND-TICKETS.md), [Recover](../../../../context-harness/reference-project/context/work/harness/recover/README.md), [Maintain](../../../../context-harness/reference-project/context/work/harness/maintain/README.md)을 확인했다. 구현을 다시 대조할 때는 최신 파일과 이 commit을 구별한다.
- **사용자 선택과 열린 부분:** [010 memory](../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/current/memory.md)와 [state](../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/current/state.md). Spec·Ticket의 세부 결정과 구현 기본값의 지위를 구분하는 근거다.
- **설명과 예시:** [Spec 구성 이유](../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/output/spec-components-and-rationale.md), [여행 답변 예시](../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/output/spec-example-travel-answer.md). 예시의 API·수치·기능 정책은 실제 TripProof 계약이나 모든 Spec의 공통 요구가 아니다.
- **검증 기록:** [Reference 적용 기록](../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/records/2026-09-08-12-reference-spec-ticket-implementation.md), [파일명 정리와 최종 커밋 기록](../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/records/2026-09-08-13-project-context-filename-and-commit.md). 앞 기록의 미커밋 표기와 옛 파일명은 당시 상태이며 뒤 기록이 후속 변경을 설명한다.

링크 없이도 중요한 선택의 의미를 재검토할 수 있도록 주 전달문의 핵심 문장을 함께 보존한다.

> 기존 Workspace의 goal·constraints는 Spec이 대체하고, Ticket은 실행할 일의 정의와 진행을 함께 관리한다.

> 개별 실행자의 입력·쓰기 범위와 Ticket의 상세 형식은 열어 두었다.

> memory는 오직 잘 바뀌지 않는 문장만 담는다는 해석을 일부 조정한 선택

첫 두 인용은 전달문의 ‘이번에 무엇이 달라졌는가’, 마지막은 ‘채택한 파일 구성과 각 내용의 책임’에 있다. 이 문서의 구조·의미·검증 요약은 확인한 전달문과 운영 기준에서 재구성했으며, 새로운 제품 요구나 적용 효과를 추가하지 않았다.
