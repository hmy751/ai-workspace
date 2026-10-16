import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Input from "./index";
import { useState } from "react";
import { useForm } from "react-hook-form";
import Button from "../Button";
const meta = {
    title: "Common/Input",
    component: Input,
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
export default meta;
export const Primary = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isFocused, setIsFocused] = useState(false);
        const [isTouched, setIsTouched] = useState(false);
        return (_jsx("div", { children: _jsx(Input, { ...Primary.args, isFocused: isFocused, isTouched: isTouched, onChangeFocus: setIsFocused, onChangeTouch: setIsTouched }) }));
    },
};
export const Focused = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isTouched, setIsTouched] = useState(true);
        const [isFocused, setIsFocused] = useState(true);
        return (_jsx("div", { children: _jsx(Input, { placeholder: "Enter Text...", isFocused: isFocused, isTouched: isTouched, onChangeFocus: setIsFocused, onChangeTouch: setIsTouched }) }));
    },
};
export const Touched = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isTouched, setIsTouched] = useState(true);
        const [isFocused, setIsFocused] = useState(false);
        return (_jsx("div", { children: _jsx(Input, { placeholder: "Enter Text...", isTouched: isTouched, isFocused: isFocused, onChangeTouch: setIsTouched, onChangeFocus: setIsFocused }) }));
    },
};
export const Error = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isFocused, setIsFocused] = useState(false);
        const [isTouched, setIsTouched] = useState(false);
        const [errorMessage, setErrorMessage] = useState("Error");
        return (_jsx("div", { children: _jsx(Input, { placeholder: "Enter Text...", isFocused: isFocused, isTouched: isTouched, onChangeFocus: setIsFocused, onChangeTouch: setIsTouched, isError: errorMessage }) }));
    },
};
export const Disabled = {
    args: {
        placeholder: "Enter Text...",
    },
    render() {
        const [isTouched, setIsTouched] = useState(false);
        const [isFocused, setIsFocused] = useState(false);
        return (_jsx("div", { children: _jsx(Input, { placeholder: "Enter Text...", isDisabled: true, isTouched: isTouched, isFocused: isFocused }) }));
    },
};
// 내 컴포넌트는 내부에 touch처리를해서 지금 잘 되지만, 일반적으로 touche를 적용하려면 Controller를 사용해야 한다.
export const UseHookForm = {
    render: () => {
        const { control, register } = useForm({
            defaultValues: {
                name: "",
            },
        });
        const handleClick = () => {
            console.log(control._formValues);
        };
        return (_jsxs("div", { style: {
                display: "flex",
                flexDirection: "column",
                alignContent: "center",
            }, children: [_jsx(Input, { ...register("name") }), _jsx(Button, { onClick: handleClick, children: "\uCD9C\uB825\uD558\uAE30" })] }));
    },
};
//# sourceMappingURL=index.stories.js.map