import { useAppPolicy } from '@/shared/policy';
import type { OperationPolicy } from '@/shared/policy/types';

interface ReadAccess {
  hasTrip: boolean;
  display: OperationPolicy;
  actual: OperationPolicy;
  enabled: boolean;
}

/** 화면 표시와 실제 조회에 같은 Policy를 각각의 관측 기준으로 적용한다. */
export function useTripReadAccess(tripId: string | null | undefined) {
  const display = useAppPolicy(tripId ?? undefined);
  const actual = useAppPolicy(tripId ?? undefined, { network: 'real' });

  const forEntity = (entity: 'schedule' | 'expense'): ReadAccess => ({
    hasTrip: !!tripId,
    display: display[entity].read,
    actual: actual[entity].read,
    enabled: !!tripId && display[entity].read.allowed && actual[entity].read.allowed,
  });

  return { schedule: forEntity('schedule'), expense: forEntity('expense') };
}

type ReadQueryView<T> =
  | { kind: 'unselected' }
  | { kind: 'blocked'; policy: OperationPolicy }
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'ready'; data: T; refreshFailed: boolean };

/** 현재 입력에서 표시 결과만 계산한다. Query 데이터나 복구 이력을 따로 저장하지 않는다. */
export function getReadQueryView<T>(
  access: ReadAccess,
  query: { data: T | undefined; isError: boolean; isFetching: boolean },
): ReadQueryView<T> {
  if (!access.hasTrip) return { kind: 'unselected' };
  if (!access.display.allowed) return { kind: 'blocked', policy: access.display };
  // 정상적인 빈 목록도 표시 가능한 결과다. 재조회 실패로 기존 내용을 가리지 않는다.
  if (query.data !== undefined) {
    return { kind: 'ready', data: query.data, refreshFailed: query.isError && !query.isFetching };
  }
  if (!access.actual.allowed) return { kind: 'blocked', policy: access.actual };
  return { kind: query.isError ? 'error' : 'loading' };
}
