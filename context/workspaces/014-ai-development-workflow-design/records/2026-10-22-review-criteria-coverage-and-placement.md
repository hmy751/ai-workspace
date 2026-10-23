# 4번 검토 관점의 실제 본문 대조와 보완 배치

**후속 확정:** 아래는 당시 본문 대조와 미채택 후보 기록이다. 이후 책임 분리·독립 리뷰·과도한 보류 정정을 거쳐 [4번 최종 합의](2026-10-23-personal-review-ownership-proposal.md#후속-확정--과도한-보류를-바로잡고4번을-마무리한다)에서 A는 기존 기준에 통합하고 B는 조건부 기준으로 반영하기로 방향을 정했다. 정확한 본문 편집은 후속이다. 아래 후보 유지·4번 미완료를 현재 상태로 이어받지 않는다.

2026-10-22. **읽기·변경 부담, 기존 도구 활용, 공통화·완료·실패·수명 판단은 현재 Personal·Project 본문에 이미 구체적으로 있다.** 새 검토용 품질 목록으로 복제할 필요가 없다. 반면 일부 외부 관점은 부분적으로만 드러나고, 검토 수행·검증 근거의 적용 방식은 후속 구체화가 필요하다. 아래 보완은 Main의 후보이며 Personal·Project의 수정·새 원칙 채택은 수행하지 않았다.

2026-10-23 후속: 사용자는 보완보다 책임 분리를 먼저 하자고 요청했다. [소유·입출력 제안](2026-10-23-personal-review-ownership-proposal.md)에서 Personal과 검토 workflow의 책임을 먼저 구체화한다. 아래 본문 대조는 근거로 유지하되 후보A·B를 먼저 채택·편집하는 순서로 진행하지 않는다.

## 이번에 바로잡는 완료 범위

사용자는 “중복관리 얘기하면서 그 이전에 제안한 리뷰랑 내용들 있잖아? 가져올것과 뭐 얘기한거 근데 지금 그게 은연중에 묻힌거 아닌가?”라고 지적했다. Main은 기준의 내용 소유와 검토 수행 계약을 구별하는 데 집중하면서, 선택한 관점이 기존 본문에 충분한지와 부족분의 실제 반영 위치를 확인하지 않은 채4번을 마무리했다고 인정했다.

이어 사용자는 “4번에서 가져오기로 했던 내용들 다시 보고 실제 Personal이랑 Project 본문에 이미 있는지, 부족한건 어디에 어떻게 보완하면 좋을지 비교해서 정리해줘 그리고 혹시 추후 항목에서 이걸 논의할 시점이 있는지도 봐줘”라고 요청했다. 이번 대조는 그 공백을 채운다. [앞선 합의](2026-10-22-shared-criteria-and-independent-review-decision.md)의 중복 관리 경계·독립 재판단·강도 방향은 유지한다. 외부 내용을 제외하거나 Personal 확장을 승인한 것으로 해석하지 않는다. 5번의 Main 판단안은 제안 상태이며 확정되지 않았다.

확인한 실제 대상은 **현재 development-workflow/noline-demo의 Personal 공통·세 주제 본문과 Project 인증 관련 본문**이다. 여기에 없는 내용을 실제 Noline 전체나 다른 Project에도 없다고 일반화하지 않는다. Reference의 Spec·실행 기준과 관련 Ticket은 내용 소유·후속 논의의 근거로만 대조했다. 코드 동작·워크플로 효과 시험은 아니다.

## 비교 근거

- Personal: [공통 관점](prototypes/development-workflow/noline-demo/context/personal/development/INDEX.md), [공통 제공과 사용처](prototypes/development-workflow/noline-demo/context/personal/development/shared-boundaries/INDEX.md), [계약과 수명](prototypes/development-workflow/noline-demo/context/personal/development/contracts-and-lifetime/INDEX.md), [이름과 완료](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/INDEX.md).
- Project: [제품의 작업 연속성](prototypes/development-workflow/noline-demo/context/project/common/device-session/INDEX.md), [인증 계약](prototypes/development-workflow/noline-demo/context/project/guidance/authentication-and-session/INDEX.md), [인증 가독성](prototypes/development-workflow/noline-demo/context/project/guidance/code-readability/INDEX.md), [현재 구현·확인 한계](prototypes/development-workflow/noline-demo/context/project/current/authentication-flow/INDEX.md).
- 연결: [DEVELOPMENT](prototypes/development-workflow/skills/development/_background/evidence/development-before-skill.txt), [Reference 실행 기준](../../../../reference-project/context/work/workspaces/spec-and-tickets/EXECUTION-CRITERIA.md), [Spec 작성](../../../../reference-project/context/work/workspaces/spec-and-tickets/SPEC.md).
- 외부: [Matt code-review](../source/workflow-references/matt-pocock/repository/skills/engineering/code-review/SKILL.md), [Lauren rubric](../source/workflow-references/pstack/repository/skills/interrogate/references/rubric.md), [Lauren code-quality](../source/workflow-references/pstack/repository/skills/interrogate/references/code-quality-review.md), [Lauren Lead 판단](../source/workflow-references/pstack/repository/skills/interrogate/references/lead-judgment.md), [Vercel 보존 원문](<../source/lectures/vercel-product-design (1).md>).

외부 원문의 모든 항목을 채택한 적은 없다. 앞서 선택한 방향, 그 방향을 구체화할 외부 후보, 명시적으로 가져오지 않기로 한 처방을 구별한다. 아래의 ‘충분’은 이번 관점을 표현하는 내용이 있다는 판단이지 해당 본문 전체의 최종 수용이나 실제 적용 효과 확인이 아니다.

## 무엇이 이미 있고 무엇이 남았는가

| 관점과 참고 원문 | 현재 본문에서 확인한 내용 | 판단과 반영 제안 |
| --- | --- | --- |
| 읽기·변경 부담, 이름·타입·책임·흐름의 명료함 — Lauren 및 우리 목적 | Personal 공통은 책임·호출·읽기·변경 비용과 코드 자체의 명료함을 직접 정의한다. 이름·완료 본문은 유지·설명·개명·동작 수정의 조건을 비교한다. Project 가독성은 인증 완료 표현과 소비자 행동에 구체화한다. | **이미 충분.** 검토 전용 원칙을 추가하지 않고 관련 본문을 선택해 사용한다. 단순 ‘읽기 좋은가’ 체크리스트로 축약하지 않는다. |
| 기존 도구의 책임 활용, 과잉 공통화·중복 상태 방지 — Lauren·Matt | Personal 공통·공통 제공 본문은 폼/요청 도구의 상태 소유, 공통 약속과 사용처 차이, 재사용 횟수보다 실제 변경 비용을 본다. 같은 업무 규칙은 모을 수 있고 다른 정책은 남긴다. | **이미 충분.** Matt의 중복→공통화 처방을 추가하지 않는다. 기존 기준을 통해 판단하고 자동 처방은 제외한다. |
| 현재안이 타당해도 의미 있는 구조 대안 탐색 — Lauren, Astra 조정 | Personal 공통은 버그가 없어도 개선 가능하며 차이가 작으면 유지한다고 명시한다. 공통 제공은 묶음을 줄이거나 없애는 선택과 관련 구조 개선을 허용한다. 이름·완료는 코드 표현 개선의 이득·비용을 비교한다. | **개발 판단은 이미 있음, 검토 수행 연결은 남음.** 주요 선택을 기본부터 재판단하는 과제는 workflow가 소유한다. 극적인 단순화나 발견 수를 요구하는 새 원칙은 만들지 않는다. |
| 증상 대신 원인·잘못된 책임 경계를 고치기 — Lauren rubric | 계약·수명은 계약 위반이면 동작을 고치고, 표현 문제·제품 충돌과 구별한다. Project 가독성도 잘못된 진입점이나 오류 전달 문제를 문구만 바꿔 덮지 않게 한다. 다만 재시도·fallback·조건 추가가 같은 잘못된 전제를 유지하는지를 비교하는 일반 설명은 제한적이다. | **부분적으로 있음. 보완 후보A.** Personal 계약·수명의 기존 ‘순서와 예외’ 설명 가까이에 조건부 원인 판단을 짧게 통합하는 안. 실제 경로를 추적해 근거를 제시하는 행동은 workflow에서 연결한다. 별도 원인 분석 원칙집은 제안하지 않는다. |
| 데이터·상태 표현으로 모순된 조합과 반복 분기 줄이기 — Lauren의 data model/type 관점 | 이름·완료는 타입의 역할, 상태/입력/문구 구별을 다룬다. 공통 제공은 도구 상태와 기능 상태의 중복을 경계한다. 그러나 가능한 상태 조합·전이와 반복 방어 분기를 데이터 표현으로 비교하는 내용은 명시적이지 않다. | **부분적으로 있음. 보완 후보B.** 여러 작업에 사용할 기준으로 채택한다면 Personal 계약·수명에 ‘가능한 상태·전이와 표현’ 내용을 보완하고 이름·타입 본문에서 연결하는 안. 항상 enum·상태 머신을 쓰라는 규칙으로 만들지 않는다. 아직 채택·새 파일 생성 결정은 아니다. |
| 실제 사용 조건, 실패·중간·종료 상태, 사용자 결과 — Vercel·Lauren | Personal 계약·수명은 비동기 실패·정리·지원 범위를 다룬다. Project 인증 계약은 저장 전후·조회 실패·소비자 대기 조건을, common은 사용자 데이터 연속성을 정의한다. current는 실제 연결·보장 밖을 구별한다. | **현재 인증 주제에는 충분.** Vercel UI 항목을 일괄 이식하지 않는다. 새 제품 기능에 필요한 상태·결과는 해당 Project/Spec에서 구체화한다. |
| 재실행·동시 변경·부분 저장·권한 등 실제 보장 — Lauren | 인증 계약은 원자성·동시 세션 변경 등을 보장 밖이라고 명시한다. 귀속 확인과 후속 인증 거부의 미구현도 구별한다. 전 영역의 멱등성·보안·성능 가이드는 이 demo의 범위가 아니다. | **범위 밖/별도 제품 판단.** 명시된 제한은 지침 누락과 다르다. 실제 목표에 포함될 때 Project의 계약과 Spec, 실제 검증을 함께 설계한다. 외부 목록을 채우려 Personal에 일반 규칙을 추가하지 않는다. |
| 요구 충족과 코드 기준을 각각 보기 — Matt | Reference Spec·실행 기준은 요구 동작·품질·보존 계약과 완료 근거를 구별한다. DEVELOPMENT도 원요구·Personal·Project를 연결한다. | **내용은 있음, 새 역할 운영에 연결 필요.** 어느 한 축의 통과로 다른 축을 덮지 않는 Main/검토 수행을 구체화한다. Personal 품질 원칙의 추가 사유가 아니다. |
| 테스트가 구현을 따라 쓰지 않고 필요한 동작을 입증하는가, 실제 대상의 증거인가 — Matt·Lauren·Vercel | Personal은 정상·실패·종료 확인과 코드 추론/실행의 구별을 요구한다. Project current는 제어 가능한 대기 검사의 확인 범위와 실제 DB·UI 미확인을 밝힌다. Reference는 테스트 통과만으로 완료하지 않게 한다. 일반적인 테스트 설계·충분성 선정·보완 절차까지 구체화된 것은 아니다. | **원칙 일부와 사례 있음, 검증 설계는 남음.** Ticket01-03에서 자기 확인·별도 검증과 연결하고 대상 Project의 테스트 도구·경로·계약에 맞춘다. 검토자는 허점을 지적할 수 있으나 전체 검증을 대체하지 않는다. |
| 독립 판단·근거 비교·문서 밖 제안·강도 조절 — Lauren 및 우리 합의 | 기존 DEVELOPMENT는 기대 결론 주입 금지와 충돌 반환을 갖지만 직접 수정 흐름 등 예전 시안도 남는다. 새1~4번 합의는 아직 실행 본문에 적용하지 않았다. | **workflow가 소유할 적용 미완료.** Personal에 넣지 않는다. 7~12번의 입력·탐색·권한·왕복을 정한 뒤14번에서 실행 본문을 맞춘다. |

## Personal을 보완한다면 무엇을 쓸까

아래 두 개는 **추가를 권하는 후보 문구**이며 아직 합의된 기준이 아니다. 기존 본문에도 관련 뜻이 있으므로 짧게 통합하고 필요한 대비 사례로 충분성을 확인하는 편이 좋다. 형성 이유·근거의 갱신은 기존 CONTENT-POLICY를 따른다.

**후보A — Personal 계약·수명의 기존 계약/예외 설명에 통합:**

> 실패를 막기 위해 조건·재시도·대체 동작을 추가할 때는 실제 실패 경로에서 어느 약속이 깨졌는지 먼저 본다. 약속을 복구해야 하는 문제와 지원하기로 한 실패에 대응하는 문제를 구별한다. 상위 계약이나 책임 배치를 바로잡는 안과 국소 처리를 비교하되, 필요한 복구 동작을 단지 우회 처리처럼 보인다는 이유로 제거하지 않는다.

이 문구는 ‘검토자는 호출 경로를 추적하라’는 수행 지시와 다르다. 무엇을 원인 수정/필요한 실패 대응으로 볼지의 개발 판단을 보완하는 안이다.

**후보B — Personal 계약·수명에서 상태 표현을 보완하고 이름·타입 본문에 연결:**

> 여러 값의 조합이나 처리 순서가 같은 모순을 반복해서 만들면, 허용할 상태·전이와 소유 책임을 먼저 설명하고 표현 방식을 비교한다. 타입이나 데이터 구조가 그 관계를 드러내 반복 방어를 줄일 수 있는지 보되, 간단한 상태를 유지하는 비용과 새 구조의 이해·변경 비용도 함께 판단한다. 타입 표현만으로 외부 입력의 실제 검증을 대신하지 않는다.

이 문구는 상태 머신·판별 유니온·클래스 등의 기술 선택을 의무화하지 않는다. 구체 소비자가 필요한 경우 Project 계약에서 상태·전이·동시성 보장을 정한다. 외부 기술 권고 전체를 개인 원칙으로 채택하는 안도 아니다.

현재 인증 Project에는 위 두 후보를 반복해 추가할 이유가 확인되지 않았다. 새로 채택한 기준을 실제 제품에 적용해 계약이나 구현 사실이 달라질 때 해당 담당 본문을 갱신한다.

## 후속에 이 내용을 논의할 자리가 있는가

**있다. 다만 읽기·갱신 항목이 기준 내용의 보완을 자동으로 대신하지 않는다.** 지금 필요한 것은 가져올 내용의 대조와 처리 방향이며, 실제 문구 채택·편집은 해당 내용 Owner에서 이어간다.

| 논의 자리 | 이 비교에서 넘길 것 |
| --- | --- |
| 현재15항목 중4번 | 위 관점별 기존 충분성·부분 공백·절차 소유·제외의 구별과 보완 후보의 처리 방향. 단지 소유 원칙을 정했다는 이유로 전부 완료하지 않는다. |
| Ticket [01-02 코드·설계 품질](../current/tickets/01-development-workflow/01-02-code-design-quality.md) | Personal 후보A·B의 필요성·문구·조건·사례·기존 내용과의 통합. 이 Ticket은 기준과 검토·수정 방법의 전체 종합이 아직 미완료이며,01-01·01-03·04-03의 결과를 받아 다시 종합하도록 되어 있다. |
| Ticket [01-03 동작 검증](../current/tickets/01-development-workflow/01-03-behavior-verification.md) | 테스트/실제 확인의 충분성, 빠진 조건, 도구·실행 환경·증거 상한. 6번 자기 확인·12번 검증 인계와 연결한다. |
| 7번 첫 입력·8번 동적 탐색 | 이미 있는 기준의 정확한 본문·조건을 어떻게 전달하고 필요할 때 더 읽는가. 읽기 설계로 원칙의 내용 공백을 해결했다고 보지 않는다. |
| 9번 반환·5번 Main 판단 | 요구 위반·비교 대안·조건부 제안을 구별하고 주장에 맞는 근거로 판단한다. Personal 내용의 별도 정본을 만들지 않는다. |
| 14번 지침·스킬 연결 / Ticket [04-03](../current/tickets/04-skill-improvements/04-03-context-skills.md) | 새 역할 운영을 DEVELOPMENT와 읽기·재판단 스킬에 반영하고 실제 기준 경로를 연결한다. 기존 직접 수정 시안과 새로운 권한 결정을 맞춘다. |
| 15번 기록·정본 갱신 | 이번 판단과 지속 기준 채택을 구별하고 Personal·Project·Work별 반영 책임을 정한다. 아직 부족한 기준 내용을 나중에 알아서 만들게 하는 항목은 아니다. |

Main 추천은 이미 충분한 내용은 유지·연결하고, Personal 보완은A·B를 별도 채택 후보로 비교하며, 검증 기준은01-03에 구체 과제로 연결하는 것이다. 지금 비교로 내용의 공백과 담당 위치는 복원했지만 후보 채택이나 본문 반영은 끝내지 않았다. 4번은 수행 방식·소유 경계 합의를 유지한 채 내용 배치 보완을 확인하는 상태이고,5번 제안도 아직 확정 전이다.

## 확인과 변경 범위

현재 본문을 직접 읽고 외부 rubric·품질 기준 및 Ticket의 책임·후속 범위와 대조했다. ‘부분적으로 있음’은 기존 관련 문장을 인정하면서 외부 관점의 구체 조건이 어디까지 표현됐는지 평가한 Main의 판단이다. 문서 분량을 늘리는 것이 효과적이라고 검증한 결과는 아니다. 이 비교와 재진입 상태만 기록했으며 Personal·Project·DEVELOPMENT·스킬·코드·04-02는 수정하지 않았다.
