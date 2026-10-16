import { jsx as _jsx } from "react/jsx-runtime";
import { forwardRef } from 'react';
import clsx from 'clsx';
import styles from './index.module.css';
const Card = forwardRef(({ variant = 'product', children, className, ...restProps }, ref) => {
    const cardClasses = clsx(styles.card, styles[variant], className);
    return (_jsx("div", { ref: ref, className: cardClasses, ...restProps, children: children }));
});
export default Card;
//# sourceMappingURL=index.js.map