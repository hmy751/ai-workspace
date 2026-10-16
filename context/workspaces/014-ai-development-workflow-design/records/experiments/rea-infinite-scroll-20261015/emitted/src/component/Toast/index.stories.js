import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import Toast from "./index";
import useToastStore from "../../store/useToastStore";
import Button from "../Button";
const meta = {
    title: "Common/Toast",
    component: Toast,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
export default meta;
const ToastDemo = () => {
    const addToast = useToastStore((state) => state.addToast);
    const showToast = () => {
        addToast({
            title: "Toast Title",
            description: "This is a toast message",
            duration: 3000,
        });
    };
    return (_jsxs(_Fragment, { children: [_jsx(Button, { onClick: showToast, children: "Show Toast" }), _jsx(Toast, {})] }));
};
export const Primary = {
    render: () => _jsx(ToastDemo, {}),
};
//# sourceMappingURL=index.stories.js.map