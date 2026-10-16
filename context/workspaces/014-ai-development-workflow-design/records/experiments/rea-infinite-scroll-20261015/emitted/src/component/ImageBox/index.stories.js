import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Image from "./index";
const meta = {
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
export const Standard = {
    args: {
        src: "https://picsum.photos/seed/standard/400/400",
        alt: "A standard square image",
        aspectRatio: "1/1",
        style: { width: 300 },
    },
    render: (args) => _jsx(Image.Standard, { ...args }),
};
export const Contained = {
    args: {
        src: "https://picsum.photos/seed/contained/300/500",
        alt: "A tall image that is contained",
        aspectRatio: "9/16",
        backgroundColor: "#f0f0f0",
        style: { width: 300 },
    },
    render: (args) => _jsx(Image.Contained, { ...args }),
};
export const Masonry = {
    args: {
        src: "https://picsum.photos/seed/masonry/600/400",
        alt: "A wide image for masonry layout",
        aspectRatio: "9/16",
        backgroundColor: "#f0f0f0",
        style: { width: 300 },
    },
    render: (args) => _jsx(Image.Masonry, { ...args }),
};
export const WithOverlays = {
    args: {
        ...Standard.args,
        src: "https://picsum.photos/seed/overlays/400/400",
    },
    render: (args) => (_jsxs(Image.Standard, { ...args, children: [_jsx("div", { style: {
                    position: "absolute",
                    top: "12px",
                    left: "12px",
                    backgroundColor: "#E53E3E",
                    color: "white",
                    padding: "4px 8px",
                    borderRadius: "4px",
                    fontSize: "12px",
                    fontWeight: "bold",
                }, children: "SALE" }), _jsx("div", { style: {
                    position: "absolute",
                    bottom: "12px",
                    right: "12px",
                    backgroundColor: "rgba(0,0,0,0.5)",
                    color: "white",
                    padding: "8px",
                    borderRadius: "50%",
                    cursor: "pointer",
                }, children: "\u2764\uFE0F" })] })),
};
export const ErrorState = {
    args: {
        src: "/this/path/does/not/exist.jpg",
        alt: "An image that will fail to load",
        aspectRatio: "1/1",
        style: { width: 300 },
    },
    render: (args) => _jsx(Image.Standard, { ...args }),
};
export const CustomFallback = {
    args: {
        ...ErrorState.args,
        fallback: (_jsxs("div", { style: {
                padding: "16px",
                fontSize: "14px",
                color: "#718096",
                textAlign: "center",
            }, children: ["\uC774\uBBF8\uC9C0\uB97C", _jsx("br", {}), "\uBD88\uB7EC\uC62C \uC218 \uC5C6\uC2B5\uB2C8\uB2E4."] })),
    },
    render: (args) => _jsx(Image.Standard, { ...args }),
};
//# sourceMappingURL=index.stories.js.map