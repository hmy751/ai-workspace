========== 기본 설정 방법 ==========

- libs/queryClient.ts와 갚이 App으로 부터 분리하여 queryClient를
- 두어서 관리한다.
- 서버 상태는 클라이언트와 분리하여 원격으로 관리되어야 하기 때문이다.

```js
import { QueryClient } from '@tanstack/react-query';

const STALE_TIME = 1000 * 60 * 5; // 5분
const GC_TIME = 1000 * 60 * 10; // 10분

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // staleTime: 데이터가 fresh 상태로 유지되는 시간.
      // 이 시간 내에는 동일 쿼리 요청 시 네트워크 요청 없이 캐시된 데이터를 즉시 반환한다.
      // 기본값은 0이며, 5분 정도로 설정하는 경우가 많다.
      staleTime: STALE_TIME,

      // gcTime (cacheTime): 데이터가 inactive 상태일 때 캐시에서 유지되는 시간.
      // 쿼리 인스턴스가 언마운트되면 데이터는 inactive 상태로 전환되고, gcTime이 지나면 가비지 컬렉터가 수집한다.
      // 기본값은 5분이다. gcTime은 항상 staleTime보다 길어야 한다.
      gcTime: GC_TIME,

      // refetchOnWindowFocus: 사용자가 브라우저 창에 다시 포커스했을 때 데이터를 자동으로 다시 가져올지 여부.
      // 사용자의 데이터 최신성을 보장하는 강력한 기능이지만, 때로는 과도한 요청을 유발할 수 있어
      // 전역으로 false로 두고 필요한 쿼리에만 개별적으로 true를 설정하기도 한다.
      refetchOnWindowFocus: true,

      // refetchOnMount: 컴포넌트 마운트 시 데이터가 stale 상태이면 자동으로 다시 가져올지 여부.
      // 기본값은 true로, 대부분의 경우 유용하다.
      refetchOnMount: true,

      // retry: 쿼리 실패 시 자동으로 재시도하는 횟수.
      // 기본값은 3이며, 인증 실패처럼 재시도가 무의미한 경우에는 0으로 설정하기도 한다.
      retry: 1,
    },
  },
});
```

기본 useQuery

```js
const {
  data: itemData,
  isLoading: isItemLoading,
  error: itemError,
} = useQuery({
  queryKey: ['catalog', 'items', itemId],
  queryFn: () => http.get < { item: Item } > `/api/catalog/items/${itemId}`,
  enabled: Boolean(itemId),
});
```

- enabled는 아직 들어오지 않은 데이터가 있을때 활용하면 좋다.

# suspense, errorboundary

```tsx
<QueryErrorResetBoundary>
  {({ reset }) => (
    <ErrorBoundary onReset={reset} FallbackComponent={CalendarBody.Error}>
      <Suspense fallback={<CalendarBody.Loading />}>
        <CalendarBody currentMonth={currentMonth} currentYear={currentYear} />
      </Suspense>
    </ErrorBoundary>
  )}
</QueryErrorResetBoundary>
```

QueryErrorResetBoundary는 ErrorBoundary내부에 useSuspenseQuery의 재시도를 하기위해 필요하다
없을 경우 QueryClient는 해당 내용을 에러로 처리한 상태이므로 reset을 해도 다시 갱신되지않고 지속해서 에럴를 발생시키기 때문에 필요하다.

```tsx
}) {
  const { days } = getCalendarDataWeeks({
    year: currentYear,
    monthIndex: (currentMonth - 1) as MonthIndex,
  });

  const { data: reservations } = useReservations();

  return (
    <div className={CALENDAR_BODY_WRAPPER_CLASSES}>
      {days.map((week) => (
        <DateRow
          key={week[0].dateString}
          week={week}
          reservations={reservations}
        />
      ))}
    </div>
  );
}

...

const useReservations = () => {
  return useSuspenseQuery<Reservation[]>({
    queryKey: ["reservations"],
    queryFn: async () => {
      const res = await getReservations();

      // 1. 필터링
      const filteredReservations = res.data.filter(
        (reservation: Reservation) =>
          reservation.status !== "PENDING_CONFIRM" &&
          reservation.status !== "CANCELED"
      );

      //
```

Suspense에 감지 되려면 useSuspenseQuery를 활용해야 감지되며
@tanstack/react-query 패키지를 사용해야한다.

# 캐시 무효화 하는 방법

```tsx
import { useQuery, useQueryClient } from '@tanstack/react-query';

const queryClient = useQueryClient();

queryClient.invalidateQueries({ queryKey: ['orders'] });
queryClient.invalidateQueries({ queryKey: ['todo'] });
```

useQueryClient를 사용하여 invalidateQueries로 무효화 할수 있고 배열의 순서가 있기때문에 순서를 고려해서 잘 활용해야한다.

# mutation 메서드

```tsx
const { mutate: createOrder, isPending: isSubmitting } = useMutation<
  OrderResponse,
  unknown,
  { totalPrice: number; items: OrderItem[] }
>({
  mutationFn: requestBody =>
    http.post('/api/orders', {
      json: requestBody,
    }),
  onSuccess: response => {
    queryClient.invalidateQueries({ queryKey: ['orders'] });
    queryClient.invalidateQueries({ queryKey: ['catalog'] });
    clearCart();
    navigate(`/order-complete?orderId=${response.orderId}`);
  },
  onError: () => {
    overlay.open(({ isOpen, close }) => (
      <Toast isOpen={isOpen} close={close} type="warn" message="주문에 실패했습니다." delay={1500} />
    ));
  },
});
```

# 외부 컴포넌트에서 isFetching과 같은 hook 활용하는 방법

```tsx
const isFetching = useIsFetching({ queryKey: ['reservations'] });

const handleLeftArrowClick = () => {
  if (isFetching > 0) return;

  if (currentMonth === 1) {
    setCurrentMonth(12);
    setCurrentYear(currentYear - 1);
  } else {
    setCurrentMonth((currentMonth - 1) as Month);
  }
};
```
