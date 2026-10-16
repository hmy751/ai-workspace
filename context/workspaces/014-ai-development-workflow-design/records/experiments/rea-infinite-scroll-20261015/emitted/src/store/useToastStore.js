import { create } from 'zustand';
const randomId = () => Math.random().toString(36).substring(2);
export const useToastStore = create(set => ({
    toasts: [],
    addToast: (toast) => set(state => ({
        toasts: [...state.toasts, { ...toast, id: randomId() }],
    })),
    removeToast: (id) => set(state => ({
        toasts: state.toasts.filter(toast => toast.id !== id),
    })),
}));
export default useToastStore;
//# sourceMappingURL=useToastStore.js.map