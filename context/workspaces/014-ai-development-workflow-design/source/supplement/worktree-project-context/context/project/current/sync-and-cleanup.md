# sync 실행과 데이터 정리의 현재 범위

동기화 완료 표시, 재시도, Local 보존 또는 여행·계정 정리를 바꿀 때 읽는다. [Local 데이터 보존의 의미](../common/local-data-preservation.md)와 [데이터·sync 변경 가이드](../guidance/local-data-and-sync.md)에 더해, 현재 Provider·DB·queue·engine·cleanup을 연결했을 때 무엇이 끝났다고 말할 수 있는지 설명한다. 2026-09-25에 제품 기준 `759cba3`의 아래 코드와 기존 검사·기록을 대조했다. 이번 문서 작성은 새 제품 실행이나 완료 수락이 아니다.

## 실행 요청과 DB 작업은 각각 공통 경계를 사용한다

실행 중복과 DB 간섭은 서로 다른 경계에서 막는다.

| 경계 | 현재 연결 | 보호 범위 |
| --- | --- | --- |
| Sync 실행 | [Provider](../../../apps/client/src/shared/services/sync/provider.tsx)와 수동 요청이 [lifecycle](../../../apps/client/src/shared/services/sync/lifecycle.ts)의 `executeSync`를 사용 | DB·인증·실제 online·override·종료 pause를 검사하고 engine/구독자보다 먼저 실행을 등록한다. 중복은 skipped이며 예약하지 않는다. |
| SQLite 작업 | [withTransaction](../../../apps/client/src/shared/db/utils.ts)과 [DB 실행기](../../../apps/client/src/shared/db/index.ts) | async callback 종료까지 commit을 기다린다. pull upsert·독립 queue 작업·metadata·reset도 같은 순서에 참여해 남의 rollback에 섞이지 않게 한다. |

Provider는 인증 세대·네트워크·override·pause 변화로 실행 가능해질 때 요청한다. 주기 실행은 기본 비활성이다. Provider remount와 React 밖 수동 호출도 같은 잠금을 쓰며, transaction 안의 queue INSERT는 바깥 큐에 다시 등록하지 않는다.

DB 보호는 같은 프로세스에서 공통 실행기를 거친 작업 사이의 보장이다. 모든 지도·경로 직접 write·조회·migration·native adapter 동시성까지 포함하지 않는다. 계정 종료의 대기 순서는 [세션 현황](session-and-local-data.md)에서 확인한다.

## queue 전송은 앞 작업의 상태와 실제 소유자에 의존한다

[getSyncableTasks](../../../apps/client/src/shared/services/sync/queue.ts)는 createdAt 순으로 PENDING과 retryCount가 3 미만인 FAILED의 연속된 앞부분을 선택한다. IN_PROGRESS 또는 한도에 도달한 FAILED를 만나면 뒤 작업을 함께 보류한다. [engine](../../../apps/client/src/shared/services/sync/engine.ts)은 각 작업을 보내기 전에 signed-in과 [원본 row에 근거한 queue 소유자](../../../apps/client/src/shared/services/auth/local-account.ts)를 현재 계정과 대조한다.

일반 전송 실패는 FAILED와 증가한 retryCount를 남기고 뒤 전송을 중단한다. 전송 중 AuthRequiredError는 현재 작업을 PENDING으로 돌리고 오류를 위로 전달한다. 인증·소유자 확인 단계에서 막힌 작업도 실패로 전달되며 다른 계정으로 전송하지 않는다. 한 번의 HTTP 요청 안에서 수행하는 5xx 재시도와 이후 sync 실행에서 저장된 FAILED를 고르는 것은 다르다. sync 전용 client의 최대 3회·2/4/8초와 일반 fetcher·Query의 차이는 [API 가이드](../guidance/api-contracts.md)의 retry 설명을 따른다.

중단된 IN_PROGRESS를 언제 어떤 방식으로 다시 보낼지는 현재 명시적 재개 정책이 남아 있다. 서버가 반영한 뒤 응답만 잃었을 가능성과 중복 적용을 다루는 문제도 status 재설정 하나로 해결되지 않는다. 재로그인 성공만으로 한도 도달 작업이나 남은 IN_PROGRESS까지 모두 재개된다고 설명할 수 없다.

## completed의 상한과 pull 저장 범위

**`completed`는 이번 engine의 push·pull 성공 반환이다. 전체 queue·정리·화면 갱신 완료가 아니다.** Lifecycle은 이 결과에 화면용 성공 시각을 갱신한다. 인증 중단이나 남은 FAILED·IN_PROGRESS는 실패로 전달한다. 활성 여행이 없어 pull을 생략해도 앞선 push 실패는 그대로 실패다.

| 함께 끝났다고 볼 수 없는 것 | 현재 이유 |
| --- | --- |
| 모든 Local 변경의 서버 반영 | 전송 목록은 시작할 때 읽고 마지막 통계는 FAILED·IN_PROGRESS를 검사한다. 실행 중 새 PENDING이 남을 수 있다. |
| 전체 cleanup·지도 삭제 | pending cleanup 실패는 push에서 잡고 계속한다. |
| 화면 재조회 | pull의 Query 무효화가 재조회 완료를 기다리지 않는다. |

화면용 성공 시각과 DB에 저장하는 pull의 serverTime cursor도 다른 값이다.

### Pull이 확인하는 것과 아직 확인하지 않는 것

| 경계 | 현재 지원 |
| --- | --- |
| 요청 대상 | 현재 계정의 활성 tripIds를 보낸다. 없으면 pull을 생략한다. |
| 응답 계정 | Trip·Schedule·Expense userId를 현재 계정과 대조한 뒤 upsert·cursor를 저장한다. |
| 응답 형태·여행 범위 | 공유 schema parse와 요청 tripId 집합/자식 tripId 검증은 없다. Raw shape·version 기본값·`as never[]`를 사용한다. |

공유 schema parse·typed upsert·malformed 거부는 아직 구현할 계약이다. 부분 저장과 cursor의 일관성, 미전송 Local 변경에 서버 값을 적용하는 충돌 결과는 추가 판단·검증이 필요하다. 현재 raw upsert를 최종 제품 선택으로 확정하지 않는다. 후속 책임은 [sync 결과·재시도·pull Ticket](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/15-sync-result-retry-pull-types.md)에 있다.

## 계정 종료와 여행 정리의 미전송 판정은 아직 다르다

| 정리 경로 | 현재 보호 | 남은 차이 |
| --- | --- | --- |
| [계정 종료](../../../apps/client/src/shared/services/auth/logout-service.ts) | PENDING·IN_PROGRESS·FAILED를 모두 손실 확인에 포함 | 여행별 정리의 보장을 대신하지 않는다. |
| 비활성화·지연 cleanup | `getPendingTasksForTrip`으로 보류 판단 | PENDING만 읽고 자식의 소속을 주로 payload.tripId로 찾는다. 다른 상태·부분 UPDATE·legacy/malformed payload의 연결이 남아 있다. |
| Vacuum | 오래된 soft-delete Schedule·Expense라도 상태와 무관하게 queue의 tableName+recordId 참조가 있으면 보존 | queue 제거 뒤에는 기간 조건으로 삭제한다. 모든 테이블·삭제 경로의 보장은 아니다. |

원본 row는 재전송과 계정 귀속 판정에 모두 필요하다. 먼저 지우면 queue 소유자가 unresolved가 되어 인증 복구에도 영향을 준다.

### 정리 실행 공유와 완료 집계

[cleanup-job](../../../apps/client/src/shared/services/sync/cleanup-job.ts)은 startup hook·sync의 요청을 activeCleanup Promise로 공유하고 결과가 있으면 캐시 무효화를 한 번 요청한다. [hook](../../../apps/client/src/shared/services/sync/usePendingCleanups.ts)은 지연 예약·해제를 맡는다. 화면 진입은 기다리지 않으며 캐시 무효화 실패도 정리 결과를 바꾸지 않는다.

**processedCount는 실제 완료 수가 아니다.** PENDING 때문에 일찍 반환한 여행도 count가 증가하고 일부 지도 정리·vacuum 실패도 성공 반환과 함께 남을 수 있다. 완료·보류·부분 실패의 결과 구분은 후속 구현이다. 미전송 predicate와 집계의 후속 책임은 [데이터 보존 Ticket](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/16-unsynced-data-cleanup.md)에 있다.

## 지도 메타데이터 정리와 native 저장 공간은 다르다

[지도 cleanup](../../../apps/client/src/shared/services/offline-map/cleanup.ts)에는 다른 두 경로가 있다.

| 경로 | 도시 참조 처리 | 참조가 0일 때 |
| --- | --- | --- |
| 만료 정리 | 삭제되지 않고 종료일+유예기간 안인 여행으로 다시 계산 | offlineCities row를 삭제한다. Native pack은 삭제하지 않는다. |
| 여행별 `cleanupOfflineMapForTrip` | 해당 여행의 참조를 줄임 | Mapbox pack과 DB row 삭제를 시도한다. |

DB row 부재나 정리 로그로 실제 byte 회수를 판단하지 않는다. [저장 용량 집계](storage-statistics.md)는 Mapbox pack의 byte를 직접 읽는다.

만료 정리에서 native pack을 어떻게 보존·회수할지는 지도 계약과 실제 동작을 더 대조해야 한다. 현재 metadata-only 경로를 최종 제품 정책으로 채택하지 않는다. 인증 만료 뒤 Local 이용 기간과 지도 참조 유예기간도 별도 정책이다.

## 근거와 갱신 책임

[lifecycle 검사](../../../apps/client/tests/shared/services/sync/lifecycle.test.ts), [인증 결과 검사](../../../apps/client/tests/shared/services/sync/auth-result.test.ts), [queue 재시도 검사](../../../apps/client/tests/shared/services/sync/retry.test.ts)는 제어 가능한 요청·queue와 실제 실행 조합의 조건·실패 전달을 다룬다. [DB transaction 검사](../../../apps/client/tests/shared/db/transaction-serialization.test.ts)와 [Local 보존 검사](../../../apps/client/tests/shared/services/auth/local-preservation.test.ts)는 실제 Drizzle SQL·Node 메모리 SQLite로 rollback·독립 upsert·원본 보존·종료 중 저장을 확인하는 기반이다. 실제 서버·native DB·Mapbox pack·기기 저장 공간의 성공은 이 증거로 확인되지 않는다. 당시 실행 대상은 [분리 검증 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-22-02-five-stage-commits-and-verification.md)에 남아 있다.

실행 진입·잠금, DB 공통 순서의 참여자, queue 상태·귀속·재시도, engine 결과·pull 검증·cursor, cleanup predicate·집계 또는 native 지도 삭제가 바뀌면 변경 책임자가 본문과 실제 consumer를 함께 갱신한다. 성공 표시를 바꾸는 작업은 completed의 상한부터, 삭제를 바꾸는 작업은 미전송 판정과 참조 원본부터 확인한다.
