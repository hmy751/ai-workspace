# 문제 분석·개입 구성·검증 상태의 근거

평가의 출발점인 문제, 그 문제를 바탕으로 개선한 구성, 비교에 사용할 판본과 기존 검증의 범위를 다룬다. 05·07에서 어떤 결과와 한계가 확인됐고 왜 이번 개선으로 이어졌는지 본문에서 읽을 수 있게 기존 09의 유효한 분석을 유지했다.

판본·파일 일치·검사 결과는 **2026-09-09 기존 현황 조사 시점의 기록**이다. 현재 정리는 그 근거를 주제별 본문으로 옮긴 것이며 최신 설치나 실행 상태의 재확인이 아니다. 적용 시에는 실제 사용할 구성·판본을 다시 특정한다. 당시 조사 경위와 초기 평가 제안은 [09 당시 기록](archive/2026-09-09-before-organization/09-pre-application-evaluation-status.md)에 있다.

전체 개념 관계는 [평가 구조](01-evaluation-structure.md), 평가에서 사용할 판단·비교·기록 방법은 [평가 방법](02-evaluation-method.md), 실제 원문과 코드에 적용한 상세 사례는 [평가 기록과 사용 예](04-worked-evaluations.md)에서 이어진다.

## 05에서 07까지 문제가 구체화된 경로

### 05: 작동한 체계와 장기 운영의 공백을 함께 확인했다

05의 기준 문서는 [최종 종합 분석](../../../source/05-tripproof-harness-retro/original/analysis-2.md)이다. `analysis.md`, `method.md`, 반박 판정은 최종 분석과 나란히 놓는 별도 결론이 아니라 특정 근거와 한계를 확인하는 지원 자료다. [source의 권위와 접근 순서](../../../source/05-tripproof-harness-retro/source.md)를 따른다.

회고에는 이미 잘 작동한 부분이 있다. 7개 spec 묶음의 계약 문장 약 480건을 코드와 정적으로 대조했고 대체로 일치했다. spec의 eval 수치·경로 인용 26건 중 24건은 보존 사본과 일치했다. 하네스 장치 20개 중 19개에서 사용 흔적이 확인됐고, no-op·revert·AC 미성립을 판단에 사용했다. 이것은 당시 계약·검증 체계의 강점이며, 개선 뒤에도 보존할 성과다. 이번 현황 분석에서 당시 테스트를 재실행한 것은 아니다. 근거는 [최종 분석의 강점](../../../source/05-tripproof-harness-retro/original/analysis-2.md#먼저-확인된-강점)에 있다.

동시에 닫힌 spec의 현재 권위, 실행 근거의 코드 상태 복원, 오래 미뤄진 화면 작업, 공백 뒤 재진입, 사용자 이해와 작업 중 완료 주장의 간극이 남았다. 반박 검증은 최초 문제 서술도 수정했다. 예를 들어 `6280d91`에서 활성 spec은 실제 갱신됐으며, 문제는 무효화된 닫힌 spec의 처리였다. “설명 규칙이 없거나 수동 호출이라 실패했다”는 설명도 충분하지 않았다. 상시 규칙과 강한 설명 모드를 호출한 뒤에도 재설명이 필요한 장면이 있었다. 근거는 [반박 판정](../../../source/05-tripproof-harness-retro/original/judgment/r2-adversarial-verdicts.md)의 문제 1·6·7에 있다.

05는 개선 전 사건과 운영 공백의 근거다. 이때 만든 새 하네스 초안의 효과를 증명한 자료는 아니다.

### 07 원자료와 01: 작업 완료와 제품·코드의 발전을 구분했다

[07 관점별 원문](../../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-conceptual.md)과 [시간순 원문](../../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-chronological.md)은 같은 회고를 두 방식으로 구성한 자료다. 독립된 두 실험으로 세지 않는다.

여기서 중심 질문은 “왜 구현과 테스트는 늘어도 제품을 믿고 사용하고 코드를 계속 키울 수 있다는 확신이 생기지 않는가”로 구체화됐다. [01 문제 분석](../01-problem-analysis.md)은 이를 제품, 코드, spec, 평가, context의 문제로 정리했다.

- 제품에서는 실제 사용자 흐름의 문제 해결보다 개별 기능의 완료가 선명했다.
- 코드에서는 새 요구를 기존 구조에 넣는 일이 현재 모델·책임 배치를 다시 보는 일보다 쉬웠다.
- spec은 해야 할 일은 이어줬지만 선택 이유·불확실성·재검토 조건까지 같은 강도로 이어주지는 못했다.
- 평가는 요구 동작뿐 아니라 제품 원자료와 실제 결과, 변경 전후 코드와 다음 변경 부담을 함께 봐야 했다.
- context는 보존 기간, 필요한 때 읽는 조건, 현재 판단을 지휘하는 권위를 구별해야 했다.

[현재 source 지위](../../../source/07-tripproof-spec-driven-continuity/source.md)는 이 중심 진단을 근거 기반 회고 결론으로 인정한다. 모든 구현 시점의 인과가 주장 단위로 추적된 것은 아니지만, 평가 준비를 위해 중심 진단 전체를 처음부터 보류하거나 재검증할 필요는 없다. 구체적인 역사 비교에 사용할 장면의 원자료를 보강하고, 제안된 개입의 효과를 별도로 확인하면 된다.

### 02·03 뒤의 04: 저장된 판단도 실행 중에 빠질 수 있음을 확인했다

02의 Workspace와 03의 Project context는 현재 작업과 여러 작업에 걸친 맥락의 책임·수명을 나눴다. 그러나 [04 대화 장면 분석](../04-conversation-scene-analysis.md)은 정보가 이미 주어졌거나 spec-driven을 사용하지 않은 작업에서도 판단이 약해졌음을 보여 줬다.

대표 장면은 다음과 같다.

| 당시 장면 | 관찰된 간극 | 평가에 가져올 질문 |
| --- | --- | --- |
| 06-09 실제 LLM 판단을 넣기로 합의한 작업 | 인터페이스와 검증기는 생겼지만 실제 LLM 호출 없이 regex가 남았다. AI가 provider 미구현을 이미 보고했어도 요구 충족의 이견은 남았고, 재질문 뒤 연결 준비에서 멈췄다고 정정했다. [원대화 순서와 판정](04-worked-evaluations.md#추가-실제-장면-정직한-상태-보고와-요구-충족)을 함께 본다. | 미구현 범위를 정확히 보고했는가와 핵심 수행을 실제 맡아 실행했는가를 구분한다. |
| 06-14~15 서버의 판단 흐름·가독성 개선 | 유효한 세 리팩터링과 서버 테스트 56개 통과 뒤 전체 완료로 보고했지만, 재질문하자 남은 주요 영역을 바로 열었다. | 완료 판단이 원래 목표와 실제 잔여 문제를 반영했는가? |
| 06-09 library chat의 작업 범위 비교 | 내부 후보를 사용자 답변으로 바꾸는 책임을 미루고 raw 후보를 화면에 표시하는 작은 대안을 추천했다. | 작은 작업으로 줄여도 현재 조각에 필요한 제품 책임을 지켰는가? |

마지막 장면은 실제 구현 실패가 아니라 계획·범위 선택의 근거다. 이 세 장면은 전체 작업의 대표 통계 표본도, 이번 평가에서 채택한 테스트 목록도 아니다. 설명·판단·실행·완료 가운데 무엇을 관찰해야 하는지 알려 주는 근거로 사용한다.

## 지금까지 마련한 개입과 현재 판본

개입은 판단을 유지할 문서 구조, 실제로 재판단하는 스킬, 사용자의 이해를 돕는 스킬로 나뉜다. 최근에는 이들을 Spec·Ticket과 Main·Maintain의 실제 전달 관계에 연결했다. 네 스킬을 하나로 합치거나 모든 작업에 검토를 강제한 구성은 아니다.

| 책임 | 바꾸려는 행동 | 현재 접근점과 지위 |
| --- | --- | --- |
| Workspace·Project context | 목표·선택 이유·현재 상태·자료 권위를 적절한 위치에 유지하고 필요한 범위로 재진입한다. | [02](../02-workspace-based-continuity-direction.md), [03](../03-project-context-foundation-direction.md)는 기반의 도출 이유다. 현재 Spec 관계는 07과 Reference를 따른다. |
| Spec·Ticket | Work 전체의 문제·결과·공통 판단과, 실행 단위의 설계·할 일·확인·결과를 연결한다. 핵심 수행을 미룬 채 작업을 닫는지 판단할 자료를 준다. | [07 통합 분석](../07-context-harness-spec-ticket-integration.md), [08 정의·범위](../08-skills-spec-ticket-integration/03-spec-ticket-definition-and-scope.md), [Ticket 구성](../08-skills-spec-ticket-integration/04-ticket-components-and-rationale.md). 현재 Reference에도 반영됨. |
| `reconsider-work` | 기대와 실제 결과의 간극, 새 조건, 막힘, 변경 부담이 있을 때 목표·근거·관련 책임을 확인하고 유지하거나 바꿀 일을 정한다. | [현재 준비본](../08-skills-spec-ticket-integration/v0/payload/.agents/skills/reconsider-work/SKILL.md). 두 리뷰 스킬로 나누던 과거 설계는 archive이며 현재 의무가 아니다. |
| `work-discussion` | 작업을 논의해 목표·범위·사례·완료 조건과 Spec을 구체화하고, 실행을 봐야 아는 가정을 구별한다. | [현재 준비본](../08-skills-spec-ticket-integration/v0/payload/.agents/skills/work-discussion/SKILL.md). 직접 호출하는 논의 역할이다. |
| `explanation-recovery`·`work-artifact-briefing` | 앞선 설명의 뜻과 필요한 정정을 복구하거나, 실제 작업물의 역할·연결·결과·근거·미확정을 설명해 다음 판단을 돕는다. | [설명 복구](../08-skills-spec-ticket-integration/v0/payload/.agents/skills/explanation-recovery/SKILL.md), [작업물 설명](../08-skills-spec-ticket-integration/v0/payload/.agents/skills/work-artifact-briefing/SKILL.md), [공통 설명 기준](../08-skills-spec-ticket-integration/v0/payload/context/project/guidance/explanation-and-evidence-criteria.md). |
| Main·Maintain 전달 | Main이 채택한 판단과 근거를 전달하고 Maintain이 허용 범위에서 기존 문서를 갱신한다. 전달한 말과 실제 반영 완료를 구분한다. | 현재 Reference의 Spec·Ticket 및 Maintain 계약. 스킬의 설명만으로 문서 갱신 성공을 주장하지 않는다. |

08의 Spec·Ticket은 기능 개발뿐 아니라 코드 개선도 다룬다. Work당 Spec 하나에 공통 문제·목표·설계 판단을 두고, Ticket에는 이번 실행의 설계·선택 이유·할 일·확인·결과를 둔다. Ticket의 기본 구성은 맡은 결과와 범위·실행 맥락과 접근·완료 조건과 확인 방법·현재 상태와 실제 결과이며, 고정 양식 채우기보다 실행과 판정에 필요한 내용을 갖추는 것이 목적이다.

예전 02의 “독립 spec을 기본으로 유지하지 않는다”는 선택과 06 비교의 조건부 Spec 도입은 현재 Reference의 기본 구조로 그대로 이어지지 않는다. [07 분석 README](../README.md)는 이 변경을 명시한다. 04 등의 당시 선택 문구를 최신 계약으로 읽으면 현재 개입의 범위를 잘못 잡게 된다.

### 이번 조사에서 확인한 Reference의 후속 반영

이 연구 저장소의 조사 시작 HEAD는 `aa6e3452f95f8208e603f568b6845fd55fa54ed5`다. 08의 README·검토 기록·manifest에는 후속 합의가 Reference 상위 계약에 아직 반영되지 않았다는 **당시 상태**가 남아 있다.

2026-09-09 read-only 실물 대조에서는 형제 저장소 [context-harness](../../../../../context-harness/README.md)의 HEAD `87d2102`를 확인했다. 스킬·Spec·Ticket 합의는 `bc3d954451384aeee2f5ee8b00d0f18cfb432960`에서 반영됐고, 이후 Decision 관련 보완이 추가됐다. 확인 시 tracked 변경은 없었고 untracked `.DS_Store`만 있었다. Reference에 가져간 08 입력 판본은 `1e07f589b0f63094cf34ad0e95cbd039ed1e3bb2`이며 현재 08 파일과의 일치도 확인했다.

- [현재 Spec·Ticket 계약](../../../../../context-harness/reference-project/context/work/workspaces/SPEC-AND-TICKETS.md)에 Work당 Spec 하나, Ticket 네 구성, Maintain 위임과 Main의 전달·실제 반영 확인이 있다.
- 08 payload의 네 스킬 본문, 네 호출 설정, 공통 설명 기준으로 이루어진 **일반 파일 아홉 개**는 Reference의 대응 파일과 byte 단위로 같다. Claude·Codex 연결 **여덟 개**도 target이 같고 해석된다. Guidance README는 Reference의 기존 색인에 병합한 차이가 있다.
- 반영 근거는 [Reference 통합 기록](../../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/records/2026-09-08-15-skills-spec-ticket-reference-integration.md)에 있다.

따라서 지금은 “스킬 파일만 준비됐고 상위 합의는 미반영” 단계보다 진행돼 있다. **Reference 구현·파일 대조와 실제 대상 프로젝트에서의 사용 효과는 구별한다.** 이번에는 실제 TripProof의 현재 checkout·host 동작·제품 결과를 새로 조사하지 않았으며, 최신 구성의 제품 효과나 다른 대상 이식을 확인했다고 주장하지 않는다. 과거 연구 기록은 고치지 않고 이 문서에 시점 차이를 남긴다.

현재 Reference의 [Decision 기준](../../../../../context-harness/reference-project/context/project/decisions/README.md)도 중요한 선택의 이유·대안·불확실성·재검토 신호를 보존하도록 보완됐다. 모든 갱신에 Decision을 만드는 요구는 아니며, 현재 답은 담당 Project 문서에서 찾는다. Reference 전체를 After로 선택한다면 이 보완도 개입 범위에 포함되는지 표시해야 한다.

## 이미 있는 검사와 아직 없는 효과 증거

이전 `reconsider-work`에는 실제 비교시험이 있다. [보존된 비교 기록](../../../../workspaces/011-tripproof-judgment-continuity-reassessment/records/2026-09-06-07-reference-based-skill/README.md)은 이전 두 판본을 같은 가상 업무에 한 번씩 읽기 전용으로 적용했다. 두 응답 모두 Main의 초기 해석을 재검토하고 빠진 책임을 찾아 다음 행동을 제안했지만, 수정본이 더 정확하거나 탐색이 더 효율적이라는 차이는 확인하지 못했다. 현재 08 판본의 시험이 아니며 실제 구현·문서 반영·다음 실행자의 인수도 수행하지 않았다. 이는 기존 Before/After 시도와 그 한계로 보존하며 현재 개선의 근거로 바꾸지 않는다.

[08 검토 기록](../08-skills-spec-ticket-integration/02-review-and-validation.md)은 스킬 형식, manifest의 파일 해시, 상대 연결, 원본 대비 diff와 의미 검토를 구분한다. 최초 준비본에는 별도 읽기 전용 검토가 있었고, 뒤의 Ticket 정의·구성 보완은 Main의 diff 대조와 형식 검사였다. 앞선 독립 검토가 후속 변경 전체의 독립 실행 검증을 대신하지 않는다.

그 검토에서 대표 요청을 읽고 기대 응답을 추론한 것은 실제 host에서 스킬을 호출하고 구현·문서 갱신을 완료한 실행이 아니다. 현재 Reference와의 파일 일치는 같은 계약이 옮겨졌다는 증거다. 사용자가 이해하고 다음 지시를 더 잘 내리는지, AI가 핵심 수행을 실제 구현하는지, 잘못된 완료 보고가 줄어드는지를 확인하는 증거는 별도로 필요하다.

현재 Reference의 [통합 기록](../../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/records/2026-09-08-15-skills-spec-ticket-reference-integration.md)에는 한 단계 더 구체적인 확인이 있다.

- 전체 테스트는 124개 중 123개 통과, 기존 Verify timeout 테스트 1개 실패였고 해당 테스트의 단독 실행은 통과했다. 원인은 미해결이며 이번에 재실행하거나 해결 여부를 확인하지 않았다.
- Recover·Maintain bootstrap과 기존 machine 파일 보존을 확인했다. 상위 계약이 start/resume prompt에 전달되는 검사는 scripted runner였으며 실제 host acceptance는 아니다.
- 설치된 세 이해 지원 스킬의 본문을 모델에게 직접 읽혀 제한된 요청의 첫 응답을 평가했다. 완료 범위·미확정·설명 정정을 구분한 응답은 확인했지만, 자동 발견·호출이나 실제 사용자의 이해 개선을 확인한 것은 아니다.
- 현행 `reconsider-work`가 재판단하고 Main이 채택한 뒤 Maintain이 문서를 갱신하고 다음 실행자가 행동하는 전체 흐름은 아직 확인하지 않았다. Project 문서 관리 스킬의 실제 수행도 별도 미검증이다.

[09-09 채택 감사](../../../../../context-harness/context/workspaces/010-spec-ticket-workspace-design/records/2026-09-09-01-research-07-adoption-audit.md)는 고정 검증 명령이 없는 조사 Workspace의 생성·초기 상태 계약도 아직 일반화되지 않았다고 남겼다. 연구 작업을 적용 대상으로 택한다면 이 조건을 확인해야 한다. Recover가 기술적으로 가능하다는 사실과 생성·상태 의미가 충분히 정해졌다는 판단은 다르다.

Context Harness의 Recover·Maintain·Verify 검사 역시 선언된 입력·상태·허용 경로와 실행 연결의 검사다. 제품 수렴, 코드 구조 개선, 판단의 적절성이나 사람의 acceptance를 대신하지 않는다. 이번 새 Workspace의 Recover 및 cold 재진입 확인은 013의 초기 안내가 첫 행동에 충분했는지에 관한 국소 근거다. 개정 전체의 효과로 합산하지 않는다.

현재 남은 효과 질문은 다음과 같다.

- 핵심 결과가 빠진 작업을 사용자 재질문 전에 알아보고 다음 행동을 바꾸는가?
- 올바른 목표·판단을 설명한 뒤에도 실제 구현과 완료 판정에서 유지하는가?
- 후속 유사 변경에서 책임 위치가 더 명확하고 불필요한 예외·중복·연결 부담이 줄어드는가?
- 다음 세션과 사용자가 목표·선택 이유·현재 상태·미확정을 충분히 복원하고 행동할 수 있는가?
- 이를 위해 추가한 읽기·갱신·검토의 부담이 실제 이득에 비해 감당할 만한가?

## Before 자료로 쓸 수 있는 것과 주의할 점

05와 04에는 “당시 무엇이 잘못됐는가”를 설명할 사건과 최소 발췌가 있다. 코드·제품 변화까지 재실행 비교하려면 해당 시점의 작업 요청, 코드, spec, 출력, run과 실제 사용자 정정 순서를 더 정확하게 묶어야 한다. 05의 상세 `evidence/`는 [원 archive](../../../source/05-tripproof-harness-retro/source.md)에 남아 있고 이 연구 묶음에는 복사되지 않았다.

특히 다음 수치를 효과의 Before 값으로 사용하지 않는다.

- 05의 키워드 집계는 사용자 발화 중심이며 마찰이 많은 세션을 우선 발췌했다. 성공한 작업의 분모가 없고 중복·승인 envelope·다른 프로젝트 혼입도 있다. 전체 실패율·이해도·개선율을 계산할 수 없다.
- dirty 상태의 73/89, 약 82%는 코드 상태가 남은 **run 관련 artifact 파일** 비율이다. 독립된 채택 실험의 실패율이나 “완료 근거 run의 82%”가 아니다.
- 기록·하네스 관련 commit 약 41%는 그 파일을 건드린 commit 비중이다. 작업 시간이나 하네스 비용의 41%가 아니다.
- 같은 사건의 문장 여러 개, 같은 대화의 두 정리본, 반복 run 파일을 독립 사례 여러 개로 세지 않는다.

방법상의 근거는 [수집 방법](../../../source/05-tripproof-harness-retro/original/method.md), 수치와 주장 정정은 [반박 판정](../../../source/05-tripproof-harness-retro/original/judgment/r2-adversarial-verdicts.md)에 있다.

과거 AI와 현재 AI, 사용자 경험, 코드 상태가 함께 달라졌으므로 과거 장면보다 이번 결과가 좋다는 사실만으로 개정 스킬의 단독 효과를 확정할 수 없다. 과거 사례는 문제의 Before와 재발 확인에 쓰고, 개입 효과는 가능한 한 비교 가능한 조건에서 별도로 관찰하는 편이 적절하다.
