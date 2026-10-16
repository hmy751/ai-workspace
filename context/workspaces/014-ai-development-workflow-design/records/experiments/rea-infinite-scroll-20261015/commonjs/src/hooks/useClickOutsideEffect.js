"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const useClickOutsideEffect = (elements, handler) => {
    (0, react_1.useEffect)(() => {
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
exports.default = useClickOutsideEffect;
//# sourceMappingURL=useClickOutsideEffect.js.map