import React from 'react';
import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import { act, renderHook, waitFor } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import apiClient from '@/shared/api/fetcher';
import { useLocationSearch } from '@/features/schedule/create-schedule/useLocationSearch';
import { networkStore, useNetworkStore } from '@/shared/store/network';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/shared/api/fetcher', () => ({ __esModule: true, default: { post: jest.fn(), get: jest.fn() } }));
jest.mock('@/shared/hooks/useDebounce', () => ({ useDebounce: (value: unknown) => value }));

const postMock = jest.mocked(apiClient.post);
const getMock = jest.mocked(apiClient.get);
const response = { data: { results: [{ id: 'place', placeId: 'place', name: 'Place', address: 'Address' }] } };
let client: QueryClient;

function Wrapper({ children }: { children: React.ReactNode }) {
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

beforeEach(() => {
  client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: 0 } } });
  useNetworkStore.setState({ realStatus: 'unknown', overrideStatus: null });
  postMock.mockResolvedValue(response);
  getMock.mockResolvedValue({ id: 'place', name: 'Place', address: 'Address', latitude: 1, longitude: 2 });
});

afterEach(() => {
  client.clear();
  networkStore.cleanup();
  jest.restoreAllMocks();
});

describe('장소 검색의 실제 네트워크 요청 경계', () => {
  it.each(['unknown', 'offline'] as const)('강제 online이어도 실제 %s에서는 검색 요청을 시작하지 않는다', async (realStatus) => {
    useNetworkStore.setState({ realStatus, overrideStatus: 'online' });
    const { result } = renderHook(() => useLocationSearch(), { wrapper: Wrapper });
    await act(async () => result.current.handleSearch('Paris'));
    expect(postMock).not.toHaveBeenCalled();
    expect(getMock).not.toHaveBeenCalled();
    expect(result.current.searchQuery).toBe('Paris');
  });

  it('offline 동안 입력과 캐시는 유지하면서 이전 결과의 서비스 접근을 제한한다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    const { result } = renderHook(() => useLocationSearch(), { wrapper: Wrapper });
    act(() => result.current.handleSearch('Paris'));
    await waitFor(() => expect(result.current.results).toHaveLength(1));
    const cached = client.getQueryCache().getAll()[0].state.data;
    act(() => useNetworkStore.setState({ realStatus: 'offline' }));
    expect(result.current.results).toEqual([]);
    expect(result.current.searchQuery).toBe('Paris');
    expect(client.getQueryCache().getAll()[0].state.data).toBe(cached);
    expect(postMock).toHaveBeenCalledTimes(1);
  });

  it('검색 전송 뒤 unknown 관측이 오면 후속 상세 요청을 새로 시작하지 않는다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    let resolveSearch!: (value: typeof response) => void;
    postMock.mockReturnValueOnce(new Promise((resolve) => { resolveSearch = resolve; }));
    const { result } = renderHook(() => useLocationSearch(), { wrapper: Wrapper });
    act(() => result.current.handleSearch('Paris'));
    await waitFor(() => expect(postMock).toHaveBeenCalledTimes(1));
    await act(async () => {
      useNetworkStore.setState({ realStatus: 'unknown' });
      resolveSearch(response);
    });
    await waitFor(() => expect(client.isFetching()).toBe(0));
    expect(getMock).not.toHaveBeenCalled();
    expect(result.current.searchQuery).toBe('Paris');
  });
});
