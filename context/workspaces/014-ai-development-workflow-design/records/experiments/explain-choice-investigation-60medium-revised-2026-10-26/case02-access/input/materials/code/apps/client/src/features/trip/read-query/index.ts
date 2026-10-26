import { useGetSchedules } from '@/entities/schedule';
import { useReadQuery, useTripReadAccess, type TripReadOptions } from './read-query';

export type { TripReadOptions, ReadQueryState, ReadRefetchOutcome } from './read-query';

export function useSchedulesRead(tripId: string | null | undefined, options: TripReadOptions = {}) {
  const access = useTripReadAccess(tripId, 'schedule', options);
  const query = useGetSchedules(tripId ?? '', { enabled: access.enabled });
  return useReadQuery(query, access);
}
