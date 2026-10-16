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
    title: "Common/Dropdown",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
exports.Primary = {
    render() {
        const [value, setValue] = (0, react_1.useState)("");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { value: value, onChange: (value) => setValue(value), children: [(0, jsx_runtime_1.jsx)(index_1.default.Trigger, { children: "프레임워크 선택해주세요." }), (0, jsx_runtime_1.jsx)(index_1.default.Menu, { children: [1, 2, 3].map((option) => ((0, jsx_runtime_1.jsx)(index_1.default.Item, { value: option, children: option }, option))) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map