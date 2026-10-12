# API 계약과 변경 가이드

Client API 함수, server route, 공유 request·response schema, DB row 직렬화와 user scope를 추가·수정·리팩터링할 때 읽는다. 이 본문은 편입한 API 주제의 현재 Project 기준을 소유한다. 기존 [API/Data context](../../../.claude/context/api-data.md)는 repository·React Query 구현 경로와 호환 진입을 맡는다.

## 경계마다 맡은 책임을 구별한다

**공유 Zod schema가 client/server 전송 계약을 소유한다.** Form 상태와 DB row는 별도 표현일 수 있지만 전송 경계에서 공유 request·response로 맞춘다.

| 책임 | 수행할 일 | 함께 맡기지 않을 일 |
| --- | --- | --- |
| Client API | HTTP 전에 request parse, 결과를 response parse한 뒤 data 반환 | Client 검증만으로 server 계약 적용을 대신하지 않음 |
| Server route | 인증·request 검증, 소유 범위의 DB 작업, response envelope 조립·검증 | Schema 선언만으로 실제 적용을 대신하지 않음 |
| Serializer | DB row를 API entity 표현으로 변환 | HTTP status·envelope·Zod 판정·query·오류 응답 |

Server 응답은 DB row를 직렬화하고 envelope를 조립한 뒤 **가장 바깥 response schema**를 적용한다. 바깥 schema가 entity를 포함하면 중간의 같은 검증은 별도 이유가 있는지 확인한다.

서버 검증은 잘못 조립한 성공 응답을 막고, client 검증은 받은 값이 잘못된 상태로 소비·Local 저장되는 것을 막는다. Activation처럼 여러 entity를 받는 경계에서도 둘을 하나의 중복 검사로 취급하지 않는다.

## Schedule에 적용되는 구체적인 계약

[Schedule entity](../../../packages/schema/src/entities/schedule.ts)는 scheduledAt·createdAt·updatedAt·nullable deletedAt을 offset-aware ISO datetime string으로 요구한다. [serializeSchedule](../../../apps/server/src/serializers/schedule.ts)이 PostgreSQL Date를 변환한다.

같은 serializer의 소비자는 **생성·전체 목록·단건·수정·Trip 하위 목록·Trip activation·sync pull**이다. 각 endpoint는 자기 envelope를 조립한 뒤 해당 response schema를 적용한다. 시간 의미는 [날짜와 시각](../common/date-and-time.md)이 소유한다.

| 작업 | 접근·삭제 조건 |
| --- | --- |
| 일반 조회·수정·삭제 | 인증 사용자 소유이며 삭제되지 않은 대상 |
| Schedule 생성 | 부모 Trip의 소유권·미삭제를 먼저 확인. `userId`는 인증 사용자에서 결정 |
| Trip 하위 목록·activation | 부모 접근 확인에 더해 자식 Schedule·Expense에도 user scope·미삭제 적용 |
| Schedule 수정·삭제의 실제 mutation | `id + userId + deletedAt IS NULL` 적용. 선행 조회 뒤 ID만으로 변경하지 않음 |
| Sync pull | User scope·갱신 시각을 적용하되 삭제 전파를 위해 soft-deleted row 포함 가능 |

일반 조회의 삭제 필터를 sync에 그대로 재사용하면 다른 기기에 삭제 사실을 전달하지 못한다. 부모가 없거나 타인 소유이거나 삭제된 경우는 같은 404로 처리해 자원 존재 여부를 추가 노출하지 않는다. 이 조건은 실제 PostgreSQL query와 route 응답 양쪽에서 확인한다.

## Expense client API와 오류 전달

[Expense client API](../../../apps/client/src/entities/expense/api/expenses.ts)는 생성·수정 request를 HTTP 전에 parse하고, 목록·생성·수정·삭제 response를 반환 전에 parse한다. API 함수 자체는 네트워크 오류를 기록한 뒤 같은 오류를 다시 던지는 catch를 두지 않는다. 현재 [apiClient](../../../apps/client/src/shared/api/fetcher.ts)가 Axios 오류를 `APIError`로 변환하고 React Query hook·화면이 전달된 오류를 소비한다.

이 사실은 서버와 client 전체의 오류 정책을 새로 정한 것이 아니다. 활성 [오류 처리 context](../../../.claude/context/error-handling.md)는 server의 `AppError + errorHandler`를 기본으로 설명하지만, Schedule route를 포함한 현재 Data route 일부는 `try/catch + sendInternalError`를 사용한다. 어느 쪽을 server 전체의 목표 구조로 삼을지와 error envelope·client mapping을 함께 바꿀지는 미결정이다. API 리팩터링 안에서 한쪽을 조용히 채택하거나 catch를 일괄 제거하지 않는다. 로그·catch 표현은 [코드 표현 기준](code-readability.md)에 따라 복구·전파·안내와 구체적인 기록 목적을 먼저 판단한다.

Expense `date`의 form·create/update request·entity response·두 DB 사이 계약 차이는 [날짜와 시각](../common/date-and-time.md), 통화 분리·금액 정밀도는 [통화와 금액](../common/currency.md)에서 판단한다.

## endpoint의 실제 인증 요구에 맞춰 요청한다

Trip·Schedule·Expense와 내 정보·회원 탈퇴 같은 보호된 요청은 현재 signed-in 세션의 공통 인증 interceptor를 사용한다. 일반 API와 sync가 다른 Axios 인스턴스를 사용해도 세션 확인·갱신·거부 기준은 공유한다. Sync의 별도 응답 형태와 HTTP retry는 그 인스턴스의 책임으로 유지한다.

토큰 교환은 인증 interceptor가 없는 `auth-transport`의 `authAxios`로 수행해 refresh가 보호된 요청에 다시 진입하거나 순환 import를 만들지 않게 한다. `auth-api`라는 파일명만으로 그 안의 모든 endpoint를 비보호 요청으로 분류하지 않는다. 현재 내 정보·회원 탈퇴는 보호된 `apiClient`를 사용하고, 로그인·refresh와 명시적인 refresh token 폐기는 해당 토큰을 전달하는 별도 경계다.

Places는 서버가 사용자 인증을 요구하지 않는 공개 서비스다. 인증 만료 상태에서도 정책상 가능한 검색을 보호된 client가 차단하지 않도록 인증 없는 전송을 사용한다. 공개 서비스라는 사실이 오프라인 실행 가능을 뜻하지는 않는다. 화면 정책과 실제 네트워크 확인은 [네트워크·Policy 가이드](network-and-policy.md)를 따르며, 요청 consumer가 이 조건까지 연결했는지는 현재 코드에서 별도로 확인한다.

## 자동 갱신과 오류의 복구 의미를 보존한다

보호된 요청은 시작 세션을 식별하고 응답·재전송 때도 현재 세션인지 확인한다. 첫 401에서는 같은 세션의 진행 중 refresh를 공유하고, 갱신·기기 저장이 성공하면 원요청을 한 번 재전송한다. Access token이 없고 refresh token이 있는 세션은 요청 전 갱신을 시도한다. 갱신이 필요한 시점에 refresh token이 없거나 refresh 응답이 401/403으로 거부되거나 재전송이 다시 401이면 재인증 필요를 전달한다.

연결 실패·일반 서버 장애는 자격 증명 거부와 다르다. 이런 실패나 갱신 토큰 저장 실패를 이유로 자동으로 재인증 상태를 만들지 않는다. 확정 거부의 즉시 요청 차단과 저장 순서, 같은 계정 새 세션 뒤 이전 응답 거절은 [인증 가이드](authentication-and-session.md)가 소유한다.

`AuthRequiredError`의 의미는 interceptor·Router·fetcher·Query를 지나도 유지해야 한다. Fetcher가 이를 일반 `UNKNOWN_ERROR`로 감싸거나 Router가 같은 상황을 일반 Error로 바꾸면 Query가 재시도하거나 UI가 다른 복구 행동을 제시할 수 있다. Axios 통신·서버 오류를 `APIError`로 바꾸는 것과 재인증 필요 오류를 보존하는 것을 구별한다.

자동 갱신 동안 원호출이 기다리는 것과 사용자가 재로그인할 때까지 HTTP 요청을 보관하는 것은 다르다. 갱신 실패로 종료한 일반 Remote 요청을 사람의 재로그인 뒤 자동 재생하는 대기열은 두지 않는다. 재로그인 뒤 새 조회와 Local `sync_queue`의 전송은 각각 별도 작업이다.

## 서로 다른 재시도의 수명을 합치지 않는다

| 재시도 | 다루는 실패·수명 | 현재 확인할 Owner·동작 |
| --- | --- | --- |
| 인증 갱신 | 한 보호 요청의 첫 401 | 공통 interceptor가 같은 세션의 refresh를 공유하고 원요청을 한 번 재전송 |
| Sync HTTP | 한 전송에서 발생한 5xx | Sync client가 최대 3회, 2·4·8초 간격으로 재시도. 네트워크 오류는 제외 |
| React Query 조회 | Query 실행 실패 | 기본값은 AuthRequiredError 재시도 없음, 나머지는 failureCount < 1. 개별 override는 별도 확인 |
| React Query mutation | Mutation 실행 실패 | 기본 retry 0 |
| 저장된 queue 재선택 | 다음 sync에도 남아 있는 Local 변경 | [데이터·동기화 가이드](local-data-and-sync.md)의 FIFO·막힌 작업·실패 보존 계약 |

횟수나 retry flag가 같아도 변경 이유와 수명은 다르다. 특히 sync HTTP 설정을 일반 API 전체의 재시도 정책으로 확대하지 않는다. 실제 구현 위치는 본문 끝의 인증·QueryClient·sync client 근거에서 찾는다.

## 재전송 결과는 실제 client 연결에서 확인한다

일반 `apiClient`는 Axios response에서 body를 꺼낸 뒤 API 함수가 response schema를 검증한다. Sync client는 Axios response 형태를 유지하므로 consumer의 body 접근 경계가 다르다. 인증 interceptor에서 `client(request)`로 재전송하면 내부 response interceptor를 이미 통과한 값이 바깥 처리로 돌아올 수 있다. 이때 body를 다시 꺼내 결과를 `undefined`로 만들지 않게 한다.

Interceptor만 단독 검사하면 refresh 횟수는 맞아도 최종 응답 shape 오류를 놓칠 수 있다. 실제 configure된 client와 API 함수를 연결해 원요청·refresh·재전송 횟수, 최종 body와 schema, 인증·일반 오류 전달을 함께 확인한다. 재전송 성공 여부와 서버에 같은 mutation이 한 번만 반영됐는지의 검증은 서로 다르다.

## 변경 전후에 확인할 증거

Schema·serializer·route 중 하나를 바꾸면 선언과 실제 소비자를 함께 대조한다. Schedule 시간 변환처럼 같은 책임이 여러 응답 경로에 있으면 한 경로의 성공만으로 전체 적용을 주장하지 않는다.

| 변경 경계 | 필요한 증거 | 그 증거만으로 입증되지 않는 것 |
| --- | --- | --- |
| Serializer | 순수 DB row → entity 단위 검사 | 모든 route의 실제 사용 |
| Server 응답 | Vitest·Supertest로 실제 Express middleware·router·status·JSON·schema 확인 | DB/auth를 대체한 경우 실제 SQL·JWT |
| 소유권·soft-delete | 타인·삭제 부모/자식·scoped mutation을 넣은 격리 PostgreSQL 검사 | 대체한 인증 middleware의 실제 JWT 처리 |
| Client API | 잘못된 request의 HTTP 전 실패, response parse, 호출 횟수·오류 전달 | Fetcher mock을 넘어선 Axios 실제 연결·네트워크·React Native 화면 |

인증 요청 변경은 [auth interceptor 검사](../../../apps/client/tests/shared/services/auth/auth-interceptor.test.ts), [auth API 요청 검사](../../../apps/client/tests/shared/services/auth/auth-api-requests.test.ts), [sync HTTP retry 검사](../../../apps/client/tests/shared/services/sync/http-retry.test.ts)에서 출발한다. 실제 SecureStore·OAuth·서버 토큰 회전과 외부 Places 서비스까지 검증한 것으로 넓히지 않는다.

현재 검증 진입점은 [client Expense API test](../../../apps/client/tests/entities/expense/api/expenses.test.ts), [Schedule route 계약 test](../../../apps/server/tests/routes/schedules.response-contract.test.ts), [Schedule serializer test](../../../apps/server/tests/serializers/schedule.test.ts), [Schedule PostgreSQL integration test](../../../apps/server/tests/integration/schedules.access-boundary.test.ts)다. 정확한 dependency 버전과 과거 실행 수치는 package 설정과 Workspace 기록이 소유한다.

Ticket 05 뒤 추가된 Trip·Expense serializer도 현재 route에서 사용되지만, 그 사실을 Ticket 05의 완료나 Schedule 외 server API 전체의 response·request·ownership 계약 완료로 확대하지 않는다. API 오류 구조, 실제 JWT·배포 process, 외부 서비스와 모든 Data route의 계약은 이 편입 근거로 확인하지 않았다.

이 기준은 Workspace 002의 [Ticket 04](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/04-expense-api.md), [Ticket 05](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/05-schedule-response.md), [Schedule 응답 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-14-01-schedule-serialization-and-response-contract.md), [접근 경계 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-14-03-schedule-access-boundary.md)과 현재 code·schema·test를 2026-09-14에 대조해 통합했다.

보호·공개 요청, 갱신·재전송과 retry 수명은 2026-09-25 [auth-interceptor](../../../apps/client/src/shared/services/auth/auth-interceptor.ts), [auth-transport](../../../apps/client/src/shared/services/auth/auth-transport.ts), [auth API](../../../apps/client/src/shared/services/auth/auth-api.ts), [fetcher](../../../apps/client/src/shared/api/fetcher.ts), [QueryClient](../../../apps/client/src/shared/lib/queryClient.ts), [sync client](../../../apps/client/src/shared/services/sync/api.ts), [Places 소비자](../../../apps/client/src/features/schedule/create-schedule/useLocationSearch.ts)와 [검사 근거 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-19-02-auth-review-checks.md)을 대조해 보강했다. 문서 반영 시 제품 검사를 새로 실행한 것은 아니다.
