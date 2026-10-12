# Project guidance

이 폴더는 관련 작업에서 지킬 구체적인 계약과 그 이유, 판단·적용·검증 방법을 담는 작업 가이드를 소유한다. 새 기능뿐 아니라 수정·리팩터링·조사에서도 선택할 수 있다. 필요하면 실행 순서나 실패 대응을 포함하지만 조언이나 순서에 한정하지 않는다.

여러 API가 함께 지킬 개발 계약도 관련 가이드의 본문이 될 수 있다. 제품·데이터 의미 자체를 소유하는 [common](../common/README.md)과의 차이는 상세함이 아니라 주 책임이다. 본문은 적용할 작업, 중요한 예외와 다시 확인할 조건을 설명하고, 필요한 제품 전제는 짧게 이어 쓴다.

## 현재 지침과 소비자

[코드 표현과 책임을 읽는 기준](code-readability.md)은 새 기능과 기존 코드 수정에서 중괄호·빈 줄·이름·함수 배치·주석·로그·비동기 표현을 판단할 때 읽는다. 기존 코드 전체 정리나 lint 변경을 요구하지 않는다.

[동작을 보존하는 코드 리팩터링](behavior-preserving-refactoring.md)은 기존 동작을 유지하며 표현·흐름·책임과 여러 소비 지점의 수정 부담을 줄일 때 읽는다. 변경 전후의 동작 보존과 개선 효과를 따로 판단하고, mock·native·DB 등 검증 경계의 상한을 구별한다.

[API 계약과 변경 가이드](api-contracts.md)는 client API, server route, 공유 schema, serializer와 user scope를 추가·수정·리팩터링할 때 읽는다. Schedule과 Expense의 구체적인 적용, 일반 조회와 sync의 soft-delete 차이, 현재 오류 정책의 열린 충돌을 함께 설명한다.

[연결 관측과 화면 접근](network-and-policy.md)은 Network Store의 관측 수명·refresh와 실제/표시 상태, Policy·Router·UI·Service 책임, 활성 조회 미확정과 제한 중 입력 보존을 바꿀 때 읽는다. 화면 정책 표와 실제 실행 조건의 차이를 함께 설명한다.

[앱 준비와 초기 작업](app-startup.md)은 DB 준비·인증 복원 시도·화면 진입의 순서, 데이터 삭제 없는 재시도, Root·Navigation·인증 후 작업의 수명을 바꿀 때 읽는다. 제한된 application 배치와 Expo route 조건을 포함한다.

[인증 상태와 기기 세션 전환](authentication-and-session.md)은 계정 검사·기기 저장·공개 상태의 순서, 인증 거부의 즉시 차단, 같은 계정의 새 세션과 늦은 응답, 로그인·종료의 실패와 데이터 보존을 변경할 때 읽는다.

[로컬 데이터·동기화·정리](local-data-and-sync.md)는 대상 여행별 repository 분기, entity와 queue의 원자성, DB 실행 간섭, sync 실행·실패·재시도와 cleanup의 원본 보존을 바꿀 때 읽는다. Data/Service와 entity 구조의 기존 의미도 이 본문이 소유한다.

[설명과 근거 기준](explanation-and-evidence-criteria.md)은 사용자가 의미와 실제 근거의 관계를 이해하고 다음 판단을 만들 수 있게 하는 조건부 기준이다. 제품 의미·현재 구현·완료 판단의 정본을 대체하지 않는다. 적용 범위·재검토 신호·제거 조건은 그 본문이 소유한다.

- [work-discussion](../../../.agents/skills/work-discussion/SKILL.md): 명시 호출로 Work의 결과·선택을 구체화할 때 읽는다.
- [work-artifact-briefing](../../../.agents/skills/work-artifact-briefing/SKILL.md): 기존 작업물의 역할·연결·현재 상태·근거 범위를 조사해 설명할 때 읽는다.
- [explanation-recovery](../../../.agents/skills/explanation-recovery/SKILL.md): Project 사실·근거 범위·용어의 현재성이 앞선 설명의 뜻을 바꿀 때 읽는다. 대화만으로 충분하면 저장소를 먼저 읽지 않는다.

호출 조건과 실행·종료 방법은 각 스킬이 소유한다. [reconsider-work](../../../.agents/skills/reconsider-work/SKILL.md)는 이 기준의 consumer가 아니다. 모든 대화나 모든 Workspace의 Recover 입력에 이 지침을 자동으로 추가하지 않는다. 설명 스킬을 사용할 때 필요한 범위에서 읽는다.

## 추가·갱신·제거

관련 작업에 계속 필요한 계약·판단·적용이 생기거나 유효한 기존 기준을 복원할 때 [구성 기준](../REFERENCE/composition.md)과 [관리 계약](../MAINTENANCE.md)을 따른다. 기존 본문에 통합할지 별도 가이드로 둘지는 읽는 상황과 갱신 책임으로 판단한다. 주제를 잘게 나누거나 같은 계약을 독립적으로 복제하지 않는다.

적용 조건이 사라지거나 다른 canonical이 그 책임을 맡게 되면 현재 소비 경로를 맞추며 통합·이동·제거한다. 중요한 선택 이유만 남길 필요가 있으면 결정 기록과 연결한다. 모든 가이드에 같은 제거 조건 목차를 요구하지 않는다.

## 기존 Noline 실행 기준

[Rules](../../../.claude/rules/README.md), [Guards](../../../.claude/guards/README.md), [Runbooks](../../../.claude/runbooks/README.md)는 compact guard와 반복 작업 진입을 유지한다. 통화·날짜·API·코드 표현·리팩터링과 위에서 다루는 네트워크·정책·앱 준비·인증·로컬 저장·동기화의 현재 의미와 적용 계약은 대응하는 Project 본문이 소유한다. 기존 경로는 해당 본문으로 이어져야 한다. 활성화·폼·지도 등 이동하지 않은 상세 책임은 각 기존 Owner가 계속 소유한다.
