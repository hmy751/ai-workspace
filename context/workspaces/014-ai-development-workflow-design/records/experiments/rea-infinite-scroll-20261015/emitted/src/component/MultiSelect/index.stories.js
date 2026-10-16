import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import MultiSelect from "./index";
import { useState } from "react";
const meta = {
    title: "Common/MultiSelect",
    component: MultiSelect,
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
const Wrapper = ({ children }) => {
    return (_jsx("div", { style: {
            width: "500px",
            border: "1px solid black",
            padding: "10px",
        }, children: children }));
};
export const Primary = {
    render() {
        const [value, setValue] = useState(["react"]);
        return (_jsx(Wrapper, { children: _jsxs(MultiSelect, { options: options, value: value, onChange: (value) => setValue(value), children: [_jsx(MultiSelect.Trigger, { placeholder: "\uAE30\uC220 \uC2A4\uD0DD\uC744 \uC120\uD0DD\uD574\uC8FC\uC138\uC694." }), _jsx(MultiSelect.Menu, { children: options.map((option) => (_jsx(MultiSelect.Item, { value: option.value, children: option.label }, option.value))) })] }) }));
    },
};
//# sourceMappingURL=index.stories.js.map