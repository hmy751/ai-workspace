import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useState } from "react";
import Select from "./index";
const meta = {
    title: "Common/Select",
    component: Select,
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
export default meta;
export const Primary = {
    render: (args) => {
        const [value, setValue] = useState("");
        return (_jsxs(Select, { ...args, value: value, onChangeValue: setValue, children: [_jsx(Select.Option, { value: "option1", children: "Option 1" }), _jsx(Select.Option, { value: "option2", children: "Option 2" }), _jsx(Select.Option, { value: "option3", children: "Option 3" })] }));
    },
    args: {
        placeholder: "Select an option...",
    },
};
export const InitialValue = {
    render: (args) => {
        const [value, setValue] = useState("option2");
        return (_jsxs(Select, { ...args, value: value, onChangeValue: setValue, isTouched: true, children: [_jsx(Select.Option, { value: "option1", children: "Option 1" }), _jsx(Select.Option, { value: "option2", children: "Option 2 (Initial)" }), _jsx(Select.Option, { value: "option3", children: "Option 3" })] }));
    },
    args: {
        placeholder: "Select an option...",
    },
};
export const Error = {
    render: (args) => {
        const [value, setValue] = useState("");
        return (_jsxs(Select, { ...args, value: value, onChangeValue: setValue, isTouched: true, children: [_jsx(Select.Option, { value: "option1", children: "Option 1" }), _jsx(Select.Option, { value: "option2", children: "Option 2" })] }));
    },
    args: {
        placeholder: "Select with error...",
        isError: "This field is required.",
    },
};
export const Disabled = {
    render: (args) => {
        const [value, setValue] = useState("option1");
        return (_jsxs(Select, { ...args, value: value, onChangeValue: setValue, children: [_jsx(Select.Option, { value: "option1", children: "Option 1 (Disabled Select)" }), _jsx(Select.Option, { value: "option2", children: "Option 2" })] }));
    },
    args: {
        placeholder: "Disabled Select...",
        disabled: true,
    },
};
export const WithDisabledOption = {
    render: (args) => {
        const [value, setValue] = useState("");
        return (_jsxs(Select, { ...args, value: value, onChangeValue: setValue, isTouched: true, children: [_jsx(Select.Option, { value: "option1", children: "Option 1" }), _jsx(Select.Option, { value: "option2", disabled: true, children: "Option 2 (Disabled)" }), _jsx(Select.Option, { value: "option3", children: "Option 3" })] }));
    },
    args: {
        placeholder: "Select with disabled option...",
    },
};
//# sourceMappingURL=index.stories.js.map