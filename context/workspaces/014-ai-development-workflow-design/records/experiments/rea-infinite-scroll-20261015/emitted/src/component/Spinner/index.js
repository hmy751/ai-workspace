import { jsx as _jsx } from "react/jsx-runtime";
import styles from "./index.module.css";
const Spinner = ({ size = "md", color = "var(--color-primary)", className, }) => {
    return (_jsx("div", { className: `
        ${styles.spinner}
        ${styles[size]}
        ${className || ""}
      `, style: { borderTopColor: color }, role: "status", "aria-label": "loading" }));
};
export default Spinner;
//# sourceMappingURL=index.js.map