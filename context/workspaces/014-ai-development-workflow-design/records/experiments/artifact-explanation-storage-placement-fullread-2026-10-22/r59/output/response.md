제공된 변경 결과 기준으로, `useStorageStats`의 중복된 통계 조립을 한곳으로 모았습니다. [변경된 hook](/private/tmp/0402-storage-fullread-20261022/r59/result/useStorageStats.ts)에서는 초기 `0 B` 값과 조회 후 결과를 `createStorageStats`로 만들고, 성공·실패 경로에 각각 있던 `setStats`를 `finally` 한 곳에서 호출합니다. DB 파일 조회와 Mapbox 팩 조회의 순서, 개별 팩 실패 시 다음 팩을 계속 처리하는 분기는 그대로입니다. 따라서 DB 파일 조회 중 실패하면 그때까지의 DB 합계를 표시하고 Mapbox 조회를 시작하지 않는 흐름도 코드상 유지됩니다.

가독성 측면에서는 `dbSize`·`mapPackSize`·`totalSize`를 함께 수정할 위치가 둘에서 하나로 줄었습니다. 표시 형식 함수도 hook 밖으로 옮겨졌지만 계산식은 바뀌지 않았습니다. 별도 파일이나 adapter는 늘지 않아, 부분 결과와 중단·계속 조건은 같은 hook에서 읽을 수 있습니다. [변경 전후 diff](/private/tmp/0402-storage-fullread-20261022/r59/result/change.diff)

[보존된 검사 결과](/private/tmp/0402-storage-fullread-20261022/r59/result/checks-2513.txt)에서는 기존 hook 특성화 테스트를 포함한 Jest 2개 suite, 7개 test가 모두 통과했습니다. 변경 파일 대상 ESLint, Prettier, diff 공백 검사도 통과했습니다. 반면 [client 전체 타입 검사](/private/tmp/0402-storage-fullread-20261022/r59/result/checks-2523.txt)는 실패했습니다. 오류는 `mapbox.ts`의 tuple 타입 1건과 `download.ts`의 `OfflinePack.size`·`tileCount` 접근 2건으로, 앞선 대화에서 확인된 동일한 제품 source 오류입니다. 보존된 출력에는 이번 hook이나 테스트 파일의 새 타입 오류가 나타나지 않습니다.

이 근거는 mock으로 제어한 hook 동작과 대상 정적 검사까지입니다. 실제 기기의 Expo 파일 경로·Mapbox native 팩 동작, 에디터 화면의 현재 진단, 커밋 여부는 제공된 결과에서 확인되지 않았습니다.
