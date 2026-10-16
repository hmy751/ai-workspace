import { ReactNode } from 'react';
import { useInfiniteScrollObserver } from '../../hooks/useInfiniteScrollObserver';

interface InfiniteScrollData<T> {
  pages: T[][];
}

export interface InfiniteScrollContainerProps<T> {
  data?: InfiniteScrollData<T>;
  isLoading: boolean;
  isFetchingNextPage: boolean;
  hasNextPage: boolean;
  isError: boolean;
  fetchNextPage: () => void;
  children: (items: T[]) => ReactNode;
  loadingComponent?: ReactNode;
  emptyComponent?: ReactNode;
  endComponent?: ReactNode;
  errorComponent?: ReactNode;
  observerOptions?: IntersectionObserverInit;
}

const InfiniteScrollContainer = <T,>({
  data,
  isLoading,
  isFetchingNextPage,
  hasNextPage,
  isError,
  fetchNextPage,
  children,
  loadingComponent = <div>Loading...</div>,
  emptyComponent = <div>No items found.</div>,
  endComponent = <div>You've reached the end!</div>,
  errorComponent = <div>An error occurred while fetching data.</div>,
  observerOptions,
}: InfiniteScrollContainerProps<T>) => {
  const { loadMoreRef } = useInfiniteScrollObserver({
    hasNextPage: hasNextPage ?? false,
    isFetchingNextPage,
    fetchNextPage,
    enabled: !isLoading && !isError && hasNextPage,
    observerOptions,
  });

  if (isLoading) {
    return <>{loadingComponent}</>;
  }

  if (isError) {
    return <>{errorComponent}</>;
  }

  // data를 가공하여 items 배열 생성
  const items = data?.pages.flatMap(page => page) ?? [];

  // 데이터가 비어있을 경우 emptyComponent를 보여주는 로직 추가
  if (items.length === 0) {
    return <>{emptyComponent}</>;
  }

  return (
    <>
      {/* children을 함수로 호출하고, 가공된 items를 인자로 전달 */}
      {children(items)}

      {/* Observer를 위한 div */}
      <div ref={loadMoreRef} style={{ height: '1px', padding: '2rem 0' }}>
        {isFetchingNextPage && loadingComponent}
        {!isFetchingNextPage && !hasNextPage && endComponent}
      </div>
    </>
  );
};

export default InfiniteScrollContainer;
