import { jsx as _jsx } from "react/jsx-runtime";
import { forwardRef, useMemo } from 'react';
import clsx from 'clsx';
import styles from './index.module.css';
// --- Component ---
const Grid = forwardRef(({ columns, gap = '24px', minChildWidth = '280px', children, className, style, ...restProps }, ref) => {
    const gridStyles = useMemo(() => {
        const newStyles = {
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
        }
        else {
            newStyles['--grid-min-child-width'] = typeof minChildWidth === 'number' ? `${minChildWidth}px` : minChildWidth;
        }
        return newStyles;
    }, [columns, gap, minChildWidth, style]);
    const gridClasses = clsx(styles.grid, 
    // columns prop 존재 여부에 따라 다른 클래스를 부여하여 CSS에서 분기 처리
    columns ? styles.explicitColumns : styles.autoFillColumns, className);
    return (_jsx("div", { ref: ref, className: gridClasses, style: gridStyles, ...restProps, children: children }));
});
export default Grid;
//# sourceMappingURL=index.js.map