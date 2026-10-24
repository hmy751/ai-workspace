import React from 'react';
import { AppState, type AppStateStatus } from 'react-native';
import { act, render } from '@testing-library/react-native';
import { beforeEach, afterEach, describe, expect, it, jest } from '@jest/globals';
import RootLayout from '../../app/_layout';
import { initializeDatabase } from '@/shared/db';
import { useAuthStore } from '@/shared/store/auth';
import { useTripStore } from '@/shared/store/useTripStore';
import { useGetTrips } from '@/entities/trip';
import { syncData } from '@/shared/services/sync/engine';
import { networkStore, useNetworkStore } from '@/shared/store/network';

jest.mock('../../styles/global.css', () => ({}));
jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/shared/services/auth/token-storage', () => ({}));
jest.mock('@/shared/db', () => ({ initializeDatabase: jest.fn() }));
jest.mock('@/shared/services/sync/engine', () => ({ syncData: jest.fn() }));
jest.mock('@/shared/services/sync/cleanup-job', () => ({ processPendingCleanups: jest.fn() }));
jest.mock('@/shared/services/offline-map', () => ({ useOfflineMapCleanup: jest.fn() }));
jest.mock('@/shared/components', () => ({ SessionExpiredBanner: () => null }));
jest.mock('@/shared/store', () => ({
  useTripStore:
    jest.requireActual<typeof import('@/shared/store/useTripStore')>('@/shared/store/useTripStore').useTripStore,
}));
jest.mock('@/entities/trip', () => ({ useGetTrips: jest.fn(), selectMainTrip: (trips: { id: string }[]) => trips[0] }));
jest.mock('@/shared/lib/queryClient', () => ({ queryClient: {} }));
jest.mock('@tanstack/react-query', () => ({
  QueryClientProvider: ({ children }: { children: React.ReactNode }) => children,
}));
jest.mock('react-native-safe-area-context', () => ({
  SafeAreaProvider: ({ children }: { children: React.ReactNode }) => children,
}));
jest.mock('@rn-primitives/portal', () => ({ PortalHost: () => null }));
jest.mock('expo-splash-screen', () => ({ preventAutoHideAsync: jest.fn(), hideAsync: jest.fn() }));
jest.mock('@rnmapbox/maps', () => ({ __esModule: true, default: { setAccessToken: jest.fn() } }));
jest.mock('expo-router', () => {
  const Stack = () => null;
  Stack.Screen = () => null;
  return { Stack, useRouter: () => ({ replace: jest.fn() }), useSegments: () => ['(tabs)'] };
});

const databaseMock = jest.mocked(initializeDatabase);
const syncMock = jest.mocked(syncData);
const tripsMock = jest.mocked(useGetTrips);

beforeEach(() => {
  jest.spyOn(networkStore, 'init').mockImplementation(() => undefined);
  jest.spyOn(networkStore, 'cleanup').mockImplementation(() => undefined);
  jest.spyOn(networkStore, 'refresh').mockResolvedValue(undefined);
  jest.spyOn(console, 'log').mockImplementation(() => undefined);
  jest.spyOn(console, 'error').mockImplementation(() => undefined);
  useNetworkStore.setState({ realStatus: 'online', overrideStatus: null });
  useAuthStore.setState({
    isInitialized: true,
    isAuthenticated: true,
    init: async () => {
      await Promise.resolve();
    },
  });
  useTripStore.setState({ selectedTripId: null });
  databaseMock.mockResolvedValue(undefined);
  syncMock.mockResolvedValue(undefined);
  tripsMock.mockReturnValue({ data: [{ id: 'default-trip' }] } as ReturnType<typeof useGetTrips>);
});
afterEach(() => {
  jest.restoreAllMocks();
});

describe('Root startup 소비 연결', () => {
  it('DB 초기화 실패로 Splash 대기를 끝내도 sync는 시작하지 않는다', async () => {
    databaseMock.mockRejectedValueOnce(new Error('database unavailable'));
    render(<RootLayout />);
    await act(async () => {
      await Promise.resolve();
    });
    expect(syncMock).not.toHaveBeenCalled();
  });

  it('DB 초기화 성공과 auth 준비 뒤 sync를 한 번 시작한다', async () => {
    let finishDatabase!: () => void;
    databaseMock.mockReturnValueOnce(
      new Promise<void>((resolve) => {
        finishDatabase = resolve;
      }),
    );
    render(<RootLayout />);
    expect(syncMock).not.toHaveBeenCalled();
    await act(async () => {
      finishDatabase();
    });
    expect(syncMock).toHaveBeenCalledTimes(1);
  });

  it('최초 기본 여행을 고른 뒤 사용자 선택은 trips 재조회에 유지된다', async () => {
    const screen = render(<RootLayout />);
    await act(async () => {
      await Promise.resolve();
    });
    expect(useTripStore.getState().selectedTripId).toBe('default-trip');
    act(() => {
      useTripStore.getState().setSelectedTripId('user-trip');
    });
    tripsMock.mockReturnValue({ data: [{ id: 'different-default' }] } as ReturnType<typeof useGetTrips>);
    screen.rerender(<RootLayout />);
    expect(useTripStore.getState().selectedTripId).toBe('user-trip');
  });

  it('background에서 active로 돌아오면 listener를 유지하며 한 번 refresh하고 정리한다', async () => {
    let onChange!: (state: AppStateStatus) => void;
    const remove = jest.fn();
    jest.spyOn(AppState, 'addEventListener').mockImplementation((_event, callback) => {
      onChange = callback;
      return { remove };
    });
    const screen = render(<RootLayout />);
    await act(async () => {
      await Promise.resolve();
    });
    act(() => {
      onChange('background');
      onChange('active');
      onChange('active');
    });
    expect(networkStore.refresh).toHaveBeenCalledTimes(1);
    expect(networkStore.cleanup).not.toHaveBeenCalled();
    screen.unmount();
    expect(remove).toHaveBeenCalledTimes(1);
    expect(networkStore.cleanup).toHaveBeenCalledTimes(1);
  });
});
