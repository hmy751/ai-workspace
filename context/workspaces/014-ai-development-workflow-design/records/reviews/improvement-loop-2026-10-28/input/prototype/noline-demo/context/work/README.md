# Work context

한 작업의 요구·현재 판단·실행 결과를 Workspace별로 유지한다. 제품 공통 의미는 Project가, 개인 판단은 Personal이 소유하고, Work는 지금 맡은 작업에 필요한 내용을 선택해 사용한다.

- [workspaces](workspaces/README.md): 작업별 current·source·output·records의 관계와 일반 재개의 기본 선택. 기본 선택은 이 목록 한곳에서 관리한다.
- [development 스킬](../../../skills/development/SKILL.md): 관련 맥락 선택·재탐색, 구현·검토·확인과 Main의 종합·결과 전달·Owner별 갱신을 맡는 공통 본문. 개발 절차의 진입점은 Work 밖의 스킬이며 구현 완성·인계·검토 입력·수정·종료를 본문과 상세에서 찾는다. 기록·정본 갱신은 대상 지침을 따르는 Main이 수행한다.
- [작업 지침](AGENTS.md): 재진입, Main의 현재 상태·근거 유지와 직접 확인
- [생성과 전환](workspaces/CREATE-AND-TRANSITION.md): 요청된 독립 목표의 의미 구성·인수 확인, 기존 또는 새 Work로의 수동 전환 계약. [생성 스킬](../../../skills/create-context-workspace/SKILL.md)은 이 계약을 적용하는 수행 수단이다.

이 프로토타입은 context 본문과 수동 적용을 다루며 Recover·Maintain·Verify 실행기를 설치하지 않았다. 문서 조회를 Recover 실행으로, 직접 테스트를 Verify receipt 생성으로, 목록의 기본 선택 변경을 실제 host 세션 연결로 부르지 않는다. 설치된 실행 장치를 사용하는 대상에 옮길 때에는 그 대상의 계약·권한과 의존을 별도로 대조한다. 과거 자동 Maintain 활성화 절차를 이 demo에 연결하지 않는다.
