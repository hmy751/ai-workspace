이 파일은 **기기에서 받은 네트워크 정보를 앱 공통 상태로 유지하고, 화면과 일반 코드가 그 상태를 읽게 하는 코드**입니다. 앱 시작 때 감시를 켜고, 연결 정보가 오면 상태를 바꾸며, 사용자가 재확인하면 한 번 더 확인합니다.

`work-artifact-briefing` 기준으로 흐름을 풀어보겠습니다. 아래는 원복 뒤인 9월 17일의 보존 코드를 따라 설명한 것이며, 실기기 실행을 관찰한 결과는 아닙니다.

먼저 네 가지 상태를 구별하면 뒤의 함수가 읽힙니다.

| 값 | 뜻 | 예 |
|---|---|---|
| `realStatus` | NetInfo에서 받은 정보로 판정한 실제 연결 상태 | `online`, `offline`, `unknown` |
| `checkStatus` | 연결이 불확실할 때 보여 줄 확인 안내 단계 | `checking`: 확인 중, `unavailable`: 확인하지 못함, `idle`: 확인 안내 불필요 |
| `isRefreshing` | 사용자가 요청한 재확인을 앱이 기다리는 중인가 | `true`이면 재확인 진행 표시 가능 |
| `overrideStatus` | debug에서 화면에 강제로 적용한 상태 | `null`이면 실제 상태를 표시 |

그래서 **`realStatus = unknown`, `checkStatus = unavailable`, `isRefreshing = false`가 동시에 가능**합니다. “연결 여부를 모르고, 확인하지 못했다는 안내를 보여 주며, 수동 재확인은 기다리지 않는다”는 뜻입니다.

**앱을 켰을 때는 `init()`에서 시작합니다.**

제공된 Root 코드에서는 화면이 처음 마운트될 때 `networkStore.init()`을 호출합니다. 그러면 [init 구현](/private/tmp/0402-network-body-20261022/r63/code/network.ts:73)은 다음 일을 합니다.

1. 이미 감시 중이면 그대로 끝냅니다. `init()`을 두 번 호출해도 감시를 두 개 만들지 않습니다.
2. 이번 감시에 필요한 자원을 담는 `session` 객체를 만들고 `currentSession`에 저장합니다.
3. `beginUnknownCheck()`로 실제 상태를 `unknown`, 안내를 `checking`으로 놓고 10초 타이머를 켭니다.
4. `subscribe()`로 NetInfo의 연결 정보 수신을 등록합니다.

NetInfo는 기기의 연결 정보를 전달하는 라이브러리입니다. 이 코드는 `addEventListener()` 등록으로 첫 정보와 이후 변경 정보를 받으며, 초기화에서 별도 `fetch()`를 호출하지 않습니다.

대표적인 상태 전달 경로는 이렇습니다. 아래는 소스에서 재구성한 호출 순서입니다.

```text
Root가 init() 호출 → NetInfo listener 등록
NetInfo 정보 도착 → applyObservation() → resolveNetworkStatus() → Store 갱신 → 구독한 화면 갱신
```

`resolveNetworkStatus()`는 두 입력을 하나의 앱 상태로 바꿉니다. `isConnected`는 기기의 네트워크 연결 여부, `isInternetReachable`은 인터넷 도달 여부를 나타냅니다.

- 하나라도 명시적으로 `false`이면 `offline`.
- 둘 다 `true`이면 `online`.
- 나머지는 `unknown`. 예를 들어 Wi-Fi에는 연결됐지만 인터넷 도달 여부가 `null`이면 아직 `online`이라고 하지 않습니다.

[applyObservation()](/private/tmp/0402-network-body-20261022/r63/code/network.ts:155)은 이 판정 결과를 반영합니다. `online`이나 `offline`으로 확정되면 안내 타이머를 끄고 `checkStatus`를 `idle`로 바꿉니다. 확정 상태에서 다시 `unknown`이 되면 새 10초 확인 안내를 시작합니다.

이미 `unknown`인데 같은 `unknown` 정보가 반복해서 들어오면 아무것도 바꾸지 않습니다. 그래서 정보가 반복된다는 이유로 10초 타이머가 계속 뒤로 밀리지 않습니다. 10초가 지나도 연결 상태는 `unknown`으로 남고 **안내만 `unavailable`로 바뀝니다.**

**재확인 버튼을 누르면 `refresh()`가 실행됩니다.**

[refresh 구현](/private/tmp/0402-network-body-20261022/r63/code/network.ts:103)은 평소의 listener 감시를 유지하면서 NetInfo에 명시적인 재확인을 요청합니다.

1. `init()`으로 감시가 준비됐는지 확보합니다.
2. 이미 재확인 중이면 기존 요청의 Promise를 반환합니다. 연타해도 새 요청을 만들지 않고 같은 완료를 기다립니다.
3. 현재 상태가 `unknown`이면 확인 안내의 10초를 다시 시작합니다. 이미 `online`이나 `offline`이면 재확인한다고 그 상태를 지우지는 않습니다.
4. listener 등록을 확보합니다. 등록 실패라면 여기서 끝냅니다.
5. `startRefreshRequest()`로 요청 관리 객체를 만들고 `isRefreshing = true`로 바꾼 뒤 `NetInfo.refresh()`를 호출합니다.

요청 관리 객체의 이름은 이렇게 읽으면 됩니다.

| 이름 | 맡은 일 |
|---|---|
| `promise` | 호출한 쪽이 재확인 대기 종료를 기다리는 값 |
| `accept(state)` | 응답을 받아 반영 가능한지 확인하고 마무리 |
| `fail()` | 실패나 대기 시간 초과를 처리하고 마무리 |
| `finish()` | 타이머·진행 중 요청을 정리하고 대기를 종료 |

응답이 오면 `accept()`가 상태를 반영하고 `finish()`가 진행 표시를 끕니다. 실패하면 `fail()`이 처리합니다. 이때 실제 상태가 `unknown`일 때만 안내를 `unavailable`로 바꾸므로, 재확인 실패 자체를 곧바로 `offline`으로 해석하지 않습니다.

응답이 없으면 최대 10초 뒤 앱의 대기를 끝냅니다. **기기의 확인 작업을 취소하는 것은 아닙니다.** 이후 연결 정보는 계속 listener로 받을 수 있습니다. 반환되는 `Promise<void>`도 “인터넷 연결 성공”을 뜻하지 않습니다. 실패·시간 초과·정리 때도 완료되므로 실제 결과는 Store의 상태로 읽습니다.

여기에는 서로 다른 10초 타이머가 있습니다. `CHECK_NOTICE_DELAY`는 unknown 안내를 바꾸는 시간이고, `REFRESH_WAIT_LIMIT`은 수동 재확인을 기다리는 최대 시간입니다. 시작 시점과 목적이 다릅니다.

**가장 복잡한 `session`과 세 조건은 늦은 응답을 처리하기 위해 있습니다.**

`session`은 로그인 세션이 아니라 **한 번의 네트워크 감시 수명 동안 사용하는 내부 자원 묶음**입니다. 구독 해제 함수, 안내 타이머, 관측 횟수, 진행 중 재확인 요청을 담습니다. 화면이 표시할 값은 Store에 있고, 감시를 관리하는 자원은 `createNetworkActions()` 내부에 있습니다. 이 함수는 Store 생성 때 `init`, `cleanup`, `refresh`를 만들어 반환하며, 그 함수들이 내부 `currentSession`을 계속 공유합니다. `set`은 Store 갱신, `get`은 최신 Store 읽기입니다.

재확인 응답을 반영하기 전에는 [canApplyResult()](/private/tmp/0402-network-body-20261022/r63/code/network.ts:205)의 세 조건을 모두 검사합니다.

| 조건 | 필요한 이유 |
|---|---|
| `currentSession === session` | 감시를 종료하고 다시 시작했다면 이전 감시의 응답을 버리기 위해 |
| `session.refreshRequest === request` | 시간 초과로 끝난 요청이나 다른 요청의 늦은 응답을 버리기 위해 |
| `observationVersion === startingObservationVersion` | 요청 후 listener 정보가 도착했다면 그 정보를 이전 재확인 응답으로 덮지 않기 위해 |

설명용으로 다음 순서를 생각하면 마지막 조건이 보입니다.

```text
재확인 시작: 관측 횟수 3을 기억
listener로 online 도착: 관측 횟수 4, Store는 online
이전 재확인에서 offline 응답 도착: 3과 4가 다르므로 반영하지 않음
```

이때 이전 요청의 대기는 끝내지만, 실제 상태는 `online`을 유지합니다. `observationVersion`은 시간이 아니라 listener가 정보를 전달할 때마다 증가하는 숫자입니다. 같은 연결 상태가 다시 전달돼도 증가합니다.

`cleanup()`은 이 수명을 끝냅니다. 먼저 `currentSession`을 비워 이전 callback이 더는 현재 상태를 바꾸지 못하게 하고, 안내 타이머·재확인 대기·listener를 정리합니다. 실제 상태와 확인 진행 상태도 초기값으로 돌립니다. 이 함수는 `overrideStatus`는 초기화하지 않습니다.

**파일 아래쪽은 같은 Store를 목적에 맞게 읽는 진입점입니다.**

[읽기 API](/private/tmp/0402-network-body-20261022/r63/code/network.ts:258)는 별도 네트워크 상태를 만들지 않습니다.

- `networkStore`: React 밖에서 현재 값을 읽거나 `init`, `refresh`, `cleanup`을 호출합니다. getter로 값을 읽는 것 자체가 화면 구독을 만들지는 않습니다.
- `useRealNetworkStatus()`: 화면이 실제 상태 변경을 구독합니다.
- `useDisplayNetworkStatus()`: 화면이 `overrideStatus ?? realStatus`를 구독합니다. 강제 값이 있으면 그 값을 표시합니다.
- `useNetworkCheck()`: 확인 안내·재확인 진행 여부·재확인 함수를 화면에 줍니다.
- `useNetworkControl()`: debug의 강제 online/offline/unknown 설정과 해제를 제공합니다.

예를 들어 실제로 `offline`인데 debug에서 `online`을 설정하면 `useDisplayNetworkStatus()`는 `online`, `useRealNetworkStatus()`와 `networkStore.realStatus`는 `offline`입니다. 제공된 소비 코드에서도 헤더는 표시용 훅을 사용하고, debug Dashboard는 실제 상태·표시 상태·확인 안내를 각각 읽습니다. 이 파일은 그 값을 제공하며 실제 서버 요청이나 sync 실행 자체는 수행하지 않습니다.
