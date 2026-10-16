import type { Meta, StoryObj } from '@storybook/react-webpack5';

import Card from './index';
import Image from '../ImageBox';

const meta: Meta<typeof Card> = {
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
type Story = StoryObj<typeof Card>;

// --- Stories ---

/**
 * 가장 일반적인 세로형 상품 카드
 * 상품 목록 페이지(PLP)에서 주로 사용된다.
 */
export const ProductCard: Story = {
  args: {
    variant: 'product',
    style: { width: 300 },
  },
  render: args => (
    <Card {...args}>
      <Image src="https://picsum.photos/seed/product/400/500" alt="Product Image" aspectRatio="4/5" />
      <div style={{ padding: '16px', textAlign: 'left' }}>
        <h3 style={{ margin: 0, fontSize: '16px' }}>클래식 코튼 티셔츠</h3>
        <p style={{ margin: '8px 0 0', fontSize: '14px', fontWeight: 'bold' }}>29,000원</p>
      </div>
    </Card>
  ),
};

/**
 * 장바구니나 위시리스트에서 사용되는 가로형 리스트 아이템 카드.
 */
export const ListItemCard: Story = {
  args: {
    variant: 'listItem',
    style: { width: 480 },
  },
  render: args => (
    <Card {...args}>
      <Image src="https://picsum.photos/seed/listitem/200/200" alt="List Item Image" aspectRatio="1/1" />
      <div style={{ textAlign: 'left', flexGrow: 1 }}>
        <h4 style={{ margin: 0 }}>라운드넥 긴팔 티셔츠</h4>
        <p style={{ margin: '4px 0 0', color: '#666', fontSize: '14px' }}>옵션: Black / M</p>
      </div>
      <button
        style={{
          border: 'none',
          background: 'transparent',
          cursor: 'pointer',
          fontSize: '24px',
        }}
      >
        &times;
      </button>
    </Card>
  ),
};

/**
 * 기획전이나 이벤트 배너로 사용되는 프로모션 카드.
 * 이미지가 배경이 되고 그 위에 텍스트가 오버레이된다.
 */
export const PromotionCard: Story = {
  args: {
    variant: 'promotion',
    style: { width: 400, height: 250 },
  },
  render: args => (
    <Card {...args}>
      <Image src="https://picsum.photos/seed/promo/800/500" alt="Promotion Background" />
      <div style={{ textAlign: 'center', textShadow: '0 1px 3px rgba(0,0,0,0.5)' }}>
        <h2 style={{ margin: 0 }}>SUMMER SALE</h2>
        <p style={{ margin: '8px 0 0' }}>UP TO 50% OFF</p>
      </div>
    </Card>
  ),
};
