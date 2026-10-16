import { useEffect } from "react";
const useClickOutsideEffect = (elements, handler) => {
    useEffect(() => {
        if (!elements?.length) {
            return;
        }
        const listener = (e) => {
            for (const elOrRef of elements) {
                if (!elOrRef) {
                    return;
                }
                const element = 'current' in elOrRef ? elOrRef.current : elOrRef;
                if (!element || element.contains(e.target)) {
                    return;
                }
            }
            handler();
        };
        document.addEventListener("mousedown", listener);
        document.addEventListener("touchstart", listener);
        return () => {
            document.removeEventListener("mousedown", listener);
            document.removeEventListener("touchstart", listener);
        };
    }, [elements, handler]);
};
export default useClickOutsideEffect;
//# sourceMappingURL=useClickOutsideEffect.js.map