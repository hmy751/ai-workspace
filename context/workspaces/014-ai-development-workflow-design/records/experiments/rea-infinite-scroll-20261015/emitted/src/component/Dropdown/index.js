import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { createContext, forwardRef, useContext, useMemo, useRef, useState, useCallback, } from "react";
import clsx from "clsx";
import styles from "./index.module.css";
import useClickOutsideEffect from "../../hooks/useClickOutsideEffect";
import useFloatingPosition from "../../hooks/useFloatingPosition";
import Portal from "../Portal";
const DropdownContext = createContext({});
const Root = ({ children, value, onChange }) => {
    const [isOpen, setIsOpen] = useState(false);
    const rootRef = useRef(null);
    const [triggerElement, setTriggerElement] = useState(null);
    const [menuElement, setMenuElement] = useState(null);
    const positionStyles = useFloatingPosition(triggerElement, menuElement, isOpen);
    useClickOutsideEffect([menuElement, rootRef.current], () => setIsOpen(false));
    const onChangeValue = useCallback((newValue) => {
        onChange?.(newValue);
        setIsOpen(false);
    }, [onChange, setIsOpen]);
    const contextValue = useMemo(() => ({
        isOpen,
        setIsOpen,
        selectedValue: value,
        onChangeValue,
        setTriggerElement,
        setMenuElement,
        positionStyles,
        rootRef,
    }), [isOpen, value, onChange, positionStyles, rootRef, menuElement]);
    return (_jsx(DropdownContext.Provider, { value: contextValue, children: _jsx("div", { ref: rootRef, className: styles.root, children: children }) }));
};
Root.displayName = "Dropdown.Root";
const Trigger = forwardRef(({ children, className, ...restProps }, ref) => {
    const { isOpen, setIsOpen, setTriggerElement } = useContext(DropdownContext);
    const combinedRef = (element) => {
        setTriggerElement(element);
        if (typeof ref === "function") {
            ref(element);
        }
        else if (ref) {
            ref.current = element;
        }
    };
    return (_jsxs("button", { ref: combinedRef, type: "button", className: clsx(styles.trigger, "global-focus-visible-default", className), onClick: () => setIsOpen((prev) => !prev), "aria-haspopup": "listbox", "aria-expanded": isOpen, ...restProps, children: [_jsx("span", { className: styles.triggerValue, children: children }), _jsx("span", { className: clsx(styles.arrow, isOpen && styles.arrowOpen), children: "\u25BC" })] }));
});
Trigger.displayName = "Dropdown.Trigger";
const Menu = ({ children, className }) => {
    const { isOpen, setMenuElement, positionStyles } = useContext(DropdownContext);
    return (_jsx(_Fragment, { children: isOpen && (_jsx(Portal, { children: _jsx("ul", { ref: setMenuElement, className: clsx(styles.menu, className), role: "listbox", style: positionStyles, children: children }) })) }));
};
Menu.displayName = "Dropdown.Menu";
const Item = ({ children, value, className, ...restProps }) => {
    const { selectedValue, onChangeValue } = useContext(DropdownContext);
    const isSelected = selectedValue === value;
    const handleKeyDown = useCallback((e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            e.stopPropagation();
            onChangeValue?.(value);
        }
    }, [value, onChangeValue]);
    const handleChange = useCallback((e) => {
        e.stopPropagation();
        onChangeValue?.(value);
    }, [value, onChangeValue]);
    return (_jsx("li", { role: "option", "aria-selected": isSelected, tabIndex: 0, onClick: handleChange, onKeyDown: handleKeyDown, className: clsx(styles.item, isSelected && styles.selected, className), ...restProps, children: children }));
};
Item.displayName = "Dropdown.Item";
// --- Component Composition ---
const Dropdown = Object.assign(Root, {
    Trigger,
    Menu,
    Item,
});
export default Dropdown;
//# sourceMappingURL=index.js.map