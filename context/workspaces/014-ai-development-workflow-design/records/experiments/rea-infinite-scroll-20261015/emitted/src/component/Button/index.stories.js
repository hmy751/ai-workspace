import { jsx as _jsx } from "react/jsx-runtime";
import Button from "./index";
const meta = {
    title: "Common/Button",
    component: Button,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        variant: {
            control: "select",
            options: ["primary", "secondary", "outline"],
        },
        size: { control: "select", options: ["sm", "md", "lg"] },
        fullWidth: { control: "boolean" },
        isLoading: { control: "boolean" },
        disabled: { control: "boolean" },
    },
};
export default meta;
export const Primary = {
    args: {
        children: "Button",
        variant: "primary",
        size: "md",
        fullWidth: false,
        isLoading: false,
    },
};
export const Secondary = {
    args: {
        children: "Button",
        variant: "secondary",
        size: "md",
    },
};
export const Outline = {
    args: {
        children: "Button",
        variant: "outline",
        size: "md",
    },
};
export const Text = {
    args: {
        children: "Button",
        variant: "text",
        size: "md",
    },
};
export const Loading = {
    args: {
        children: "Loading",
        isLoading: true,
    },
};
export const FullWidth = {
    render: (args) => (_jsx("div", { style: {
            width: "300px",
            border: "1px solid var(--color-base-black)",
            padding: "var(--space-4)",
        }, children: _jsx(Button, { ...args }) })),
    args: {
        children: "Full Width",
        fullWidth: true,
    },
};
export const SizeSmall = {
    args: {
        children: "Small",
        size: "sm",
    },
};
export const SizeLarge = {
    args: {
        children: "Large",
        size: "lg",
    },
};
export const Disabled = {
    args: {
        children: "Disabled",
        disabled: true,
    },
};
//# sourceMappingURL=index.stories.js.map