import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Card from './index';
import Image from '../ImageBox';
const meta = {
    title: 'Common/Card',
    component: Card,
    parameters: {
        layout: 'centered',
    },
    tags: ['autodocs'],
    argTypes: {
        variant: {
            control: 'radio',
            options: ['product', 'listItem', 'promotion'],
        },
        children: { control: false, description: '첫번째 요소가 Image, 나머지는 overlay 또는 설명 요소들' }, // children은 render 함수에서 직접 제어
    },
};
export default meta;
// --- Stories ---
/**
 * 가장 일반적인 세로형 상품 카드
 * 상품 목록 페이지(PLP)에서 주로 사용된다.
 */
export const ProductCard = {
    args: {
        variant: 'product',
        style: { width: 300 },
    },
    render: args => (_jsxs(Card, { ...args, children: [_jsx(Image, { src: "https://picsum.photos/seed/product/400/500", alt: "Product Image", aspectRatio: "4/5" }), _jsxs("div", { style: { padding: '16px', textAlign: 'left' }, children: [_jsx("h3", { style: { margin: 0, fontSize: '16px' }, children: "\uD074\uB798\uC2DD \uCF54\uD2BC \uD2F0\uC154\uCE20" }), _jsx("p", { style: { margin: '8px 0 0', fontSize: '14px', fontWeight: 'bold' }, children: "29,000\uC6D0" })] })] })),
};
/**
 * 장바구니나 위시리스트에서 사용되는 가로형 리스트 아이템 카드.
 */
export const ListItemCard = {
    args: {
        variant: 'listItem',
        style: { width: 480 },
    },
    render: args => (_jsxs(Card, { ...args, children: [_jsx(Image, { src: "https://picsum.photos/seed/listitem/200/200", alt: "List Item Image", aspectRatio: "1/1" }), _jsxs("div", { style: { textAlign: 'left', flexGrow: 1 }, children: [_jsx("h4", { style: { margin: 0 }, children: "\uB77C\uC6B4\uB4DC\uB125 \uAE34\uD314 \uD2F0\uC154\uCE20" }), _jsx("p", { style: { margin: '4px 0 0', color: '#666', fontSize: '14px' }, children: "\uC635\uC158: Black / M" })] }), _jsx("button", { style: {
                    border: 'none',
                    background: 'transparent',
                    cursor: 'pointer',
                    fontSize: '24px',
                }, children: "\u00D7" })] })),
};
/**
 * 기획전이나 이벤트 배너로 사용되는 프로모션 카드.
 * 이미지가 배경이 되고 그 위에 텍스트가 오버레이된다.
 */
export const PromotionCard = {
    args: {
        variant: 'promotion',
        style: { width: 400, height: 250 },
    },
    render: args => (_jsxs(Card, { ...args, children: [_jsx(Image, { src: "https://picsum.photos/seed/promo/800/500", alt: "Promotion Background" }), _jsxs("div", { style: { textAlign: 'center', textShadow: '0 1px 3px rgba(0,0,0,0.5)' }, children: [_jsx("h2", { style: { margin: 0 }, children: "SUMMER SALE" }), _jsx("p", { style: { margin: '8px 0 0' }, children: "UP TO 50% OFF" })] })] })),
};
//# sourceMappingURL=index.stories.js.map