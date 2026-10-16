# 주문 mutation의 요청·캐시·업무·화면 책임

2026-10-16. 사용자가 template 주문 mutation 예제의 실제 코드부터 캐시 갱신·장바구니 정리·화면 이동의 현재 책임과 다른 화면에서 재사용할 때의 공통 범위를 비교해 달라고 요청했다. 분석·설명용 대안이며 제품 수정·실행 검증·사용자 선택은 없다.

## 근거와 현재 코드

원자료는 `/Users/hammyeong-yeon/Desktop/20_lab/template/src/store/react-query/index.md:135`의 Markdown 예제다. 완성된 제품 기능·파일 배치·별도 Hook 구현이 확인된 것은 아니다. http·clearCart·navigate 및 타입의 정의는 이 코드 조각에 없으므로 실제 앱 계약으로 단정하지 않는다.

```ts
onSuccess: response => {
  queryClient.invalidateQueries({ queryKey: ['orders'] });
  queryClient.invalidateQueries({ queryKey: ['catalog'] });
  clearCart();
  navigate(`/order-complete?orderId=${response.orderId}`);
}
```

mutationFn은 http.post로 요청을 맡기고 위 콜백이 성공 뒤 처리를 조율한다. 캐시를 관리하는 도구는 QueryClient, 장바구니의 실제 변경은 clearCart, 이동은 navigate가 수행한다. 호출부가 이 모두의 실행을 결정한다. await가 없으므로 캐시 무효화 호출 다음에 즉시 clearCart·navigate를 호출하며 재조회 완료를 기다리는 코드가 아니다.

## 설명용 비교와 조건

대안은 파싱된 OrderResponse를 반환하는 requestOrder(body)라는 요청 함수를 가정하고 useCreateOrder(onCreated)에서 mutationFn과 orders·catalog 캐시 무효화를 공유한다. 기존처럼 무효화 완료를 기다리지 않고 onCreated(response)를 호출한다. 장바구니 화면은 onCreated에서 clearCart와 완료 화면 이동을, 바로 구매 화면은 장바구니를 건드리지 않고 모달 닫기·자기 화면의 완료 표시를 선택하는 가상 비교다. 두 화면이 실제 template에 구현되어 있다는 뜻은 아니다. 실패 안내는 이 성공 처리 비교에서 생략했으며 제거 정책을 제안한 것은 아니다.

- 캐시 무효화는 주문 생성이 해당 데이터를 바꾼다는 도메인 관계가 여러 사용처에서 같을 때 공통화한다. 예제의 orders·catalog를 유지했지만 catalog가 실제로 영향을 받는지는 프로젝트 계약으로 확인해야 한다. 무조건 모든 캐시를 갱신하는 규칙이 아니다.
- 장바구니 정리는 모든 주문 생성에 필수인지는 별도다. 장바구니를 거친 주문 흐름의 규칙이라면 그 흐름이 소유한다. 같은 흐름이 여러 화면에서 반복되면 useCheckoutOrder 같은 기능 단위로 요청·캐시·정리를 묶을 수 있다. 단순히 UI와 가까워 보인다는 이유로 화면마다 복제하지 않는다.
- 화면 이동은 목적지가 달라지는 사용처에서 선택한다. 모든 호출이 같은 완료 화면으로 가는 전용 흐름이면 함께 묶는 것도 가능하다.
- 한 화면에서만 쓰이고 항상 네 동작이 함께 필요한 현재 목적이라면 기존 onSuccess에 모인 코드도 자연스럽다. 공통 Hook이나 새 파일 생성 자체가 개선의 근거는 아니다.
- 사용처는 공통 Hook이 보장하는 요청·캐시 처리를 알고 자기 흐름의 정리·완료 표시를 연결한다. 모든 코드를 매번 직접 처리하는 것과 모든 동작이 자동으로 따라오는 것 사이의 경계를 필요에 맞게 선택한다.

## 순서와 검증 한계

캐시 무효화 Promise를 반환·await하도록 바꾸면 onSuccess 완료와 pending 수명도 달라질 수 있다. 위치 분리와 이 동작 변경은 구별한다. [TanStack Query v5 공식 문서](https://tanstack.com/query/latest/docs/framework/react/guides/invalidations-from-mutations)를 2026-10-16 확인했다. 문서의 의존 내용은 onSuccess가 Promise를 반환하면 그 이행까지 isPending이 유지된다는 것이다. 다른 mutation 문서·reference 접근은 도구 오류로 실패했으며 그 결과에 근거한 주장은 하지 않는다.

현재는 코드 관찰과 비교 제안이다. 주문 도중 장바구니가 바뀌는 경우·부분 구매·실패별 제품 정책을 이미 결정했다고 해석하지 않는다. 사용자와 공통 범위의 판단을 이어가되 세부 API 설계 자체를 목표로 확대하지 않는다.


## 사용자 판단

> 맞아 같은 API를 쓴다고 다 묶는 게 아니라 같은 업무 흐름인지 보고 공통 범위를 정하면 되겠네. 이것도 기준으로 기록하고 다음엔 이벤트 Hook 실제 사용 코드부터 보자.

사용자는 API 호출의 동일성보다 같은 업무 흐름인지 보고 공통 범위를 판단한다는 기준에 동의했다. 특정 useCreateOrder·useCheckoutOrder API나 파일 분할을 채택한 것은 아니다. 다음은 사용자 지시로 이벤트 Hook의 실제 사용 코드이며 기록 50에서 이어간다.
