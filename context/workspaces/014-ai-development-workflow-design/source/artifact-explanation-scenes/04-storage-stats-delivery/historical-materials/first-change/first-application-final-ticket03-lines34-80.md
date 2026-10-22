동작 보존과 별도로 성공·실패 표시 조립을 함께 수정할 위치가 줄었는지, 부분 결과와 실패 정책을 가까운 코드에서 이해할 수 있는지 변경 전후를 비교한다.

## 현재 상태와 실제 결과

2026-09-11에 client 소유 테스트 환경과 최소 React hook smoke test를 구성했다. 이어서 `apps/client/tests/features/profile/hooks/useStorageStats.test.ts`에 변경 전 특성화 테스트 6개를 작성해 빈 입력·대상 파일 선별과 단위 표시·DB 중간 실패·`getPacks` 실패·개별 pack 실패 후 계속·`refresh` 재계산을 현재 구현에서 확인했다.

제품 코드에서는 byte 표시 변환을 hook 밖의 `formatBytes`로 옮기고, DB·지도·합계 표시값 조립을 같은 파일의 `createStorageStats` 한 곳으로 모았다. 비동기 계산은 성공과 바깥 실패에서 각각 stats를 조립하던 대신 `finally`에서 한 번 조립한다. DB 파일 조회 중간 실패 시 Mapbox 조회를 시작하지 않는 조건, `getPacks` 실패 시 DB 부분 결과 보존, 개별 pack 실패 후 다음 pack 계속이라는 기존 정책과 실행 순서는 바꾸지 않았다. 별도 파일이나 adapter는 추가하지 않았다.

변경 후 전체 client Jest 2 suites·7 tests, hook·특성화 테스트 대상 ESLint, 해당 파일 Prettier와 `git diff --check`가 통과했다. 프로젝트 TypeScript 5.3.3과 에디터 TypeScript 6.0.3 모두 새 테스트와 변경한 hook에서는 진단을 내지 않는다. 단일 client config의 전체 `test:typecheck`는 이번 변경 밖의 기존 client source 오류 3개(`src/shared/lib/mapbox.ts` 1개, `src/shared/services/offline-map/download.ts` 2개) 때문에 실패한다. client 기본 lint는 기존 `eslint-plugin-prettier`와 Prettier 3의 호환 문제로 전체 통과를 확인하지 못했으며, development build와 실제 기기·native module 연결도 미확인이다. 설정 결과와 검증 범위는 [테스트 환경 구축 기록](../../../records/2026-09-11-03-storage-stats-test-setup.md)에 보존한다.
