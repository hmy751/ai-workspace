"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.CustomFallback = exports.ErrorState = exports.WithOverlays = exports.Masonry = exports.Contained = exports.Standard = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const index_1 = __importDefault(require("./index"));
const meta = {
    title: "Common/Image",
    component: index_1.default,
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
exports.default = meta;
exports.Standard = {
    args: {
        src: "https://picsum.photos/seed/standard/400/400",
        alt: "A standard square image",
        aspectRatio: "1/1",
        style: { width: 300 },
    },
    render: (args) => (0, jsx_runtime_1.jsx)(index_1.default.Standard, { ...args }),
};
exports.Contained = {
    args: {
        src: "https://picsum.photos/seed/contained/300/500",
        alt: "A tall image that is contained",
        aspectRatio: "9/16",
        backgroundColor: "#f0f0f0",
        style: { width: 300 },
    },
    render: (args) => (0, jsx_runtime_1.jsx)(index_1.default.Contained, { ...args }),
};
exports.Masonry = {
    args: {
        src: "https://picsum.photos/seed/masonry/600/400",
        alt: "A wide image for masonry layout",
        aspectRatio: "9/16",
        backgroundColor: "#f0f0f0",
        style: { width: 300 },
    },
    render: (args) => (0, jsx_runtime_1.jsx)(index_1.default.Masonry, { ...args }),
};
exports.WithOverlays = {
    args: {
        ...exports.Standard.args,
        src: "https://picsum.photos/seed/overlays/400/400",
    },
    render: (args) => ((0, jsx_runtime_1.jsxs)(index_1.default.Standard, { ...args, children: [(0, jsx_runtime_1.jsx)("div", { style: {
                    position: "absolute",
                    top: "12px",
                    left: "12px",
                    backgroundColor: "#E53E3E",
                    color: "white",
                    padding: "4px 8px",
                    borderRadius: "4px",
                    fontSize: "12px",
                    fontWeight: "bold",
                }, children: "SALE" }), (0, jsx_runtime_1.jsx)("div", { style: {
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
exports.ErrorState = {
    args: {
        src: "/this/path/does/not/exist.jpg",
        alt: "An image that will fail to load",
        aspectRatio: "1/1",
        style: { width: 300 },
    },
    render: (args) => (0, jsx_runtime_1.jsx)(index_1.default.Standard, { ...args }),
};
exports.CustomFallback = {
    args: {
        ...exports.ErrorState.args,
        fallback: ((0, jsx_runtime_1.jsxs)("div", { style: {
                padding: "16px",
                fontSize: "14px",
                color: "#718096",
                textAlign: "center",
            }, children: ["\uC774\uBBF8\uC9C0\uB97C", (0, jsx_runtime_1.jsx)("br", {}), "\uBD88\uB7EC\uC62C \uC218 \uC5C6\uC2B5\uB2C8\uB2E4."] })),
    },
    render: (args) => (0, jsx_runtime_1.jsx)(index_1.default.Standard, { ...args }),
};
//# sourceMappingURL=index.stories.js.map