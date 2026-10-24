import { beforeEach, describe, expect, it, jest } from '@jest/globals';
import { TripRepository } from '@/entities/trip/repository/trip-repository';
import { ScheduleRepository } from '@/entities/schedule/repository/schedule-repository';
import { ExpenseRepository } from '@/entities/expense/repository/expense-repository';
import * as TripLocal from '@/entities/trip/lib/trip-local';
import * as TripApi from '@/entities/trip/api/trips';
import * as ScheduleLocal from '@/entities/schedule/lib/schedule-local';
import * as ScheduleApi from '@/entities/schedule/api/schedules';
import * as ExpenseLocal from '@/entities/expense/lib/expense-local';
import * as ExpenseApi from '@/entities/expense/api/expenses';
import { getTripActivationStatus, hasAnyActivatedTrip } from '@/shared/services/offline-prep/metadata';
import { useNetworkStore } from '@/shared/store/network';

jest.mock('@react-native-community/netinfo', () => ({
  __esModule: true,
  default: { addEventListener: jest.fn(), refresh: jest.fn() },
}));
jest.mock('@/shared/services/offline-prep/metadata', () => ({
  getTripActivationStatus: jest.fn(),
  hasAnyActivatedTrip: jest.fn(),
}));
jest.mock('@/entities/trip/lib/trip-local', () => ({
  getTripsLocal: jest.fn(),
  getTripByIdLocal: jest.fn(),
  createTripLocal: jest.fn(),
  updateTripLocal: jest.fn(),
  deleteTripLocal: jest.fn(),
}));
jest.mock('@/entities/trip/api/trips', () => ({
  fetchAllTrips: jest.fn(),
  fetchCreateTrip: jest.fn(),
  fetchUpdateTrip: jest.fn(),
  fetchDeleteTrip: jest.fn(),
}));
jest.mock('@/entities/schedule/lib/schedule-local', () => ({
  getScheduleTripIdLocal: jest.fn(),
  updateScheduleLocal: jest.fn(),
  deleteScheduleLocal: jest.fn(),
}));
jest.mock('@/entities/schedule/api/schedules', () => ({
  fetchUpdateSchedule: jest.fn(),
  fetchDeleteSchedule: jest.fn(),
}));
jest.mock('@/entities/expense/lib/expense-local', () => ({
  getExpenseTripIdLocal: jest.fn(),
  getTripIdByScheduleIdLocal: jest.fn(),
  updateExpenseLocal: jest.fn(),
  deleteExpenseLocal: jest.fn(),
  getExpensesByScheduleIdLocal: jest.fn(),
}));
jest.mock('@/entities/expense/api/expenses', () => ({
  fetchUpdateExpense: jest.fn(),
  fetchDeleteExpense: jest.fn(),
  fetchExpensesByScheduleId: jest.fn(),
}));

const inactiveTrip = { id: 'trip-b', name: '비활성 여행' } as Awaited<ReturnType<typeof TripRepository.create>>;
const createTrip = { id: 'trip-b' } as Parameters<typeof TripRepository.create>[0];
const schedule = { id: 'schedule-b', tripId: 'trip-b' } as Awaited<ReturnType<typeof ScheduleRepository.update>>;
const expense = { id: 'expense-b', tripId: 'trip-b' } as Awaited<ReturnType<typeof ExpenseRepository.update>>;
const deleted = { id: 'deleted-b', deletedAt: '2026-09-17T00:00:00Z' };

beforeEach(() => {
  useNetworkStore.setState({ realStatus: 'online', overrideStatus: null });
  jest.mocked(hasAnyActivatedTrip).mockResolvedValue(true);
  jest.mocked(getTripActivationStatus).mockImplementation(async (id) => id === 'trip-a');
  jest.mocked(TripApi.fetchAllTrips).mockResolvedValue({ data: [inactiveTrip], success: true });
  jest.mocked(TripApi.fetchCreateTrip).mockResolvedValue(inactiveTrip);
  jest.mocked(TripApi.fetchUpdateTrip).mockResolvedValue(inactiveTrip);
  jest.mocked(TripApi.fetchDeleteTrip).mockResolvedValue(deleted);
  jest.mocked(ScheduleApi.fetchUpdateSchedule).mockResolvedValue(schedule);
  jest.mocked(ScheduleApi.fetchDeleteSchedule).mockResolvedValue(deleted);
  jest.mocked(ExpenseApi.fetchUpdateExpense).mockResolvedValue(expense);
  jest.mocked(ExpenseApi.fetchDeleteExpense).mockResolvedValue(deleted);
  jest.mocked(ExpenseApi.fetchExpensesByScheduleId).mockResolvedValue([expense]);
});

describe('다른 여행 A가 활성화된 동안 비활성 여행 B의 요청', () => {
  it('단건 조회는 B의 서버 결과를 반환한다', async () => {
    await expect(TripRepository.getById('trip-b')).resolves.toEqual(inactiveTrip);
    expect(TripLocal.getTripByIdLocal).not.toHaveBeenCalled();
  });

  it('수정은 B의 서버 결과를 반환한다', async () => {
    await expect(TripRepository.update('trip-b', { name: '수정' })).resolves.toEqual(inactiveTrip);
    expect(TripLocal.updateTripLocal).not.toHaveBeenCalled();
  });

  it('삭제는 B의 서버 결과를 반환한다', async () => {
    await expect(TripRepository.delete('trip-b')).resolves.toEqual(deleted);
    expect(TripLocal.deleteTripLocal).not.toHaveBeenCalled();
  });

  it('전체 목록은 기존 전역 활성 여행 Local 조회를 유지한다', async () => {
    jest.mocked(TripLocal.getTripsLocal).mockResolvedValue([inactiveTrip]);
    await expect(TripRepository.getAll()).resolves.toEqual([inactiveTrip]);
    expect(TripApi.fetchAllTrips).not.toHaveBeenCalled();
  });

  it('새 여행 B 생성은 Local 생성 대신 서버에 client ID를 그대로 전달한다', async () => {
    await expect(TripRepository.create(createTrip)).resolves.toEqual(inactiveTrip);
    expect(TripApi.fetchCreateTrip).toHaveBeenCalledWith(createTrip);
    expect(TripLocal.createTripLocal).not.toHaveBeenCalled();
  });
});

const inactiveChildCases = [
  {
    name: '일정 수정',
    run: () => ScheduleRepository.update('schedule-b', 'trip-b', { title: '수정' }),
    result: schedule,
    remote: ScheduleApi.fetchUpdateSchedule,
    local: ScheduleLocal.updateScheduleLocal,
  },
  {
    name: '일정 삭제',
    run: () => ScheduleRepository.delete('schedule-b', 'trip-b'),
    result: deleted,
    remote: ScheduleApi.fetchDeleteSchedule,
    local: ScheduleLocal.deleteScheduleLocal,
  },
  {
    name: '경비 수정',
    run: () => ExpenseRepository.update('expense-b', 'trip-b', { title: '수정' }),
    result: expense,
    remote: ExpenseApi.fetchUpdateExpense,
    local: ExpenseLocal.updateExpenseLocal,
  },
  {
    name: '경비 삭제',
    run: () => ExpenseRepository.delete('expense-b', 'trip-b'),
    result: deleted,
    remote: ExpenseApi.fetchDeleteExpense,
    local: ExpenseLocal.deleteExpenseLocal,
  },
  {
    name: '일정별 경비 조회',
    run: () => ExpenseRepository.getByScheduleId('schedule-b', 'trip-b'),
    result: [expense],
    remote: ExpenseApi.fetchExpensesByScheduleId,
    local: ExpenseLocal.getExpensesByScheduleIdLocal,
  },
];

describe.each(inactiveChildCases)('Local에 없는 비활성 여행의 $name', ({ run, result, remote, local }) => {
  it('알고 있는 소속 여행으로 서버를 선택해 결과를 반환한다', async () => {
    await expect(run()).resolves.toEqual(result);
    expect(getTripActivationStatus).toHaveBeenCalledWith('trip-b');
    expect(remote).toHaveBeenCalledTimes(1);
    expect(local).not.toHaveBeenCalled();
    expect(ScheduleLocal.getScheduleTripIdLocal).not.toHaveBeenCalled();
    expect(ExpenseLocal.getExpenseTripIdLocal).not.toHaveBeenCalled();
    expect(ExpenseLocal.getTripIdByScheduleIdLocal).not.toHaveBeenCalled();
  });

  it.each(['offline', 'unknown'] as const)('%s에서는 서버·Local 동작을 시작하지 않는다', async (realStatus) => {
    useNetworkStore.setState({ realStatus });
    await expect(run()).rejects.toMatchObject({ name: 'OfflineError' });
    expect(remote).not.toHaveBeenCalled();
    expect(local).not.toHaveBeenCalled();
  });
});
