"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const useInfiniteScrollObserver_1 = require("../../hooks/useInfiniteScrollObserver");
const InfiniteScrollContainer = ({ data, isLoading, isFetchingNextPage, hasNextPage, isError, fetchNextPage, children, loadingComponent = (0, jsx_runtime_1.jsx)("div", { children: "Loading..." }), emptyComponent = (0, jsx_runtime_1.jsx)("div", { children: "No items found." }), endComponent = (0, jsx_runtime_1.jsx)("div", { children: "You've reached the end!" }), errorComponent = (0, jsx_runtime_1.jsx)("div", { children: "An error occurred while fetching data." }), observerOptions, }) => {
    const { loadMoreRef } = (0, useInfiniteScrollObserver_1.useInfiniteScrollObserver)({
        hasNextPage: hasNextPage ?? false,
        isFetchingNextPage,
        fetchNextPage,
        enabled: !isLoading && !isError && hasNextPage,
        observerOptions,
    });
    if (isLoading) {
        return (0, jsx_runtime_1.jsx)(jsx_runtime_1.Fragment, { children: loadingComponent });
    }
    if (isError) {
        return (0, jsx_runtime_1.jsx)(jsx_runtime_1.Fragment, { children: errorComponent });
    }
    // data를 가공하여 items 배열 생성
    const items = data?.pages.flatMap(page => page) ?? [];
    // 데이터가 비어있을 경우 emptyComponent를 보여주는 로직 추가
    if (items.length === 0) {
        return (0, jsx_runtime_1.jsx)(jsx_runtime_1.Fragment, { children: emptyComponent });
    }
    return ((0, jsx_runtime_1.jsxs)(jsx_runtime_1.Fragment, { children: [children(items), (0, jsx_runtime_1.jsxs)("div", { ref: loadMoreRef, style: { height: '1px', padding: '2rem 0' }, children: [isFetchingNextPage && loadingComponent, !isFetchingNextPage && !hasNextPage && endComponent] })] }));
};
exports.default = InfiniteScrollContainer;
//# sourceMappingURL=index.js.map