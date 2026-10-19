# Work context

한 작업의 요구·현재 판단·실행 결과를 Workspace별로 유지한다. 제품 공통 의미는 Project가, 개인 판단은 Personal이 소유하고, Work는 지금 맡은 작업에 필요한 내용을 선택해 사용한다.

- [workspaces](workspaces/README.md): 작업별 current·source·output·records와 현재 작업
- [개발 절차](DEVELOPMENT.md): 개인 기준과 제품 계약 선택, 구현·검토, 결과별 갱신
- [작업 지침](AGENTS.md): 재진입과 직접 확인

실제 Noline에는 이 경계 안에 Recover·Maintain·Verify를 실행하는 `harness/`가 있다. 이 프로토타입은 context 본문과 수동 적용 장면을 다루므로 해당 실행기를 설치하지 않았다. 문서 조회를 Recover 실행으로, 직접 테스트를 Verify receipt 생성으로 부르지 않는다. 기계 계약·상태 파일은 실제 runtime을 연결할 때 그 schema와 함께 구성한다.
