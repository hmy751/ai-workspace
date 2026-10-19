# 001 — 로그인 완료 표현과 실행 경계

인증 적용과 조회 갱신의 완료를 구별해 호출부가 이름·callback·안내만 보고 과도한 결과를 기대하지 않게 하는 Work다. 부여한 초기 장면을 바탕으로 실행 가능한 작은 예제를 작성했고, 현재는 그 결과와 context 적용 구성을 검토한다.

- [작업 정의와 선택한 맥락](current/memory/index.md): Spec 다섯 관점, Ticket, 개인·제품 입력
- [전체 상황과 다음 행동](current/state/index.md)
- [초기 입력](source/index.md), [실제 산출물](output/index.md), [선택·실행 기록](records/README.md)

개인 기준은 목적·사용처·변경 비용을 판단하게 하고, Project 계약은 저장·상태 적용·후속 조회의 경계를 제공한다. 이 Work는 그 둘을 현재 두 소비자의 조건에 대입한 선택과 근거를 소유한다. 함수명 선택을 개인 공통 의무나 모든 Noline 코드의 정책으로 승격하지 않는다.

이 Work의 예제 실행과 프로토타입 전체를 설계하는 바깥 작업은 별개다. 현재 작성한 코드는 실제 Noline 제품의 변경이 아니며, 자동 Harness나 기계 상태 대신 이 README·memory·state에서 직접 재진입한다.
