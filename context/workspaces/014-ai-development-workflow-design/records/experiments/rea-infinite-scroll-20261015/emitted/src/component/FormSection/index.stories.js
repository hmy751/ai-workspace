import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useForm, Controller } from "react-hook-form";
import Field from "./Field";
import Input from "../Input";
import Select from "../Select";
import Text from "../Text";
import Checkbox from "../Checkbox";
import Button from "../Button";
import RadioGroup from "../RadioGroup";
import MultiSelect from "../MultiSelect";
const meta = {
    title: "Common/FormSection",
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
export default meta;
const options = [
    { value: "react", label: "React" },
    { value: "vue", label: "Vue" },
    { value: "angular", label: "Angular" },
    { value: "svelte", label: "Svelte" },
    { value: "solid", label: "Solid.js" },
];
const Form = ({ children, ...restProps }) => {
    return (_jsx("form", { style: {
            width: "500px",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            gap: "4px",
        }, ...restProps, children: children }));
};
export const Primary = {
    render: () => {
        const { register, handleSubmit } = useForm({
            defaultValues: {
                name: "",
                emailLocal: "",
                emailDomain: "",
                password: "",
                terms: false,
            },
        });
        const onSubmit = (data) => {
            console.log(data);
        };
        return (_jsxs(Form, { onSubmit: handleSubmit(onSubmit), children: [_jsxs(Field, { ariaLabelledby: "name-group", children: [_jsx(Field.Title, { id: "name-group", children: "\uC774\uB984" }), _jsx(Field.ElementsBox, { children: _jsx(Field.Label, { children: _jsx(Input, { ...register("name") }) }) })] }), _jsxs(Field, { ariaLabelledby: "email-group", children: [_jsx(Field.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), _jsxs(Field.ElementsBox, { children: [_jsxs(Field.Label, { style: { maxWidth: "100px" }, children: [_jsx(Input, { ...register("emailLocal") }), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), _jsx(Text, { children: "@" }), _jsxs(Field.Label, { children: [_jsxs(Select, { ...register("emailDomain"), children: [_jsx(Select.Option, { value: "option1", children: "gmail.com" }), _jsx(Select.Option, { value: "option2", children: "naver.com" })] }), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] })] }), _jsxs(Field, { ariaLabelledby: "password-group", children: [_jsx(Field.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), _jsx(Field.ElementsBox, { children: _jsxs(Field.Label, { children: [_jsx(Input, { ...register("password"), type: "password" }), _jsx("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), _jsx(Field.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." })] }), _jsxs(Field, { ariaLabelledby: "terms-group", children: [_jsx(Field.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), _jsx(Field.ElementsBox, { children: _jsx(Checkbox, { id: "checkbox", value: "agreed", ...register("terms"), children: "\uC57D\uAD00 \uB3D9\uC758" }) })] }), _jsx(Button, { type: "submit", children: "\uC81C\uCD9C" })] }));
    },
};
// register는 단순 event객체를 받는 onChange메서드 형태로 이루어져서 event.target값을 직접받아서 처리하는 경우 적합하다.
// 포인트는 네이티브 요소 input과 직접 소통하는 형태가 register에 적합하다.
export const WithRegisterValidate = {
    render: () => {
        const { register, formState: { errors }, handleSubmit, } = useForm({
            defaultValues: {
                name: "",
                emailLocal: "",
                emailDomain: "",
                password: "",
                age: "",
                terms: false,
            },
        });
        const onSubmit = (data) => {
            console.log(data);
        };
        // control, register 다양한 유효성검사
        // submit전에는 유효성 검사가 되지 않지만, 후에는 onChange 시에도 유효성 검사가 실행된다.
        // trigger 후에는 자동 포커스 된다.
        // errors.name 객체 다음에 type 속성은, 각 validate 함수의 키값과 매칭이된다.
        return (_jsxs(Form, { onSubmit: handleSubmit(onSubmit), children: [_jsxs(Field, { ariaLabelledby: "name-group", children: [_jsx(Field.Title, { id: "name-group", children: "\uC774\uB984" }), _jsx(Field.ElementsBox, { children: _jsx(Field.Label, { children: _jsx(Input, { ...register("name", {
                                        required: true,
                                    }), isError: errors?.name && "필수 항목입니다." }) }) }), _jsx(Field.Message, { children: errors.name && "필수 항목입니다." })] }), _jsxs(Field, { ariaLabelledby: "email-group", children: [_jsx(Field.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), _jsxs(Field.ElementsBox, { children: [_jsxs(Field.Label, { style: { maxWidth: "100px" }, children: [_jsx(Input, { ...register("emailLocal", {
                                                validate: {
                                                    minLength: (v) => v.length >= 3 || "최소 3글자 이상 입력해주세요.",
                                                },
                                            }), isError: errors.emailLocal?.message }), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), _jsx(Text, { children: "@" }), _jsxs(Field.Label, { children: [_jsxs(Select, { ...register("emailDomain", {
                                                validate: {
                                                    required: (v) => !!v || "반드시 도메인 하나는 선택해주세요.",
                                                },
                                            }), isError: errors?.emailDomain?.message, children: [_jsx(Select.Option, { value: "", disabled: true, children: "\uB3C4\uBA54\uC778\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), _jsx(Select.Option, { value: "gmail", children: "gmail.com" }), _jsx(Select.Option, { value: "naver", children: "naver.com" })] }), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] }), _jsx(Field.Message, { children: errors.emailLocal?.message || errors.emailDomain?.message })] }), _jsxs(Field, { ariaLabelledby: "password-group", children: [_jsx(Field.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), _jsx(Field.ElementsBox, { children: _jsxs(Field.Label, { children: [_jsx(Input, { ...register("password", {
                                            validate: {
                                                require: (v) => !!v || "필수 항목입니다.",
                                            },
                                        }), type: "password", isError: errors.password?.message }), _jsx("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), _jsx(Field.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." }), _jsx(Field.Message, { children: errors.password?.message })] }), _jsxs(Field, { ariaLabelledby: "age-group", children: [_jsx(Field.Title, { id: "age-group", children: "\uB098\uC774" }), _jsx(Field.ElementsBox, { children: _jsxs(RadioGroup, { name: "age", direction: "horizontal", children: [_jsx(RadioGroup.Item, { value: "10", direction: "horizontal", ...register("age", {
                                            required: true,
                                        }), children: "10\uB300" }), _jsx(RadioGroup.Item, { value: "20", direction: "horizontal", ...register("age", {
                                            required: true,
                                        }), children: "20\uB300" }), _jsx(RadioGroup.Item, { value: "30", direction: "horizontal", ...register("age", {
                                            required: true,
                                        }), children: "30\uB300" })] }) }), _jsx(Field.Message, { children: errors.age && "필수 항목입니다." })] }), _jsxs(Field, { ariaLabelledby: "terms-group", children: [_jsx(Field.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), _jsx(Field.ElementsBox, { children: _jsx(Checkbox, { id: "checkbox-1", value: "agreed", ...register("terms", {
                                    required: true,
                                }), children: "\uC57D\uAD00 \uB3D9\uC758" }) }), _jsx(Field.Message, { children: errors.terms && "약관에 동의해주세요." })] }), _jsx(Button, { type: "submit", children: "\uC81C\uCD9C" })] }));
    },
};
export const WithController = {
    render: () => {
        const { control, formState: { errors }, handleSubmit, } = useForm({
            mode: "onChange",
            defaultValues: {
                name: "",
                emailLocal: "",
                emailDomain: "",
                password: "",
                age: "",
                techStack: [],
                terms: false,
            },
        });
        const onSubmit = (data) => {
            console.log(data);
        };
        return (_jsxs(Form, { onSubmit: handleSubmit(onSubmit), children: [_jsxs(Field, { ariaLabelledby: "name-group", children: [_jsx(Field.Title, { id: "name-group", children: "\uC774\uB984" }), _jsx(Field.ElementsBox, { children: _jsx(Field.Label, { children: _jsx(Controller, { name: "name", control: control, rules: { required: "필수 항목입니다." }, render: ({ field, fieldState }) => (_jsx(Input, { ...field, isError: fieldState.error?.message })) }) }) }), _jsx(Field.Message, { children: errors.name?.message })] }), _jsxs(Field, { ariaLabelledby: "email-group", children: [_jsx(Field.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), _jsxs(Field.ElementsBox, { children: [_jsxs(Field.Label, { style: { maxWidth: "100px" }, children: [_jsx(Controller, { name: "emailLocal", control: control, rules: {
                                                validate: {
                                                    minLength: (v) => v.length >= 3 || "최소 3글자 이상 입력해주세요.",
                                                },
                                            }, render: ({ field, fieldState }) => (_jsx(Input, { ...field, isError: fieldState.error?.message })) }), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), _jsx(Text, { children: "@" }), _jsxs(Field.Label, { children: [_jsx(Controller, { name: "emailDomain", control: control, rules: {
                                                validate: {
                                                    required: (v) => !!v || "반드시 도메인 하나는 선택해주세요.",
                                                },
                                            }, render: ({ field, fieldState }) => (_jsxs(Select, { ...field, isError: fieldState.error?.message, children: [_jsx(Select.Option, { value: "", disabled: true, children: "\uB3C4\uBA54\uC778\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), _jsx(Select.Option, { value: "gmail", children: "gmail.com" }), _jsx(Select.Option, { value: "naver", children: "naver.com" })] })) }), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] }), _jsx(Field.Message, { children: errors.emailLocal?.message || errors.emailDomain?.message })] }), _jsxs(Field, { ariaLabelledby: "password-group", children: [_jsx(Field.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), _jsx(Field.ElementsBox, { children: _jsxs(Field.Label, { children: [_jsx(Controller, { name: "password", control: control, rules: {
                                            validate: { required: (v) => !!v || "필수 항목입니다." },
                                        }, render: ({ field, fieldState }) => (_jsx(Input, { ...field, type: "password", isError: fieldState.error?.message })) }), _jsx("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), _jsx(Field.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." }), _jsx(Field.Message, { children: errors.password?.message })] }), _jsxs(Field, { ariaLabelledby: "age-group", children: [_jsx(Field.Title, { id: "age-group", children: "\uB098\uC774" }), _jsx(Field.ElementsBox, { children: _jsx(Controller, { name: "age", control: control, rules: { required: "필수 항목입니다." }, render: ({ field }) => (_jsxs(RadioGroup, { name: field.name, direction: "horizontal", value: field.value, onChange: field.onChange, children: [_jsx(RadioGroup.Item, { value: "10", direction: "horizontal", ref: field.ref, children: "10\uB300" }), _jsx(RadioGroup.Item, { value: "20", direction: "horizontal", children: "20\uB300" }), _jsx(RadioGroup.Item, { value: "30", direction: "horizontal", children: "30\uB300" })] })) }) }), _jsx(Field.Message, { children: errors.age?.message })] }), _jsxs(Field, { ariaLabelledby: "techStack-group", children: [_jsx(Field.Title, { id: "techStack-group", children: "\uAE30\uC220 \uC2A4\uD0DD" }), _jsx(Field.ElementsBox, { elementsHeight: "50px", children: _jsx(Controller, { name: "techStack", control: control, rules: {
                                    validate: {
                                        min: (v) => v.length >= 1 || "최소 1개 이상 선택해주세요.",
                                        max: (v) => v.length <= 3 || "최대 3개까지 선택이 가능합니다.",
                                    },
                                }, render: ({ field, fieldState }) => (_jsxs(MultiSelect, { options: options, value: field.value, onChange: field.onChange, children: [_jsx(MultiSelect.Trigger, { ref: field.ref, onBlur: field.onBlur, isError: !!fieldState.error, placeholder: "\uAE30\uC220 \uC2A4\uD0DD\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), _jsx(MultiSelect.Menu, { children: options.map((option) => (_jsx(MultiSelect.Item, { value: option.value, children: option.label }, option.value))) })] })) }) }), _jsx(Field.Description, { children: "\uAE30\uC220\uC2A4\uD0DD\uC740 \uCD5C\uC18C 1\uAC1C\uC5D0\uC11C \uCD5C\uB300 3\uAC1C\uAE4C\uC9C0 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), _jsx(Field.Message, { children: errors.techStack?.message })] }), _jsxs(Field, { ariaLabelledby: "terms-group", children: [_jsx(Field.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), _jsx(Field.ElementsBox, { children: _jsx(Controller, { name: "terms", control: control, rules: {
                                    validate: (value) => value === true || "약관에 동의해주세요.",
                                }, render: ({ field }) => (_jsx(Checkbox, { id: "checkbox-1", onChange: field.onChange, checked: field.value, ref: field.ref, children: "\uC57D\uAD00 \uB3D9\uC758" })) }) }), _jsx(Field.Message, { children: errors.terms?.message })] }), _jsx(Button, { type: "submit", children: "\uC81C\uCD9C" })] }));
    },
};
//# sourceMappingURL=index.stories.js.map