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
