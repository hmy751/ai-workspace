import React from 'react';
import { Alert } from 'react-native';
import { act, fireEvent, render } from '@testing-library/react-native';
import { beforeEach, afterEach, describe, expect, it, jest } from '@jest/globals';
import DebugScreen from '@/features/debug/ui/DebugScreen';
import { SyncProvider } from '@/shared/services/sync/provider';
import { useNetworkStore } from '@/shared/store/network';
import { useAuthStore } from '@/shared/store/auth';
import { syncData as runSyncData } from '@/shared/services/sync/engine';
import { db } from '@/shared/db';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/shared/services/auth/token-storage', () => ({}));
jest.mock('@/shared/services/sync/engine', () => {
  const engineRun = jest.fn<() => Promise<void>>();
  return {
    syncData: engineRun,
    triggerSync: async () => {
      try {
        await engineRun();
        return { success: true, message: '동기화가 완료되었습니다.' };
      } catch {
        return { success: false, message: '동기화에 실패했습니다.' };
      }
    },
  };
});
jest.mock('@/shared/services/sync/queue', () => ({
  getSyncQueueStats: jest.fn(async () => ({ pending: 0, inProgress: 0, failed: 0, total: 0 })),
}));
jest.mock('@/shared/db', () => ({ db: { select: jest.fn(() => ({ from: () => ({ all: async () => [] }) })) } }));
jest.mock('@/shared/components', () => {
  const { View } = jest.requireActual<typeof import('react-native')>('react-native');
  return { MobileHeader: () => null, Container: View, Stack: View };
});
jest.mock('@repo/ui', () => {
  const ReactRuntime = jest.requireActual<typeof import('react')>('react');
  const { Pressable, Text } = jest.requireActual<typeof import('react-native')>('react-native');
  return {
    Pressable: ({ children, ...props }: { children: React.ReactNode }) =>
      ReactRuntime.createElement(
        Pressable,
        props,
        typeof children === 'string' ? ReactRuntime.createElement(Text, null, children) : children,
      ),
  };
});
jest.mock('lucide-react-native', () => ({
  ArrowLeft: () => null,
  Database: () => null,
  Wifi: () => null,
  WifiOff: () => null,
  RotateCcw: () => null,
  RefreshCw: () => null,
  Upload: () => null,
}));
jest.mock('expo-router', () => ({ router: { back: jest.fn() } }));
jest.mock('@rnmapbox/maps', () => ({ __esModule: true, default: {} }));
jest.mock('@/features/debug/ui/DataInspectorView', () => ({ DataInspectorView: () => null }));
jest.mock('@/features/debug/ui/ToolsView', () => ({ ToolsView: () => null }));

const syncMock = jest.mocked(runSyncData);
const selectMock = jest.mocked(db.select);

beforeEach(() => {
  useNetworkStore.setState({ realStatus: 'unknown', overrideStatus: null });
  useAuthStore.setState({ isInitialized: true, isAuthenticated: true });
  syncMock.mockResolvedValue(undefined);
  jest.spyOn(Alert, 'alert').mockImplementation(() => undefined);
  jest.spyOn(console, 'log').mockImplementation(() => undefined);
});
afterEach(() => {
  jest.restoreAllMocks();
});

async function openDebug() {
  const screen = render(
    <SyncProvider isDatabaseReady={true}>
      <DebugScreen />
    </SyncProvider>,
  );
  await act(async () => {
    await Promise.resolve();
  });
  return screen;
}

describe('실제 DebugScreen → Dashboard 버튼 → Provider 실행 연결', () => {
  it.each([
    { realStatus: 'unknown', overrideStatus: null },
    { realStatus: 'offline', overrideStatus: 'online' },
    { realStatus: 'online', overrideStatus: 'offline' },
  ] as const)('차단 조건 $realStatus/$overrideStatus은 성공 안내와 재조회를 하지 않는다', async (state) => {
    useNetworkStore.setState(state);
    const screen = await openDebug();
    const initialReads = selectMock.mock.calls.length;
    await act(async () => {
      fireEvent.press(screen.getByText('전체 동기화 (Push + Pull)'));
    });
    expect(syncMock).not.toHaveBeenCalled();
    expect(Alert.alert).toHaveBeenCalledWith('동기화할 수 없습니다', expect.any(String));
    expect(selectMock).toHaveBeenCalledTimes(initialReads);
  });

  it('허용된 수동 완료 때 엔진을 실행하고 DB를 새로 읽은 뒤 성공을 안내한다', async () => {
    const screen = await openDebug();
    await act(async () => {
      useNetworkStore.setState({ realStatus: 'online' });
    });
    syncMock.mockClear();
    const initialReads = selectMock.mock.calls.length;
    await act(async () => {
      fireEvent.press(screen.getByText('전체 동기화 (Push + Pull)'));
    });
    expect(syncMock).toHaveBeenCalledTimes(1);
    expect(selectMock).toHaveBeenCalledTimes(initialReads + 6);
    expect(Alert.alert).toHaveBeenCalledWith('✅ 성공', '동기화가 완료되었습니다.');
  });

  it('엔진 reject는 실패 안내로 전달되고 성공 후 DB 재조회는 하지 않는다', async () => {
    const screen = await openDebug();
    await act(async () => {
      useNetworkStore.setState({ realStatus: 'online' });
    });
    syncMock.mockRejectedValueOnce(new Error('failed'));
    const initialReads = selectMock.mock.calls.length;
    await act(async () => {
      fireEvent.press(screen.getByText('전체 동기화 (Push + Pull)'));
    });
    expect(Alert.alert).toHaveBeenCalledWith('❌ 실패', '동기화에 실패했습니다.');
    expect(selectMock).toHaveBeenCalledTimes(initialReads);
  });
});
