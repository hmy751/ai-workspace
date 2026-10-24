# Work context

한 작업의 요구·현재 판단·실행 결과를 Workspace별로 유지한다. 제품 공통 의미는 Project가, 개인 판단은 Personal이 소유하고, Work는 지금 맡은 작업에 필요한 내용을 선택해 사용한다.

- [workspaces](workspaces/README.md): 작업별 current·source·output·records와 현재 작업
- [development 스킬](../../../skills/development/SKILL.md): 관련 맥락 선택·재탐색, 구현·검토·확인과 Main의 종합·결과 전달·Owner별 갱신을 맡는 공통 본문. 개발 절차의 진입점은 Work 밖의 스킬이며 구현 완성·인계·검토 입력·수정·종료를 본문과 상세에서 찾는다. 기록·정본 갱신은 대상 지침을 따르는 Main이 수행한다.
- [작업 지침](AGENTS.md): 재진입과 직접 확인

실제 Noline에는 이 경계 안에 Recover·Maintain·Verify를 실행하는 `harness/`가 있다. 이 프로토타입은 context 본문과 수동 적용 장면을 다루므로 해당 실행기를 설치하지 않았다. 문서 조회를 Recover 실행으로, 직접 테스트를 Verify receipt 생성으로 부르지 않는다. 기계 계약·상태 파일은 실제 runtime을 연결할 때 그 schema와 함께 구성한다.
