import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import { getDirections } from '@/shared/services/directions/mapbox';
import { networkStore, useNetworkStore } from '@/shared/store/network';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));

const originalFetch = global.fetch;
const tokenKey = 'EXPO_PUBLIC_MAPBOX_PUBLIC_ACCESS_TOKEN';
const originalToken = process.env[tokenKey];
const fetchMock = jest.fn<typeof fetch>();
const coordinates = { from: { latitude: 1, longitude: 2 }, to: { latitude: 3, longitude: 4 } };

beforeEach(() => {
  useNetworkStore.setState({ realStatus: 'unknown', overrideStatus: null });
  process.env[tokenKey] = 'fixture-token';
  global.fetch = fetchMock;
  fetchMock.mockResolvedValue({
    ok: true,
    json: async () => ({ code: 'Ok', routes: [{ geometry: 'route', distance: 10, duration: 20 }] }),
  } as Response);
  jest.spyOn(console, 'log').mockImplementation(() => undefined);
  jest.spyOn(console, 'error').mockImplementation(() => undefined);
});

afterEach(() => {
  global.fetch = originalFetch;
  if (originalToken === undefined) delete process.env[tokenKey];
  else process.env[tokenKey] = originalToken;
  networkStore.cleanup();
  jest.restoreAllMocks();
});

describe('길찾기의 실제 네트워크 요청 경계', () => {
  it.each(['unknown', 'offline'] as const)('강제 online이어도 실제 %s에서는 HTTP를 시작하지 않는다', async (realStatus) => {
    useNetworkStore.setState({ realStatus, overrideStatus: 'online' });
    await expect(getDirections(coordinates)).rejects.toMatchObject({ name: 'PolicyError' });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('실제 online에서는 화면 override와 관계없이 조회할 수 있다', async () => {
    useNetworkStore.setState({ realStatus: 'online', overrideStatus: 'offline' });
    await expect(getDirections(coordinates)).resolves.toEqual({ geometry: 'route', distance: 10, duration: 20 });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('서버 오류가 실제 네트워크 관측을 offline으로 바꾸지 않는다', async () => {
    useNetworkStore.setState({ realStatus: 'online' });
    fetchMock.mockResolvedValueOnce({ ok: false, status: 503, statusText: 'Unavailable' } as Response);
    await expect(getDirections(coordinates)).rejects.toThrow('HTTP 503');
    expect(networkStore.realStatus).toBe('online');
  });
});
