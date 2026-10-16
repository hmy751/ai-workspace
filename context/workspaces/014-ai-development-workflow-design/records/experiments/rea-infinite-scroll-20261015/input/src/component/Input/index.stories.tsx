import type { Meta, StoryObj } from "@storybook/react-webpack5";
import Input from "./index";
import { useState } from "react";
import { useForm } from "react-hook-form";
import Button from "../Button";

const meta = {
  title: "Common/Input",
  component: Input,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    placeholder: {
      control: {
        type: "text",
      },
    },
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    placeholder: "Enter Text...",
  },
  render() {
    const [isFocused, setIsFocused] = useState(false);
    const [isTouched, setIsTouched] = useState(false);

    return (
      <div>
        <Input
          {...Primary.args}
          isFocused={isFocused}
          isTouched={isTouched}
          onChangeFocus={setIsFocused}
          onChangeTouch={setIsTouched}
        />
      </div>
    );
  },
};

export const Focused: Story = {
  args: {
    placeholder: "Enter Text...",
  },
  render() {
    const [isTouched, setIsTouched] = useState(true);
    const [isFocused, setIsFocused] = useState(true);
    return (
      <div>
        <Input
          placeholder="Enter Text..."
          isFocused={isFocused}
          isTouched={isTouched}
          onChangeFocus={setIsFocused}
          onChangeTouch={setIsTouched}
        />
      </div>
    );
  },
};

export const Touched: Story = {
  args: {
    placeholder: "Enter Text...",
  },
  render() {
    const [isTouched, setIsTouched] = useState(true);
    const [isFocused, setIsFocused] = useState(false);

    return (
      <div>
        <Input
          placeholder="Enter Text..."
          isTouched={isTouched}
          isFocused={isFocused}
          onChangeTouch={setIsTouched}
          onChangeFocus={setIsFocused}
        />
      </div>
    );
  },
};

export const Error: Story = {
  args: {
    placeholder: "Enter Text...",
  },
  render() {
    const [isFocused, setIsFocused] = useState(false);
    const [isTouched, setIsTouched] = useState(false);
    const [errorMessage, setErrorMessage] = useState("Error");
    return (
      <div>
        <Input
          placeholder="Enter Text..."
          isFocused={isFocused}
          isTouched={isTouched}
          onChangeFocus={setIsFocused}
          onChangeTouch={setIsTouched}
          isError={errorMessage}
        />
      </div>
    );
  },
};

export const Disabled: Story = {
  args: {
    placeholder: "Enter Text...",
  },
  render() {
    const [isTouched, setIsTouched] = useState(false);
    const [isFocused, setIsFocused] = useState(false);
    return (
      <div>
        <Input
          placeholder="Enter Text..."
          isDisabled={true}
          isTouched={isTouched}
          isFocused={isFocused}
        />
      </div>
    );
  },
};

// 내 컴포넌트는 내부에 touch처리를해서 지금 잘 되지만, 일반적으로 touche를 적용하려면 Controller를 사용해야 한다.
export const UseHookForm = {
  render: () => {
    const { control, register } = useForm({
      defaultValues: {
        name: "",
      },
    });

    const handleClick = () => {
      console.log(control._formValues);
    };

    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignContent: "center",
        }}
      >
        <Input {...register("name")} />
        <Button onClick={handleClick}>출력하기</Button>
      </div>
    );
  },
};
