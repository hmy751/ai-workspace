import { useCallback, useRef, useEffect } from "react";
export const useInfiniteScrollObserver = ({ hasNextPage, isFetchingNextPage, fetchNextPage, enabled = true, // 기본값은 true로 설정
observerOptions, }) => {
    const loadMoreRef = useRef(null);
    const handleObserver = useCallback((entries) => {
        const [target] = entries;
        if (enabled &&
            target?.isIntersecting &&
            hasNextPage &&
            !isFetchingNextPage) {
            fetchNextPage();
        }
    }, [enabled, hasNextPage, isFetchingNextPage, fetchNextPage]);
    useEffect(() => {
        if (!enabled) {
            return;
        }
        const { root = null, threshold = 0.1, rootMargin = "0px", } = observerOptions ?? {};
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
//# sourceMappingURL=useInfiniteScrollObserver.js.map