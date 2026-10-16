"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Primary = void 0;
const index_1 = __importDefault(require("./index"));
const meta = {
    title: "Common/Spinner",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        size: { control: "select", options: ["sm", "md", "lg"] },
        color: { control: "color" },
    },
};
exports.default = meta;
exports.Primary = {
    args: {
        size: "md",
    },
};
//# sourceMappingURL=index.stories.js.map