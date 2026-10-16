"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const index_module_css_1 = __importDefault(require("./index.module.css"));
const Text_1 = __importDefault(require("../../Text"));
const clsx_1 = __importDefault(require("clsx"));
const Root = ({ ariaLabelledby, children }) => {
    return ((0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.root, "aria-labelledby": ariaLabelledby, children: children }));
};
Root.displayName = "Field.Root";
const Title = ({ id, hidden = false, children }) => {
    return ((0, jsx_runtime_1.jsx)(Text_1.default, { id: id, size: "sm", weight: "bold", className: (0, clsx_1.default)(hidden && "visually-hidden"), children: children }));
};
Title.displayName = "Field.Title";
const ElementsBox = ({ elementsHeight = "var(--space-10)", children, }) => {
    return ((0, jsx_runtime_1.jsx)("div", { className: index_module_css_1.default.elementsBox, style: { height: elementsHeight }, children: children }));
};
ElementsBox.displayName = "Field.ElementsBox";
const Label = ({ children, ...restProps }) => {
    return ((0, jsx_runtime_1.jsx)("label", { className: index_module_css_1.default.label, ...restProps, children: children }));
};
Label.displayName = "Field.Label";
const Description = ({ children }) => {
    return ((0, jsx_runtime_1.jsx)(Text_1.default, { size: "sm", weight: "light", children: children }));
};
Description.displayName = "Field.Description";
const Message = ({ children }) => {
    return ((0, jsx_runtime_1.jsx)(Text_1.default, { size: "sm", color: "error", children: children }));
};
Message.displayName = "Field.Message";
const Field = Object.assign(Root, {
    Title,
    ElementsBox,
    Label,
    Description,
    Message,
});
exports.default = Field;
//# sourceMappingURL=index.js.map