"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Disabled = exports.SizeLarge = exports.SizeSmall = exports.FullWidth = exports.Loading = exports.Text = exports.Outline = exports.Secondary = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const index_1 = __importDefault(require("./index"));
const meta = {
    title: "Common/Button",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        variant: {
            control: "select",
            options: ["primary", "secondary", "outline"],
        },
        size: { control: "select", options: ["sm", "md", "lg"] },
        fullWidth: { control: "boolean" },
        isLoading: { control: "boolean" },
        disabled: { control: "boolean" },
    },
};
exports.default = meta;
exports.Primary = {
    args: {
        children: "Button",
        variant: "primary",
        size: "md",
        fullWidth: false,
        isLoading: false,
    },
};
exports.Secondary = {
    args: {
        children: "Button",
        variant: "secondary",
        size: "md",
    },
};
exports.Outline = {
    args: {
        children: "Button",
        variant: "outline",
        size: "md",
    },
};
exports.Text = {
    args: {
        children: "Button",
        variant: "text",
        size: "md",
    },
};
exports.Loading = {
    args: {
        children: "Loading",
        isLoading: true,
    },
};
exports.FullWidth = {
    render: (args) => ((0, jsx_runtime_1.jsx)("div", { style: {
            width: "300px",
            border: "1px solid var(--color-base-black)",
            padding: "var(--space-4)",
        }, children: (0, jsx_runtime_1.jsx)(index_1.default, { ...args }) })),
    args: {
        children: "Full Width",
        fullWidth: true,
    },
};
exports.SizeSmall = {
    args: {
        children: "Small",
        size: "sm",
    },
};
exports.SizeLarge = {
    args: {
        children: "Large",
        size: "lg",
    },
};
exports.Disabled = {
    args: {
        children: "Disabled",
        disabled: true,
    },
};
//# sourceMappingURL=index.stories.js.map