"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = __importDefault(require("react"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const sizeMap = {
    xs: 24,
    sm: 32,
    md: 40,
    lg: 48,
    xl: 160,
};
const Avatar = ({ src, size = "md", alt = "avatar", className, ...props }) => {
    const containerClasses = [
        index_module_css_1.default.container,
        index_module_css_1.default[`size-${size}`],
        className || "",
    ]
        .filter(Boolean)
        .join(" ");
    const imageSrc = src || "/assets/images/default-avatar.svg";
    return ((0, jsx_runtime_1.jsx)("div", { className: containerClasses, ...props, children: (0, jsx_runtime_1.jsx)("img", { src: imageSrc, alt: alt, width: sizeMap[size], height: sizeMap[size], className: index_module_css_1.default.image, loading: "lazy" }) }));
};
exports.default = Avatar;
//# sourceMappingURL=index.js.map