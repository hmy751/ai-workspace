### ========== 1. JavaScript 네이티브 Date 객체 ==========

JavaScript에 내장된 객체로 별도 라이브러리 없이 날짜와 시간을 다룰 수 있음.
하지만 가변성(mutable), 0부터 시작하는 월 인덱스, 불안정한 문자열 파싱 등 다루기 까다로운 부분이 많아 주의가 필요함.

#### 특징 및 주의사항

- **가변성 (Mutability)**: `Date` 객체의 메서드는 객체 원본을 직접 변경함. 이는 예상치 못한 사이드 이펙트를 유발할 수 있음.
  ```js
  const date = new Date('2025-12-24');
  const sameDate = date;
  sameDate.setDate(25); // sameDate를 변경했지만
  console.log(date.getDate()); // 원본인 date까지 변경됨 -> 25
  ```
- **0-indexed 월 (Month)**: `getMonth()` 메서드는 1월을 `0`으로, 12월을 `11`로 반환하여 실수를 유발하기 쉬움.
- **불안정한 문자열 파싱**: `new Date('2025-05-01')`과 같은 코드는 브라우저 또는 실행 환경에 따라 UTC 자정 또는 로컬 타임존 자정으로 다르게 해석될 수 있어 일관성이 떨어짐. ISO 8601 형식(`YYYY-MM-DDTHH:mm:ss.sssZ`)을 사용하는 것이 비교적 안전함.

#### 코드 속 활용 예시

**Date 객체 생성 및 월(Month) 처리**

- `Calendar.tsx`에서 `new Date()`로 현재 날짜를 가져오고, `getMonth()`에 `+1`을 더해 UI에 표시될 월(1-12)을 구함.
  ```tsx
  // Calendar.tsx
  export default function Calendar() {
    const [currentMonth, setCurrentMonth] = useState<Month>(() => {
      // getMonth()는 0-11을 반환하므로, 실제 월을 얻기 위해 +1을 해줌.
      return (new Date().getMonth() + 1) as Month;
    });
    // ...
  }
  ```

**문자열에서 Date 객체 생성**

- `DateRow.tsx`에서 서버로부터 받은 날짜 문자열(`reservation.moveInDate`)로 `Date` 객체를 생성하여 날짜 비교에 사용함.

  ```tsx
  // DateRow.tsx
  // ...
  const reservationsForThisWeek = (allReservationsForPeriod || []).filter(reservation => {
    // 'reservation.moveInDate' 문자열 형식에 따라 파싱 결과가 달라질 수 있어 주의가 필요함.
    const reservationStart = startOfDay(new Date(reservation.moveInDate));
    const reservationEnd = startOfDay(new Date(reservation.moveOutDate));

    return reservationStart <= weekEnd && reservationEnd > weekStart;
  });
  // ...
  ```

### ========== 2. `date-fns` 라이브러리 활용 ==========

`Date` 객체의 단점을 보완하고, 날짜를 더 쉽고 안전하게 다루기 위해 사용하는 라이브러리.
불변성을 유지하며, 직관적인 함수를 제공하고, 필요한 함수만 가져와 사용할 수 있어 효율적임.

#### 날짜 정규화를 통한 정확한 비교

- 시간, 분, 초를 제외하고 오직 '날짜' 기준으로만 비교하고 싶을 때 `startOfDay`나 `endOfDay`가 매우 유용함.

  ```tsx
  // DateRow.tsx
  import { startOfDay, endOfDay } from 'date-fns';

  // ...
  const weekStart = startOfDay(week[0].date); // 해당 주의 시작일 00:00:00
  const weekEnd = endOfDay(week[6].date); // 해당 주의 마지막일 23:59:59.999

  const reservationStart = startOfDay(new Date(reservation.moveInDate));
  const reservationEnd = startOfDay(new Date(reservation.moveOutDate));

  // 시간을 제외하고 날짜만으로 정확하게 기간 포함 여부를 검사할 수 있음.
  const isOverlapping = reservationStart <= weekEnd && reservationEnd >= weekStart;
  ```

#### 복잡한 로직 단순화 (getCalendarDataWeeks)

- 캘린더 그리드를 만드는 복잡한 계산을 직관적인 함수 조합으로 해결함.

  ```ts
  // utils/date.ts
  import { startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, format } from 'date-fns';

  export const getCalendarDataWeeks = ({ year, monthIndex }) => {
    const targetDate = new Date(year, monthIndex, 1);

    // 1. 현재 달의 시작일과 마지막일을 구함.
    const firstDayOfCurrentMonth = startOfMonth(targetDate);
    const lastDayOfCurrentMonth = endOfMonth(targetDate);

    // 2. 달력 그리드의 시작일(이전 달)과 마지막일(다음 달)을 구함.
    const calendarGridStartDate = startOfWeek(firstDayOfCurrentMonth);
    const calendarGridEndDate = endOfWeek(lastDayOfCurrentMonth);

    // 3. 그리드 시작일부터 종료일까지의 모든 날짜를 배열로 만듦.
    const calendarDays = eachDayOfInterval({
      start: calendarGridStartDate,
      end: calendarGridEndDate,
    });

    // ... 이후 데이터를 가공하여 주 단위로 그룹화 ...
    return {
      /* ... 가공된 캘린더 데이터 ... */
    };
  };
  ```

### ========== 3. 날짜 처리 모범 사례 (Best Practices) ==========

`Date`와 `date-fns`를 함께 사용하며 발생할 수 있는 혼란을 줄이고 코드의 안정성을 높이는 패턴.

#### 1-based 월과 0-based 인덱스 처리

- **UI와 상태는 사용자 친화적인 1-based 월(1~12)**을 사용하고, **`Date` 객체나 `date-fns`에 전달할 때만 0-based 인덱스(0~11)**로 변환함.
  ```tsx
  // CalendarBody.tsx
  export default function CalendarBody({
    currentMonth, // 상태값은 1~12
    currentYear,
  }) {
    const { days } = getCalendarDataWeeks({
      year: currentYear,
      // date-fns 함수에 전달할 때는 -1을 하여 0-based 인덱스로 변환.
      monthIndex: (currentMonth - 1) as MonthIndex,
    });
    // ...
  }
  ```

#### `useMemo`를 사용한 계산 최적화

- 렌더링 시마다 반복될 필요 없는 계산은 `useMemo`로 감싸 성능을 최적화함. `isToday` 함수는 하루에 한 번만 결과가 바뀌므로 좋은 대상임.

  ```tsx
  // DateCell.tsx
  import { useMemo } from 'react';
  import { isToday as checkToday } from 'date-fns';

  export default function DateCell({ day }: { day: CalendarDay }) {
    // day.dateString이 바뀔 때만 checkToday 함수를 다시 실행함.
    const isToday = useMemo(() => checkToday(day.date), [day.dateString]);

    const todayClass = isToday ? 'text-amber-200' : '';
    // ...
  }
  ```
