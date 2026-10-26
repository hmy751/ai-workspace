# Case B — 로그인 예제 지원 설명의 확인·반영 관찰

대상: `update/noline-demo`. 요청: “로그인 예제의 현재 지원 설명이 실제 확인 범위와 맞는지 확인하고 필요한 내용을 반영해줘.”

## 실제 결과

지원 설명 한 문장이 실제 근거보다 넓었다. `context/project/current/authentication-flow/INDEX.md`의 「지원 범위와 확인」에서 다음 문장을 정정했다.

변경 전:

> 제품의 DB·queue 귀속 검사와 조율, UI·네트워크·디스크 저장까지 실제 환경에서 확인했다.

변경 후:

> 제품의 DB·queue 귀속 검사와 조율, UI·네트워크·디스크 저장은 연결하지 않았으며 실제 환경에서 확인하지 않았다.

현재 코드·검사의 대상은 메모리 세션 저장, 주입한 대기·조회 함수와 Login·Reauth의 함수 호출이다. 기존 인증 계약과 root README, Work 실행 기록·state, current 본문의 형성 맥락도 같은 제한을 설명한다. 따라서 새 제품 약속을 축소한 것이 아니라 지속할 현재 사실의 오류를 정정한 것이다. A에서 본 파일이 같다고 전제하지 않고 B의 파일과 코드를 별도로 읽어 판단했다.

## 읽은 진입점과 핵심 근거

- B root `AGENTS.md`, `README.md`, `context/README.md`, `context/USAGE.md`, Work 지침·목록을 확인했다.
- B `../skills/context-update/SKILL.md`와 Project의 `MAINTENANCE.md`, `REFERENCE/reading.md`, `REFERENCE/composition.md`, `context/CONTENT-POLICY.md`를 읽었다. 허용된 사실 정정은 반복 승인 없이 진행하고 Work current·코드 변경으로 권한을 넓히지 않았다.
- `../skills/development/SKILL.md` 및 verification 상세의 검사 적절성·근거 재사용 절을 읽고, 기존 검사의 이름뿐 아니라 입력·실행 경로·assertion이 지원하는 범위를 대조했다. 별도 개발 구현·전체 검증 역할을 시작하지 않았다.
- Project current의 본문·구성 안내·형성 자료 README·context·evidence·구성 기록, 인증 guidance, Work 001의 현재 state·Project 선택·output·기존 실행 기록을 읽었다. 인용된 원본 저장소 경로로 조사 범위를 넓히지 않았다.
- `examples/authentication/README.md`와 실제 `src/{authentication,device-session,consumers,demo}.mjs`, `tests/authentication.test.mjs`를 읽었다. `demo.mjs`는 메모리 변수에 저장하고, 인증 응답을 내부에서 만들고, 선행 대기를 즉시 끝내며, 이동은 “UI 없음”을 출력한다. 검사도 주입한 함수와 메모리 값을 사용한다.

## 직접 실행한 확인

현재 복사본에서 Node.js `v23.11.0`으로 아래 세 실행을 수행했다. 과거 기록의 Node.js 24.16.0 실행과 구별한다. 외부 패키지·서비스를 사용하지 않았다.

| 실행 | 직접 확인한 결과 |
| --- | --- |
| `node --test examples/authentication/tests/*.test.mjs` | 검사 7, 통과 7, 실패·취소·건너뜀 0, 종료 코드 0 |
| `node examples/authentication/src/demo.mjs` | 메모리 저장 → signed-in 공개 상태 → Query 요청 → “로그인 완료” → 이동 요청(UI 없음) → Query 완료. 종료 코드 0 |
| `node examples/authentication/src/demo.mjs --refresh-fails` | 인증 완료·이동 요청 뒤 조회 오류를 별도로 전달. 종료 코드 0 |

정상·실패 실행 모두 최종 상태 `signed-in`, 저장 계정 `demo-user`, 보존 여행 1개였다. 첫 검사는 제어 가능한 Promise로 선행 작업과 저장이 끝나기 전 새 공개 상태가 나오지 않는지, 조회 Promise가 끝나기 전에 인증 완료가 전달되는지 확인한다. 나머지 검사는 저장 실패 보존, 조회의 동기·비동기 실패 분리, 인증 실패·다른 계정 및 귀속 불명 데이터 보호, 두 소비자의 안내·행동을 확인한다. 실제 DB·queue·UI·네트워크·디스크 저장을 확인한 실행은 없다.

## 실제 변경과 반영 확인

복사본 내부 변경은 `context/project/current/authentication-flow/INDEX.md` 한 파일의 한 문장이다. 본문을 다시 읽고 Project 진입·current 안내 및 Work의 Project 선택·output에서 연결되는 역할과 대조했다. 진입점이 약속하는 “현재 구현·검사 범위”를 본문에서 읽으면 이제 메모리 예제와 실제품 미연결 범위가 일치한다. 관련 문서 검색에서도 기존 README·state·형성 자료는 제한을 이미 올바르게 설명했다.

제품 계약·Personal 기준·코드·테스트·Work current·output·과거 source/records는 수정하지 않았다. 형성 맥락과 기존 기록은 이미 메모리 예제와 실제품 통합의 차이를 설명하므로 새 결론으로 덮어쓰거나 날짜·문구를 형식상 맞추지 않았다. 사실 정정의 전후와 근거·이번 실행 결과는 Main이 요청한 이 관찰 파일에 남겼다. 이번 실행의 수치를 Project 본문에 새 현황 정본으로 복제하지 않았다.

## 미확인·남은 일

요청된 지원 설명의 확인·반영은 완료했다. 실제 UI·서버·디스크 저장소·Query 라이브러리·DB/queue 조율, 부분 저장 실패·재시작 복구, 동시 세션 변경, callback 예외와 후속 응답의 인증 거부 전환은 확인하지 않았으며 현재 예제의 지원 완료로 보고하지 않는다. 실제 연결이나 새로운 소비자 요구를 수행할 때 해당 경계의 설계·검사가 필요하다.

Work의 기존 상태는 메모리 예제 확인과 실제품 미확인을 계속 올바르게 가리킨다. 이번 문서 정정은 Work 목표 전체 완료나 사용자 수락을 새로 판정하지 않는다. 요청된 관찰 파일을 제외한 지속 실행 이력 추가가 필요하면 Main이 Work의 관리 책임으로 판단할 수 있다.

원본 ai-workspace, 다른 Desktop 저장소, 다른 담당자의 복사본, 외부 서비스에 접근하지 않았다. 패키지 설치·커밋·child agent 생성은 하지 않았다.
