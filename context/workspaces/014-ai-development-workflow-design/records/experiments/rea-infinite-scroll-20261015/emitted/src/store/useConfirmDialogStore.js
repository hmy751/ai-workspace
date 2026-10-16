import { create } from 'zustand';
export const useConfirmDialogStore = create(set => ({
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
export default useConfirmDialogStore;
//# sourceMappingURL=useConfirmDialogStore.js.map