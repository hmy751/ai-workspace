import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Grid from './index';
import Card from '../Card';
import Image from '../ImageBox';
const sampleProducts = Array.from({ length: 8 }, (_, i) => ({
    id: i + 1,
    name: `샘플 상품 ${i + 1}`,
    price: `${(2 + i) * 10},000원`,
    imageUrl: `https://picsum.photos/seed/${i + 1}/500/600`,
}));
const SampleCard = ({ product }) => (_jsxs(Card, { variant: "product", children: [_jsx(Image, { src: product.imageUrl, alt: product.name, aspectRatio: "4/5" }), _jsxs("div", { style: { padding: '16px' }, children: [_jsx("h3", { style: { margin: 0, fontSize: '16px', whiteSpace: 'nowrap' }, children: product.name }), _jsx("p", { style: { margin: '8px 0 0', fontSize: '14px', fontWeight: 'bold' }, children: product.price })] })] }));
const meta = {
    title: 'Common/Grid',
    component: Grid,
    parameters: {
        layout: 'padded', // 전체 너비를 사용하는 레이아웃
    },
    tags: ['autodocs'],
    argTypes: {
        columns: { control: 'object' },
        gap: { control: 'text' },
        minChildWidth: { control: 'text' },
        children: { control: false },
    },
};
export default meta;
// --- Stories ---
/**
 * `columns` prop에 반응형 객체를 전달하여 화면 크기별로 컬럼 수를 명시적으로 제어한다.
 */
export const ResponsiveGrid = {
    args: {
        columns: { base: 2, md: 3, lg: 4 },
        gap: '24px',
    },
    render: args => (_jsx(Grid, { ...args, children: sampleProducts.map(p => (_jsx(SampleCard, { product: p }, p.id))) })),
};
/**
 * `columns` prop에 숫자를 전달하여 모든 화면 크기에서 컬럼 수를 고정한다.
 */
export const FixedColumnGrid = {
    args: {
        columns: 3,
        gap: '16px',
    },
    render: args => (_jsx(Grid, { ...args, children: sampleProducts.slice(0, 6).map(p => (_jsx(SampleCard, { product: p }, p.id))) })),
};
/**
 * `columns` prop을 생략하고 `minChildWidth`를 지정하면,
 * 컨테이너 너비에 따라 최적의 컬럼 수를 자동으로 계산하여 아이템을 채운다.
 */
export const AutoFillGrid = {
    name: 'Auto-Fill Grid (Default)',
    args: {
        columns: undefined, // columns를 명시적으로 비워야 minChildWidth가 동작한다.
        minChildWidth: '280px',
        gap: '24px',
    },
    render: args => (_jsx(Grid, { ...args, children: sampleProducts.map(p => (_jsx(SampleCard, { product: p }, p.id))) })),
};
//# sourceMappingURL=index.stories.js.map