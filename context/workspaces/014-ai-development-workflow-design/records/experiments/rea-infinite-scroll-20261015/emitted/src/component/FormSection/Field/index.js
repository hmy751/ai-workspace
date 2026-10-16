import { jsx as _jsx } from "react/jsx-runtime";
import styles from "./index.module.css";
import Text from "../../Text";
import clsx from "clsx";
const Root = ({ ariaLabelledby, children }) => {
    return (_jsx("div", { className: styles.root, "aria-labelledby": ariaLabelledby, children: children }));
};
Root.displayName = "Field.Root";
const Title = ({ id, hidden = false, children }) => {
    return (_jsx(Text, { id: id, size: "sm", weight: "bold", className: clsx(hidden && "visually-hidden"), children: children }));
};
Title.displayName = "Field.Title";
const ElementsBox = ({ elementsHeight = "var(--space-10)", children, }) => {
    return (_jsx("div", { className: styles.elementsBox, style: { height: elementsHeight }, children: children }));
};
ElementsBox.displayName = "Field.ElementsBox";
const Label = ({ children, ...restProps }) => {
    return (_jsx("label", { className: styles.label, ...restProps, children: children }));
};
Label.displayName = "Field.Label";
const Description = ({ children }) => {
    return (_jsx(Text, { size: "sm", weight: "light", children: children }));
};
Description.displayName = "Field.Description";
const Message = ({ children }) => {
    return (_jsx(Text, { size: "sm", color: "error", children: children }));
};
Message.displayName = "Field.Message";
const Field = Object.assign(Root, {
    Title,
    ElementsBox,
    Label,
    Description,
    Message,
});
export default Field;
//# sourceMappingURL=index.js.map