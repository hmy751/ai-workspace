# 무한 스크롤 사용 코드의 책임과 변경 범위

2026-10-13. 사용자는 Field 기준을 남긴 뒤 같은 템플릿의 무한 스크롤로 이어가자고 했고, 다음과 같이 요청했다.

> 좋아 실제 사용 코드부터 보여주면서 각자 뭘 맡고 어디까지 자유롭게 바꿀 수 있는지 보자

현재 구현을 읽어 책임과 공개된 변경 범위를 설명하는 단계다. 사용자 의도나 선호, 변경할 구조는 아직 확인하지 않았다.

## 사용 코드에서 확인한 책임

원자료는 `/Users/hammyeong-yeon/Desktop/20_lab/template`의 다음 세 파일이다. 실제 실행·설치·수정은 하지 않았다.

| 파일 | 현재 책임 |
| --- | --- |
| `src/component/InfiniteScrollContainer/index.stories.tsx` | useInfiniteQuery 호출과 queryKey, 상품 요청, 응답 변환, 페이지 계산을 정의한다. 컨테이너에 데이터·상태·추가 조회 함수를 전달한다. children 함수에서 Grid·Card·Image로 전체 목록을 구성한다. |
| `src/component/InfiniteScrollContainer/index.tsx` | 관찰 Hook을 연결하고 페이지 배열을 하나로 펼친다. 초기 로딩·오류·빈 목록은 각각 해당 표시만 반환한다. 정상 목록과 그 아래 관찰 요소를 렌더링하고, 추가 로딩·끝 표시를 관찰 요소 안에 둔다. |
| `src/hooks/useInfiniteScrollObserver.ts` | IntersectionObserver를 생성·연결·해제한다. enabled, 교차 여부, 다음 페이지 존재, 추가 조회 여부를 확인한 뒤 전달받은 함수를 호출한다. 데이터 조회 구현이나 목록 UI는 소유하지 않는다. |

현재 story의 다음 페이지 판단은 마지막 페이지 항목 수가 20이면 다음 번호를 반환하는 방식이다. 전체 개수나 서버 커서를 사용하는 계약으로 검증한 것은 아니다.

## 사용처에 열린 부분과 컨테이너가 결정하는 부분

| 변경 | 현재 인터페이스에서의 범위 |
| --- | --- |
| 상품 대신 다른 데이터 조회, 페이지 번호 대신 커서 사용 | 조회·페이지 계산은 사용처에서 정의한다. 컨테이너에 전달하는 각 page는 항목 배열이어야 한다. |
| Grid를 다른 목록 배치로 변경, Card·Image 교체 | children 함수가 전체 items를 받으므로 사용처가 목록 JSX를 구성한다. 컨테이너는 특정 Grid·Card를 요구하지 않는다. |
| 로딩·오류·빈 목록·끝의 문구나 컴포넌트 변경 | 각각 ReactNode를 받는 props로 교체한다. 표시 조건·위치까지 props로 제어하는 것은 아니다. |
| 기존 목록을 유지하면서 추가 조회 오류를 아래에 표시 | 현재 `isError`이면 errorComponent만 반환한다. 그 조건에서 목록을 함께 렌더링하려면 다른 조합이나 컨테이너의 표시 정책 변경이 필요하다. |
| 초기 로딩과 추가 로딩에 서로 다른 UI 사용 | 현재 두 위치에 같은 loadingComponent를 쓴다. 별도의 두 입력은 없다. 사용처의 상태별 JSX 계산 등 우회 가능성과 별개로 현재 공통 API가 두 슬롯을 제공하지는 않는다. |
| 관찰 범위 설정 | observerOptions를 Hook에 전달한다. 관찰 요소 자체는 Container의 목록 뒤 div로 정해져 있으며 외부 ref로 직접 지정하는 API는 없다. |
| React Query 대신 다른 요청 도구 사용 | Container·Hook은 React Query를 import하지 않는다. 데이터·boolean 상태·함수 계약에 맞춰 연결하는 방식은 인터페이스상 가능하다. 다른 도구로 실행 검증한 것은 아니다. |

핵심 코드 근거:

```tsx
interface InfiniteScrollData<T> {
  pages: T[][];
}

if (isError) {
  return <>{errorComponent}</>;
}

const items = data?.pages.flatMap(page => page) ?? [];
```

목록과 하단 표시의 배치:

```tsx
{children(items)}
<div ref={loadMoreRef} style={{ height: '1px', padding: '2rem 0' }}>
  {isFetchingNextPage && loadingComponent}
  {!isFetchingNextPage && !hasNextPage && endComponent}
</div>
```

이 범위에서의 해석은 **조회 도구와 목록 디자인의 선택은 사용처에 열려 있고, 표시 조건·위치와 스크롤 감지의 기본 조합은 Container가 제공한다**는 것이다. 직접 import 여부와 데이터·상태 계약에 대한 의존성을 구별한다. 이 분리가 잘못됐거나 모든 표시를 합성형 API로 바꿔야 한다고 판정한 것은 아니다. 필요한 디자인·동작 변화에서 이 경계가 적합한지는 이후 사용자와 논의한다.

Hook만 직접 사용할 수도 있지만 그 경우 관찰할 div에 반환된 ref를 연결하고 목록·상태 표시를 사용하는 곳에서 구성해야 한다. 호출 조건의 런타임 안정성이나 전체 품질 리뷰는 이번 설명의 확인 범위가 아니다.
