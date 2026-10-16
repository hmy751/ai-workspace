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
const DropdownContext = (0, react_1.createContext)({});
const Root = ({ children, value, onChange }) => {
    const [isOpen, setIsOpen] = (0, react_1.useState)(false);
    const rootRef = (0, react_1.useRef)(null);
    const [triggerElement, setTriggerElement] = (0, react_1.useState)(null);
    const [menuElement, setMenuElement] = (0, react_1.useState)(null);
    const positionStyles = (0, useFloatingPosition_1.default)(triggerElement, menuElement, isOpen);
    (0, useClickOutsideEffect_1.default)([menuElement, rootRef.current], () => setIsOpen(false));
    const onChangeValue = (0, react_1.useCallback)((newValue) => {
        onChange?.(newValue);
        setIsOpen(false);
    }, [onChange, setIsOpen]);
    const contextValue = (0, react_1.useMemo)(() => ({
        isOpen,
        setIsOpen,
        selectedValue: value,
        onChangeValue,
        setTriggerElement,
        setMenuElement,
        positionStyles,
        rootRef,
    }), [isOpen, value, onChange, positionStyles, rootRef, menuElement]);
    return ((0, jsx_runtime_1.jsx)(DropdownContext.Provider, { value: contextValue, children: (0, jsx_runtime_1.jsx)("div", { ref: rootRef, className: index_module_css_1.default.root, children: children }) }));
};
Root.displayName = "Dropdown.Root";
const Trigger = (0, react_1.forwardRef)(({ children, className, ...restProps }, ref) => {
    const { isOpen, setIsOpen, setTriggerElement } = (0, react_1.useContext)(DropdownContext);
    const combinedRef = (element) => {
        setTriggerElement(element);
        if (typeof ref === "function") {
            ref(element);
        }
        else if (ref) {
            ref.current = element;
        }
    };
    return ((0, jsx_runtime_1.jsxs)("button", { ref: combinedRef, type: "button", className: (0, clsx_1.default)(index_module_css_1.default.trigger, "global-focus-visible-default", className), onClick: () => setIsOpen((prev) => !prev), "aria-haspopup": "listbox", "aria-expanded": isOpen, ...restProps, children: [(0, jsx_runtime_1.jsx)("span", { className: index_module_css_1.default.triggerValue, children: children }), (0, jsx_runtime_1.jsx)("span", { className: (0, clsx_1.default)(index_module_css_1.default.arrow, isOpen && index_module_css_1.default.arrowOpen), children: "\u25BC" })] }));
});
Trigger.displayName = "Dropdown.Trigger";
const Menu = ({ children, className }) => {
    const { isOpen, setMenuElement, positionStyles } = (0, react_1.useContext)(DropdownContext);
    return ((0, jsx_runtime_1.jsx)(jsx_runtime_1.Fragment, { children: isOpen && ((0, jsx_runtime_1.jsx)(Portal_1.default, { children: (0, jsx_runtime_1.jsx)("ul", { ref: setMenuElement, className: (0, clsx_1.default)(index_module_css_1.default.menu, className), role: "listbox", style: positionStyles, children: children }) })) }));
};
Menu.displayName = "Dropdown.Menu";
const Item = ({ children, value, className, ...restProps }) => {
    const { selectedValue, onChangeValue } = (0, react_1.useContext)(DropdownContext);
    const isSelected = selectedValue === value;
    const handleKeyDown = (0, react_1.useCallback)((e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            e.stopPropagation();
            onChangeValue?.(value);
        }
    }, [value, onChangeValue]);
    const handleChange = (0, react_1.useCallback)((e) => {
        e.stopPropagation();
        onChangeValue?.(value);
    }, [value, onChangeValue]);
    return ((0, jsx_runtime_1.jsx)("li", { role: "option", "aria-selected": isSelected, tabIndex: 0, onClick: handleChange, onKeyDown: handleKeyDown, className: (0, clsx_1.default)(index_module_css_1.default.item, isSelected && index_module_css_1.default.selected, className), ...restProps, children: children }));
};
Item.displayName = "Dropdown.Item";
// --- Component Composition ---
const Dropdown = Object.assign(Root, {
    Trigger,
    Menu,
    Item,
});
exports.default = Dropdown;
//# sourceMappingURL=index.js.map