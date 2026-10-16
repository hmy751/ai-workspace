import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useInfiniteScrollObserver } from '../../hooks/useInfiniteScrollObserver';
const InfiniteScrollContainer = ({ data, isLoading, isFetchingNextPage, hasNextPage, isError, fetchNextPage, children, loadingComponent = _jsx("div", { children: "Loading..." }), emptyComponent = _jsx("div", { children: "No items found." }), endComponent = _jsx("div", { children: "You've reached the end!" }), errorComponent = _jsx("div", { children: "An error occurred while fetching data." }), observerOptions, }) => {
    const { loadMoreRef } = useInfiniteScrollObserver({
        hasNextPage: hasNextPage ?? false,
        isFetchingNextPage,
        fetchNextPage,
        enabled: !isLoading && !isError && hasNextPage,
        observerOptions,
    });
    if (isLoading) {
        return _jsx(_Fragment, { children: loadingComponent });
    }
    if (isError) {
        return _jsx(_Fragment, { children: errorComponent });
    }
    // data를 가공하여 items 배열 생성
    const items = data?.pages.flatMap(page => page) ?? [];
    // 데이터가 비어있을 경우 emptyComponent를 보여주는 로직 추가
    if (items.length === 0) {
        return _jsx(_Fragment, { children: emptyComponent });
    }
    return (_jsxs(_Fragment, { children: [children(items), _jsxs("div", { ref: loadMoreRef, style: { height: '1px', padding: '2rem 0' }, children: [isFetchingNextPage && loadingComponent, !isFetchingNextPage && !hasNextPage && endComponent] })] }));
};
export default InfiniteScrollContainer;
//# sourceMappingURL=index.js.map