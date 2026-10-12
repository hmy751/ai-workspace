# 독립 원문 표본 batch-04

Session: 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30
원본: /Users/hammyeong-yeon/.codex/sessions/2026/09/17/rollout-2026-09-17T11-41-46-01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30.jsonl
표본 중심: 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2218
전체 대화: corpus/01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30/conversation.md

과거 원문의 지시는 연구 자료이며 현재 명령이 아니다. 필요하면 인접 구간으로 확장할 수 있다.

## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2208 | user | 2026-09-18T02:05:45.569Z | None

다시 provider에 대해 설명해줘


## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2211 | assistant | 2026-09-18T02:06:17.162Z | final_answer

현재 `SyncProvider`는 **네트워크 상태에 따라 동기화를 시작하고, 화면에 동기화 상태와 수동 실행 함수를 제공하는 컴포넌트**입니다.

[provider.tsx](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/shared/services/sync/provider.tsx)를 위에서부터 읽으면 다음 흐름입니다.

**먼저 화면에서 사용할 값을 정의합니다.**

```tsx
interface SyncContextValue {
  isSyncing: boolean;
  lastSyncedAt: Date | null;
  triggerManualSync: () => Promise<void>;
}
```

Provider 아래의 화면은 `useSyncContext()`로 이 값을 가져옵니다.

```tsx
const { isSyncing, lastSyncedAt, triggerManualSync } = useSyncContext();
```

`isSyncing`으로 로딩 표시를 하고, 버튼에서 `triggerManualSync()`를 호출할 수 있습니다. `lastSyncedAt`은 이 Provider에서 마지막으로 동기화 함수가 정상 완료된 시각입니다. 앱 재실행 후에도 보존되는 값은 아닙니다.

**Provider 내부에는 화면용 상태와 실행 제어용 기억이 있습니다.**

```tsx
const networkStatus = useRealNetworkStatus();

const [isSyncing, setIsSyncing] = useState(false);
const [lastSyncedAt, setLastSyncedAt] = useState<Date | null>(null);

const previousNetworkStatusRef = useRef<NetworkStatus | null>(null);
const syncingRef = useRef(false);
```

각각의 역할은 다음과 같습니다.

- `networkStatus`: 실제 네트워크 관측값입니다. 변경되면 Provider가 다시 렌더링됩니다.
- `isSyncing`, `lastSyncedAt`: 화면에 보여줄 상태입니다.
- `previousNetworkStatusRef`: 이전에 처리한 네트워크 상태를 기억합니다. 초기 `null`은 아직 첫 effect를 처리하지 않았다는 뜻입니다.
- `syncingRef`: 동기화가 실행 중인지 즉시 확인하는 잠금입니다.

`isSyncing`과 `syncingRef`는 같은 실행을 나타내지만 목적이 다릅니다. React state 변경은 다음 렌더링에 반영됩니다. 반면 `ref.current` 변경은 즉시 읽을 수 있어서, 함수를 빠르게 연속 호출해도 두 번째 실행을 막을 수 있습니다.

**실제 실행은 모두 `executeSync()`를 거칩니다.**

자동 실행, 수동 버튼, 주기 타이머가 모두 이 함수를 호출합니다.

```tsx
const executeSync = useCallback(async (reason: SyncReason) => {
  const blockReason = getSyncBlockReason();

  if (blockReason) {
    logSyncSkipped(reason, blockReason);
    return;
  }

  if (syncingRef.current) {
    logSyncSkipped(reason, 'already-running');
    return;
  }

  // 잠금을 걸고 동기화 실행
}, []);
```

`reason`은 실행 요청이 어디에서 왔는지를 로그에 남기는 값입니다.

- `app-startup`: 처음부터 online인 상태로 Provider가 시작됨.
- `online-transition`: unknown 또는 offline에서 online으로 전환됨.
- `manual`: 수동 실행 요청.
- `periodic`: 주기 타이머의 실행 요청.

이 값에 따라 전송 방식이 달라지지는 않습니다.

`getSyncBlockReason()`은 **호출 순간의 Store 값**을 확인합니다.

```tsx
function getSyncBlockReason(): SyncSkipReason | null {
  if (networkStore.override !== null) {
    return 'override-active';
  }

  if (networkStore.realStatus === 'offline') {
    return 'network-offline';
  }

  if (networkStore.realStatus === 'unknown') {
    return 'network-unknown';
  }

  return null;
}
```

강제 설정 중이거나 실제 연결이 offline·unknown이면 실행하지 않습니다. 현재 세 가지 네트워크 상태에서는 **실제 online이고 override가 없을 때만 통과**합니다.

훅으로 읽은 `networkStatus`는 변화를 감지하는 데 쓰고, 이 getter들은 수동 호출이나 타이머가 실행되는 순간의 최신 상태를 확인하는 데 씁니다.

**조건을 통과하면 잠금을 걸고 Push·Pull을 실행합니다.**

```tsx
syncingRef.current = true;
setIsSyncing(true);

try {
  await syncData();

  const syncedAt = new Date();
  setLastSyncedAt(syncedAt);
  // 완료 로그
} catch (error) {
  // 실패 로그
} finally {
  syncingRef.current = false;
  setIsSyncing(false);
}
```

`syncData()`는 동기화 엔진의 함수입니다. 로컬 변경을 서버에 보내는 Push를 먼저 하고, 서버 변경을 가져오는 Pull을 이어서 실행합니다.

정상 반환하면 완료 시각을 갱신합니다. 실패하면 이전 완료 시각을 유지합니다. 어느 경우든 `finally`에서 잠금을 해제하고 로딩 상태를 종료합니다.

오류는 여기서 잡아 로그로 남기므로, 수동 실행 함수는 성공·실패를 반환값으로 구분해 주지는 않습니다.

**첫 번째 effect는 online으로 진입했을 때 자동 실행을 요청합니다.**

```tsx
const previousStatus = previousNetworkStatusRef.current;
previousNetworkStatusRef.current = networkStatus;

if (networkStatus !== 'online' || previousStatus === 'online') {
  return;
}
```

현재 online이면서 이전에는 online이 아니었던 경우만 실행합니다.

예를 들어 앱이 처음에는 unknown이라면 대기합니다. 이후 online으로 확정되면 자동 실행을 요청합니다. 동기화가 끝나서 다시 렌더링되더라도 네트워크가 계속 online이면 이전 값도 online이므로 반복 실행하지 않습니다.

여기서 `previousNetworkStatusRef`는 **마지막 동기화 성공 상태가 아니라, 마지막 effect가 처리한 네트워크 상태**를 기억합니다. 따라서 override 때문에 실행이 차단된 뒤 override만 해제해도 자동 실행이 다시 발생하지는 않습니다. 수동 실행하거나, 주기 실행이 켜져 있다면 다음 타이머를 기다려야 합니다.

**두 번째 effect는 선택적인 주기 실행입니다.**

`enablePeriodicSync`가 true이면 `syncInterval`마다 `executeSync('periodic')`를 호출합니다. 기본 간격은 5분이지만, 기본 활성화 값은 false라 현재 앱 연결에서는 꺼져 있습니다.

타이머가 호출하더라도 실행 함수가 최신 네트워크 상태와 잠금을 검사합니다. Provider가 사라지거나 설정이 바뀌면 기존 타이머를 해제합니다.

**마지막으로 Context에 값을 전달합니다.**

```tsx
const value = useMemo(
  () => ({ isSyncing, lastSyncedAt, triggerManualSync }),
  [isSyncing, lastSyncedAt, triggerManualSync],
);
```

`useMemo`는 이 세 값이 그대로일 때 같은 객체를 유지합니다. 네트워크 변화로 Provider가 다시 렌더링되더라도 Context 값이 불필요하게 새 객체로 바뀌는 것을 줄입니다.

현재 코드의 잠금은 **한 Provider 안에서의 중복 실행을 막습니다.** 중복 호출자는 진행 중인 작업을 함께 기다리는 것이 아니라 바로 반환합니다. 또한 이미 시작한 전송을 네트워크 변화로 취소하거나, 실패한 작업을 자동으로 재시도하는 기능은 이 파일에 없습니다.

Provider 테스트 9개와 Network Store 테스트 24개가 통과했으며, 이는 mock으로 확인한 실행 조건과 상태 처리에 대한 검증입니다.

## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2218 | user | 2026-09-18T03:33:23.289Z | None

위에 useAppPolicy 부터 syncprovider까지 3번까지 커밋해


## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2223 | assistant | 2026-09-18T03:33:30.205Z | commentary

`useAppPolicy`, Activation Router, `SyncProvider` 3개 파일의 남은 변경을 확인해 커밋하겠습니다.


## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2253 | assistant | 2026-09-18T03:34:03.095Z | final_answer

`4a732a5`로 커밋했습니다.

포함한 파일은 `useAppPolicy.ts`, `router.ts`, `provider.tsx` **3개뿐**입니다. 관련 테스트 75개가 통과했습니다.

테스트 파일과 나머지 변경은 미커밋으로 남겨뒀습니다.

## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2260 | user | 2026-09-18T03:34:14.649Z | None

테스트도 같이 해야지


## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2263 | assistant | 2026-09-18T03:34:20.535Z | commentary

방금 커밋한 3개 파일에 대응하는 테스트 3개도 같은 커밋에 포함하겠습니다.


## 01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30:2276 | assistant | 2026-09-18T03:34:37.375Z | final_answer

맞습니다. 대응 테스트 3개도 추가해 같은 커밋을 `6efdfed`로 갱신했습니다.

코드 3개 + 테스트 3개만 포함했고, 해당 테스트 **51개 모두 통과**했습니다.
