import { forwardRef, HTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';
import styles from './index.module.css';

export type CardVariant = 'product' | 'listItem' | 'promotion';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * 카드의 시각적/구조적 유형을 결정한다.
   * - `product`: 일반적인 세로형 상품 카드 (기본값)
   * - `listItem`: 좌우로 나열되는 가로형 리스트 아이템
   * - `promotion`: 이미지가 배경이 되는 프로모션 배너형
   */
  variant?: CardVariant;
  children: ReactNode;
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ variant = 'product', children, className, ...restProps }, ref) => {
    const cardClasses = clsx(styles.card, styles[variant], className);

    return (
      <div ref={ref} className={cardClasses} {...restProps}>
        {children}
      </div>
    );
  }
);

export default Card;
