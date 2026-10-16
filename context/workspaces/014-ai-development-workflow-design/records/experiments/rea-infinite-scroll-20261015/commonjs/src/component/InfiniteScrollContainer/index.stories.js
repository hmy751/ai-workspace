"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.InfiniteScroll = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const react_query_1 = require("@tanstack/react-query");
const fetcher_1 = __importDefault(require("../../api/fetcher"));
const Grid_1 = __importDefault(require("../Grid"));
const Card_1 = __importDefault(require("../Card"));
const ImageBox_1 = __importDefault(require("../ImageBox"));
const index_1 = __importDefault(require("./index"));
const meta = {
    title: 'Common/InfiniteScrollContainer',
    component: index_1.default,
    parameters: {
        layout: 'padded',
    },
    tags: ['autodocs'],
};
exports.default = meta;
exports.InfiniteScroll = {
    render: () => {
        const { data, isLoading, isError, hasNextPage, isFetchingNextPage, fetchNextPage } = (0, react_query_1.useInfiniteQuery)({
            queryKey: ['products'],
            queryFn: async ({ pageParam = 1 }) => {
                const response = await fetcher_1.default.get(`products?skip=${(pageParam - 1) * 20}&limit=20`);
                return response.products.map(p => ({ ...p, name: p.title, price: `${p.id * 100}` }));
            },
            getNextPageParam: (lastPage, allPages) => {
                return lastPage.length === 20 ? allPages.length + 1 : undefined;
            },
            initialPageParam: 1,
        });
        return ((0, jsx_runtime_1.jsxs)("div", { children: [(0, jsx_runtime_1.jsx)("h1", { style: { marginBottom: '2rem', fontSize: '2.5rem' }, children: "Our Products" }), (0, jsx_runtime_1.jsx)(index_1.default, { data: data, isLoading: isLoading, isError: isError, hasNextPage: !!hasNextPage, isFetchingNextPage: isFetchingNextPage, fetchNextPage: fetchNextPage, loadingComponent: (0, jsx_runtime_1.jsx)("p", { style: { fontSize: '1.2rem', color: '#555' }, children: "Loading products..." }), endComponent: (0, jsx_runtime_1.jsx)("p", { style: { fontSize: '1.2rem', color: '#555' }, children: "\uBAA8\uB4E0 \uC0C1\uD488\uC744 \uB458\uB7EC\uBCF4\uC168\uC2B5\uB2C8\uB2E4!" }), children: products => ((0, jsx_runtime_1.jsx)(Grid_1.default, { columns: { base: 2, md: 3, lg: 4 }, gap: '24px', children: products.map((product) => ((0, jsx_runtime_1.jsxs)(Card_1.default, { variant: "product", children: [(0, jsx_runtime_1.jsx)(ImageBox_1.default, { src: product.thumbnail, alt: product.name, aspectRatio: "4/5" }), (0, jsx_runtime_1.jsxs)("div", { style: { padding: '16px' }, children: [(0, jsx_runtime_1.jsx)("h3", { style: {
                                                margin: 0,
                                                fontSize: '16px',
                                                whiteSpace: 'nowrap',
                                                overflow: 'hidden',
                                                textOverflow: 'ellipsis',
                                            }, children: product.name }), (0, jsx_runtime_1.jsx)("p", { style: { margin: '8px 0 0', fontSize: '14px', fontWeight: 'bold' }, children: product.price })] })] }, product.id))) })) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map