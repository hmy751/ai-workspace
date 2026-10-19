# 구조 정정 뒤 Main의 직접 확인

2026-10-19. 사용자가 실제 Noline 구조를 직접 파악해 고치라고 요청한 뒤 Main이 context와 Workspace 배치를 재구성하고 직접 확인했다. 별도 실행자·검토자에게 위임하지 않았다. 상세 사용자 정정과 실제 Noline 조사 근거는 [바깥 기록89](../../../../../../../../2026-10-19-89-local-context-structure-correction.md)에 있다.

## 내용을 찾아 적용하는 경로

프로젝트 AGENTS에서 context로 들어가 personal·project·work의 책임을 구별한다. Work 지침에서 현재 Workspace의 Spec·Ticket·state·output을 찾고, 개발 절차에서 이름·완료 기준과 인증 계약을 각각 선택한다. Project 본문은 개인 기준을 읽지 않아도 인증 적용·조회 후속 실패의 의미를 설명한다.

이번 요구는 인증 적용 뒤 조회를 요청하되 결과를 기다리지 않는 완료 표현이다. Personal의 상세는 개명 자체를 의무로 만들지 않고 내부 사용처·호환 비용과 설명 보완 대안을 비교하게 한다. Project는 저장·상태 적용과 조회 완료를 구별한다. 두 입력의 현재 선택은 memory, 초기 가정은 source, 실제 코드·검사는 output, 선택·확인 이력은 records에서 찾을 수 있다.

이것은 작성자인 Main의 경로·의미 대조다. 새로운 작업자가 아무 맥락 없이 스스로 발견·이해·적용한 실험이나 사용자 수락은 아니다.

## 옮긴 경로에서 직접 실행

기준 디렉터리: `development-workflow/noline-demo/`.

```sh
node --test examples/authentication/tests/authentication.test.mjs
node examples/authentication/src/demo.mjs
node examples/authentication/src/demo.mjs --refresh-fails
```

검사7개가 통과하고 실패·취소·건너뜀은0개였다. 정상 장면은 저장·상태 적용, 조회 요청, 로그인 완료·이동 요청, 후속 조회 완료 순서였다. 실패 장면에서도 인증 완료 후 조회 오류를 따로 전달했고 최종 상태는 signed-in, 보존한 여행은1개였다. 이전 실행 결과를 복사해 이번 실행으로 대신하지 않았다.

예제 코드의 내용은 재배치 전과 같다. 실제 Noline UI·디스크·DB·queue·서버 연결, 동시 세션 변경·부분 저장 실패·callback 예외는 확인하지 않았다. 자동 Harness도 설치·실행하지 않았다.
