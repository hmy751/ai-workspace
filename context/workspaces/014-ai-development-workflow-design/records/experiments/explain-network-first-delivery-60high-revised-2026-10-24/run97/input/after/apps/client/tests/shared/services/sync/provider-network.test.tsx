import React from 'react';
import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import { act, render, renderHook } from '@testing-library/react-native';

import { networkStore, useNetworkStore } from '@/shared/store/network';
import { SyncProvider, useSyncContext } from '@/shared/services/sync/provider';
import { useAuthStore } from '@/shared/store/auth';
import { syncData } from '@/shared/services/sync/engine';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));

jest.mock('@/shared/services/auth/token-storage', () => ({}));

jest.mock('@/shared/services/sync/engine', () => ({ syncData: jest.fn() }));

const syncMock = jest.mocked(syncData);

function SyncWrapper({ children }: { children: React.ReactNode }) {
  return <SyncProvider isDatabaseReady={true}>{children}</SyncProvider>;
}

beforeEach(() => {
  useNetworkStore.setState({ realStatus: 'unknown', overrideStatus: null });
  useAuthStore.setState({ isInitialized: true, isAuthenticated: true });
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

describe('SyncProvider 실행 경계', () => {
  it('같은 act의 연타와 이전 callback은 하나의 실행 완료를 기다린다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    const { result } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });
    await act(async () => {
      await Promise.resolve();
    });
    syncMock.mockClear();
    let finish!: () => void;
    syncMock.mockReturnValueOnce(
      new Promise<void>((resolve) => {
        finish = resolve;
      }),
    );
    const previousTrigger = result.current.triggerManualSync;
    let first!: ReturnType<typeof previousTrigger>;
    let second!: ReturnType<typeof previousTrigger>;
    let settled = false;
    act(() => {
      first = previousTrigger();
      second = previousTrigger();
      second.then(() => {
        settled = true;
      });
    });
    expect(syncMock).toHaveBeenCalledTimes(1);
    expect(settled).toBe(false);
    let third!: ReturnType<typeof previousTrigger>;
    act(() => {
      third = previousTrigger();
    });
    expect(syncMock).toHaveBeenCalledTimes(1);
    await act(async () => {
      finish();
      expect(await first).toMatchObject({ status: 'completed' });
      expect(await second).toMatchObject({ status: 'completed' });
      await third;
    });
    expect(settled).toBe(true);
  });

  it('실패를 반환하고 잠금을 해제해 다시 실행한다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    const { result } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });
    await act(async () => {
      await Promise.resolve();
    });
    syncMock.mockRejectedValueOnce(new Error('sync failure'));
    await act(async () => {
      expect(await result.current.triggerManualSync()).toMatchObject({ status: 'failed' });
    });
    expect(result.current.isSyncing).toBe(false);
    await act(async () => {
      expect(await result.current.triggerManualSync()).toMatchObject({ status: 'completed' });
    });
  });

  it.each(['isInitialized', 'isAuthenticated'] as const)(
    '%s가 false면 차단하고 준비 전환에서 시작한다',
    async (field) => {
      useNetworkStore.setState({ realStatus: 'online' });
      useAuthStore.setState({ [field]: false });
      const { result } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });
      await act(async () => {
        expect(await result.current.triggerManualSync()).toMatchObject({ status: 'blocked' });
      });
      expect(syncMock).not.toHaveBeenCalled();
      await act(async () => {
        useAuthStore.setState({ [field]: true });
      });
      expect(syncMock).toHaveBeenCalledTimes(1);
    },
  );

  it('DB 성공 전에는 차단하고 DB 사용 가능 전환에서 시작한다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    const { rerender } = render(<SyncProvider isDatabaseReady={false}>{null}</SyncProvider>);
    expect(syncMock).not.toHaveBeenCalled();
    await act(async () => {
      rerender(<SyncProvider isDatabaseReady={true}>{null}</SyncProvider>);
    });
    expect(syncMock).toHaveBeenCalledTimes(1);
  });

  it('override 해제는 자동 sync를 시작하며 겹친 수동 호출은 기다린다', async () => {
    useNetworkStore.setState({ realStatus: 'online', overrideStatus: 'offline' });
    let finish!: () => void;
    syncMock.mockReturnValueOnce(
      new Promise<void>((resolve) => {
        finish = resolve;
      }),
    );
    const { result } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });
    act(() => {
      networkStore.setOverride(null);
    });
    let manual!: ReturnType<typeof result.current.triggerManualSync>;
    act(() => {
      manual = result.current.triggerManualSync();
    });
    expect(syncMock).toHaveBeenCalledTimes(1);
    await act(async () => {
      finish();
      expect(await manual).toMatchObject({ status: 'completed' });
    });
  });
});

it('전송 시작 뒤 연결·override 변화는 진행 중 Promise를 취소하거나 새 실행을 시작하지 않는다', async () => {
  useNetworkStore.setState({ realStatus: 'online' });
  let finish!: () => void;
  syncMock.mockReturnValueOnce(
    new Promise<void>((resolve) => {
      finish = resolve;
    }),
  );
  const { result } = renderHook(() => useSyncContext(), { wrapper: SyncWrapper });
  let waiting!: ReturnType<typeof result.current.triggerManualSync>;
  act(() => {
    useNetworkStore.setState({ realStatus: 'offline', overrideStatus: 'online' });
    waiting = result.current.triggerManualSync();
  });
  expect(syncMock).toHaveBeenCalledTimes(1);
  expect(result.current.isSyncing).toBe(true);
  await act(async () => {
    finish();
    expect(await waiting).toMatchObject({ status: 'completed' });
  });
  await act(async () => {
    expect(await result.current.triggerManualSync()).toMatchObject({ status: 'blocked' });
  });
  expect(syncMock).toHaveBeenCalledTimes(1);
});
