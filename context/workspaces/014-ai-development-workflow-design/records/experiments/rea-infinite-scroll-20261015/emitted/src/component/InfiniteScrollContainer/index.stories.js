import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useInfiniteQuery } from '@tanstack/react-query';
import fetcher from '../../api/fetcher';
import Grid from '../Grid';
import Card from '../Card';
import Image from '../ImageBox';
import InfiniteScrollContainer from './index';
const meta = {
    title: 'Common/InfiniteScrollContainer',
    component: InfiniteScrollContainer,
    parameters: {
        layout: 'padded',
    },
    tags: ['autodocs'],
};
export default meta;
export const InfiniteScroll = {
    render: () => {
        const { data, isLoading, isError, hasNextPage, isFetchingNextPage, fetchNextPage } = useInfiniteQuery({
            queryKey: ['products'],
            queryFn: async ({ pageParam = 1 }) => {
                const response = await fetcher.get(`products?skip=${(pageParam - 1) * 20}&limit=20`);
                return response.products.map(p => ({ ...p, name: p.title, price: `${p.id * 100}` }));
            },
            getNextPageParam: (lastPage, allPages) => {
                return lastPage.length === 20 ? allPages.length + 1 : undefined;
            },
            initialPageParam: 1,
        });
        return (_jsxs("div", { children: [_jsx("h1", { style: { marginBottom: '2rem', fontSize: '2.5rem' }, children: "Our Products" }), _jsx(InfiniteScrollContainer, { data: data, isLoading: isLoading, isError: isError, hasNextPage: !!hasNextPage, isFetchingNextPage: isFetchingNextPage, fetchNextPage: fetchNextPage, loadingComponent: _jsx("p", { style: { fontSize: '1.2rem', color: '#555' }, children: "Loading products..." }), endComponent: _jsx("p", { style: { fontSize: '1.2rem', color: '#555' }, children: "\uBAA8\uB4E0 \uC0C1\uD488\uC744 \uB458\uB7EC\uBCF4\uC168\uC2B5\uB2C8\uB2E4!" }), children: products => (_jsx(Grid, { columns: { base: 2, md: 3, lg: 4 }, gap: '24px', children: products.map((product) => (_jsxs(Card, { variant: "product", children: [_jsx(Image, { src: product.thumbnail, alt: product.name, aspectRatio: "4/5" }), _jsxs("div", { style: { padding: '16px' }, children: [_jsx("h3", { style: {
                                                margin: 0,
                                                fontSize: '16px',
                                                whiteSpace: 'nowrap',
                                                overflow: 'hidden',
                                                textOverflow: 'ellipsis',
                                            }, children: product.name }), _jsx("p", { style: { margin: '8px 0 0', fontSize: '14px', fontWeight: 'bold' }, children: product.price })] })] }, product.id))) })) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map