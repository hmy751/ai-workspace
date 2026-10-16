"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useInfiniteScrollObserver = void 0;
const react_1 = require("react");
const useInfiniteScrollObserver = ({ hasNextPage, isFetchingNextPage, fetchNextPage, enabled = true, // 기본값은 true로 설정
observerOptions, }) => {
    const loadMoreRef = (0, react_1.useRef)(null);
    const handleObserver = (0, react_1.useCallback)((entries) => {
        const [target] = entries;
        if (enabled &&
            target?.isIntersecting &&
            hasNextPage &&
            !isFetchingNextPage) {
            fetchNextPage();
        }
    }, [enabled, hasNextPage, isFetchingNextPage, fetchNextPage]);
    (0, react_1.useEffect)(() => {
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
exports.useInfiniteScrollObserver = useInfiniteScrollObserver;
//# sourceMappingURL=useInfiniteScrollObserver.js.map