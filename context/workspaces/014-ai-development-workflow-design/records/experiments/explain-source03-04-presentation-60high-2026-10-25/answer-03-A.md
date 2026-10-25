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
