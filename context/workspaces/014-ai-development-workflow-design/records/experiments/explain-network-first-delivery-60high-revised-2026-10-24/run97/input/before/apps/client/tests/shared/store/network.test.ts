import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import NetInfo, {
  type NetInfoState,
  type NetInfoChangeHandler,
  NetInfoStateType,
} from '@react-native-community/netinfo';
import { act, renderHook } from '@testing-library/react-native';

import {
  networkStore,
  resolveNetworkStatus,
  useNetworkCheck,
  useDisplayNetworkStatus,
  useNetworkStore,
  useRealNetworkStatus,
  type NetworkStatus,
} from '@/shared/store/network';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: {
    addEventListener: jest.fn(),
    fetch: jest.fn(),
    refresh: jest.fn(),
  },
  NetInfoStateType: { unknown: 'unknown' },
}));

const addListenerMock = jest.mocked(NetInfo.addEventListener);
const refreshMock = jest.mocked(NetInfo.refresh);

let listeners: NetInfoChangeHandler[];
let unsubscribe: ReturnType<typeof jest.fn>;

function createObservation(isConnected: boolean | null, isInternetReachable: boolean | null): NetInfoState {
  return {
    type: NetInfoStateType.unknown,
    isConnected,
    isInternetReachable,
    details: null,
  } as NetInfoState;
}

function emit(isConnected: boolean | null, isInternetReachable: boolean | null) {
  listeners[listeners.length - 1](createObservation(isConnected, isInternetReachable));
}

function createDeferredObservation() {
  let resolve!: (state: NetInfoState) => void;
  let reject!: (error: Error) => void;

  const promise = new Promise<NetInfoState>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });

  return { promise, resolve, reject };
}

beforeEach(() => {
  jest.useFakeTimers();

  networkStore.cleanup();
  networkStore.setOverride(null);
  jest.resetAllMocks();

  listeners = [];
  unsubscribe = jest.fn();

  addListenerMock.mockImplementation((listener) => {
    listeners.push(listener);
    return unsubscribe;
  });
});

afterEach(() => {
  networkStore.cleanup();
  jest.useRealTimers();
});

describe('인터넷 연결 관측 변환', () => {
  it.each<[boolean | null, boolean | null, NetworkStatus]>([
    [true, true, 'online'],
    [true, false, 'offline'],
    [false, true, 'offline'],
    [false, false, 'offline'],
    [false, null, 'offline'],
    [null, false, 'offline'],
    [true, null, 'unknown'],
    [null, true, 'unknown'],
    [null, null, 'unknown'],
  ])('%s / %s → %s', (isConnected, isInternetReachable, expected) => {
    expect(resolveNetworkStatus({ isConnected, isInternetReachable })).toBe(expected);
  });
});

describe('Network Store 수명과 확인 안내', () => {
  it('최초 관측 전에는 unknown이며 중복 init이 listener나 앱 fetch를 추가하지 않는다', () => {
    expect(networkStore.realStatus).toBe('unknown');

    networkStore.init();
    networkStore.init();

    expect(addListenerMock).toHaveBeenCalledTimes(1);
    expect(NetInfo.fetch).not.toHaveBeenCalled();

    emit(true, true);

    expect(networkStore.realStatus).toBe('online');
  });

  it('같은 unknown을 반복해도 최초 10초 뒤 안내만 확인 불가로 바뀐다', () => {
    networkStore.init();

    jest.advanceTimersByTime(9_000);
    emit(true, null);

    expect(useNetworkStore.getState().checkStatus).toBe('checking');

    jest.advanceTimersByTime(1_000);

    expect(networkStore.realStatus).toBe('unknown');
    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');

    emit(null, null);

    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');

    emit(true, true);

    expect(networkStore.realStatus).toBe('online');
    expect(useNetworkStore.getState().checkStatus).toBe('idle');
  });

  it('등록 중 첫 관측이 동기적으로 도착해도 확인 timer를 남기지 않는다', () => {
    addListenerMock.mockImplementationOnce((listener) => {
      listeners.push(listener);
      listener(createObservation(true, true));
      return unsubscribe;
    });

    networkStore.init();

    expect(networkStore.realStatus).toBe('online');
    expect(useNetworkStore.getState().checkStatus).toBe('idle');
    expect(jest.getTimerCount()).toBe(0);
  });

  it('사용 중 다시 unknown이 되면 새 10초 안내를 시작한다', () => {
    networkStore.init();
    emit(true, true);
    jest.advanceTimersByTime(20_000);

    emit(true, null);

    expect(useNetworkStore.getState().checkStatus).toBe('checking');

    jest.advanceTimersByTime(10_000);

    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');
  });

  it('동일한 확정 관측은 Store 변경을 통지하지 않는다', () => {
    networkStore.init();
    emit(true, true);
    const onStoreChange = jest.fn();
    const unsubscribeStore = useNetworkStore.subscribe(onStoreChange);

    emit(true, true);

    expect(onStoreChange).not.toHaveBeenCalled();

    unsubscribeStore();
  });

  it('cleanup은 listener와 timer를 정리하고 이전 listener의 늦은 호출을 무시한다', () => {
    networkStore.init();
    const oldListener = listeners[0];

    networkStore.cleanup();
    networkStore.cleanup();

    expect(unsubscribe).toHaveBeenCalledTimes(1);
    expect(jest.getTimerCount()).toBe(0);

    networkStore.init();
    emit(false, false);
    oldListener(createObservation(true, true));

    expect(networkStore.realStatus).toBe('offline');
    expect(addListenerMock).toHaveBeenCalledTimes(2);
  });

  it('listener 등록 실패는 unknown으로 남고 재확인 때 다시 등록할 수 있다', async () => {
    addListenerMock.mockImplementationOnce(() => {
      throw new Error('등록 실패');
    });

    networkStore.init();

    expect(networkStore.realStatus).toBe('unknown');
    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');

    refreshMock.mockResolvedValue(createObservation(true, true));

    await networkStore.refresh();

    expect(addListenerMock).toHaveBeenCalledTimes(2);
    expect(networkStore.realStatus).toBe('online');
  });
});

describe('수동 재확인', () => {
  it('연타는 한 요청을 공유하며 완료 뒤 null을 online으로 추정하지 않는다', async () => {
    networkStore.init();
    const pendingRefreshResult = createDeferredObservation();
    refreshMock.mockReturnValue(pendingRefreshResult.promise);

    const firstRefresh = networkStore.refresh();

    expect(networkStore.refresh()).toBe(firstRefresh);
    expect(refreshMock).toHaveBeenCalledTimes(1);
    expect(useNetworkStore.getState().isRefreshing).toBe(true);

    pendingRefreshResult.resolve(createObservation(true, null));
    await firstRefresh;

    expect(networkStore.realStatus).toBe('unknown');
    expect(useNetworkStore.getState().isRefreshing).toBe(false);

    jest.advanceTimersByTime(10_000);

    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');

    emit(true, true);

    expect(networkStore.realStatus).toBe('online');
  });

  it('명시적 재확인만 unknown의 안내 시간을 다시 시작한다', async () => {
    networkStore.init();
    jest.advanceTimersByTime(10_000);
    refreshMock.mockResolvedValue(createObservation(null, null));

    await networkStore.refresh();

    expect(useNetworkStore.getState().checkStatus).toBe('checking');

    jest.advanceTimersByTime(9_000);
    emit(true, null);
    jest.advanceTimersByTime(1_000);

    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');
  });

  it('재확인 시작과 실패가 기존 확정 상태를 unknown/offline으로 초기화하지 않는다', async () => {
    networkStore.init();
    emit(true, true);
    refreshMock.mockRejectedValue(new Error('재확인 실패'));

    const promise = networkStore.refresh();

    expect(networkStore.realStatus).toBe('online');

    await promise;

    expect(networkStore.realStatus).toBe('online');
    expect(useNetworkStore.getState().checkStatus).toBe('idle');
  });

  it('unknown의 재확인 실패는 확인 불가를 안내하고 늦은 listener 결과는 수용한다', async () => {
    networkStore.init();
    refreshMock.mockRejectedValue(new Error('재확인 실패'));

    await networkStore.refresh();

    expect(networkStore.realStatus).toBe('unknown');
    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');
    expect(useNetworkStore.getState().isRefreshing).toBe(false);
    expect(jest.getTimerCount()).toBe(0);

    emit(false, null);

    expect(networkStore.realStatus).toBe('offline');
  });

  it('새 listener 관측 뒤 도착한 오래된 refresh 결과나 실패는 상태를 덮지 않는다', async () => {
    networkStore.init();
    const olderRefreshResult = createDeferredObservation();
    refreshMock.mockReturnValueOnce(olderRefreshResult.promise);

    const firstRefresh = networkStore.refresh();
    emit(true, true);
    olderRefreshResult.resolve(createObservation(false, false));
    await firstRefresh;

    expect(networkStore.realStatus).toBe('online');

    const failedRefreshResult = createDeferredObservation();
    refreshMock.mockReturnValueOnce(failedRefreshResult.promise);

    const secondRefresh = networkStore.refresh();
    emit(true, null);
    failedRefreshResult.reject(new Error('이전 확인 실패'));
    await secondRefresh;

    expect(useNetworkStore.getState().checkStatus).toBe('checking');
  });

  it('미응답 요청은 10초 뒤 해제되고 이전 응답이 다음 확인을 덮지 않는다', async () => {
    networkStore.init();
    const olderRefreshResult = createDeferredObservation();
    refreshMock.mockReturnValueOnce(olderRefreshResult.promise);

    const firstRefresh = networkStore.refresh();
    jest.advanceTimersByTime(10_000);
    await firstRefresh;

    expect(useNetworkStore.getState().isRefreshing).toBe(false);
    expect(useNetworkStore.getState().checkStatus).toBe('unavailable');

    const newerRefreshResult = createDeferredObservation();
    refreshMock.mockReturnValueOnce(newerRefreshResult.promise);
    const secondRefresh = networkStore.refresh();

    olderRefreshResult.resolve(createObservation(false, false));
    await olderRefreshResult.promise;

    expect(networkStore.realStatus).toBe('unknown');
    expect(useNetworkStore.getState().checkStatus).toBe('checking');
    expect(useNetworkStore.getState().isRefreshing).toBe(true);
    expect(networkStore.refresh()).toBe(secondRefresh);

    newerRefreshResult.resolve(createObservation(true, true));
    await secondRefresh;

    expect(refreshMock).toHaveBeenCalledTimes(2);
    expect(networkStore.realStatus).toBe('online');
    expect(useNetworkStore.getState().isRefreshing).toBe(false);
    expect(jest.getTimerCount()).toBe(0);
  });

  it('cleanup은 진행 중 확인을 해제하고 이전 확인 결과는 재초기화에 반영하지 않는다', async () => {
    networkStore.init();
    const olderRefreshResult = createDeferredObservation();
    refreshMock.mockReturnValueOnce(olderRefreshResult.promise);

    const promise = networkStore.refresh();
    networkStore.cleanup();
    await promise;

    expect(useNetworkStore.getState().isRefreshing).toBe(false);
    expect(jest.getTimerCount()).toBe(0);

    networkStore.init();
    emit(false, false);
    olderRefreshResult.resolve(createObservation(true, true));
    await olderRefreshResult.promise;

    expect(networkStore.realStatus).toBe('offline');
  });
});

describe('실제 관측과 화면 표시', () => {
  it('override는 화면 훅만 바꾸며 실제 실행 판단과 확인 안내는 유지한다', () => {
    networkStore.init();
    const { result } = renderHook(() => ({
      display: useDisplayNetworkStatus(),
      real: useRealNetworkStatus(),
      check: useNetworkCheck(),
    }));

    act(() => {
      emit(false, false);
      networkStore.setOverride('online');
    });

    expect(result.current.display).toBe('online');
    expect(result.current.real).toBe('offline');
    expect(networkStore.realStatus).toBe('offline');

    act(() => networkStore.setOverride('unknown'));

    expect(result.current.display).toBe('unknown');
    expect(result.current.check.checkStatus).toBe('idle');

    act(() => networkStore.setOverride(null));

    expect(result.current.display).toBe('offline');
  });
});
