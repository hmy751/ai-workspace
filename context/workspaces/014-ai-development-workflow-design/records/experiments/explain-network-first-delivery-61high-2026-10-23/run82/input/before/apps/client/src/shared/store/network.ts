import { create, type StoreApi } from 'zustand';
import NetInfo, { type NetInfoState, type NetInfoSubscription } from '@react-native-community/netinfo';

export type NetworkStatus = 'online' | 'offline' | 'unknown';
export type NetworkCheckStatus = 'idle' | 'checking' | 'unavailable';

const CHECK_NOTICE_DELAY = 10_000;
const REFRESH_WAIT_LIMIT = 10_000;

/** 인터넷 도달 여부가 미확정인 값을 연결 실패로 추정하지 않는다. */
export function resolveNetworkStatus(state: Pick<NetInfoState, 'isConnected' | 'isInternetReachable'>): NetworkStatus {
  if (state.isConnected === false || state.isInternetReachable === false) {
    return 'offline';
  }

  if (state.isConnected === true && state.isInternetReachable === true) {
    return 'online';
  }

  return 'unknown';
}

interface NetworkState {
  realStatus: NetworkStatus;
  overrideStatus: NetworkStatus | null;
  checkStatus: NetworkCheckStatus;
  isRefreshing: boolean;

  init: () => void;
  cleanup: () => void;
  refresh: () => Promise<void>;
  setOverride: (status: NetworkStatus | null) => void;
}

interface NetworkRefreshRequest {
  promise: Promise<void>;
  accept: (state: NetInfoState) => void;
  fail: () => void;
  finish: () => void;
}

interface NetworkSession {
  unsubscribe: NetInfoSubscription | null;
  noticeTimer: ReturnType<typeof setTimeout> | null;
  observationVersion: number;
  refreshRequest: NetworkRefreshRequest | null;
}

export const useNetworkStore = create<NetworkState>((set, get) => ({
  realStatus: 'unknown',
  overrideStatus: null,
  checkStatus: 'checking',
  isRefreshing: false,

  ...createNetworkActions(set, get),
  setOverride: (status) => set({ overrideStatus: status }),
}));

function clearNoticeTimer(session: NetworkSession) {
  if (session.noticeTimer !== null) {
    clearTimeout(session.noticeTimer);
  }

  session.noticeTimer = null;
}

function createNetworkActions(
  set: StoreApi<NetworkState>['setState'],
  get: StoreApi<NetworkState>['getState'],
): Pick<NetworkState, 'init' | 'cleanup' | 'refresh'> {
  let currentSession: NetworkSession | null = null;

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

  function cleanup() {
    const session = currentSession;
    currentSession = null;

    if (session) {
      clearNoticeTimer(session);
      session.refreshRequest?.finish();
      session.unsubscribe?.();
    }

    set({ realStatus: 'unknown', checkStatus: 'checking', isRefreshing: false });
  }

  function refresh(): Promise<void> {
    init();

    const session = currentSession;

    if (!session) {
      return Promise.resolve();
    }

    if (session.refreshRequest) {
      return session.refreshRequest.promise;
    }

    if (get().realStatus === 'unknown') {
      beginUnknownCheck(session);
    }

    if (!subscribe(session)) {
      return Promise.resolve();
    }

    const request = startRefreshRequest(session);

    try {
      NetInfo.refresh().then(request.accept, request.fail);
    } catch {
      request.fail();
    }

    return request.promise;
  }

  function markUnavailable(session: NetworkSession) {
    if (currentSession !== session || get().realStatus !== 'unknown') {
      return;
    }

    clearNoticeTimer(session);

    if (get().checkStatus === 'unavailable') {
      return;
    }

    set({ checkStatus: 'unavailable' });
  }

  function beginUnknownCheck(session: NetworkSession) {
    clearNoticeTimer(session);
    session.noticeTimer = setTimeout(() => markUnavailable(session), CHECK_NOTICE_DELAY);
    set({ realStatus: 'unknown', checkStatus: 'checking' });
  }

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

  function subscribe(session: NetworkSession): boolean {
    if (session.unsubscribe) {
      return true;
    }

    try {
      // 등록 자체가 첫 상태를 조회하므로 앱의 추가 fetch는 사용하지 않는다.
      session.unsubscribe = NetInfo.addEventListener((state) => {
        if (currentSession !== session) {
          return;
        }

        session.observationVersion += 1;
        applyObservation(session, state);
      });

      return true;
    } catch {
      markUnavailable(session);
      return false;
    }
  }

  function startRefreshRequest(session: NetworkSession): NetworkRefreshRequest {
    const startingObservationVersion = session.observationVersion;
    let resolveRefresh!: () => void;

    const promise = new Promise<void>((resolvePromise) => {
      resolveRefresh = resolvePromise;
    });

    function canApplyResult() {
      return (
        currentSession === session &&
        session.refreshRequest === request &&
        session.observationVersion === startingObservationVersion
      );
    }

    function finish() {
      clearTimeout(timeout);

      if (session.refreshRequest === request) {
        session.refreshRequest = null;

        if (currentSession === session) {
          set({ isRefreshing: false });
        }
      }

      resolveRefresh();
    }

    const request: NetworkRefreshRequest = {
      promise,
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
      finish,
    };

    session.refreshRequest = request;
    // 미응답 요청의 앱 대기만 해제한다. 늦은 실측은 기존 listener로 받는다.
    const timeout = setTimeout(request.fail, REFRESH_WAIT_LIMIT);
    set({ isRefreshing: true });

    return request;
  }

  return { init, cleanup, refresh };
}

/** 비React 실행 판단은 화면용 override를 사용하지 않는다. */
export const networkStore = {
  get realStatus() {
    return useNetworkStore.getState().realStatus;
  },
  get override() {
    return useNetworkStore.getState().overrideStatus;
  },
  setOverride(status: NetworkStatus | null) {
    useNetworkStore.getState().setOverride(status);
  },
  init() {
    useNetworkStore.getState().init();
  },
  cleanup() {
    useNetworkStore.getState().cleanup();
  },
  refresh() {
    return useNetworkStore.getState().refresh();
  },
};

/** 화면 표시·제한 시뮬레이션용. 실제 요청 판단에는 사용하지 않는다. */
export function useDisplayNetworkStatus(): NetworkStatus {
  return useNetworkStore((state) => state.overrideStatus ?? state.realStatus);
}

export function useRealNetworkStatus(): NetworkStatus {
  return useNetworkStore((state) => state.realStatus);
}

export function useNetworkCheck() {
  const checkStatus = useNetworkStore((state) => state.checkStatus);
  const isRefreshing = useNetworkStore((state) => state.isRefreshing);
  const refresh = useNetworkStore((state) => state.refresh);

  return { checkStatus, isRefreshing, refresh };
}

export function useNetworkControl() {
  const overrideStatus = useNetworkStore((state) => state.overrideStatus);
  const setOverride = useNetworkStore((state) => state.setOverride);

  return {
    overrideStatus,
    setOverrideOnline: () => setOverride('online'),
    setOverrideOffline: () => setOverride('offline'),
    setOverrideUnknown: () => setOverride('unknown'),
    clearOverride: () => setOverride(null),
  };
}
