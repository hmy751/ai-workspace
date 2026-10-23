import { getTripActivationStatus, hasAnyActivatedTrip } from './metadata';
import { OfflineError, type OfflineErrorOptions } from './errors';
import { networkStore } from '@/shared/store/network';

interface RouteOperations<T> {
  local: () => Promise<T>;
  remote: () => Promise<T>;
}

function assertRemoteAvailable(
  offlineMessage: string,
  tripId?: string,
  offlineAction: NonNullable<OfflineErrorOptions['action']> = 'ACTIVATE_PROMPT',
) {
  const status = networkStore.realStatus;

  if (status === 'online') {
    return;
  }

  throw new OfflineError(
    status === 'unknown' ? '인터넷 연결을 아직 확인하지 못했어요. 잠시 후 다시 시도해주세요.' : offlineMessage,
    { action: status === 'unknown' ? 'ONLINE_REQUIRED' : offlineAction, tripId },
  );
}

function assertWritesAllowed() {
  if (networkStore.override !== null) {
    throw new OfflineError('네트워크 화면 테스트 중에는 저장·삭제할 수 없어요. 강제 설정을 해제해주세요.', {
      action: 'ONLINE_REQUIRED',
    });
  }
}

/** 여행 목록은 활성 여행이 있으면 기존 Local 목록을 사용한다. */
export async function routeTripListQuery<T>(operations: RouteOperations<T>): Promise<T> {
  const hasActivated = await hasAnyActivatedTrip();

  if (hasActivated) {
    return await operations.local();
  }

  assertRemoteAvailable('오프라인에서는 활성화된 여행만 볼 수 있어요');
  return await operations.remote();
}

/** Trip 단건 조회는 대상 여행의 활성 여부로 분기한다. */
export async function routeTripQuery<T>(tripId: string, operations: RouteOperations<T>): Promise<T> {
  return routeChildQuery(tripId, operations);
}

/** Schedule·Expense 조회는 소속 여행의 활성 여부로 분기한다. */
export async function routeChildQuery<T>(tripId: string, operations: RouteOperations<T>): Promise<T> {
  const isActivated = await getTripActivationStatus(tripId);

  if (isActivated) {
    return await operations.local();
  }

  assertRemoteAvailable('오프라인에서는 활성화된 여행만 볼 수 있어요', tripId);
  return await operations.remote();
}

/** 새 여행은 아직 활성화되지 않았으므로 서버에서 생성한다. */
export async function routeTripCreate<T>(remote: () => Promise<T>): Promise<T> {
  assertWritesAllowed();
  assertRemoteAvailable('새 여행을 만들려면 인터넷에 연결해주세요', undefined, 'ONLINE_REQUIRED');
  return remote();
}

/** Trip 수정·삭제는 대상 여행의 활성 여부로 분기한다. */
export async function routeTripMutation<T>(tripId: string, operations: RouteOperations<T>): Promise<T> {
  return routeChildMutation(tripId, operations);
}

/** Schedule·Expense 쓰기는 소속 여행의 활성 여부로 분기한다. */
export async function routeChildMutation<T>(tripId: string, operations: RouteOperations<T>): Promise<T> {
  const isActivated = await getTripActivationStatus(tripId);

  assertWritesAllowed();

  if (isActivated) {
    return await operations.local();
  }

  assertRemoteAvailable('오프라인에서는 활성화된 여행만 수정할 수 있어요', tripId);
  return await operations.remote();
}
