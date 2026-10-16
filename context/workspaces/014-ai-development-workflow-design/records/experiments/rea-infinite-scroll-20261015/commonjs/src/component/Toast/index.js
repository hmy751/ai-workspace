"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const react_dom_1 = require("react-dom");
const index_module_css_1 = __importDefault(require("./index.module.css"));
const Text_1 = __importDefault(require("../Text"));
const useToastStore_1 = __importDefault(require("../../store/useToastStore"));
const Toast = ({ children }) => {
    const toasts = (0, useToastStore_1.default)((state) => state.toasts);
    return ((0, jsx_runtime_1.jsxs)(jsx_runtime_1.Fragment, { children: [children, (0, react_dom_1.createPortal)((0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.viewport, children: toasts.map((toast) => ((0, jsx_runtime_1.jsx)(ToastItem, { ...toast }, toast.id))) }), document.body)] }));
};
const ToastItem = ({ id, title, description, duration = 5000 }) => {
    const removeToast = (0, useToastStore_1.default)((state) => state.removeToast);
    (0, react_1.useEffect)(() => {
        const timer = setTimeout(() => removeToast(id), duration);
        return () => clearTimeout(timer);
    }, [duration, removeToast, id]);
    return ((0, jsx_runtime_1.jsxs)("div", { className: index_module_css_1.default.root, children: [title && ((0, jsx_runtime_1.jsx)(Text_1.default, { size: "md", weight: "medium", className: index_module_css_1.default.title, children: title })), description && ((0, jsx_runtime_1.jsx)(Text_1.default, { size: "sm", weight: "normal", children: description }))] }));
};
exports.default = Toast;
//# sourceMappingURL=index.js.map