import type { Meta, StoryObj } from '@storybook/react-webpack5';

import { useInfiniteQuery } from '@tanstack/react-query';
import fetcher from '../../api/fetcher';

import Grid from '../Grid';
import Card from '../Card';
import Image from '../ImageBox';
import InfiniteScrollContainer from './index';

const meta: Meta<typeof InfiniteScrollContainer> = {
  title: 'Common/InfiniteScrollContainer',
  component: InfiniteScrollContainer,
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof InfiniteScrollContainer>;

export type Product = {
  id: number;
  title: string;
  description: string;
  thumbnail: string;
  price: string;
  name: string;
};

export const InfiniteScroll: Omit<Story, 'args'> = {
  render: () => {
    const { data, isLoading, isError, hasNextPage, isFetchingNextPage, fetchNextPage } = useInfiniteQuery({
      queryKey: ['products'],
      queryFn: async ({ pageParam = 1 }) => {
        const response = await fetcher.get<{ products: Product[] }>(`products?skip=${(pageParam - 1) * 20}&limit=20`);
        return response.products.map(p => ({ ...p, name: p.title, price: `${p.id * 100}` }));
      },
      getNextPageParam: (lastPage, allPages) => {
        return lastPage.length === 20 ? allPages.length + 1 : undefined;
      },
      initialPageParam: 1,
    });

    return (
      <div>
        <h1 style={{ marginBottom: '2rem', fontSize: '2.5rem' }}>Our Products</h1>
        <InfiniteScrollContainer<Product>
          data={data}
          isLoading={isLoading}
          isError={isError}
          hasNextPage={!!hasNextPage}
          isFetchingNextPage={isFetchingNextPage}
          fetchNextPage={fetchNextPage}
          loadingComponent={<p style={{ fontSize: '1.2rem', color: '#555' }}>Loading products...</p>}
          endComponent={<p style={{ fontSize: '1.2rem', color: '#555' }}>모든 상품을 둘러보셨습니다!</p>}
        >
          {/*  children을 함수 형태로 전달 */}
          {products => (
            <Grid columns={{ base: 2, md: 3, lg: 4 }} gap={'24px'}>
              {products.map((product: Product) => (
                <Card key={product.id} variant="product">
                  <Image src={product.thumbnail} alt={product.name} aspectRatio="4/5" />
                  <div style={{ padding: '16px' }}>
                    <h3
                      style={{
                        margin: 0,
                        fontSize: '16px',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                      }}
                    >
                      {product.name}
                    </h3>
                    <p style={{ margin: '8px 0 0', fontSize: '14px', fontWeight: 'bold' }}>{product.price}</p>
                  </div>
                </Card>
              ))}
            </Grid>
          )}
        </InfiniteScrollContainer>
      </div>
    );
  },
};
