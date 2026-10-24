import { useQuery } from '@tanstack/react-query';
import { useEffect, useRef } from 'react';
import { useRealNetworkStatus } from '@/shared/store/network';
import { TripRepository } from '../repository/trip-repository';
import { tripQueryKeys } from './keys';

/**
 * 전체 여행을 조회하는 React Query 훅
 *
 * - Repository를 통해 활성화 상태에 따라 Local/Remote 자동 분기
 * - deletedAt이 null인 항목만 조회 (Soft Delete)
 * - updatedAt 기준 내림차순 정렬
 * - 비활성+오프라인 시 OfflineError 발생 → UI에서 "활성화하기" 안내
 *
 * @example
 * ```tsx
 * const { data: trips, isLoading } = useGetTrips();
 * ```
 */
export const useGetTrips = () => {
  const realStatus = useRealNetworkStatus();
  const previousStatus = useRef(realStatus);
  const query = useQuery({
    queryKey: tripQueryKeys.all(),
    queryFn: () => TripRepository.getAll(),
    staleTime: 5 * 60 * 1000, // 5분
    gcTime: 10 * 60 * 1000, // 10분
  });
  const { refetch } = query;

  useEffect(() => {
    const becameOnline = previousStatus.current !== 'online' && realStatus === 'online';
    previousStatus.current = realStatus;
    // 초기 unknown에서 거부된 목록도 회복한다. 이미 보낸 조회는 취소하거나 다시 보내지 않는다.
    if (becameOnline) refetch({ cancelRefetch: false });
  }, [realStatus, refetch]);

  return query;
};
