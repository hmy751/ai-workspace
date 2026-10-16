import type { Meta, StoryObj } from "@storybook/react-webpack5";
import { useState } from "react";
import RadioGroup from "./index";

const meta = {
  title: "Common/RadioGroup",
  component: RadioGroup,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof RadioGroup>;

export default meta;
type Story = StoryObj<typeof meta>;
type StoryOmitArgs = Omit<Story, "args">;

export const Primary: StoryOmitArgs = {
  render() {
    return (
      <div
        style={{ width: "200px", height: "50px", border: "1px solid black" }}
      >
        <RadioGroup name="radio" direction="horizontal">
          <RadioGroup.Item value="0" direction="horizontal">
            1
          </RadioGroup.Item>
          <RadioGroup.Item value="1" direction="horizontal">
            2
          </RadioGroup.Item>
          <RadioGroup.Item value="2" direction="horizontal">
            3
          </RadioGroup.Item>
        </RadioGroup>
      </div>
    );
  },
};

export const VerticalGroup: StoryOmitArgs = {
  render() {
    const [value, setValue] = useState<string>("");

    return (
      <div
        style={{ width: "200px", height: "200px", border: "1px solid black" }}
      >
        <RadioGroup
          value={value}
          name="radio"
          onChange={(e) => {
            setValue(e.target.value);
          }}
          direction="vertical"
        >
          <RadioGroup.Item value="0" direction="horizontal">
            1
          </RadioGroup.Item>
          <RadioGroup.Item value="1" direction="horizontal">
            2
          </RadioGroup.Item>
          <RadioGroup.Item value="2" direction="horizontal">
            3
          </RadioGroup.Item>
        </RadioGroup>
      </div>
    );
  },
};

export const VerticalItem: StoryOmitArgs = {
  render() {
    const [value, setValue] = useState<string>("");

    return (
      <div
        style={{ width: "200px", height: "200px", border: "1px solid black" }}
      >
        <RadioGroup
          value={value}
          name="radio"
          onChange={(e) => {
            setValue(e.target.value);
          }}
          direction="horizontal"
        >
          <RadioGroup.Item value="0" direction="vertical">
            1
          </RadioGroup.Item>
          <RadioGroup.Item value="1" direction="vertical">
            2
          </RadioGroup.Item>
          <RadioGroup.Item value="2" direction="vertical">
            3
          </RadioGroup.Item>
        </RadioGroup>
      </div>
    );
  },
};
