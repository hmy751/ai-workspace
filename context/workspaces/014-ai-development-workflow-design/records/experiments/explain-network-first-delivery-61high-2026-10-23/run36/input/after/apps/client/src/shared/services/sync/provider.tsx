import React, { createContext, useContext, useEffect, useRef, useState, useCallback } from 'react';
import { networkStore, useNetworkStore, useRealNetworkStatus } from '@/shared/store/network';
import { authStore, useAuthStore } from '@/shared/store/auth';
import { syncData } from './engine';

export type SyncRunResult =
  | { status: 'completed'; message: string }
  | { status: 'failed'; message: string }
  | { status: 'blocked'; message: string };

interface SyncContextValue {
  isSyncing: boolean;
  lastSyncedAt: Date | null;
  triggerManualSync: () => Promise<SyncRunResult>;
}

const SyncContext = createContext<SyncContextValue | undefined>(undefined);

export function useSyncContext() {
  const context = useContext(SyncContext);
  if (!context) {
    throw new Error('useSyncContext must be used within SyncProvider');
  }
  return context;
}

interface SyncProviderProps {
  children: React.ReactNode;
  isDatabaseReady: boolean;
  enablePeriodicSync?: boolean;
  syncInterval?: number;
}

export function SyncProvider({
  children,
  isDatabaseReady,
  enablePeriodicSync = false,
  syncInterval = 5 * 60 * 1000,
}: SyncProviderProps) {
  const networkStatus = useRealNetworkStatus();
  const overrideStatus = useNetworkStore((state) => state.overrideStatus);
  const isAuthInitialized = useAuthStore((state) => state.isInitialized);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const canSync =
    isDatabaseReady && isAuthInitialized && isAuthenticated && networkStatus === 'online' && overrideStatus === null;

  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSyncedAt, setLastSyncedAt] = useState<Date | null>(null);
  const inFlightRef = useRef<Promise<SyncRunResult> | null>(null);
  const databaseReadyRef = useRef(isDatabaseReady);
  databaseReadyRef.current = isDatabaseReady;
  const previouslyEligibleRef = useRef(false);

  const executeSync = useCallback((): Promise<SyncRunResult> => {
    // 이전 render의 callback과 자동/수동 호출도 같은 진행 중 실행을 기다린다.
    if (inFlightRef.current) {
      return inFlightRef.current;
    }

    let blockedMessage: string | null = null;
    if (!databaseReadyRef.current) {
      blockedMessage = '데이터베이스가 준비되지 않아 동기화할 수 없습니다.';
    } else if (!authStore.isInitialized || !authStore.isAuthenticated) {
      blockedMessage = '로그인 준비가 완료된 뒤 동기화할 수 있습니다.';
    } else if (networkStore.override !== null) {
      blockedMessage = '네트워크 강제 설정 중에는 동기화할 수 없습니다. 실제 상태로 되돌려 주세요.';
    } else if (networkStore.realStatus !== 'online') {
      blockedMessage = '인터넷 연결이 확인된 뒤 동기화할 수 있습니다.';
    }
    if (blockedMessage) {
      return Promise.resolve({ status: 'blocked', message: blockedMessage });
    }

    let resolveRun!: (result: SyncRunResult) => void;
    const run = new Promise<SyncRunResult>((resolve) => {
      resolveRun = resolve;
    });
    // React 표시 상태를 갱신하기 전에 실행 소유권을 선점한다.
    inFlightRef.current = run;
    previouslyEligibleRef.current = true;
    setIsSyncing(true);

    (async () => {
      let result: SyncRunResult;
      try {
        await syncData();
        setLastSyncedAt(new Date());
        // engine가 반환됐음을 뜻한다. queue 전체 반영 여부는 engine의 결과 계약에 따른다.
        result = { status: 'completed', message: '동기화가 완료되었습니다.' };
      } catch {
        result = { status: 'failed', message: '동기화에 실패했습니다.' };
      }
      inFlightRef.current = null;
      setIsSyncing(false);
      resolveRun(result);
    })();

    return run;
  }, []);

  // 최초 준비 완료, 로그인, 연결 복구, 강제 설정 해제가 같은 시작 경계를 사용한다.
  useEffect(() => {
    const wasEligible = previouslyEligibleRef.current;
    previouslyEligibleRef.current = canSync;
    if (canSync && !wasEligible) {
      executeSync();
    }
  }, [canSync, executeSync]);

  useEffect(() => {
    if (!enablePeriodicSync) {
      return;
    }
    const intervalId = setInterval(() => {
      executeSync();
    }, syncInterval);
    return () => clearInterval(intervalId);
  }, [enablePeriodicSync, syncInterval, executeSync]);

  return (
    <SyncContext.Provider value={{ isSyncing, lastSyncedAt, triggerManualSync: executeSync }}>
      {children}
    </SyncContext.Provider>
  );
}
