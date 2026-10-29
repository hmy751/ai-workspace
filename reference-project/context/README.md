# Personal·Project·Work context

이 디렉터리는 개인의 판단 기준, 제품의 지속 맥락, 개별 작업의 현재 의미와 기록을 서로 다른 책임으로 유지한다. Work는 이번 목표에 필요한 Personal·Project 본문을 선택해 사용하며 그 내용을 복제하거나 자동으로 채택하지 않는다.

- [Personal](personal/README.md): 여러 작업에 가져갈 개인 판단의 이유·조건과 협업 경험·해석·열린 후보. 기준 채택은 사용자가, 허용된 편집은 Main 또는 지정 담당자가 맡는다.
- [Project](project/README.md): 여러 작업에 지속되는 제품 의미·현재 현실·작업 계약을 `common/current/guidance`와 Owner 관계로 유지한다. `decisions`는 선택 이유를, `REFERENCE`는 구성·읽기 기준을 맡는다.
- [Work](work/README.md): Workspace의 현재 상태·원자료·goal 산출물 지도·기록과 이를 복구·유지·검증하는 공용 Harness의 운영 경계. 기존 Main·Maintain 관계와 생성·전환 계약을 유지한다.

Project 본문은 제품 문서의 복사본이나 링크 목록이 아니다. [Project README](project/README.md)는 실제 본문과 Owner를 찾는 안정된 진입점이며 Workspace는 필요한 본문과 선택 이유를 계약에 남긴다. Harness는 관리 장치로서 개인 기준·제품 의미·작업 목표를 소유하지 않는다. 제품 구현과 테스트는 [src](../src/)와 [tests](../tests/)가 소유한다.

## 읽고 적용할 때

[USAGE](USAGE.md)에서 질문별 선택·근거 대조·유효한 읽기 재사용 방법을 따른다. 현재 작업의 일반 재개는 [Work 지침](work/AGENTS.md), 한정된 제품 질문은 [Project 읽기 기준](project/REFERENCE/reading.md)으로 연결한다. 모든 영역과 형성 자료를 공통 필독 묶음으로 만들지 않는다.

## 본문을 관리할 때

Personal·Project와 이 공통 context 본문은 [CONTENT-POLICY](CONTENT-POLICY.md)의 본문·형성 자료 구별을 따른다. 체계 지침의 역할·진입·분할을 바꿀 때는 [SYSTEM-GUIDANCE](SYSTEM-GUIDANCE.md)를 적용한다. Work에는 새 정책의 구성을 적용하지 않고 기존 관리 계약을 따른다.

허용된 한정 반영은 [context-update](../.agents/skills/context-update/SKILL.md), 실제 권한과 내용 판단은 [Personal 관리](personal/README.md#기준을-고치는-경우)와 [Project 관리](project/MAINTENANCE.md)가 맡는다. 책임과 위치의 선택 이유는 [형성 자료](_background/README.md)에서 찾는다. Harness나 스킬을 교체해도 각 내용 Owner와 Work의 README·current·source·output·records 의미는 남는다.
