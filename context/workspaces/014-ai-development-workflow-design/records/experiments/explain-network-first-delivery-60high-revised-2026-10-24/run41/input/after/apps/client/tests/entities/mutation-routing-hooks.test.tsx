import React from 'react';
import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import { act, cleanup, renderHook } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUpdateSchedule } from '@/entities/schedule/data/useUpdateSchedule';
import { useDeleteSchedule } from '@/entities/schedule/data/useDeleteSchedule';
import { useUpdateExpense } from '@/entities/expense/data/useUpdateExpense';
import { useDeleteExpense } from '@/entities/expense/data/useDeleteExpense';
import { ScheduleRepository } from '@/entities/schedule/repository/schedule-repository';
import { ExpenseRepository } from '@/entities/expense/repository/expense-repository';
import { OfflineError } from '@/shared/services/offline-prep/errors';

jest.mock('@/entities/schedule/repository/schedule-repository', () => ({
  ScheduleRepository: { update: jest.fn(), delete: jest.fn() },
}));
jest.mock('@/entities/expense/repository/expense-repository', () => ({
  ExpenseRepository: { update: jest.fn(), delete: jest.fn() },
}));

let queryClient: QueryClient;
const blocked = new OfflineError('인터넷 연결을 아직 확인하지 못했어요.', { action: 'ONLINE_REQUIRED' });

function Wrapper({ children }: { children: React.ReactNode }) {
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}

beforeEach(() => {
  queryClient = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
});

afterEach(() => {
  cleanup();
  queryClient.clear();
  jest.restoreAllMocks();
});

describe('mutation hook의 대상 여행과 제한 오류 전달', () => {
  it('일정 수정은 tripId를 전달하고 Router 거부를 그대로 반환해 성공 후 처리를 실행하지 않는다', async () => {
    jest.mocked(ScheduleRepository.update).mockRejectedValue(blocked);
    const invalidate = jest.spyOn(queryClient, 'invalidateQueries');
    const { result } = renderHook(() => useUpdateSchedule(), { wrapper: Wrapper });

    await act(async () => {
      await expect(result.current.mutateAsync({ id: 'schedule-b', tripId: 'trip-b', data: { title: '작성 중 입력' } }))
        .rejects.toBe(blocked);
    });

    expect(ScheduleRepository.update).toHaveBeenCalledWith('schedule-b', 'trip-b', { title: '작성 중 입력' });
    expect(invalidate).not.toHaveBeenCalled();
  });

  it('일정 삭제는 Local 조회 없이 분기할 수 있도록 소속 여행을 전달한다', async () => {
    jest.mocked(ScheduleRepository.delete).mockResolvedValue({ id: 'schedule-b', deletedAt: '2026-09-17T00:00:00Z' });
    const { result } = renderHook(() => useDeleteSchedule(), { wrapper: Wrapper });

    await act(async () => {
      await result.current.mutateAsync({ id: 'schedule-b', tripId: 'trip-b' });
    });

    expect(ScheduleRepository.delete).toHaveBeenCalledWith('schedule-b', 'trip-b');
  });

  it('경비 수정은 요청 body와 분기에 사용할 tripId를 나누어 전달한다', async () => {
    jest.mocked(ExpenseRepository.update).mockRejectedValue(blocked);
    const { result } = renderHook(() => useUpdateExpense(), { wrapper: Wrapper });

    await act(async () => {
      await expect(result.current.mutateAsync({ id: 'expense-b', tripId: 'trip-b', data: { title: '작성 중 입력' } }))
        .rejects.toBe(blocked);
    });

    expect(ExpenseRepository.update).toHaveBeenCalledWith('expense-b', 'trip-b', { title: '작성 중 입력' });
  });

  it('경비 삭제의 제한 오류도 caller에게 그대로 전달한다', async () => {
    jest.mocked(ExpenseRepository.delete).mockRejectedValue(blocked);
    const { result } = renderHook(() => useDeleteExpense(), { wrapper: Wrapper });

    await act(async () => {
      await expect(result.current.mutateAsync({ id: 'expense-b', tripId: 'trip-b' })).rejects.toBe(blocked);
    });

    expect(ExpenseRepository.delete).toHaveBeenCalledWith('expense-b', 'trip-b');
  });
});
