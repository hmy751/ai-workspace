import { jsx as _jsx } from "react/jsx-runtime";
import React from "react";
import styles from "./index.module.css";
const sizeMap = {
    xs: 24,
    sm: 32,
    md: 40,
    lg: 48,
    xl: 160,
};
const Avatar = ({ src, size = "md", alt = "avatar", className, ...props }) => {
    const containerClasses = [
        styles.container,
        styles[`size-${size}`],
        className || "",
    ]
        .filter(Boolean)
        .join(" ");
    const imageSrc = src || "/assets/images/default-avatar.svg";
    return (_jsx("div", { className: containerClasses, ...props, children: _jsx("img", { src: imageSrc, alt: alt, width: sizeMap[size], height: sizeMap[size], className: styles.image, loading: "lazy" }) }));
};
export default Avatar;
//# sourceMappingURL=index.js.map