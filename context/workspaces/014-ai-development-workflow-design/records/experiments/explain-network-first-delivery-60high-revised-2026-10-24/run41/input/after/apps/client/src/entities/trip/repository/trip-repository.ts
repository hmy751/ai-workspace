// ========================================
// Trip Repository - 활성화 상태에 따른 Local/Remote 분기
// ========================================

import {
  routeTripListQuery,
  routeTripQuery,
  routeTripCreate,
  routeTripMutation,
} from '@/shared/services/offline-prep/router';
import * as TripLocal from '../lib/trip-local';
import * as TripApi from '../api/trips';
import type { Trip, CreateTripRequest, UpdateTripRequest, DeleteTripResponse } from '../model';

/**
 * Trip Repository
 *
 * 목록은 기존 전역 활성 상태로, 단건 조회·수정·삭제는 대상 여행으로 분기한다.
 * 새 여행 생성은 서버에서 처리하고 이후 별도 활성화한다.
 */
export const TripRepository = {
  /**
   * 모든 여행 조회
   */
  getAll: async (): Promise<Trip[]> => {
    return await routeTripListQuery({
      local: () => TripLocal.getTripsLocal(),
      remote: async () => {
        const response = await TripApi.fetchAllTrips();
        return response.data;
      },
    });
  },

  /**
   * 특정 여행 조회
   */
  getById: async (id: string): Promise<Trip | undefined> => {
    return await routeTripQuery(id, {
      local: () => TripLocal.getTripByIdLocal(id),
      remote: async () => {
        // TODO: fetchTripById API 필요시 추가
        const response = await TripApi.fetchAllTrips();
        return response.data.find((trip) => trip.id === id);
      },
    });
  },

  /**
   * 여행 생성
   */
  create: async (data: CreateTripRequest): Promise<Trip> => {
    return await routeTripCreate(() => TripApi.fetchCreateTrip(data));
  },

  /**
   * 여행 수정
   */
  update: async (id: string, data: UpdateTripRequest): Promise<Trip> => {
    return await routeTripMutation(id, {
      local: () => TripLocal.updateTripLocal(id, data),
      remote: () => TripApi.fetchUpdateTrip(id, data),
    });
  },

  /**
   * 여행 삭제 (Soft Delete)
   */
  delete: async (id: string): Promise<DeleteTripResponse> => {
    return await routeTripMutation(id, {
      local: () => TripLocal.deleteTripLocal(id),
      remote: () => TripApi.fetchDeleteTrip(id),
    });
  },
};
