"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const index_1 = __importDefault(require("./index"));
const react_1 = require("react");
const meta = {
    title: "Common/MultiSelect",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
const options = [
    { value: "react", label: "React" },
    { value: "vue", label: "Vue" },
    { value: "angular", label: "Angular" },
    { value: "svelte", label: "Svelte" },
    { value: "solid", label: "Solid.js" },
];
const Wrapper = ({ children }) => {
    return ((0, jsx_runtime_1.jsx)("div", { style: {
            width: "500px",
            border: "1px solid black",
            padding: "10px",
        }, children: children }));
};
exports.Primary = {
    render() {
        const [value, setValue] = (0, react_1.useState)(["react"]);
        return ((0, jsx_runtime_1.jsx)(Wrapper, { children: (0, jsx_runtime_1.jsxs)(index_1.default, { options: options, value: value, onChange: (value) => setValue(value), children: [(0, jsx_runtime_1.jsx)(index_1.default.Trigger, { placeholder: "\uAE30\uC220 \uC2A4\uD0DD\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(index_1.default.Menu, { children: options.map((option) => ((0, jsx_runtime_1.jsx)(index_1.default.Item, { value: option.value, children: option.label }, option.value))) })] }) }));
    },
};
//# sourceMappingURL=index.stories.js.map