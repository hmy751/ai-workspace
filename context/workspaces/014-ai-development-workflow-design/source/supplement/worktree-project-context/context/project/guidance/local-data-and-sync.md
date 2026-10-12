# 로컬 데이터·동기화·정리를 변경할 때

Trip·Schedule·Expense repository, Local 저장, sync queue·engine·cleanup을 추가·수정할 때 읽는다. 이 본문은 기존 Selective Activation Data Layer Guide의 개발 계약을 소유한다. 활성 여행과 데이터 보존의 제품 의미는 [여행 이용](../common/travel-access.md)과 [로컬 변경 보존](../common/local-data-preservation.md), 실제 적용 범위와 남은 간격은 [동기화와 정리의 현재 연결](../current/sync-and-cleanup.md)에 있다.

## 데이터 출처와 외부 서비스를 구별한다

활성화된 여행의 진실의 원천은 Local SQLite이며 로컬 변경을 `sync_queue`에 남긴다. 비활성 여행은 Server API를 사용한다. 활성화 판단의 원천은 `tripActivations`이고, 지금 읽고 쓸 출처는 Activation Router가 결정한다. Sync Engine은 이미 저장된 로컬 변경을 서버와 맞추는 별도 책임이다.

Map·Search·Directions는 사용자 소유의 sync 대상 Data Entity가 아니다. 외부 서비스 호출과 표시를 맡으며 `useAppPolicy`의 서비스 정책을 사용한다. 오프라인 지도·경로 다운로드가 활성화의 부가 작업이라고 해서 Data Router 안에 새 분기로 넣지 않는다. 활성화·다운로드 전체 절차는 [Activation system](../../../.claude/context/activation-system.md)이 계속 소유한다.

Data Entity의 기본 책임은 다음 구조로 찾는다.

```text
entities/{entity}/
├── model/       # @repo/schema에서 추론한 타입
├── api/         # Remote 요청·응답 경계
├── lib/         # Local SQLite 데이터 처리
├── repository/  # Activation Router에 출처 선택 요청
├── data/        # React Query key와 hook
├── ui/          # Entity UI
└── index.ts     # 공개 export
```

화면·feature·data hook이 Local DB와 Server API를 직접 선택하지 않는다. Data hook은 repository를 호출하고 repository가 Router에 Local·Remote 작업을 전달한다. 타입은 schema에서 `z.infer`로 추론하며 전송 검증은 [API 가이드](api-contracts.md)를 따른다.

## 대상 여행을 알고 있으면 그 ID로 먼저 출처를 고른다

**화면이 아는 `tripId`로 출처를 먼저 고른다.** Local row를 먼저 찾아 소속을 얻으면 이 기기에 없는 비활성 여행의 Remote 작업이 막힌다.

| 작업 | 라우팅에 쓰는 입력 |
| --- | --- |
| Schedule·Expense 조회·수정·삭제, 일정별 경비 조회 | 호출자가 전달한 tripId의 활성 여부 |
| Trip 단건 조회·수정·삭제 | 대상 Trip의 활성 여부 |
| Trip 목록·생성 | 현재 사용자의 활성 여행 존재 여부를 사용하는 전역 분기 |

화면·hook·repository·Router까지 ID를 이어 주고 실제 Local 실행에서 소유권을 확인한다. Router helper 이름만으로 모든 Trip 작업을 전역 분기로 묶지 않는다.

- Remote는 보호된 인증과 실제 online을 확인한다. Unknown이나 표시 override를 실제 연결로 쓰지 않는다.
- Override 중에는 Local·Remote mutation을 모두 거절한다.
- Router 상태 검사와 Local SQL의 계정·활성 대상 검사는 각각 필요하다. [인증 기준](authentication-and-session.md)을 따른다.

라우팅 성공은 endpoint 계약의 성공을 보장하지 않는다. 현재 Trip client PATCH/server PUT 차이는 [현재 구조](../current/architecture.md)와 API 변경에서 따로 확인한다.

## 로컬 변경과 queue INSERT는 하나의 저장 결과다

Local mutation은 entity 변경과 `sync_queue` 추가를 반드시 `withTransaction`으로 묶는다. Queue 저장에 실패하면 entity 변경도 취소되어야 한다. `addToSyncQueue`는 서버 전송이 아니라 같은 SQLite에 수행하는 INSERT이며, entity만 먼저 저장한 뒤 실패 시 별도 삭제하는 보상 작업으로 대체하지 않는다.

생성 ID는 클라이언트의 `generateId()`/ULID로 만들고 서버가 이 ID를 받아야 한다. `createdAt`, `updatedAt`, `version`, `deletedAt` 같은 sync 필드는 생성·변경 의미에 맞게 유지한다. 삭제는 soft delete로 변경 사실을 남기고 실제 제거는 cleanup의 안전 조건을 따른다. 시간은 공통 ISO datetime 계약을 사용하되 Expense `date` 등의 실제 계약 차이는 [날짜와 시각](../common/date-and-time.md)을 확인한다.

트랜잭션 API에 callback을 전달했다는 모양만으로 원자성을 판단하지 않는다. 실제 DB adapter가 async callback 종료를 기다린 뒤 COMMIT하고 실패 시 ROLLBACK하는지 확인한다. 현재 `runDatabaseTransaction`은 이 완료 시점을 직접 관리한다. Queue 실패 주입 시 entity와 queue가 모두 변경 전 상태인지 실제 SQL로 확인해야 한다.

## 같은 SQLite 연결의 독립 작업도 순서를 맞춘다

열린 transaction 안에 독립 pull upsert가 끼어들면, 성공을 반환한 upsert도 남의 rollback과 함께 사라질 수 있다. Transaction끼리만 직렬화해서는 부족하다.

| 진입 위치 | 실행 기준 | 이유 |
| --- | --- | --- |
| Transaction 밖의 sync·maintenance | `runDatabaseOperation`의 공통 순서 사용 | 독립 queue 조회·상태 변경·삭제, metadata, 서버 upsert, reset의 간섭 방지 |
| 이미 열린 transaction 안의 queue INSERT | 같은 transaction에서 직접 실행 | 바깥 큐에 다시 등록하면 자기 transaction 종료를 기다리는 교착 가능 |

호출자에게 반환한 원래 Promise는 실패를 전달한다. 다음 작업을 잇는 내부 Promise의 오류 처리는 큐 진행을 위한 것이며 원래 호출을 성공으로 바꾸지 않는다.

이 보장은 같은 프로세스에서 공통 경계를 거친 작업에 적용된다. 새 Local write·activation·지도·경로 저장은 실제 진입을 확인한다. 일부 경로 참여를 모든 DB 접근의 직렬화 완료로 확대하지 않는다.

**Reset은 삭제와 스키마 재생성을 함께 rollback해야 한다.** 시작할 때 ready를 해제하고 실패 뒤에도 `getDatabase()`가 준비된 DB를 제공하지 않게 한다. 데이터 rollback 이후 DB 재준비·화면 재시도는 별도로 확인한다. 삭제 없는 앱 시작 재시도 및 서버·SecureStore까지 포함한 전체 로그아웃 원자성과 구별한다.

## sync 요청과 실행 가능 여부를 한 경계에서 판단한다

Provider·수동 버튼·Debug 진입은 공통 `executeSync`를 호출해 실행 순간의 DB 준비, signed-in, 실제 online, override 해제와 세션 종료 여부를 확인한다. React 화면에서 가능해 보였다는 사실만으로 engine을 직접 실행하지 않는다.

표시용 `isSyncing`은 실행 잠금이 아니다. 같은 렌더에서 두 호출이 오래된 값을 볼 수 있으므로 engine·구독자 실행 전에 공통 실행 소유권을 확보한다. Provider remount와 React 밖 진입에도 같은 잠금을 적용한다.

동시 요청의 결과는 수명에 따라 다르다. Network refresh는 Promise를 공유하지만, 진행 중 sync에 새 요청이 오면 현재 계약은 `skipped`이며 다음 실행을 예약하지 않는다. 내부 active Promise는 종료 대기에도 사용되지만 모든 요청자에게 성공 대기를 공유한다는 뜻은 아니다.

자동 시작 effect는 실행 불가에서 가능으로 바뀐 조건을 소비한다. 로그인·같은 계정 인증 복구·실제 online·override 해제 등이 해당하며, 소비한 전환을 먼저 기록해 중복 실행을 막는다. 새 세션은 새 맥락이다. 일반 rerender, callback identity 변경, sync 완료 자체는 새 요청 이유가 아니다.

주기 sync는 opt-in이다. Timer 수명은 활성화 설정과 interval에 연결하고 네트워크 변화·sync 완료마다 timer를 다시 시작하지 않는다. 각 tick은 공통 실행 경계에서 최신 조건을 다시 확인한다. 세션 종료의 pause·대기 순서는 [인증 가이드](authentication-and-session.md)가 소유한다.

## queue의 실패와 순서를 지운 성공을 만들지 않는다

Queue는 서버 반영을 확인하지 못한 로컬 변경이다. 전송 직전 현재 계정과 각 task의 귀속을 확인하고, 다른 계정이거나 확인할 수 없으면 전송하지 않는다. 귀속 검사에 필요한 원본 row와 payload는 cleanup에서도 보존해야 한다.

현재 전송 선택은 `createdAt` FIFO 순서에서 `PENDING`과 `retryCount < 3`인 `FAILED`로 이루어진 앞부분이다. 재시도 한도 FAILED나 남은 IN_PROGRESS를 건너뛰어 뒤 변경을 먼저 보내지 않는다. 한 작업의 일반 실패는 FAILED와 증가한 retry count로 남기고 뒤 작업 진행을 멈춘다. 인증 실패는 작업을 PENDING으로 되돌리고 재인증 필요를 위로 전달한다.

첫 401의 자동 갱신·원요청 재전송, sync HTTP의 5xx 재시도와 저장된 queue를 다음 sync에서 고르는 재시도는 다른 수명이다. 정확한 HTTP 경계는 [API 가이드](api-contracts.md)에서 확인한다. 중단된 IN_PROGRESS의 앱 재시작 뒤 복구, 한도 도달 뒤 사용자 회복, 응답 유실로 가능한 중복 서버 반영의 처리 방식은 아직 추가 판단이 필요하다. 기존 retry helper가 있다는 이유로 이 제품 흐름이 완료됐다고 보지 않는다.

Engine은 push 뒤 pull을 진행하고 인증 중단이나 남은 FAILED/IN_PROGRESS를 실패로 전달해야 한다. 활성 여행이 없어 pull을 생략했다고 앞의 push 실패를 완료로 바꾸지 않는다. 호출자가 받는 `completed`, `skipped`, `failed`를 구별하고 skipped·failed에서 성공 안내나 성공 시각을 갱신하지 않는다.

`completed`의 범위를 과장하지 않는다. 현재 engine은 시작할 때 전송 목록을 읽고, 그 사이 생긴 새 PENDING까지 전부 비웠다고 보장하지 않는다. Cleanup 부분 실패, 캐시 재조회 완료, native 지도 정리도 별도 결과다. 이 경계를 변경할 때에는 반환 타입·성공 시각·UI 안내를 함께 검토한다.

## pull 저장과 삭제의 안전 조건을 이어 본다

Pull은 현재 계정의 활성 여행을 대상으로 요청하고 응답 row의 계정을 확인한 뒤 저장한다. 활성 대상이 없으면 pull을 생략하며 비활성 여행의 서버 데이터를 일반적인 로컬 캐시로 받아들이지 않는다. 요청한 tripId 집합의 검증, schema parse에서 Local 타입으로 전달되는 경계, 부분 저장 뒤 cursor 전진·충돌의 의미는 각각 확인해야 한다. 현재 구현의 계정 검사를 모든 응답의 shape·대상 검증 완료로 설명하지 않는다.

일반 조회는 soft-deleted 데이터를 감추지만 pull은 삭제 사실을 전달해야 한다. Upsert는 원래 생성 시각을 보존하고 서버 삭제 상태·version을 반영한다. Typed pull을 정리할 때 `as never[]`를 새 단언이나 조용한 기본값으로 옮겨 검증을 대신하지 않는다. 관련 현재 간격은 [동기화 현황](../current/sync-and-cleanup.md)에 남긴다.

비활성화는 사용 가능 상태 전환, soft delete는 로컬 표시 대상에서 제외, vacuum은 물리 제거라는 서로 다른 단계다. 미전송 변경이 있으면 정리를 보류하고 `cleanupPending`을 남기는 취지를 유지한다. 서버 반영 미확인에는 PENDING·IN_PROGRESS·FAILED가 모두 포함되지만 현재 여행별 cleanup predicate는 PENDING 중심인 간격이 있다. 전역 로그아웃 통계가 보완됐다는 이유로 여행별 cleanup도 완료됐다고 판단하지 않는다.

오래된 soft-deleted Schedule·Expense도 queue가 참조하면 vacuum에서 보존한다. 상태나 보존 기간만 보고 원본을 지우면 다음 복원·전송에서 소유자를 확인할 근거를 잃는다. Cleanup의 처리 개수는 실제로 정리한 수와 시도·보류한 수를 구별하고, 지도 metadata 삭제를 native pack 공간 회수로 표시하지 않는다.

## 가장 위험한 실패를 실제 경계에서 확인한다

| 변경 대상 | 실패·경계 사례 | 보존할 결과 |
| --- | --- | --- |
| 라우팅 | 다른 여행은 활성, 대상은 Local에 없는 비활성 여행 | 대상의 Remote 경로 실행 |
| Local 저장 | Queue INSERT 실패 | Entity·queue 함께 rollback |
| DB 공통 순서 | 실패 transaction 옆의 독립 upsert·queue 변경 | 다른 작업의 결과 보존 |
| Reset | 스키마 재생성 실패 | DB·queue rollback과 ready 해제. 화면의 재준비 경로는 별도 확인 |
| Sync | 동시 진입·조건 불충족·task 실패·인증 만료 | skipped/실패 구분, 뒤 task 중단, 거짓 성공 안내 방지 |
| Vacuum | Queue가 오래된 삭제 원본을 참조 | 참조 원본 보존 |

실제 Drizzle·Node SQLite 검사는 SQL·rollback·간섭의 근거다. Expo native SQLite 전체와 동일하지 않으며 mock API도 서버 중복 반영·토큰 회전·응답 유실을 입증하지 않는다.

직접 근거: [Router](../../../apps/client/src/shared/services/offline-prep/router.ts), [DB 실행](../../../apps/client/src/shared/db/index.ts)·[저장/upsert](../../../apps/client/src/shared/db/utils.ts), [sync lifecycle](../../../apps/client/src/shared/services/sync/lifecycle.ts)·[Provider](../../../apps/client/src/shared/services/sync/provider.tsx)·[queue](../../../apps/client/src/shared/services/sync/queue.ts)·[engine](../../../apps/client/src/shared/services/sync/engine.ts), [cleanup](../../../apps/client/src/shared/services/sync/cleanup-job.ts).

2026-09-25 코드와 기존 Selective Activation Owner·[단계별 구현 근거](../../work/workspaces/002-code-readability-refactoring/records/2026-09-22-02-five-stage-commits-and-verification.md)를 대조했다. 전체 Local write·typed pull·여행별 cleanup의 남은 차이는 [현황](../current/sync-and-cleanup.md)에서 확인한다.
