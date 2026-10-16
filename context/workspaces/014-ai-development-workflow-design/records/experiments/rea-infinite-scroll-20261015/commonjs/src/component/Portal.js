"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const react_dom_1 = require("react-dom");
const Portal = ({ children, selector = "portal-root" }) => {
    const [element, setElement] = (0, react_1.useState)(null);
    (0, react_1.useLayoutEffect)(() => {
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
    return (0, react_dom_1.createPortal)(children, element);
};
exports.default = Portal;
//# sourceMappingURL=Portal.js.map