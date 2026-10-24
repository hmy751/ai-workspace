import React from 'react';
import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import { act, renderHook } from '@testing-library/react-native';

import { networkStore, useNetworkStore } from '@/shared/store/network';
import { SyncProvider, useSyncContext } from '@/shared/services/sync/provider';
import { syncData } from '@/shared/services/sync/engine';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));

jest.mock('@/shared/services/sync/engine', () => ({ syncData: jest.fn() }));

const syncMock = jest.mocked(syncData);

function SyncWrapper({ children }: { children: React.ReactNode }) {
  return <SyncProvider>{children}</SyncProvider>;
}

beforeEach(() => {
  useNetworkStore.setState({ realStatus: 'unknown', overrideStatus: null });
  syncMock.mockResolvedValue(undefined);
  jest.spyOn(console, 'log').mockImplementation(() => undefined);
});

afterEach(() => {
  networkStore.cleanup();
  jest.restoreAllMocks();
});

describe('SyncProvider의 실제 네트워크 소비', () => {
  it('실제 online으로 mount하면 한 번 시작한다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    const initialSync = Promise.resolve();
    syncMock.mockReturnValueOnce(initialSync);
    renderHook(() => useSyncContext(), { wrapper: SyncWrapper });

    await act(async () => {
      await initialSync;
    });

    expect(syncMock).toHaveBeenCalledTimes(1);
  });

  it.each(['unknown', 'offline'] as const)(
    '초기 %s에서는 전송하지 않고 실제 online 확정 뒤 한 번 시작한다',
    async (realStatus) => {
      useNetworkStore.setState({ realStatus });
      renderHook(() => useSyncContext(), { wrapper: SyncWrapper });

      expect(syncMock).not.toHaveBeenCalled();

      await act(async () => {
        useNetworkStore.setState({ realStatus: 'online' });
      });

      expect(syncMock).toHaveBeenCalledTimes(1);
    },
  );

  it('online의 일반 rerender와 sync 진행·완료에 따른 실행 함수 변경은 자동 sync를 반복하지 않는다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    let finishSync!: () => void;
    syncMock.mockReturnValueOnce(
      new Promise<void>((resolve) => {
        finishSync = resolve;
      }),
    );
    const { result, rerender } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });

    expect(result.current.isSyncing).toBe(true);
    expect(syncMock).toHaveBeenCalledTimes(1);

    rerender({});

    expect(syncMock).toHaveBeenCalledTimes(1);

    await act(async () => {
      finishSync();
    });

    expect(result.current.isSyncing).toBe(false);
    expect(syncMock).toHaveBeenCalledTimes(1);

    rerender({});
    rerender({});

    expect(syncMock).toHaveBeenCalledTimes(1);
  });

  it('화면 강제 online은 unknown의 수동 sync나 실제 online 전환의 자동 sync를 열지 않는다', async () => {
    networkStore.setOverride('online');
    const { result } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });

    await act(async () => {
      await result.current.triggerManualSync();
      useNetworkStore.setState({ realStatus: 'online' });
    });

    expect(syncMock).not.toHaveBeenCalled();
  });

  it('실제 online이어도 override 중 전송하지 않고 해제 뒤 수동 실행할 수 있다', async () => {
    useNetworkStore.setState({ realStatus: 'online', overrideStatus: 'unknown' });
    const { result } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });

    await act(async () => {
      await result.current.triggerManualSync();
    });

    expect(syncMock).not.toHaveBeenCalled();

    await act(async () => {
      networkStore.setOverride(null);
      await result.current.triggerManualSync();
    });

    expect(syncMock).toHaveBeenCalledTimes(1);
  });
});
