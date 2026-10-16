"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const CheckmarkIcon = () => ((0, jsx_runtime_1.jsx)("svg", { className: index_module_css_1.default.checkmarkIcon, viewBox: "0 0 12 9", fill: "none", xmlns: "http://www.w3.org/2000/svg", children: (0, jsx_runtime_1.jsx)("path", { d: "M10.6667 1.16663L4.25002 7.24996L1.33335 4.33329", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round" }) }));
const Checkbox = (0, react_1.forwardRef)(({ id, onChange, children, disabled, className, value, ...restProps }, ref) => {
    return ((0, jsx_runtime_1.jsxs)("label", { htmlFor: id, className: (0, clsx_1.default)(index_module_css_1.default.wrapper, className, disabled && index_module_css_1.default.disabled), children: [(0, jsx_runtime_1.jsx)("input", { id: id, type: "checkbox", ref: ref, className: (0, clsx_1.default)("visually-hidden"), onChange: onChange, disabled: disabled, value: value, ...restProps }), (0, jsx_runtime_1.jsx)("span", { className: (0, clsx_1.default)(index_module_css_1.default.customCheckbox, "global-focus-visible-default"), "aria-hidden": "true", children: (0, jsx_runtime_1.jsx)(CheckmarkIcon, {}) }), (0, jsx_runtime_1.jsx)("span", { className: index_module_css_1.default.labelText, children: children })] }));
});
Checkbox.displayName = "Checkbox";
exports.default = Checkbox;
//# sourceMappingURL=index.js.map