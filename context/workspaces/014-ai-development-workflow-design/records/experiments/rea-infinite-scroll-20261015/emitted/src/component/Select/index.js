import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { createContext, forwardRef, useState, useRef, useCallback, useMemo, } from "react";
import clsx from "clsx";
import styles from "./index.module.css";
const SelectContext = createContext({});
const Root = forwardRef(({ value, children, placeholder, fullWidth, size, onChange, onChangeValue, isTouched: controlledTouch, onTouchStart, onMouseDown, onChangeTouch, isFocused: controlledFocus, onFocus, onChangeFocus, onBlur, isError, className, ...restProps }, ref) => {
    // ref 처리
    const internalSelectRef = useRef(null);
    const assignRef = useCallback((element) => {
        if (element) {
            internalSelectRef.current = element;
        }
        if (typeof ref === "function") {
            ref(element);
        }
        else if (ref) {
            ref.current = element;
        }
    }, [ref]);
    // isTouched와 같은 value는 control, unControl에 따라서 기준을 정하고,
    // 이벤트는 control, unControl 모두 실행하여 일관성을 유지한다.
    // touch 이벤트
    const [unControlledTouch, setUnControlledTouch] = useState(false);
    const isControlledTouch = controlledTouch !== undefined;
    const isTouched = isControlledTouch ? controlledTouch : unControlledTouch;
    const handleTouch = (e) => {
        e.stopPropagation();
        // 내부 unControlled 상태 이벤트
        setUnControlledTouch(true);
        // 단순 boolean 상태 이벤트
        onChangeTouch?.(true);
        // 상위 useForm과 같은 controlled 상태 이벤트
        onTouchStart?.(e);
        onMouseDown?.(e);
    };
    // focus 이벤트
    const [unControlledFocus, setUncontrolledFocus] = useState(false);
    const isControlledFocus = controlledFocus !== undefined;
    const isFocused = isControlledFocus ? controlledFocus : unControlledFocus;
    const handleFocus = useCallback((e) => {
        e.stopPropagation();
        onChangeFocus?.(true);
        setUncontrolledFocus(true);
        onFocus?.(e);
    }, [onChangeFocus, onFocus]);
    // blur 이벤트
    const handleBlur = useCallback((e) => {
        e.stopPropagation();
        setUncontrolledFocus(false);
        onChangeFocus?.(false);
        onBlur?.(e);
    }, [onChangeFocus, onBlur, isControlledFocus]);
    // change 이벤트
    const handleChange = useCallback((e) => {
        e.stopPropagation();
        onChangeValue?.(e.target.value);
        onChange?.(e);
    }, [onChange, onChangeValue]);
    const contextValue = useMemo(() => ({
        value,
        onChangeValue,
    }), [value, onChangeValue]);
    return (_jsx(SelectContext.Provider, { value: contextValue, children: _jsxs("select", { ref: assignRef, value: value, onChange: handleChange, onFocus: handleFocus, onBlur: handleBlur, onMouseDown: handleTouch, onTouchStart: handleTouch, className: clsx(styles.select, styles[`size-${size}`], fullWidth && styles.fullWidth, isTouched && styles.isTouched, isFocused && styles.isFocused, isError && styles.isError, isError
                ? "global-focus-visible-error"
                : "global-focus-visible-default", className), ...restProps, children: [placeholder && _jsx("option", { value: "", children: placeholder }), children] }) }));
});
Root.displayName = "Select.Root";
const Option = forwardRef(({ children, ...restProps }, ref) => {
    return (_jsx("option", { ref: ref, ...restProps, children: children }));
});
Option.displayName = "Select.Option";
const Select = Object.assign(Root, {
    Option,
});
Select.displayName = "Select";
export default Select;
//# sourceMappingURL=index.js.map