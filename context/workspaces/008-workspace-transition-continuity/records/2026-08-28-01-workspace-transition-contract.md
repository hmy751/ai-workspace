# Workspace 생성·전환 의미 계약

날짜: `2026-08-28`

## 발단과 정정

이미 Context Harness가 적용된 Project에서 001의 후속으로 002 Workspace를 만들었다. 001의 원래 문제 문서는 002의 첫 설계 판단에도 중요했지만, 생성 세션은 채택 방향 문서만 선택하고 원래 문제 문서의 현재 역할과 필수 읽기 시점을 002 current에 남기지 않았다. 새 002 세션은 bounded Recover가 제공한 current를 따라 현황을 파악했으므로 그 원문을 먼저 읽지 않았다.

사용자는 이 사건이 이식 skill을 사용한 세션에서 생긴 것이 아니라 이미 이식된 환경의 Workspace 전환에서 생겼다고 정정했다. 따라서 직접 문제는 `apply-context-harness`가 아니며, Recover도 선택된 packet을 제한적으로 읽는 자기 역할을 수행했다. 빠진 책임은 새 Workspace 생성자가 새 goal을 기준으로 predecessor의 의미를 다시 선별해 successor가 독립적으로 재진입하게 만드는 기준이었다.

## 사용자 결정에서 유지할 의미

- 관련 자료를 무지성으로 모두 옮기지 않는다.
- 다음 Workspace가 모르면 판단이 달라지는 의미는 링크로만 두지 않고 새 current에 실제로 적는다.
- 상세 원문과 근거는 복제하지 않고 원래 canonical로 연결한다.
- 필요하면 이전 Workspace의 exact artifact를 참고할 수 있지만 Workspace끼리 계속 갱신하거나 역전파하지 않는다.
- 공통 Project context가 별도 층으로 있으므로 Workspace 사이의 복제와 동기화로 공통 사실을 유지하지 않는다.
- Recover 정의를 넓혀 과거 Workspace나 source·records 전체를 자동 탐색하게 하지 않는다.

## 선택한 책임 배치

- Workspace collection canonical: 생성·전환의 의미 선별 기준, successor의 독립성, 단방향 참조와 비동기화 경계
- Main과 사람: 새 goal 해석, 현재 의미 선별, source 권위나 Project 공통 승격이 애매할 때의 결정
- Successor current: 다음 재진입에 현재 적용되는 의미와 필수 원문의 exact 경로·역할·이유·읽을 시점
- Successor source: 선택한 원래 canonical과 provenance
- Predecessor output·records: 필요할 때만 읽는 당시 산출물과 역사적 선택 근거
- Project context: 상세 Owner와 source 권위가 Project 전체 적용을 뒷받침하고 Project context Owner가 반영을 결정한 현재 사실
- Recover: 이미 선별된 successor packet의 bounded read
- Maintain: explicit Workspace 하나 안의 durable 변화 관리
- Main session 경계: 이전 session 종료 뒤 active 기본값·host binding을 맞추고 successor의 explicit Recover와 새 Maintain grounding으로 시작

## 의도적으로 만들지 않은 것

- 이전 Workspace 전체 상속 또는 live current dependency
- bidirectional sync, back propagation과 predecessor 변경 자동 추종
- 과거 Workspace를 차례로 열어야 하는 recursive recovery
- Workspace 사용 횟수에 따른 Project context 자동 승격
- 필수 `parent_workspace_id`, 공통 handoff 문서, 새 schema·hook·자동 생성기

## 검증 상한

이번 변경은 사람과 AI가 적용할 의미 계약과 Harness 비소유 경계를 문서로 정한다. 구조·링크·기존 tests를 확인할 수 있지만, 어떤 원문이 실제로 빠지면 판단이 달라지는지 자동 판정하거나 실제 후속 Workspace 생성이 항상 충분한 current를 만든다는 것은 semantic acceptance 전에는 증명하지 않는다.
