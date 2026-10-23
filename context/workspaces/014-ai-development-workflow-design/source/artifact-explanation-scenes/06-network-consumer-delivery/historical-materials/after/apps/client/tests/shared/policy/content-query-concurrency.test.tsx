import type { PropsWithChildren } from 'react';
import { Text, View } from 'react-native';
import { act, render, waitFor } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useGetTripExpenses } from '@/entities/expense/data/useGetTripExpenses';
import { expenseQueryKeys } from '@/entities/expense/data/keys';
import { ExpenseRepository } from '@/entities/expense/repository/expense-repository';
import type { Expense } from '@/entities/expense/model/types';
import { useTripContentAccess } from '@/shared/policy/useTripContentAccess';
import { useNetworkStore } from '@/shared/store/network';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/entities/trip/data/useGetTripActivation', () => ({
  useGetTripActivation: () => ({ data: null }),
}));
jest.mock('@/entities/expense/repository/expense-repository', () => ({
  ExpenseRepository: { getByTripId: jest.fn() },
}));

const repository = jest.mocked(ExpenseRepository.getByTripId);
const cachedExpense: Expense = {
  id: 'expense-b',
  tripId: 'trip-b',
  userId: null,
  scheduleId: null,
  title: '이전 서버 응답',
  amount: '10',
  currency: 'USD',
  category: '식사',
  date: '2026-09-17',
  createdAt: '2026-09-17T00:00:00Z',
  updatedAt: '2026-09-17T00:00:00Z',
  hasReceipt: false,
  receiptUrl: null,
};

function Consumer({ name }: { name: string }) {
  const query = useGetTripExpenses('trip-b');
  const access = useTripContentAccess('trip-b', query);
  return (
    <View>
      <Text testID={`${name}-status`}>{access.status}</Text>
      {access.status === 'ready' && <Text testID={`${name}-content`}>{query.data?.[0]?.title}</Text>}
    </View>
  );
}

it('동일 여행의 두 실제 Query observer는 복구 요청 하나를 공유하고 성공 전 캐시 내용을 숨긴다', async () => {
  useNetworkStore.setState({ realStatus: 'online', overrideStatus: null, checkStatus: 'idle' });
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: Infinity, refetchOnReconnect: false } },
  });
  const key = expenseQueryKeys.byTrip('trip-b');
  client.setQueryData(key, [cachedExpense]);
  let resolveRequest!: (data: Expense[]) => void;
  const request = new Promise<Expense[]>((resolve) => {
    resolveRequest = resolve;
  });
  repository.mockImplementation(() => request);
  function Wrapper({ children }: PropsWithChildren) {
    return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
  }
  const screen = render(
    <Wrapper>
      <Consumer name='one' />
      <Consumer name='two' />
    </Wrapper>,
  );
  try {
    expect(screen.getAllByText('이전 서버 응답')).toHaveLength(2);
    expect(repository).not.toHaveBeenCalled();
    act(() => useNetworkStore.setState({ realStatus: 'offline' }));
    expect(screen.queryByTestId('one-content')).toBeNull();
    expect(screen.queryByTestId('two-content')).toBeNull();
    expect(screen.getAllByText('restricted')).toHaveLength(2);

    await act(async () => {
      useNetworkStore.setState({ realStatus: 'online' });
    });
    expect(repository).toHaveBeenCalledTimes(1);
    expect(repository).toHaveBeenCalledWith('trip-b');
    expect(screen.getAllByText('loading')).toHaveLength(2);
    expect(screen.queryByTestId('one-content')).toBeNull();
    expect(screen.queryByTestId('two-content')).toBeNull();
    expect(client.getQueryData(key)).toEqual([cachedExpense]);

    const freshExpense = { ...cachedExpense, title: '재조회한 서버 응답' };
    await act(async () => {
      resolveRequest([freshExpense]);
      await request;
    });
    await waitFor(() => expect(screen.getAllByText('ready')).toHaveLength(2));
    expect(screen.getAllByText('재조회한 서버 응답')).toHaveLength(2);
    expect(repository).toHaveBeenCalledTimes(1);
    expect(client.getQueryData(key)).toEqual([freshExpense]);
  } finally {
    screen.unmount();
    client.clear();
  }
});
