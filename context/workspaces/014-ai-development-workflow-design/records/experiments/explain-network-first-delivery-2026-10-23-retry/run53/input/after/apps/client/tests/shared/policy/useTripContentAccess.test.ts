import { act, renderHook } from '@testing-library/react-native';
import { useTripContentAccess } from '@/shared/policy/useTripContentAccess';
import { useNetworkStore } from '@/shared/store/network';
import { useGetTripActivation } from '@/entities/trip/data/useGetTripActivation';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/entities/trip/data/useGetTripActivation', () => ({ useGetTripActivation: jest.fn() }));
const activation = jest.mocked(useGetTripActivation);
const success = { isError: false, error: null };
const deferred = () => {
  let resolve!: (value: typeof success) => void;
  const promise = new Promise<typeof success>((done) => {
    resolve = done;
  });
  return { promise, resolve };
};
const network = (realStatus: 'online' | 'offline' | 'unknown') => act(() => useNetworkStore.setState({ realStatus }));

beforeEach(() => {
  activation.mockReturnValue({ data: null } as ReturnType<typeof useGetTripActivation>);
  useNetworkStore.setState({ realStatus: 'online', overrideStatus: null, checkStatus: 'checking' });
});

it('남아 있는 서버 캐시는 offline/unknown에 제한하고, offline→unknown→online 재조회 성공 후 한 번 안내한다', async () => {
  const pending = deferred();
  const refetch = jest.fn(() => pending.promise);
  const query = { data: ['cached'], isLoading: false, isError: false, refetch };
  const { result, rerender } = renderHook(() => useTripContentAccess('b', query));
  expect(result.current.status).toBe('ready');
  network('offline');
  expect(result.current.status).toBe('restricted');
  network('unknown');
  expect(result.current.status).toBe('restricted');
  network('online');
  expect(result.current.status).toBe('loading');
  expect(refetch).toHaveBeenCalledTimes(1);
  await act(async () => {
    pending.resolve(success);
    await pending.promise;
  });
  expect(result.current.status).toBe('ready');
  expect(result.current.notice).toContain('복구');
  rerender({});
  network('online');
  expect(refetch).toHaveBeenCalledTimes(1);
  expect(query.data).toEqual(['cached']);
});

it('초기 unknown 해소와 단순 online 재확인은 복구 안내를 만들지 않는다', async () => {
  useNetworkStore.setState({ realStatus: 'unknown' });
  const refetch = jest.fn(async () => success);
  const { result } = renderHook(() => useTripContentAccess('b', { isLoading: false, isError: false, refetch }));
  await act(async () => {
    useNetworkStore.setState({ realStatus: 'online' });
  });
  expect(result.current.status).toBe('ready');
  expect(result.current.notice).toBeNull();
  network('online');
  expect(refetch).toHaveBeenCalledTimes(1);
});

it('복구 조회 실패는 빈 결과와 구별하고 사용자 재시도 성공 후 내용을 연다', async () => {
  const refetch = jest
    .fn()
    .mockResolvedValueOnce({ isError: true, error: new Error('server') })
    .mockResolvedValueOnce(success);
  const { result } = renderHook(() => useTripContentAccess('b', { isLoading: false, isError: false, refetch }));
  network('offline');
  await act(async () => {
    useNetworkStore.setState({ realStatus: 'online' });
  });
  expect(result.current.status).toBe('error');
  expect(result.current.notice).toBeNull();
  await act(async () => result.current.retry());
  expect(result.current.status).toBe('ready');
  expect(result.current.notice).toContain('복구');
});

it('다른 여행으로 옮긴 뒤 이전 복구 결과는 현재 내용이나 안내를 바꾸지 않는다', async () => {
  const pending = deferred();
  const refetch = jest.fn(() => pending.promise);
  const { result, rerender } = renderHook(
    ({ tripId }: { tripId: string }) => useTripContentAccess(tripId, { isLoading: false, isError: false, refetch }),
    { initialProps: { tripId: 'b' } },
  );
  network('offline');
  network('online');
  rerender({ tripId: 'a' });
  await act(async () => {
    pending.resolve(success);
    await pending.promise;
  });
  expect(result.current.status).toBe('ready');
  expect(result.current.notice).toBeNull();
  expect(refetch).toHaveBeenCalledTimes(1);
});

it('복구 대기 중 다시 끊기면 이전 응답을 무시하고 새 online에서 새 조회만 복구한다', async () => {
  const first = deferred();
  const second = deferred();
  const refetch = jest.fn().mockReturnValueOnce(first.promise).mockReturnValueOnce(second.promise);
  const { result } = renderHook(() => useTripContentAccess('b', { isLoading: false, isError: false, refetch }));
  network('offline');
  network('online');
  network('unknown');
  await act(async () => {
    first.resolve(success);
    await first.promise;
  });
  expect(result.current.status).toBe('restricted');
  network('online');
  await act(async () => {
    second.resolve(success);
    await second.promise;
  });
  expect(result.current.status).toBe('ready');
  expect(refetch).toHaveBeenCalledTimes(2);
});

it.each(['online', 'offline', 'unknown'] as const)(
  '활성 Local 여행은 %s에서도 내용과 선택을 유지한다',
  (realStatus) => {
    activation.mockReturnValue({ data: { isActivated: true } } as ReturnType<typeof useGetTripActivation>);
    useNetworkStore.setState({ realStatus });
    const refetch = jest.fn(async () => success);
    const { result } = renderHook(() => useTripContentAccess('a', { isLoading: false, isError: false, refetch }));
    expect(result.current.status).toBe('ready');
    expect(refetch).not.toHaveBeenCalled();
  },
);

it.each([
  { isLoading: true, isError: false, status: 'loading' },
  { isLoading: false, isError: true, status: 'error' },
  { isLoading: false, isError: false, status: 'ready' },
])('일반 로딩/오류/성공한 빈 결과를 구별한다: $status', ({ isLoading, isError, status }) => {
  const { result } = renderHook(() =>
    useTripContentAccess('b', { isLoading, isError, refetch: jest.fn(async () => success) }),
  );
  expect(result.current.status).toBe(status);
});
