### 1. 기본 패턴 (Basic Pattern)

상태와 그 상태를 변경하는 메서드를 하나의 스토어에 정의해서 사용하는 가장 기본적인 방식.
상태와 액션이 많아지면 스토어가 비대해져 구분이 어려워지는 단점이 있음.

```js
import { create } from 'zustand';

interface CounterState {
  count: number;
  increase: () => void;
  decrease: () => void;
}

export const useCountStore =
  create <
  CounterState >
  (set => ({
    count: 0,
    increase: () => set(state => ({ count: state.count + 1 })),
    decrease: () => set(state => ({ count: state.count - 1 })),
  }));
```

2. 액션 분리 패턴 (Action Separation Pattern)
   상태와 액션을 명확히 구분하기 위해, 모든 액션 함수를 actions라는 하나의 객체 안에 그룹화하는 패턴.

```tsx

import { create } from "zustand";

interface CounterState {
count: number;
actions: {
increase: () => void;
reset: () => void;
};
}

const initialState = { count: 0 };

export const useCountStore = create<CounterState>((set) => ({
...initialState,
actions: {
increase: () => set((state) => ({ count: state.count + 1 })),
reset: () => set(initialState),
},
}));

/_
// 컴포넌트에서 사용할 때
const count = useCountStore(state => state.count);
const { increase, reset } = useCountStore(state => state.actions);
_/
```

단점: persist 미들웨어와 함께 사용할 때 actions 객체는 함수를 포함하므로 JSON으로 변환될 수 없어 스토리지에 저장되지 않음. 이 문제를 해결하기 위해 Slice 패턴이 많이 사용됨.

3. Slice 패턴 (Slice Pattern)
   Redux의 모듈 방식처럼, 거대한 스토어를 기능 단위의 'slice'라는 작은 조각으로 나누어 관리하고 최종적으로 하나로 결합하는 패턴. 복잡한 상태 관리에 가장 권장됨.

기본 Slice 구성
각각의 slice는 (set, get)을 인자로 받는 함수로 정의하고, 관련된 상태와 액션을 객체로 반환함.

```js
// slices/countSlice.js
export const createCountSlice = set => ({
  count: 0,
  increase: () => set(state => ({ count: state.count + 1 })),
});

// slices/userSlice.js
export const createUserSlice = set => ({
  user: null,
  login: username => set({ user: { name: username } }),
  logout: () => set({ user: null }),
});

// stores/useBoundStore.js
import { create } from 'zustand';
import { createCountSlice } from './countSlice';
import { createUserSlice } from './userSlice';

// 각 slice를 스프레드 연산자로 합쳐서 하나의 스토어를 생성.
export const useBoundStore = create((set, get) => ({
  ...createCountSlice(set, get),
  ...createUserSlice(set, get),
}));
```

Immer 미들웨어 적용
immer를 사용하면 깊게 중첩된(nested) 객체의 상태를 불변성 유지에 대한 걱정 없이 직접 수정하는 것처럼 편리하게 다룰 수 있음.

```js
// slices/userSlice.js
// immer가 적용된 slice는 set 대신 draft를 받아 직접 수정.
export const createUserSliceWithImmer = set => ({
  user: {
    name: null,
    address: { city: null, street: null },
  },
  setCity: newCity =>
    set(draft => {
      // 깊은 객체도 new Object(), ...spread 없이 바로 수정 가능.
      draft.user.address.city = newCity;
    }),
});

// stores/useBoundStore.js
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer'; // immer 미들웨어 임포트
// ... 다른 slice 임포트

// 최종 스토어 생성 시 create 함수를 immer 미들웨어로 감쌈.
export const useBoundStore = create(
  immer((set, get) => ({
    ...createCountSlice(set, get),
    ...createUserSliceWithImmer(set, get),
  }))
);
```

Persist 미들웨어 적용 (부분 저장)
persist 미들웨어를 사용해 스토리지에 상태를 저장할 때, partialize 옵션을 통해 저장할 상태만 선택적으로 고를 수 있음. 이는 함수를 포함한 actions 객체 등을 제외하는 데 핵심적임.

```js
// stores/useBoundStore.js
import { create } from 'zustand';
import { persist } from 'zustand/middleware'; // persist 임포트
import { createCountSlice } from './countSlice';
import { createUserSlice } from './userSlice';

export const useBoundStore = create(
  // 1. persist 미들웨어로 전체 스토어 생성 로직을 감쌈.
  persist(
    (set, get) => ({
      ...createCountSlice(set, get),
      ...createUserSlice(set, get),
    }),
    {
      // 2. 스토리지에 저장될 고유한 이름 (필수)
      name: 'app-storage',

      // 3. (핵심) 저장할 상태를 선택하는 함수.
      //    전체 state 객체를 받아서, 저장하고 싶은 값만 포함된 객체를 반환.
      partialize: state => ({
        count: state.count, // count 슬라이스의 'count'는 저장.
        user: state.user, // user 슬라이스의 'user' 객체 전체를 저장.
        // 액션(함수)들은 partialize 결과에 포함되지 않았으므로 스토리지에 저장되지 않음.
      }),
    }
  )
);
```
