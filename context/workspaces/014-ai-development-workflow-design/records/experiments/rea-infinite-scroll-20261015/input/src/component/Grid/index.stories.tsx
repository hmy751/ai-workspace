import type { Meta, StoryObj } from '@storybook/react-webpack5';

import Grid from './index';
import Card from '../Card';
import Image from '../ImageBox';

const sampleProducts = Array.from({ length: 8 }, (_, i) => ({
  id: i + 1,
  name: `샘플 상품 ${i + 1}`,
  price: `${(2 + i) * 10},000원`,
  imageUrl: `https://picsum.photos/seed/${i + 1}/500/600`,
}));

const SampleCard = ({ product }: { product: (typeof sampleProducts)[0] }) => (
  <Card variant="product">
    <Image src={product.imageUrl} alt={product.name} aspectRatio="4/5" />
    <div style={{ padding: '16px' }}>
      <h3 style={{ margin: 0, fontSize: '16px', whiteSpace: 'nowrap' }}>{product.name}</h3>
      <p style={{ margin: '8px 0 0', fontSize: '14px', fontWeight: 'bold' }}>{product.price}</p>
    </div>
  </Card>
);

const meta: Meta<typeof Grid> = {
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
type Story = StoryObj<typeof Grid>;

// --- Stories ---

/**
 * `columns` prop에 반응형 객체를 전달하여 화면 크기별로 컬럼 수를 명시적으로 제어한다.
 */
export const ResponsiveGrid: Story = {
  args: {
    columns: { base: 2, md: 3, lg: 4 },
    gap: '24px',
  },
  render: args => (
    <Grid {...args}>
      {sampleProducts.map(p => (
        <SampleCard key={p.id} product={p} />
      ))}
    </Grid>
  ),
};

/**
 * `columns` prop에 숫자를 전달하여 모든 화면 크기에서 컬럼 수를 고정한다.
 */
export const FixedColumnGrid: Story = {
  args: {
    columns: 3,
    gap: '16px',
  },
  render: args => (
    <Grid {...args}>
      {sampleProducts.slice(0, 6).map(p => (
        <SampleCard key={p.id} product={p} />
      ))}
    </Grid>
  ),
};

/**
 * `columns` prop을 생략하고 `minChildWidth`를 지정하면,
 * 컨테이너 너비에 따라 최적의 컬럼 수를 자동으로 계산하여 아이템을 채운다.
 */
export const AutoFillGrid: Story = {
  name: 'Auto-Fill Grid (Default)',
  args: {
    columns: undefined, // columns를 명시적으로 비워야 minChildWidth가 동작한다.
    minChildWidth: '280px',
    gap: '24px',
  },
  render: args => (
    <Grid {...args}>
      {sampleProducts.map(p => (
        <SampleCard key={p.id} product={p} />
      ))}
    </Grid>
  ),
};
