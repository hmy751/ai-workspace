핵심은 이 파일이 **NetInfo의 관측값을 앱의 네트워크 상태로 바꾸고, 그 상태를 화면과 실제 실행 코드에 제공한다**는 것입니다. `init()`으로 관측을 시작하고, NetInfo 알림이 올 때마다 상태를 갱신합니다. `refresh()`는 사용자가 다시 확인할 때 쓰며, `cleanup()`은 관측을 끝냅니다.

```text
앱 시작 → init() → NetInfo 구독 → 관측값 수신 → realStatus 갱신
                          ↘ 수동 refresh() → 재확인 결과 반영
앱 종료 → cleanup() → 구독·타이머·대기 중인 재확인 정리
```

### 1. NetInfo 값은 어떻게 상태가 되나

NetInfo는 `isConnected`(네트워크에 연결됐는가)와 `isInternetReachable`(인터넷에 도달하는가)을 줍니다. `resolveNetworkStatus()`는 **둘 중 하나라도 `false`면 `offline`**, **둘 다 `true`면 `online`**, 그 밖에는 `unknown`으로 바꿉니다. 예를 들어 Wi-Fi 연결이 `true`여도 인터넷 도달 여부가 `null`이면 아직 `online`이라고 단정하지 않아 `unknown`입니다.

여기서 `realStatus`가 실제 관측으로 얻은 결과입니다. 별도의 `checkStatus`는 `unknown`을 어떻게 안내할지만 나타냅니다. `checking`은 확인 중, `unavailable`은 한동안 확인하지 못했다는 뜻입니다. **10초가 지나도 `realStatus`를 `offline`으로 바꾸지는 않습니다.**

### 2. 앱이 시작할 때

Root에서 `networkStore.init()`을 부릅니다. `init()`은 이미 `currentSession`이 있으면 그대로 돌아가므로 구독을 중복 생성하지 않습니다. 처음이면 새 `session`을 저장하고 `beginUnknownCheck()`로 상태를 `unknown`·`checking`으로 두면서 10초 안내 타이머를 건 뒤, `NetInfo.addEventListener()`로 관측을 구독합니다. 구독 등록 자체가 첫 상태를 받아오므로 이 경로에서 별도의 `NetInfo.fetch()`를 호출하지 않습니다.

알림이 오면 `applyObservation()`이 위 규칙으로 상태를 바꿉니다. `online`이나 `offline`이 확정되면 안내 타이머를 지우고 `checkStatus`를 `idle`로 둡니다. 사용 중 확정 상태에서 다시 `unknown`이 되면 새 10초 확인을 시작합니다. 반면 **이미 `unknown`인데 같은 `unknown` 알림이 반복되면** 상태가 같다는 검사에서 돌아가므로 10초를 매번 연장하지 않습니다.

예를 들어 시작 후 `true/null`만 관측되면 `realStatus=unknown`, `checkStatus=checking`입니다. 10초가 지나면 `unknown/unavailable`이 되고, 이후 `true/true`가 오면 `online/idle`이 됩니다.

### 3. 수동으로 다시 확인할 때

`refresh()`는 필요하면 먼저 `init()`을 하고 `NetInfo.refresh()`를 요청합니다. 이미 재확인 중이면 `session.refreshRequest.promise`를 그대로 반환하므로 버튼을 연달아 눌러도 새 요청을 만들지 않습니다. 현재 `unknown`이라면 안내 타이머를 다시 시작해 `checkStatus`를 `checking`으로 돌립니다. `isRefreshing`은 **이 수동 재확인을 기다리는 중인지** 표시하는 값이며, 연결 상태 자체는 아닙니다.

재확인에는 별도의 10초 대기 한도가 있습니다. 응답이 없거나 실패하면 대기를 끝내고 `isRefreshing`을 내립니다. 그 시점에도 실제 상태가 `unknown`이면 `checkStatus`를 `unavailable`로 표시합니다. 이 한도는 앱의 **대기를 해제하는 것**이지, NetInfo 관측 구독을 중단하거나 `unknown`을 `offline`으로 확정하는 것이 아닙니다. `refresh()`가 돌려주는 `Promise<void>`도 재확인이 끝났다는 신호이지 `online` 성공 결과가 아닙니다.

### 4. 왜 `session`과 번호를 비교하나

비동기 응답은 도착 순서가 바뀔 수 있습니다. 재확인을 요청한 뒤 구독 알림으로 최신 `online`을 받았는데, 앞선 재확인 결과가 늦게 `offline`으로 도착할 수 있습니다. 구독 알림마다 `observationVersion`을 올리고, 재확인을 시작할 때의 번호와 결과 도착 때의 번호를 비교하는 이유가 이것입니다. 번호가 달라졌으면 그사이 새 관측이 있었으므로 오래된 재확인 결과를 상태에 적용하지 않습니다.

나머지 두 비교도 역할이 다릅니다. `currentSession === session`은 `cleanup()` 후 옛 구독·응답이 새 실행에 끼어들지 못하게 하고, `session.refreshRequest === request`는 시간 초과된 옛 요청이 다음 재확인을 덮지 못하게 합니다. 결과를 무시하더라도 해당 요청의 대기는 `finish()`로 마칩니다. `cleanup()`은 구독과 타이머를 해제하고 기다리던 재확인도 끝낸 뒤 실제 상태를 초기값으로 돌립니다.

### 5. 화면에는 어떤 값을 주나

`useDisplayNetworkStatus()`는 `overrideStatus ?? realStatus`를 반환합니다. debug 화면에서 강제로 `online`·`offline`·`unknown`을 표시할 수 있다는 뜻입니다. 반면 `useRealNetworkStatus()`와 `networkStore.realStatus`는 실제 관측값을 줍니다. 따라서 **화면에 강제로 online을 표시해도 실제 요청 판단이 online으로 바뀌지는 않습니다.** `useNetworkCheck()`는 확인 안내와 수동 재확인을, `useNetworkControl()`은 강제 표시 설정을 화면에 제공합니다.

즉 이 파일을 읽을 때는 **`realStatus`는 연결 판정, `checkStatus`는 unknown 안내, `isRefreshing`은 수동 확인의 진행 표시, `overrideStatus`는 화면용 강제 표시**로 나눠 보면 흐름이 잡힙니다. 이 설명은 해당 코드와 제공된 검사 발췌를 따라 해석한 것이며, 실기기 네트워크 동작을 새로 실행해 확인한 결과는 아닙니다.
