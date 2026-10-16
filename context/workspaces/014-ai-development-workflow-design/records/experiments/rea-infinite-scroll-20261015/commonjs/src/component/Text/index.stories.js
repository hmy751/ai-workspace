"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MultiLineTruncatedText = exports.TruncatedText = exports.ErrorText = exports.H6 = exports.H5 = exports.H4 = exports.H3 = exports.H2 = exports.H1 = exports.Primary = void 0;
const index_1 = __importDefault(require("./index"));
const meta = {
    title: "Common/Text",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
exports.Primary = {
    args: {
        size: "md",
        weight: "normal",
        as: "p",
        children: "Hello, World!",
    },
};
exports.H1 = {
    args: {
        size: "3xl",
        weight: "bold",
        as: "h1",
        children: "H1 Hello, World!",
    },
};
exports.H2 = {
    args: {
        size: "2xl",
        weight: "bold",
        as: "h2",
        children: "H2 Hello, World!",
    },
};
exports.H3 = {
    args: {
        size: "xl",
        weight: "bold",
        as: "h3",
        children: "H3 Hello, World!",
    },
};
exports.H4 = {
    args: {
        size: "lg",
        weight: "normal",
        as: "h4",
        children: "H4 Hello, World!",
    },
};
exports.H5 = {
    args: {
        size: "lg",
        weight: "normal",
        as: "h5",
        children: "H5 Hello, World!",
    },
};
exports.H6 = {
    args: {
        size: "sm",
        weight: "normal",
        as: "h6",
        children: "H6 Hello, World!",
    },
};
exports.ErrorText = {
    args: {
        color: "error",
        children: "Error message",
    },
};
exports.TruncatedText = {
    args: {
        truncate: true,
        maxWidth: "130px",
        children: "This is a very long text ",
    },
};
exports.MultiLineTruncatedText = {
    args: {
        lines: 2,
        maxWidth: "100px",
        children: "This is a very long text ",
    },
};
//# sourceMappingURL=index.stories.js.map