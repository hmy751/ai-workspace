import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { forwardRef } from "react";
import clsx from "clsx";
import styles from "./index.module.css";
const CheckmarkIcon = () => (_jsx("svg", { className: styles.checkmarkIcon, viewBox: "0 0 12 9", fill: "none", xmlns: "http://www.w3.org/2000/svg", children: _jsx("path", { d: "M10.6667 1.16663L4.25002 7.24996L1.33335 4.33329", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round" }) }));
const Checkbox = forwardRef(({ id, onChange, children, disabled, className, value, ...restProps }, ref) => {
    return (_jsxs("label", { htmlFor: id, className: clsx(styles.wrapper, className, disabled && styles.disabled), children: [_jsx("input", { id: id, type: "checkbox", ref: ref, className: clsx("visually-hidden"), onChange: onChange, disabled: disabled, value: value, ...restProps }), _jsx("span", { className: clsx(styles.customCheckbox, "global-focus-visible-default"), "aria-hidden": "true", children: _jsx(CheckmarkIcon, {}) }), _jsx("span", { className: styles.labelText, children: children })] }));
});
Checkbox.displayName = "Checkbox";
export default Checkbox;
//# sourceMappingURL=index.js.map