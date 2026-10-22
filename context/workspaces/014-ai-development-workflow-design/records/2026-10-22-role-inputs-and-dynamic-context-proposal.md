# 구현자·검토자의 입력과 작업 중 맥락 선택

2026-10-22. 실제 Personal·Project·Spec/Ticket 본문과 보존한 Matt·pstack·Vercel 자료를 대조한 **Main의 설계 후보**다. 로그인 완료 표현 데모를 문서 구성의 구체 예로 사용했으며 새 구현 실험이나 모델 비교를 수행한 것은 아니다. 실행 스킬·DEVELOPMENT·데모 본문은 변경하지 않았다.

## 이어받을 사용자 방향과 이번 제안의 지위

[앞선 의도 기록](2026-10-21-dynamic-context-and-review-intent.md) 이후 사용자는 다음처럼 역할을 정정했다.

> 검토자는 구현단계에서 구현자와 같은 단계 역할을 말하는거 맞지? 검증이 아니라
> 그리고 검증도 검증자가 필요하다고 생각해 서브로

따라서 구현 단계 안에서 구현자와 별도 관점 검토자가 Main에게 결과를 돌리고, 이후 검증 및 수정 단계에는 별도 검증자 서브를 둔다. 구현자도 자기 변경을 확인한다. 검토자의 의견을 Main이 판단한다는 기존 의도와 함께 읽는다. 기존 DEVELOPMENT의 같은 입력·검토자 직접 수정 흐름을 이 구성의 확정 계약으로 가져오지 않는다.

모델 구성에 관한 사용자 추가 방향:

> 서브 에이전트는 프론티어 모델보다 한단계 낮은걸로 구성하면 좋겠어 미디엄 정도로

서브의 기본 방향은 프론티어보다 한 단계 아래 모델과 medium 추론 수준이다. 정확한 모델명은 미정이며 이번 조사에서 서브를 새로 실행하거나 설정을 바꾸지 않았다. 모델 수준을 이유로 근거 접근·판단 책임을 줄이지 않는다.

직전 Main안은 구현자가 완성한 첫 결과·선택 이유·확인과 한계를 반환하고, 검토자는 현재안과 의미 있는 대안·비용·근거를 비교하며, Main이 채택한 수정을 기본적으로 기존 구현자에게 돌리는 것이었다. 수정 담당의 기본값·입력 선별·구체 권한은 제안이고 사용자 상세 채택은 아직 확인하지 않았다.

## 실제 문서에서 확인한 점

- [Personal 공통](prototypes/development-workflow/noline-demo/context/personal/development/INDEX.md)은 호출·읽기·변경 부담, 코드 명료함, 현재 조건에 따른 유지·수정 판단을 설명한다. [이름 기준](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/INDEX.md)은 원칙뿐 아니라 초대 코드 예시와 사례 링크를 포함한다. `INDEX.cases.md`만 제외해도 사례 없는 입력이 되는 것은 아니다.
- [이름 사례](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/INDEX.cases.md)에는 현재 데모와 같은 인증 코드의 A/B 비교와 개명 선택이 있다. 이 내용을 먼저 주면 검토가 기존 결론을 따라갈 가능성이 있으나, 실제 영향은 아직 측정하지 않았다.
- [Project 입구](prototypes/development-workflow/noline-demo/context/project/README.md)는 제품 의미·인증 계약·표현 가이드·현재 구현을 질문별로 연결한다. [읽기 기준](prototypes/development-workflow/noline-demo/context/project/REFERENCE/reading.md)은 필요한 본문 선택, 충분할 때 읽기 종료, 문서와 코드의 불일치 판별을 이미 설명한다.
- [Work의 Spec 진입](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/current/memory/index.md)은 다섯 파일 전체를 Spec으로 정의한다. [Ticket](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/current/memory/tickets/01-authentication-completion.md)에는 범위와 실제 완료 조건이 있다. 이 데모에서는 다섯 Spec이 짧고 관련되므로 함께 읽는 것이 타당하다. 이를 모든 크기의 Spec 전독 의무로 일반화하지 않는다.
- Work의 [개인 기준 선택](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/current/memory/personal-context.md), Spec의 개념·품질·제약, Project current에는 이미 선택한 `signInAndRequestRefresh`·`onSignedIn`과 이유가 있다. 현재 코드를 검토하면서 이전 선택을 전혀 보지 않는 조건은 성립하지 않는다.
- [초기 시나리오](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/source/scenario-input.md)는 가상 시작 입력이고 현재 실행 코드와 다르다. 현행 문서를 입력으로 쓰는 것은 현재 결과 재검토이며 최초 구현의 독립 재현이 아니다.

## 첫 입력의 제안

두 역할 모두 적용되는 진입 지침, 이번 목표·범위·보존 계약·미정, Spec/Ticket 원문, 실제 대상과 코드·사용처 접근점을 받는다. Main은 원문 위치와 함께 각 자료를 읽을 이유를 짧게 전달한다. 현재 선택과 변경 가능한 판단을 구별하되 기존 명시적 제약을 임의로 선호로 낮추지 않는다.

| 입력 | 구현자 | 구현 단계의 검토자 |
| --- | --- | --- |
| 이번 Work | Spec 다섯 본문·Ticket·현재 상태를 읽고 이번에 맡은 결과를 파악 | 같은 요구·제약·실제 변경을 읽는다. 구현자의 완료 주장만으로 원문을 대체하지 않음 |
| Project | 기기 세션의 제품 의미, 인증·실패 계약, 표현 가이드, 현재 인증 흐름 | 같은 본문으로 제품 계약과 현황을 직접 대조. 지원되지 않은 실제 DB·UI 동작을 확인 사실로 취급하지 않음 |
| Personal | 개발 공통과 이름·완료 본문. 판단 차이가 불명확하면 관련 사례 | 첫 입력은 출처가 연결된 관련 원칙·적용 조건 발췌 후보. 기존 해법 A/B와 선호 결론을 기본 선제공하지 않음 |
| 기존 선택·구현자 설명 | 구현을 이어가기 위한 현재 선택과 이유 | 현재 선택임을 알고 실제 코드와 대조. 가능한 경우 원요구·코드의 초기 관찰 뒤 상세 이유를 확인하지만 필수 제약·알려진 위험은 처음부터 공유 |
| 형성 자료·이전 기록 | 기준의 의미·이유가 불명확하거나 기존 선택을 바꿀 때 관련 부분 | 원칙 해석이나 기존 선택을 재판단하는 데 필요하면 질문에 맞게 접근. 전면 차단하지 않음 |

검토자용 발췌는 새 Personal 정본이나 평가 규칙을 만드는 일이 아니다. 원문 절과 연결된 작업 입력으로 구성하고 중요한 적용 조건·예외를 함께 남긴다. Main이 특정 결론에 유리한 문장만 선별해서는 안 된다. 검토자가 부족한 근거를 직접 찾고 Main의 자료 선택이 잘못됐다고 지적할 수 있어야 한다.

이름 작업에 줄 원칙 후보는 공통·이름 본문에서 다음 의미를 취한다. 호출자가 맡기는 일과 완료 뒤 필요한 결과를 본다. 이름·타입·흐름으로 드러나는 의미와 설명에 의존하는 의미를 비교한다. 필요한 결과를 제공하지 못하면 개명으로 요구를 축소하지 않는다. 유지·개명의 이득과 비용은 같은 동작·소비자·설명 조건에서 비교한다. 이는 같은 함수명을 고르라는 요구가 아니며 검토자는 관련된 다른 개선 근거도 제시할 수 있다.

개인 사례를 처음에 보류하는 것과 요구사항의 사례·실패 재현·Project 계약을 숨기는 것은 다르다. 실제 코드·Project 가이드 자체에도 현재 선택이 보이므로 이 방식은 기존 선택으로부터 완전히 격리된 평가가 아니다. 원칙만으로 충분한지와 원문·사례를 조건부로 더 읽는 방식의 효과는 후속 확인 대상이다.

## 동적 라우팅: 새 질문을 해결하는 데 필요한 본문으로 돌아간다

Main이 처음 골라 준 경로는 출발점이다. 서브는 자기 작업 중 새 쟁점을 만나면 질문을 정하고 관련 진입점·정본·코드·사용처를 선택한다. 자료를 더 읽는 데 매번 Main 허가를 받지 않는다. 이미 충분히 읽은 내용은 재사용하고 해당 질문을 판단할 수 있으면 작업으로 돌아간다. 무관한 저장소나 전체 context로 조사 범위를 자동 확대하지 않는다.

| 작업 중 새로 드러난 질문 | 추가로 읽을 곳과 판단 |
| --- | --- |
| 이름 문제인지, 실제 반환이 너무 이른지 불분명하다 | Project 인증 계약, Spec 동작·계약, 실제 소비자를 대조한다. 최신 조회 결과가 필요한가와 인증만 필요한가를 먼저 구별한다. |
| Login·Reauth의 후속 행동을 공통 함수 안으로 모으려 한다 | Personal [공통 제공과 사용처 선택](prototypes/development-workflow/noline-demo/context/personal/development/shared-boundaries/INDEX.md)과 두 사용처를 읽어 함께 지킬 규칙과 이동·닫기의 차이를 판단한다. 검토자는 관련 원칙·조건을 먼저 사용한다. |
| 조회 오류나 callback 오류의 의미까지 바꾸게 된다 | Project 인증·실패 계약, Personal [계약과 수명](prototypes/development-workflow/noline-demo/context/personal/development/contracts-and-lifetime/INDEX.md), Spec 가정·실제 경로를 대조한다. callback 정상 반환이 현재 가정인 점도 확인한다. |
| 문서는 비대기인데 코드가 기다리거나 새 소비자는 최신 값을 요구한다 | 오래된 현황인지, 구현 결함인지, 승인된 요구 변경인지 근거를 대조한다. 최신 파일을 자동 정답으로 삼지 않는다. 남는 계약 충돌·범위 변경은 Main에게 돌린다. |
| 기존 선택의 이유가 불명확하거나 반대 근거가 나왔다 | 관련 Work 기록 또는 해당 본문의 `_background`에서 필요한 이유·조건을 확인한다. 과거 선택을 본 사실과 그것이 판단에 미친 관계를 필요할 때 반환한다. |

예를 들어 검토자가 인증 후 조회까지 기다리는 대안을 생각했다면, 먼저 두 소비자의 다음 행동과 비대기 계약을 읽는다. 현재 조건에서는 이동·닫기를 시작하고 최신 조회 값을 즉시 읽지 않으므로 기다림을 자동 개선으로 채택할 근거가 없다. 반면 새 소비자가 최신 값을 실제로 필요로 한다는 증거가 나오면 해당 소비자만 기다릴지 공통 계약을 바꿀지가 Main의 판단 대상이 된다. 이는 입력 선택을 설명하는 가정이며 이번에 새 동작을 실행하거나 요구를 변경한 것이 아니다.

반환에는 결론에 영향을 준 추가 맥락과 효과를 짧게 남긴다. 예: “조회 대기안을 검토했으나 두 소비자와 비대기 계약을 대조해 현재안 유지 권고.” 모든 파일 읽기를 별도 로그로 출력할 필요는 없다. 서브가 해결 가능한 구현 문제는 직접 처리하고, 검토자는 수정 권한이 별도로 부여되지 않은 동안 발견·대안·근거를 반환한다. 자료 접근 불가, 요구·계약 충돌, 제품 정책·범위 변경, 검토 입력으로 원칙을 이해할 수 없는 문제는 Main이 보완·판단한다.

## 레퍼런스와 기존 스킬에 연결할 부분

| 근거 | 참고할 점 | 우리 구성에서 더 정할 점 |
| --- | --- | --- |
| Matt [implement-spec](../source/workflow-references/matt-pocock/repository/skills/engineering/implement-spec/SKILL.md), [code-review](../source/workflow-references/matt-pocock/repository/skills/engineering/code-review/SKILL.md) | Spec·Ticket·조사·변경 접근점으로 협업하고 요구와 기준 검토를 구별 | Main이 기대 결론을 넣지 않으면서 역할별 Personal 입력을 다르게 구성. 원문의 HEAD diff만으로 미커밋 변경을 놓치지 않도록 실제 대상 상태 식별 |
| Lauren [architect](../source/workflow-references/pstack/repository/skills/architect/SKILL.md), [interrogate](../source/workflow-references/pstack/repository/skills/interrogate/SKILL.md) | 현재 구조와 이유를 조사하고 구현 중 마찰에서 전제를 재검토. 검토 의견은 lead가 적용 판단 | 모든 작업에 복수 모델·복수 구현을 의무화하지 않고 Main·구현자·검토자 관계에 선택적으로 반영 |
| [Vercel 원문](<../source/lectures/vercel-product-design (1).md>) Workflow 2·3·5·6 | 구현과 전체 검토 모두 관련 제품 맥락·판단 기준을 읽고 작업의 필요에 따라 정본을 선택 | Personal/Project/Work의 역할과 질문에 따른 반복 탐색은 우리 흐름에 구체화한 제안. 원문에 완성된 반복 알고리즘이 있다고 주장하지 않음 |
| 기존 [read-project-context](../source/noline-baseline/.claude/skills/read-project-context/SKILL.md), Project 읽기 기준 | 작업 주제 변화로 기존 선택이 부족할 때 읽고, 이미 확보한 유효 맥락 재사용, 충분하면 본래 작업 복귀 | Project 읽기를 재설계하기보다 Main·각 역할의 호출 시점과 Personal 입력 경계를 연결. Personal 정본의 책임을 Project 스킬로 옮기지 않음 |

## 다음 판단과 확인 범위

이 문서의 파일별 입력과 동적 읽기 조건은 실제 본문에서 구성했으나 작업자에게 전달해 효과를 확인하지는 않았다. 기존 사례를 읽은 검토와 조건부로 보류한 검토의 차이, medium 모델의 적용 품질, 별도 검증자의 상세 입력은 미확인이다.

다음에는 이 입력 후보에서 검토자에게 줄 원칙·조건의 실제 발췌와 구현자·검토자 지시를 함께 검토할 수 있다. 모델·검증 효과 비교는 별도 설계를 거쳐 수행한다. 이번 제안만으로 Personal 본문을 원칙 전용으로 재편하거나 기존 DEVELOPMENT·설치된 스킬을 수정하지 않는다.
