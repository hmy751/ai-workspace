# 연구 07 전체의 Reference 반영 대조

2026-09-09. 외부 연구 08 통합 커밋 `bc3d954` 이후, 사용자가 이전 연구까지 다시 확인하도록 요청했다.

> 02,03은 정독해서 반영햇나? 아무튼 하긴했엇고 지금 직전 최근에는 08에 대해서 한거고
>
> 그래서 다시 저기 내용중에 우리 레포에 반영이 되지 않은것 들이 있나 좀 제대로 봐봐

## 결론과 판정 범위

02·03은 이전에 읽고 실제로 반영했다. 04·05·06에서 발전시킨 판단 연속성과 이해 지원의 현행 내용도 08의 네 스킬과 상위 Spec·Ticket 계약으로 이어졌다. **현재 채택된 큰 묶음이 통째로 빠진 경우는 찾지 못했다.** 다만 모든 연구 내용의 완전 적용·운영 검증까지 끝났다는 뜻은 아니다.

- **부분 반영:** 03의 Decision 생성 조건과 판단 맥락 보존 기준은 일반 역할만 반영돼 있다. 당시 추가 보완을 범위로 확정하지 않고 남겼다.
- **미구체화:** 고정 제품 검증이 없는 조사·판단 Workspace를 만드는 경우, Verify 계약을 생략·유예할 조건과 초기 기계 상태의 의미가 정의돼 있지 않다. 연구의 개별 적용 사례를 Reference 공통 경로로 일반화할지는 아직 정하지 않았다.
- **구현 후 미검증:** 현행 `reconsider-work`의 재판단·반영·후속 실행, `update-project-context`의 대표 변경 수행, 실제 host에서 Main·Maintain·다음 실행자가 이어지는 동작은 별도 확인이 남았다.
- **후속 선택으로 대체:** 별도 Spec을 기본으로 배제하던 02의 방향, 선택적 Spec·Ticket이라는 06 비교의 당시 기본값, 05의 Main 직접 기록 방식은 이후 합의로 바뀌었다. 이를 미반영으로 세어 되살리지 않는다.

적용 대상은 이 저장소의 실행 가능한 기준인 `reference-project/`와 바깥 이식 skill이다. 이 연구 작업대 root의 `current/memory.md`·`state.md` 구조와 비활성 자동 Maintain은 기존 계약을 유지한다. Reference의 네 스킬을 연구 작업대 root나 외부 연구 저장소·실제 TripProof에도 설치했다는 뜻은 아니다.

## 확인한 판본과 자료

- 대상 HEAD: `bc3d954` — `feat: integrate work skills with spec and ticket contracts`. 조사 시작 때 tracked 변경은 없고 기존 untracked `.DS_Store`만 있었다.
- 외부 연구 HEAD: `6bd06b50704bb7984384043999e03ef5f35b4299`. 지정한 [연구 07 폴더](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/README.md)의 마지막 변경은 `1e07f589b0f63094cf34ad0e95cbd039ed1e3bb2`이며 해당 경로의 working tree는 clean이었다.
- 지정 폴더의 tracked 파일·symlink는 77개이고, 그중 archive 밖은 63개, archive 아래는 14개다. 이는 목록의 크기이며 77개 모두를 현재 지침으로 정독했다는 수치가 아니다. 현재 분석 본문·배포 준비본과 그 계승 관계를 읽고, archive는 두 README의 역사적 지위만 확인했다.
- 우리 저장소의 현재 canonical·관련 코드, 정확한 009·010 기록과 Git 이력을 대조했다. 다른 Desktop 프로젝트, 외부 원대화·private 로그나 source 원본으로 조사 범위를 넓히지 않았다.
- 02의 구조·runtime, 03의 Project context, 04~06의 판단·이해 지원을 별도로 조사했다. Main은 01·06 비교·07·08과 현행 산출물·판본을 대조하고, 부분 반영 후보의 원문과 과거 유보 근거를 다시 확인했다.

## 02·03을 실제 읽고 반영한 이력

[009 최초 intake](../../009-project-work-continuity-integration/records/2026-09-04-01-source-intake.md)는 01·02·03을 읽은 입력과 SHA-256을 보존한다. [09-06 재독·보완 기록](../../009-project-work-continuity-integration/records/2026-09-06-08-project-context-update.md)은 사용자 요청으로 세 문서를 다시 읽은 사실과 03의 핵심 원문을 남긴다.

> 선택한 책임 범위에서 다음 판단에 필요한 근거가 있는데도 불확실하다는 이유만으로 조용히 빼서는 안 된다. 현재 답, 역사 근거, 열린 판단 중 어느 역할인지 권위와 수명에 맞게 드러낸다.

이 문장은 연구를 읽었다는 기록에만 남지 않고 실제 Project 보존 기준으로 반영됐다. 커밋별 결과는 다음과 같다.

| 커밋 | 실제 반영 |
| --- | --- |
| `7bd5089` | Project 공통 맥락·현재 상태·조건부 지침의 물리층, Owner·권위·선택 읽기, 실제 PRD·architecture와 Recover·이식 경로 |
| `5e45310` | 불확실성을 이유로 근거 있는 제품 이해를 누락하지 않는 보존 기준, `update-project-context`와 호출·이식 경로 |
| `dcd3c6f` | Spec 다섯 파일과 Ticket, 기존 goal·constraints 대체, Recover·Maintain·생성 계약, Project 선택 파일명 정리 |
| `bc3d954` | 08의 네 스킬·호출 설정·공통 설명 기준·연결, Work당 Spec 하나와 Ticket 네 구성, Main·Maintain 관계와 이식 절차 |

현재 01의 SHA는 `8017201ad2e93d6f67a13321dd99f77943257b65332a7e85165e2fa13e4fba64`, 03은 `893e1d4c739abe3044c8e19a8dc464ec2c2d708e4a0c0ea9fe6a0d0f275ff9c8`로 09-06 기록과 같다. **03에 나중에 추가된 본문을 놓친 상황이 아니다.**

02의 과거 SHA는 `f4bab25385a968780015f07ccabcc7a7f333360e8672c4459819ed0ee05ddb85`, 현재는 `5b24628a255e8127a1824c57103357dd3778efa2bfc08ed757c21bdeab5fff74`다. Exact-path Git 대조에서 차이는 `c2b707d`가 추가한 2026-09-08 후속 결과 안내 문단과 공백뿐이었다. 나머지 본문에 새 요구가 추가된 것은 아니다.

## 문서별 반영 관계

연구 번호는 전개 순서다. 뒤 번호가 앞 문서의 문제의식과 모든 선택을 일괄 대체하지 않으며, 아래는 현행 내용과 명시적인 변경을 구별한 결과다.

| 연구 문서 | 유지할 내용과 현재 대응 | 판정 |
| --- | --- | --- |
| [01 문제 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/01-problem-analysis.md) | 제품 결과와 코드 성장 품질을 따로 판단하고, 국소 완료·옛 Spec·과거 증거의 권위를 제한한다. [Spec 기준](../../../../reference-project/context/work/workspaces/SPEC-AND-TICKETS.md), [reconsider-work](../../../../reference-project/.agents/skills/reconsider-work/SKILL.md), [Project 계약](../../../../reference-project/context/project/README.md), [Verify](../../../../reference-project/context/work/harness/verify/README.md)에 대응한다. | 문제 대응 기반은 반영. 원문 자체는 확정 구현 요구안이 아니며 효과는 별도 확인 |
| [02 Workspace 방향](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/02-workspace-based-continuity-direction.md) | 작업별 독립성, current·records·source·output의 책임, 필요한 Project 내용 선택, 과거 Workspace 비동기화, 세 Harness 역할. [Workspace](../../../../reference-project/context/work/workspaces/README.md)·[생성](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)·Recover·Maintain·Verify에 연결된다. | 구조적 핵심 반영. Spec 배제·최소 current만 읽는 옛 기본값은 대체 |
| [03 Project foundation](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/03-project-context-foundation-direction.md) | common/current/guidance, 내용·Owner·갱신·읽기·권위, 방어적 누락 방지, 얇은 관리 skill. [Project 계약](../../../../reference-project/context/project/README.md)과 [갱신 skill](../../../../reference-project/.agents/skills/update-project-context/SKILL.md)이 맡는다. | 핵심 반영. Decision 세부 기준은 부분 반영, 실제 관리 동작 미검증 |
| [04 실제 장면 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/04-conversation-scene-analysis.md) | 기반·인터페이스와 실제 핵심 수행, 개별 완료와 전체 목표, 작업 분해 중 핵심 수행이 밀리는 문제. `reconsider-work`와 Spec·Ticket의 결과·완료 판단에 연결된다. | 문제의식 반영. 세 장면을 모든 작업의 의무 절차로 가져오지 않음 |
| [05 현재 판단 연속성 설계](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/05-judgment-continuity-solution-direction/README.md) | 실제 결과로 구현 누락과 가정의 부족을 구별하고, 관련 기존 결과·완료와 다음 행동을 다시 본다. 반대 근거·제품 의미·실제 사용 관계·변경 부담을 확인한다. | 현행 `reconsider-work`에 반영. Main 직접 기록 문구는 08의 Main 채택·전달과 Maintain 갱신으로 대체 |
| [06 판단·이해 공동 적용](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-judgment-and-understanding-application/README.md) | 네 스킬의 역할·호출 조건·권한, 세 이해 지원 스킬의 공통 설명 기준, 같은 원본을 읽는 도구 연결. | 08을 통해 반영. 별도 중복 설치 불필요 |
| [06 Work-first 비교](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md) | Work의 수명·권위 관리와 Spec/Ticket 실행 규율의 비용·이득, 일반적 우월성을 주장하지 않는 기준. | 선택 근거는 [종합 전달문](../output/research-feedback-spec-ticket-integration.md)에 반영. 실제 비용·효과 비교는 남음 |
| [07 Spec·Ticket 통합 결과](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/07-context-harness-spec-ticket-integration.md) | 이미 우리 `dcd3c6f`·`9505bf3`를 연구 쪽에서 정리한 문서다. 구조·읽기·갱신·독립 스냅샷과 후속 실행 관계가 대응한다. | 구현 결과의 되먹임 문서. Spec 개수·Ticket 구성의 당시 미정은 08에서 확정 |
| [08 스킬·Spec·Ticket 통합](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/08-skills-spec-ticket-integration/README.md) | 적극적인 Spec 구체화, Work당 Spec 하나, Ticket 네 구성·실행 내부 설계, Main 결과 전달·실제 문서 준비 확인. | `bc3d954`에 반영. 설치와 실제 공동 운영의 효과는 구별 |

### 04·05의 핵심 의미가 살아 있는 위치

- 기반 완료와 실제 핵심 수행·후속 책임: `reconsider-work/SKILL.md` 14–21행, Spec·Ticket 기준 44·66행.
- 요구 구현 누락과 상위 가정의 문제: 같은 skill 25–29·61행, Spec·Ticket 기준 100행.
- 제품 결과와 코드의 다음 변경 부담: 같은 skill 33–37행, Spec·Ticket 기준 56·80행. 파일 분리·테스트 통과를 구조 개선으로 대체하지 않는다.
- 제품에서 지킬 의미와 옛 내부 구현 선택: 같은 skill 49행, Spec·Ticket 기준 60행.
- 바뀐 판단에 실제로 의존한 기존 결과·완료: 같은 skill 59–61행, Spec·Ticket 기준 100–102행. 무관하게 유효한 결과는 유지한다.
- 채택한 판단·근거의 전달과 실제 반영·후속 실행 구별: 같은 skill 65–69행, Spec·Ticket 기준 104–106행.

05의 현재 `reconsider-work` 원본은 06의 대응 파일과 byte 동일하다. 06에서 08로 넘어갈 때 위 핵심 사례·판단은 유지하고 Spec·Ticket 및 Main·Maintain 연결을 추가했다. 현행 Reference의 네 `SKILL.md`, 네 `agents/openai.yaml`, 공통 설명 기준 본문 **9개 일반 파일은 현재 08 payload와 byte 동일**하다. 여덟 도구별 symlink의 상대 target도 같다. `guidance/README.md`는 기존 대상의 책임·소비자·수명 기준에 병합했기 때문에 다르며 내용 누락으로 세지 않았다.

## 실제로 남아 있는 것

### 1. Decision을 만드는 조건과 남길 판단 맥락

[연구 03](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/03-project-context-foundation-direction.md)의 190–208행은 선택·이유·대안·불확실성·재검토 신호·현재 답의 Owner·대체 관계를 설명한다. 별도 Decision은 의미 있는 대안, 이유를 잃었을 때 반복될 논쟁, 여러 책임에 미치는 영향, 재판단 신호, 현재 결과만으로 복원할 수 없는 이유가 있을 때 검토한다. 모든 변경에 만드는 것이 아니다. 429–431행의 확인 기준도 이유·대안·불확실성·다시 열 신호와 무조건적인 생성 금지를 요구한다.

현재 [decisions/README.md](../../../../reference-project/context/project/decisions/README.md) 3행에는 **이유·기각 대안·재검토 신호라는 역할이 이미 있다.** 9행에는 대체 관계도 있고 Project 진입점에서 현재 답의 Owner도 찾을 수 있다. 따라서 그 의미 전체가 빠졌다고 말하면 과장이다. 확실한 잔여는 **별도 Decision을 만드는 조건과 단순 현재값 갱신마다 강제하지 않는 경계, 중요한 선택의 불확실성을 남긴다는 명시적 기준**이다. [Project README](../../../../reference-project/context/project/README.md) 90행과 [갱신 skill](../../../../reference-project/.agents/skills/update-project-context/SKILL.md) 20행이 이 계약에서 기록 필요를 판단하도록 위임하므로 실제 관리에서도 남는 공백이다.

이는 08 이식의 회귀가 아니다. [009 보완 기록](../../009-project-work-continuity-integration/records/2026-09-06-08-project-context-update.md) 32행은 다음과 같이 당시 범위를 남겼다.

> `decisions/` 기록 항목 자체의 추가 보완, 새 reviewer·hook·상태 schema는 이번 범위로 승격하지 않았다.

보완한다면 Decision Owner의 계약에서 처리하는 편이 맞다. 갱신 skill에 같은 정책을 복제하거나 새 필수 양식을 만드는 필요는 확인되지 않았다. 기존 timeout Decision에는 기본값이 필요한 이유는 있지만 왜 `5000`을 다른 값보다 택했는지의 상세 대안·불확실성은 없다. 이를 새 기준에 맞추려고 역사적 이유를 창작해서 채우면 안 된다.

### 2. 고정 Verify가 없는 조사·판단 Workspace의 생성

연구 02 29행은 Workspace를 조사·결정에도 사용할 수 있다고 설명하고, 107행은 다음과 같이 해당 연구의 적용 선택을 남긴다.

> 현재 연구에는 연구 주장을 판정할 고정 명령과 evidence 범위가 없으므로 이 Workspace에 `verify.json`을 두지 않는다.

현재 [생성 계약](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md) 27행과 [생성 skill](../../../../reference-project/.agents/skills/create-context-workspace/SKILL.md) 24행은 Verify 계약·claim·basis·evidence·상태 구성까지 요구한다. 고정 검증이 없는 경우의 생략·유예 분기는 없다. Verify를 필요할 때만 **실행**한다는 문구는 계약 파일의 **생략** 조건과 다르다.

반면 [Recover 구현](../../../../reference-project/context/work/harness/recover/operation.py) 415–444행은 `verify.json`을 읽지 않으며, [Maintain bootstrap](../../../../reference-project/context/work/harness/maintain/operation.py) 67–88행도 Recover packet을 그대로 사용한다. 따라서 임의 명령을 발명해야만 이 두 runtime을 쓸 수 있는 기술적 제약은 아니다.

Recover는 기계 상태를 읽어야 한다. [공통 상태 계약](../../../../reference-project/context/work/harness/workspace_contract.py) 35–39행은 `ready_for_verification`, `verification_failed`, `verification_passed`만 정의하며, 337–340행에서 receipt 없는 초기 상태는 허용한다. 검증이 비적용인 연구 작업에서 이 상태를 어떻게 해석할지는 생성 계약에 없다. 실제 Verify는 비어 있는 argv·basis·evidence를 허용하지 않는다.

판정은 **일반화되지 않은 생성·초기 상태 계약**이다. 연구의 개별 선택을 모든 Reference Workspace의 필수 요구로 올려 확정 위반이라고 하지 않으며, 코드상 Recover 가능성을 곧 정의된 생성 경로로 보지도 않는다. 관련 009 기록에서 이를 공통 경로로 채택하거나 의도적으로 배제한 근거는 찾지 못했다. 후속으로 조사·판단 Workspace까지 이식할 때 생략·유예와 상태의 의미를 정할 필요가 있다.

### 3. 설치한 판단·관리 지침의 실제 수행

**`reconsider-work`의 현행 경로:** 05가 목표로 한 것은 완료 표현을 정확하게 바꾸는 데서 더 나아가 다음 작업 선택과 이미 의존한 결과를 바꾸는 일이다. [08 통합 기록](2026-09-08-15-skills-spec-ticket-reference-integration.md) 86–92행의 제한 모델 평가는 `work-artifact-briefing`, `work-discussion`, `explanation-recovery` 세 스킬이다. 현행 `reconsider-work`를 수행해 Main의 채택, Maintain의 실제 Spec·Ticket·state 갱신과 다음 실행까지 확인한 기록은 아니다.

**`update-project-context`의 현행 경로:** 03 457행의 대표 Project-wide 변화 검토는 [009 보완 기록](../../009-project-work-continuity-integration/records/2026-09-06-08-project-context-update.md) 62행과 [009 output](../../009-project-work-continuity-integration/output/index.md)에서 독립 행동 평가·실제 host 호출이 미검증으로 남아 있다. 최근 네 스킬의 검토를 이 관리 skill의 검증으로 합칠 수 없다.

**실제 host와 다음 실행자:** 등록·symlink·prompt 전달 코드와 제한 평가만으로 host의 발견·호출, 비동기 반영, 문서를 사용하는 다음 실행자의 인수까지 완료했다고 하지 않는다. [이전 통합 기록](2026-09-08-15-skills-spec-ticket-reference-integration.md)의 start/resume prompt 검사는 scripted runner였고 실제 host acceptance는 아니었다.

이를 현행 코드·문서가 없는 것과 구별한다. 이미 반영된 지침이 실제 행동에서 작동하는지의 미검증이다. 과거 05의 평가를 현재 08의 통합 동작 검증으로 재사용하지 않는다.

### 4. 연구의 비교·재현성 질문

01 274–279행과 06 비교의 후반부는 같은 코드 상태에 재접근 가능한 근거, 사용자 재설명·current 팽창·중복·유지비, 기능 완료와 전체 품질 사이의 차이를 질문한다. 현재 Verify에는 실행 전 선언 파일의 경로·SHA·크기와 argv·출력을 남기고 freshness를 읽는 장치가 있다. 다만 이는 전체 dirty worktree를 복구할 소스 보관이나 선언 밖 입력까지 포함한 완전한 재현을 보장하지 않는다. [Verify 계약](../../../../reference-project/context/work/harness/verify/README.md) 9–14·25–27행도 그 상한을 제한한다.

이 질문들은 전부 추가 runtime을 구현하라는 확정 요구가 아니다. 실제 적용 효과·비용을 주장할 때 확인할 항목이다. 지금 문서·코드가 제공하는 범위와 장기 운용에서 확인할 효과를 계속 구별해야 한다.

## 누락으로 세지 않은 차이

- **Spec 기본 도입:** 02의 Spec 배제·상세 AC 기본 읽기 제외는 07에서 변경됐고, Work당 Spec 하나와 Ticket 네 구성은 08에서 확정했다.
- **Project 물리 세 층:** 03의 물리 폴더 비강제 방향은 사용자 “그냥 층위를 만들어라” 정정으로 변경했다. [물리층 기록](../../009-project-work-continuity-integration/records/2026-09-04-07-project-context-physical-layers.md)에 근거가 있다.
- **timeout Decision의 현재 값 소유:** Decision을 현재 답의 기본 Owner로 삼지 않는 원칙은 유지하되 기존 명시적 normative Owner 예외를 보존했다. 당시 채택·물리층 기록에 의도가 있다.
- **과거 Workspace 비동기화와 현재 소비자:** 역사 Workspace는 자동 갱신하지 않는다. Project 경로·책임을 바꿀 때 실제 사용하는 active/default·session-bound Workspace는 먼저 맞추는 live consumer reconciliation을 보강했다.
- **옛 두 리뷰 스킬:** 05 archive의 `claim-impact-review`·`direction-gap-review`, 고정 판정 단위·reviewer·호출 절차는 현재 README가 자동 상속하지 않도록 정했다. 현재 `reconsider-work`에 더해 재설치할 요구가 아니다.
- **Matt의 전체 실행 체계:** 한 세션 크기의 Ticket, tracker·frontier·고정 분해/구현/리뷰 파이프라인을 보편 계약으로 채택하지 않았다. 실제 작업별 분해·위임·검토는 Main이 정하는 열린 배치다.
- **모든 작은 수정에 Workspace 생성:** 생성 skill의 명시 요청 조건·기존 수정 비대상과 Maintain의 unbound 기본값이 있다. 02의 작은 수정 예외를 생성 문서에 더 직접 표현할 수는 있지만, 현재 반대 동작을 강제하는 경로는 확인되지 않았다.
- **연구 작업대 root의 구조:** root의 memory/state와 비활성 자동 Maintain은 명시적인 적용 경계다. Reference 설치 상태와 구별한다.

## 후속 판단과 이번 작업의 한계

남은 내용을 한꺼번에 재이식할 필요는 확인되지 않았다. 계약 보완 후보는 Decision의 좁은 생성·보존 기준과 고정 검증이 없는 조사 Workspace의 생성·초기 상태다. 실제 효과를 확인할 우선 대상은 이미 설치한 재판단이 목표·의존 결과·다음 실행을 바꾸는 장면이다. Project 관리 skill과 실제 host 연결은 각각의 책임과 증명 범위로 이어서 확인할 수 있다. 이 우선순위는 이번 감사의 제안이며 새 실행·검토 체계를 채택한 것은 아니다.

이번에는 자료·Git·현재 파일·준비본을 읽기 전용으로 대조했다. 제품·Harness 테스트를 새로 실행하지 않았으며, 이전 전체 124개 중 timeout 한 개 실패·단독 통과를 해결된 것으로 바꾸지 않는다. 실제 Workspace activation·새 Verify·제품 코드·Reference 운영 계약·외부 저장소·전역 하네스는 변경하지 않았다. 이 분석과 active Workspace의 재진입 정보만 갱신한다.

별도 검토자가 이 보고서의 핵심 판정을 원문·현재 계약에 다시 대조해 중요한 정정사항을 찾지 못했다. 특히 Decision의 기존 내용을 누락으로 세지 않았는지, 고정 Verify가 없는 경우를 실행 불가로 과장하지 않았는지, 01의 질문·05 archive를 의무로 되살리지 않았는지 확인했다. 분석과 진입점 Markdown 6개의 로컬 링크 117개를 검사해 누락 target이 없었고 `git diff --check`도 통과했다. 분석 기록은 미커밋 상태로 남긴다.

## 후속 반영 — Decision 기준

같은 날 사용자가 다음과 같이 요청하고 감사 결과의 분류를 확인했다.

> 1번은 반영하면 될거고
>
> 2번은 뭐지?고정 검증 명령?
>
> 3번은 당연히 운영 검증이 남았다는거잖아?
>
> 나머지는 없는거야?

1번을 [Decision 계약](../../../../reference-project/context/project/decisions/README.md)에 반영했다. 별도 기록을 검토할 다섯 조건과 단순 현재값 갱신마다 만들지 않는 경계, 중요한 불확실성과 재검토 신호·실제 근거를 남기는 기준을 추가했다. 현재 답의 Owner와 대체 관계, 기존 timeout Decision의 명시적 예외는 유지한다. 기존 Project README와 갱신 skill이 이 계약을 참조하므로 같은 정책을 중복 작성하지 않았다. 과거 timeout 선택의 대안·이유를 새로 만들어 채우지 않았다.

2번의 고정 검증 명령은 `verify.json`에 사전에 지정해 두는 테스트·평가 실행 명령을 뜻한다. 코드 변경에는 실제 테스트 명령이 있을 수 있지만 설계 비교·조사에는 해당 주장을 판정할 실행 명령이 없을 수 있다. 이때 Verify 계약을 생략·유예하는 생성 규칙이 미구체화된 것이며, 원문에서 확정한 요구의 이식 누락으로 판정한 항목은 아니다. 이번에는 설명만 했고 Verify나 생성 계약을 바꾸지 않았다.

3번은 사용자가 지적한 대로 실제 운영 검증의 잔여다. 이식 누락에 포함하지 않는다. 이번 조사 범위에서 이 외에 현행 채택 내용의 추가 이식 누락은 찾지 못했다. 앞의 전체 대조는 반영 전 감사로 보존하며, 그중 Decision의 부분 반영 상태는 이 후속 변경으로 보완됐다. 커밋은 하지 않았다.

## 마무리와 커밋 요청

후속 사용자가 “그래 마무리 기록하고 커밋하자”라고 요청했다. 전체 대조 기록·현재 상태·진입점과 Decision 계약 보완을 함께 커밋 대상으로 정했다. 앞 절의 미커밋 표현은 각각 작성 당시의 상태다.

Decision 변경을 별도로 원문과 대조해 생성 조건·불확실성 보존의 잔여를 채웠고, 기존 Owner·예외·대체 관계와 Project README·갱신 skill의 참조 경로를 유지했음을 확인했다. 새 고정 형식이나 과거 선택 이유의 창작, skill별 정책 복제는 추가하지 않았다. 변경 Markdown 8개의 로컬 링크 136개와 공백·파일 끝을 검사해 오류가 없었고 `git diff --check`도 통과했다. 제품·Harness runtime 변경이 없어 테스트를 반복하지 않았다.

이번 대조와 요청받은 보완은 마무리한다. 고정 검증 없는 조사 Workspace의 생성 경계는 열린 일반화 사항이고, 실제 운영 검증은 별도 잔여다. 둘을 추가 이식 누락이나 이번 미완료 실행으로 취급하지 않는다. 커밋 범위에서 기존 untracked `.DS_Store`를 제외한다.
