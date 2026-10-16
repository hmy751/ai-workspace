"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useToastStore = void 0;
const zustand_1 = require("zustand");
const randomId = () => Math.random().toString(36).substring(2);
exports.useToastStore = (0, zustand_1.create)(set => ({
    toasts: [],
    addToast: (toast) => set(state => ({
        toasts: [...state.toasts, { ...toast, id: randomId() }],
    })),
    removeToast: (id) => set(state => ({
        toasts: state.toasts.filter(toast => toast.id !== id),
    })),
}));
exports.default = exports.useToastStore;
//# sourceMappingURL=useToastStore.js.map