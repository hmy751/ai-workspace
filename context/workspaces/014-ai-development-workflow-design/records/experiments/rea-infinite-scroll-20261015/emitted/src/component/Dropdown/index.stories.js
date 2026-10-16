import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Dropdown from "./index";
import { useState } from "react";
const meta = {
    title: "Common/Dropdown",
    component: Dropdown,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
export default meta;
export const Primary = {
    render() {
        const [value, setValue] = useState("");
        return (_jsxs(Dropdown, { value: value, onChange: (value) => setValue(value), children: [_jsx(Dropdown.Trigger, { children: "프레임워크 선택해주세요." }), _jsx(Dropdown.Menu, { children: [1, 2, 3].map((option) => (_jsx(Dropdown.Item, { value: option, children: option }, option))) })] }));
    },
};
//# sourceMappingURL=index.stories.js.map