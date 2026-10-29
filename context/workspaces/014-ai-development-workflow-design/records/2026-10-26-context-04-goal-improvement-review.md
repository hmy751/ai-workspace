# 04-03 항목4 — 완료·연속의 구체화와 독립 개선 리뷰

2026-10-26. [항목4](2026-10-26-context-04-completion-continuation-proposal.md)를 기존 합의·현재 실행/관리 계약·외부 고정판과 대조해 Main 초안을 구체화하고, 새 독립 개선 리뷰의 두 의견을 보완했다. **사용자는 설명 뒤 현재 구체안으로 기록·커밋하도록 요청했다. 다음은 네 항목의 전체 연결·조항 배치 점검이다.** 설계 문서와 재진입 기록만 다루며 스킬·생성 계약·Workspace·runtime을 실제로 만들거나 설치하지 않았다. 앞선3번의 미커밋 변경은 유지했다.

## 요청과 입력

사용자 원문:

> 그래 그럼 이번엔 4번에 대해서도 앞서 한것 처럼 하자

앞선 방식은 Main 초안, 같은 원자료에서의 독립 개선 리뷰, Main의 채택·보완, 사용자에게 결과·남은 판단 설명이다. 기존 스킬을 무조건 유지하거나 신설하지 않고, [전체 범위 정정](2026-10-26-context-whole-scope-reconciliation.md)에 따라 create만의 조사나 최근 제안만으로 전체를 대신하지 않는다. [잠정 합의](2026-10-25-context-framework-provisional-agreement.md)와 실제 시스템을 함께 사용한다.

직전 [3번 후속](2026-10-26-context-03-goal-improvement-review.md#사용자-후속--project-내용-선별과-대화-기준-루프)도 입력이다. 구현·검사 상태를 Project에 자동 이관하지 않고 지속할 공통 맥락을 먼저 선별한다. 루프는 추후 명시적인 단계로 설계하며 매 작업보다 대화를 기준으로 하는 방향이다. 스킬·담당·시점은 미정이고 완료·중단·재개·생성과 자동 결합하지 않는다.

## 기존 책임과 이번 구체화

| 이미 있는 책임·방향 | 이번에 실제 흐름으로 펼친 부분 |
| --- | --- |
| [development](prototypes/development-workflow/skills/development/SKILL.md)가 최신 근거와 중요한 공백으로 전체 완료를 판단하고 [explain](prototypes/development-workflow/skills/explain/SKILL.md)으로 첫 결과를 설명한다. | 이번 한정 요청에 답한 것·Work 목표를 마친 것·대화를 중단한 것을 구별했다. 필수 미확인과 원래 범위 밖의 한계를 같은 완료 장애물로 취급하지 않는다. |
| Main은 [Work 지침](prototypes/development-workflow/noline-demo/context/work/AGENTS.md)과 [13~15 합의](2026-10-23-runtime-integration-and-records-13-15-proposal.md)에 따라 의미 변화 때 기록하고 실제 반영을 확인한다. | 마무리 때 결과 설명·current/Ticket·output이 같은 대상과 완료 범위를 가리키는지 맞춘다. 낡은 다음 행동과 검토 전 판본을 최신 결과로 취하지 않으며 새 종합 보고서를 추가하지 않는다. |
| 같은 목표는 같은 Work에서 이어가며 새 독립 Work는 요청됐을 때 생성한다. | 중단 시 중요한 미완료·근거·다음 행동을 남기고, 새 세션의 요청이 설명인지 수행인지에 맞춰 재개한다. 늦은 결과는 원래 배정에 귀속한다. |
| [기존 생성 계약](../source/ai-workspace-baseline/reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)과 [create 원형](../source/ai-workspace-baseline/reference-project/.agents/skills/create-context-workspace/SKILL.md)은 새 목표의 현재 의미 선별·원본 보호·단방향 참조·생성과 활성화 구별을 갖고 있다. | 새 Work 생성과 원래 Work 의무의 이관을 구별하고, 생성 준비·전환·host 확인의 각각 끝나는 결과를 설명했다. 수동 demo의 읽기 확인 강도와 목록 연결은 세부 권고이며 설치된 runtime 계약을 대체하지 않는다. |

사전 대조는 기존 합의 담당과 외부 원문 담당이 읽기 전용으로 수행했다. 이 조사는 Main 초안을 위한 입력이며 초안 이후의 독립 개선 리뷰와 구별한다. Main이 최종 설계·기록을 작성한다.

## 외부 원자료와 차용 범위

Matt skills1.3.1 / `5beb35b040e3de97e54fa9e386d7e42d15c295c2`, pstack0.15.29 / `190d28736eff128ec94f502a22c7fe0c4b56cd37`의 보존판을 재사용했다. 최신 인터넷 조사나 저자 지침의 실행·효과 확인은 아니다.

| 원문과 실제 책임 | 우리에게 이어 쓴 관계와 적용 제한 |
| --- | --- |
| Matt [PHASE-BOUNDARIES](../source/workflow-references/matt-pocock/repository/skills/engineering/ask-matt/PHASE-BOUNDARIES.md)21~40행, [handoff](../source/workflow-references/matt-pocock/repository/skills/productivity/handoff/SKILL.md)8~16행: 대화 연속과 실제 전달물 이동, 다음 세션 목적에 맞는 정보·기존 산출물 연결 | 세션 교체와 새 독립 목표를 구별하고 필요한 의미·원자료를 잇는다. OS 임시 인계 파일이나 토큰 기준을 Work 정본·생성 조건으로 옮기지 않는다. 현재 재개에 필수인 의미는 우리 계약대로 current에 직접 쓴다. |
| Lauren [pause-safely](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/pause-safely.md)3~10행: 명시적 중단, 실제 상태·남은 것·재개 첫 행동 반환 | 중단을 완료로 올리지 않고 실제 남긴 상태와 다음 수행을 잇는다. 모든 담당자 취소·WIP commit·임시 resume 파일을 기본 동작으로 가져오지 않는다. |
| Lauren [session-pickup](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/session-pickup.md)3~11행: 이전 결정·완료·미완료와 현재 실물 대조, 남은 수행의 인계 | 끝난 일을 반복하지 않으면서 이어받은 주장의 유효 범위를 대조한다. 무조건 신뢰나 전면 재검증으로 단순화하지 않는다. |
| Lauren [recall](../source/workflow-reference-supplements/2026-10-25-pstack-context/recall/SKILL.md)17~35행: 주제 복원과 특정 세션 pickup 구별, 충분한 상태가 있으면 재탐색 생략 | 현재 정본과 필요한 근거를 선택해 재개하며 모든 대화를 기본 재수집하지 않는다. 주제 brief를 Work 생성·상태 갱신·activation으로 취급하지 않는다. |
| Matt [implement-spec](../source/workflow-references/matt-pocock/repository/skills/engineering/implement-spec/SKILL.md)11·36~40행, Lauren [opening-a-pr](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/opening-a-pr.md)30~34행·[shipping](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/shipping.md)5~12행: 과업별 완료와 다음 실행, 실제 상태 확인 | 요청한 결과와 후속 수행을 구별한다. 자동 commit·push·PR·merge나 고정 verifier·회고 권한을 우리 마무리 규칙에 넣지 않는다. |
| Lauren [show-me-your-work](../source/workflow-references/pstack/repository/skills/show-me-your-work/SKILL.md)9~22·40~52·57~74·80~82행: 선택·근거·결과의 정본 기록과 중요한 경계, 실제 원문 대조 | 결과 설명과 지속 판단 근거를 연결하고 매번 복제 보고서를 만들지 않는다. TSV·append-only·매 반환의 다른 모델 리뷰를 우리 current/records/source/output 대신 쓰지 않는다. |

외부 원문은 우리 새 Work의 정체성·선택적 계승·원본 보호·기본 선택/host 전환·늦은 결과의 귀속을 정하지 않는다. 해당 부분은 기존 사용자 합의와 Work 계약에서 판단한다. 외부 수행자의 결과가 좋아 보인다는 이유로04-03의 구체 형태·운영 효과를 확정하지 않는다.

## Main 초안과 독립 리뷰

Main은 항목4와 [통합안](2026-10-26-context-integrated-proposal.md)에 완료 범위·중단·기록의 실제 대조,3번 선별·05 연결, 요청된 생성/전환의 반환 결과를 구체화했다. 원래 create의 큰그림을 새 선택처럼 되묻지 않고 현재 수동 demo와 보존 Harness의 실제 차이를 유지한다.

이후 새 독립 담당에게 사용자 원문·앞선 합의와 실제 계약·외부 원자료 접근점·Main 초안을 제공했다. 사전 조사 결론이나 Main의 예상 개선점을 정답으로 주지 않고, 초안의 문제 정의와 범위도 검토할 수 있게 했다. 파일 수정·실제 생성·전환은 맡기지 않았다.

리뷰 대상 첫 초안의 SHA-256은 다음과 같다. 기준 commit은 `3d58d8aa`이며 이 사이의3번 후속 변경을 포함한 작업 트리에서 작성했다.

- 항목4: `732502293c730682aa6cbc70bf62ac83b26d951da2fc826a1e2332c594e651fd`
- 통합안: `79b65856c2c61fae9fe9564473f0d034956cef9db77ec076d2a05dae619f6999`

외부 조사 담당은 별도로 출처 표를 좁게 대조했다. 링크9개는 모두 실제 보존파일과 일치했고, 고정 verifier·매 반환의 다른 모델 리뷰를 뒷받침하는 인용 범위를 보완했다. 이 사실 대조를 설계의 독립 개선 리뷰로 세지 않는다.

새 독립 리뷰어는 두 판본의 해시 일치를 확인했고, 이 사전 조사 기록을 읽지 않고 사용자 원문·기존 합의·실행/검증/explain·demo Work 계약·보존 create·외부 고정판을 대조했다. 파일 수정·실제 전환·효과 시험은 하지 않았다.

리뷰의 핵심 원문:

> 구조를 다시 나눌 문제는 찾지 못했습니다. 실제 수행에서 오해를 줄일 보완점은 두 가지입니다.
>
> 늦은 결과의 귀속과 계속 수정할 권한을 구별하면 좋겠습니다.
>
> 루프 시점의 미정을 4번에서 먼저 닫지 않는 편이 정확합니다.

| 초안의 문제와 근거 | Main 판단·실제 보완 |
| --- | --- |
| ‘계속 수행할 일과 늦게 도착하는 결과’를 함께 원래 Work·판본·권한에 귀속하면, 새 Work가 공유 산출물을 바꾸어도 과거 권한으로 계속 수정하는 것처럼 읽힌다. | [execution](prototypes/development-workflow/skills/development/references/execution.md)17·21행의 최신 대상·공유 변경·갱신 권한과 대조해 채택했다. 결과는 원 Work·실제 사용 조건에 귀속하고, 계속 수정은 최신 배정과 공유 상태를 따른다. 겹치는 산출물의 범위·순서만 조정하도록 항목4와 통합안을 보완했다. |
| ‘응답 종료를 루프 실행의 기준으로 삼지 않는다’는 초안19행은05가 아직 열어 둔 대화 경계 선택을 제한할 수 있다. | 사용자 후속과 [05 입력](../current/tickets/05-improvement-loop.md)을 대조해 채택했다. 세션 길이·응답 종료만으로 자동 결정하지 않는다는 뜻으로 한정하고 루프 경계·발동 조건은05에 남겼다. 대화 끝을 이후 조건의 일부로 선택할 가능성까지 금지하지 않는다. |

두 의견 모두 기존 합의로 보완할 수 있어 새 사용자 답을 선행 조건으로 요구하지 않았다. 완료·설명·기록의 기존 소유, 같은 목표 재개, 선택적 계승·원본 보존, 생성·기본 선택·host 연결 구별을 유지했다. 독립 리뷰의 정합성 판단은 실제 수행·사용감·운영 효과의 확인이 아니다.

같은 리뷰어에게 두 수정 지점만 좁게 후속 확인을 요청했다. 원 Work 결과 귀속과 최신 수정 권한·공유 상태를 분리한 조건이 항목4와 통합안에 일치하고, 응답 종료만으로 자동 결정하지 않으면서05의 대화 경계·발동 조건을 남긴 것도 정확히 반영됐다고 반환했다. 지정 범위에서 새 모순은 찾지 못했으며 전체안을 새로 재리뷰하거나 실제 운영을 시험한 것은 아니다.

## 확인 범위와 다음 판단

이번은 설계 구체화이며 완료 보고·재개·생성·host 전환을 실제로 수행한 시험은 아니다. Main은 한정 질문 완료·필수 확인이 남은 중단·같은 목표 재개·독립 목표 생성·미완료 책임 이관·공유 산출물의 늦은 결과를 본문에 대입해 책임과 반환을 대조했다. 사용자와4번을 논의한 뒤 네 항목의 전체 책임·이관 조항을 점검한다. USAGE/context-update의 형태·사용감, 실제 스킬 구성·설치·05/06/07 후속 전체는 별도다. 기존3번 미커밋 변경과 원자료·prototype 실행 본문은 보존한다.

확인 결과:3번 후속을 포함한 현재 변경12개는 모두014의 설계·기록·진입 Markdown이다. 로컬 링크720개·절 연결18개에서 누락이 없고, 공백 검사와 `git diff --check`를 통과했다. 실제 스킬·source·prototype 실행 본문·설정·제품은 변경하지 않았다. 이번에는 커밋·설치·생성·전환·제품 테스트를 수행하지 않았다.

## 구체화 확인과 기록·커밋 요청

사용자 원문:

> 그래 이렇게 하고 구체화 된거지? 그럼 기록할거하고 커밋 하자

네 항목의 초안·독립 개선 리뷰·보완을 진행한 현재 구체안을 기록하고,3번의 Project 내용 선별·대화 기준 루프 연결과4번의 완료·연속·리뷰 보완을 함께 커밋한다. 위 ‘커밋 미수행’은 이 요청 전의 확인 상태다. 다음 재개는 같은4번 설명을 다시 요구하는 것이 아니라 네 항목의 전체 연결·책임·실제 조항 배치 점검이다. USAGE/context-update의 정확한 형태·사용감 유보, 실행 스킬 구현·설치·효과 확인과02/05/06/07의 남은 범위는 유지한다. 기록·커밋 요청을 그 실행 전체의 승인이나04-03 전체 완료로 확대하지 않는다.
