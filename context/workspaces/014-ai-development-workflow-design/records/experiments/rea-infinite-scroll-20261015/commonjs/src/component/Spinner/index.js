"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const index_module_css_1 = __importDefault(require("./index.module.css"));
const Spinner = ({ size = "md", color = "var(--color-primary)", className, }) => {
    return ((0, jsx_runtime_1.jsx)("div", { className: `
        ${index_module_css_1.default.spinner}
        ${index_module_css_1.default[size]}
        ${className || ""}
      `, style: { borderTopColor: color }, role: "status", "aria-label": "loading" }));
};
exports.default = Spinner;
//# sourceMappingURL=index.js.map