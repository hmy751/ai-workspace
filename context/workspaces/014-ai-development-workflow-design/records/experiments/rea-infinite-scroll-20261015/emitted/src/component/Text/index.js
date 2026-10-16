import { jsx as _jsx } from "react/jsx-runtime";
import clsx from "clsx";
import styles from "./index.module.css";
const ELEMENT_MAPPING = {
    h1: "h1",
    h2: "h2",
    h3: "h3",
    h4: "h4",
    h5: "h5",
    h6: "h6",
    p: "p",
    span: "span",
};
const Text = ({ size = "md", weight = "normal", as = "p", children, align = "left", maxWidth = "fit", truncate = false, color = "primary", lines, className, ...restProps }) => {
    const Element = ELEMENT_MAPPING[as];
    return (_jsx(Element, { className: clsx(styles.text, styles[size], styles[weight], styles[as], truncate && styles.truncate, lines && styles.multiLineTruncate, styles[color], styles[align], maxWidth && styles[maxWidth], className), style: maxWidth && !styles[maxWidth]
            ? { maxWidth }
            : undefined, ...restProps, children: children }));
};
export default Text;
//# sourceMappingURL=index.js.map