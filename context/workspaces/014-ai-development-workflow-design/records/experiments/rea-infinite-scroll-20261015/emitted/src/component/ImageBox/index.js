import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect, forwardRef, useCallback, } from "react";
import clsx from "clsx";
import styles from "./index.module.css";
import Skeleton from "../Skeleton";
const DefaultFallbackIcon = () => (_jsx("svg", { className: styles.fallbackIcon, viewBox: "0 0 24 24", fill: "currentColor", children: _jsx("path", { d: "M21.9,4.1c-0.4-0.4-1-0.4-1.4,0L12,12.6L3.5,4.1c-0.4-0.4-1-0.4-1.4,0s-0.4,1,0,1.4L10.6,14L2.1,22.5c-0.4,0.4-0.4,1,0,1.4 C2.3,24,2.6,24,2.8,24s0.5-0.1,0.7-0.3L12,15.4l8.5,8.5c0.2,0.2,0.5,0.3,0.7,0.3s0.5-0.1,0.7-0.3c0.4-0.4,0.4-1,0-1.4L13.4,14 l8.5-8.5C22.3,5.1,22.3,4.5,21.9,4.1z" }) }));
// --- Base Component ---
const Base = forwardRef(({ src, alt, aspectRatio = "1/1", backgroundColor = "transparent", fallback = _jsx(DefaultFallbackIcon, {}), children, className, style, sizing = "ratio", objectFit = "cover", }, ref) => {
    const [status, setStatus] = useState("loading");
    const isLoading = status === "loading";
    const isError = status === "error";
    useEffect(() => {
        if (!src) {
            setStatus("error");
            return;
        }
        setStatus("loading");
    }, [src]);
    const isMasonry = sizing === "natural";
    const handleLoad = useCallback(() => setStatus("success"), []);
    const handleError = useCallback(() => setStatus("error"), []);
    const containerStyle = {
        ...style,
        aspectRatio: !isMasonry ? aspectRatio.replace("/", " / ") : undefined,
        backgroundColor,
    };
    return (_jsxs("div", { ref: ref, className: clsx(styles.container, isMasonry && styles.masonryContainer, className), style: containerStyle, children: [isLoading && (_jsx(Skeleton, { className: styles.placeholder, aspectRatio: aspectRatio })), isError && _jsx("div", { className: styles.fallbackWrapper, children: fallback }), _jsx("img", { src: src, alt: alt, className: clsx(styles.image, isMasonry && styles.masonryImage), style: { objectFit }, onLoad: handleLoad, onError: handleError, "data-status": status }), !isLoading && !isError && children && (_jsx("div", { className: styles.overlay, children: children }))] }));
});
Base.displayName = "Image.Base";
// --- Standard Components ---
const Standard = forwardRef((props, ref) => (_jsx(Base, { ref: ref, ...props, sizing: "ratio", objectFit: "cover" })));
Standard.displayName = "Image.Standard";
// --- Contained Components ---
const Contained = forwardRef((props, ref) => (_jsx(Base, { ref: ref, ...props, sizing: "ratio", objectFit: "contain" })));
Contained.displayName = "Image.Contained";
// --- Masonry Components ---
const Masonry = forwardRef((props, ref) => _jsx(Base, { ref: ref, ...props, sizing: "natural" }));
Masonry.displayName = "Image.Masonry";
// --- Component Composition ---
const Image = Object.assign(Standard, {
    Standard,
    Contained,
    Masonry,
    Base,
});
export default Image;
//# sourceMappingURL=index.js.map