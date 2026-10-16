"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WithDisabledOption = exports.Disabled = exports.Error = exports.InitialValue = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = __importStar(require("react"));
const index_1 = __importDefault(require("./index"));
const meta = {
    title: "Common/Select",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        placeholder: { control: "text" },
        isError: { control: "text" },
        disabled: { control: "boolean" },
    },
};
exports.default = meta;
exports.Primary = {
    render: (args) => {
        const [value, setValue] = (0, react_1.useState)("");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ...args, value: value, onChangeValue: setValue, children: [(0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option1", children: "Option 1" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option2", children: "Option 2" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option3", children: "Option 3" })] }));
    },
    args: {
        placeholder: "Select an option...",
    },
};
exports.InitialValue = {
    render: (args) => {
        const [value, setValue] = (0, react_1.useState)("option2");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ...args, value: value, onChangeValue: setValue, isTouched: true, children: [(0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option1", children: "Option 1" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option2", children: "Option 2 (Initial)" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option3", children: "Option 3" })] }));
    },
    args: {
        placeholder: "Select an option...",
    },
};
exports.Error = {
    render: (args) => {
        const [value, setValue] = (0, react_1.useState)("");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ...args, value: value, onChangeValue: setValue, isTouched: true, children: [(0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option1", children: "Option 1" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option2", children: "Option 2" })] }));
    },
    args: {
        placeholder: "Select with error...",
        isError: "This field is required.",
    },
};
exports.Disabled = {
    render: (args) => {
        const [value, setValue] = (0, react_1.useState)("option1");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ...args, value: value, onChangeValue: setValue, children: [(0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option1", children: "Option 1 (Disabled Select)" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option2", children: "Option 2" })] }));
    },
    args: {
        placeholder: "Disabled Select...",
        disabled: true,
    },
};
exports.WithDisabledOption = {
    render: (args) => {
        const [value, setValue] = (0, react_1.useState)("");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ...args, value: value, onChangeValue: setValue, isTouched: true, children: [(0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option1", children: "Option 1" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option2", disabled: true, children: "Option 2 (Disabled)" }), (0, jsx_runtime_1.jsx)(index_1.default.Option, { value: "option3", children: "Option 3" })] }));
    },
    args: {
        placeholder: "Select with disabled option...",
    },
};
//# sourceMappingURL=index.stories.js.map