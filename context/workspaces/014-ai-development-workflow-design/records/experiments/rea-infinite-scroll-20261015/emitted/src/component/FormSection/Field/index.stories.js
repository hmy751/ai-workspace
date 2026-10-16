import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import Field from "./index";
import Input from "../../Input";
import Select from "../../Select";
import Text from "../../Text";
import RadioGroup from "../../RadioGroup";
import Checkbox from "../../Checkbox";
const meta = {
    title: "Common/Field",
    component: Field,
    parameters: {
        layout: "centered",
    },
    decorators: [
        (Story) => (_jsx("div", { style: {
                border: "1px solid black",
                padding: "10px",
                width: "500px",
            }, children: _jsx(Story, {}) })),
    ],
    tags: ["autodocs"],
};
export default meta;
export const Primary = {
    render: () => {
        return (_jsxs(Field, { ariaLabelledby: "name-group", children: [_jsx(Field.Title, { id: "name-group", children: "\uC774\uB984" }), _jsx(Field.ElementsBox, { children: _jsx(Field.Label, { children: _jsx(Input, { name: "name" }) }) })] }));
    },
};
export const DoubleItem = {
    render: () => {
        const [value, setValue] = useState("");
        return (_jsxs(Field, { ariaLabelledby: "email-group", children: [_jsx(Field.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), _jsxs(Field.ElementsBox, { children: [_jsxs(Field.Label, { style: { maxWidth: "100px" }, children: [_jsx(Input, {}), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), _jsx(Text, { children: "@" }), _jsxs(Field.Label, { children: [_jsxs(Select, { value: value, onChangeValue: setValue, children: [_jsx(Select.Option, { value: "option1", children: "gmail.com" }), _jsx(Select.Option, { value: "option2", children: "naver.com" })] }), _jsx("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] })] }));
    },
};
export const WithDescription = {
    render: () => {
        return (_jsxs(Field, { ariaLabelledby: "password-group", children: [_jsx(Field.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), _jsx(Field.ElementsBox, { children: _jsxs(Field.Label, { children: [_jsx(Input, {}), _jsx("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), _jsx(Field.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." })] }));
    },
};
export const WithError = {
    render: () => {
        const [errorMessage, setErrorMessage] = useState("숫자를 포함해주세요.");
        return (_jsxs(Field, { ariaLabelledby: "password-group", children: [_jsx(Field.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), _jsx(Field.ElementsBox, { children: _jsxs(Field.Label, { children: [_jsx(Input, { isError: errorMessage }), _jsx("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), _jsx(Field.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." }), _jsx(Field.Message, { children: errorMessage })] }));
    },
};
export const WithRadioGroup = {
    render: () => {
        return (_jsxs(Field, { ariaLabelledby: "survey-group", children: [_jsx(Field.Title, { id: "survey-group", children: "\uC124\uBB38 \uBB38\uD56D" }), _jsx(Field.ElementsBox, { children: _jsxs(RadioGroup, { name: "survey", direction: "horizontal", children: [_jsx(RadioGroup.Item, { value: "1", direction: "vertical", children: "1" }), _jsx(RadioGroup.Item, { value: "2", direction: "vertical", children: "2" }), _jsx(RadioGroup.Item, { value: "3", direction: "vertical", children: "3" })] }) })] }));
    },
};
export const WithCheckBox = {
    render: () => {
        const [isChecked, setIsChecked] = useState(false);
        return (_jsxs(Field, { ariaLabelledby: "terms-group", children: [_jsx(Field.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), _jsx(Field.ElementsBox, { children: _jsx(Checkbox, { id: "checkbox", checked: isChecked, onChange: (e) => setIsChecked(e.target.checked), value: "agreed", name: "terms", children: "\uC57D\uAD00 \uB3D9\uC758" }) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map