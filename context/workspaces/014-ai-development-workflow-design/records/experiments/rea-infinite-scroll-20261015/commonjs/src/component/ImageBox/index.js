"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const clsx_1 = __importDefault(require("clsx"));
const index_module_css_1 = __importDefault(require("./index.module.css"));
const Skeleton_1 = __importDefault(require("../Skeleton"));
const DefaultFallbackIcon = () => ((0, jsx_runtime_1.jsx)("svg", { className: index_module_css_1.default.fallbackIcon, viewBox: "0 0 24 24", fill: "currentColor", children: (0, jsx_runtime_1.jsx)("path", { d: "M21.9,4.1c-0.4-0.4-1-0.4-1.4,0L12,12.6L3.5,4.1c-0.4-0.4-1-0.4-1.4,0s-0.4,1,0,1.4L10.6,14L2.1,22.5c-0.4,0.4-0.4,1,0,1.4 C2.3,24,2.6,24,2.8,24s0.5-0.1,0.7-0.3L12,15.4l8.5,8.5c0.2,0.2,0.5,0.3,0.7,0.3s0.5-0.1,0.7-0.3c0.4-0.4,0.4-1,0-1.4L13.4,14 l8.5-8.5C22.3,5.1,22.3,4.5,21.9,4.1z" }) }));
// --- Base Component ---
const Base = (0, react_1.forwardRef)(({ src, alt, aspectRatio = "1/1", backgroundColor = "transparent", fallback = (0, jsx_runtime_1.jsx)(DefaultFallbackIcon, {}), children, className, style, sizing = "ratio", objectFit = "cover", }, ref) => {
    const [status, setStatus] = (0, react_1.useState)("loading");
    const isLoading = status === "loading";
    const isError = status === "error";
    (0, react_1.useEffect)(() => {
        if (!src) {
            setStatus("error");
            return;
        }
        setStatus("loading");
    }, [src]);
    const isMasonry = sizing === "natural";
    const handleLoad = (0, react_1.useCallback)(() => setStatus("success"), []);
    const handleError = (0, react_1.useCallback)(() => setStatus("error"), []);
    const containerStyle = {
        ...style,
        aspectRatio: !isMasonry ? aspectRatio.replace("/", " / ") : undefined,
        backgroundColor,
    };
    return ((0, jsx_runtime_1.jsxs)("div", { ref: ref, className: (0, clsx_1.default)(index_module_css_1.default.container, isMasonry && index_module_css_1.default.masonryContainer, className), style: containerStyle, children: [isLoading && ((0, jsx_runtime_1.jsx)(Skeleton_1.default, { className: index_module_css_1.default.placeholder, aspectRatio: aspectRatio })), isError && (0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.fallbackWrapper, children: fallback }), (0, jsx_runtime_1.jsx)("img", { src: src, alt: alt, className: (0, clsx_1.default)(index_module_css_1.default.image, isMasonry && index_module_css_1.default.masonryImage), style: { objectFit }, onLoad: handleLoad, onError: handleError, "data-status": status }), !isLoading && !isError && children && ((0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.overlay, children: children }))] }));
});
Base.displayName = "Image.Base";
// --- Standard Components ---
const Standard = (0, react_1.forwardRef)((props, ref) => ((0, jsx_runtime_1.jsx)(Base, { ref: ref, ...props, sizing: "ratio", objectFit: "cover" })));
Standard.displayName = "Image.Standard";
// --- Contained Components ---
const Contained = (0, react_1.forwardRef)((props, ref) => ((0, jsx_runtime_1.jsx)(Base, { ref: ref, ...props, sizing: "ratio", objectFit: "contain" })));
Contained.displayName = "Image.Contained";
// --- Masonry Components ---
const Masonry = (0, react_1.forwardRef)((props, ref) => (0, jsx_runtime_1.jsx)(Base, { ref: ref, ...props, sizing: "natural" }));
Masonry.displayName = "Image.Masonry";
// --- Component Composition ---
const Image = Object.assign(Standard, {
    Standard,
    Contained,
    Masonry,
    Base,
});
exports.default = Image;
//# sourceMappingURL=index.js.map