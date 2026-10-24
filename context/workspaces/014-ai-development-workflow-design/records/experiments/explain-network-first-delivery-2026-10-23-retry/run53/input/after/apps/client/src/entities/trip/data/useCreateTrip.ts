import { useMutation, useQueryClient } from '@tanstack/react-query';
import { TripRepository } from '../repository/trip-repository';
import type { CreateTripRequest } from '../model';
import { tripQueryKeys } from './keys';

/**
 * 여행 생성 Mutation Hook
 *
 * - 아직 활성화되지 않은 새 여행은 서버에 생성한다.
 * - Client-Side ID: 외부에서 ID 생성하여 전달
 *
 * @example
 * ```tsx
 * const { mutate, isPending } = useCreateTrip();
 * mutate({
 *   id: generateId(), // Client-Side ID: 외부에서 ID 생성
 *   name: 'Tokyo Trip',
 *   destination: 'Tokyo',
 *   country: 'Japan',
 *   // ...
 * });
 * ```
 */
export const useCreateTrip = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateTripRequest) => TripRepository.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: tripQueryKeys.all(),
      });
    },
  });
};
