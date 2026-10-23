`useStorageStats`의 중복된 표시값 조립을 한곳으로 모은 변경 결과를 확인했습니다. 성공했을 때와 전체 조회가 실패했을 때 모두 `createStorageStats(dbSizeBytes, mapSizeBytes)`를 사용하고, `finally`에서 현재까지 집계한 값을 한 번 반영합니다. 초기 `0 B` 상태도 같은 함수로 만듭니다. 변경은 [useStorageStats.ts](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/features/profile/hooks/useStorageStats.ts)에 한정됩니다.

DB 파일 조회 중 실패하면 앞서 합산한 DB 용량을 남기고 Mapbox 조회를 시작하지 않습니다. `getPacks()` 실패 시에는 DB 값이 남으며, 개별 `pack.status()` 실패 시에는 다음 팩을 계속 집계합니다. 이 실패 처리와 1,024 기준 표시 형식은 변경된 코드에서 유지됩니다.

보존된 검사 결과에서는 Jest 2개 suite의 7개 테스트, 대상 ESLint, Prettier, diff 공백 검사가 통과했습니다. 전체 client TypeScript 검사는 기존에 확인된 다른 파일의 오류 3개(`mapbox.ts` 1개, `download.ts` 2개)로 실패했고, 저장된 에디터 TypeScript 진단에도 같은 3개만 남았습니다. 따라서 이 변경으로 전체 타입 검사가 통과했다고 말할 수는 없습니다. 실제 기기의 FileSystem·Mapbox 동작은 이 mock 기반 테스트로 확인되지 않았습니다.
