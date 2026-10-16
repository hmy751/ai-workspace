import { useCallback, useRef, useEffect } from "react";

interface UseInfiniteScrollObserverProps {
  hasNextPage: boolean;
  isFetchingNextPage: boolean;
  fetchNextPage: () => void;
  enabled?: boolean; // 훅의 활성화 여부를 제어하는 옵션
  observerOptions?: IntersectionObserverInit; // IntersectionObserver 옵션을 외부에서 받는 속성
}

export const useInfiniteScrollObserver = ({
  hasNextPage,
  isFetchingNextPage,
  fetchNextPage,
  enabled = true, // 기본값은 true로 설정
  observerOptions,
}: UseInfiniteScrollObserverProps) => {
  const loadMoreRef = useRef<HTMLDivElement | null>(null);

  const handleObserver = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [target] = entries;

      if (
        enabled &&
        target?.isIntersecting &&
        hasNextPage &&
        !isFetchingNextPage
      ) {
        fetchNextPage();
      }
    },
    [enabled, hasNextPage, isFetchingNextPage, fetchNextPage]
  );

  useEffect(() => {
    if (!enabled) {
      return;
    }

    const {
      root = null,
      threshold = 0.1,
      rootMargin = "0px",
    } = observerOptions ?? {};

    const observer = new IntersectionObserver(handleObserver, {
      root,
      threshold,
      rootMargin,
    });

    const element = loadMoreRef.current;
    if (element) {
      observer.observe(element);
    }

    return () => {
      if (element) {
        observer.unobserve(element);
      }
    };
  }, [handleObserver, enabled, JSON.stringify(observerOptions)]);

  return { loadMoreRef };
};
