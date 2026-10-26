`access`는 없어진 게 아니라 **조합 훅 내부로 들어갔고, 반환값에서는 빠졌습니다.** 제가 앞서 합의한 `{ query, access, view }`를 `{ query, actions, view }`로 설명하면서 이 변경을 짚지 않았습니다.

현재 일정 조회의 연결은 이렇습니다.

```ts
const access = useTripReadAccess(tripId, 'schedule', options);
const query = useGetSchedules(tripId ?? '', { enabled: access.enabled });
return useReadQuery(query, access);
```

`useReadQuery`는 `access`로 표시 결과를 계산하고, 재조회 직전 차단 여부를 확인합니다. 바깥에는 `actions.canRefetch`로 조회 가능 여부를, `view.kind === 'blocked'`일 때 `view.policy`로 제한 이유를 내보냅니다. 그래서 일정 화면은 지금 `access`를 직접 받지 않습니다.

하지만 **`actions`는 `access`의 대체물이 아닙니다.** `access`에는 표시 정책과 실제 네트워크 기준 정책, 조회를 잠시 꺼 둔 상태까지 들어 있습니다. 폼의 보조 조회처럼 그 구별이 필요한 사용처까지 고려한다면, 이를 숨기는 결정을 자동으로 해서는 안 됩니다. 제가 제안했던 계약대로 `{ query, access, actions, view }`를 반환하고, 정책을 고려한 실행만 `actions.refetch`로 열어 두는 편이 일관됩니다. 이번 한 곳 적용에서는 `access`가 내부에서만 쓰이고 있다는 것이 현재 구현의 정확한 상태입니다.
