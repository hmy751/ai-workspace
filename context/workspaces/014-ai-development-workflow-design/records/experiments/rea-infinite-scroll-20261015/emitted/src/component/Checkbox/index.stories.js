import { jsx as _jsx } from "react/jsx-runtime";
import Checkbox from "./index";
import { useState } from "react";
const meta = {
    title: "Common/Checkbox",
    component: Checkbox,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
export default meta;
export const Primary = {
    render: () => {
        const [isChecked, setIsChecked] = useState(false);
        const handleChange = (e) => {
            setIsChecked(e.target.checked);
        };
        return (_jsx(Checkbox, { id: "checkbox", checked: isChecked, onChange: handleChange, value: "agreed", name: "terms", children: "\uC57D\uAD00\uB3D9\uC758" }));
    },
};
export const Disabled = {
    render: () => {
        const [isChecked, setIsChecked] = useState(false);
        const handleChange = (event) => {
            setIsChecked(event.target.checked);
        };
        return (_jsx(Checkbox, { id: "checkbox", checked: isChecked, disabled: true, onChange: handleChange, value: "agreed", name: "terms", children: "\uC57D\uAD00\uB3D9\uC758" }));
    },
};
//# sourceMappingURL=index.stories.js.map