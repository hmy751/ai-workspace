# 저장 용량 집계의 현재 동작 경계

프로필의 SQLite·오프라인 지도 저장 용량 계산, 표시나 refresh 상태 연결을 수정할 때 읽는다. 이 본문은 2026-09-14 현재 [useStorageStats](../../../apps/client/src/features/profile/hooks/useStorageStats.ts)의 부분 결과·실패·비동기 적용 관계를 소유한다. 모든 hook이나 native 조회의 공통 정책으로 확대하지 않는다.

## 집계와 표시

[useStorageStats](../../../apps/client/src/features/profile/hooks/useStorageStats.ts)는 **SQLite 집계 뒤 Mapbox 집계**를 진행한다. 실패에 따라 중단하거나 부분 합계를 남기는 순서다.

| 대상 | 집계하는 값 |
| --- | --- |
| SQLite | `.db`, `.db-wal`, `.db-shm` 파일 byte |
| Mapbox | Offline pack별 `completedResourceSize` |
| 공통 | 음수·NaN·무한대 등 유효하지 않은 byte는 제외 |

표시는 1,024 단위의 B·KB·MB·GB·TB로 소수 한 자리까지 정리한다. Hook은 dbSize·mapPackSize·totalSize 문자열을 반환하지만 [ProfileScreen](../../../apps/client/src/screens/ProfileScreen.tsx)은 앞의 두 값만 표시한다. `totalSize`를 추가로 표시하거나 반환 필드를 제거할 때는 consumer와 hook 검사를 함께 맞춘다.

## 실패 위치가 남길 결과를 결정한다

| 관찰한 상황 | DB 결과 | Mapbox 진행·결과 |
| --- | --- | --- |
| Document directory 사용 불가 또는 SQLite 파일 조회 중 실패 | 그때까지 모은 byte 보존 | 시작하지 않음 |
| SQLite directory 없음 | 정상 완료한 0 | 조회 계속 |
| Mapbox getPacks 실패 | DB 합계 보존 | 지도 합계 0 |
| 개별 pack status 실패 | DB 합계 보존 | 해당 pack만 건너뛰고 다음 pack 합산 |

이 결과를 하나의 catch나 무조건 병렬 조회로 바꾸면 중단 위치와 부분 합계가 달라진다. 리팩터링에서는 성공 합계뿐 아니라 **어디서 멈추고 무엇을 남기는지**를 보존한다. 실패로 표시된 0을 실제 저장 공간이 없다는 측정 결과로 해석하지 않는다.

## React 상태와 검증 상한

- 초기 mount와 공개 refresh가 계산을 시작한다.
- Refresh가 겹치면 가장 최근 요청의 결과만 state에 반영한다.
- Unmount 뒤 도착한 native 결과는 state를 갱신하지 않는다.

병렬 조회·공개 실패 상태·새 단위 체계는 현재 계약에 포함되지 않는다.

[Hook test](../../../apps/client/tests/features/profile/hooks/useStorageStats.test.ts)는 FileSystem·Mapbox를 대체하고 실제 hook에서 파일 선별·표시·부분 실패·유효하지 않은 byte·겹친 요청을 확인한다. Expo 경로·native pack·development build·실기기 연결은 입증하지 않는다. Native API shape, 집계 순서, 반환 필드, Profile consumer, 최신 요청 적용 방식이 바뀌면 이 경계를 다시 확인한다.

작성 근거는 [Ticket 03](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/03-storage-stats.md), [리팩터링 실행 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-11-04-storage-stats-refactor.md), [최초 범위 재확인](../../work/workspaces/002-code-readability-refactoring/records/2026-09-12-01-ticket-03-initial-scope-reanalysis.md)이다. 당시 helper 추출만 한 최소안은 내부 I/O·실패·React 책임을 남겨 후속 개선으로 확대됐다. 2026-10-01 편집에서는 두 기록과 현재 브랜치 hook을 대조했으며 제품 검사를 재실행하지 않았다.
