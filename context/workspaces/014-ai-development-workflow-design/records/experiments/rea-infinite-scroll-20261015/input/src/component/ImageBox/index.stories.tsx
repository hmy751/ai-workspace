import type { Meta, StoryObj } from "@storybook/react-webpack5";
import Image from "./index";

const meta: Meta<typeof Image> = {
  title: "Common/Image",
  component: Image,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    src: { control: "text", description: "이미지 경로" },
    alt: { control: "text", description: "대체 텍스트 (접근성)" },
    aspectRatio: {
      control: "text",
      description: "가로/세로 비율 (예: '16/9')",
    },
    backgroundColor: {
      control: "color",
      description: "Contained 이미지의 배경색",
    },
    children: { description: "이미지 위 오버레이 요소" },
    fallback: { description: "에러 발생 시 보여줄 UI" },
  },
};

export default meta;
type Story = StoryObj<typeof Image>;

export const Standard: Story = {
  args: {
    src: "https://picsum.photos/seed/standard/400/400",
    alt: "A standard square image",
    aspectRatio: "1/1",
    style: { width: 300 },
  },
  render: (args) => <Image.Standard {...args} />,
};

export const Contained: Story = {
  args: {
    src: "https://picsum.photos/seed/contained/300/500",
    alt: "A tall image that is contained",
    aspectRatio: "9/16",
    backgroundColor: "#f0f0f0",
    style: { width: 300 },
  },
  render: (args) => <Image.Contained {...args} />,
};

export const Masonry: Story = {
  args: {
    src: "https://picsum.photos/seed/masonry/600/400",
    alt: "A wide image for masonry layout",
    aspectRatio: "9/16",
    backgroundColor: "#f0f0f0",
    style: { width: 300 },
  },
  render: (args) => <Image.Masonry {...args} />,
};

export const WithOverlays: Story = {
  args: {
    ...Standard.args,
    src: "https://picsum.photos/seed/overlays/400/400",
  },
  render: (args) => (
    <Image.Standard {...args}>
      <div
        style={{
          position: "absolute",
          top: "12px",
          left: "12px",
          backgroundColor: "#E53E3E",
          color: "white",
          padding: "4px 8px",
          borderRadius: "4px",
          fontSize: "12px",
          fontWeight: "bold",
        }}
      >
        SALE
      </div>
      <div
        style={{
          position: "absolute",
          bottom: "12px",
          right: "12px",
          backgroundColor: "rgba(0,0,0,0.5)",
          color: "white",
          padding: "8px",
          borderRadius: "50%",
          cursor: "pointer",
        }}
      >
        ❤️
      </div>
    </Image.Standard>
  ),
};

export const ErrorState: Story = {
  args: {
    src: "/this/path/does/not/exist.jpg",
    alt: "An image that will fail to load",
    aspectRatio: "1/1",
    style: { width: 300 },
  },
  render: (args) => <Image.Standard {...args} />,
};

export const CustomFallback: Story = {
  args: {
    ...ErrorState.args,
    fallback: (
      <div
        style={{
          padding: "16px",
          fontSize: "14px",
          color: "#718096",
          textAlign: "center",
        }}
      >
        이미지를
        <br />
        불러올 수 없습니다.
      </div>
    ),
  },
  render: (args) => <Image.Standard {...args} />,
};
