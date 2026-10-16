import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Spinner from "../Spinner";
import styles from "./index.module.css";
import clsx from "clsx";
const Button = ({ variant = "primary", size = "md", fullWidth = false, isLoading = false, children, disabled, className, ...restProps }) => {
    return (_jsx("button", { className: clsx(styles.button, styles[variant], styles[`size-${size}`], fullWidth && styles.fullWidth, isLoading && styles.loading, disabled && styles.disabled, className), disabled: isLoading || disabled, ...restProps, children: isLoading ? (_jsxs("div", { className: styles.loadingContainer, children: [_jsx(Spinner, { size: size }), children] })) : (children) }));
};
export default Button;
//# sourceMappingURL=index.js.map