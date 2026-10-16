"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = __importStar(require("react"));
const react_dom_1 = require("react-dom");
const index_module_css_1 = __importDefault(require("./index.module.css"));
const Text_1 = __importDefault(require("../Text"));
const Button_1 = __importDefault(require("../Button"));
const DialogContext = (0, react_1.createContext)({});
const Root = ({ children, open: controlledOpen, onOpenChange, }) => {
    const [uncontrolledOpen, setUncontrolledOpen] = (0, react_1.useState)(false);
    const isControlled = controlledOpen !== undefined;
    const open = isControlled ? controlledOpen : uncontrolledOpen;
    const setOpen = (0, react_1.useMemo)(() => {
        if (isControlled) {
            return onOpenChange || (() => { });
        }
        return setUncontrolledOpen;
    }, [isControlled, onOpenChange]);
    const contextValue = (0, react_1.useMemo)(() => ({
        open,
        setOpen,
        controlled: isControlled,
    }), [open, setOpen, isControlled]);
    return ((0, jsx_runtime_1.jsx)(DialogContext.Provider, { value: contextValue, children: children }));
};
Root.displayName = "Dialog.Root";
const Trigger = (0, react_1.forwardRef)(({ children, onClick, ...restProps }, ref) => {
    const { setOpen } = (0, react_1.useContext)(DialogContext);
    const handleClick = (e) => {
        setOpen(true);
        onClick?.(e);
    };
    return ((0, jsx_runtime_1.jsx)("div", { ref: ref, onClick: handleClick, ...restProps, children: children }));
});
Trigger.displayName = "Dialog.Trigger";
const Content = ({ children }) => {
    const { open, setOpen } = (0, react_1.useContext)(DialogContext);
    (0, react_1.useEffect)(() => {
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
    return (0, react_dom_1.createPortal)((0, jsx_runtime_1.jsxs)(jsx_runtime_1.Fragment, { children: [(0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.overlay, onClick: () => setOpen(false) }), (0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.content, children: children })] }), document.body);
};
Content.displayName = "Dialog.Content";
const Title = ({ children }) => {
    return (0, jsx_runtime_1.jsx)(Text_1.default, { as: "h2", children: children });
};
Title.displayName = "Dialog.Title";
const Description = ({ children }) => {
    return (0, jsx_runtime_1.jsx)(Text_1.default, { as: "p", children: children });
};
Description.displayName = "Dialog.Description";
const Footer = (0, react_1.forwardRef)(({ children, ...restProps }, ref) => {
    return ((0, jsx_runtime_1.jsx)("div", { ref: ref, className: index_module_css_1.default.footer, ...restProps, children: children }));
});
Footer.displayName = "Dialog.Footer";
const Confirm = ({ callback, children, onClick, ...restProps }) => {
    const { setOpen } = (0, react_1.useContext)(DialogContext);
    const handleConfirm = (e) => {
        e.stopPropagation();
        callback?.();
        setOpen(false);
        onClick?.(e);
    };
    return ((0, jsx_runtime_1.jsx)(Button_1.default, { variant: "primary", fullWidth: true, onClick: handleConfirm, ...restProps, children: children }));
};
Confirm.displayName = "Dialog.Confirm";
const Cancel = ({ callback, children, onClick, ...restProps }) => {
    const { setOpen } = (0, react_1.useContext)(DialogContext);
    const handleCancel = (e) => {
        e.stopPropagation();
        callback?.();
        setOpen(false);
        onClick?.(e);
    };
    return ((0, jsx_runtime_1.jsx)(Button_1.default, { variant: "outline", fullWidth: true, onClick: handleCancel, ...restProps, children: children }));
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
exports.default = Dialog;
//# sourceMappingURL=index.js.map