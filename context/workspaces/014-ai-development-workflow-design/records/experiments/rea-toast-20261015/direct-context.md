# 직접 분석으로 준비한 Toast 개발 컨텍스트

REA 결과를 읽기 전에 고정한 초안. 경로는 `input/` 기준이며 줄 번호는 원본과 같다. 실제 브라우저 실행 전 정적 분석이다.

## 책임과 사용법

Toast는 모듈 수준 Zustand store에 알림 목록을 보관하고, 마운트된 표시 컴포넌트가 각 알림의 삭제 타이머를 관리한다. 호출자는 store의 `addToast`에 title·description·duration을 넘기며, 별도로 `<Toast />`가 마운트돼 있어야 화면에 나타나고 자동 삭제가 시작된다.

| ID | 확인한 코드 사실 | 근거 |
| --- | --- | --- |
| D1 | store는 `toasts`, `addToast`, `removeToast`를 제공한다. 생성은 모듈 수준이며 각 표시 컴포넌트 내부에서 새로 만들지 않는다. | `src/store/useToastStore.ts:18` |
| D2 | 추가는 기존 배열 뒤에 새 항목을 붙인다. id는 내부 `Math.random` 기반 함수로 생성하며 호출자가 전달한 값보다 뒤에 대입한다. 삭제는 해당 id와 일치하는 항목을 필터링한다. | store 16~27 |
| D3 | Toast는 목록을 구독하고 각 항목을 id key의 ToastItem으로 표시한다. 렌더링 위치는 `document.body` portal이며 children은 별도로 렌더링한다. | `src/component/Toast/index.tsx:11`~25 |
| D4 | ToastItem에서 duration을 생략하면 5000ms를 사용한다. title과 description은 각각 값이 있을 때 렌더링한다. | Toast 29~47 |
| D5 | effect가 `setTimeout(() => removeToast(id), duration)`을 만들고 cleanup은 `clearTimeout(timer)`를 수행한다. 의존성은 duration·removeToast·id다. cleanup에 store 항목 삭제는 없다. | Toast 30~35 |
| D6 | story는 버튼 클릭으로 알림을 추가하고 `<Toast />`를 함께 렌더링한다. 예시는 duration 3000ms를 명시한다. Button은 나머지 props를 실제 button에 전달한다. | `src/component/Toast/index.stories.tsx:19`~34, `src/component/Button/index.tsx` |

## 코드와 React 계약에서 도출하는 동작

- **D7 — 상태 수명과 표시 수명이 다르다.** 표시부를 제거하면 effect 타이머는 취소되지만 store 항목은 남는 것으로 예상한다. 같은 store 인스턴스에서 다시 마운트하면 남은 항목이 다시 표시되고 duration 전체의 새 타이머가 시작될 것이다. 따라서 duration은 추가 시각부터의 절대 만료 시간이 아니다. 원본 코드에는 생성·만료 timestamp도 없다. 실제 실행으로 확인할 가설이다.
- **D8 — 표시부 없는 동안의 자동 만료는 없다.** addToast 자체에는 타이머가 없으므로, 표시부가 없을 때 추가한 항목도 이후 마운트까지 남을 것으로 예상한다. 실제 실행으로 확인할 가설이다.
- 같은 store를 구독하는 Toast를 여러 개 마운트하면 각각 표시·타이머를 갖는 구조다. 앱의 단일 표시부 배치는 이 작은 입력으로 확인하지 못했다.
- duration 변경 시 React effect 계약에 따라 이전 타이머 정리 후 재설정된다. 공개 store 액션에는 별도 update 액션이 없다.

React 계약 근거: <https://react.dev/reference/react/useEffect> (2026-10-15 확인). dependency 변경 전과 unmount 때 cleanup을 호출하며, mount 때 setup을 실행한다. 제품의 기대 동작은 이 API 계약에서 도출하지 않는다.

## 개발 판단에 쓸 조건

앱에 하나의 표시부를 계속 유지하며 ‘화면에 나타난 뒤 일정 시간 보여준다’가 목적이라면 현재 책임 배치는 설명 가능하다. 반대로 화면 이동·표시부 부재와 무관하게 ‘추가 후 N초에 만료’를 보장해야 한다면 만료 시각 또는 표시부 밖의 수명 관리가 필요하다. 요구 확인 없이 타이머를 store로 옮기는 리팩터링을 정답으로 정하지 않는다.

기간 정책을 바꾸려면 store의 데이터·액션과 ToastItem effect를 함께 검토한다. 표시 디자인은 Text·Toast 렌더링을, 호출법은 story를 진입점으로 삼는다. 무작위 id의 충돌 가능성·duration 입력 검증 부재는 관찰할 수 있지만 실제 빈도·요구를 모르므로 이번 컨텍스트에서 긴급 결함으로 올리지 않는다.

## 미확인과 다음 확인

브라우저의 실제 출력·타이밍, 전체 앱의 표시부 배치, 마운트 해제 중 알림 처리에 관한 사용자 의도, 실제 의존성 설치 버전은 이 초안에서 검증하지 않았다. 우선 정상 만료, 표시부 제거 후 재마운트, 표시부 없는 동안의 추가를 실제 React·Zustand로 확인하면 D7·D8의 상한을 높일 수 있다. 시각적 스타일·접근성의 품질 판단은 별도다.
