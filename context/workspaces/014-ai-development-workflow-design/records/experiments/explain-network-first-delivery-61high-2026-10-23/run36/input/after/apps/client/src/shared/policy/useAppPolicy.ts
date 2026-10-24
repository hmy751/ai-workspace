/**
 * useAppPolicy Hook
 *
 * 범용 Policy Hook - 모든 Entity의 CRUD 정책을 한 번에 제공
 * 여러 Entity 정책을 동시에 체크해야 할 때 사용
 */

import { useMemo } from 'react';
import {
  useDisplayNetworkStatus,
  useNetworkCheck,
  type NetworkStatus,
  type NetworkCheckStatus,
} from '@/shared/store/network';
import { useGetTripActivation } from '@/entities/trip/data/useGetTripActivation';
import { TRIP_POLICIES, SCHEDULE_POLICIES, EXPENSE_POLICIES, SERVICE_POLICIES } from './constants';
import type { CRUDPermission, ServiceConfig, PolicyKey, ActivationStatus } from './types';

/**
 * App Policy Context
 *
 * 모든 Entity의 CRUD 정책 + Service 설정
 */
export interface TripContentPermission extends CRUDPermission {
  status:
    | 'ready'
    | 'no-trip'
    | 'activation-loading'
    | 'activation-error'
    | 'offline'
    | 'network-checking'
    | 'network-unavailable';
}

export interface AppPolicyContext {
  retryActivation: () => void;
  activationStatus: 'active' | 'inactive' | 'loading' | 'error';
  content: TripContentPermission;
  trip: {
    create: CRUDPermission;
    read: CRUDPermission;
    update: CRUDPermission;
    delete: CRUDPermission;
  };
  schedule: {
    create: CRUDPermission;
    read: CRUDPermission;
    update: CRUDPermission;
    delete: CRUDPermission;
  };
  expense: {
    create: CRUDPermission;
    read: CRUDPermission;
    update: CRUDPermission;
    delete: CRUDPermission;
  };
  service: ServiceConfig;
}

/**
 * 앱 전역 Policy Hook
 *
 * @param tripId - Trip ID (optional)
 * @returns 모든 Entity의 CRUD 정책
 *
 * @example
 * ```tsx
 * // 여러 Entity 정책을 동시에 체크
 * const policy = useAppPolicy(tripId);
 *
 * if (!policy.schedule.create.allowed) {
 *   return <DisabledMessage reason={policy.schedule.create.reason} />;
 * }
 *
 * if (policy.expense.create.mode === 'manual-only') {
 *   return <ManualInputForm />;
 * }
 *
 * // Service 설정도 접근 가능
 * if (policy.service.mapProvider === 'mapbox') {
 *   return <OfflineMap />;
 * }
 * ```
 */
export function useAppPolicy(tripId?: string): AppPolicyContext {
  const networkStatus = useDisplayNetworkStatus();

  const { data: activation, isError, refetch: refetchActivation } = useGetTripActivation(tripId ?? '');
  const { checkStatus } = useNetworkCheck();

  let activationStatus: AppPolicyContext['activationStatus'] = 'inactive';
  if (tripId) {
    if (activation?.isActivated) activationStatus = 'active';
    else if (isError) activationStatus = 'error';
    else if (activation === undefined) activationStatus = 'loading';
  }
  const policyActivationStatus: ActivationStatus = activationStatus === 'active' ? 'active' : 'inactive';

  // unknown도 Remote 기능을 열지 않는다. 현재 4-state 권한 표의 제한 모드를 재사용한다.
  const policyNetworkStatus = networkStatus === 'online' ? 'online' : 'offline';
  const policyKey: PolicyKey = `${policyNetworkStatus}_${policyActivationStatus}`;

  return useMemo(() => {
    const content = getContentPermission(tripId, activationStatus, networkStatus, checkStatus);

    const permissions = (table: typeof TRIP_POLICIES) => {
      const permission = (operation: keyof typeof table): CRUDPermission => {
        const value = table[operation][policyKey];
        if ((activationStatus === 'loading' || activationStatus === 'error') && operation !== 'create') {
          return { allowed: false, reason: content.reason };
        }
        if (!value.allowed && networkStatus === 'unknown') {
          return { ...value, reason: '인터넷 연결을 아직 확인하지 못했어요. 잠시 후 다시 시도해주세요.' };
        }
        return value;
      };
      return {
        create: permission('create'),
        read: permission('read'),
        update: permission('update'),
        delete: permission('delete'),
      };
    };

    return {
      activationStatus,
      retryActivation: () => {
        refetchActivation();
      },
      content,
      trip: permissions(TRIP_POLICIES),
      schedule: { ...permissions(SCHEDULE_POLICIES), read: content },
      expense: { ...permissions(EXPENSE_POLICIES), read: content },
      service:
        SERVICE_POLICIES[
          activationStatus === 'loading' || activationStatus === 'error' ? 'offline_inactive' : policyKey
        ],
    };
  }, [tripId, policyKey, activationStatus, networkStatus, checkStatus, refetchActivation]);
}

/** 이미 알고 있는 여행 기본 정보와 그 여행의 일정·경비 내용 접근은 구별한다. */
function getContentPermission(
  tripId: string | undefined,
  activationStatus: AppPolicyContext['activationStatus'],
  networkStatus: NetworkStatus,
  checkStatus: NetworkCheckStatus,
): TripContentPermission {
  if (!tripId) return { allowed: false, status: 'no-trip', reason: '여행을 선택해주세요' };
  if (activationStatus === 'loading') {
    return { allowed: false, status: 'activation-loading', reason: '이 기기의 여행 준비 상태를 확인하는 중이에요.' };
  }
  if (activationStatus === 'error') {
    return {
      allowed: false,
      status: 'activation-error',
      reason: '여행 준비 상태를 확인하지 못했어요. 다시 시도해주세요.',
    };
  }
  if (activationStatus === 'active' || networkStatus === 'online') return { allowed: true, status: 'ready' };
  if (networkStatus === 'offline') {
    return {
      allowed: false,
      status: 'offline',
      reason: '오프라인에서는 준비된 활성 여행만 볼 수 있어요. 연결 후 다시 이용해주세요.',
    };
  }
  if (checkStatus === 'unavailable') {
    return {
      allowed: false,
      status: 'network-unavailable',
      reason: '인터넷 연결을 확인하지 못했어요. 연결 상태를 재확인해주세요.',
    };
  }
  return {
    allowed: false,
    status: 'network-checking',
    reason: '인터넷 연결을 확인하는 중이에요. 활성 여행은 계속 이용할 수 있어요.',
  };
}
