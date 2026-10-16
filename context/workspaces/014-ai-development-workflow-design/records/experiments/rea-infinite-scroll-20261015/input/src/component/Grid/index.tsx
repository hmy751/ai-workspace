import { forwardRef, HTMLAttributes, useMemo, CSSProperties, ReactNode } from 'react';
import clsx from 'clsx';
import styles from './index.module.css';

// --- Types ---
type ResponsiveValue<T> =
  | T
  | {
      base?: T;
      sm?: T;
      md?: T;
      lg?: T;
      xl?: T;
    };

type NewStyle = {
  '--grid-gap': string;
  '--grid-columns'?: string;
  '--grid-columns-base'?: string;
  '--grid-columns-sm'?: string;
  '--grid-columns-md'?: string;
  '--grid-columns-lg'?: string;
  '--grid-columns-xl'?: string;
  '--grid-min-child-width'?: string;
} & CSSProperties;

export interface GridProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * 그리드의 컬럼 수를 지정한다.
   * - 숫자: 모든 화면 크기에서 고정된 컬럼 수
   * - 객체: 화면 크기별로 다른 컬럼 수 (예: { base: 2, md: 4 })
   */
  columns?: ResponsiveValue<number>;
  /** 아이템 사이의 간격 (CSS gap 속성) */
  gap?: string | number;
  /**
   * 'columns'가 없을 때, 자동으로 아이템을 채우기 위한 자식의 최소 너비.
   * 이 값이 있으면 auto-fill 방식으로 동작한다.
   */
  minChildWidth?: string | number;
  children: ReactNode;
}

// --- Component ---
const Grid = forwardRef<HTMLDivElement, GridProps>(
  ({ columns, gap = '24px', minChildWidth = '280px', children, className, style, ...restProps }, ref) => {
    const gridStyles = useMemo(() => {
      const newStyles: NewStyle = {
        ...style,
        '--grid-gap': `${gap}`,
      };

      if (columns) {
        switch (typeof columns) {
          case 'number':
            newStyles['--grid-columns'] = columns.toString();

            break;
          case 'object':
            if (columns?.base) {
              newStyles['--grid-columns-base'] = columns.base.toString();
            }
            if (columns.sm) {
              newStyles['--grid-columns-sm'] = columns.sm.toString();
            }
            if (columns.md) {
              newStyles['--grid-columns-md'] = columns.md.toString();
            }
            if (columns.lg) {
              newStyles['--grid-columns-lg'] = columns.lg.toString();
            }
            if (columns.xl) {
              newStyles['--grid-columns-xl'] = columns.xl.toString();
            }

            break;
        }
      } else {
        newStyles['--grid-min-child-width'] = typeof minChildWidth === 'number' ? `${minChildWidth}px` : minChildWidth;
      }

      return newStyles;
    }, [columns, gap, minChildWidth, style]);

    const gridClasses = clsx(
      styles.grid,
      // columns prop 존재 여부에 따라 다른 클래스를 부여하여 CSS에서 분기 처리
      columns ? styles.explicitColumns : styles.autoFillColumns,
      className
    );

    return (
      <div ref={ref} className={gridClasses} style={gridStyles} {...restProps}>
        {children}
      </div>
    );
  }
);

export default Grid;
