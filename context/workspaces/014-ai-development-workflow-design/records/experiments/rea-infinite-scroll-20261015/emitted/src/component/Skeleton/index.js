import { jsx as _jsx } from "react/jsx-runtime";
import React, { forwardRef } from "react";
import clsx from "clsx";
import styles from "./index.module.css";
const Skeleton = forwardRef(({ shape = "rect", width, height, aspectRatio, className, ...restProps }, ref) => {
    const style = {
        width,
        height,
        aspectRatio,
    };
    return (_jsx("div", { ref: ref, className: clsx(styles.skeleton, styles[shape], className), style: style, ...restProps }));
});
export default Skeleton;
//# sourceMappingURL=index.js.map