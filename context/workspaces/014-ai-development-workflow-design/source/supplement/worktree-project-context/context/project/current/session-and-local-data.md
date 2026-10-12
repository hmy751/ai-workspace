# 기기 세션과 Local 데이터의 현재 연결

인증 만료·재로그인·로그아웃을 바꿀 때, 기기 데이터와 진행 중 요청·저장이 실제로 어떻게 이어지는지 확인한다. [기기 세션의 제품 의미](../common/device-session.md)와 [인증·세션 변경 가이드](../guidance/authentication-and-session.md)에 더해 현재 Store·보안 저장소·SQLite·요청·화면이 나누어 맡은 보호 범위를 설명한다. 2026-09-25에 제품 기준 `759cba3`의 아래 코드와 기존 검사·기록을 대조했으며, 이번 문서 작성에서 제품 검사를 새로 실행하지 않았다.

## 복원한 계정과 DB의 실제 귀속을 함께 확인한다

복원에는 **기기 세션의 계정 확인과 실제 DB·queue의 귀속 확인**이 함께 필요하다. 두 검사의 책임은 다음처럼 연결돼 있다.

| 책임 | 현재 구현 | 판단에 필요한 경계 |
| --- | --- | --- |
| 기기 기록 읽기·공개 상태 적용 | [token-storage](../../../apps/client/src/shared/services/auth/token-storage.ts), [Auth Store](../../../apps/client/src/shared/store/auth.ts) | DB 준비 뒤 복원한다. 기록 부재는 signed-out, 읽기·해석·귀속 확인 실패는 restore-failed다. 실패 시 기록·DB·queue를 보존하고 Local 접근을 막는다. |
| DB·queue 계정 확인 | [local-account](../../../apps/client/src/shared/services/auth/local-account.ts) | queue의 별도 userId 컬럼이 없어 원본 row와 payload를 대조한다. 원본 누락·해석 실패는 unresolved이며 다른 계정 row 발견보다 우선한다. |
| Local 실행 대상 확인 | [local-access](../../../apps/client/src/shared/services/auth/local-access.ts) | Store가 제공한 Local 계정에 더해 SQL에서 계정·삭제되지 않은 여행·활성 조건을 확인한다. |

Store는 signed-in과 reauth-required에 Local 계정을 제공하고 보호된 Remote에는 signed-in만 허용한다. Signed-in은 사용할 인증 수단을 보유했다는 뜻이다. DB의 userId만으로 새 세션을 복원하지 않는다.

Queue 원본은 재전송과 같은 계정 복원 양쪽의 근거다. [vacuum의 참조 보호](sync-and-cleanup.md)는 이 관계를 지키지만 모든 손상을 복구하는 기능은 아니다.

## 인증 저장과 사용자 절차는 다른 범위를 조율한다

현재 두 가지 순서 보호가 함께 사용된다.

| 보호하는 작업 | 담당 | 보호 범위 |
| --- | --- | --- |
| 계정 검사·기기 저장·상태 적용 | [Auth Store](../../../apps/client/src/shared/store/auth.ts)의 저장 큐 | 복원·로그인·refresh가 메모리와 기기를 서로 다른 순서로 덮지 않게 한다. 토큰은 private session에 둔다. |
| 로그인·로그아웃·탈퇴 전체 | [session-lifecycle](../../../apps/client/src/shared/services/auth/session-lifecycle.ts) | sync 종료, cleanup 종료, 접수된 DB 작업 종료를 기다린 뒤 본작업을 실행한다. |

[로그인 서비스](../../../apps/client/src/shared/services/auth/login-service.ts)는 전체 절차 안에서 Store 검사·저장을 실행한다. 같은 계정의 DB·queue는 유지하고 다른 계정은 거절한다. 저장 실패는 기존 상태·세대를 유지하며, 적용하지 못한 새 서버 토큰은 폐기를 시도한다. 저장 후 Query 무효화 실패는 완료된 인증을 되돌리지 않는다.

인증 거부는 메모리의 토큰·상태·세대를 먼저 바꿔 즉시 요청을 막고 기기 저장을 뒤따르게 한다. 느린 refresh 저장이 이전 인증을 다시 공개하지 못한다. 저장 포맷·legacy 처리와 순서의 변경 계약은 [인증 가이드](../guidance/authentication-and-session.md)가 소유한다.

**현재 보호의 범위:** 공통 DB 실행 경계를 사용하는 작업에 대한 조율이다. 모든 직접 DB write·지도 작업·일반 HTTP 취소를 포함하지 않는다. Store action도 공개돼 있어 소비자가 전체 절차를 거치도록 타입만으로 강제하지 않는다. 별도 session-store/facade나 재시작 복구 journal은 없다.

## 같은 사용자 ID라도 이전 요청은 새 세션에 적용하지 않는다

[공유 인증 interceptor](../../../apps/client/src/shared/services/auth/auth-interceptor.ts)는 요청 config에 시작 당시 sessionId를 유지하고, 토큰 사용·갱신·재전송·성공 응답에서 현재 세션인지를 확인한다. 같은 계정으로 재로그인해도 세대가 바뀌므로 이전 요청의 결과를 새 세션의 성공으로 적용하지 않는다. 일반 API와 sync가 이 인증 경계를 공유하며, 각 응답 형태와 retry의 차이는 [API 가이드](../guidance/api-contracts.md)에서 다룬다.

서버 응답을 받은 뒤 Local 저장까지 기다리는 경로도 별도 확인이 필요하다. [여행 활성화](../../../apps/client/src/entities/trip/data/useActivateTrip.ts)는 transaction 진입에서 요청 세대와 응답 Trip·Schedule·Expense의 userId를 다시 대조한다. 이는 해당 응답의 Local 저장 경계에 대한 보호다. 이미 활성화된 빠른 경로, 후속 지도·경로 다운로드 전체 또는 앱 재시작을 넘는 지속 세대까지 같은 보호로 입증하지 않았다.

## 종료 실패는 실패한 저장소까지 설명해야 한다

[logout-service](../../../apps/client/src/shared/services/auth/logout-service.ts)는 접수된 저장을 끝낸 뒤 PENDING·IN_PROGRESS·FAILED를 모두 확인한다. 미전송 데이터가 있으면 일반 종료를 보류한다. 확인 이후에는 새 Local transaction이 차단되며 보류·실패 뒤 차단을 해제한다.

| 실패 지점 | 현재 남는 결과 |
| --- | --- |
| 서버 logout | Local 종료를 계속한다. |
| 서버 계정 삭제 | Local 종료로 진행하지 않는다. |
| DB reset의 재생성 | row·queue는 rollback되지만 **DB 준비 상태는 해제된다.** |
| DB reset 성공 후 기기 인증 삭제 | DB는 이미 비어 있다. Store는 이전 보호 인증을 다시 허용하지 않고 선택·캐시는 finally에서 비운다. |

### DB reset 실패 뒤 재시도 연결은 남아 있다

2026-10-01에 이 브랜치의 코드를 다시 대조했다. [DB reset](../../../apps/client/src/shared/db/index.ts)은 실패 뒤 DB를 미준비로 남긴다. 로그아웃·force logout 재시도도 먼저 queue 통계를 읽으므로 DB 재준비 없이 같은 절차를 다시 부르면 통계 조회에서 막힐 수 있다.

[AppInitialization](../../../apps/client/src/application/AppInitialization.tsx)의 재시도는 앱 진입 준비 실패에 연결돼 있다. 이미 진입한 화면에서 reset 실패를 받아 이 준비를 다시 실행하는 연결은 확인되지 않았다. [보존 검사](../../../apps/client/tests/shared/services/auth/local-preservation.test.ts)도 reset 실패 뒤 `initializeDatabase()`를 직접 호출한 다음 row·queue를 확인한다. **데이터 rollback 근거를 같은 프로세스의 화면 복구 완료로 읽지 않는다.**

### 로그인 화면에서 제공하는 복구

[LoginScreen](../../../apps/client/src/screens/LoginScreen.tsx)은 restore-failed 재시도와 데이터 손실 확인 후 force logout을 제공한다. signed-out에서도 기기 정리에 접근할 수 있어 잔존 DB 때문에 다른 계정 로그인이 막힌 경우의 진입점을 제공한다. 이 진입점의 존재가 위 DB 실패 복구를 보장하지는 않는다.

재인증 중 기존 여행으로 돌아갈 수 있고, [Root Navigation](../../../apps/client/app/_layout.tsx)은 같은 계정 재로그인 뒤 가능한 경우 이전 화면으로 돌아간다. 같은 계정 key의 Stack 유지와 모든 native form 입력 보존은 구별한다.

## 확인 범위와 다시 볼 변화

[세션 동시성 검사](../../../apps/client/tests/shared/services/auth/session-concurrency.test.ts), [interceptor 검사](../../../apps/client/tests/shared/services/auth/auth-interceptor.test.ts), [복원 검사](../../../apps/client/tests/shared/services/auth/session-restoration.test.ts)는 제어 가능한 저장·요청으로 순서와 세대·실패 전달을 다룬다. [Local 보존 검사](../../../apps/client/tests/shared/services/auth/local-preservation.test.ts)는 실제 Drizzle SQL과 Node 메모리 SQLite로 종료 중 새 저장 거절, 접수된 저장 반영 뒤 종료 보류, reset 실패의 rollback과 queue 원본 보존을 다룬다. [과거 분리 검증 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-22-02-five-stage-commits-and-verification.md)의 실행 범위는 이 fixture와 실제 OAuth·SecureStore·서버 rotation·기기 SQLite·화면 조작을 구별한다.

세션 상태·저장 포맷·계정 판정·세대 확인, 로그인/종료 consumer, activation 저장 또는 DB pause 참여가 바뀌면 변경 책임자가 연결을 다시 확인한다. 특히 인증 삭제 실패의 안내를 바꿀 때에는 이미 끝난 DB reset까지 함께 보고, 전체 절차 밖에서 Store action을 새로 쓰면 그 consumer가 생략한 보호가 없는지 대조한다. 원격 기기 제어와 앱 강제 종료 뒤 지속적인 종료 재개는 현재 지원에 포함되지 않는다.
