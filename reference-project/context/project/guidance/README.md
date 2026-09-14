# Project guidance

이 폴더는 관련 작업에서 지킬 구체적인 개발 계약과 이유, 적용·변경 판단·검증 방법을 소유한다. 새 기능뿐 아니라 관련 수정·리팩터링·조사에도 쓰는 작업 가이드이며 조언이나 실행 순서에 한정하지 않는다.

각 본문에서 적용할 작업과 중요한 예외를 이해할 수 있어야 한다. 모든 가이드에 같은 제목이나 적용·비적용·재검토·제거 항목을 강제하지 않으며, 실제 판단에 필요한 구조를 따른다.

## 현재 지침과 소비자

[설명과 근거 기준](explanation-and-evidence-criteria.md)은 사용자가 의미와 실제 근거의 관계를 이해하고 다음 판단을 만들 수 있게 하는 조건부 기준이다. 제품 의미·현재 구현·완료 판단의 정본을 대체하지 않는다. 적용 범위·재검토 신호·제거 조건은 그 본문이 소유한다.

- [work-discussion](../../../.agents/skills/work-discussion/SKILL.md): 명시 호출로 Work의 결과·선택을 구체화할 때 읽는다.
- [work-artifact-briefing](../../../.agents/skills/work-artifact-briefing/SKILL.md): 기존 작업물의 역할·연결·현재 상태·근거 범위를 조사해 설명할 때 읽는다.
- [explanation-recovery](../../../.agents/skills/explanation-recovery/SKILL.md): Project 사실·근거 범위·용어의 현재성이 앞선 설명의 뜻을 바꿀 때 읽는다. 대화만으로 충분하면 저장소를 먼저 읽지 않는다.

호출 조건과 실행·종료 방법은 각 스킬이 소유한다. [reconsider-work](../../../.agents/skills/reconsider-work/SKILL.md)는 이 기준의 consumer가 아니다. 모든 대화나 모든 Workspace의 Recover 입력에 이 지침을 자동으로 추가하지 않는다. 현재 default-timeout 제품 검증의 선택 문서에도 추가하지 않으며, 설명 스킬을 사용할 때 필요한 범위에서 읽는다.

## 추가·갱신·제거

새 guidance는 관련 작업에서 반복해서 적용할 계약·판단·검증이 있고 기존 본문으로 충분히 설명되지 않을 때 추가한다. 적용 조건이 사라지거나 다른 canonical이 그 책임을 직접 소유하면 통합·제거한다. 세부 구성은 [Project 구성 기준](../REFERENCE/composition.md)을 따른다.
