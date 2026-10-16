import type { Meta, StoryObj } from "@storybook/react-webpack5";
import MultiSelect from "./index";
import { ReactNode, useState } from "react";

const meta = {
  title: "Common/MultiSelect",
  component: MultiSelect,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof MultiSelect>;

export default meta;
type Story = StoryObj<typeof meta>;

const options = [
  { value: "react", label: "React" },
  { value: "vue", label: "Vue" },
  { value: "angular", label: "Angular" },
  { value: "svelte", label: "Svelte" },
  { value: "solid", label: "Solid.js" },
];

const Wrapper = ({ children }: { children: ReactNode }) => {
  return (
    <div
      style={{
        width: "500px",
        border: "1px solid black",
        padding: "10px",
      }}
    >
      {children}
    </div>
  );
};

export const Primary = {
  render() {
    const [value, setValue] = useState<string[]>(["react"]);

    return (
      <Wrapper>
        <MultiSelect
          options={options}
          value={value}
          onChange={(value) => setValue(value)}
        >
          <MultiSelect.Trigger placeholder="기술 스택을 선택해주세요." />
          <MultiSelect.Menu>
            {options.map((option) => (
              <MultiSelect.Item key={option.value} value={option.value}>
                {option.label}
              </MultiSelect.Item>
            ))}
          </MultiSelect.Menu>
        </MultiSelect>
      </Wrapper>
    );
  },
};
