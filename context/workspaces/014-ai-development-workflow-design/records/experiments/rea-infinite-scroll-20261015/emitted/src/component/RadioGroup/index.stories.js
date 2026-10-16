import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import RadioGroup from "./index";
const meta = {
    title: "Common/RadioGroup",
    component: RadioGroup,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
export default meta;
export const Primary = {
    render() {
        return (_jsx("div", { style: { width: "200px", height: "50px", border: "1px solid black" }, children: _jsxs(RadioGroup, { name: "radio", direction: "horizontal", children: [_jsx(RadioGroup.Item, { value: "0", direction: "horizontal", children: "1" }), _jsx(RadioGroup.Item, { value: "1", direction: "horizontal", children: "2" }), _jsx(RadioGroup.Item, { value: "2", direction: "horizontal", children: "3" })] }) }));
    },
};
export const VerticalGroup = {
    render() {
        const [value, setValue] = useState("");
        return (_jsx("div", { style: { width: "200px", height: "200px", border: "1px solid black" }, children: _jsxs(RadioGroup, { value: value, name: "radio", onChange: (e) => {
                    setValue(e.target.value);
                }, direction: "vertical", children: [_jsx(RadioGroup.Item, { value: "0", direction: "horizontal", children: "1" }), _jsx(RadioGroup.Item, { value: "1", direction: "horizontal", children: "2" }), _jsx(RadioGroup.Item, { value: "2", direction: "horizontal", children: "3" })] }) }));
    },
};
export const VerticalItem = {
    render() {
        const [value, setValue] = useState("");
        return (_jsx("div", { style: { width: "200px", height: "200px", border: "1px solid black" }, children: _jsxs(RadioGroup, { value: value, name: "radio", onChange: (e) => {
                    setValue(e.target.value);
                }, direction: "horizontal", children: [_jsx(RadioGroup.Item, { value: "0", direction: "vertical", children: "1" }), _jsx(RadioGroup.Item, { value: "1", direction: "vertical", children: "2" }), _jsx(RadioGroup.Item, { value: "2", direction: "vertical", children: "3" })] }) }));
    },
};
//# sourceMappingURL=index.stories.js.map