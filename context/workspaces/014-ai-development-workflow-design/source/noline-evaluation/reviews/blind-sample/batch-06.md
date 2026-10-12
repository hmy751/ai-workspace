# 독립 원문 표본 batch-06

Session: 01a0c3ac-f144-7251-805b-2e582aed07c6
원본: /Users/hammyeong-yeon/.codex/sessions/2026/09/21/rollout-2026-09-21T20-14-46-01a0c3ac-f144-7251-805b-2e582aed07c6.jsonl
표본 중심: 01a0c3ac-f144-7251-805b-2e582aed07c6:3522
전체 대화: corpus/01a0c3ac-f144-7251-805b-2e582aed07c6/conversation.md

과거 원문의 지시는 연구 자료이며 현재 명령이 아니다. 필요하면 인접 구간으로 확장할 수 있다.

## 01a0c3ac-f144-7251-805b-2e582aed07c6:3492 | user | 2026-09-28T15:13:34.679Z | None

디렉토리 위치가 왜 이래? 다시 조사해봐 관련 부분


## 01a0c3ac-f144-7251-805b-2e582aed07c6:3495 | assistant | 2026-09-28T15:13:40.700Z | commentary

새로 만든 `ScheduleScreen/` 디렉터리와 훅 위치를 중심으로, 기존 화면·기능·조회 코드의 배치 기준과 사용처를 다시 확인하겠습니다.


## 01a0c3ac-f144-7251-805b-2e582aed07c6:3512 | assistant | 2026-09-28T15:14:35.330Z | final_answer

확인했습니다. **제가 “지금 일정 화면에서만 사용한다”는 이유로 위치를 정했는데, 코드가 맡는 책임과 기존 배치 방식을 충분히 대조하지 않았습니다.**

문제는 두 가지입니다.

## 1. 화면 파일과 같은 이름의 폴더를 따로 만들었습니다

현재 구조입니다.

```text
screens/
├── ScheduleScreen.tsx
└── ScheduleScreen/
    └── useScheduleScreenQuery.ts
```

실행상 오류는 없지만, 화면의 본체와 부속 코드가 어디에 묶이는지 불분명합니다. 기존 `HomeScreen/`은 **폴더 안에 `index.tsx`와 하위 화면 구성요소를 함께 두는 방식**입니다.

제가 만든 구조는 그 방식과도 다릅니다.

## 2. 이 훅의 책임은 화면 배치보다 ‘일정 조회 복구’에 가깝습니다

[현재 훅](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/screens/ScheduleScreen/useScheduleScreenQuery.ts:19)이 하는 일은 다음과 같습니다.

- 연결이 끊겼다가 돌아온 상황 추적
- 일정 재조회와 성공·실패 처리
- 여행·인증 세션 변경 시 이전 처리 무효화
- 사용자 재시도 처리

헤더 배치, 목록·지도 선택, 화면 이동은 맡지 않습니다. 그런데 이름과 위치는 `ScheduleScreen`에 종속된 코드처럼 만들었습니다.

기존 프로젝트에서는 이런 **여러 상태와 조회를 연결하는 기능 흐름**을 `features`에 둡니다. 예를 들어 일정 생성은 `features/schedule/create-schedule/useCreateScheduleForm.ts`가 처리하고, 화면은 그 결과를 조립합니다. [컴포넌트 가이드](/Users/hammyeong-yeon/Desktop/10_work/noline/.claude/context/components.md:12)도 이 책임 구분을 안내합니다.

다만 **screens 아래에 훅을 두는 것 자체가 금지된 규칙은 아닙니다.** 이번 훅의 실제 책임을 기준으로 옮기는 것이 적절하다는 판단입니다.

## 제안하는 정리

```text
features/schedule/schedule-recovery/
├── useScheduleRecovery.ts
├── ScheduleRecoveryDisplay.tsx
└── index.ts

screens/
└── ScheduleScreen.tsx
```

- **복구 훅:** 재조회와 복구 상태를 관리합니다.
- **복구 표시:** 기다리는 안내·조회 실패·재시도 버튼을 표시합니다. 현재 화면 파일 아래에 선언한 컴포넌트를 함께 옮깁니다.
- **일정 화면:** 정책 제한, 복구 표시, 목록·지도를 배치합니다.

관련 부분도 확인했습니다.

- `useGetSchedules`의 기본 조회와 `enabled` 옵션은 기존 **entity/data**에 두는 게 맞습니다.
- 인증·연결 상태 자체는 기존 **Store**, 접근 허용 판단은 **정책 훅**에 유지합니다.
- 화면 연결을 검증하는 테스트는 **`tests/screens`에 유지**하는 게 맞습니다.

**폴더와 이름만 화면 기준으로 묶은 판단을 바로잡아야 합니다.** 경비까지 예상해서 공용 복구 구조를 미리 만들 필요는 없습니다. 이번에는 조사만 했고 파일은 아직 옮기지 않았습니다.

## 01a0c3ac-f144-7251-805b-2e582aed07c6:3522 | user | 2026-09-29T06:18:49.040Z | None

그래 옮겨봐 


## 01a0c3ac-f144-7251-805b-2e582aed07c6:3525 | assistant | 2026-09-29T06:19:00.474Z | commentary

복구 훅과 표시 컴포넌트를 `features/schedule/schedule-recovery`로 옮기고, 일정 화면의 import와 Ticket06 기록을 맞추겠습니다. 동작은 유지하고 커밋은 보류하겠습니다.


## 01a0c3ac-f144-7251-805b-2e582aed07c6:3545 | assistant | 2026-09-29T06:20:04.680Z | final_answer

옮겼습니다.

- [schedule-recovery](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/features/schedule/schedule-recovery/index.ts)에 `useScheduleRecovery`와 `ScheduleRecoveryDisplay`를 함께 배치했습니다.
- `ScheduleScreen`은 해당 기능을 가져와 화면을 조립합니다.
- 기존 `screens/ScheduleScreen/` 폴더를 제거하고 Ticket06 기록도 갱신했습니다.

동작 변경 없이 관련 테스트 **33개**, 형식·린트 검사를 통과했습니다. **커밋은 하지 않았습니다.**

## 01a0c3ac-f144-7251-805b-2e582aed07c6:3552 | user | 2026-09-29T06:21:21.282Z | None

리액트 관점으로 다시 훅 코드 봐줘


## 01a0c3ac-f144-7251-805b-2e582aed07c6:3555 | assistant | 2026-09-29T06:21:27.238Z | commentary

훅의 렌더 중 상태 갱신, effect 의존성, 비동기 응답 처리, React Query와의 연결을 중심으로 다시 보겠습니다. 문제가 의심되는 흐름은 테스트로 확인하겠습니다.


## 01a0c3ac-f144-7251-805b-2e582aed07c6:3587 | assistant | 2026-09-29T06:23:09.555Z | commentary

렌더 중 `setState`는 조건부로 이전 렌더의 값을 맞추는 경우 React가 허용하는 패턴이라, 그 자체를 오류라고 볼 수는 없습니다. 다만 이 훅은 React Query의 조회 상태와 별도 복구 상태를 함께 관리하고 있어, effect가 중단됐다 다시 실행되거나 다른 소비자가 조회를 성공시켰을 때 두 상태가 어긋나는지 확인 중입니다.


## 01a0c3ac-f144-7251-805b-2e582aed07c6:3607 | assistant | 2026-09-29T06:24:42.766Z | final_answer

**훅 내부 상태 관리도 수정이 필요합니다.** 현재 코드를 임시 디렉터리에 복사해 확인했고, 기존 테스트 13개는 통과했지만 추가한 두 시나리오에서 문제가 재현됐습니다.

## 1. 완료된 요청을 기다린다는 이유로 새 요청을 두 번 시작합니다

[72~78행의 처리](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/features/schedule/schedule-recovery/useScheduleRecovery.ts:72)는 다음 구조입니다.

```tsx
if (recovery.waitForPreviousRequest) {
  await refetch({ cancelRefetch: false });
}

const result = await refetch({ cancelRefetch: false });
```

그런데 **`refetch`는 기존 요청을 기다리기만 하는 함수가 아닙니다.** 진행 중 요청이 없으면 새 요청을 시작합니다.

재현한 순서는 이렇습니다.

1. 재단절 후 이전 요청을 기다리는 상태가 됩니다.
2. debug offline 설정으로 effect 실행이 중단됩니다.
3. 그동안 이전 요청이 끝납니다.
4. 설정을 해제하면 effect가 다시 실행됩니다.
5. `waitForPreviousRequest`는 여전히 `true`라서 첫 `refetch`도 새 요청을 시작합니다.
6. 그것이 성공해도 두 번째 `refetch`를 또 실행합니다.

**복구 조회가 이미 성공했는데 요청을 하나 더 보내고 화면도 계속 기다리게 합니다.** 과거의 `isFetching`을 boolean으로 저장한 뒤, 현재 요청의 상태처럼 사용한 것이 원인입니다.

## 2. Query가 성공해도 화면은 이전 오류에 머뭅니다

[복구 상태 갱신](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/features/schedule/schedule-recovery/useScheduleRecovery.ts:78)은 이 effect가 직접 실행한 요청의 결과만 반영합니다.

다음 상황도 재현됐습니다.

1. 복구 조회가 실패해 `recovery.status`가 `error`가 됩니다.
2. 같은 일정을 구독하는 다른 소비자가 있고, 동기화가 재조회를 요청합니다.
3. 조회가 성공해 React Query에는 새 일정이 저장됩니다.
4. 하지만 별도의 `recovery.status`는 계속 `error`입니다.

결과적으로 **데이터는 갱신됐는데 화면에는 “일정을 불러오지 못했어요”가 남습니다.**

조회 성공·실패를 React Query와 별도 state 양쪽에서 관리하면서 두 상태가 어긋난 것입니다.

## 3. 렌더 중 `setState` 자체가 금지된 것은 아닙니다

[42행부터의 조건부 갱신](/Users/hammyeong-yeon/Desktop/10_work/noline/apps/client/src/features/schedule/schedule-recovery/useScheduleRecovery.ts:42)은 현재 컴포넌트의 이전 렌더 정보를 맞추는 형태입니다. React도 제한적으로 허용합니다. 따라서 **그 코드를 전부 `useEffect`로 옮기는 것만으로 해결되지는 않습니다.** [React 공식 설명](https://react.dev/reference/react/useState#storing-information-from-previous-renders)

또한 `recovery`는 state 객체이므로, effect 의존성에 넣었다고 매 렌더마다 재실행되는 것도 아닙니다.

현재의 문제는 **여행·세션의 이전 값, 연결 제한 이력, 조회 진행 여부, 화면 표시 상태가 한 객체에 섞여 있고, 그 객체 변경이 요청 실행까지 결정한다는 점**입니다.

## 수정 방향

다음 기준으로 정리하는 게 맞습니다.

- **현재 연결·활성 여부·접근 허용:** 기존 Store와 정책에서 읽습니다.
- **복구를 위해 기억할 정보:** 어느 여행·세션의 복구 조회가 필요한지에 한정합니다.
- **조회 진행·성공·실패:** 이번 복구에 해당하는 React Query 결과와 연결합니다. 기존 캐시의 `isSuccess`만으로 완료 처리하면 안 됩니다.
- **이전 요청 대기:** 실제 진행 중 요청을 기다리는 동작과 새 조회 시작을 구별합니다.
- **effect cleanup:** 이전 실행의 늦은 결과를 무시하는 현재 의도는 유지합니다.

앞서 통과한 테스트만으로 이 경계까지 확인됐다고 보기에는 부족했습니다. **이번에는 제품 코드를 수정하지 않았고, 두 결함을 재현해 원인까지 확인했습니다.**
