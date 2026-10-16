"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const Card = (0, react_1.forwardRef)(({ variant = 'product', children, className, ...restProps }, ref) => {
    const cardClasses = (0, clsx_1.default)(index_module_css_1.default.card, index_module_css_1.default[variant], className);
    return ((0, jsx_runtime_1.jsx)("div", { ref: ref, className: cardClasses, ...restProps, children: children }));
});
exports.default = Card;
//# sourceMappingURL=index.js.map