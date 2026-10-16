import { create } from 'zustand';
export const useAlertDialogStore = create(set => ({
    open: false,
    title: '',
    description: '',
    setOpen: (open) => set({ open }),
    setAlert: (title, description) => {
        set({ open: true, title, description });
    },
    clearAlert: () => set({ open: false, title: '', description: '' }),
}));
export default useAlertDialogStore;
//# sourceMappingURL=useAlertDialogStore.js.map