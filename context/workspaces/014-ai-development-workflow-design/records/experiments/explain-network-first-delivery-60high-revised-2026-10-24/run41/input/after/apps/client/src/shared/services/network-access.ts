import { createPolicyError } from '@/shared/policy/errors';
import { networkStore, type NetworkStatus } from '@/shared/store/network';

type OnlineServicePermission = { allowed: true } | { allowed: false; reason: string };

/** Service 요청은 화면용 override가 아닌 실제 관측을 사용한다. */
export function getOnlineServicePermission(realStatus: NetworkStatus): OnlineServicePermission {
  if (realStatus === 'online') return { allowed: true };

  return {
    allowed: false,
    reason:
      realStatus === 'unknown'
        ? '인터넷 연결을 아직 확인하지 못했어요. 잠시 후 다시 시도해주세요.'
        : '인터넷 연결이 필요해요. 연결 후 다시 시도해주세요.',
  };
}

export function assertOnlineServiceAccess() {
  const permission = getOnlineServicePermission(networkStore.realStatus);
  if (!permission.allowed) throw createPolicyError('NETWORK', permission);
}
