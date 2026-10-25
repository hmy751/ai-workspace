## 03-A

이 파일은 **NetInfo의 관측값을 앱이 사용할 네트워크 상태로 바꾸고, 그 상태를 계속 갱신하는 Store**입니다. 흐름을 한 줄로 잡으면 `init()`으로 관측을 시작하고 → NetInfo 이벤트가 올 때마다 상태를 바꾸고 → 필요하면 `refresh()`로 다시 확인하고 → 앱이 끝날 때 `cleanup()`으로 구독과 대기를 정리합니다.

### 1. 먼저 어떤 값을 보관하는가

`realStatus`는 실제 관측 결과입니다. `online`, `offline`, `unknown` 중 하나입니다. `resolveNetworkStatus()`가 NetInfo의 두 값으로 결정합니다.

| `isConnected` / `isInternetReachable` | 결과 | 뜻 |
|---|---|---|
| 둘 다 `true` | `online` | 인터넷 연결을 확인함 |
| 하나라도 `false` | `offline` | 연결 실패가 명시됨 |
| 나머지, 예를 들어 `true` / `null` | `unknown` | 아직 단정할 수 없음 |

`unknown`은 `offline`이 아닙니다. 이 구별 때문에 연결 확인이 늦어져도 서버 요청에 필요한 `online`을 추측하지 않고, 동시에 사용자에게 “오프라인”이라고 잘못 단정하지 않습니다.

나머지 값은 서로 다른 질문에 답합니다. `checkStatus`는 **`unknown`을 얼마나 확인했는지**를 나타냅니다. `checking`은 확인 중, `unavailable`은 10초가 지나도 확인하지 못했다는 안내, `idle`은 확정 상태입니다. `isRefreshing`은 사용자가 요청한 **수동 재확인이 진행 중인지**를 나타냅니다. `overrideStatus`는 debug 화면의 표시용 강제 값이며 실제 `realStatus`를 바꾸지 않습니다.

### 2. 앱이 시작하면: `init()` → 구독 → 관측

Root에서 `networkStore.init()`을 호출합니다. `init()`은 이미 세션이 있으면 바로 돌아가므로 구독을 중복 등록하지 않습니다. 처음 호출했을 때는 `session`을 만들고 `beginUnknownCheck()`로 `realStatus: 'unknown'`, `checkStatus: 'checking'`을 설정한 뒤 10초 안내 타이머를 켭니다. 이어 `subscribe()`가 `NetInfo.addEventListener()`를 등록합니다. 여기서는 별도의 초기 `NetInfo.fetch()`를 하지 않습니다. 리스너에 전달되는 첫 관측도 같은 경로로 처리합니다.

이벤트가 오면 리스너가 `observationVersion`을 올리고 `applyObservation()`에 값을 넘깁니다. 이 함수는 위 표로 상태를 계산합니다. 예를 들어 처음 `true / null`이면 여전히 `unknown`이므로 확인 중 상태를 유지합니다. 이후 `true / true`가 오면 `online`으로 바꾸고 안내 타이머를 끄며 `checkStatus`를 `idle`로 만듭니다. `false`가 하나라도 오면 같은 방식으로 `offline`이 됩니다.

같은 상태가 반복되면 `applyObservation()`은 아무것도 바꾸지 않습니다. 특히 `unknown` 이벤트가 여러 번 온다고 10초 안내 시간을 매번 처음부터 세지 않습니다. 반대로 `online`이었다가 다시 `unknown`이 되면 그때 새 10초 확인을 시작합니다. 10초가 끝나도 실제 상태는 `unknown` 그대로이고, 안내 값만 `unavailable`로 바뀝니다.

### 3. 사용자가 다시 확인하면: `refresh()`

`refresh()`는 먼저 `init()`을 보장하고, 이미 재확인 요청이 진행 중이면 **그 요청의 Promise를 그대로 반환**합니다. 그래서 버튼을 연달아 눌러도 `NetInfo.refresh()`를 여러 번 시작하지 않습니다. 실제 상태가 `unknown`이면 확인 안내의 10초 시간을 다시 시작합니다. 리스너 등록에 실패해 있었다면 다시 등록을 시도한 뒤 재확인 요청을 만듭니다.

여기에는 **서로 다른 두 개의 10초 대기**가 있습니다. `CHECK_NOTICE_DELAY`는 `unknown`일 때 안내를 “확인 중”에서 “확인할 수 없음”으로 바꾸는 시간입니다. `REFRESH_WAIT_LIMIT`는 `NetInfo.refresh()`가 응답하지 않을 때 앱이 그 재확인을 무한히 기다리지 않도록 요청을 끝내는 시간입니다. 둘 다 연결을 `offline`으로 판정하는 타이머는 아닙니다. `refresh()`의 반환형도 `Promise<void>`이므로, 그 Promise가 끝났다는 사실 자체가 `online` 확인을 뜻하지 않습니다. 결과는 `realStatus`를 봐야 합니다.

### 4. 왜 `session`, `refreshRequest`, `observationVersion`이 필요한가

네트워크 응답은 늦게 올 수 있습니다. 예를 들어 수동 재확인을 시작한 뒤 리스너가 먼저 `online`을 관측했는데, 이전 재확인 응답이 뒤늦게 `offline`으로 도착할 수 있습니다. 그 오래된 응답이 최신 관측을 덮으면 화면과 요청 판단이 거꾸로 돌아갑니다.

`startRefreshRequest()`는 요청 시작 시점의 `observationVersion`을 기억합니다. 응답을 적용하기 전에 `canApplyResult()`가 세 가지를 확인합니다. **여전히 같은 세션인가, 이 요청이 현재 진행 중인 요청인가, 요청 이후 리스너의 새 관측이 없었는가.** 하나라도 아니면 그 응답은 상태에 반영하지 않고 요청만 마칩니다. 요청이 10초를 넘겨 종료된 뒤 도착한 응답도 현재 요청이 아니므로 반영되지 않습니다.

`session`은 리스너 해제 함수, 안내 타이머, 진행 중 요청을 함께 소유합니다. `cleanup()`은 현재 세션을 먼저 비운 다음 타이머를 끄고, 재확인 대기를 끝내고, 리스너를 해제합니다. 이후 이전 리스너나 요청의 콜백이 늦게 와도 `currentSession !== session` 검사로 새 상태를 바꾸지 못합니다. Store의 실제 상태와 확인 표시는 초기 상태로 돌아갑니다. `overrideStatus`는 이 `cleanup()`에서 초기화하지 않는다는 점은 별개입니다.

### 5. 다른 코드가 이 값을 읽는 방법

- `networkStore.realStatus`와 `useRealNetworkStatus()`는 **실제 관측값**을 읽습니다. 실제 요청이나 sync 실행 여부를 판단할 때 기준이 되는 값입니다.
- `useDisplayNetworkStatus()`는 `overrideStatus ?? realStatus`를 읽습니다. debug에서 `online`으로 강제 표시해도 실제 상태는 그대로입니다. 헤더 상태 표시처럼 화면에서 사용하는 경로입니다.
- `useNetworkCheck()`는 확인 안내, 수동 재확인 진행 여부, `refresh()`를 화면에 제공합니다. `useNetworkControl()`은 debug override를 설정하거나 해제합니다.

따라서 이 파일을 읽을 때는 **실제 연결 판정(`realStatus`)**, **확인 과정의 안내(`checkStatus`, `isRefreshing`)**, **화면용 강제 표시(`overrideStatus`)**를 따로 보면 흐름이 단순해집니다. 예를 들어 실제 관측이 `unknown`인 채 10초가 지나면 연결 판정은 계속 `unknown`, 안내만 `unavailable`입니다. 그때 debug에서 `online`을 선택하면 화면 표시만 `online`이 되고 실제 연결을 필요로 하는 판단은 여전히 `unknown`을 봅니다.


---

## 03-B

이 파일은 **실제 인터넷 상태를 관측해 저장하고, 화면에 보여 줄 상태를 따로 제공하는 곳**입니다. 흐름을 읽을 때는 `init → NetInfo 관측 → 상태 갱신 → 필요하면 refresh → cleanup` 순서로 보면 됩니다. 아래 설명은 질문 시점의 [network.ts](/private/tmp/explain-source03-04-presentation-60high-20261025/run66932/code/network.ts)를 기준으로 합니다.

### 먼저, 상태 네 개의 뜻

| 값 | 뜻 |
|---|---|
| `realStatus` | 기기에서 실제로 관측한 인터넷 상태: `online`, `offline`, `unknown` |
| `overrideStatus` | debug 화면에서 강제로 **표시할** 상태. 실제 관측값은 바꾸지 않음 |
| `checkStatus` | 실제 상태가 `unknown`일 때 안내할 확인 단계: `checking` 또는 `unavailable`. 확정 상태에서는 `idle` |
| `isRefreshing` | 사용자가 누른 재확인 요청을 현재 기다리는지 |

`unknown`은 오프라인이라는 뜻이 아닙니다. `resolveNetworkStatus()`는 NetInfo의 `isConnected`와 `isInternetReachable` 중 **하나라도 명시적으로 `false`면 offline**, **둘 다 `true`면 online**, 그 외에는 `unknown`으로 둡니다. 예를 들어 Wi-Fi 연결은 확인됐지만 인터넷 도달 여부가 `null`이면 `unknown`입니다.

### 앱이 시작되면

Root가 `networkStore.init()`을 호출합니다. `init()`은 한 번의 관측 수명을 나타내는 `session`을 만들고, `beginUnknownCheck()`로 `unknown / checking` 상태와 10초 안내 타이머를 설정한 뒤 `NetInfo.addEventListener()`를 등록합니다. 이미 session이 있으면 다시 등록하지 않습니다. 이 listener가 첫 관측도 전달하므로 `init()`에서 별도 `fetch()`를 하지 않습니다.

관측이 오면 `applyObservation()`이 위 규칙으로 `realStatus`를 바꿉니다.

- `online` 또는 `offline`으로 확정되면 안내 타이머를 지우고 `checkStatus`를 `idle`로 만듭니다.
- 확정 상태에서 다시 `unknown`이 되면 `checking`으로 바꾸고 새 10초 타이머를 시작합니다.
- 이미 `unknown`인데 같은 `unknown` 관측이 반복되면 아무것도 다시 시작하지 않습니다. 이미 9초 기다렸다면 1초 뒤 기존 안내가 바뀝니다.

10초가 지나도 `realStatus`를 `offline`으로 추정하지 않습니다. 여전히 `unknown`인 경우에만 `checkStatus`를 `unavailable`로 바꿔 “연결을 확인할 수 없어요”라고 안내합니다. 나중에 실제 관측이 오면 그때 `online` 또는 `offline`으로 갱신됩니다.

### 수동으로 다시 확인하면

`refresh()`는 먼저 listener가 있는지 확인하고 `NetInfo.refresh()`를 요청합니다. 같은 요청이 진행 중이면 새 요청을 만들지 않고 **기존 Promise를 반환**합니다. 시작할 때 `isRefreshing`을 `true`로, 응답·실패·대기 시간 종료 때 `false`로 돌립니다. 실제 상태가 `unknown`이었다면 안내용 10초 시간을 다시 시작합니다.

여기에는 **서로 다른 10초 제한 두 개**가 있습니다. 하나는 `unknown` 안내를 `checking → unavailable`로 바꾸는 시간이고, 다른 하나는 응답 없는 수동 `refresh()`를 더 기다리지 않기 위한 시간입니다. 어느 쪽도 인터넷을 `offline`으로 판정하지 않습니다. `refresh()`가 반환됐다는 것 역시 온라인 확인 성공을 뜻하지 않습니다.

재확인 중 listener가 더 새로운 관측을 보낼 수도 있습니다. 그래서 요청 시작 때 `observationVersion`을 기억해 두고, 응답이 왔을 때 그 사이 새 관측이 있었다면 **늦은 재확인 결과로 최신 상태를 덮지 않습니다**. 예를 들어 재확인 요청 후 listener가 `online`을 알려 줬는데, 오래된 요청이 `offline`으로 돌아와도 화면은 `online`을 유지합니다.

### 화면 표시와 정리

`useDisplayNetworkStatus()`는 `overrideStatus ?? realStatus`를 반환합니다. debug에서 online을 강제로 골라도 `realStatus`는 그대로이며, 실제 요청을 판단하는 `networkStore.realStatus`에도 영향을 주지 않습니다. `useNetworkCheck()`는 확인 안내와 재확인 버튼에 필요한 값들을 제공합니다.

Root가 내려갈 때 `cleanup()`은 listener와 타이머를 정리하고 진행 중인 재확인의 기다림을 끝냅니다. `currentSession`을 먼저 비우기 때문에 이전 listener나 오래된 재확인 결과가 나중에 도착해도 새 session의 상태를 바꾸지 못합니다. 화면에 노출된 상태는 다시 `unknown / checking`으로 초기화됩니다.

요약하면 **`realStatus`는 관측 결과, `checkStatus`는 아직 모를 때의 안내, `isRefreshing`은 수동 요청의 대기 여부, `overrideStatus`는 debug 표시용**입니다. `session`과 `observationVersion`은 오래된 비동기 결과가 현재 관측을 덮지 않게 지키는 내부 장치입니다.


---

## 03-C

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


---

## 04-A

맞아요. **코드를 바꾼 뒤에는 테스트를 다시 실행해야 합니다.** 다만 이번처럼 외부 동작을 보존하는 리팩터링이라면, 테스트의 기대값까지 바뀌어야 하는 것은 아닙니다.

이번 테스트는 변경 전 `useStorageStats`에서 먼저 통과했습니다. 테스트가 확인하는 것은 `dbSize`·`mapPackSize`·`totalSize`의 결과, DB 조회 실패 시 Mapbox를 시작하지 않는 동작, 개별 팩 실패 후 계속 집계하는 동작, `refresh()` 재계산입니다. 변경 후에는 성공 경로와 `catch`에 각각 있던 `setStats`를 `finally`의 한 호출로 모았지만, 이 결과와 실패 정책은 바꾸지 않았습니다. 그래서 **같은 테스트를 수정하지 않고 다시 돌려 통과하는 것**이 이번 동작 보존의 근거입니다. 당시 결과는 저장 용량 테스트 6개와 설정 확인 테스트 1개, 총 7개 통과였습니다.

테스트를 새 `createStorageStats` 함수나 `finally` 호출 횟수에 맞춰 고치면 내부 구현에 테스트가 묶입니다. 반대로 기존 테스트가 놓친 실제 계약을 발견했거나 의도적으로 동작을 바꾸기로 했다면, 그때는 해당 사례와 기대값을 보완해야 합니다. 이번 변경에서는 그런 동작 변경이 확인되지 않아 테스트 코드를 그대로 둔 것이 맞습니다. 다만 이 통과 결과는 mock으로 확인한 시나리오의 근거이며 실제 기기의 FileSystem·Mapbox 연결까지 증명하지는 않습니다.


---

## 04-B

꼭 바뀌어야 하는 것은 아닙니다. 이번 테스트는 **코드를 바꾸기 전에 기존 동작을 기준으로 만든 회귀 테스트**입니다. 리팩터링 뒤에도 사용자에게 반환하는 값과 실패 처리 방식이 같아야 하므로, 같은 입력과 기대값으로 다시 실행하는 것이 핵심입니다. 테스트의 기대값을 코드에 맞춰 함께 고치면 동작이 달라져도 알아채기 어려워집니다.

이번 변경은 `formatBytes`와 stats 조립을 한곳으로 모으고, 성공 경로와 바깥 `catch`에 각각 있던 `setStats`를 `finally`의 한 호출로 합친 것입니다. DB 조회 실패 시 Mapbox 조회를 중단하고 부분 합계를 남기는 방식, 개별 지도 팩 실패 후 다음 팩을 처리하는 방식, `refresh()` 결과는 바꾸지 않았습니다. 기존 테스트 6개가 바로 이런 **결과와 중단·계속 조건**을 확인하며, 변경 전과 후에 모두 통과했습니다. 새 helper의 이름이나 `setStats` 호출 위치에 맞춰 테스트를 고칠 필요는 없습니다.

테스트를 바꿔야 하는 경우는 요구 동작이 실제로 바뀌었거나, 새 분기가 생겼거나, 기존 테스트가 중요한 결과를 놓친 것으로 확인됐을 때입니다. 현재의 7개 통과 결과는 mock으로 만든 6가지 저장 용량 상황과 테스트 환경 확인 1건에 대한 근거입니다. 실제 기기의 FileSystem·Mapbox 연결이나 모든 가능한 입력까지 증명하는 것은 아닙니다. 제가 앞서 “코드 변경 완료”라고만 하면서 **테스트를 그대로 둔 이유와 검증 범위**를 설명하지 않았습니다.
