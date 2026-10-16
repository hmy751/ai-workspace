import { useLayoutEffect, useState } from "react";
import { createPortal } from "react-dom";
const Portal = ({ children, selector = "portal-root" }) => {
    const [element, setElement] = useState(null);
    useLayoutEffect(() => {
        let portalRoot = document.getElementById(selector);
        if (!portalRoot) {
            portalRoot = document.createElement("div");
            portalRoot.id = selector;
            document.body.appendChild(portalRoot);
        }
        setElement(portalRoot);
    }, [selector]);
    if (!element) {
        return null;
    }
    return createPortal(children, element);
};
export default Portal;
//# sourceMappingURL=Portal.js.map