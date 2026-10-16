# 무한 스크롤 Container와 Hook 직접 사용 비교

2026-10-14. 사용자 요청:

> 그럼 컨테이너를 쓰는 방식이랑 Hook만 직접 쓰는 방식을 실제 코드로 비교해보자. 어떤 편의가 생기고 어떤 자유도가 달라지는지 보고 싶어.

`/Users/hammyeong-yeon/Desktop/20_lab/template`의 `src/component/InfiniteScrollContainer/index.stories.tsx`, `index.tsx`, `src/hooks/useInfiniteScrollObserver.ts`를 다시 읽었다. 원본 수정·설치·실행은 하지 않았다. 아래는 기존 인터페이스로 만든 설명용 대비 코드다. Container 방식은 현재 사용 예시의 구조를 따르며, Hook 직접 사용은 비교용으로 펼친 안이다. 사용자 선택이나 실행 검증 결과가 아니다.

## 같은 조회·목록을 유지한 대비

두 안 모두 기존 useInfiniteQuery 설정과 반환 변수(data, isLoading, isError, hasNextPage, isFetchingNextPage, fetchNextPage)를 유지한다. `ProductList`는 기존 Grid·Card·Image 목록 JSX를 같은 이름으로 줄여 쓴 비교용 표기이며, 실제 저장소에 그 이름의 컴포넌트를 추가하지 않았다. 코드는 컴포넌트 안의 useInfiniteQuery 호출 이후 부분이다.

Container를 사용하면 데이터·상태·함수와 표시 내용을 전달한다.

```tsx
return (
  <InfiniteScrollContainer<Product>
    data={data}
    isLoading={isLoading}
    isError={isError}
    hasNextPage={!!hasNextPage}
    isFetchingNextPage={isFetchingNextPage}
    fetchNextPage={fetchNextPage}
    loadingComponent={<p>불러오는 중...</p>}
    errorComponent={<p>조회에 실패했습니다.</p>}
    emptyComponent={<p>상품이 없습니다.</p>}
    endComponent={<p>모든 상품을 봤습니다.</p>}
  >
    {products => <ProductList products={products} />}
  </InfiniteScrollContainer>
);
```

같은 표시 정책을 Hook만 사용해 펼치면 다음과 같다. Hook 호출은 조건부 return보다 앞에 둔다.

```tsx
const { loadMoreRef } = useInfiniteScrollObserver({
  hasNextPage: !!hasNextPage,
  isFetchingNextPage,
  fetchNextPage,
  enabled: !isLoading && !isError && !!hasNextPage,
});

const products = data?.pages.flatMap(page => page) ?? [];

if (isLoading) return <p>불러오는 중...</p>;
if (isError) return <p>조회에 실패했습니다.</p>;
if (products.length === 0) return <p>상품이 없습니다.</p>;

return (
  <>
    <ProductList products={products} />
    <div ref={loadMoreRef} style={{ height: '1px', padding: '2rem 0' }}>
      {isFetchingNextPage && <p>불러오는 중...</p>}
      {!isFetchingNextPage && !hasNextPage && <p>모든 상품을 봤습니다.</p>}
    </div>
  </>
);
```

이 비교에서 Container가 제공하는 편의는 감지 Hook 연결, 페이지 배열 펼치기, 상태별 분기, 하단 감지 요소와 상태 표시의 기본 배치를 사용하는 곳마다 다시 작성하지 않는 것이다. 초기·오류·빈 목록의 표시 우선순위도 Container가 맡는다. 조회 구현과 목록 내부 디자인은 두 방식 모두 사용처가 소유한다.

## 자유도가 드러나는 변경

Hook 직접 사용안에서는 이미 받은 목록이 있을 때 오류가 나도 목록을 유지할 수 있다. 위의 무조건 isError 반환을 `if (isError && products.length === 0)`으로 바꾸고, 목록 JSX 아래에 조건부 오류 문구를 추가한다. Container를 그대로 사용하는 안은 isError이면 errorComponent만 반환하므로 errorComponent의 문구만 바꿔서는 같은 동작이 되지 않는다. 오류 화면 안에 목록을 다시 넣는 등의 사용처 우회도 가능하지만, 정상 목록 렌더링과 분기가 다시 사용처에 생긴다.

초기 로딩과 추가 로딩도 Hook 직접 사용에서는 각각 다른 JSX로 작성할 수 있다. Container에서는 같은 loadingComponent를 두 위치에서 사용한다. 사용처가 isLoading에 따라 그 prop의 값을 계산하는 방법도 있으므로 '서로 다른 UI는 불가능하다'고 단정하지 않는다. 단지 별도 두 슬롯을 제공하지는 않는다.

| 비교할 내용 | Container 사용 | Hook 직접 사용 |
| --- | --- | --- |
| 조회 API·React Query 설정 | 사용처에서 결정 | 동일 |
| 목록 내부 Grid·Card·항목 구성 | children에서 결정 | 직접 JSX로 결정 |
| 감지와 추가 조회 호출 조건 | Container가 Hook을 연결 | 같은 Hook을 직접 연결 |
| 데이터 펼치기·상태 표시 우선순위 | Container의 기본 정책 사용 | 화면에서 작성·변경 |
| 관찰 요소·추가 상태 표시의 배치 | Container의 목록 뒤 div | 화면에서 div 위치·표시 구성을 결정 |
| 여러 화면에서 같은 정책 유지 | Container 수정으로 반영 | 사용처들이 직접 관리하거나 반복이 확인되면 다시 공통화 |

Hook 직접 사용도 현재 Hook의 계약(enabled·페이지 상태·함수, HTMLDivElement ref, IntersectionObserver 감지 조건)은 따른다. 모든 동작의 자유를 얻는다는 뜻은 아니다. Container 역시 React Query 직접 의존은 없지만 `pages: T[][]`와 상태·함수 입력을 요구한다. Hook 직접 사용에서는 데이터 모양은 화면에서 해석하고 Hook에는 상태·함수만 전달할 수 있다.

비교 당시 Main은 동일한 표시 정책을 쓰는 화면에는 Container가 반복을 줄이고 정책을 모으는 편의를 제공하며, 그 정책이 화면 요구와 달라질 때 Hook 직접 조합의 이점이 생긴다고 설명했다. 아래 사용자 설명으로 당시 Container를 만든 의도를 추가 확인했다. 자동 테스트·런타임 안정성·제품 효과를 확인한 것으로 읽지 않는다.

## 사용자가 밝힌 Container의 필요와 Hook 분리 확인

사용자:

> 맞아 결국 상황에 따라 다르다고 해야하나? 그러니까 저 인피니트 스크롤 훅 말고 컴포넌트를 만든건 일정 디자인 형식이 있고 필요하다 판단해서 한거고 그게 불필요하다 생각되고 재사용이 적을거라 생각하면 없애는거고 다만 내가 만든건 어느정도 형태가 있으니까 있는만큼주고 또 자유도를 줄 부분은 주고 이런거지 단순히 컨테이너는 옳다 이게 아니라
> 어쨋든 저상황에서 내가 만들 당시 생각은 컨테이너도 필요하다 생각이 돼서 그랬어  훅 분리도 좋고 근데 난 훅분리를 햇었나?

현재 파일을 다시 확인했다. `src/hooks/useInfiniteScrollObserver.ts`가 감지를 독립 Hook으로 제공하고, `src/component/InfiniteScrollContainer/index.tsx`가 이를 import해 호출하므로 이미 Hook이 분리돼 있다. 이 구조는 비교를 위해 새로 만든 것이 아니다.

사용자의 판단은 당시 존재하던 디자인 형식과 필요를 공통 컴포넌트로 제공하고, 사용하는 곳마다 달라질 부분은 열어 두는 것이다. 공통 형식이 불필요해지고 재사용할 가치가 낮다고 판단하면 컴포넌트를 없앨 수도 있다. 재사용 횟수의 고정 문턱, 무조건 Container 사용, 모든 표시를 외부에 노출하는 규칙으로 일반화하지 않는다.

따라서 이 사례에서 남길 판단은 **공통으로 제공할 형식·동작과 예상 사용의 필요를 근거로 컴포넌트의 존재·범위를 정하고, 변화할 부분에는 필요한 자유도를 제공한다**는 것이다. Hook과 Container는 둘 중 하나만 선택할 대상이 아니라, 현재도 감지 재사용과 기본 화면 조합의 책임을 나누어 함께 존재한다. 사용자가 기존 Container의 필요를 설명한 것이며 새 API나 코드 변경을 요청한 것은 아니다.
