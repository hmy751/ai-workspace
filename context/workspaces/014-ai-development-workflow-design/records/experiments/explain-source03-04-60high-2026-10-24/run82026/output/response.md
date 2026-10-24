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
