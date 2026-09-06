# Project·Work continuity integration memory

마지막 갱신: `2026-09-06`

## 목표

TripProof 작업에서 관찰·분석한 판단 연속성 문제를 현재 `reference-project/`의 실제 책임과 대조해 다음을 결정한다.

- Project common context가 여러 Work에 필요한 현재 의미·상태·조건부 기준과 실제 Owner를 더 잘 드러내려면 어떤 계약이 필요한가.
- Work가 변하는 판단의 재진입 경계이면서도 안정된 구현 구간의 Spec·Ticket·bounded brief를 배제하거나 복제하지 않으려면 어떤 관계를 가져야 하는가.
- 국소 근거가 넓은 완료로 승격되는 문제를 기존 Verify·Maintain과 책임 충돌 없이 어디까지 다룰 수 있는가.
- 실제 적용 효과가 없는 설계 후보를 어떤 bounded replay와 live pilot 뒤에만 Reference 책임으로 채택할 것인가.

물리 layer와 적용 acceptance는 `7bd5089`에 반영됐다. 후속 논의에서는 Project 맥락의 충분한 보존·구체적인 불확실성 표현과 `update-project-context`의 도입을 확정했다. 이 기준은 Project README가, skill은 적용 절차가 소유한다. 이번에는 문서·skill·호출·이식 경로를 보완하며 Workspace·Spec 관계와 Verify는 변경하지 않는다.

## 계속 유지할 판단

- 현재 Reference는 이미 Project common context와 Work context, Workspace와 교체 가능한 Harness를 분리한다. 이번 작업은 그 구조를 다시 만드는 일이 아니다.
- 외부 연구가 가장 강하게 드러낸 문제는 context 부재 하나가 아니라 **국소적으로 유효한 구현·test·interface·commit이 자신보다 넓은 제품·코드·Work 완료의 충분성으로 승격되는 것**이다.
- Project context의 `공통 맥락 / 현재 상태 / 조건부 지침`은 반복해서 혼동하지 않도록 `context/project/common/`, `current/`, `guidance/`라는 필수 물리 layer로 드러낸다. `decisions/`는 현재 답의 네 번째 층이 아니라 중요한 선택 이유와 재검토 신호를 보존하는 별도 경계다.
- `context/project/README.md`는 물리 layer와 실제 내용 위치를 찾는 안정된 Recover routing anchor다. 각 layer의 `README.md`는 책임과 현재 항목을 명시한다. Guidance 본문이 없어도 layer README에 그 사실과 추가 조건을 남기며, root의 포괄 `overview.md`는 두지 않는다.
- Workspace는 Project 전체나 모든 layer를 자동으로 읽지 않는다. Root README와 현재 goal의 판단을 바꾸는 `common/`, `current/`, `guidance/`, `decisions/` 아래 실제 문서만 선택하고, guidance는 적용 조건이 맞을 때만 고른다.
- Recover contract schema `6`은 root README를 필수 anchor로 두고, 다른 Project 선택을 네 허용 경계 아래 Markdown으로 제한한다. Recovery packet schema는 shape가 바뀌지 않아 `6`을 유지한다. Project routing 변경 뒤에는 active/default와 current-generation explicit binding을 포함한 live consumer를 실제 Recover와 semantic target review로 확인한다.
- Project 일반 진입점은 실제 내용의 정본 위치, 유효성을 판단할 책임 주체, 관련 작업에서의 읽기 조건, 변경 규칙과 관리 장치의 비소유 경계를 찾게 해야 한다.
- Project context 완료는 파일·link 존재만이 아니라 다음 관련 Work가 제품 목적·사용자 문제·domain 관계·현재 구현 경계·관련 판단 기준을 재추론하지 않아도 되는 content recoverability를 요구한다.
- 필요한 근거 있는 맥락은 일부가 불확실하다는 이유로 조용히 빼거나 전체 의미를 약화하지 않는다. 지지되는 내용은 해당 층에 분명하게 쓰고, 미정·미확인·충돌은 그 대상과 근거를 구체적으로 밝힌다. 층위는 책임 구분이며 확실성 등급이 아니다.
- 위 보완의 근거는 TripProof 첫 재구성이 층위·색인을 갖추고도 코드로 확인하기 쉬운 사실과 방어적 제한을 우선해 제품 목적·판단 이유를 빠뜨렸던 실패다. 보존과 새로운 결정의 구분을 함께 유지하며, 이미 승인된 반영을 위해 같은 결정을 반복 요청하지 않는다.
- `update-project-context`는 여러 Workspace에 계속 유효할 변화와 요청된 누락 복원을 기존 Project 문서에 반영한다. 작업 중 자연스러운 경계에서 사용하고 Workspace 종료에 묶지 않는다. Workspace Maintain과 합치지 않으며, 관리 기준은 Project README에서 읽는다.
- Project context를 바꾼 뒤에는 producer만 보지 않는다. 영향을 받는 live consumer—active/default Recover consumer와 explicit session-bound Workspace—의 사람용 current·선택·output target을 reconcile하거나 successor로 전환하고 실제 Recover와 fresh-context 의미 검토로 확인한다.
- 완료되어 소비 경로에서 내려온 역사 Workspace는 새 Project 구조에 역동기화하지 않는다. 아직 live consumer인 Workspace에는 이 예외를 적용하지 않는다.
- Workspace·Spec 관계는 사용자가 다시 생각할 필요가 있지만 현재는 두자고 했다. 과거 문서의 독립 장기 Spec 대체 방향과 이후 Spec/Ticket·bounded brief 가설을 근거로 현재 Reference를 더 규칙화하지 않는다. Verify의 필수 여부·조건부 구성도 이번에는 변경하지 않는다.
- 제품·코드·국소 판단은 서로 다른 근거를 요구한다. 근거가 직접 관찰한 대상·범위·revision보다 넓은 완료를 닫아서는 안 된다는 제한 원칙은 기존 Verify의 proof ceiling과 정합적이다.
- 판단 변경이 관련 기존 결과에 영향을 줄 수 있다는 방향은 유지하되, 영향 검색법과 결과 상태 분류는 아직 적용 전 설계다.
- `claim-impact-review`, `direction-gap-review`, 정확한 trigger와 두-reviewer 구성은 Reference 채택안이 아니다. 먼저 report-only bounded replay에서 실제 선택·범위·완료와 기존 결과 지위가 달라지는지 확인한다.
- Finding은 조사·구현·새 Workspace·Project context 변경을 자동 실행하지 않는다. 고권위 제품 의미, 핵심 책임 변경·연기, 중요한 trade-off와 acceptance는 사용자 또는 명시된 책임자에게 남는다.
- Harness나 skill은 Project·Work 의미의 Owner가 아니며, 제거해도 사람이 canonical 계약을 따라 같은 책임을 수행할 수 있어야 한다.

## 현재 Reference에서 이어받는 실제 기준

- [`reference-project/context/project/README.md`](../../../../reference-project/context/project/README.md): Project 물리 layer, 상세 Owner 우선순위와 선택적 읽기의 live 기준
- [`update-project-context`](../../../../reference-project/.agents/skills/update-project-context/SKILL.md): Project 관리 기준을 적용하는 실행 절차
- [`reference-project/context/work/workspaces/README.md`](../../../../reference-project/context/work/workspaces/README.md): Workspace 내부 Owner와 수명 경계의 live 기준
- [`reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md`](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md): 독립 Workspace 생성·전환과 단방향 참조의 live 기준
- [`reference-project/context/work/harness/verify/README.md`](../../../../reference-project/context/work/harness/verify/README.md): claim·basis·evidence와 사람 acceptance를 분리하는 live 기준
- [`reference-project/context/work/harness/maintain/README.md`](../../../../reference-project/context/work/harness/maintain/README.md): 한 Workspace의 durable 변화 반영과 Project-level 자동 승격 비소유의 live 기준

완료된 [`001-reference-implementation`](../../001-reference-implementation/)의 current는 live Reference의 이후 schema·Maintain 변경을 모두 반영하지 못해 이번 작업의 현재 기준으로 사용하지 않는다. 필요한 과거 선택 이유만 exact record로 확인한다. [`008-workspace-transition-continuity`](../../008-workspace-transition-continuity/)의 session binding 결과도 이번 Project·Work 의미 설계의 전제로 자동 상속하지 않고, 실제 live Reference와 관련 canonical만 대조한다.

## 조사와 변경 제약

- 외부 입력의 기준 경로는 `/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity`다.
- 최초 외부 intake는 `f9a397d75d99da9c42aa2eac0562eb6d7d204dda` 위 dirty working tree였다. 이번 재독 때 HEAD는 `d80f571`이며 지정한 01·02·03 문서는 최초 intake와 SHA-256이 같다. 시점별 근거는 source intake와 08 보완 기록을 함께 본다.
- 지정 범위 밖의 다른 Desktop 저장소, private 대화 원문과 네트워크 자료로 근거를 확장하지 않는다.
- 외부 자료의 수치와 장면은 보존된 내부 감사·분석으로만 사용하며 이번 작업에서 원 evidence를 독립 재검산했다고 말하지 않는다.
- 실제 TripProof 적용은 `chore/archive-project-harness`의 clean HEAD `8b1418d6e67c7897e933af3c8eaf0c76547c5d9b`에서 읽었고 `main`보다 4 commits 앞선 미병합 상태다. 현재 적용 구조와 장기 유지·제품 효과를 구분한다.
- 새 taxonomy·hook·runtime·reviewer는 이번 범위가 아니다. 도입이 확정된 Project 관리 skill은 책임·호출·비적용 경계를 보존해 이식하며, 실제 host invocation과 장기 효과를 정적 검사로 주장하지 않는다.
- Reference 구현 뒤에는 이 Workspace의 current·output을 실제 diff·검증 상태와 함께 갱신하고, 과거 analysis나 machine receipt를 새 완료 증거로 바꾸지 않는다.
