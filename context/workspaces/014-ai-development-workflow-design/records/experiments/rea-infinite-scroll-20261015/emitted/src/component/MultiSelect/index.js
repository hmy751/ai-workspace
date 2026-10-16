import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { createContext, forwardRef, useContext, useMemo, useState, useCallback, } from "react";
import clsx from "clsx";
import styles from "./index.module.css";
import useClickOutsideEffect from "../../hooks/useClickOutsideEffect";
import useFloatingPosition from "../../hooks/useFloatingPosition";
import Portal from "../Portal";
const MultiSelectContext = createContext({});
const Root = ({ children, options, value, onChange }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [triggerElement, setTriggerElement] = useState(null);
    const [menuElement, setMenuElement] = useState(null);
    const handleItemSelect = useCallback((itemValue) => {
        const newValues = value.includes(itemValue)
            ? value.filter((v) => v !== itemValue)
            : [...value, itemValue];
        onChange(newValues);
    }, [value, onChange]);
    useClickOutsideEffect([triggerElement, menuElement], () => {
        setIsOpen(false);
    });
    const positionStyles = useFloatingPosition(triggerElement, menuElement, isOpen);
    const contextValue = useMemo(() => ({
        isOpen,
        setIsOpen,
        selectedValues: value,
        handleItemSelect,
        triggerElement,
        setTriggerElement,
        menuElement,
        setMenuElement,
        positionStyles,
        options,
    }), [
        isOpen,
        value,
        onChange,
        triggerElement,
        menuElement,
        positionStyles,
        options,
    ]);
    return (_jsx(MultiSelectContext.Provider, { value: contextValue, children: _jsx("div", { className: styles.root, children: children }) }));
};
Root.displayName = "MultiSelect.Root";
const Trigger = forwardRef(({ className, placeholder, disabled, isError, ...restProps }, ref) => {
    const { isOpen, setIsOpen, setTriggerElement, selectedValues, options, handleItemSelect, } = useContext(MultiSelectContext);
    const handleRef = (element) => {
        setTriggerElement(element);
        if (typeof ref === "function")
            ref(element);
        else if (ref)
            ref.current = element;
    };
    const optionsMap = useMemo(() => new Map(options.map((opt) => [opt.value, opt.label])), [options]);
    return (_jsxs("button", { ref: handleRef, type: "button", className: clsx(styles.trigger, isError && styles.isError, className), onClick: () => setIsOpen((prev) => !prev), "aria-haspopup": "listbox", "aria-expanded": isOpen, disabled: disabled, ...restProps, children: [_jsx("div", { className: styles.triggerValueWrapper, children: selectedValues.length === 0 ? (_jsx("span", { className: styles.placeholder, children: placeholder || "선택..." })) : (selectedValues.map((value) => (_jsxs("span", { className: styles.tag, onClick: (e) => e.stopPropagation(), children: [optionsMap.get(value) || value, _jsx("span", { className: styles.tagRemoveButton, onClick: () => handleItemSelect(value), "aria-label": `${optionsMap.get(value)} 제거`, children: "\u00D7" })] }, value)))) }), _jsx("span", { className: clsx(styles.arrow, isOpen && styles.arrowOpen), children: "\u25BC" })] }));
});
Trigger.displayName = "MultiSelect.Trigger";
const Menu = ({ children, className }) => {
    const { isOpen, positionStyles, setMenuElement } = useContext(MultiSelectContext);
    return (_jsx(_Fragment, { children: isOpen && (_jsx(Portal, { children: _jsx("ul", { ref: setMenuElement, className: clsx(styles.dropdown, className), role: "listbox", style: positionStyles, children: children }) })) }));
};
Menu.displayName = "MultiSelect.Menu";
const Item = ({ children, value, className, ...restProps }) => {
    const { selectedValues, handleItemSelect } = useContext(MultiSelectContext);
    const isSelected = selectedValues.includes(value);
    const handleKeyDown = useCallback((e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            e.stopPropagation();
            handleItemSelect(value);
        }
    }, [handleItemSelect]);
    return (_jsxs("li", { className: clsx(styles.item, isSelected && styles.selected, className), onClick: () => handleItemSelect(value), role: "option", "aria-selected": isSelected, tabIndex: 0, onKeyDown: handleKeyDown, ...restProps, children: [_jsx("span", { className: styles.itemCheckbox, children: isSelected && _jsx("span", { className: styles.itemCheckmark, children: "\u2713" }) }), _jsx("span", { children: children })] }));
};
Item.displayName = "MultiSelect.Item";
// --- Component Composition ---
const MultiSelect = Object.assign(Root, {
    Trigger,
    Menu,
    Item,
});
export default MultiSelect;
//# sourceMappingURL=index.js.map