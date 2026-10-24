import { View, Text } from 'react-native';
import { Pressable } from '@repo/ui';
import { PolicyErrorDisplay } from './PolicyErrorDisplay';
import { useNetworkCheck } from '@/shared/store/network';
import { useGetActiveTrip } from '@/entities/trip/data/useGetTripActivation';
import { useTripStore } from '@/shared/store/useTripStore';
import type { useTripContentAccess } from '@/shared/policy/useTripContentAccess';

type Access = ReturnType<typeof useTripContentAccess>;

export function TripContentStatus({
  access,
  onReturnToActiveTrip,
}: {
  access: Access;
  onReturnToActiveTrip?: () => void;
}) {
  const { checkStatus, isRefreshing, refresh } = useNetworkCheck();
  const { data: activeTrip } = useGetActiveTrip();
  const setSelectedTripId = useTripStore((state) => state.setSelectedTripId);

  if (access.status === 'loading') {
    return (
      <View className='flex-1 items-center justify-center p-lg'>
        <Text>여행 내용을 불러오는 중...</Text>
      </View>
    );
  }
  if (access.status === 'error') {
    return (
      <View className='flex-1 items-center justify-center gap-sm p-lg'>
        <Text>여행 내용을 불러오지 못했어요. 다시 시도해주세요.</Text>
        <Pressable onPress={access.retry}>다시 불러오기</Pressable>
      </View>
    );
  }

  const { status } = access.permission;
  const networkRestricted = status === 'offline' || status === 'network-checking' || status === 'network-unavailable';
  return (
    <View className='flex-1 gap-sm p-md'>
      <PolicyErrorDisplay permission={access.permission} variant='inline' />
      {networkRestricted && (
        <>
          {activeTrip ? (
            <Pressable
              onPress={() => {
                setSelectedTripId(activeTrip.tripId);
                onReturnToActiveTrip?.();
              }}
            >
              활성 여행으로 돌아가기
            </Pressable>
          ) : (
            <Text className='text-body text-muted-foreground'>현재 이 기기에서 사용할 수 있는 활성 여행이 없어요.</Text>
          )}
          {(status === 'offline' || status === 'network-unavailable' || checkStatus === 'unavailable') && (
            <Pressable disabled={isRefreshing} onPress={() => refresh()}>
              {isRefreshing ? '연결 확인 중...' : '연결 재확인'}
            </Pressable>
          )}
        </>
      )}
      {status === 'activation-error' && <Pressable onPress={access.retry}>다시 확인하기</Pressable>}
    </View>
  );
}

export function TripRecoveryNotice({ notice }: { notice: string | null }) {
  if (!notice) return null;
  return (
    <View
      accessibilityRole='alert'
      accessibilityLiveRegion='polite'
      className='absolute bottom-md left-md right-md rounded-md bg-muted p-sm'
    >
      <Text className='text-body text-foreground'>{notice}</Text>
    </View>
  );
}
