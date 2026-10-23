# Development 스킬의 진입점·상세 구성 제안

후속 적용: Personal 범위 정정과 Astra high 개선 리뷰 뒤 사용자가 적용을 요청했다. 현재 실물과 확인 범위는 [적용 기록](2026-10-23-development-skill-prototype-adoption.md)을 따른다. 아래 제안·미실행 표기는 그 당시 상태다.

사용자는 지금까지 논의를 prototype에 구체화하되 development 전용 스킬과 그 안의 검토 reference 등으로 구성하고 싶다고 했다. 후속으로 DEVELOPMENT 진입점 자체의 이전도 제안했다. **Main의 추천은 개발 절차의 진입점과 본체를 `skills/development/SKILL.md`로 옮기고, 구현·검토·검증의 실행 상세를 함께 관리하는 것이다.** 현재는 구성 제안이며 실제 스킬 생성·본문 이전·운영 연결은 하지 않았다.

이미 확정한 [1~5번 판단·책임](2026-10-23-main-review-disposition-proposal.md#후속-확정--5번과-판단책임-묶음의-마무리)은 입력으로 유지한다. 구체 파일명·분할 깊이·호출 조건과6~15번의 실행 세부가 이번 구상으로 일괄 확정된 것은 아니다.

## 사용자 구상과 뒤이은 보완

현재 대화의 최소 원문을 보존한다. 아래는 사용자 구상이고, 이후 구성표·이전 순서는 Main의 추천이다.

> 형탸는 단순히 가이던스가 아니라 스킬에 추가하고 싶어 development 전용으로 스킬을 만들어서 검토와 같은 이런 래퍼런스도 같이 두는형태 그리고 스킬을 좀 계층적으로 만들고 싶어 안에서 라우팅 까지 아니더라고 내용이 쌓이는거지 하나 스킬에는 실제 방대하기도 하니까

> 참고로 진입점 DEVELOPMENT 도 옮기는게 나아보이기도 하고

핵심은 기존 문서를 그대로 둔 채 호출용 포장만 추가하는 데 있지 않다. 개발할 때 실제 사용하는 절차와 관련 상세가 한 스킬 안에서 성장하도록 구성하려는 의도다. 계층적 구성을 곧바로 복잡한 자동 분기나 여러 에이전트의 계층으로 해석하지 않는다.

## 현재 구조에서 확인한 것

- [기존 DEVELOPMENT](prototypes/development-workflow/skills/development/_background/evidence/development-before-skill.txt)는 입력 선택·구현·검토·갱신을 설명하지만 자동 호출 스킬은 아니다. 최근 합의 이전의 검토자 직접 수정 흐름도 남아 있어 단순 이동만으로 최신 설계 적용이 되지 않는다.
- [prototype의 skills](prototypes/development-workflow/skills/README.md)에는 작업 논의·브리핑·설명 복구와 공유 기준이 있다. 개발 절차의 전용 스킬을 추가할 기존 위치가 있다.
- [스킬 본문 정책](prototypes/development-workflow/skills/SKILLS-CONTENT-POLICY.md)은 SKILL.md가 목적·호출·핵심 판단·행동을 소유하고, 조건별 실행 상세는 references 등에, 형성 이유는 _background에 두도록 한다. 파일 수나 깊이를 의무화하지 않는다.
- [체계 지침](prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md)은 기존 진입을 주변 정리만으로 이동하지 말라는 기준이다. 실제 진입 구조를 변경하는 이번 제안을 금지하지 않으며, 위치 변경과 함께 본문 책임·현재 참조를 맞추도록 한다.

## 외부 구성과 우리에게 가져올 부분

| 자료 | 원자료에서 확인한 구성 | 이번 추천에 연결할 점 |
| --- | --- | --- |
| [Lauren의 poteto-mode](../source/workflow-references/pstack/repository/skills/poteto-mode/SKILL.md) | 상위 스킬이 작업별 playbook과 형제 스킬·원칙 스킬을 연결한다. Main이 playbook을 수행한다. | 공통 운영과 조건별 상세를 구별한다. 원칙까지 모두 leaf skill로 바꾸거나 원본의 모든 호출을 가져오지는 않는다. |
| [Lauren의 interrogate](../source/workflow-references/pstack/repository/skills/interrogate/SKILL.md) | 검토 수행 본문에서 reviewer prompt·rubric·code quality·lead judgment를 각각 연결한다. | 검토 수행과 Main의 의견 판단은 관련돼 있어도 서로 다른 읽기 목적을 가질 수 있다. 우선 한 검토 상세에 설명하고 분량·독자가 실제로 갈리면 더 나눌 수 있다. |
| [Matt의 implement](../source/workflow-references/matt-pocock/repository/skills/engineering/implement/SKILL.md)·[code-review](../source/workflow-references/matt-pocock/repository/skills/engineering/code-review/SKILL.md) | 구현 스킬이 별도 검토 스킬을 호출한다. 검토는 Standards와 Spec을 분리해 반환한다. | 독립적으로 요청·재사용할 작업은 별도 스킬이 될 수 있다. 지금 곧바로 역할마다 스킬을 하나씩 만들 근거로 삼지는 않는다. |
| [Vercel product-design 자료](../source/lectures/vercel-product-design%20%281%29.md) | SKILL.md가 실행 흐름을 소유하고 작업·surface별 references를 선택한다. 다른 Owner의 canonical은 복제하지 않는다. | 한 진입점과 필요한 상세의 구성, Personal·Project 정본을 받아 사용하는 관계가 우리 제안에 가깝다. 외부 시스템 전체의 효과가 우리 환경에서도 확인됐다는 뜻은 아니다. |

## 추천하는 책임과 파일 구성

파일명은 논의용이며 모두 지금 생성하자는 뜻은 아니다. 구현·검증 상세는 남은 항목을 구체화하면서 채운다.

```text
skills/development/
├── SKILL.md
├── references/
│   ├── implementation.md
│   ├── review.md
│   └── verification.md
└── _background/
```

| 위치 | 소유할 내용 |
| --- | --- |
| SKILL.md | 개발 작업의 목적·적용 조건, Main의 전체 책임, 구현·검토·검증 관계, Personal·Project·Spec/Ticket을 사용하는 공통 원칙, 현재 작업에 필요한 상세를 읽는 조건. 파일 목록만 남기지 않는다. |
| implementation.md | 구현자의 구체 설계·구현·자기 확인·검토 전 완성 책임과 Main에게 넘길 내용.6번부터 구체화할 실행 상세다. |
| review.md | 공유 기준으로 독립 판단하는 목적·범위·강도, 요구 위반과 개선 의견의 근거, Main의 채택·조정·기각·추가 확인·사용자 연결. 정확한 입력·권한·반환은 후속 항목을 연결한다. |
| verification.md | 수정된 결과의 요구·계약 충족과 증거 충분성, 수정 후 확인·종료 연결. 검토의 대안 탐색과 구별하며12번·01-03에서 구체화한다. |
| _background | 원래 사용자 목적, 기준 공유로 바뀐 이유, Personal과 workflow의 책임 구분, 외부에서 가져오거나 달리 정한 부분과 최소 원문. 일상 실행의 필수 입력으로 만들지 않는다. |

SKILL.md와 상세 파일은 같은 실행 지침의 서로 다른 범위를 소유한다. references라는 이름이 단순 참고용이나 선택적으로 무시할 자료라는 뜻은 아니다. 그 절차를 수행할 때 필요한 상세라면 읽을 조건을 진입 본문에서 밝힌다. 동시에 상세를 나눴다는 이유로 모든 작업에서 모든 파일을 읽게 하지 않는다.

검토 내용이 커지고 검토자와 Main이 읽을 내용이 뚜렷이 갈리면 `references/review/reviewer.md`, `references/review/main-judgment.md`처럼 나눌 수 있다. 지금부터 빈 하위 폴더·중간 색인을 늘리지는 않는다. 별도 스킬 분리는 독립 호출 목적·결과·사용처가 생길 때 판단한다. 문서의 깊이와 스킬 수, 에이전트 수는 각각 다른 선택이다.

## 기존 소유 관계는 유지한다

- Personal은 지속할 개발 판단의 의미·조건·절충을 소유한다.4번의 A·B 반영은01-02에서 해당 본문에 통합한다. development의 검토 기준 목록으로 복제하지 않는다.
- Project는 해당 제품의 약속·개발 규약·현재 사실을 소유한다.
- Work의 Spec/Ticket·current·records·output은 이번 목표·선택·진행·결과를 소유한다.
- development 스킬은 이 입력을 읽고 작업을 배치하며, 결과를 판단·수정·확인·기록으로 잇는 수행 방법을 소유한다. 실행 조율자는 현재 대화의 Main이다.

스킬 내부의 references 선택은 어떤 절차 상세를 읽을지에 관한 구성이다. 작업 중 구현·의문·요구를 보고 Personal·Project·코드를 다시 찾는 동적 맥락 탐색은8번의 행동 설계다. 파일을 분할했다고 동적 탐색이나 검토 독립성이 자동으로 확보되는 것은 아니다.

기존 work-discussion·맥락 읽기·브리핑 등의 독립 책임은 유지한다. development는 실제 필요 조건에서 연결하고 그 본문을 흡수·복제하지 않는 안을 추천한다. 정확한 호출은14번·04-03과 대조하며04-02의 진행 중 본문은 이번 제안에서 수정하지 않는다.

## DEVELOPMENT 이전과 다음 작업

이전한다면 새 SKILL.md가 공통 실행 계약을 직접 설명하도록 기존 내용을 재구성한다. 옛 DEVELOPMENT와 새 스킬을 개발 절차의 두 정본으로 유지하지 않는다. 현재 읽기 연결을 이전한 뒤 옛 본문은 제거하는 안을 추천한다. 단순히 파일명만 바꾸거나 옛 파일을 영구적인 안내 파일로 남기는 안은 기본 추천이 아니다.

현재 참조 조사에서 demo AGENTS·Work AGENTS/README·context README·SYSTEM-GUIDANCE·prototype README·walkthrough·viewer/build.mjs와 로그인 Work의 현재 연결을 확인했다. 실제 이전 작업에서는 그 시점의 전체 참조를 다시 확인한다. 현재 본문을 찾는 링크는 새 위치로 맞추고, 당시 판본을 증명하는 source·형성 근거·과거 기록의 의미는 보존한다. Work의 Spec/Ticket/current/source/records 체계 전체 재편으로 넓히지 않는다.

추천하는 다음 작업은 **확정한1~5번으로 SKILL.md의 공통 계약과 review 상세를 실제 초안으로 구성하고, 이를 보면서6~12번을 구체화하는 것**이다. 모든 미정을 해결할 때까지 초안을 미루지는 않는다. 반대로 아직 정하지 않은 검토자 수정 권한·고정 호출·모델 배치를 조용히 기본값으로 넣지도 않는다. 전체 실행에 필요한 공백은 설계 기록에서 구별하며, 중간 초안을 완성된 운영 절차로 표시하지 않는다.

이번 스킬 형태와 DEVELOPMENT의 위치는 원래13~15번 중 기존 지침·스킬 연결에 해당하는 구조적 선택을 먼저 살펴본 것이다. 원래15항목의 번호와6번 이후 미정은 유지한다. 실제 prototype 이전은01-01의 개발 절차와04-03의 연결 작업을 함께 다루고, 전역·실제 Project 설치는 별도 적용 범위로 남긴다.

## 이번 확인과 변경 범위

현재 prototype·스킬 정책·확정 기록·로컬 외부 원자료와 현재 참조를 읽어 비교했다. 이 제안 기록과Workspace 재진입 안내만 추가했다. 스킬 생성·DEVELOPMENT 이동·Personal 편집·서브 실행·행동 시험·새 커밋은 하지 않았다. 구성의 적합성 추천과 실제 사용 효과 확인을 구별한다.
