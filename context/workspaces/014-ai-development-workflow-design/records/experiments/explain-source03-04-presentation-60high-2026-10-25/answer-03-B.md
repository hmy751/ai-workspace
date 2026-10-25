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
