## 03 — A

이 파일은 **NetInfo가 알려 준 연결 상태를 앱에서 쓸 세 가지 값으로 바꾸고, 그 값을 계속 갱신하는 곳**입니다. 흐름을 먼저 한 줄로 보면 이렇습니다.

`Root에서 init()` → `NetInfo 구독` → `관측값을 online/offline/unknown으로 변환` → `Store 갱신` → `화면이나 요청 코드가 읽음`

### 1. 처음 시작할 때

Root가 `networkStore.init()`을 부르면 `currentSession`을 하나 만들고, 상태를 `unknown`·`checking`으로 둡니다. 이어서 10초 안내 타이머를 시작하고 `NetInfo.addEventListener`를 등록합니다. NetInfo가 첫 값을 알려 주면 listener가 `applyObservation()`에 전달합니다. 이미 session이 있으면 `init()`은 아무것도 더 만들지 않아 구독이 중복되지 않습니다.

여기서 `currentSession`은 화면에 보여 줄 상태가 아닙니다. **현재 구독, 타이머, 진행 중인 재확인 요청을 묶어 관리하는 실행 단위**입니다. 화면에서 읽는 값은 Zustand Store의 `realStatus`, `checkStatus`, `isRefreshing`입니다.

### 2. 관측값이 들어올 때

`resolveNetworkStatus()`가 NetInfo의 두 신호를 판정합니다.

| `isConnected` / `isInternetReachable` | 결과 |
|---|---|
| 둘 다 `true` | `online` |
| 하나라도 `false` | `offline` |
| 그 외, 예를 들어 `true` / `null` | `unknown` |

즉 기기에 네트워크가 연결돼 있다는 신호만으로 인터넷 사용 가능을 단정하지 않습니다. `applyObservation()`은 결과가 이전 `realStatus`와 같으면 그대로 두고, 달라졌을 때만 갱신합니다. `online`이나 `offline`이 확정되면 10초 타이머를 지우고 `checkStatus`를 `idle`로 만듭니다. 사용 중 다시 `unknown`이 되면 새 10초 확인 안내가 시작됩니다.

**10초는 연결 판정의 제한 시간이 아닙니다.** 그때까지 `unknown`이면 `realStatus`는 그대로 두고 `checkStatus`만 `checking`에서 `unavailable`로 바꿉니다. 따라서 화면 문구는 “확인 중”에서 “확인할 수 없음”으로 바뀌지만, 코드가 임의로 offline이라고 판단하지는 않습니다. 이후 확정된 관측이 오면 그 상태로 갱신됩니다.

### 3. 사용자가 재확인을 누를 때

`refresh()`는 `NetInfo.refresh()`를 호출해 지금 상태를 다시 요청합니다. 이미 재확인 중이면 새 요청을 보내지 않고 진행 중인 Promise를 돌려줍니다. `isRefreshing`은 이 요청을 기다리는 동안 화면에 진행 상태를 표시하는 값입니다. 현재 상태가 `unknown`이면 10초 안내 시간도 새로 시작합니다.

재확인 결과가 늦게 도착할 수 있어서 세 가지를 확인한 뒤에만 적용합니다. **같은 session인지, 아직 그 재확인 요청이 유효한지, 요청을 시작한 뒤 listener가 더 새로운 관측을 받지 않았는지**입니다. 예를 들어 재확인을 요청한 뒤 listener가 `online`을 알렸는데 옛 재확인 결과가 `offline`으로 돌아오면, 옛 결과는 상태를 덮지 않습니다. 재확인 응답이 10초 동안 없으면 앱의 대기만 끝내며, NetInfo의 구독은 계속 살아 있습니다. 이 10초는 앞의 `unknown` 안내 타이머와 용도가 다릅니다.

### 4. 실제 상태와 화면용 상태

`realStatus`는 NetInfo 관측 결과입니다. `overrideStatus`는 debug에서 화면을 online/offline/unknown으로 **보이게 하는 설정**입니다. `useDisplayNetworkStatus()`는 override가 있으면 그것을 돌려주고, 없으면 실제 상태를 돌려줍니다. 반면 `networkStore.realStatus`와 `useRealNetworkStatus()`는 실제 관측값을 읽습니다. 그래서 debug 화면을 강제로 online으로 보여 줘도 실제 연결이 unknown인 상황에서 이를 인터넷 연결의 증거로 쓰면 안 됩니다. `useNetworkCheck()`는 안내 상태·진행 상태·재확인 함수를 묶어 화면에 제공합니다.

마지막으로 Root가 내려가 `cleanup()`을 부르면 현재 session을 무효화하고 구독·타이머·대기 중인 재확인을 정리합니다. 이후 옛 listener나 재확인 결과가 도착해도 새 session의 상태를 바꾸지 못합니다. Store의 실제 상태는 다시 `unknown`·`checking`으로 돌아갑니다.

헷갈리기 쉬운 핵심은 **`realStatus`는 연결 판정, `checkStatus`는 unknown일 때 보여 줄 안내 단계, `isRefreshing`은 수동 재확인 진행 여부**라는 점입니다. 셋은 서로 다른 질문에 답합니다.


---

## 03 — B

`network.ts`는 **NetInfo의 관측값을 앱에서 쓸 세 가지 상태로 바꾸고, 그 관측을 시작·재확인·정리하는 Store**입니다. 흐름은 `init → NetInfo 알림 수신 → 상태 갱신`이고, 사용자가 다시 확인할 때만 `refresh`가 추가됩니다. 질문 시점의 코드 기준으로 설명할게요.

먼저 상태 네 가지를 구별하면 나머지가 읽힙니다.

- `realStatus`: 실제 관측한 연결 상태. `online`, `offline`, `unknown` 중 하나입니다.
- `checkStatus`: **실제 상태가 `unknown`일 때 보여 줄 안내 단계**입니다. `checking`은 확인 중, `unavailable`은 10초가 지나도 확인하지 못했다는 뜻입니다. 10초가 지나도 `realStatus`를 `offline`으로 추정하지 않습니다.
- `isRefreshing`: 수동 재확인 요청을 기다리는 중인지 표시합니다.
- `overrideStatus`: debug 화면에서 상태를 강제로 *표시*할 때 쓰는 값입니다. 실제 연결 상태는 바꾸지 않습니다.

앱의 Root가 `networkStore.init()`을 호출하면 `init`은 먼저 세션을 하나 만듭니다. 이 세션이 NetInfo 구독 해제 함수, 10초 안내 타이머, 진행 중인 재확인 요청을 소유합니다. 이미 세션이 있으면 다시 구독하지 않습니다.

```ts
currentSession = session;
beginUnknownCheck(session);
subscribe(session);
```

`beginUnknownCheck`는 `realStatus: 'unknown'`, `checkStatus: 'checking'`으로 두고 10초 타이머를 겁니다. `subscribe`는 `NetInfo.addEventListener`를 등록합니다. **첫 관측도 이 listener를 통해 받도록** 만들어서, 시작할 때 별도의 `NetInfo.fetch()`는 호출하지 않습니다.

관측이 오면 listener가 `observationVersion`을 올린 뒤 `applyObservation`에 전달합니다. 여기서 두 신호를 이렇게 해석합니다.

```ts
if (state.isConnected === false || state.isInternetReachable === false) return 'offline';
if (state.isConnected === true && state.isInternetReachable === true) return 'online';
return 'unknown';
```

즉 **하나라도 명시적으로 `false`면 offline, 둘 다 `true`여야 online**, 나머지는 unknown입니다. 새 값이 이전 `realStatus`와 같으면 그대로 둡니다. online 또는 offline으로 확정되면 안내 타이머를 지우고 `checkStatus`를 `idle`로 바꿉니다. 확정 상태에서 다시 unknown으로 바뀌면 새 10초 확인을 시작합니다.

예를 들어 첫 관측이 `isConnected: true`, `isInternetReachable: null`이면 `unknown`입니다. 10초 뒤에도 미확정이면 실제 상태는 그대로 `unknown`이고 안내만 `unavailable`로 바뀝니다. 이후 `true / true` 관측이 오면 `online`과 `idle`로 바뀝니다. 같은 unknown 관측이 반복된다고 10초 타이머를 매번 새로 시작하지는 않습니다.

**수동 재확인 `refresh()`는 listener와 별개의 일회성 확인입니다.** 호출 시 구독이 없으면 시작하거나 재등록을 시도하고, 이미 재확인 중이면 새 요청을 만들지 않고 그 요청의 Promise를 돌려줍니다. 실제 요청은 `NetInfo.refresh()`로 보냅니다. unknown 상태에서 누르면 10초 안내 시간도 그 시점부터 다시 시작합니다.

여기서 `observationVersion`과 `refreshRequest`가 필요한 이유는 *늦은 결과가 더 새로운 관측을 덮지 않게* 하기 위해서입니다. 재확인을 시작할 때 관측 번호를 기억하고, 응답이 돌아왔을 때 **같은 세션·같은 요청이며 그 사이 listener 관측이 없었을 때만** 결과를 적용합니다. 그 사이 listener가 새 상태를 알려 줬다면 재확인 응답은 상태에 반영하지 않고 요청만 끝냅니다. 10초 동안 응답이 없을 때도 기다림을 해제합니다. 늦게 도착한 응답이 다음 재확인이나 새 세션을 바꾸지는 못합니다. `refresh()`의 Promise가 끝났다는 것은 *재확인 대기가 끝났다*는 뜻이지, online 확인에 성공했다는 뜻은 아닙니다.

앱이 Root에서 내려가며 `cleanup()`을 호출하면 현재 세션을 비우고 타이머·진행 중인 재확인·NetInfo 구독을 정리합니다. 실제 상태와 안내는 초기값으로 되돌립니다. 옛 listener나 옛 재확인 결과는 더 이상 현재 세션과 일치하지 않아 무시됩니다.

마지막의 `networkStore`는 React 밖에서도 `init`, `cleanup`, `refresh`, 실제 상태를 쓰도록 만든 입구입니다. React 화면은 hook으로 구독합니다. `useRealNetworkStatus()`는 실제 관측값, `useDisplayNetworkStatus()`는 `overrideStatus ?? realStatus`를 돌려줍니다. 따라서 debug에서 online으로 강제 표시해도 실제 상태가 unknown이라면 **화면 표시만 online**이고, 실제 연결을 판단하는 코드는 여전히 unknown을 보게 됩니다.


---

## 03 — C

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


---

## 04 — A

맞아요. **코드를 바꾼 뒤에는 테스트를 다시 실행해야 합니다.** 다만 이번 변경은 저장 용량을 계산하는 *결과*를 바꾸는 작업이 아니라, 같은 결과를 만드는 중복 코드를 정리하는 리팩터링이라 테스트의 기대값까지 바꿀 이유는 없습니다. 변경 전 테스트를 그대로 통과시키는 것이 동작 보존 확인의 핵심입니다.

변경 전에는 정상 경로와 바깥 `catch`가 각각 `setStats`로 DB·지도·합계 문자열을 조립했습니다. 변경 후에는 두 경로가 `finally`의 `setStats(createStorageStats(dbSizeBytes, mapSizeBytes))`를 함께 사용합니다. 기존 테스트는 내부 함수 이름이 아니라 실제 hook의 결과를 봅니다. 예를 들어 DB 파일 조회가 중간에 실패하면 이전까지의 `1 KB`를 남기고 Mapbox를 호출하지 않는지, 지도 팩 하나가 실패해도 다음 팩을 합산하는지를 검사합니다. 그래서 이 테스트를 구현에 맞춰 고치면 오히려 동작 변화가 가려질 수 있습니다.

당시 기록상 변경 전 특성화 테스트 6개가 통과했고, 변경 후에도 **같은 테스트 6개와 환경 확인 테스트 1개가 통과**했습니다. 테스트 파일은 이 리팩터링 때문에 수정되지 않았습니다. 중복된 조립 위치가 실제로 하나로 줄었는지는 테스트 통과가 아니라 코드의 전후 비교로 확인할 사항입니다.

반대로 의도적으로 반환값이나 실패 정책을 바꾼다면 새 계약에 맞춰 테스트를 바꿔야 합니다. 이번처럼 초기값을 만드는 코드도 바뀌었으므로, 렌더 직후 `0 B` 표시 자체를 별도 계약으로 보호하고 싶다면 그 시점을 확인하는 테스트를 **추가**할 수는 있습니다. 현재의 빈 저장소 테스트는 조회 후 값을 확인합니다. 이것은 보강할 수 있는 지점이지, 기존 회귀 테스트의 기대값을 새 구현에 맞춰 바꿔야 한다는 뜻은 아닙니다.


---

## 04 — B

꼭 그렇지는 않습니다. **이번 변경은 테스트가 확인하는 동작을 유지하려는 리팩터링**이라, 변경 전에 만든 회귀 테스트를 그대로 두고 변경 후에도 통과하는지 보는 게 핵심입니다.

이전 코드는 정상 완료와 바깥 `catch`에서 각각 `dbSize`, `mapPackSize`, `totalSize`를 만들어 `setStats`에 넣었습니다. 변경 후에는 두 경로 모두 `finally`에서 `setStats(createStorageStats(dbSizeBytes, mapSizeBytes))`를 호출합니다. 테스트는 그 내부 위치가 아니라, 예를 들어 DB 파일 조회가 중간에 실패하면 **그때까지의 DB 용량만 표시하고 Mapbox는 호출하지 않는지**, 개별 지도 팩이 실패하면 **다음 팩을 계속 합산하는지**, `refresh()`가 **새 값으로 다시 계산하는지**를 확인합니다. 이 기대 결과를 바꾸지 않았으므로 테스트의 기대값도 바꿀 이유가 없습니다.

실제로 변경 전 작성한 hook 테스트 6개가 기존 구현에서 통과했고, 코드 변경 후에도 같은 테스트 6개가 통과했습니다. 당시 보고한 **7개 통과**에는 테스트 환경 확인용 smoke test 1개가 포함됩니다. 다만 통과가 모든 동작을 증명한다는 뜻은 아닙니다. 예를 들어 현재 빈 저장소 테스트는 조회가 끝난 뒤의 `0 B`를 확인하며, 변경된 **초기 렌더 시점**의 값을 직접 확인하지는 않습니다. 초기 표시까지 명시적인 보존 조건으로 확인하려면 그 단언을 추가할 수 있습니다.

테스트를 바꿔야 하는 경우는 요구한 동작 자체가 달라졌거나, 기존 테스트의 기대값이 잘못됐거나, 변경으로 드러난 중요한 조건이 빠져 있을 때입니다. 이번처럼 조립 위치만 바꾼 뒤 결과에 맞춰 기존 기대값을 고치면, 오히려 회귀를 잡는 기준을 잃을 수 있습니다.
