import type { Meta, StoryObj } from "@storybook/react-webpack5";

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
} satisfies Meta<typeof Spinner>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    size: "md",
  },
};
