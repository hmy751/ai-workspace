"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const index_1 = __importDefault(require("./index"));
const useToastStore_1 = __importDefault(require("../../store/useToastStore"));
const Button_1 = __importDefault(require("../Button"));
const meta = {
    title: "Common/Toast",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
const ToastDemo = () => {
    const addToast = (0, useToastStore_1.default)((state) => state.addToast);
    const showToast = () => {
        addToast({
            title: "Toast Title",
            description: "This is a toast message",
            duration: 3000,
        });
    };
    return ((0, jsx_runtime_1.jsxs)(jsx_runtime_1.Fragment, { children: [(0, jsx_runtime_1.jsx)(Button_1.default, { onClick: showToast, children: "Show Toast" }), (0, jsx_runtime_1.jsx)(index_1.default, {})] }));
};
exports.Primary = {
    render: () => (0, jsx_runtime_1.jsx)(ToastDemo, {}),
};
//# sourceMappingURL=index.stories.js.map