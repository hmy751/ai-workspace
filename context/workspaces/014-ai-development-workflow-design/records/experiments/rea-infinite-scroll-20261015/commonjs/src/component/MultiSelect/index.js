"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const useClickOutsideEffect_1 = __importDefault(require("../../hooks/useClickOutsideEffect"));
const useFloatingPosition_1 = __importDefault(require("../../hooks/useFloatingPosition"));
const Portal_1 = __importDefault(require("../Portal"));
const MultiSelectContext = (0, react_1.createContext)({});
const Root = ({ children, options, value, onChange }) => {
    const [isOpen, setIsOpen] = (0, react_1.useState)(false);
    const [triggerElement, setTriggerElement] = (0, react_1.useState)(null);
    const [menuElement, setMenuElement] = (0, react_1.useState)(null);
    const handleItemSelect = (0, react_1.useCallback)((itemValue) => {
        const newValues = value.includes(itemValue)
            ? value.filter((v) => v !== itemValue)
            : [...value, itemValue];
        onChange(newValues);
    }, [value, onChange]);
    (0, useClickOutsideEffect_1.default)([triggerElement, menuElement], () => {
        setIsOpen(false);
    });
    const positionStyles = (0, useFloatingPosition_1.default)(triggerElement, menuElement, isOpen);
    const contextValue = (0, react_1.useMemo)(() => ({
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
    return ((0, jsx_runtime_1.jsx)(MultiSelectContext.Provider, { value: contextValue, children: (0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.root, children: children }) }));
};
Root.displayName = "MultiSelect.Root";
const Trigger = (0, react_1.forwardRef)(({ className, placeholder, disabled, isError, ...restProps }, ref) => {
    const { isOpen, setIsOpen, setTriggerElement, selectedValues, options, handleItemSelect, } = (0, react_1.useContext)(MultiSelectContext);
    const handleRef = (element) => {
        setTriggerElement(element);
        if (typeof ref === "function")
            ref(element);
        else if (ref)
            ref.current = element;
    };
    const optionsMap = (0, react_1.useMemo)(() => new Map(options.map((opt) => [opt.value, opt.label])), [options]);
    return ((0, jsx_runtime_1.jsxs)("button", { ref: handleRef, type: "button", className: (0, clsx_1.default)(index_module_css_1.default.trigger, isError && index_module_css_1.default.isError, className), onClick: () => setIsOpen((prev) => !prev), "aria-haspopup": "listbox", "aria-expanded": isOpen, disabled: disabled, ...restProps, children: [(0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.triggerValueWrapper, children: selectedValues.length === 0 ? ((0, jsx_runtime_1.jsx)("span", { className: index_module_css_1.default.placeholder, children: placeholder || "선택..." })) : (selectedValues.map((value) => ((0, jsx_runtime_1.jsxs)("span", { className: index_module_css_1.default.tag, onClick: (e) => e.stopPropagation(), children: [optionsMap.get(value) || value, (0, jsx_runtime_1.jsx)("span", { className: index_module_css_1.default.tagRemoveButton, onClick: () => handleItemSelect(value), "aria-label": `${optionsMap.get(value)} 제거`, children: "\u00D7" })] }, value)))) }), (0, jsx_runtime_1.jsx)("span", { className: (0, clsx_1.default)(index_module_css_1.default.arrow, isOpen && index_module_css_1.default.arrowOpen), children: "\u25BC" })] }));
});
Trigger.displayName = "MultiSelect.Trigger";
const Menu = ({ children, className }) => {
    const { isOpen, positionStyles, setMenuElement } = (0, react_1.useContext)(MultiSelectContext);
    return ((0, jsx_runtime_1.jsx)(jsx_runtime_1.Fragment, { children: isOpen && ((0, jsx_runtime_1.jsx)(Portal_1.default, { children: (0, jsx_runtime_1.jsx)("ul", { ref: setMenuElement, className: (0, clsx_1.default)(index_module_css_1.default.dropdown, className), role: "listbox", style: positionStyles, children: children }) })) }));
};
Menu.displayName = "MultiSelect.Menu";
const Item = ({ children, value, className, ...restProps }) => {
    const { selectedValues, handleItemSelect } = (0, react_1.useContext)(MultiSelectContext);
    const isSelected = selectedValues.includes(value);
    const handleKeyDown = (0, react_1.useCallback)((e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            e.stopPropagation();
            handleItemSelect(value);
        }
    }, [handleItemSelect]);
    return ((0, jsx_runtime_1.jsxs)("li", { className: (0, clsx_1.default)(index_module_css_1.default.item, isSelected && index_module_css_1.default.selected, className), onClick: () => handleItemSelect(value), role: "option", "aria-selected": isSelected, tabIndex: 0, onKeyDown: handleKeyDown, ...restProps, children: [(0, jsx_runtime_1.jsx)("span", { className: index_module_css_1.default.itemCheckbox, children: isSelected && (0, jsx_runtime_1.jsx)("span", { className: index_module_css_1.default.itemCheckmark, children: "\u2713" }) }), (0, jsx_runtime_1.jsx)("span", { children: children })] }));
};
Item.displayName = "MultiSelect.Item";
// --- Component Composition ---
const MultiSelect = Object.assign(Root, {
    Trigger,
    Menu,
    Item,
});
exports.default = MultiSelect;
//# sourceMappingURL=index.js.map