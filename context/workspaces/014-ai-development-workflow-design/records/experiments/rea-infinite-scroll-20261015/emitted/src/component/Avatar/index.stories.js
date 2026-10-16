import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Avatar from "./index";
const meta = {
    title: "Common/Avatar",
    component: Avatar,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        size: {
            control: "select",
            options: ["xs", "sm", "md", "lg", "xl"],
        },
    },
};
export default meta;
export const Primary = {
    args: {
        src: "/images/profile.webp",
        size: "md",
    },
};
export const ExtraSmall = {
    args: {
        src: "/images/profile.webp",
        size: "xs",
    },
};
export const Small = {
    args: {
        src: "/images/profile.webp",
        size: "sm",
    },
};
export const Large = {
    args: {
        src: "/images/profile.webp",
        size: "lg",
    },
};
export const ExtraLarge = {
    args: {
        src: "/images/profile.webp",
        size: "xl",
    },
};
export const Group = {
    args: {
        src: "",
        size: "xl",
    },
    render: () => (_jsxs("div", { style: { display: "flex", gap: "8px", alignItems: "center" }, children: [_jsx(Avatar, { src: "/images/profile.webp", size: "xs" }), _jsx(Avatar, { src: "/images/profile.webp", size: "sm" }), _jsx(Avatar, { src: "/images/profile.webp", size: "md" }), _jsx(Avatar, { src: "/images/profile.webp", size: "lg" }), _jsx(Avatar, { src: "/images/profile.webp", size: "xl" })] })),
};
//# sourceMappingURL=index.stories.js.map