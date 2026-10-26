`useStorageStats`의 중복된 표시값 조립을 한곳으로 모았습니다. 이전에는 정상 종료와 바깥 `catch`에서 `dbSize`·`mapPackSize`·`totalSize`를 각각 같은 방식으로 만들었습니다. 이제 `createStorageStats(dbSizeBytes, mapSizeBytes)`가 세 값을 만들고, 조회가 끝나면 한 번만 상태에 반영합니다. 초기 `0 B` 상태도 같은 함수를 사용합니다.

```ts
} catch (error) {
  console.warn('Failed to calculate storage stats:', error);
} finally {
  setStats(createStorageStats(dbSizeBytes, mapSizeBytes));
}
```

`finally`는 정상 종료와 바깥 오류 모두에서 실행됩니다. 따라서 DB 파일 조회가 중간에 실패하면 그때까지의 DB 합계를 표시하고 Mapbox 조회는 시작하지 않습니다. `getPacks()`가 실패하면 DB 합계가 남고, 개별 팩의 `status()`가 실패하면 기존 안쪽 `catch`가 다음 팩 조회를 계속합니다. 이 실패 정책과 1,024 기준 표시 규칙은 건드리지 않았습니다. 앞으로 표시 필드를 바꿀 때 함께 고칠 조립 위치는 두 곳에서 한 곳으로 줄었고, 중단·계속 조건은 같은 hook 안에서 보입니다.

당시 검사에서 기존 hook 특성화 테스트와 설정 테스트 **2 suites, 7 tests가 통과**했습니다. Prettier 검사도 통과했습니다. 다만 client 전체 `test:typecheck`는 실패했습니다. 진단은 `mapbox.ts`의 tuple 타입 1건과 `download.ts`의 `OfflinePack.size`·`tileCount` 사용 2건으로, 이번 변경 파일에서는 나오지 않았습니다. 따라서 전체 타입 검사가 통과했다고 보지는 않습니다. 실제 Expo 파일 경로와 Mapbox native pack의 기기 동작도 이번 mock 테스트로 확인한 범위는 아닙니다.
