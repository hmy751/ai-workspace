import { useCallback, useLayoutEffect, useRef } from 'react';
import type { RefetchOptions, UseQueryResult } from '@tanstack/react-query';
import { useAppPolicy } from '@/shared/policy';
import type { OperationPolicy } from '@/shared/policy/types';

// Union의 각 구성원에서 제외해야 status와 data 사이의 타입 관계가 유지된다.
type WithoutRefetch<T> = T extends unknown ? Omit<T, 'refetch'> : never;
export type ReadQueryState<T, E> = WithoutRefetch<UseQueryResult<T, E>>;

type ReadBlock =
  | { reason: 'unselected' | 'disabled' }
  | { reason: 'policy'; policy: OperationPolicy };

export type ReadRefetchOutcome<T, E> =
  | ({ kind: 'blocked' } & ReadBlock)
  | { kind: 'finished'; result: ReadQueryState<T, E> };

interface ReadAccess {
  hasTrip: boolean;
  requested: boolean;
  display: OperationPolicy;
  actual: OperationPolicy;
  block: ReadBlock | undefined;
  enabled: boolean;
}

export interface TripReadOptions {
  enabled?: boolean;
}

export function useTripReadAccess(
  tripId: string | null | undefined,
  entity: 'schedule' | 'expense',
  { enabled = true }: TripReadOptions,
): ReadAccess {
  const display = useAppPolicy(tripId ?? undefined)[entity].read;
  const actual = useAppPolicy(tripId ?? undefined, { network: 'real' })[entity].read;
  const block: ReadBlock | undefined = !tripId
    ? { reason: 'unselected' }
    : !enabled
      ? { reason: 'disabled' }
      : !display.allowed
        ? { reason: 'policy', policy: display }
        : !actual.allowed
          ? { reason: 'policy', policy: actual }
          : undefined;
  return { hasTrip: !!tripId, requested: enabled, display, actual, block, enabled: !block };
}

type ReadQueryView<T> =
  | { kind: 'unselected' }
  | { kind: 'idle' }
  | { kind: 'blocked'; policy: OperationPolicy }
  | { kind: 'loading' }
  | { kind: 'error' }
  | { kind: 'ready'; data: T; refreshFailed: boolean };

function getReadQueryView<T, E>(access: ReadAccess, query: UseQueryResult<T, E>): ReadQueryView<T> {
  if (!access.hasTrip) return { kind: 'unselected' };
  if (!access.display.allowed) return { kind: 'blocked', policy: access.display };
  // 성공한 undefined나 빈 배열도 유효한 결과다. 재조회 실패로 기존 내용을 가리지 않는다.
  if (query.isSuccess || query.isRefetchError) {
    return { kind: 'ready', data: query.data, refreshFailed: query.isError && !query.isFetching };
  }
  if (!access.requested) return { kind: 'idle' };
  if (!access.actual.allowed) return { kind: 'blocked', policy: access.actual };
  return { kind: query.isError ? 'error' : 'loading' };
}

/** refetch를 실제 객체에서도 빼고, 나머지 필드는 접근할 때 원본에서 읽는다. */
function toQueryState<T, E>(query: UseQueryResult<T, E>): ReadQueryState<T, E> {
  const state = {};
  for (const key of Object.keys(query) as (keyof typeof query)[]) {
    if (key === 'refetch') continue;
    Object.defineProperty(state, key, { enumerable: true, get: () => query[key] });
  }
  // 필드 값/판별자를 바꾸지 않고 refetch만 제외한다. spread로 모든 추적 필드를 읽지 않는다.
  return state as ReadQueryState<T, E>;
}

/** Query 소유의 상태, Policy를 적용하는 실행, 표시 결과를 조합한다. 데이터는 별도 저장하지 않는다. */
export function useReadQuery<T, E>(query: UseQueryResult<T, E>, access: ReadAccess) {
  const current = useRef({ query, access });
  useLayoutEffect(() => {
    current.current = { query, access };
  }, [query, access]);

  // 이전 렌더에서 받은 callback도 최근 commit의 접근 조건을 확인한다.
  const refetch = useCallback(async (options?: RefetchOptions): Promise<ReadRefetchOutcome<T, E>> => {
    const { query: latestQuery, access: latestAccess } = current.current;
    if (latestAccess.block) return { kind: 'blocked', ...latestAccess.block };
    const result = await latestQuery.refetch(options);
    return { kind: 'finished', result: toQueryState(result) };
  }, []);

  return {
    query: toQueryState(query),
    actions: { canRefetch: access.enabled, refetch },
    view: getReadQueryView(access, query),
  };
}
