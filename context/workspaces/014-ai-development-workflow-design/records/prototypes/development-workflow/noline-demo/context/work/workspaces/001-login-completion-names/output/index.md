# 현재 산출물

이 Work는 아래 실제 코드·검사를 현재 결과로 선택했다. 이 폴더에 사본을 만들지 않는다.

| 결과 | 실제 위치 |
| --- | --- |
| 인증 적용과 조회 요청의 완료 분리 | [서비스와 wrapper](../../../../../examples/authentication/src/authentication.mjs) |
| 귀속 확인·저장·공개 상태 | [기기 세션 Store](../../../../../examples/authentication/src/device-session.mjs) |
| Login·Reauth의 완료 표현 | [두 소비자](../../../../../examples/authentication/src/consumers.mjs) |
| 정상·조회 실패를 실행할 장면 | [실행 코드](../../../../../examples/authentication/src/demo.mjs) |
| 완료·실패 경계를 확인할 검사 | [동작 검사](../../../../../examples/authentication/tests/authentication.test.mjs) |

제품 계약은 [Project 인증 가이드](../../../../project/guidance/authentication-and-session.md), 현재 구현 관계는 [Project current](../../../../project/current/authentication-flow.md)가 소유한다. 이 Work의 함수명 선택과 실행 결과는 [records](../records/README.md), 전체 상황은 [state](../current/state/index.md)에서 구별한다. 결과로 선택했다는 사실이 실제품 통합이나 사용자 수락을 뜻하지 않는다.
