"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useConfirmDialogStore = void 0;
const zustand_1 = require("zustand");
exports.useConfirmDialogStore = (0, zustand_1.create)(set => ({
    open: false,
    title: '',
    description: '',
    confirmCallback: () => { },
    setOpen: (open) => set({ open }),
    setConfirm: (title, description, confirmCallback) => {
        set({ open: true, title, description, confirmCallback });
    },
    clearConfirm: () => set({
        open: false,
        title: '',
        description: '',
        confirmCallback: () => { },
    }),
}));
exports.default = exports.useConfirmDialogStore;
//# sourceMappingURL=useConfirmDialogStore.js.map