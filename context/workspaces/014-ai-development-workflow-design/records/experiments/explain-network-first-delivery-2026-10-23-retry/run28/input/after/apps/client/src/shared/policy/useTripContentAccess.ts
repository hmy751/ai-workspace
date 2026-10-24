import { useEffect, useRef, useState } from 'react';
import { useAppPolicy } from './useAppPolicy';
import { useRealNetworkStatus } from '@/shared/store/network';

type ContentQuery = {
  isLoading: boolean;
  isError: boolean;
  refetch: (options?: { cancelRefetch: boolean }) => Promise<{ isError: boolean; error: unknown }>;
};

type Recovery = {
  tripId?: string;
  blocked: boolean;
  hadOffline: boolean;
  phase: 'idle' | 'pending' | 'error';
};

/** 이전 서버 캐시는 보존하고, 현재 여행의 복구 조회가 성공할 때 내용을 다시 연다. */
export function useTripContentAccess(tripId: string | undefined, query: ContentQuery) {
  const policy = useAppPolicy(tripId);
  const realStatus = useRealNetworkStatus();
  const [recovery, setRecovery] = useState<Recovery>({ tripId, blocked: false, hadOffline: false, phase: 'idle' });
  const [notice, setNotice] = useState<string | null>(null);
  const latest = useRef({ tripId, realStatus });
  latest.current = { tripId, realStatus };
  const requestVersion = useRef(0);
  const refetch = useRef(query.refetch);
  refetch.current = query.refetch;

  useEffect(() => {
    if (recovery.tripId !== tripId) {
      requestVersion.current += 1;
      setNotice(null);
      setRecovery({ tripId, blocked: false, hadOffline: false, phase: 'idle' });
      return;
    }
    if (!tripId || policy.activationStatus !== 'inactive') {
      if (recovery.blocked) {
        requestVersion.current += 1;
        setRecovery({ tripId, blocked: false, hadOffline: false, phase: 'idle' });
      }
      return;
    }

    if (realStatus !== 'online') {
      setNotice(null);
      requestVersion.current += 1;
      setRecovery((current) => ({
        ...current,
        blocked: true,
        hadOffline: current.hadOffline || realStatus === 'offline',
        phase: 'idle',
      }));
      return;
    }
    if (!recovery.blocked || recovery.phase !== 'idle') return;

    const version = ++requestVersion.current;
    setRecovery((current) => ({ ...current, phase: 'pending' }));
    refetch.current({ cancelRefetch: false }).then(
      (result) => {
        if (
          version !== requestVersion.current ||
          latest.current.tripId !== tripId ||
          latest.current.realStatus !== 'online'
        )
          return;
        if (result.isError) {
          setRecovery((current) => ({ ...current, phase: 'error' }));
        } else {
          if (recovery.hadOffline) setNotice('연결이 복구되어 여행 내용을 다시 불러왔어요.');
          setRecovery({ tripId, blocked: false, hadOffline: false, phase: 'idle' });
        }
      },
      () => {
        if (version === requestVersion.current && latest.current.tripId === tripId) {
          setRecovery((current) => ({ ...current, phase: 'error' }));
        }
      },
    );
  }, [
    tripId,
    realStatus,
    policy.activationStatus,
    recovery.tripId,
    recovery.blocked,
    recovery.phase,
    recovery.hadOffline,
  ]);

  useEffect(
    () => () => {
      requestVersion.current += 1;
    },
    [],
  );

  useEffect(() => {
    if (!notice) return;
    const timer = setTimeout(() => setNotice(null), 3500);
    return () => clearTimeout(timer);
  }, [notice]);

  const awaitingRecovery =
    recovery.tripId === tripId && recovery.blocked && realStatus === 'online' && policy.activationStatus === 'inactive';
  const status = !policy.content.allowed
    ? 'restricted'
    : awaitingRecovery
      ? recovery.phase === 'error'
        ? 'error'
        : 'loading'
      : query.isLoading
        ? 'loading'
        : query.isError
          ? 'error'
          : 'ready';

  const retry = () => {
    if (policy.activationStatus === 'error') policy.retryActivation();
    else if (awaitingRecovery) setRecovery((current) => ({ ...current, phase: 'idle' }));
    else query.refetch({ cancelRefetch: false });
  };

  return { status, permission: policy.content, notice, retry };
}
