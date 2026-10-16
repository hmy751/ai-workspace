import type { Meta, StoryObj } from "@storybook/react-webpack5";
import Dropdown from "./index";
import { useState } from "react";

const meta = {
  title: "Common/Dropdown",
  component: Dropdown,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Dropdown>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary = {
  render() {
    const [value, setValue] = useState<string | number>("");

    return (
      <Dropdown value={value} onChange={(value) => setValue(value)}>
        <Dropdown.Trigger>{"프레임워크 선택해주세요."}</Dropdown.Trigger>
        <Dropdown.Menu>
          {[1, 2, 3].map((option) => (
            <Dropdown.Item key={option} value={option}>
              {option}
            </Dropdown.Item>
          ))}
        </Dropdown.Menu>
      </Dropdown>
    );
  },
};
