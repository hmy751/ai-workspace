import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { forwardRef, createContext, useContext, useMemo, useId, } from "react";
import clsx from "clsx";
import styles from "./index.module.css";
const RadioGroupContext = createContext({});
const Root = ({ value, onChange, name, direction, children }) => {
    const isVertical = direction === "vertical";
    const isHorizontal = direction === "horizontal";
    const contextValue = useMemo(() => ({
        value,
        onChange,
        name,
    }), [value, name, onChange]);
    return (_jsx(RadioGroupContext.Provider, { value: contextValue, children: _jsx("div", { className: clsx(styles.root, isVertical && styles.vertical, isHorizontal && styles.horizontal), children: children }) }));
};
Root.displayName = "RadioGroup.Root";
const Item = forwardRef(({ id: propId, value, direction, children, ...restProps }, ref) => {
    const isVertical = direction === "vertical";
    const isHorizontal = direction === "horizontal";
    const inputId = propId ?? useId();
    const { name, value: selectedValue, onChange, } = useContext(RadioGroupContext);
    const isControlled = selectedValue !== undefined;
    const checkedProp = isControlled
        ? { checked: selectedValue === value }
        : {};
    const handleChange = (e) => {
        onChange?.(e);
    };
    return (_jsxs("div", { className: clsx(styles.item, isHorizontal && styles.horizontal, isVertical && styles.vertical), children: [_jsx("input", { id: inputId, value: value, ref: ref, type: "radio", name: name, onChange: handleChange, ...checkedProp, className: clsx("global-focus-visible-default:focus-visible"), ...restProps }), _jsx("label", { htmlFor: inputId, className: styles.text, children: children })] }));
});
Item.displayName = "RadioGroup.Item";
const RadioGroup = Object.assign(Root, {
    Item,
});
export default RadioGroup;
//# sourceMappingURL=index.js.map