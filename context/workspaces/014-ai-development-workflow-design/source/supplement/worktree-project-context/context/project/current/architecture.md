# 현재 구현과 검증 경계

작업 범위와 영향을 받을 책임, 필요한 검증 경계를 정할 때 읽는다. Package·Harness 개관은 2026-09-14의 대조를 바탕으로 하며, 아래 앱 준비·라우팅·client 검증 연결은 2026-09-25에 제품 기준 `759cba3`과 현재 작업 트리를 다시 대조했다. 활성 상태 최초 확인의 미커밋 변경은 [네트워크와 화면 접근](network-and-screen-access.md)에서 별도로 설명한다. 이 지도는 코드·문서·검사 본문의 관계를 설명하며 앱 전체 동작을 재실행한 증거는 아니다.

## 구성과 흐름

| 구성 | 현재 책임 |
| --- | --- |
| [Client](../../../apps/client/CLAUDE.md) | React Native·Expo 화면, FSD entity/data/repository, SQLite·활성화·정책 UI |
| [Server](../../../apps/server/CLAUDE.md) | Express route·인증·user scope, PostgreSQL/Drizzle·sync endpoint |
| [Schema](../../../packages/schema/CLAUDE.md) | Zod entity·request·response·sync 계약 |
| [UI](../../../packages/ui/CLAUDE.md) | Domain logic과 분리한 공유 primitive |

pnpm workspace가 package별 개발·검증 명령을 연결한다.

### 앱 진입

[AppInitialization](../../../apps/client/src/application/AppInitialization.tsx)은 mount 동안 네트워크 감지를 유지하며 DB 준비 뒤 인증 복원 시도를 기다린다.

- DB 실패: 삭제 없는 재시도 화면.
- 인증 복원 실패: 앱 구성을 연결하고 로그인 화면에서 복구.
- 준비 종료: [Root](../../../apps/client/app/_layout.tsx)의 Provider·Navigation 진입. Local 세션이 있으면 여행 선택·지도 만료 정리·pending cleanup 연결.

준비 완료가 네트워크·서버 인증·sync 성공을 뜻하지 않으며 후속 작업 완료도 화면 진입을 기다리게 하지 않는다. 변경 기준은 [앱 준비](../guidance/app-startup.md), 인증 뒤 실제 보호 범위는 [세션 현황](session-and-local-data.md)에서 확인한다.

### 데이터 접근과 후속 작업

Trip·Schedule·Expense의 data hook은 repository를 호출하고 Activation Router가 Local/Remote 구현을 고른다. [TripRepository](../../../apps/client/src/entities/trip/repository/trip-repository.ts)의 목록·생성은 전역 활성 여행 존재 여부를 사용하지만, 단건 조회·수정·삭제는 대상 여행의 활성 여부를 사용한다. Schedule·Expense의 수정·삭제와 일정별 경비 조회도 caller의 `tripId`로 먼저 분기하므로 비활성 자식의 Local row가 없어도 Remote 경로에 도달할 수 있다. 이 차이와 소유권·원자적 저장의 변경 기준은 [로컬 데이터와 sync 가이드](../guidance/local-data-and-sync.md)가 소유한다.

라우팅 경로가 열린 것과 해당 API가 끝까지 성공하는 것은 구별한다. 현재 Trip Remote 단건 조회는 서버 목록에서 ID를 찾고, 수정은 [client의 PATCH](../../../apps/client/src/entities/trip/api/trips.ts)와 [server의 PUT](../../../apps/server/src/routes/trips.ts)이 맞지 않는다. 대상 여행별 Router 보완만으로 온라인 Trip 수정 전체가 검증됐다고 볼 수 없다.

활성 여행의 Local mutation과 queue 기록은 DB 실행 경계를 사용하고, Sync Engine은 queue 전송과 활성 여행의 서버 변경 반영을 맡는다. Provider의 시작 요청·공통 실행 잠금·engine 결과·여행별 cleanup의 실제 연결과 남은 차이는 [sync와 정리](sync-and-cleanup.md)에서 읽는다. 지도·검색·길찾기는 Data Router의 소유권·동기화 대상이 아니며 [네트워크·Policy 가이드](../guidance/network-and-policy.md)에 따라 소비한다. 화면 정책이 실제 요청 제한과 어디까지 연결됐는지는 [네트워크와 화면 접근](network-and-screen-access.md)이 설명한다.

## 지원 경계와 확인 방법

제품 문서는 iOS 중심 배포, 활성 여행의 오프라인 핵심 입력, 온라인 보강과 통화별 관리를 설명한다. Android 동등 지원, 외부 공급자·운영 DB 상태, 실제 네트워크 전환·동시 sync의 성공은 이 지도에 사용한 source 대조만으로 확인되지 않는다. 기능별 현재 여부는 해당 source와 실제 환경에서 다시 판정한다.

제품 변경은 해당 app/package guide에서 영향에 맞는 검증을 선택한다.

| 근거 | 확인하는 경계 | 넘어설 수 없는 한계 |
| --- | --- | --- |
| Client Jest | Hook·API fixture, Root, 인증 Store/interceptor·동시성, 화면·Drawer render | Mock 기반 검사로 native·외부 서비스를 입증하지 않음 |
| [DB transaction](../../../apps/client/tests/shared/db/transaction-serialization.test.ts)·[Local 보존](../../../apps/client/tests/shared/services/auth/local-preservation.test.ts) 검사 | Node 메모리 SQLite에 Expo API를 연결해 실제 Drizzle SQL의 rollback·독립 upsert·queue 원본 보존 확인 | Native adapter·파일·기기 동시성은 미확인 |
| Server Vitest·Supertest | 단위 변환과 route 계약 | DB/auth mock은 실제 PostgreSQL·JWT와 다름 |
| Server PostgreSQL integration | 격리된 실제 DB query | 별도로 대체한 인증·배포 경계는 미확인 |
| Schema build·server typecheck/build | Package 수준 정적·빌드 확인 | iOS 실기기·외부 서비스 acceptance를 대신하지 않음 |
| Harness 검사 | 지침 bridge·링크·surface·공백, 임시 fixture의 Recover/Maintain/Verify | 여행 기능의 동작 검사가 아님 |

이 기반의 존재가 client/server 전체 검사 완료를 뜻하지 않는다. [리팩터링](../guidance/behavior-preserving-refactoring.md)·[API 가이드](../guidance/api-contracts.md)에서 변경별 확인을 고르고, 인증·sync·화면의 과거 실행 범위는 [분리 검증 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-22-02-five-stage-commits-and-verification.md)과 대조한다. 문서 편집으로 새 테스트 통과·사용자 수락을 추가하지 않는다.

Root [Context Harness](../../README.md)는 Project layer와 Workspace Spec·Ticket·state를 연결한다. Noline의 `.claude/skills/` 원본은 `.agents/skills/` bridge로 공유한다. Codex·Claude lifecycle wrapper가 설치돼 있지만 새 session은 unbound이며 hook trust·사용자 explicit activation·실제 event receipt 전에는 `activation_pending`이다. Claude adapter의 semantic runner는 기존 Codex 구현을 재사용한다.

준비·Provider 구성, repository 분기, DB 실행 참여자, 검증 adapter나 Harness runtime이 바뀌면 변경 책임자가 관련 부분을 갱신한다. 제품 의미·개발 계약의 현재 Owner는 [Project README](../README.md)에서 확인하며, 코드는 실제 적용 여부를 대조하는 근거다. 이 지도만으로 다른 상세 문서의 최신화나 제품 전체 지원을 주장하지 않는다.
