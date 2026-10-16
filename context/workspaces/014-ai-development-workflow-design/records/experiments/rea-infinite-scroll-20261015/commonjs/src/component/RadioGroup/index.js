"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const RadioGroupContext = (0, react_1.createContext)({});
const Root = ({ value, onChange, name, direction, children }) => {
    const isVertical = direction === "vertical";
    const isHorizontal = direction === "horizontal";
    const contextValue = (0, react_1.useMemo)(() => ({
        value,
        onChange,
        name,
    }), [value, name, onChange]);
    return ((0, jsx_runtime_1.jsx)(RadioGroupContext.Provider, { value: contextValue, children: (0, jsx_runtime_1.jsx)("div", { className: (0, clsx_1.default)(index_module_css_1.default.root, isVertical && index_module_css_1.default.vertical, isHorizontal && index_module_css_1.default.horizontal), children: children }) }));
};
Root.displayName = "RadioGroup.Root";
const Item = (0, react_1.forwardRef)(({ id: propId, value, direction, children, ...restProps }, ref) => {
    const isVertical = direction === "vertical";
    const isHorizontal = direction === "horizontal";
    const inputId = propId ?? (0, react_1.useId)();
    const { name, value: selectedValue, onChange, } = (0, react_1.useContext)(RadioGroupContext);
    const isControlled = selectedValue !== undefined;
    const checkedProp = isControlled
        ? { checked: selectedValue === value }
        : {};
    const handleChange = (e) => {
        onChange?.(e);
    };
    return ((0, jsx_runtime_1.jsxs)("div", { className: (0, clsx_1.default)(index_module_css_1.default.item, isHorizontal && index_module_css_1.default.horizontal, isVertical && index_module_css_1.default.vertical), children: [(0, jsx_runtime_1.jsx)("input", { id: inputId, value: value, ref: ref, type: "radio", name: name, onChange: handleChange, ...checkedProp, className: (0, clsx_1.default)("global-focus-visible-default:focus-visible"), ...restProps }), (0, jsx_runtime_1.jsx)("label", { htmlFor: inputId, className: index_module_css_1.default.text, children: children })] }));
});
Item.displayName = "RadioGroup.Item";
const RadioGroup = Object.assign(Root, {
    Item,
});
exports.default = RadioGroup;
//# sourceMappingURL=index.js.map