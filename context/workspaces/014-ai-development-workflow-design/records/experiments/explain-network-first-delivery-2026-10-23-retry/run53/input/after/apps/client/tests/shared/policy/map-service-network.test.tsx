import React from 'react';
import { render, screen, act } from '@testing-library/react-native';
import { PolicyBasedMapView } from '@/shared/components/PolicyBasedMapView/PolicyBasedMapView';
import { PolicyBasedScheduleMapView } from '@/shared/components/Map/PolicyBasedScheduleMapView';
import { networkStore, useNetworkStore } from '@/shared/store/network';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/shared/policy', () => ({
  useAppPolicy: () => {
    const { useDisplayNetworkStatus } = jest.requireActual('@/shared/store/network');
    return { service: { mapProvider: useDisplayNetworkStatus() === 'online' ? 'google' : 'mapbox' } };
  },
}));
jest.mock('@/entities/offline-city', () => ({
  useOfflineCity: () => ({ data: { cityName: 'Paris', cityId: 'paris' }, isLoading: false }),
}));
jest.mock('@/shared/hooks/map/useMyLocation', () => ({ useMyLocation: () => ({ moveToCurrentLocation: jest.fn() }) }));
jest.mock('@/shared/components/Map/MyLocationButton', () => ({ MyLocationButton: () => null }));
jest.mock('react-native-maps', () => {
  const React = require('react');
  const { Text } = require('react-native');
  return { __esModule: true, default: React.forwardRef(() => <Text>Google search map</Text>), Marker: () => null };
});
jest.mock('@/shared/components/Map/GoogleScheduleMapView', () => ({
  GoogleScheduleMapView: () => { const { Text } = require('react-native'); return <Text>Google schedule map</Text>; },
}));
jest.mock('@/shared/components/Map/MapboxScheduleMapView', () => ({
  MapboxScheduleMapView: () => { const { Text } = require('react-native'); return <Text>Local schedule map</Text>; },
}));
jest.mock('@/shared/components/PolicyBasedMapView/OfflineMapView', () => ({
  OfflineMapView: () => { const { Text } = require('react-native'); return <Text>Local search map</Text>; },
}));

const location = { latitude: 1, longitude: 2, name: 'Place', address: 'Address' };
function Maps() {
  return <>
    <PolicyBasedMapView tripId='active' locations={[location]} selectedLocation={null} />
    <PolicyBasedScheduleMapView tripId='active' schedules={[]} />
  </>;
}
afterEach(() => networkStore.cleanup());

it.each(['unknown', 'offline'] as const)('표시 online·실측 %s는 Google native 지도를 마운트하지 않는다', (realStatus) => {
  useNetworkStore.setState({ realStatus, overrideStatus: 'online' });
  render(<Maps />);
  expect(screen.queryByText('Google search map')).toBeNull();
  expect(screen.queryByText('Google schedule map')).toBeNull();
  expect(screen.getAllByText('실제 연결이 확인되면 지도를 다시 사용할 수 있어요')).toHaveLength(2);
  act(() => useNetworkStore.setState({ realStatus: 'online' }));
  expect(screen.getByText('Google search map')).toBeTruthy();
  expect(screen.getByText('Google schedule map')).toBeTruthy();
});

it('실측 online·표시 offline은 기존 Local 지도 선택을 유지한다', () => {
  useNetworkStore.setState({ realStatus: 'online', overrideStatus: 'offline' });
  render(<Maps />);
  expect(screen.getByText('Local search map')).toBeTruthy();
  expect(screen.getByText('Local schedule map')).toBeTruthy();
  expect(screen.queryByText('Google search map')).toBeNull();
});
