import { act, fireEvent, render } from '@testing-library/react-native';
import { Alert } from 'react-native';
import { ScheduleCard } from '@/shared/components/Card/ScheduleCard';
import { TripSelector } from '@/entities/trip/ui/TripSelector';
import ScheduleScreen from '@/screens/ScheduleScreen';
import CreateExpenseScreen from '@/screens/CreateExpenseScreen';
import TripDateForm from '@/features/trip/create-trip/TripDateForm';
import { useNetworkStore } from '@/shared/store/network';
import { useTripStore } from '@/shared/store/useTripStore';
import { OfflineError } from '@/shared/services/offline-prep/errors';

const mockMutate = jest.fn();
const mockBack = jest.fn();
let mockActiveTrip: { tripId: string; mapDownloaded: boolean } | null = { tripId: 'a', mapDownloaded: true };
const mockTrips = [
  { id: 'a', destination: '활성 여행', baseCurrency: 'USD', startDate: '2026-09-17', endDate: '2026-09-18' },
  { id: 'b', destination: '비활성 여행', baseCurrency: 'USD', startDate: '2026-09-17', endDate: '2026-09-18' },
];

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('expo-router', () => ({
  useLocalSearchParams: () => ({ tripId: 'b' }),
  useRouter: () => ({ back: mockBack }),
}));
jest.mock('lucide-react-native', () => new Proxy({}, { get: () => () => null }));
jest.mock('@repo/ui', () => {
  const { View, TouchableOpacity, Text } = require('react-native');
  return {
    Card: ({ children }: any) => <View>{children}</View>,
    cn: (...args: any[]) => args.join(' '),
    Badge: ({ children }: any) => <View>{children}</View>,
    Drawer: ({ isOpen, children }: any) => (isOpen ? <View>{children}</View> : null),
    Pressable: ({ children, ...props }: any) => (
      <TouchableOpacity {...props}>
        {typeof children === 'string' ? <Text>{children}</Text> : children}
      </TouchableOpacity>
    ),
  };
});
jest.mock('@/entities/trip/data', () => ({ useGetTrips: () => ({ data: mockTrips, isLoading: false }) }));
jest.mock('@/entities/trip/utils', () => ({ selectMainTrip: () => mockTrips[0] }));
jest.mock('@/entities/trip', () => ({
  useGetTrips: () => ({ data: mockTrips }),
  useCreateTrip: () => ({ mutate: mockMutate, isPending: false }),
  TripSelector: () => null,
}));
jest.mock('@/entities/trip/data/useGetTripActivation', () => ({
  useGetActiveTrip: () => ({ data: mockActiveTrip }),
  useGetTripActivation: () => ({ data: null }),
}));
jest.mock('@/entities/schedule', () => ({
  useGetSchedules: () => ({
    data: [],
    isLoading: false,
    isError: false,
    refetch: jest.fn(async () => ({ isError: false })),
  }),
  useDeleteSchedule: () => ({ mutate: mockMutate }),
}));
jest.mock('@/features/schedule/schedule-list-view', () => {
  const { Text } = require('react-native');
  return { ScheduleListView: () => <Text>서버 일정 목록</Text> };
});
jest.mock('@/features/schedule/schedule-map-view', () => ({ ScheduleMapViewContainer: () => null }));
jest.mock('@/features/schedule/schedule-menu', () => ({ ScheduleMenu: () => null }));
jest.mock('@/features/schedule/update-schedule', () => {
  const { Text } = require('react-native');
  return { UpdateScheduleDrawer: () => <Text>유지되는 수정 입력</Text> };
});
jest.mock('@/entities/expense', () => ({ useCreateExpense: () => ({ mutate: mockMutate, isPending: false }) }));
jest.mock('@/shared/components/DatePicker/DatePicker', () => {
  const { TouchableOpacity, Text } = require('react-native');
  return {
    __esModule: true,
    default: ({ visible, onSelectDate }: any) =>
      visible ? (
        <TouchableOpacity testID='choose-date' onPress={() => onSelectDate('2026-09-17')}>
          <Text>날짜 고르기</Text>
        </TouchableOpacity>
      ) : null,
  };
});
jest.mock('@/shared/components/Navigation', () => ({ MobileHeader: () => null }));
jest.mock('@/shared/components', () => {
  const { Text } = require('react-native');
  return {
    PolicyErrorDisplay: ({ permission }: any) => <Text>{permission.reason}</Text>,
    MobileHeader: ({ rightAction }: any) => rightAction ?? null,
  };
});
jest.mock('@/features/expense/create-expense', () => {
  const { View, TextInput, Text, TouchableOpacity } = require('react-native');
  const { Controller } = require('react-hook-form');
  return {
    useCreateExpenseForm: jest.requireActual('@/features/expense/create-expense/useCreateExpenseForm')
      .useCreateExpenseForm,
    ExpenseForm: ({ form, onSubmit }: any) => (
      <View>
        <Controller
          control={form.control}
          name='title'
          render={({ field: { value, onChange } }: { field: { value: string; onChange: (value: string) => void } }) => (
            <TextInput testID='title' value={value} onChangeText={onChange} />
          )}
        />
        <TouchableOpacity
          testID='save'
          onPress={() => {
            form.setValue('amount', '10');
            form.setValue('category', 'food');
            onSubmit();
          }}
        >
          <Text>저장</Text>
        </TouchableOpacity>
      </View>
    ),
  };
});

beforeEach(() => {
  useNetworkStore.setState({ realStatus: 'online', overrideStatus: null });
  useTripStore.setState({ selectedTripId: 'a' });
  mockActiveTrip = { tripId: 'a', mapDownloaded: true };
  jest.clearAllMocks();
});

it('같은 카드 props에서도 네트워크와 화면 override 변화가 좌표 경고에 반영된다', () => {
  const screen = render(<ScheduleCard time='09:00' title='일정' location='장소' />);
  expect(screen.getByText(/좌표 없음/)).toBeTruthy();
  act(() => useNetworkStore.setState({ realStatus: 'offline' }));
  expect(screen.queryByText(/좌표 없음/)).toBeNull();
  act(() => useNetworkStore.setState({ overrideStatus: 'online' }));
  expect(screen.getByText(/좌표 없음/)).toBeTruthy();
  act(() => useNetworkStore.setState({ overrideStatus: 'unknown' }));
  expect(screen.queryByText(/좌표 없음/)).toBeNull();
});

it.each(['offline', 'unknown'] as const)(
  '%s에 새 비활성 여행 선택을 거부하고 기존 선택과 목록을 유지한다',
  (realStatus) => {
    useNetworkStore.setState({ realStatus });
    const alert = jest.spyOn(Alert, 'alert');
    const screen = render(<TripSelector />);
    fireEvent.press(screen.getByText('활성 여행'));
    fireEvent.press(screen.getByText('비활성 여행'));
    expect(useTripStore.getState().selectedTripId).toBe('a');
    expect(screen.getByText('비활성 여행')).toBeTruthy();
    expect(alert).toHaveBeenCalledTimes(1);
  },
);

it('생성 폼 작성 중 unknown이 되어도 입력을 유지하고 Router 이유를 한 번 안내하며 이동하지 않는다', async () => {
  const alert = jest.spyOn(Alert, 'alert');
  mockMutate.mockImplementation((_data, options) =>
    options.onError(new OfflineError('인터넷 연결을 아직 확인하지 못했어요.')),
  );
  const screen = render(<CreateExpenseScreen />);
  fireEvent.changeText(screen.getByTestId('title'), '작성 중인 경비');
  act(() => useNetworkStore.setState({ realStatus: 'unknown' }));
  expect(screen.getByTestId('title').props.value).toBe('작성 중인 경비');
  await act(async () => {
    fireEvent.press(screen.getByTestId('save'));
  });
  expect(mockMutate).toHaveBeenCalledTimes(1);
  expect(alert).toHaveBeenCalledWith('오류', '인터넷 연결을 아직 확인하지 못했어요.');
  expect(alert).toHaveBeenCalledTimes(1);
  expect(screen.getByTestId('title').props.value).toBe('작성 중인 경비');
  expect(mockBack).not.toHaveBeenCalled();
});

it('여행 생성 Router 거부를 정확한 이유로 안내하고 선택한 날짜를 유지한다', async () => {
  const alert = jest.spyOn(Alert, 'alert');
  mockMutate.mockImplementation((_data, options) =>
    options.onError(new OfflineError('화면 테스트 중에는 저장할 수 없어요.')),
  );
  const city = { id: 1, name: '서울', country: '대한민국', countryCode: 'KR', latitude: 37.5, longitude: 127 };
  const screen = render(<TripDateForm city={city} />);
  fireEvent.press(screen.getByText('시작일을 선택하세요'));
  fireEvent.press(screen.getByTestId('choose-date'));
  fireEvent.press(screen.getByText('종료일을 선택하세요'));
  fireEvent.press(screen.getByTestId('choose-date'));
  act(() => useNetworkStore.setState({ overrideStatus: 'unknown' }));
  await act(async () => fireEvent.press(screen.getByText('여행 생성')));
  expect(mockMutate).toHaveBeenCalledTimes(1);
  expect(alert).toHaveBeenCalledWith('오류', '화면 테스트 중에는 저장할 수 없어요.');
  expect(screen.getAllByText('2026-09-17')).toHaveLength(2);
});

it('활성 여행이 없어도 이미 알고 있는 여행 목록과 기존 선택은 유지한다', () => {
  mockActiveTrip = null;
  useTripStore.setState({ selectedTripId: 'b' });
  useNetworkStore.setState({ realStatus: 'offline' });
  const screen = render(<TripSelector />);
  fireEvent.press(screen.getByText('비활성 여행'));
  expect(screen.getByText('활성 여행')).toBeTruthy();
  expect(screen.getAllByText('비활성 여행')).toHaveLength(2);
  expect(useTripStore.getState().selectedTripId).toBe('b');
});

it('실제 일정 화면은 캐시 내용을 가리고 제한 안내를 본문에 한 번 표시하며 수정 입력을 유지한다', () => {
  useTripStore.setState({ selectedTripId: 'b' });
  const screen = render(<ScheduleScreen />);
  expect(screen.getByText('서버 일정 목록')).toBeTruthy();
  act(() => useNetworkStore.setState({ realStatus: 'offline' }));
  expect(screen.queryByText('서버 일정 목록')).toBeNull();
  expect(
    screen.getAllByText('오프라인에서는 준비된 활성 여행만 볼 수 있어요. 연결 후 다시 이용해주세요.'),
  ).toHaveLength(1);
  expect(screen.getByText('유지되는 수정 입력')).toBeTruthy();
  fireEvent.press(screen.getByLabelText('지도 보기로 전환'));
  expect(
    screen.getAllByText('오프라인에서는 준비된 활성 여행만 볼 수 있어요. 연결 후 다시 이용해주세요.'),
  ).toHaveLength(1);
});
