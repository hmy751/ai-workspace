import { useRealNetworkStatus } from '@/shared/store/network';
import { useAuthStore } from '@/shared/store/auth';
import { useQuery } from '@tanstack/react-query';
import { TripRepository } from '../repository/trip-repository';
import { tripQueryKeys } from './keys';

/** 여행 목록을 조회하며 실제 Local/Remote 출처를 함께 제공한다. */
export const useGetTrips = () => {
  const networkStatus = useRealNetworkStatus();
  const authStatus = useAuthStore((state) => state.status);
  const canQueryServer = networkStatus === 'online' && authStatus === 'signed-in';

  const query = useQuery({
    queryKey: tripQueryKeys.list(canQueryServer),
    queryFn: ({ signal }) => TripRepository.getAllWithSource(signal),
    // 연결 복구로 이전 서버 Query를 다시 구독할 때도 최신 목록을 확인한다.
    staleTime: 0,
    gcTime: 10 * 60 * 1000, // 10분
  });

  // 데이터와 실제 조회 출처를 함께 보존한다. 현재 네트워크 상태로 출처를 추정하지 않는다.
  return { ...query, data: query.data?.trips, dataSource: query.data?.source };
};
