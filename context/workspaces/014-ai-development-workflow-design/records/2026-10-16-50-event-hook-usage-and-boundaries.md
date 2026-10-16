# 이벤트 Hook의 실제 호출과 책임

2026-10-16. 사용자가 주문 공통화 기준에 동의하고 이벤트 Hook의 실제 사용 코드로 진행하도록 요청했다. 첫 설명은 useClickOutsideEffect에 집중하고 useFloatingPosition은 연결 역할만 구별한다. 분석만 수행했으며 제품 수정·실행 검증은 없다.

## 근거

루트 `/Users/hammyeong-yeon/Desktop/20_lab/template`의 실제 파일을 읽었다.

- `src/component/Dropdown/index.stories.tsx:19`: 선택 값과 onChange, Trigger·Menu·Item을 합성하는 Storybook 사용처.
- `src/component/Dropdown/index.tsx:46`: Root가 isOpen과 DOM 요소를 소유하고 위치 Hook 및 외부 입력 Hook을 호출한다.
- `src/component/MultiSelect/index.tsx:72`: 같은 외부 입력 Hook에 triggerElement와 menuElement를 전달하고 setIsOpen(false)를 연결한다.
- `src/hooks/useClickOutsideEffect.ts`: document mousedown·touchstart 등록과 cleanup, 내부 포함 여부 판별, 외부 입력 시 handler 실행.
- `src/hooks/useFloatingPosition.ts`: 열린 상태와 두 DOM 요소가 있을 때 위치를 계산하고 resize·scroll 이벤트로 재계산, cleanup에서 해제한다.
- `src/component/Portal.tsx`: 기본 portal-root를 body 아래에 생성하거나 기존 노드를 사용한다. Dropdown Menu는 이 Portal에 렌더링된다.

## 호출과 책임

```ts
useClickOutsideEffect([menuElement, rootRef.current], () => setIsOpen(false));
```

Dropdown은 어느 DOM 영역을 내부로 취급할지와 바깥 입력 뒤 닫는다는 정책을 결정한다. Hook은 document 이벤트 연결·해제와 대상 포함 판별을 맡고 Dropdown 상태나 닫기 자체를 소유하지 않는다. 메뉴가 별도 portal에 놓이므로 root와 menu를 함께 대상으로 전달한다. 일반 Dropdown 사용처는 값·변경 콜백과 UI 합성을 알면 되고 내부 document 리스너의 연결은 몰라도 된다. Hook을 직접 쓰는 구성요소는 대상 영역과 callback을 제공해야 한다.

## 현재 계약의 확인 지점

현재 listener는 배열 항목이 null이거나 RefObject.current가 없으면 그 이벤트 판별 전체를 return한다. 준비되지 않은 항목을 건너뛰고 나머지만 검사하는 구현이 아니다. 모든 요소가 존재하고 입력 대상이 어느 요소 안에도 없을 때 handler를 실행한다. Dropdown은 닫힌 동안 menu가 렌더링되지 않아 null이 될 수 있다. Hook에는 isOpen·enabled 인자가 없고 배열 길이가 있으면 document 리스너를 등록하므로, 닫힌 상태의 판별 생략은 현재 null 처리와 연결된다.

배열·callback이 effect 의존성이고 호출부는 매 렌더 새 배열·함수를 전달한다. 재연결 가능성을 코드 관찰로 구별하되 이번에 성능 문제·useCallback 의무를 판정하지 않는다. 일부 요소 부재를 판단 보류로 볼지 준비된 영역만 검사할지는 사용 조건에 따라 달라질 수 있다. 사용자 선호나 수정 지시는 아직 없다.

핵심은 이벤트 연결의 기계적인 처리와 사용처의 영역·행동 정책을 나누고, null·활성 시점 같은 입력 조건의 의미도 계약으로 명확히 하는 것이다. 이 기준은 이번 관찰에서 제안한 적용점이며 사용자가 이미 채택한 것으로 해석하지 않는다.


## null 처리에 대한 사용자 회고

모든 대상이 준비될 때까지 판별하지 않는 현재 방식과, 준비된 대상만으로 판별하는 대안을 비교해 당시 의도를 물었다. 사용자:

> 뭐 만들시점에는 전달한 영역이 모두 준비되어야 동작한다 의도였던것 같은데 음 뭐 2번도 완전 틀린걸로 보이진 않긴하네

현재 코드는 사용자가 회고한 의도와 부합한다. 다만 “의도였던것 같은데”라는 기억의 강도를 유지하며 당시 요구를 확정된 사실로 강화하지 않는다. 준비된 영역만으로 동작하는 대안도 다른 요구에서 가능한 선택지로 받아들였으며, 현재 방식의 변경 요청은 없다.

이번 사례의 판단은 null을 단순히 무시해야 할 값으로 처리하지 않고, 해당 기능에서 준비되지 않음과 선택적 부재 중 무엇을 의미하는지 확인해야 한다는 것이다. 모든 Hook에 동일한 null 정책을 적용하거나 enabled 옵션을 추가하는 규칙으로 확대하지 않는다. 이 null 분기에 대해서는 별도 수정 결정을 요구하지 않고, 다음으로 useFloatingPosition의 실제 호출·계산·이벤트 수명을 볼 수 있다.


## useFloatingPosition의 실제 사용과 책임

사용자 요청으로 같은 Dropdown의 위치 Hook을 이어 읽었다. `src/component/Dropdown/index.tsx:54`는 triggerElement·menuElement·isOpen을 전달한다. Trigger의 callback ref는 버튼 DOM을 state에 넣고 Menu의 ref={setMenuElement}는 메뉴 DOM을 state에 넣는다. Root의 반환 스타일은 Context를 거쳐 Menu의 ul에 style={positionStyles}로 적용된다. Menu는 isOpen일 때만 Portal에서 렌더링된다.

`src/hooks/useFloatingPosition.ts:27`의 effect는 열림 상태와 두 요소가 모두 준비되면 초기 계산을 수행하고 resize·scroll 이벤트에 같은 계산 함수를 등록한다. scroll은 capture=true로 등록하고 cleanup에서 동일한 옵션으로 제거한다. 닫힘·요소·gap 변경 및 unmount 시 이전 effect의 리스너를 정리하는 구조다. gap 기본값은 4px다.

calculatePosition은 DOM 측정과 계산, setStyles를 함께 수행한다. 버튼 rect, 메뉴 offsetHeight, window 높이를 읽고 기본 아래 배치, 아래쪽 공간 부족 시 위 배치, 버튼 왼쪽 정렬과 minWidth를 계산한다. viewport rect에 scrollX/Y를 더한 문서 기준 좌표를 absolute 스타일로 반환한다. 위치 계산은 별도 순수 함수로 분리되지 않았고 이벤트 수명과 함께 한 Hook에 있다. 단일 위치 기능을 위해 함께 바뀌는 코드이므로 분리 여부를 역할 개수만으로 판정하지 않는다.

Dropdown은 어떤 DOM을 기준으로 삼을지, 언제 메뉴를 열고 닫을지, Portal 위치와 반환 스타일 적용을 맡는다. Hook은 좌표 측정·배치 정책·재계산 이벤트와 정리를 맡는다. 일반 Dropdown 사용처는 이 내부 이벤트를 직접 다룰 필요가 없다. Hook 직접 사용처는 실제 DOM·열림 상태·간격·style 적용과 문서 기준 absolute 좌표에 맞는 배치 환경을 알아야 한다. Portal을 빼고 positioned 부모 아래로 옮기면 같은 좌표를 그대로 적용할 수 있다는 보장은 없다. isOpen=false일 때 Hook이 DOM을 숨기지는 않으며 반환 스타일은 이전 값이 남을 수 있고, 표시 여부는 실제 Menu의 조건부 렌더링이 맡는다.

현재 자동 재계산은 effect 입력 변경과 resize·scroll에 한정된다. 동일 DOM에서 내용만 바뀌어 메뉴 높이가 변하면 그 변화 자체를 감지하는 ResizeObserver는 없다. 수평 넘침·위아래 모두 부족한 경우를 해결하는 일반 배치 엔진도 아니다. 이들은 지원 범위 관찰이며 실제 사용 요구나 확인된 화면 결함으로 승격하지 않는다. 코드 읽기만 수행했고 수정·실행 검증·새로운 사용자 정책 선택은 없다.


## 위치 Hook의 목적·지원 범위에 대한 사용자 회고

> 만들 때는 Dropdown이나 MultiSelect에서 쓸 정도로 생각했던 것 같아. 툴팁이나 팝오버까지 다 고려한 건 아니고 필요하면 확장하면 되는 거지. 이것도 결국 목적에 맞는 범위를 정하는 거겠네.

사용자는 당시 Dropdown·MultiSelect 사용 정도를 생각했던 것 같다고 회고했고, 툴팁·팝오버를 포함한 일반 배치 기능은 필요할 때 확장한다는 입장을 밝혔다. 목적에 맞는 지원 범위를 정한다는 기준에 동의한 것이며, 당시 요구를 모두 재구성했거나 현재 코드의 모든 정확성을 검증한 것은 아니다.

검토에서는 현재 목적 안에서 필요한 동작과 다른 사용처로 확장할 때 필요한 기능을 구별한다. 다른 종류의 UI까지 지원하지 않는다는 이유만으로 현재 구현을 결함으로 판정하지 않는다. 반대로 Dropdown·MultiSelect의 실제 요구에서도 발생하는 문제라면 제한된 목적을 이유로 무시하지 않는다. 확장 요구가 생기면 그때 입력·좌표·재계산 조건의 계약을 다시 판단한다. 지금 범용 옵션이나 라이브러리 도입을 요구하지 않는다.

이벤트 Hook 사례는 현재 설명과 회고를 기록한 지점으로 정리한다. 다음 추천은 계획 42의 날짜·데이터 변환 예제에서 입력 단위·경계값·반환 의미를 살펴보는 것이다. `src/utils/date.md`는 Markdown 예제이며 실제 제품 함수로 단정하지 않는다. 다음 진행은 아직 추천이고 01-02 전체 완료는 아니다.
