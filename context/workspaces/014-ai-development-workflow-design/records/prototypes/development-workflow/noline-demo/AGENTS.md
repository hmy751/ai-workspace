# Noline demo 작업 진입

이 지침은 이 demo의 context와 예제 코드에 적용한다. 먼저 [context](context/README.md)에서 Personal·Project·Work의 담당을 확인한다.

Main이 일반 작업을 재개할 때에는 [Work 지침](context/work/AGENTS.md)과 지정된 Workspace의 memory·state·output을 읽는다. 사용자 지정이 없으면 [Workspace 목록](context/work/workspaces/README.md)의 기본 선택을 따른다. 이번 요청의 대상 지정과 다음 일반 재개의 기본 선택을 바꾸는 일은 구별한다.

관련 맥락의 선택·읽기·실물 대조는 [공통 사용 방법](context/USAGE.md)을 따른다. 한정 설명·읽기 요청은 해당 본문과 필요한 실물에서 시작하고, Work가 없어도 수행한다. 개발 구현·수정·검토·실행 재개는 [개발 절차](../skills/development/SKILL.md)로 연결한다. 읽기 요청을 이유로 개발 전체나 새 Work를 시작하지 않는다.

범위를 정해 위임받은 구현·검토·검증 담당자는 적용 지침과 맡은 목표·계약·실물·관련 원문부터 읽는다. 전체 Workspace 인수를 자동으로 수행하지 않고, 불분명한 조건은 필요한 current·원자료를 추가로 확인한다. 상위 지침과 맡은 범위의 계약은 계속 적용한다.

제품의 의미·계약은 [Project](context/project/README.md), 개인의 판단 조건은 [Personal](context/personal/README.md)이 각각 소유한다. 구현이 계약과 다르면 이름만 좁혀 감추거나 문서를 코드에 맞춰 조용히 바꾸지 않는다. 관련 요구와 실제 동작을 대조한다.

지정한 Personal·Project 반영은 [context-update](../skills/context-update/SKILL.md), 이번 Work 정리는 Work 관리 계약으로 수행한다. 요청된 새 독립 Work는 [create-context-workspace](../skills/create-context-workspace/SKILL.md)를 사용하며, 기존·새 Work로의 전환은 [생성·전환 계약](context/work/workspaces/CREATE-AND-TRANSITION.md)을 따른다. 실제 host 연결은 이 수동 demo의 목록 변경과 다르다.

예제 코드는 [examples/authentication](examples/authentication/README.md)에 있다. 변경한 경계의 검사를 직접 수행하고 실제 결과·미확인을 해당 Work에 남긴다. 실제 Noline의 Harness나 제품 검증을 실행한 것으로 보고하지 않는다.
