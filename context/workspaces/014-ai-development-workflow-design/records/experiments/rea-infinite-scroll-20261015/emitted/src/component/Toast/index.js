import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect } from "react";
import { createPortal } from "react-dom";
import styles from "./index.module.css";
import Text from "../Text";
import useToastStore from "../../store/useToastStore";
const Toast = ({ children }) => {
    const toasts = useToastStore((state) => state.toasts);
    return (_jsxs(_Fragment, { children: [children, createPortal(_jsx("div", { className: styles.viewport, children: toasts.map((toast) => (_jsx(ToastItem, { ...toast }, toast.id))) }), document.body)] }));
};
const ToastItem = ({ id, title, description, duration = 5000 }) => {
    const removeToast = useToastStore((state) => state.removeToast);
    useEffect(() => {
        const timer = setTimeout(() => removeToast(id), duration);
        return () => clearTimeout(timer);
    }, [duration, removeToast, id]);
    return (_jsxs("div", { className: styles.root, children: [title && (_jsx(Text, { size: "md", weight: "medium", className: styles.title, children: title })), description && (_jsx(Text, { size: "sm", weight: "normal", children: description }))] }));
};
export default Toast;
//# sourceMappingURL=index.js.map