이 파일은 **휴대폰의 네트워크 관측값(NetInfo)을 앱에서 쓰는 상태로 바꾸고, 관측을 시작·재확인·정리하는 Store**입니다. 흐름은 `init() → listener의 관측값 반영 → 필요하면 refresh() → cleanup()` 순서로 보면 됩니다. 화면에 강제로 보여 주는 상태는 실제 관측과 따로 보관합니다.

먼저 상태 네 가지를 구별하면 뒤의 코드가 쉬워집니다.

| 값 | 뜻 |
| --- | --- |
| `realStatus` | 실제 관측으로 판단한 `online`·`offline`·`unknown` |
| `checkStatus` | 실제 상태가 `unknown`일 때 안내할 말: 확인 중(`checking`) 또는 확인 불가(`unavailable`). 상태가 확정되면 `idle` |
| `isRefreshing` | 사용자가 요청한 재확인을 기다리는 중인지 |
| `overrideStatus` | 디버그 화면용 강제 표시값. 실제 연결 상태를 바꾸지 않음 |

### 1. 관측값을 세 상태로 바꿉니다

```ts
export function resolveNetworkStatus(state: Pick<NetInfoState, 'isConnected' | 'isInternetReachable'>): NetworkStatus {
  if (state.isConnected === false || state.isInternetReachable === false) {
    return 'offline';
  }

  if (state.isConnected === true && state.isInternetReachable === true) {
    return 'online';
  }

  return 'unknown';
}
```

`isConnected`는 기기가 네트워크에 연결됐는지, `isInternetReachable`은 인터넷에 닿는지를 나타냅니다. **하나라도 명시적으로 `false`이면 offline**, 둘 다 `true`여야 online입니다. 예를 들어 `true / null`은 인터넷 도달 여부가 아직 불확실하므로 unknown입니다. `null`을 offline이나 online으로 추측하지 않는 것이 이 파일의 출발점입니다.

### 2. `init()`이 이번 관측 세션을 만듭니다

```ts
function init() {
  if (currentSession) {
    return;
  }

  const session: NetworkSession = {
    unsubscribe: null,
    noticeTimer: null,
    observationVersion: 0,
    refreshRequest: null,
  };

  currentSession = session;
  beginUnknownCheck(session);
  subscribe(session);
}
```

`currentSession`은 지금 유효한 listener, 타이머, 재확인 요청을 묶어 둡니다. 이미 세션이 있으면 `init()`을 다시 불러도 listener를 또 만들지 않습니다. 앱의 Root가 `networkStore.init()`을 호출하면 먼저 unknown 안내 타이머를 걸고 `NetInfo.addEventListener`로 관측을 시작합니다. 등록 자체가 첫 상태를 조회하므로 여기서 별도의 `NetInfo.fetch()`는 하지 않습니다.

listener가 값을 받으면 `observationVersion`을 올리고 `applyObservation()`에 전달합니다. 관측 결과가 이전 `realStatus`와 같으면 그대로 둡니다. **새로 unknown이 된 경우에만** 10초 안내를 다시 시작하므로, unknown 관측이 반복돼도 타이머가 계속 밀리지 않습니다.

```ts
function applyObservation(session: NetworkSession, state: NetInfoState) {
  if (currentSession !== session) {
    return;
  }

  const status = resolveNetworkStatus(state);

  if (status === get().realStatus) {
    return;
  }

  if (status === 'unknown') {
    beginUnknownCheck(session);
  } else {
    clearNoticeTimer(session);
    set({ realStatus: status, checkStatus: 'idle' });
  }
}
```

`beginUnknownCheck()`는 `realStatus: 'unknown'`, `checkStatus: 'checking'`으로 두고 10초 뒤 `markUnavailable()`을 예약합니다. 그때까지 확정 관측이 없으면 **`checkStatus`만 `unavailable`로 바뀝니다. `realStatus`는 여전히 unknown**입니다. 반대로 online/offline 관측이 오면 타이머를 지우고 `checkStatus`를 `idle`로 돌립니다. 즉, 10초는 연결 실패 판정 시간이 아니라 안내 문구가 바뀌는 시간입니다.

### 3. `refresh()`는 수동으로 한 번 더 확인합니다

`refresh()`는 우선 `init()`으로 구독을 확보하고, 진행 중인 `refreshRequest`가 있으면 **그 요청의 Promise를 그대로 반환**합니다. 연달아 눌러도 새 `NetInfo.refresh()`를 여러 번 시작하지 않는 이유입니다. 현재 상태가 unknown이면 확인 안내의 10초 타이머를 새로 시작하고, listener 등록이 실패해 있었다면 등록도 다시 시도합니다. 등록할 수 있으면 새 요청을 보관한 뒤 `NetInfo.refresh()`를 호출하고 `isRefreshing`을 true로 둡니다.

이 요청의 결과를 그대로 적용하지는 않습니다. 기다리는 동안 listener가 더 최신 상태를 알려 줄 수 있기 때문입니다.

```ts
function canApplyResult() {
  return (
    currentSession === session &&
    session.refreshRequest === request &&
    session.observationVersion === startingObservationVersion
  );
}

// request의 일부
accept: (state) => {
  if (canApplyResult()) {
    applyObservation(session, state);
  }

  finish();
},
fail: () => {
  if (canApplyResult()) {
    markUnavailable(session);
  }

  finish();
},
```

여기서 세 비교는 각각 다른 늦은 응답을 막습니다. `currentSession === session`은 cleanup 뒤 옛 세션의 결과를, `refreshRequest === request`는 끝난 요청의 뒤늦은 결과를, `observationVersion` 비교는 재확인 도중 listener가 이미 전한 새 관측을 옛 refresh 결과가 덮는 일을 막습니다. `finish()`는 요청 보관을 해제하고 `isRefreshing`을 false로 바꾸며 기다리던 Promise를 끝냅니다. refresh 실패나 10초 무응답도 이 대기를 끝내지만, **refresh가 끝났다는 것 자체가 online 확인 성공을 뜻하지는 않습니다.** 이후 listener 관측은 계속 받을 수 있습니다.

예를 들어 `unknown → 수동 재확인 시작 → listener가 online을 알림 → refresh가 늦게 offline을 반환`했다면, listener가 `observationVersion`을 올렸으므로 늦은 offline 결과는 적용하지 않습니다. `realStatus`는 online으로 남습니다. 이는 코드가 보호하려는 상황을 따라가 본 예시입니다.

### 4. 화면 표시와 실제 판단은 다른 값을 읽습니다

```ts
export function useDisplayNetworkStatus(): NetworkStatus {
  return useNetworkStore((state) => state.overrideStatus ?? state.realStatus);
}

export function useRealNetworkStatus(): NetworkStatus {
  return useNetworkStore((state) => state.realStatus);
}
```

`useDisplayNetworkStatus()`는 override가 있으면 그것을 보여 줍니다. `useRealNetworkStatus()`와 `networkStore.realStatus`는 실제 관측값만 읽습니다. 따라서 실제가 unknown인데 디버그에서 online으로 강제해도, 그 표시가 실제 연결 확인 결과가 되지는 않습니다. `useNetworkCheck()`는 확인 안내와 재확인 버튼에 필요한 `checkStatus`, `isRefreshing`, `refresh`를 묶어 제공합니다.

마지막으로 `cleanup()`은 현재 세션을 먼저 무효화한 뒤 타이머·진행 중 재확인·listener를 정리하고 실제 상태를 초기값(`unknown`/`checking`)으로 돌립니다. 그래서 정리 전 listener나 refresh 결과가 뒤늦게 와도 새 세션에 반영되지 않습니다. 이 초기화에는 `overrideStatus`가 포함되지 않으므로 강제 표시값은 그대로 남습니다.

한 줄로 묶으면, **listener가 실제 상태를 계속 갱신하고, 타이머는 unknown 안내만 바꾸며, refresh는 같은 세션에서 추가 확인을 요청하고, 세션·버전 검사가 늦은 결과를 걸러냅니다.**
