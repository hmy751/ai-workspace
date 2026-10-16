import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useMemo, useEffect, useState, createContext, useContext, forwardRef, } from "react";
import { createPortal } from "react-dom";
import styles from "./index.module.css";
import Text from "../Text";
import Button from "../Button";
const DialogContext = createContext({});
const Root = ({ children, open: controlledOpen, onOpenChange, }) => {
    const [uncontrolledOpen, setUncontrolledOpen] = useState(false);
    const isControlled = controlledOpen !== undefined;
    const open = isControlled ? controlledOpen : uncontrolledOpen;
    const setOpen = useMemo(() => {
        if (isControlled) {
            return onOpenChange || (() => { });
        }
        return setUncontrolledOpen;
    }, [isControlled, onOpenChange]);
    const contextValue = useMemo(() => ({
        open,
        setOpen,
        controlled: isControlled,
    }), [open, setOpen, isControlled]);
    return (_jsx(DialogContext.Provider, { value: contextValue, children: children }));
};
Root.displayName = "Dialog.Root";
const Trigger = forwardRef(({ children, onClick, ...restProps }, ref) => {
    const { setOpen } = useContext(DialogContext);
    const handleClick = (e) => {
        setOpen(true);
        onClick?.(e);
    };
    return (_jsx("div", { ref: ref, onClick: handleClick, ...restProps, children: children }));
});
Trigger.displayName = "Dialog.Trigger";
const Content = ({ children }) => {
    const { open, setOpen } = useContext(DialogContext);
    useEffect(() => {
        const handleEscape = (e) => {
            if (e.key === "Escape")
                setOpen(false);
        };
        if (open) {
            document.addEventListener("keydown", handleEscape);
        }
        return () => document.removeEventListener("keydown", handleEscape);
    }, [open, setOpen]);
    if (!open)
        return null;
    return createPortal(_jsxs(_Fragment, { children: [_jsx("div", { className: styles.overlay, onClick: () => setOpen(false) }), _jsx("div", { className: styles.content, children: children })] }), document.body);
};
Content.displayName = "Dialog.Content";
const Title = ({ children }) => {
    return _jsx(Text, { as: "h2", children: children });
};
Title.displayName = "Dialog.Title";
const Description = ({ children }) => {
    return _jsx(Text, { as: "p", children: children });
};
Description.displayName = "Dialog.Description";
const Footer = forwardRef(({ children, ...restProps }, ref) => {
    return (_jsx("div", { ref: ref, className: styles.footer, ...restProps, children: children }));
});
Footer.displayName = "Dialog.Footer";
const Confirm = ({ callback, children, onClick, ...restProps }) => {
    const { setOpen } = useContext(DialogContext);
    const handleConfirm = (e) => {
        e.stopPropagation();
        callback?.();
        setOpen(false);
        onClick?.(e);
    };
    return (_jsx(Button, { variant: "primary", fullWidth: true, onClick: handleConfirm, ...restProps, children: children }));
};
Confirm.displayName = "Dialog.Confirm";
const Cancel = ({ callback, children, onClick, ...restProps }) => {
    const { setOpen } = useContext(DialogContext);
    const handleCancel = (e) => {
        e.stopPropagation();
        callback?.();
        setOpen(false);
        onClick?.(e);
    };
    return (_jsx(Button, { variant: "outline", fullWidth: true, onClick: handleCancel, ...restProps, children: children }));
};
Cancel.displayName = "Dialog.Cancel";
const Dialog = Object.assign(Root, {
    Trigger,
    Content,
    Title,
    Description,
    Footer,
    Confirm,
    Cancel,
});
Dialog.displayName = "Dialog";
export default Dialog;
//# sourceMappingURL=index.js.map