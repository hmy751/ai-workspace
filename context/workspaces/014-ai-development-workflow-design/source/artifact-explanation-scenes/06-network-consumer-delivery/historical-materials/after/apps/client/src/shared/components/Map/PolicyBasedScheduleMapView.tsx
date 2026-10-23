/**
 * PolicyBasedScheduleMapView - 정책 기반 지도 제공자 선택
 *
 * 정책에 따라 자동으로 지도 제공자를 선택:
 * - online (active/inactive): Google Maps
 * - offline_active: Mapbox (오프라인 지도)
 * - offline_inactive: 지도 사용 불가
 */

import { useAppPolicy } from '@/shared/policy';
import { GoogleScheduleMapView } from './GoogleScheduleMapView';
import { MapboxScheduleMapView } from './MapboxScheduleMapView';
import { MapUnavailableView } from './MapUnavailableView';
import type { ScheduleMapViewProps } from './types';
import { useRealNetworkStatus } from '@/shared/store/network';
import { getOnlineServicePermission } from '@/shared/services/network-access';

/**
 * 정책 기반으로 적절한 지도 제공자를 자동 선택
 * Policy Layer (v3.0)의 service.mapProvider 정책을 따름
 */
export function PolicyBasedScheduleMapView(props: ScheduleMapViewProps) {
  const { tripId, ...mapProps } = props;
  const policy = useAppPolicy(tripId);
  const permission = getOnlineServicePermission(useRealNetworkStatus());

  if (policy.service.mapProvider === 'google' && !permission.allowed) {
    return <MapUnavailableView message={permission.reason} hint='실제 연결이 확인되면 지도를 다시 사용할 수 있어요' />;
  }

  switch (policy.service.mapProvider) {
    case 'google':
      return <GoogleScheduleMapView {...mapProps} tripId={tripId} />;

    case 'mapbox':
      return <MapboxScheduleMapView {...mapProps} tripId={tripId} />;

    case 'none':
      return (
        <MapUnavailableView
          message='오프라인 상태에서는 지도를 사용할 수 없습니다'
          hint='네트워크에 연결하거나 여행을 활성화해주세요'
        />
      );

    default:
      return <MapUnavailableView message='지도를 사용할 수 없어요' />;
  }
}
