import React from 'react';
import { act, renderHook, waitFor } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useGetTrips } from '@/entities/trip/data/useGetTrips';
import { TripRepository } from '@/entities/trip/repository/trip-repository';
import { networkStore, useNetworkStore } from '@/shared/store/network';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/entities/trip/repository/trip-repository', () => ({ TripRepository: { getAll: jest.fn() } }));

const getAll = jest.mocked(TripRepository.getAll);
let client: QueryClient;
function Wrapper({ children }: { children: React.ReactNode }) {
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

beforeEach(() => {
  getAll.mockReset();
  client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: 0, refetchOnReconnect: false } } });
  useNetworkStore.setState({ realStatus: 'unknown', overrideStatus: null });
});
afterEach(() => { client.clear(); networkStore.cleanup(); });

it('초기 unknown에서 실패한 목록은 실제 online 관측 후 다시 조회한다', async () => {
  getAll.mockRejectedValueOnce(new Error('아직 연결을 확인하지 못했어요')).mockResolvedValueOnce([]);
  const { result } = renderHook(() => { const query = useGetTrips(); return { isError: query.isError, isSuccess: query.isSuccess }; }, { wrapper: Wrapper });
  await waitFor(() => expect(result.current.isError).toBe(true));
  act(() => networkStore.setOverride('online'));
  expect(getAll).toHaveBeenCalledTimes(1);
  act(() => useNetworkStore.setState({ realStatus: 'online' }));
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(getAll).toHaveBeenCalledTimes(2);
});

it('실제 offline→online 전환은 이미 전송한 목록 조회를 취소하거나 중복 전송하지 않는다', async () => {
  useNetworkStore.setState({ realStatus: 'online' });
  let finish!: (value: Awaited<ReturnType<typeof TripRepository.getAll>>) => void;
  getAll.mockReturnValueOnce(new Promise((resolve) => { finish = resolve; }));
  const { result } = renderHook(() => { const query = useGetTrips(); return { isSuccess: query.isSuccess }; }, { wrapper: Wrapper });
  await waitFor(() => expect(getAll).toHaveBeenCalledTimes(1));
  act(() => useNetworkStore.setState({ realStatus: 'offline' }));
  act(() => useNetworkStore.setState({ realStatus: 'online' }));
  await act(async () => finish([]));
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(getAll).toHaveBeenCalledTimes(1);
});
