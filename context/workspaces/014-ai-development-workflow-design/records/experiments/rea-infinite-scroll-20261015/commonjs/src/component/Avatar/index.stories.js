"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Group = exports.ExtraLarge = exports.Large = exports.Small = exports.ExtraSmall = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const index_1 = __importDefault(require("./index"));
const meta = {
    title: "Common/Avatar",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        size: {
            control: "select",
            options: ["xs", "sm", "md", "lg", "xl"],
        },
    },
};
exports.default = meta;
exports.Primary = {
    args: {
        src: "/images/profile.webp",
        size: "md",
    },
};
exports.ExtraSmall = {
    args: {
        src: "/images/profile.webp",
        size: "xs",
    },
};
exports.Small = {
    args: {
        src: "/images/profile.webp",
        size: "sm",
    },
};
exports.Large = {
    args: {
        src: "/images/profile.webp",
        size: "lg",
    },
};
exports.ExtraLarge = {
    args: {
        src: "/images/profile.webp",
        size: "xl",
    },
};
exports.Group = {
    args: {
        src: "",
        size: "xl",
    },
    render: () => ((0, jsx_runtime_1.jsxs)("div", { style: { display: "flex", gap: "8px", alignItems: "center" }, children: [(0, jsx_runtime_1.jsx)(index_1.default, { src: "/images/profile.webp", size: "xs" }), (0, jsx_runtime_1.jsx)(index_1.default, { src: "/images/profile.webp", size: "sm" }), (0, jsx_runtime_1.jsx)(index_1.default, { src: "/images/profile.webp", size: "md" }), (0, jsx_runtime_1.jsx)(index_1.default, { src: "/images/profile.webp", size: "lg" }), (0, jsx_runtime_1.jsx)(index_1.default, { src: "/images/profile.webp", size: "xl" })] })),
};
//# sourceMappingURL=index.stories.js.map