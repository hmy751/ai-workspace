import type { Meta, StoryObj } from "@storybook/react-webpack5";
import Avatar from "./index";

const meta = {
  title: "Common/Avatar",
  component: Avatar,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    size: {
      control: "select",
      options: ["xs", "sm", "md", "lg", "xl"],
    },
  },
} satisfies Meta<typeof Avatar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    src: "/images/profile.webp",
    size: "md",
  },
};

export const ExtraSmall: Story = {
  args: {
    src: "/images/profile.webp",
    size: "xs",
  },
};

export const Small: Story = {
  args: {
    src: "/images/profile.webp",
    size: "sm",
  },
};

export const Large: Story = {
  args: {
    src: "/images/profile.webp",
    size: "lg",
  },
};

export const ExtraLarge: Story = {
  args: {
    src: "/images/profile.webp",
    size: "xl",
  },
};

export const Group: Story = {
  args: {
    src: "",
    size: "xl",
  },
  render: () => (
    <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
      <Avatar src="/images/profile.webp" size="xs" />
      <Avatar src="/images/profile.webp" size="sm" />
      <Avatar src="/images/profile.webp" size="md" />
      <Avatar src="/images/profile.webp" size="lg" />
      <Avatar src="/images/profile.webp" size="xl" />
    </div>
  ),
};
