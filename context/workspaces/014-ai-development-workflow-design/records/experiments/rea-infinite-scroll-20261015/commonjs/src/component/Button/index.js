"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const Spinner_1 = __importDefault(require("../Spinner"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const clsx_1 = __importDefault(require("clsx"));
const Button = ({ variant = "primary", size = "md", fullWidth = false, isLoading = false, children, disabled, className, ...restProps }) => {
    return ((0, jsx_runtime_1.jsx)("button", { className: (0, clsx_1.default)(index_module_css_1.default.button, index_module_css_1.default[variant], index_module_css_1.default[`size-${size}`], fullWidth && index_module_css_1.default.fullWidth, isLoading && index_module_css_1.default.loading, disabled && index_module_css_1.default.disabled, className), disabled: isLoading || disabled, ...restProps, children: isLoading ? ((0, jsx_runtime_1.jsxs)("div", { className: index_module_css_1.default.loadingContainer, children: [(0, jsx_runtime_1.jsx)(Spinner_1.default, { size: size }), children] })) : (children) }));
};
exports.default = Button;
//# sourceMappingURL=index.js.map