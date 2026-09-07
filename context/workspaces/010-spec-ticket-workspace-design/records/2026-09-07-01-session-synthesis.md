# Spec·Ticket 도입 논의 종합

기록일: 2026-09-07

범위: 이 대화의 첫 Spec·Ticket 조사 요청부터 Workspace 010 생성·분리 요청까지

지위: 논의·조사·제안·정정·리뷰를 보존한 종합 기록. 최종 설계나 구현 합의가 아니다.

## 읽는 법과 보존 범위

이 문서는 현재 대화에서 직접 확인할 수 있는 사용자 발화, 세션에서 수행·보고한 조사, 기존에 작성한 상세 기록, 내부 리뷰 결과를 종합한다. 대화 전체의 축어록을 복원한 것은 아니다. 인용 블록은 이번 문맥에서 직접 확인되는 핵심 사용자 원문이며, assistant의 초기 답변·도구 실행 세부는 당시 작성 기록과 세션에 남은 작업 요약을 대조해 서술했다. 정확한 원문을 확인하지 못한 답변을 인용으로 재구성하지 않는다.

처음 논의는 009에서 시작했고 [초기 비교 기록](../../009-project-work-continuity-integration/records/2026-09-07-09-spec-ticket-current-assessment.md)과 [개발 영향 분석](../../009-project-work-continuity-integration/records/2026-09-07-10-spec-development-impact.md)을 그곳에 작성했다. 이후 사용자는 파일 수정 없이 설계를 논의하도록 요청했다. 최신 010 생성 요청은 이 세션의 기록을 독립 Workspace로 구성하도록 허용한 것이며 Reference 구현 요청은 아니다.

009가 앞서 수행한 Project 물리 layer 및 갱신 skill 구현은 선행 배경이다. 그 작업을 이 Spec·Ticket 세션이 수행한 것으로 기록하지 않는다.

## 1. 출발: Spec·Ticket이 필요한 이유와 current 중복

사용자는 첫 요청에서 Spec과 Ticket이 필요해 보인다며 외부 레퍼런스를 찾아 의견을 제시하도록 했다. 기존 Work current, 특히 goal과 겹쳐 구조를 많이 손봐야 할 가능성을 함께 물었다.

> 보면 current 와 많이 겹치는 것 같아 spec이아닌가?

> 보통 spec-driven 언급하는데 여기서 spec은 어던 정의고 구성요소는 어떻게 돼?

이후 다른 곳에서 논의한 입력문을 가져와 처음에는 읽고 이해하도록 했고, 그 방향을 바탕으로 설계를 구체화하자고 했다. 목적을 가장 명확히 표현한 대목은 다음과 같다.

> “current를 바탕으로 작업한다”만으로는 무엇을 정의하고 어떤 실행 단위를 다루는지 지칭하기 애매해.

> 그래서 Spec·Ticket을 실제 개념과 용어로 사용하는 방향으로 논의하고 싶어. 특정 spec-driven 개발 체계 전체를 그대로 도입하겠다는 뜻은 아니지만, 개념을 잘게 분해해서 별도 이름의 대체물을 만들려는 것도 아니야.

스킬 작성·작업 분해·인계에서 외부 자료와 같은 개념을 사용하려는 것이 목적이다. 익숙한 개념을 다시 자체 용어로 번역하는 비용도 고려 대상이다. 기존 구조 역시 필요하면 변경할 수 있다.

동시에 사용자는 “Workspace 하나에 Spec 하나”, “Spec을 current 안에 둔다”, “current는 진행 요약만 남긴다”를 앞서 나온 후보일 뿐 채택한 결정이 아니라고 밝혔다. 이 문서는 후보를 사용자 결정으로 소급하지 않는다.

## 2. 공개 자료 조사와 Spec 구성의 초기 이해

당시 공개 원자료에서 확인한 것은 다음과 같다.

- AI 명세 개발 도구 [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/spec-driven.md)는 기능 명세, 구현 계획, 실행 항목을 구분한다. [Spec template](https://github.com/github/spec-kit/blob/main/templates/spec-template.md)에서는 사용자 시나리오·수락 조건·예외 상황·기능 요구·성공 기준 등을 살폈다.
- AI 개발 도구 [Kiro Specs](https://kiro.dev/docs/specs/)는 요구·설계·실행 항목을 포함한 문서 묶음으로 Spec을 다룬다.
- 명세 기반 변경 관리 도구 [OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)은 시스템 동작을 나타내는 명세와 변경 제안을 구분하며 반복적인 수정 흐름을 설명한다.
- 작업 추적 기능 [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)는 버그·아이디어·논의·실행 항목과 상태·관계를 다룬다.

공통적으로 요구하는 결과를 명시하는 기능과 실행할 일을 식별하는 기능은 찾을 수 있다. 하지만 Spec의 문서 범위·수명·필수 파일과 Ticket의 크기는 일치하지 않는다. 특정 도구의 전체 폴더나 규율을 보편 정의로 옮기지 않는다.

기존 Reference의 goal·scope·완료 기준·constraints가 Spec 일부 역할을 이미 맡는다는 사실도 확인했다. 그래서 핵심은 동일 요구의 정본을 두 개 만드는 것이 아니라, 도입할 Spec과 기존 current의 책임을 정하는 것이다. 요구 요약과 실제 요구를 양쪽에서 독립 수정하는 일은 구별해야 한다.

공개 문서의 구체적인 당시 비교와 초기 제안은 009의 09 기록에 있다. 초기 제안의 모든 내용이 현재도 유효한 것은 아니다.

## 3. 실제 Workspace/current·Recover·Maintain·Verify 영향 조사

사용자는 개념 설명 다음에 실제 개발 접점을 확인하도록 요청했다.

> 그럼 그것좀 분석해봐 어쨋든 spec 도입이면 어느 부분이 개발적으로 영향이 가는지 이 시스템에 그러니까 예를 들어 만약 recover가 goal을 건드린다면 그건 범위잖아 ? 그런식으로

Reference revision 5e45310 기준으로 읽기·쓰기·검증·생성·이식의 책임을 추적했고, Recover/Maintain/lifecycle 접점은 내부 조사 주체에 나눠 확인했다. 코드 수준의 상세 정본은 [009의 10 분석](../../009-project-work-continuity-integration/records/2026-09-07-10-spec-development-impact.md)이다.

확인한 중요한 구분은 다음과 같다.

- Recover는 goal 본문을 수정하지 않는다. 정해진 최소 memory 파일을 검사하고 memory 바로 아래 Markdown 본문을 읽어 입력 packet에 넣는다. 하위 폴더나 링크된 문서 본문은 자동으로 읽지 않는다.
- Maintain은 Recover packet으로 최초 이해를 만들고, 허용된 memory 문서와 사람용 state 등에 지속 변화를 반영한다. 실제 goal writer다. 하위 Spec/Ticket 폴더는 당시 직접 자식 쓰기 허용 범위 밖이다.
- Maintain의 파일 hash 검사는 수정 대상의 기존 내용 충돌을 확인한다. 그 판단이 의존한 다른 문서까지 최신인지 자동 증명하는 것은 아니다.
- Verify는 별도의 verify.json에 선언한 claim·basis·evidence와 실행 명령을 다룬다. goal이나 Spec의 모든 요구를 자동으로 읽고 충족 여부를 집계하지 않는다.
- Workspace 생성·전환·이식의 문서 계약과 sample·fixture 역시 goal 파일과 책임 배치에 의존한다. 문장 변경과 파일 경로·필수 입력·읽기·쓰기 규칙 변경은 영향이 다르다.
- root 연구 작업대와 실행 가능한 Reference는 다른 대상이다. root 자동 Maintain은 비활성이며 이 조사에서 다시 연결하지 않았다.

초기 분석에서 사용한 임시 WorkspaceFixture의 관찰은 다음과 같다. 실제 sample receipt/status를 바꾸지 않았고 임시 자료는 정리됐다.

| 당시 조작 | 관찰 |
| --- | --- |
| 기본 Verify 뒤 Recover | fresh |
| basis에 등록하지 않은 goal 본문만 변경 | fresh 유지 |
| goal에서 별도 Spec으로 링크 | 해당 Spec 본문이 packet에 포함되지 않음 |
| 별도 Spec을 canonical_basis로 등록해 Verify | exit 0, fresh |
| 등록한 Spec의 본문 변경 | stale |
| 다시 Verify한 뒤 현재 verify.json의 claim만 변경 | fresh 유지 |

관련 기존 회귀 검사 5개도 당시 통과했다.

- RecoverTests.test_requires_minimum_memory_files
- RecoverTests.test_does_not_require_or_inspect_workspace_output_artifacts
- RecoverTests.test_accepts_nested_markdown_from_each_project_layer
- MaintainOperationTests.test_allowed_existing_update_requires_and_matches_preimage
- VerifyTests.test_canonical_basis_is_not_limited_to_recover_project_layers

정확한 실행 위치·fully-qualified test·fixture 조건은 10 분석에 있다. 이번 종합 기록 작성에서 제품 테스트를 다시 실행하지 않았다. 이 근거는 현재 코드가 무엇을 읽고 비교하는지를 보여 주며, 새 설계의 효과나 실제 host 행동, Spec 전체 충족을 증명하지 않는다. Freshness와 전체 목표 달성은 다른 판단이다.

## 4. 공유 Spec 제안과 독립 스냅샷 조건

assistant는 개발 영향 논의 중 여러 Workspace가 공유하는 Spec 후보를 도입했다. 사용자는 그 전제를 문제 삼고 다음과 같이 정정했다.

> 갑자기 공유 spec 은 뭐야?

> 안돼 그럼 관리가 어려워 spec을 다시 다른 워크스페이스에 새로 작성하더라도 스냅샷 개념은 유지해야돼

현재 조건은 Workspace마다 독립된 작업 맥락과 Spec 스냅샷을 소유하는 것이다. 다른 Workspace의 현재 Spec을 연쇄적으로 읽거나 자동으로 추종하는 공유 관계는 채택하지 않는다. 새 Workspace에서 필요한 의미를 다시 작성할 수 있으며, 상세 과거 근거는 정확한 위치를 참고할 수 있다.

이 조건만으로 Workspace 내부의 모든 편집이 불변이어야 하거나 매번 새 revision 파일을 발행해야 한다는 정책이 확정된 것은 아니다. 스냅샷의 이득은 당시 입력과 판단의 재현 및 작업 간 간섭 감소이고, 대가는 이후 변화가 각 작업과 결과에 미치는 영향을 별도로 판단하는 비용이다.

009의 09·10에 남은 공유 Spec 관련 항목은 당시 비교 후보·영향 가정이다. 현재 도입 방향으로 집행하지 않는다.

## 5. memory 제거 제안과 기존 memory/state 선택 이유의 재조사

구체적인 파일 층위를 논의하며 assistant는 memory를 없애고 Spec·Ticket·state를 재배치하는 안을 제시했다. 사용자는 기존 결정의 이유를 다시 확인한 뒤 판단하자고 했다.

> 아 memor를 없앤다 음 그럼 기존에 moemory, state 결정 때 이유 찾게 시켜서 한번더 확인해보자 지금 결정이 괜찮을지

내부 조사와 별도 독립 검토에서 다음 역사 자료를 대조했다.

- [2026-08-13 Project–Workspace 운영 구조 합의](../../001-reference-implementation/records/2026-08-13-03-project-workspace-context-agreement.md), 관련 commit 499e172: memory는 단계가 바뀌어도 유효한 목표·기준·결정·제약·계속 영향을 주는 결과·선택한 Project 맥락을, state는 현재 문제·진행·근거·불확실성·다음 행동을 맡는다.
- [2026-08-13 current 폴더 이관](../../001-reference-implementation/records/2026-08-13-05-workspace-current-folder-migration.md), 관련 commit df2ce77: 의미 책임을 유지하면서 주제 확장과 사람 문서·machine JSON 구분을 위해 Reference에 폴더를 적용했다. 이 연구 root의 current까지 동일하게 이관한 것은 아니다.
- [2026-08-14 source와 최소 memory](../../001-reference-implementation/records/2026-08-14-01-workspace-source-layer-and-minimum-memory.md), 관련 commit 504bd93: 최소 세 파일과 누락 검사 보완은 앞선 의미 분리·폴더 선택과 구분되는 결정이다.

과거 합의 기록과 Git을 확인한 것이며 그 결정을 낳은 모든 원대화까지 복구한 것은 아니다. 작은 sample을 근거로 대규모 운영 문제나 반복 누락이 이미 입증됐다고 표현하지 않는다.

Spec의 전형적 구성 밖에도 지속할 수 있는 의미가 있었다. 예를 들어 [Workspace 008 memory](../../008-workspace-transition-continuity/current/memory.md)에는 새 Main session의 절대 규칙을 사용자 결정이나 기술적 불가능으로 볼 수 없고, 특정 당시 상황에서 고른 보수적 fallback으로 되돌렸다는 판단 교정이 남아 있다. 이는 요구사항이나 최근 진행만으로 설명하기 어려운 지속 맥락이다.

독립 검토는 memory 폴더 자체가 필수라고 결론 내리지 않았다. 제거하려면 그 책임 모두를 다른 곳에서 소유하고 읽을 수 있어야 한다는 조건을 확인했다. assistant의 제거안은 이 부분이 충분히 설계되지 않았으므로 보류했다. 현재 후보는 memory/state 책임을 유지하면서 Spec·Ticket을 배치하는 것이다.

## 6. Ticket 정의와 진행 상태, current와 records

사용자는 Spec과 Ticket을 기존 memory/state 중 어디에 둘지 물었고, Ticket이 계속 변하는 진행 상태를 가져야 하는지 재질문했다.

> ticket은 계속 변하는 진행상태가 있어야 하나?

assistant는 처음에 Ticket의 진행 추적을 이유로 state 배치를 제안했지만, 실행 정의와 진행 추적을 반드시 한 문서가 함께 소유해야 한다고 볼 근거는 없음을 인정했다. 이후 다음 후보를 논의했다.

- Spec: 현재 적용하는 목적·요구·범위·제약·완료 기준.
- Ticket 정의: 맡긴 실행의 범위·입력·완료 조건과 필요한 관계.
- State: 어떤 Ticket을 진행 중인지, 막힘과 현재 결과 해석, 전체 작업의 남은 판단.

그 정의를 memory에 둘 이유는 스냅샷이라는 형식 자체가 아니라 현재에도 적용되는 기준이라는 점이다. Ticket은 일반적으로 상태를 추적하는 데도 쓰이므로, 정의와 상태의 물리적 분리는 이번 후보의 운영 선택이며 보편 정의가 아니다.

사용자는 과거 기록을 기존 current/records처럼 구분하는 뜻인지 확인했다. 새 archive 체계를 전제하지 않고 기존 현재·역사 경계를 사용하기로 논의했다. 완료된 Ticket도 후속 판단에 필요할 수 있으므로 완료만으로 자동 records 이동을 결정하지 않는다. 당시 실행 기준·변경 이유·상세 결과는 records에, 여전히 적용되는 의미와 현재 해석은 적절한 current에 남기는 방향이다.

## 7. memory/spec과 memory/tickets 후보 및 Spec 구성요소

사용자가 제안한 물리 배치 후보는 다음과 같다.

> 그럼 이렇게 할까? memory하위에 spec, tickets 계층을 둘까? 폴더로
>
> spec에서 필요한 구성요소는 그 하위에 파일로 만들고 관리하고

assistant가 예시로 제시한 내용은 다음과 같다. 아래는 Reference 설계 후보의 요약이며 010 연구 Workspace에 구현한 구조가 아니다.

    current/
      memory/
        index.md
        spec/
          index.md
          goal.md
          requirements.md
          constraints.md
          acceptance.md
          design.md
        tickets/
          index.md
          T001.md
          T002.md
        project-context.md
        그 밖의 계속 유효한 맥락
      state/
        index.md
        status.json

설명한 의도는 다음과 같다.

- 이번 작업 정의에 해당하는 기존 goal·constraints를 Spec이 맡는다면 같은 내용을 밖에서 독립 관리하지 않는다.
- memory index와 spec index는 읽기 경로를 안내하며 요구사항의 두 번째 정본이 되지 않는다.
- Spec 밖에도 계속 유효한 판단 교정과 Project 선택 맥락은 남을 수 있다.
- 필요한 내용이 있을 때 파일을 나누며 design 등을 포함한 모든 빈 파일을 의무 생성하지 않는다.
- 전체 목표의 정의 위치와 Spec/Workspace 범위가 미정이므로 goal을 실제로 옮기는 결정을 끝낸 것은 아니다.
- status.json은 당시 기존 제품 Verify의 기계 상태를 나타내며 Ticket 진행 tracker로 확정한 것이 아니다.

사용자는 이 배치를 결정하기 전에 제3 리뷰를 요청했다. 따라서 Spec 하위 파일 목록, Workspace당 Spec 수, Ticket 상태 위치, 읽기 정책과 관리 책임은 아직 확정하지 않았다.

## 8. 트레이드오프 문서와 제3 리뷰의 질문 정정

사용자가 지정한 배경은 memory-harness-research의 [06 Work-first와 Spec/Ticket-first 트레이드오프 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md)이다. 사용자는 이 문서를 확정 설계나 Spec 도입 금지 규칙으로 읽지 말고 선택의 근거와 이유를 확인하는 자료로 쓰라고 했다.

처음 제3 리뷰를 구성하면서 main은 memory 내부 배치의 타당성과 실제 Recover·Maintain 변경 비용에 초점을 맞췄다. 사용자는 이 비교의 질문을 정정했다.

> 잠깐 트레이드오프 관점을 우리 작업을 떠나서 spec ticket project work 이 개념들을 비교하라고 그러니까 기술스택이나 뭐 개발하면 이유가 있고 트레이드오프등 그런게 잇잖아? 그런 관점 당장 우리 시스템 recover 뭐 수정하고 비교 말고

> 그래 그래서 context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md 이것도 다시읽어서 본질적인 개념 확인하고해서 생각해보라고

main은 구현 중심 리뷰를 중단하고, 새 맥락의 독립 리뷰어에게 사용자 원문·06 및 관련 01·02·03 분석만을 출발점으로 개념·운영의 선택 이유와 비용을 검토하도록 했다. 기존 배치를 승인하는 결론을 입력으로 주지 않았다. main도 06을 다시 읽고 공개 upstream을 별도로 확인했다.

첫 구현 중심 리뷰의 예비 의견은 최종 개념 리뷰를 대신하지 않는다. 수정할 코드가 적거나 많다는 이유로 개념 선택을 정당화하거나 기각하지 않는다.

## 9. 최종 개념 리뷰와 main의 판단

리뷰어와 main은 네 개념이 같은 질문에 답하는 네 대안이 아니라고 판단했다.

Spec은 무엇을 만들거나 충족해야 하는지 명시하는 대상이다. Ticket은 해야 할 일을 식별·배분·추적하는 단위다. 이 연구의 Project는 여러 작업이 공유하는 목적·개념·제약·현재 현실의 범위이고, Work는 하나의 목표를 추구하며 현재 판단과 진행을 이어가는 범위다. 이는 특정 파일 구조를 떼어낸 개념 비교이며 업계의 유일한 정의를 선언하는 것이 아니다.

| 선택 | 얻으려는 이득 | 감수할 비용과 한계 |
| --- | --- | --- |
| Spec | 요구의 암묵성을 줄이고 서로의 해석과 결과를 검토할 기준을 확보 | 작성·검토·변경 비용, 미확정 판단을 조기 확정할 위험 |
| Ticket | 실행 범위·담당·진행·의존·완료를 특정해 인계와 조율 | 분해·상태 관리·통합 비용, 과분해와 국소 완료 편향 |
| Project 공통 맥락 | 작업마다 목적·개념·제약을 다시 협상하는 비용 감소 | 현재 공통 기준 유지, 임시 선택의 과도한 일반화 위험 |
| 별도 Work | 계획·Spec·Ticket이 바뀌어도 목표와 현재 판단을 이어감 | 지속 갱신과 중복 정리 비용, 범위가 흐려질 때 맥락 팽창 |

06은 당시 Work-first와 개발자 Matt Pocock의 Spec/Ticket 스킬 흐름을 비교하는 데에는 한계와 반론을 명시했다. 다만 다음을 개념의 본질로 확대하면 안 된다는 리뷰를 받았다.

- “Spec/Ticket은 판단이 닫힌 뒤, Work는 판단이 움직일 때”는 선택한 운영 방식의 기본값이다. Spec으로 미확정 요구를 드러내거나 Ticket으로 조사·실험을 맡길 수 있다.
- 한 세션 크기, 기능 전체를 좁게 관통하는 구현 조각, blocker graph는 특정 Ticket 작성 규율이다. 모든 Ticket의 필수 정의는 아니다.
- 현재와 역사 분리, 재검토 조건, 전체 목표 확인은 Work라는 이름 없이도 수행할 수 있다.
- 판단을 이어가는 책임이 필요하다는 주장과 Work라는 별도 관리 단위가 필요하다는 주장은 다르다.
- Work 목표도 좁거나 잘못될 수 있다. Work 완료가 제품 전체 목표 달성을 자동 보장하지 않는다.

공개 원자료 대조에서도 [Matt의 to-spec](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/docs/engineering/to-spec.md)은 이미 내린 결정의 스냅샷을, [OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)은 구현 중 요구·설계가 바뀌는 반복적 운영을 설명했다. Spec의 변경 가능성과 수명은 이름만으로 결정되지 않는다. [Matt의 to-tickets](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/docs/engineering/to-tickets.md)의 독립 실행 크기와 분해 규율도 일반 Ticket 개념과 구분했다.

대표적인 선택 조건은 다음과 같다.

- 요구가 안정된 여러 실행자의 기능 개발: Spec으로 결과를 맞추고 Ticket으로 나누는 이득이 크다. 이미 상위 작업과 진행 관리에서 목표·현재 판단을 충분히 다루면 별도 Work는 중복일 수 있다.
- 해결 방향을 알아가는 제품 작업: 조사·실험 때문에 요구 해석과 실행 묶음이 교체될 수 있다. Work가 이 변화 속의 목표·현재 판단을 실제로 이어간다면 별도 가치가 있다. 그 대신 기준과 기존 결과를 계속 재판정하는 관리 비용을 부담한다.
- 작은 변경: 별도 Spec 작성·Ticket 분해·Work 관리가 반복 설명을 줄이는 이득보다 클 수 있다. 각 개념을 반드시 별도 산출물로 생성해야 한다는 결론은 없다.

사용자는 이어서 비교 목적을 다시 분명히 했다.

> 왜냐면 spec driven도 있는데 project work 를 도입한거면 타당한 트레이드 오프가 있어야 하잖아? 그래서 그런거야

main의 현재 판단은 다음과 같다. Spec·Ticket은 요구 명시·실행 인계·공통 용어 사용에서 합당한 이유가 있다. Project·Work 선택의 문제의식과 조건부 타당성은 설명되지만, 충분히 관리되는 Spec-driven 운영보다 추가 비용이 정당하다는 실제 비교 근거는 아직 없다. 비교 상대에 Project 공통 맥락이나 판단 변경 관리가 없다고 가정해서는 안 된다.

사용자가 현재 겪는 “current만으로는 정의할 대상과 전달할 실행 단위를 지칭하기 애매하다”는 불편은 기존 Work 중심 선택이 치른 비용으로도 평가해야 한다. 새 개념을 기존 구조에 끼워 넣는 문제로만 축소하지 않는다.

## 10. 현재 조건·후보·미결정 사항

사용자에게서 명확히 확인된 방향과 제약은 Spec·Ticket을 실제 용어로 사용하려는 목적, 특정 체계의 일괄 도입을 원하지 않음, 기존 구조도 수정 가능함, Workspace별 독립 스냅샷 유지, 국소 완료와 과거 판단의 자동 권위 승계를 경계함, 개념 선택의 트레이드오프 검토다.

현재 유력 후보는 memory/state의 책임을 유지하면서 memory 아래 spec/과 tickets/를 두고 필요한 Spec 요소를 하위 파일로 나누는 것이다. 이는 확정된 구현 계약이 아니다.

다음은 아직 결정하지 않았다.

1. Spec의 구성요소·필수 내용·파일 분할.
2. Spec과 Workspace의 범위·개수 및 전체 목표의 정의 위치.
3. Spec·Ticket·기존 goal/constraints/state 사이의 의미 소유.
4. Ticket의 입력·실행 범위·완료 조건·의존 관계·진행 정보.
5. 새 세션, main, 개별 실행자, Maintainer가 읽어야 할 내용.
6. 실행으로 판단이 바뀔 때 기준과 현재 상태를 갱신할 책임 및 실행자에게 전달할 방식.
7. 영향받는 미완료·완료 Ticket과 기존 검증 결과를 재판정하는 기준.
8. Workspace 내부에서 현재 Spec을 수정·교체하고 과거 기준을 보존하는 세부 방식.
9. 실제 Reference 코드·계약·migration의 변경 범위.

추가 비교 실험·reviewer·자동화·승인 단계가 필수라는 결정을 새로 만들지 않는다. 현재 다음 논의는 Spec 구성요소이며, 그 정의가 전체 목표와 기존 current에 어떤 영향을 주는지를 함께 본다.

## 11. 010 분리 요청과 수행 경계

사용자는 처음에 지금까지 논의와 작업을 어디에 남길지 물었고, main이 009 기록을 제안하자 최근 내용만이 아니라 대화 전체를 종합하라고 했다. 이어서 저장 단위를 바꿨다.

> 잠깐 근데 009 말고 새로 010 만들어서 우리 세션 작업에 관한거 기록하자 분리하자 이건 우리 대화 처음 시작할 때부터 작업을

이에 010은 세션 전체 설계 논의를 소유하는 독립 연구 Workspace로 생성한다. 현재 의미는 010의 current에 직접 서술하고, 초기 세부 조사 09·10은 009의 원래 기록을 연결한다. 과거 기록을 옮기거나 새 결론에 맞춰 다시 쓰지 않는다. 009의 현재 진입점은 이관 사실과 010의 위치를 안내하도록 정리한다.

이 단계의 변경은 010 문서, 연구 Workspace 목록의 active 선택, 009의 관련 진입점이다. Reference 제품·코드·test·schema·hook, 외부 연구 저장소, 전역 설정, 원자료 및 기존 machine receipt는 변경 대상이 아니다. 이 세션에서 commit을 만들지 않았다.

## 12. 자료와 증거의 상한

### 현재 설계에 필요한 배경

- [01 문제 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/01-problem-analysis.md): Spec의 실행 가치는 유지하면서 과거 계약이 재판단 권한을 대신하는 문제를 다룬다. 특히 87~89행은 제품 결과의 명시와 내부 구현의 사전 확정을 구분한다.
- [02 Workspace 기반 방향](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/02-workspace-based-continuity-direction.md): 당시 Work-first 선택과 현재/역사 경계. 136~145행은 제품 전체 수렴·코드 성장성 평가를 해결 범위 밖으로 밝힌다.
- [03 Project context 방향](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/03-project-context-foundation-direction.md): 여러 작업에 유효한 의미, 현재 상태, 조건부 기준과 그 수명·읽기·권위.
- [06 트레이드오프 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md): 운영 기본값의 비교, 반론과 효과의 증거 상한. 178~186행은 Work가 별도 가치 없이 중복되거나 current도 stale해질 가능성을 인정한다.
- [TripProof 회고](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/05-tripproof-harness-retro.md): 내부 리뷰가 관련 부분을 참고한 선행 분석. 이번에 과거 실행 원자료 전체를 재감사한 것은 아니다.

외부 분석은 사용자가 지정한 배경이며 이 Workspace의 채택 규칙이 아니다. 위 로컬 분석은 2026-09-07 읽은 working-tree 내용에 대한 링크다. 이번 기록을 위해 원본을 복제하거나 새 불변 snapshot을 만들지 않았다. Matt 자료는 commit 068b6e0c62393147daf03530149cdce209c93da8에 고정했고, 그 외 공식 main·문서 링크는 열람일 기준이며 변경될 수 있다.

### 검토 결과의 지위

memory/state 역사 조사와 독립 리뷰는 당시 책임과 제안의 누락을 평가했다. 최종 개념 리뷰는 사용자가 정정한 질문으로 새 맥락에서 수행한 read-only 비교다. 위 5e45310 코드 조사와 임시 fixture·5개 테스트는 초기 상세 기록에 남은 실행 근거다.

이 모든 근거를 합쳐도 새 Spec/Ticket 구조의 실제 운영 효과, 추가 관리 비용 대비 이득, 자동 호출과 갱신의 신뢰성, 제품 전체 목표 달성이나 사람 acceptance가 입증되지는 않는다. 이 문서의 목적은 다음 논의가 같은 전제와 정정을 다시 잃지 않도록 현재 선택 조건과 미결정 사항을 재구성하는 것이다.
