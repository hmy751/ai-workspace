"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.UseHookForm = exports.Disabled = exports.Error = exports.Touched = exports.Focused = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const index_1 = __importDefault(require("./index"));
const react_1 = require("react");
const react_hook_form_1 = require("react-hook-form");
const Button_1 = __importDefault(require("../Button"));
const meta = {
    title: "Common/Input",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        placeholder: {
            control: {
                type: "text",
            },
        },
    },
};
exports.default = meta;
exports.Primary = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isFocused, setIsFocused] = (0, react_1.useState)(false);
        const [isTouched, setIsTouched] = (0, react_1.useState)(false);
        return ((0, jsx_runtime_1.jsx)("div", { children: (0, jsx_runtime_1.jsx)(index_1.default, { ...exports.Primary.args, isFocused: isFocused, isTouched: isTouched, onChangeFocus: setIsFocused, onChangeTouch: setIsTouched }) }));
    },
};
exports.Focused = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isTouched, setIsTouched] = (0, react_1.useState)(true);
        const [isFocused, setIsFocused] = (0, react_1.useState)(true);
        return ((0, jsx_runtime_1.jsx)("div", { children: (0, jsx_runtime_1.jsx)(index_1.default, { placeholder: "Enter Text...", isFocused: isFocused, isTouched: isTouched, onChangeFocus: setIsFocused, onChangeTouch: setIsTouched }) }));
    },
};
exports.Touched = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isTouched, setIsTouched] = (0, react_1.useState)(true);
        const [isFocused, setIsFocused] = (0, react_1.useState)(false);
        return ((0, jsx_runtime_1.jsx)("div", { children: (0, jsx_runtime_1.jsx)(index_1.default, { placeholder: "Enter Text...", isTouched: isTouched, isFocused: isFocused, onChangeTouch: setIsTouched, onChangeFocus: setIsFocused }) }));
    },
};
exports.Error = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isFocused, setIsFocused] = (0, react_1.useState)(false);
        const [isTouched, setIsTouched] = (0, react_1.useState)(false);
        const [errorMessage, setErrorMessage] = (0, react_1.useState)("Error");
        return ((0, jsx_runtime_1.jsx)("div", { children: (0, jsx_runtime_1.jsx)(index_1.default, { placeholder: "Enter Text...", isFocused: isFocused, isTouched: isTouched, onChangeFocus: setIsFocused, onChangeTouch: setIsTouched, isError: errorMessage }) }));
    },
};
exports.Disabled = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isTouched, setIsTouched] = (0, react_1.useState)(false);
        const [isFocused, setIsFocused] = (0, react_1.useState)(false);
        return ((0, jsx_runtime_1.jsx)("div", { children: (0, jsx_runtime_1.jsx)(index_1.default, { placeholder: "Enter Text...", isDisabled: true, isTouched: isTouched, isFocused: isFocused }) }));
    },
};
// 내 컴포넌트는 내부에 touch처리를해서 지금 잘 되지만, 일반적으로 touche를 적용하려면 Controller를 사용해야 한다.
exports.UseHookForm = {
    render: () => {
        const { control, register } = (0, react_hook_form_1.useForm)({
            defaultValues: {
                name: "",
            },
        });
        const handleClick = () => {
            console.log(control._formValues);
        };
        return ((0, jsx_runtime_1.jsxs)("div", { style: {
                display: "flex",
                flexDirection: "column",
                alignContent: "center",
            }, children: [(0, jsx_runtime_1.jsx)(index_1.default, { ...register("name") }), (0, jsx_runtime_1.jsx)(Button_1.default, { onClick: handleClick, children: "\uCD9C\uB825\uD558\uAE30" })] }));
    },
};
//# sourceMappingURL=index.stories.js.map