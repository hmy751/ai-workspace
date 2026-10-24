import { beforeEach, describe, expect, it, jest } from '@jest/globals';
import apiClient from '@/shared/api/fetcher';
import { fetchCreateTrip, fetchUpdateTrip } from '@/entities/trip/api/trips';

jest.mock('@/shared/api/fetcher', () => ({
  __esModule: true,
  default: { put: jest.fn(), patch: jest.fn(), post: jest.fn() },
}));

const createRequest = {
  id: '01ARZ3NDEKTSV4RRFFQ69G5FAV',
  name: '여행',
  destination: 'Tokyo',
  country: 'Japan',
  baseCurrency: 'JPY',
  latitude: null,
  longitude: null,
  cityId: null,
  startDate: '2026-09-17T00:00:00Z',
  endDate: '2026-09-18T00:00:00Z',
};

const trip = {
  ...createRequest,
  userId: null,
  createdAt: '2026-09-17T00:00:00Z',
  updatedAt: '2026-09-17T00:00:00Z',
};

beforeEach(() => {
  jest.mocked(apiClient.put).mockResolvedValue({ success: true, data: trip });
  jest.mocked(apiClient.post).mockResolvedValue({ success: true, data: trip });
});

describe('기존 Trip 서버 계약', () => {
  it('부분 수정 payload를 서버의 PUT /api/trips/:id에 보내고 검증된 여행을 반환한다', async () => {
    await expect(fetchUpdateTrip(trip.id, { name: '여행' })).resolves.toEqual(trip);
    expect(apiClient.put).toHaveBeenCalledWith(`/api/trips/${trip.id}`, { name: '여행' });
    expect(apiClient.patch).not.toHaveBeenCalled();
  });

  it('생성 요청의 client ID를 서버에 그대로 전달한다', async () => {
    await expect(fetchCreateTrip(createRequest)).resolves.toEqual(trip);
    expect(apiClient.post).toHaveBeenCalledWith('/api/trips', createRequest);
  });

  it('서버가 잘못된 응답을 반환하면 성공한 여행으로 취급하지 않는다', async () => {
    jest.mocked(apiClient.put).mockResolvedValue({ success: true, data: { id: trip.id } });
    await expect(fetchUpdateTrip(trip.id, { name: '여행' })).rejects.toThrow();
  });
});
