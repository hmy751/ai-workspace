import type { Meta, StoryObj } from "@storybook/react-webpack5";
import { useState } from "react";

import Field from "./index";
import Input from "../../Input";
import Select from "../../Select";
import Text from "../../Text";
import RadioGroup from "../../RadioGroup";
import Checkbox from "../../Checkbox";

const meta = {
  title: "Common/Field",
  component: Field,
  parameters: {
    layout: "centered",
  },
  decorators: [
    (Story) => (
      <div
        style={{
          border: "1px solid black",
          padding: "10px",
          width: "500px",
        }}
      >
        <Story />
      </div>
    ),
  ],
  tags: ["autodocs"],
} satisfies Meta<typeof Field>;

export default meta;
type Story = StoryObj<typeof meta>;
type StoryOmitArgs = Omit<Story, "args">;

export const Primary: StoryOmitArgs = {
  render: () => {
    return (
      <Field ariaLabelledby="name-group">
        <Field.Title id="name-group">이름</Field.Title>
        <Field.ElementsBox>
          <Field.Label>
            <Input name="name" />
          </Field.Label>
        </Field.ElementsBox>
      </Field>
    );
  },
};

export const DoubleItem: StoryOmitArgs = {
  render: () => {
    const [value, setValue] = useState("");

    return (
      <Field ariaLabelledby="email-group">
        <Field.Title id="email-group">이메일</Field.Title>
        <Field.ElementsBox>
          <Field.Label style={{ maxWidth: "100px" }}>
            <Input />
            <span className="visually-hidden">이메일 아이디 입력</span>
          </Field.Label>
          <Text>@</Text>
          <Field.Label>
            <Select value={value} onChangeValue={setValue}>
              <Select.Option value="option1">gmail.com</Select.Option>
              <Select.Option value="option2">naver.com</Select.Option>
            </Select>
            <span className="visually-hidden">이메일 도메인 선택</span>
          </Field.Label>
        </Field.ElementsBox>
      </Field>
    );
  },
};

export const WithDescription: StoryOmitArgs = {
  render: () => {
    return (
      <Field ariaLabelledby="password-group">
        <Field.Title id="password-group">비밀번호</Field.Title>
        <Field.ElementsBox>
          <Field.Label>
            <Input />
            <span className="visually-hidden">비밀번호 입력</span>
          </Field.Label>
        </Field.ElementsBox>
        <Field.Description>
          비밀번호는 숫자와 조합해서 입력해주세요.
        </Field.Description>
      </Field>
    );
  },
};

export const WithError: StoryOmitArgs = {
  render: () => {
    const [errorMessage, setErrorMessage] = useState("숫자를 포함해주세요.");

    return (
      <Field ariaLabelledby="password-group">
        <Field.Title id="password-group">비밀번호</Field.Title>
        <Field.ElementsBox>
          <Field.Label>
            <Input isError={errorMessage} />
            <span className="visually-hidden">비밀번호 입력</span>
          </Field.Label>
        </Field.ElementsBox>
        <Field.Description>
          비밀번호는 숫자와 조합해서 입력해주세요.
        </Field.Description>
        <Field.Message>{errorMessage}</Field.Message>
      </Field>
    );
  },
};

export const WithRadioGroup: StoryOmitArgs = {
  render: () => {
    return (
      <Field ariaLabelledby="survey-group">
        <Field.Title id="survey-group">설문 문항</Field.Title>
        <Field.ElementsBox>
          <RadioGroup name="survey" direction="horizontal">
            <RadioGroup.Item value="1" direction="vertical">
              1
            </RadioGroup.Item>
            <RadioGroup.Item value="2" direction="vertical">
              2
            </RadioGroup.Item>
            <RadioGroup.Item value="3" direction="vertical">
              3
            </RadioGroup.Item>
          </RadioGroup>
        </Field.ElementsBox>
      </Field>
    );
  },
};

export const WithCheckBox: StoryOmitArgs = {
  render: () => {
    const [isChecked, setIsChecked] = useState(false);

    return (
      <Field ariaLabelledby="terms-group">
        <Field.Title id="terms-group">약관 동의</Field.Title>
        <Field.ElementsBox>
          <Checkbox
            id="checkbox"
            checked={isChecked}
            onChange={(e) => setIsChecked(e.target.checked)}
            value="agreed"
            name="terms"
          >
            약관 동의
          </Checkbox>
        </Field.ElementsBox>
      </Field>
    );
  },
};
