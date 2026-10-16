"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const ELEMENT_MAPPING = {
    h1: "h1",
    h2: "h2",
    h3: "h3",
    h4: "h4",
    h5: "h5",
    h6: "h6",
    p: "p",
    span: "span",
};
const Text = ({ size = "md", weight = "normal", as = "p", children, align = "left", maxWidth = "fit", truncate = false, color = "primary", lines, className, ...restProps }) => {
    const Element = ELEMENT_MAPPING[as];
    return ((0, jsx_runtime_1.jsx)(Element, { className: (0, clsx_1.default)(index_module_css_1.default.text, index_module_css_1.default[size], index_module_css_1.default[weight], index_module_css_1.default[as], truncate && index_module_css_1.default.truncate, lines && index_module_css_1.default.multiLineTruncate, index_module_css_1.default[color], index_module_css_1.default[align], maxWidth && index_module_css_1.default[maxWidth], className), style: maxWidth && !index_module_css_1.default[maxWidth]
            ? { maxWidth }
            : undefined, ...restProps, children: children }));
};
exports.default = Text;
//# sourceMappingURL=index.js.map