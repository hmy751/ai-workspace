"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Disabled = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const index_1 = __importDefault(require("./index"));
const react_1 = require("react");
const meta = {
    title: "Common/Checkbox",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
exports.Primary = {
    render: () => {
        const [isChecked, setIsChecked] = (0, react_1.useState)(false);
        const handleChange = (e) => {
            setIsChecked(e.target.checked);
        };
        return ((0, jsx_runtime_1.jsx)(index_1.default, { id: "checkbox", checked: isChecked, onChange: handleChange, value: "agreed", name: "terms", children: "\uC57D\uAD00\uB3D9\uC758" }));
    },
};
exports.Disabled = {
    render: () => {
        const [isChecked, setIsChecked] = (0, react_1.useState)(false);
        const handleChange = (event) => {
            setIsChecked(event.target.checked);
        };
        return ((0, jsx_runtime_1.jsx)(index_1.default, { id: "checkbox", checked: isChecked, disabled: true, onChange: handleChange, value: "agreed", name: "terms", children: "\uC57D\uAD00\uB3D9\uC758" }));
    },
};
//# sourceMappingURL=index.stories.js.map