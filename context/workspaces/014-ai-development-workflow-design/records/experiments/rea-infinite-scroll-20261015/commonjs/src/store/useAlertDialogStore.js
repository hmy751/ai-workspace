"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useAlertDialogStore = void 0;
const zustand_1 = require("zustand");
exports.useAlertDialogStore = (0, zustand_1.create)(set => ({
    open: false,
    title: '',
    description: '',
    setOpen: (open) => set({ open }),
    setAlert: (title, description) => {
        set({ open: true, title, description });
    },
    clearAlert: () => set({ open: false, title: '', description: '' }),
}));
exports.default = exports.useAlertDialogStore;
//# sourceMappingURL=useAlertDialogStore.js.map