"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.VerticalItem = exports.VerticalGroup = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const index_1 = __importDefault(require("./index"));
const meta = {
    title: "Common/RadioGroup",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
exports.Primary = {
    render() {
        return ((0, jsx_runtime_1.jsx)("div", { style: { width: "200px", height: "50px", border: "1px solid black" }, children: (0, jsx_runtime_1.jsxs)(index_1.default, { name: "radio", direction: "horizontal", children: [(0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "0", direction: "horizontal", children: "1" }), (0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "1", direction: "horizontal", children: "2" }), (0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "2", direction: "horizontal", children: "3" })] }) }));
    },
};
exports.VerticalGroup = {
    render() {
        const [value, setValue] = (0, react_1.useState)("");
        return ((0, jsx_runtime_1.jsx)("div", { style: { width: "200px", height: "200px", border: "1px solid black" }, children: (0, jsx_runtime_1.jsxs)(index_1.default, { value: value, name: "radio", onChange: (e) => {
                    setValue(e.target.value);
                }, direction: "vertical", children: [(0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "0", direction: "horizontal", children: "1" }), (0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "1", direction: "horizontal", children: "2" }), (0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "2", direction: "horizontal", children: "3" })] }) }));
    },
};
exports.VerticalItem = {
    render() {
        const [value, setValue] = (0, react_1.useState)("");
        return ((0, jsx_runtime_1.jsx)("div", { style: { width: "200px", height: "200px", border: "1px solid black" }, children: (0, jsx_runtime_1.jsxs)(index_1.default, { value: value, name: "radio", onChange: (e) => {
                    setValue(e.target.value);
                }, direction: "horizontal", children: [(0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "0", direction: "vertical", children: "1" }), (0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "1", direction: "vertical", children: "2" }), (0, jsx_runtime_1.jsx)(index_1.default.Item, { value: "2", direction: "vertical", children: "3" })] }) }));
    },
};
//# sourceMappingURL=index.stories.js.map