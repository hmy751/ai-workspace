"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WithCheckBox = exports.WithRadioGroup = exports.WithError = exports.WithDescription = exports.DoubleItem = exports.Primary = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const index_1 = __importDefault(require("./index"));
const Input_1 = __importDefault(require("../../Input"));
const Select_1 = __importDefault(require("../../Select"));
const Text_1 = __importDefault(require("../../Text"));
const RadioGroup_1 = __importDefault(require("../../RadioGroup"));
const Checkbox_1 = __importDefault(require("../../Checkbox"));
const meta = {
    title: "Common/Field",
    component: index_1.default,
    parameters: {
        layout: "centered",
    },
    decorators: [
        (Story) => ((0, jsx_runtime_1.jsx)("div", { style: {
                border: "1px solid black",
                padding: "10px",
                width: "500px",
            }, children: (0, jsx_runtime_1.jsx)(Story, {}) })),
    ],
    tags: ["autodocs"],
};
exports.default = meta;
exports.Primary = {
    render: () => {
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ariaLabelledby: "name-group", children: [(0, jsx_runtime_1.jsx)(index_1.default.Title, { id: "name-group", children: "\uC774\uB984" }), (0, jsx_runtime_1.jsx)(index_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(index_1.default.Label, { children: (0, jsx_runtime_1.jsx)(Input_1.default, { name: "name" }) }) })] }));
    },
};
exports.DoubleItem = {
    render: () => {
        const [value, setValue] = (0, react_1.useState)("");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ariaLabelledby: "email-group", children: [(0, jsx_runtime_1.jsx)(index_1.default.Title, { id: "email-group", children: "\uC774\uBA54\uC77C" }), (0, jsx_runtime_1.jsxs)(index_1.default.ElementsBox, { children: [(0, jsx_runtime_1.jsxs)(index_1.default.Label, { style: { maxWidth: "100px" }, children: [(0, jsx_runtime_1.jsx)(Input_1.default, {}), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uC544\uC774\uB514 \uC785\uB825" })] }), (0, jsx_runtime_1.jsx)(Text_1.default, { children: "@" }), (0, jsx_runtime_1.jsxs)(index_1.default.Label, { children: [(0, jsx_runtime_1.jsxs)(Select_1.default, { value: value, onChangeValue: setValue, children: [(0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "option1", children: "gmail.com" }), (0, jsx_runtime_1.jsx)(Select_1.default.Option, { value: "option2", children: "naver.com" })] }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uC774\uBA54\uC77C \uB3C4\uBA54\uC778 \uC120\uD0DD" })] })] })] }));
    },
};
exports.WithDescription = {
    render: () => {
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ariaLabelledby: "password-group", children: [(0, jsx_runtime_1.jsx)(index_1.default.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), (0, jsx_runtime_1.jsx)(index_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsxs)(index_1.default.Label, { children: [(0, jsx_runtime_1.jsx)(Input_1.default, {}), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), (0, jsx_runtime_1.jsx)(index_1.default.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." })] }));
    },
};
exports.WithError = {
    render: () => {
        const [errorMessage, setErrorMessage] = (0, react_1.useState)("숫자를 포함해주세요.");
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ariaLabelledby: "password-group", children: [(0, jsx_runtime_1.jsx)(index_1.default.Title, { id: "password-group", children: "\uBE44\uBC00\uBC88\uD638" }), (0, jsx_runtime_1.jsx)(index_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsxs)(index_1.default.Label, { children: [(0, jsx_runtime_1.jsx)(Input_1.default, { isError: errorMessage }), (0, jsx_runtime_1.jsx)("span", { className: "visually-hidden", children: "\uBE44\uBC00\uBC88\uD638 \uC785\uB825" })] }) }), (0, jsx_runtime_1.jsx)(index_1.default.Description, { children: "\uBE44\uBC00\uBC88\uD638\uB294 \uC22B\uC790\uC640 \uC870\uD569\uD574\uC11C \uC785\uB825\uD574\uC8FC\uC138\uC694." }), (0, jsx_runtime_1.jsx)(index_1.default.Message, { children: errorMessage })] }));
    },
};
exports.WithRadioGroup = {
    render: () => {
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ariaLabelledby: "survey-group", children: [(0, jsx_runtime_1.jsx)(index_1.default.Title, { id: "survey-group", children: "\uC124\uBB38 \uBB38\uD56D" }), (0, jsx_runtime_1.jsx)(index_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsxs)(RadioGroup_1.default, { name: "survey", direction: "horizontal", children: [(0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "1", direction: "vertical", children: "1" }), (0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "2", direction: "vertical", children: "2" }), (0, jsx_runtime_1.jsx)(RadioGroup_1.default.Item, { value: "3", direction: "vertical", children: "3" })] }) })] }));
    },
};
exports.WithCheckBox = {
    render: () => {
        const [isChecked, setIsChecked] = (0, react_1.useState)(false);
        return ((0, jsx_runtime_1.jsxs)(index_1.default, { ariaLabelledby: "terms-group", children: [(0, jsx_runtime_1.jsx)(index_1.default.Title, { id: "terms-group", children: "\uC57D\uAD00 \uB3D9\uC758" }), (0, jsx_runtime_1.jsx)(index_1.default.ElementsBox, { children: (0, jsx_runtime_1.jsx)(Checkbox_1.default, { id: "checkbox", checked: isChecked, onChange: (e) => setIsChecked(e.target.checked), value: "agreed", name: "terms", children: "\uC57D\uAD00 \uB3D9\uC758" }) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map