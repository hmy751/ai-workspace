# memory·Ticket 배치와 records 경계 제3 리뷰

날짜: 2026-09-08

## 요청과 목적

사용자 원문:

> 그럼 마지막으로 이상황을 제3리뷰한테 줘봐 필요한 근거 논의들 줘서

memory 유지·제거와 Ticket의 정의·진행 배치에 관한 [직전 대화](2026-09-08-04-memory-removal-and-records-boundary.md)를 독립적으로 검토한다. Main이 Ticket state 배치, memory 제거 가능성과 추천, 다시 memory 유지 추천으로 설명을 바꾼 과정 자체도 검토 대상이다. 유지·제거 중 어느 결론을 확인해 달라는 의뢰는 아니다.

## 전달한 입력과 권한

독립 reviewer `review_memory_ticket_boundary`를 새 맥락에서 실행했다. Main의 대화 전체를 자동 상속하지 않고, Ticket의 state 배치 질문부터 최신 리뷰 요청까지 사용자 원문과 Main 답변의 핵심 원문 발췌를 순서대로 전달했다. 모델·추론 설정은 parent에서 상속했으며 별도 하향 설정하지 않았다.

함께 제공한 자료 접근점:

- 이 저장소의 context·Workspace 책임 문서.
- Workspace 001의 active/history, current/records, memory/state 합의, 폴더화, 최소 memory, output/records 결정 기록.
- Reference의 실제 Workspace 규칙과 sample current. 읽기 전용이며 runtime 실행·binding 활성화는 하지 않도록 했다.
- Workspace 010의 초기 종합, Spec 범위·배치 결정, Ticket 외부 용례, memory 제거 후보 분석과 채택한 Spec 구성·예시.
- 사용자가 지정한 Matt 한국어 독해본의 `to-tickets`와 고정 revision, memory-harness-research의 06 개념 트레이드오프와 01 문제 분석.

Spec·Ticket 도입, 다섯 Spec 구성과 각 Markdown 파일, 기존 goal/constraints 대체, project-context 유지, 가벼운 Spec 하나 가정, Workspace별 독립 스냅샷 조건은 유지한다고 전달했다. memory 배치와 Ticket 상태는 검토 대상이다. 과거 선택을 새 설계를 막는 규칙으로 읽지 않도록 했다.

Reviewer는 문제 정의와 자료 선택을 기각하거나, 필요한 repo 내 관련 근거를 더 읽을 수 있다. Main의 최신 추천도 검토 대상이다. 파일 수정·설치·다른 agent 생성·외부 게시·지정하지 않은 Desktop 저장소·archive/private JSONL 접근은 범위 밖이다.

## 요청한 판단

memory 유지 아래 Ticket 정의·진행을 함께 두는 안, memory 제거 후 current 직접 배치, 필요한 경우 기존 정의·진행 분리나 state 배치를 비교한다. 후보 구분이 부적절하면 그것도 지적할 수 있다.

records/current의 원래 선택 이유, 새 실행자에게 전달할 단위, 중복 갱신, Spec 밖에 유지할 판단과 전체 목표 판단을 근거로 추천·비용·반대안이 더 나아지는 조건을 설명하도록 했다. 기존 memory/state 의미가 바뀌면 무엇이 바뀌는지 밝히고, ‘가능함’과 ‘지금 더 나음’을 구별하도록 했다.

보고는 기존 어휘와 구체 항목으로 설명하고, 핵심 쟁점과 정확한 근거 위치·확인 범위를 남기도록 했다. 세부 구현 영향 목록이나 Ticket schema 전체 확정은 요청하지 않았다.

## 추가 근거 전달

Reviewer의 중간 보고는 008의 새-session fallback 교정을 채택한 Spec의 ‘제약·현재 설계·가정’에서 다룰 수 있다는 의견을 포함했다. Main은 Workspace 공통 운영 규칙을 Spec에 복사하지 않기로 한 기존 합의와 대조하도록 요청했다. 해당 Workspace에서 설계하는 산출물의 판단인지, 작업에 적용하는 공통 운영 맥락인지 구별하고, 한 사례가 Spec에 들어간다는 사실을 모든 지속 판단에 확대하지 않도록 했다. 추천 방향을 바꾸도록 요구하지 않았다.

## Reviewer 최종 보고

아래는 reviewer가 반환한 최종 보고다. Main의 채택 여부는 뒤에서 구분한다.

**Ticket의 정의와 진행은 함께 두고, state는 Workspace 전체의 상황·판단·다음 행동을 맡기는 편을 추천합니다. 그 조건에서는 memory 폴더를 제거하고 current에 직접 배치하는 쪽에 조금 더 무게를 둡니다.** current가 이미 ‘지금 사용할 내용’을 모으므로, memory가 추가로 구분할 역할이 작아지기 때문입니다. 다만 memory 유지안도 성립하며, 두 안의 운영 효과 차이가 확인된 것은 아닙니다.

1. **records를 고려해야 한다는 지적은 맞지만, 그것이 memory 폴더 유지의 근거는 아닙니다.**
   처음 구분한 이유는 누적 기록과 현재 행동에 적용할 내용을 분리하기 위해서였습니다. 완료한 일도 후속 행동에 영향을 주면 current에 남고, 여전히 사실이어도 필요하지 않으면 records에서 찾게 했습니다. 이 선택 책임은 `current/spec`, `current/tickets`, `current/project-context`에서도 유지할 수 있습니다. Main이 “제거 가능이 제거 우월을 뜻하지 않는다”고 정정한 것은 타당합니다. 그러나 최신 유지 추천에도 **current 아래 한 번 더 묶는 것이 무엇을 개선하는지**에 대한 근거는 부족합니다. [current·records 결정 17행](/Users/hammyeong-yeon/Desktop/context-harness/context/workspaces/001-reference-implementation/records/2026-08-13-02-current-records-migration.md:17)

2. **memory에 진행까지 담은 Ticket을 두는 것은 기존 의미를 유지하는 선택이 아닙니다.**
   기존 memory는 작업 단계가 바뀌어도 유효한 목표·기준·결정 등을, state는 진행·불확실성·최근 결과를 맡았습니다. Ticket 전체를 memory에 넣으면 memory는 ‘유지하는 작업 문서’, state는 ‘전체 상황과 판단’으로 바뀝니다. 이 변경 자체는 합리적이지만 명시해야 합니다. 정의와 진행을 분리하면 기존 구분은 유지되지만 실행자가 두 위치를 맞춰 읽어야 합니다. 이번처럼 Ticket을 받고 실행·갱신하려는 목적에서는 함께 두는 이득이 더 분명합니다. 다만 Ticket 한 문서가 관련 Spec과 Project 맥락까지 전부 대신한다는 뜻은 아닙니다. [기존 역할 18행](/Users/hammyeong-yeon/Desktop/context-harness/context/workspaces/001-reference-implementation/records/2026-08-13-03-project-workspace-context-agreement.md:18), [인계 비용을 기록한 논의 26행](/Users/hammyeong-yeon/Desktop/context-harness/context/workspaces/010-spec-ticket-workspace-design/records/2026-09-08-03-ticket-references-and-placement.md:26)

3. **‘Spec 밖에 유지할 판단’이 있다는 이유도 새 Spec 구성에 맞춰 다시 봐야 합니다.**
   앞선 논의는 “새 세션을 반드시 시작해야 한다는 규칙은 당시 상황의 보수적 선택이었다”는 판단 교정을 memory 필요성의 사례로 들었습니다. 그런데 지금 채택한 Spec에는 ‘제약·현재 설계·가정’과 선택 이유가 있으므로, 해당 작업에서는 그 부분이 이 판단을 맡을 수 있습니다. 이 사례가 더는 Spec 밖 문서를 반드시 요구하지는 않습니다. `project-context`는 별도로 유지할 이유가 확인됐고, 그 밖의 내용은 실제로 생겼을 때 적절한 current 문서에 두면 됩니다. 미리 모든 나머지를 memory로 분류할 필요까지 입증된 것은 아닙니다. [실제 판단 교정 36행](/Users/hammyeong-yeon/Desktop/context-harness/context/workspaces/008-workspace-transition-continuity/current/memory.md:36), [채택한 Spec의 판단 유지 역할 69행](/Users/hammyeong-yeon/Desktop/context-harness/context/workspaces/010-spec-ticket-workspace-design/output/spec-components-and-rationale.md:69)

4. **전체 목표 판단을 지키는 핵심은 폴더보다 서로 다른 내용을 맡기는 데 있습니다.**
   예를 들어 timeout 작업이라면 Spec은 ‘설정 누락 시 기본값을 적용한다’는 요구와 완료 기준을, Ticket은 그 구현 범위·개별 진행·완료 근거를 맡습니다. state는 “구현은 확인했지만 전체 완료 판단에는 무엇이 남았는가”를 설명합니다. records에는 분석 과정과 상세 검증을 남깁니다. state가 Ticket의 상태 목록을 다시 수동 관리하면 어느 폴더에 두든 중복 갱신 문제가 생깁니다. 반대로 완료한 Ticket이 후속 작업의 근거라면 current에 남겨도 됩니다. 실제 Reference도 검증 결과와 사람의 해석·완료를 구분합니다. [현재 state의 책임 7행](/Users/hammyeong-yeon/Desktop/context-harness/reference-project/context/work/workspaces/001-default-timeout/current/state/index.md:7)

따라서 제 추천은 **current 아래 Spec·Ticket·project-context를 직접 두고, state에서 전체 상황과 판단을 관리하는 것**입니다. 이득은 Ticket을 memory/state 기준으로 다시 분류하지 않아도 된다는 점입니다. 비용은 memory라는 공통 위치가 사라지므로 current 진입점에서 문서의 역할과 읽을 위치를 안내해야 한다는 점입니다.

반대로 사용자가 **Spec·Ticket·지속 판단 문서를 한 묶음으로 탐색하고 관리하는 것이 실제로 편하다**면 memory를 유지해도 됩니다. 그 경우에는 ‘변화가 적은 맥락’이라는 기존 정의를 ‘현재 사용하는 작업 문서’로 바꾼다는 선택을 분명히 하면 됩니다. records와의 구분은 어느 안에서도 current 전체가 책임집니다.

확인 범위는 기존 결정 기록, 실제 Reference 문서, 채택한 Spec 구성, 지정한 Ticket 독해본과 배경 분석입니다. 과거 대화 전체와 실제 운영 효과를 재검증하지 않았으며, 파일 변경이나 runtime 실행은 하지 않았습니다.

## Main의 대조와 판단

기존 합의의 memory/state 정의, 실제 Reference state의 기계 사실·사람 해석·완료 구분, 008의 작업 목표와 fallback 교정, 채택한 Spec 5번의 역할을 직접 대조했다.

- **근거 있는 지적으로 받아들임:** memory 아래 Ticket 진행을 함께 두고 state를 전체 상황으로 설명하면 기존 역할 정의를 일부 바꾸는 것이다. 직전 Main이 이를 단지 기존 해석을 덜 엄격하게 하는 정도로 설명한 것은 변경을 충분히 드러내지 못했다.
- **근거 있는 지적으로 받아들임:** records/current 경계는 memory 폴더 유지의 충분한 이유도 제거의 충분한 이유도 아니다. 현재 의미를 선택해 유지할 책임은 두 배치 모두 필요하다. Main의 제거 추천과 이후 유지 추천 모두 ‘가능함’에 비해 상대안보다 나은 이득의 설명이 약했다.
- **설계 추천으로 수용 가능:** Ticket 정의·진행을 함께 관리하고 Workspace 전체 state에서 같은 상태를 중복 관리하지 않는 안은 인계 목적에 맞는다. 관련 Spec·Project 맥락까지 Ticket에 복사한다는 뜻으로 확대하지 않는다. 아직 사용자 채택은 아니다.
- **008 사례의 적용 범위:** 008은 session 전환 동작 자체를 설계·구현하는 Workspace이므로 그 fallback을 해당 작업 Spec의 설계·가정에서 다룰 수 있다는 해석은 타당하다. 다른 작업에서 적용받는 공통 운영 규칙까지 Spec에 옮기거나 Spec 밖 지속 맥락이 전혀 없다고 결론 내리지 않는다.
- **최종 선택 보류:** reviewer의 약한 제거 선호는 역할 중복을 줄이려는 설계 판단이다. 실제 탐색·읽기·갱신 편의의 비교 효과가 입증된 것은 아니므로 자동 채택하지 않는다. 유지한다면 기존 memory 의미가 일부 바뀐다는 사실과 문서를 별도로 묶는 편의에 근거해 선택해야 한다.

리뷰 수신과 주요 근거 대조는 완료했다. 사용자가 유지·제거와 배치를 확정한 상태는 아니다. 실제 Reference 구조·runtime·schema·hook은 변경하지 않았다.
