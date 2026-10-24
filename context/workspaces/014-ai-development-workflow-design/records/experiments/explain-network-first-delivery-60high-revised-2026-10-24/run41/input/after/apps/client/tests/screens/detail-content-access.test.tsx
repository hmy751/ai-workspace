import React from 'react';
import { act, fireEvent, render } from '@testing-library/react-native';
import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import ScheduleDetailScreen from '@/screens/ScheduleDetailScreen';
import ExpenseDetailScreen from '@/screens/ExpenseDetailScreen';
import { useNetworkStore } from '@/shared/store/network';
import { useTripStore } from '@/shared/store/useTripStore';
import { useGetTripActivation, useGetActiveTrip } from '@/entities/trip/data/useGetTripActivation';
import { useGetScheduleById } from '@/entities/schedule/data';
import { useGetSchedules } from '@/entities/schedule';
import { useGetScheduleExpenses, useGetTripExpenses } from '@/entities/expense';
import { useRouter } from 'expo-router';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/entities/trip/data/useGetTripActivation', () => ({
  useGetTripActivation: jest.fn(),
  useGetActiveTrip: jest.fn(),
}));
jest.mock('@/entities/schedule/data', () => ({ useGetScheduleById: jest.fn() }));
jest.mock('@/entities/schedule', () => ({ useGetSchedules: jest.fn() }));
jest.mock('@/entities/expense', () => ({ useGetScheduleExpenses: jest.fn(), useGetTripExpenses: jest.fn() }));
jest.mock('@/features/schedule/schedule-expense-list', () => ({ ScheduleExpenseList: () => null }));
jest.mock('@/shared/components', () => {
  const ReactRuntime = jest.requireActual<typeof import('react')>('react');
  const { View, Pressable, Text } = jest.requireActual<typeof import('react-native')>('react-native');
  return {
    Container: View,
    Stack: View,
    MobileHeader: ({ title, onLeftPress }: { title: string; onLeftPress: () => void }) =>
      ReactRuntime.createElement(Pressable, { onPress: onLeftPress }, ReactRuntime.createElement(Text, null, title)),
  };
});
jest.mock('@repo/ui', () => {
  const ReactRuntime = jest.requireActual<typeof import('react')>('react');
  const { View, Pressable, Text } = jest.requireActual<typeof import('react-native')>('react-native');
  return {
    Card: View,
    Separator: View,
    Pressable: ({ children, ...props }: { children: React.ReactNode }) =>
      ReactRuntime.createElement(
        Pressable,
        props,
        typeof children === 'string' ? ReactRuntime.createElement(Text, null, children) : children,
      ),
  };
});
jest.mock('lucide-react-native', () => ({
  MapPin: () => null,
  Clock: () => null,
  Wallet: () => null,
  ChevronLeft: () => null,
  Tag: () => null,
  Calendar: () => null,
  Receipt: () => null,
  AlertCircle: () => null,
  WifiOff: () => null,
  Lock: () => null,
}));
jest.mock('expo-router', () => ({
  useLocalSearchParams: () => ({ id: 'expense', tripId: 'inactive' }),
  useRouter: jest.fn(),
}));

const success = { isError: false, error: null };
const schedule = {
  id: 'schedule',
  tripId: 'inactive',
  title: '일정 서버 캐시',
  scheduledAt: '2026-09-17T12:00:00Z',
  location: 'Paris',
};
const expense = {
  id: 'expense',
  tripId: 'inactive',
  title: '경비 서버 캐시',
  amount: '12',
  currency: 'USD',
  category: '식사',
  date: '2026-09-17T12:00:00Z',
  scheduleId: 'schedule',
};
const firstRefetch = jest.fn<(options?: { cancelRefetch: boolean }) => Promise<typeof success>>();
const secondRefetch = jest.fn<(options?: { cancelRefetch: boolean }) => Promise<typeof success>>();
const goBack = jest.fn();
const replaceRoute = jest.fn();

beforeEach(() => {
  useNetworkStore.setState({ realStatus: 'online', overrideStatus: null, checkStatus: 'checking' });
  useTripStore.setState({ selectedTripId: 'inactive' });
  jest.mocked(useGetTripActivation).mockReturnValue({ data: null } as ReturnType<typeof useGetTripActivation>);
  jest.mocked(useGetActiveTrip).mockReturnValue({ data: { tripId: 'active' } } as ReturnType<typeof useGetActiveTrip>);
  jest
    .mocked(useRouter)
    .mockReturnValue({ back: goBack, push: jest.fn(), replace: replaceRoute } as unknown as ReturnType<
      typeof useRouter
    >);
  firstRefetch.mockReset().mockResolvedValue(success);
  secondRefetch.mockReset().mockResolvedValue(success);
  const query = { isLoading: false, isError: false };
  jest
    .mocked(useGetScheduleById)
    .mockReturnValue({ ...query, data: schedule, refetch: firstRefetch } as unknown as ReturnType<
      typeof useGetScheduleById
    >);
  jest
    .mocked(useGetScheduleExpenses)
    .mockReturnValue({ ...query, data: [expense], refetch: secondRefetch } as unknown as ReturnType<
      typeof useGetScheduleExpenses
    >);
  jest
    .mocked(useGetTripExpenses)
    .mockReturnValue({ ...query, data: [expense], refetch: firstRefetch } as unknown as ReturnType<
      typeof useGetTripExpenses
    >);
  jest
    .mocked(useGetSchedules)
    .mockReturnValue({ ...query, data: [schedule], refetch: secondRefetch } as unknown as ReturnType<
      typeof useGetSchedules
    >);
});
afterEach(() => {
  jest.restoreAllMocks();
});

const cases = [
  {
    name: '일정',
    title: '일정 서버 캐시',
    header: '일정 상세',
    activeRoute: '/(tabs)/schedules',
    component: () => (
      <ScheduleDetailScreen
        scheduleId='schedule'
        tripId='inactive'
        scheduledAt={schedule.scheduledAt}
        onBack={goBack}
      />
    ),
  },
  {
    name: '경비',
    title: '경비 서버 캐시',
    header: '경비 상세',
    activeRoute: '/(tabs)/expenses',
    component: () => <ExpenseDetailScreen />,
  },
];

describe.each(cases)('$name 상세 화면의 실제 캐시 제한·복구 연결', ({ title, header, activeRoute, component }) => {
  it('offline/unknown에서는 캐시를 숨기고 두 조회가 성공한 뒤 내용과 복구 안내를 연다', async () => {
    const screen = render(component());
    expect(screen.getByText(title)).toBeTruthy();
    act(() => {
      useNetworkStore.setState({ realStatus: 'offline' });
    });
    expect(screen.queryByText(title)).toBeNull();
    expect(screen.getByText(header)).toBeTruthy();
    act(() => {
      useNetworkStore.setState({ realStatus: 'unknown' });
    });
    expect(screen.queryByText(title)).toBeNull();
    let finishSecond!: (result: typeof success) => void;
    secondRefetch.mockReturnValueOnce(
      new Promise((resolve) => {
        finishSecond = resolve;
      }),
    );
    await act(async () => {
      useNetworkStore.setState({ realStatus: 'online' });
    });
    expect(firstRefetch).toHaveBeenCalledTimes(1);
    expect(secondRefetch).toHaveBeenCalledTimes(1);
    expect(firstRefetch).toHaveBeenCalledWith({ cancelRefetch: false });
    expect(secondRefetch).toHaveBeenCalledWith({ cancelRefetch: false });
    expect(screen.queryByText(title)).toBeNull();
    await act(async () => {
      finishSecond(success);
    });
    expect(screen.getByText(title)).toBeTruthy();
    expect(screen.getByText('연결이 복구되어 여행 내용을 다시 불러왔어요.')).toBeTruthy();
    expect(useTripStore.getState().selectedTripId).toBe('inactive');
  });

  it.each([firstRefetch, secondRefetch])(
    '어느 조회든 실패하면 cached 내용을 열지 않고 재시도 성공 후 복구한다',
    async (failedQuery) => {
      const screen = render(component());
      act(() => {
        useNetworkStore.setState({ realStatus: 'offline' });
      });
      failedQuery.mockResolvedValueOnce({ isError: true, error: null });
      await act(async () => {
        useNetworkStore.setState({ realStatus: 'online' });
      });
      expect(screen.queryByText(title)).toBeNull();
      expect(screen.getByText('여행 내용을 불러오지 못했어요. 다시 시도해주세요.')).toBeTruthy();
      await act(async () => {
        fireEvent.press(screen.getByText('다시 불러오기'));
      });
      expect(screen.getByText(title)).toBeTruthy();
      expect(firstRefetch).toHaveBeenCalledTimes(2);
      expect(secondRefetch).toHaveBeenCalledTimes(2);
    },
  );

  it.each(['offline', 'unknown'] as const)('활성 Local 여행은 %s에서도 상세를 유지한다', (realStatus) => {
    jest
      .mocked(useGetTripActivation)
      .mockReturnValue({ data: { isActivated: true } } as ReturnType<typeof useGetTripActivation>);
    useNetworkStore.setState({ realStatus });
    const screen = render(component());
    expect(screen.getByText(title)).toBeTruthy();
    expect(firstRefetch).not.toHaveBeenCalled();
  });

  it('일반 header 뒤로가기는 기존 경로 이동을 유지한다', () => {
    const screen = render(component());
    fireEvent.press(screen.getByText(header));
    expect(goBack).toHaveBeenCalledTimes(1);
    expect(replaceRoute).not.toHaveBeenCalled();
  });

  it('활성 여행으로 돌아가기는 여행 선택을 바꾸고 상세 경로도 닫는다', () => {
    useNetworkStore.setState({ realStatus: 'offline' });
    const screen = render(component());
    fireEvent.press(screen.getByText('활성 여행으로 돌아가기'));
    expect(useTripStore.getState().selectedTripId).toBe('active');
    expect(replaceRoute).toHaveBeenCalledWith(activeRoute);
    expect(goBack).not.toHaveBeenCalled();
  });
});
