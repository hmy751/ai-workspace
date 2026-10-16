import type { Meta, StoryObj } from "@storybook/react-webpack5";
import { ElementType, FormHTMLAttributes, ReactNode, useState } from "react";
import { useForm, SubmitHandler, Controller } from "react-hook-form";

import Field from "./Field";
import Input from "../Input";
import Select from "../Select";
import Text from "../Text";
import Checkbox from "../Checkbox";
import Button from "../Button";
import RadioGroup from "../RadioGroup";
import MultiSelect from "../MultiSelect";

const meta = {
  title: "Common/FormSection",
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
};

export default meta;

type FormValues = {
  name: string;
  emailLocal: string;
  emailDomain: string;
  password: string;
  terms: boolean;
  age: string;
  techStack: string[];
};

const options = [
  { value: "react", label: "React" },
  { value: "vue", label: "Vue" },
  { value: "angular", label: "Angular" },
  { value: "svelte", label: "Svelte" },
  { value: "solid", label: "Solid.js" },
];

interface FormProps extends FormHTMLAttributes<HTMLFormElement> {
  children: ReactNode;
}

const Form = ({ children, ...restProps }: FormProps) => {
  return (
    <form
      style={{
        width: "500px",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        gap: "4px",
      }}
      {...restProps}
    >
      {children}
    </form>
  );
};

export const Primary = {
  render: () => {
    const { register, handleSubmit } = useForm<FormValues>({
      defaultValues: {
        name: "",
        emailLocal: "",
        emailDomain: "",
        password: "",
        terms: false,
      },
    });

    const onSubmit: SubmitHandler<FormValues> = (data) => {
      console.log(data);
    };

    return (
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Field ariaLabelledby="name-group">
          <Field.Title id="name-group">이름</Field.Title>
          <Field.ElementsBox>
            <Field.Label>
              <Input {...register("name")} />
            </Field.Label>
          </Field.ElementsBox>
        </Field>

        <Field ariaLabelledby="email-group">
          <Field.Title id="email-group">이메일</Field.Title>
          <Field.ElementsBox>
            <Field.Label style={{ maxWidth: "100px" }}>
              <Input {...register("emailLocal")} />
              <span className="visually-hidden">이메일 아이디 입력</span>
            </Field.Label>
            <Text>@</Text>
            <Field.Label>
              <Select {...register("emailDomain")}>
                <Select.Option value="option1">gmail.com</Select.Option>
                <Select.Option value="option2">naver.com</Select.Option>
              </Select>
              <span className="visually-hidden">이메일 도메인 선택</span>
            </Field.Label>
          </Field.ElementsBox>
        </Field>

        <Field ariaLabelledby="password-group">
          <Field.Title id="password-group">비밀번호</Field.Title>
          <Field.ElementsBox>
            <Field.Label>
              <Input {...register("password")} type="password" />
              <span className="visually-hidden">비밀번호 입력</span>
            </Field.Label>
          </Field.ElementsBox>
          <Field.Description>
            비밀번호는 숫자와 조합해서 입력해주세요.
          </Field.Description>
        </Field>

        {/* 체크박스는 register의 속성으로는 제어가 어려워 Controller를 활용한다. => checked 속성 의존성을 바꿔서 괜찮다. */}
        <Field ariaLabelledby="terms-group">
          <Field.Title id="terms-group">약관 동의</Field.Title>
          <Field.ElementsBox>
            <Checkbox id="checkbox" value="agreed" {...register("terms")}>
              약관 동의
            </Checkbox>
          </Field.ElementsBox>
        </Field>

        <Button type="submit">제출</Button>
      </Form>
    );
  },
};

// register는 단순 event객체를 받는 onChange메서드 형태로 이루어져서 event.target값을 직접받아서 처리하는 경우 적합하다.
// 포인트는 네이티브 요소 input과 직접 소통하는 형태가 register에 적합하다.
export const WithRegisterValidate = {
  render: () => {
    const {
      register,
      formState: { errors },
      handleSubmit,
    } = useForm<FormValues>({
      defaultValues: {
        name: "",
        emailLocal: "",
        emailDomain: "",
        password: "",
        age: "",
        terms: false,
      },
    });

    const onSubmit: SubmitHandler<FormValues> = (data) => {
      console.log(data);
    };

    // control, register 다양한 유효성검사
    // submit전에는 유효성 검사가 되지 않지만, 후에는 onChange 시에도 유효성 검사가 실행된다.
    // trigger 후에는 자동 포커스 된다.
    // errors.name 객체 다음에 type 속성은, 각 validate 함수의 키값과 매칭이된다.
    return (
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Field ariaLabelledby="name-group">
          <Field.Title id="name-group">이름</Field.Title>
          <Field.ElementsBox>
            <Field.Label>
              <Input
                {...register("name", {
                  required: true,
                })}
                isError={errors?.name && "필수 항목입니다."}
              />
            </Field.Label>
          </Field.ElementsBox>
          <Field.Message>{errors.name && "필수 항목입니다."}</Field.Message>
        </Field>

        <Field ariaLabelledby="email-group">
          <Field.Title id="email-group">이메일</Field.Title>
          <Field.ElementsBox>
            <Field.Label style={{ maxWidth: "100px" }}>
              <Input
                {...register("emailLocal", {
                  validate: {
                    minLength: (v) =>
                      v.length >= 3 || "최소 3글자 이상 입력해주세요.",
                  },
                })}
                isError={errors.emailLocal?.message}
              />
              <span className="visually-hidden">이메일 아이디 입력</span>
            </Field.Label>
            <Text>@</Text>
            <Field.Label>
              <Select
                {...register("emailDomain", {
                  validate: {
                    required: (v) =>
                      !!v || "반드시 도메인 하나는 선택해주세요.",
                  },
                })}
                isError={errors?.emailDomain?.message}
              >
                <Select.Option value="" disabled={true}>
                  도메인을 선택해주세요.
                </Select.Option>
                <Select.Option value="gmail">gmail.com</Select.Option>
                <Select.Option value="naver">naver.com</Select.Option>
              </Select>
              <span className="visually-hidden">이메일 도메인 선택</span>
            </Field.Label>
          </Field.ElementsBox>
          <Field.Message>
            {errors.emailLocal?.message || errors.emailDomain?.message}
          </Field.Message>
        </Field>

        <Field ariaLabelledby="password-group">
          <Field.Title id="password-group">비밀번호</Field.Title>
          <Field.ElementsBox>
            <Field.Label>
              <Input
                {...register("password", {
                  validate: {
                    require: (v) => !!v || "필수 항목입니다.",
                  },
                })}
                type="password"
                isError={errors.password?.message}
              />
              <span className="visually-hidden">비밀번호 입력</span>
            </Field.Label>
          </Field.ElementsBox>
          <Field.Description>
            비밀번호는 숫자와 조합해서 입력해주세요.
          </Field.Description>
          <Field.Message>{errors.password?.message}</Field.Message>
        </Field>

        <Field ariaLabelledby="age-group">
          <Field.Title id="age-group">나이</Field.Title>
          <Field.ElementsBox>
            <RadioGroup name={"age"} direction="horizontal">
              <RadioGroup.Item
                value="10"
                direction="horizontal"
                {...register("age", {
                  required: true,
                })}
              >
                10대
              </RadioGroup.Item>
              <RadioGroup.Item
                value="20"
                direction="horizontal"
                {...register("age", {
                  required: true,
                })}
              >
                20대
              </RadioGroup.Item>
              <RadioGroup.Item
                value="30"
                direction="horizontal"
                {...register("age", {
                  required: true,
                })}
              >
                30대
              </RadioGroup.Item>
            </RadioGroup>
          </Field.ElementsBox>
          <Field.Message>{errors.age && "필수 항목입니다."}</Field.Message>
        </Field>

        <Field ariaLabelledby="terms-group">
          <Field.Title id="terms-group">약관 동의</Field.Title>
          <Field.ElementsBox>
            <Checkbox
              id="checkbox-1"
              value="agreed"
              {...register("terms", {
                required: true,
              })}
            >
              약관 동의
            </Checkbox>
          </Field.ElementsBox>
          <Field.Message>
            {errors.terms && "약관에 동의해주세요."}
          </Field.Message>
        </Field>

        <Button type="submit">제출</Button>
      </Form>
    );
  },
};

export const WithController: StoryObj = {
  render: () => {
    const {
      control,
      formState: { errors },
      handleSubmit,
    } = useForm<FormValues>({
      mode: "onChange",
      defaultValues: {
        name: "",
        emailLocal: "",
        emailDomain: "",
        password: "",
        age: "",
        techStack: [],
        terms: false,
      },
    });

    const onSubmit: SubmitHandler<FormValues> = (data) => {
      console.log(data);
    };

    return (
      <Form onSubmit={handleSubmit(onSubmit)}>
        {/* 이름 필드 */}
        <Field ariaLabelledby="name-group">
          <Field.Title id="name-group">이름</Field.Title>
          <Field.ElementsBox>
            <Field.Label>
              <Controller
                name="name"
                control={control}
                rules={{ required: "필수 항목입니다." }}
                render={({ field, fieldState }) => (
                  <Input {...field} isError={fieldState.error?.message} />
                )}
              />
            </Field.Label>
          </Field.ElementsBox>
          <Field.Message>{errors.name?.message}</Field.Message>
        </Field>

        {/* 이메일 필드 */}
        <Field ariaLabelledby="email-group">
          <Field.Title id="email-group">이메일</Field.Title>
          <Field.ElementsBox>
            <Field.Label style={{ maxWidth: "100px" }}>
              <Controller
                name="emailLocal"
                control={control}
                rules={{
                  validate: {
                    minLength: (v) =>
                      v.length >= 3 || "최소 3글자 이상 입력해주세요.",
                  },
                }}
                render={({ field, fieldState }) => (
                  <Input {...field} isError={fieldState.error?.message} />
                )}
              />
              <span className="visually-hidden">이메일 아이디 입력</span>
            </Field.Label>
            <Text>@</Text>
            <Field.Label>
              <Controller
                name="emailDomain"
                control={control}
                rules={{
                  validate: {
                    required: (v) =>
                      !!v || "반드시 도메인 하나는 선택해주세요.",
                  },
                }}
                render={({ field, fieldState }) => (
                  <Select {...field} isError={fieldState.error?.message}>
                    <Select.Option value="" disabled>
                      도메인을 선택해주세요.
                    </Select.Option>
                    <Select.Option value="gmail">gmail.com</Select.Option>
                    <Select.Option value="naver">naver.com</Select.Option>
                  </Select>
                )}
              />
              <span className="visually-hidden">이메일 도메인 선택</span>
            </Field.Label>
          </Field.ElementsBox>
          <Field.Message>
            {errors.emailLocal?.message || errors.emailDomain?.message}
          </Field.Message>
        </Field>

        {/* 비밀번호 필드 */}
        <Field ariaLabelledby="password-group">
          <Field.Title id="password-group">비밀번호</Field.Title>
          <Field.ElementsBox>
            <Field.Label>
              <Controller
                name="password"
                control={control}
                rules={{
                  validate: { required: (v) => !!v || "필수 항목입니다." },
                }}
                render={({ field, fieldState }) => (
                  <Input
                    {...field}
                    type="password"
                    isError={fieldState.error?.message}
                  />
                )}
              />
              <span className="visually-hidden">비밀번호 입력</span>
            </Field.Label>
          </Field.ElementsBox>
          <Field.Description>
            비밀번호는 숫자와 조합해서 입력해주세요.
          </Field.Description>
          <Field.Message>{errors.password?.message}</Field.Message>
        </Field>

        {/* 나이(RadioGroup) 필드 */}
        <Field ariaLabelledby="age-group">
          <Field.Title id="age-group">나이</Field.Title>
          <Field.ElementsBox>
            <Controller
              name="age"
              control={control}
              rules={{ required: "필수 항목입니다." }}
              render={({ field }) => (
                <RadioGroup
                  name={field.name}
                  direction="horizontal"
                  value={field.value}
                  onChange={field.onChange}
                >
                  <RadioGroup.Item
                    value="10"
                    direction="horizontal"
                    ref={field.ref}
                  >
                    10대
                  </RadioGroup.Item>
                  <RadioGroup.Item value="20" direction="horizontal">
                    20대
                  </RadioGroup.Item>
                  <RadioGroup.Item value="30" direction="horizontal">
                    30대
                  </RadioGroup.Item>
                </RadioGroup>
              )}
            />
          </Field.ElementsBox>
          <Field.Message>{errors.age?.message}</Field.Message>
        </Field>

        {/* 기숙스택 필드 */}
        <Field ariaLabelledby="techStack-group">
          <Field.Title id="techStack-group">기술 스택</Field.Title>
          <Field.ElementsBox elementsHeight="50px">
            <Controller
              name="techStack"
              control={control}
              rules={{
                validate: {
                  min: (v) => v.length >= 1 || "최소 1개 이상 선택해주세요.",
                  max: (v) =>
                    v.length <= 3 || "최대 3개까지 선택이 가능합니다.",
                },
              }}
              render={({ field, fieldState }) => (
                <MultiSelect
                  options={options}
                  value={field.value}
                  onChange={field.onChange}
                >
                  <MultiSelect.Trigger
                    ref={field.ref}
                    onBlur={field.onBlur}
                    isError={!!fieldState.error}
                    placeholder="기술 스택을 선택해주세요."
                  />
                  <MultiSelect.Menu>
                    {options.map((option) => (
                      <MultiSelect.Item key={option.value} value={option.value}>
                        {option.label}
                      </MultiSelect.Item>
                    ))}
                  </MultiSelect.Menu>
                </MultiSelect>
              )}
            />
          </Field.ElementsBox>
          <Field.Description>
            기술스택은 최소 1개에서 최대 3개까지 선택해주세요.
          </Field.Description>
          <Field.Message>{errors.techStack?.message}</Field.Message>
        </Field>

        {/* 약관 동의(Checkbox) 필드 */}
        <Field ariaLabelledby="terms-group">
          <Field.Title id="terms-group">약관 동의</Field.Title>
          <Field.ElementsBox>
            <Controller
              name="terms"
              control={control}
              rules={{
                validate: (value) => value === true || "약관에 동의해주세요.",
              }}
              render={({ field }) => (
                <Checkbox
                  id="checkbox-1"
                  onChange={field.onChange}
                  checked={field.value}
                  ref={field.ref}
                >
                  약관 동의
                </Checkbox>
              )}
            />
          </Field.ElementsBox>
          <Field.Message>{errors.terms?.message}</Field.Message>
        </Field>

        <Button type="submit">제출</Button>
      </Form>
    );
  },
};
