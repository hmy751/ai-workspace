import Spinner from "./index";
const meta = {
    title: "Common/Spinner",
    component: Spinner,
    parameters: {
        layout: "centered",
    },
    tags: ["autodocs"],
    argTypes: {
        size: { control: "select", options: ["sm", "md", "lg"] },
        color: { control: "color" },
    },
};
export default meta;
export const Primary = {
    args: {
        size: "md",
    },
};
//# sourceMappingURL=index.stories.js.map