import Text from "./index";
const meta = {
    title: "Common/Text",
    component: Text,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
};
export default meta;
export const Primary = {
    args: {
        size: "md",
        weight: "normal",
        as: "p",
        children: "Hello, World!",
    },
};
export const H1 = {
    args: {
        size: "3xl",
        weight: "bold",
        as: "h1",
        children: "H1 Hello, World!",
    },
};
export const H2 = {
    args: {
        size: "2xl",
        weight: "bold",
        as: "h2",
        children: "H2 Hello, World!",
    },
};
export const H3 = {
    args: {
        size: "xl",
        weight: "bold",
        as: "h3",
        children: "H3 Hello, World!",
    },
};
export const H4 = {
    args: {
        size: "lg",
        weight: "normal",
        as: "h4",
        children: "H4 Hello, World!",
    },
};
export const H5 = {
    args: {
        size: "lg",
        weight: "normal",
        as: "h5",
        children: "H5 Hello, World!",
    },
};
export const H6 = {
    args: {
        size: "sm",
        weight: "normal",
        as: "h6",
        children: "H6 Hello, World!",
    },
};
export const ErrorText = {
    args: {
        color: "error",
        children: "Error message",
    },
};
export const TruncatedText = {
    args: {
        truncate: true,
        maxWidth: "130px",
        children: "This is a very long text ",
    },
};
export const MultiLineTruncatedText = {
    args: {
        lines: 2,
        maxWidth: "100px",
        children: "This is a very long text ",
    },
};
//# sourceMappingURL=index.stories.js.map