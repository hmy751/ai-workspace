보존된 구현 결과를 확인했습니다. [useStorageStats.ts](/private/tmp/0402-storage-fullread-20261022/r14/result/useStorageStats.ts)에서는 DB·지도 용량을 표시 문자열로 바꾸는 `createStorageStats`를 같은 파일에 두고, 조회의 성공·실패 모두 `finally`에서 한 번만 `setStats`를 호출합니다. 초기 `0 B` 값도 같은 함수로 만듭니다. 이전에는 성공 경로와 바깥 `catch`에서 세 필드를 각각 조립했는데, 이제 표시 형식을 고칠 곳이 한 군데입니다. DB 조회 실패 시 지도 조회를 시작하지 않는 흐름과 개별 지도 팩 실패 시 다음 팩으로 진행하는 흐름은 그대로 읽힙니다.

보존된 검사 출력에서는 Jest 2개 suite의 7개 테스트가 통과했습니다. 여기에는 변경 전에 작성한 저장 용량 hook 시나리오 6개가 포함됩니다. 변경 파일 대상 ESLint, Prettier, diff 공백 검사도 통과했습니다. 이 결과는 mock으로 제어한 hook 동작의 보존 근거이며, 실제 기기의 Expo 파일 경로나 Mapbox 연결을 확인한 결과는 아닙니다.

client 전체 TypeScript 검사는 **통과하지 않았습니다**. 프로젝트 검사와 에디터 TypeScript 진단 모두 기존 제품 코드의 오류 3개를 보고했습니다: `mapbox.ts`의 좌표 tuple 타입 1개, `offline-map/download.ts`의 `OfflinePack.size`·`tileCount` 접근 2개입니다. 이번 저장 용량 변경 파일이나 테스트 파일의 새 진단은 제공된 출력에 없습니다. 이전에 에디터 오류와 CLI 결과를 혼동했던 만큼, 여기서는 두 검사의 범위를 구분해 보고합니다.

이 자료만으로는 실제 앱 실행, 전체 lint, 사용자 에디터 화면에서의 표시 변화, 커밋 여부를 확인할 수 없습니다. 따라서 현재 확인 가능한 결론은 **중복된 stats 조립을 한 곳으로 줄였고, 제공된 hook 테스트가 변경 후에도 통과했다**는 범위까지입니다.
