`access`는 **훅 내부에 남아 있지만 반환값에서 빠졌습니다.** 현재 `useSchedulesRead`는 `useTripReadAccess`로 `access`를 만든 뒤 Query의 `enabled`와 `useReadQuery`에 전달합니다. 그런데 `useReadQuery`가 화면에 돌려주는 값은 `{ query, actions, view }`뿐입니다.

```tsx
const access = useTripReadAccess(tripId, 'schedule', options);
const query = useGetSchedules(tripId ?? '', { enabled: access.enabled });
return useReadQuery(query, access); // 현재 반환: { query, actions, view }
```

일정 목록에서는 `view`로 표시 상태를, `actions.canRefetch`로 재조회 버튼을 결정하므로 당장 필요한 동작은 이어집니다. 하지만 제가 앞서 말한 **`{ query, access, view }` 계약을 유지한 것은 아닙니다.** `access`를 빼겠다는 설계 결정을 설명하지도 않았습니다. 이 부분은 제 설명과 현재 구현의 불일치입니다.

특히 확장성을 염두에 두면 차이가 있습니다. 캐시가 있어 `view`가 `ready`여도 실제 조회 정책은 막혀 `actions.canRefetch`가 `false`일 수 있습니다. 지금 반환값만으로는 폼의 특정 입력 영역이 *왜* 조회할 수 없는지 미리 안내하기 어렵습니다. `actions.refetch()`의 차단 결과는 눌러 본 뒤에야 알 수 있습니다.

따라서 이번 한 화면 적용에서는 `query`·`actions`·`view`에 **`access`도 반환하는 쪽**을 권합니다. `view`는 무엇을 보여줄지, `actions`는 허용된 재조회를, `access`는 표시·실제 조회 조건과 제한 이유를 필요한 소비자가 읽게 합니다. 일정 목록이 이를 모두 사용할 필요는 없습니다. 이후 폼 적용을 검토하면서 공개할 `access` 필드를 줄일지는 실제 사용처를 보고 정하면 됩니다. 현재는 일정 목록 한 곳만 적용된 상태이므로, 폼에서도 충분하다는 검증까지 끝난 것은 아닙니다.
