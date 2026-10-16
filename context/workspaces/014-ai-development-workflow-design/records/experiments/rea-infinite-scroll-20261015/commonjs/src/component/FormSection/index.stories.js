"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WithController = exports.WithRegisterValidate = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const react_hook_form_1 = require("react-hook-form");
const Field_1 = __importDefault(require("./Field"));
const Input_1 = __importDefault(require("../Input"));
const Select_1 = __importDefault(require("../Select"));
const Text_1 = __importDefault(require("../Text"));
const Checkbox_1 = __importDefault(require("../Checkbox"));
const Button_1 = __importDefault(require("../Button"));
const RadioGroup_1 = __importDefault(require("../RadioGroup"));
const MultiSelect_1 = __importDefault(require("../MultiSelect"));
const meta = {
    title: "Common/FormSection",
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
exports.default = meta;
const options = [
    { value: "react", label: "React" },
    { value: "vue", label: "Vue" },
    { value: "angular", label: "Angular" },
    { value: "svelte", label: "Svelte" },
    { value: "solid", label: "Solid.js" },
];
const Form = ({ children, ...restProps }) => {
    return ((0, jsx_runtime_1.jsx)("form", { style: {
            width: "500px",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            gap: "4px",
        }, ...restProps, children: children }));
};
exports.Primary = {
    render: () => {
        const { register, handleSubmit } = (0, react_hook_form_1.useForm)({
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
        return ((0, jsx_runtime_1.jsxs)(Form, { onSubmit: handleSubmit(onSubmit), children: [(0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "name-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "name-group", children: "\uC774\uB984" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(Field_1.default.Label, { children: (0, jsx_runtime_1.jsx)(Input_1.default, { ...register("name") }) }) })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "email-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), (0, jsx_runtime_1.jsxs)(Field_1.default.ElementsBox, { children: [(0, jsx_runtime_1.jsxs)(Field_1.default.Label, { style: { maxWidth: "100px" }, children: [(0, jsx_runtime_1.jsx)(Input_1.default, { ...register("emailLocal") }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), (0, jsx_runtime_1.jsx)(Text_1.default, { children: "@" }), (0, jsx_runtime_1.jsxs)(Field_1.default.Label, { children: [(0, jsx_runtime_1.jsxs)(Select_1.default, { ...register("emailDomain"), children: [(0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "option1", children: "gmail.com" }), (0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "option2", children: "naver.com" })] }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "password-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsxs)(Field_1.default.Label, { children: [(0, jsx_runtime_1.jsx)(Input_1.default, { ...register("password"), type: "password" }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "terms-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(Checkbox_1.default, { id: "checkbox", value: "agreed", ...register("terms"), children: "\uC57D\uAD00 \uB3D9\uC758" }) })] }), (0, jsx_runtime_1.jsx)(Button_1.default, { type: "submit", children: "\uC81C\uCD9C" })] }));
    },
};
// register는 단순 event객체를 받는 onChange메서드 형태로 이루어져서 event.target값을 직접받아서 처리하는 경우 적합하다.
// 포인트는 네이티브 요소 input과 직접 소통하는 형태가 register에 적합하다.
exports.WithRegisterValidate = {
    render: () => {
        const { register, formState: { errors }, handleSubmit, } = (0, react_hook_form_1.useForm)({
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
        return ((0, jsx_runtime_1.jsxs)(Form, { onSubmit: handleSubmit(onSubmit), children: [(0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "name-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "name-group", children: "\uC774\uB984" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(Field_1.default.Label, { children: (0, jsx_runtime_1.jsx)(Input_1.default, { ...register("name", {
                                        required: true,
                                    }), isError: errors?.name && "필수 항목입니다." }) }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.name && "필수 항목입니다." })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "email-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), (0, jsx_runtime_1.jsxs)(Field_1.default.ElementsBox, { children: [(0, jsx_runtime_1.jsxs)(Field_1.default.Label, { style: { maxWidth: "100px" }, children: [(0, jsx_runtime_1.jsx)(Input_1.default, { ...register("emailLocal", {
                                                validate: {
                                                    minLength: (v) => v.length >= 3 || "최소 3글자 이상 입력해주세요.",
                                                },
                                            }), isError: errors.emailLocal?.message }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), (0, jsx_runtime_1.jsx)(Text_1.default, { children: "@" }), (0, jsx_runtime_1.jsxs)(Field_1.default.Label, { children: [(0, jsx_runtime_1.jsxs)(Select_1.default, { ...register("emailDomain", {
                                                validate: {
                                                    required: (v) => !!v || "반드시 도메인 하나는 선택해주세요.",
                                                },
                                            }), isError: errors?.emailDomain?.message, children: [(0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "", disabled: true, children: "\uB3C4\uBA54\uC778\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "gmail", children: "gmail.com" }), (0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "naver", children: "naver.com" })] }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.emailLocal?.message || errors.emailDomain?.message })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "password-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsxs)(Field_1.default.Label, { children: [(0, jsx_runtime_1.jsx)(Input_1.default, { ...register("password", {
                                            validate: {
                                                require: (v) => !!v || "필수 항목입니다.",
                                            },
                                        }), type: "password", isError: errors.password?.message }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.password?.message })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "age-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "age-group", children: "\uB098\uC774" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsxs)(RadioGroup_1.default, { name: "age", direction: "horizontal", children: [(0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "10", direction: "horizontal", ...register("age", {
                                            required: true,
                                        }), children: "10\uB300" }), (0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "20", direction: "horizontal", ...register("age", {
                                            required: true,
                                        }), children: "20\uB300" }), (0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "30", direction: "horizontal", ...register("age", {
                                            required: true,
                                        }), children: "30\uB300" })] }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.age && "필수 항목입니다." })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "terms-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(Checkbox_1.default, { id: "checkbox-1", value: "agreed", ...register("terms", {
                                    required: true,
                                }), children: "\uC57D\uAD00 \uB3D9\uC758" }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.terms && "약관에 동의해주세요." })] }), (0, jsx_runtime_1.jsx)(Button_1.default, { type: "submit", children: "\uC81C\uCD9C" })] }));
    },
};
exports.WithController = {
    render: () => {
        const { control, formState: { errors }, handleSubmit, } = (0, react_hook_form_1.useForm)({
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
        return ((0, jsx_runtime_1.jsxs)(Form, { onSubmit: handleSubmit(onSubmit), children: [(0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "name-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "name-group", children: "\uC774\uB984" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(Field_1.default.Label, { children: (0, jsx_runtime_1.jsx)(react_hook_form_1.Controller, { name: "name", control: control, rules: { required: "필수 항목입니다." }, render: ({ field, fieldState }) => ((0, jsx_runtime_1.jsx)(Input_1.default, { ...field, isError: fieldState.error?.message })) }) }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.name?.message })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "email-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), (0, jsx_runtime_1.jsxs)(Field_1.default.ElementsBox, { children: [(0, jsx_runtime_1.jsxs)(Field_1.default.Label, { style: { maxWidth: "100px" }, children: [(0, jsx_runtime_1.jsx)(react_hook_form_1.Controller, { name: "emailLocal", control: control, rules: {
                                                validate: {
                                                    minLength: (v) => v.length >= 3 || "최소 3글자 이상 입력해주세요.",
                                                },
                                            }, render: ({ field, fieldState }) => ((0, jsx_runtime_1.jsx)(Input_1.default, { ...field, isError: fieldState.error?.message })) }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), (0, jsx_runtime_1.jsx)(Text_1.default, { children: "@" }), (0, jsx_runtime_1.jsxs)(Field_1.default.Label, { children: [(0, jsx_runtime_1.jsx)(react_hook_form_1.Controller, { name: "emailDomain", control: control, rules: {
                                                validate: {
                                                    required: (v) => !!v || "반드시 도메인 하나는 선택해주세요.",
                                                },
                                            }, render: ({ field, fieldState }) => ((0, jsx_runtime_1.jsxs)(Select_1.default, { ...field, isError: fieldState.error?.message, children: [(0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "", disabled: true, children: "\uB3C4\uBA54\uC778\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "gmail", children: "gmail.com" }), (0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "naver", children: "naver.com" })] })) }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.emailLocal?.message || errors.emailDomain?.message })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "password-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsxs)(Field_1.default.Label, { children: [(0, jsx_runtime_1.jsx)(react_hook_form_1.Controller, { name: "password", control: control, rules: {
                                            validate: { required: (v) => !!v || "필수 항목입니다." },
                                        }, render: ({ field, fieldState }) => ((0, jsx_runtime_1.jsx)(Input_1.default, { ...field, type: "password", isError: fieldState.error?.message })) }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.password?.message })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "age-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "age-group", children: "\uB098\uC774" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(react_hook_form_1.Controller, { name: "age", control: control, rules: { required: "필수 항목입니다." }, render: ({ field }) => ((0, jsx_runtime_1.jsxs)(RadioGroup_1.default, { name: field.name, direction: "horizontal", value: field.value, onChange: field.onChange, children: [(0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "10", direction: "horizontal", ref: field.ref, children: "10\uB300" }), (0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "20", direction: "horizontal", children: "20\uB300" }), (0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "30", direction: "horizontal", children: "30\uB300" })] })) }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.age?.message })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "techStack-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "techStack-group", children: "\uAE30\uC220 \uC2A4\uD0DD" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { elementsHeight: "50px", children: (0, jsx_runtime_1.jsx)(react_hook_form_1.Controller, { name: "techStack", control: control, rules: {
                                    validate: {
                                        min: (v) => v.length >= 1 || "최소 1개 이상 선택해주세요.",
                                        max: (v) => v.length <= 3 || "최대 3개까지 선택이 가능합니다.",
                                    },
                                }, render: ({ field, fieldState }) => ((0, jsx_runtime_1.jsxs)(MultiSelect_1.default, { options: options, value: field.value, onChange: field.onChange, children: [(0, jsx_runtime_1.jsx)(MultiSelect_1.default.Trigger, { ref: field.ref, onBlur: field.onBlur, isError: !!fieldState.error, placeholder: "\uAE30\uC220 \uC2A4\uD0DD\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(MultiSelect_1.default.Menu, { children: options.map((option) => ((0, jsx_runtime_1.jsx)(MultiSelect_1.default.Item, { value: option.value, children: option.label }, option.value))) })] })) }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Description, { children: "\uAE30\uC220\uC2A4\uD0DD\uC740 \uCD5C\uC18C 1\uAC1C\uC5D0\uC11C \uCD5C\uB300 3\uAC1C\uAE4C\uC9C0 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.techStack?.message })] }), (0, jsx_runtime_1.jsxs)(Field_1.default, { ariaLabelledby: "terms-group", children: [(0, jsx_runtime_1.jsx)(Field_1.default.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), (0, jsx_runtime_1.jsx)(Field_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(react_hook_form_1.Controller, { name: "terms", control: control, rules: {
                                    validate: (value) => value === true || "약관에 동의해주세요.",
                                }, render: ({ field }) => ((0, jsx_runtime_1.jsx)(Checkbox_1.default, { id: "checkbox-1", onChange: field.onChange, checked: field.value, ref: field.ref, children: "\uC57D\uAD00 \uB3D9\uC758" })) }) }), (0, jsx_runtime_1.jsx)(Field_1.default.Message, { children: errors.terms?.message })] }), (0, jsx_runtime_1.jsx)(Button_1.default, { type: "submit", children: "\uC81C\uCD9C" })] }));
    },
};
//# sourceMappingURL=index.stories.js.map