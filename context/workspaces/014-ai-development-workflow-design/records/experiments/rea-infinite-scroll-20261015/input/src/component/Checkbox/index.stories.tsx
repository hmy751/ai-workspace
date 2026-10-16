import type { Meta, StoryObj } from "@storybook/react-webpack5";

import Checkbox from "./index";
import { useState } from "react";

const meta = {
  title: "Common/Checkbox",
  component: Checkbox,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Checkbox>;

export default meta;
type Story = StoryObj<typeof meta>;
type StoryOmitArgs = Omit<Story, "args">;

export const Primary: StoryOmitArgs = {
  render: () => {
    const [isChecked, setIsChecked] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setIsChecked(e.target.checked);
    };

    return (
      <Checkbox
        id="checkbox"
        checked={isChecked}
        onChange={handleChange}
        value="agreed"
        name="terms"
      >
        약관동의
      </Checkbox>
    );
  },
};

export const Disabled: StoryOmitArgs = {
  render: () => {
    const [isChecked, setIsChecked] = useState(false);

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setIsChecked(event.target.checked);
    };

    return (
      <Checkbox
        id="checkbox"
        checked={isChecked}
        disabled={true}
        onChange={handleChange}
        value="agreed"
        name="terms"
      >
        약관동의
      </Checkbox>
    );
  },
};
