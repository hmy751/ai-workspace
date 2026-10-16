import { ReactNode, useLayoutEffect, useState } from "react";
import { createPortal } from "react-dom";

interface PortalProps {
  children: ReactNode;
  selector?: string;
}

const Portal = ({ children, selector = "portal-root" }: PortalProps) => {
  const [element, setElement] = useState<HTMLElement | null>(null);

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
