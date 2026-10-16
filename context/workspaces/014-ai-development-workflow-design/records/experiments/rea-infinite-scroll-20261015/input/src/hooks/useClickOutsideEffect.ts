import { useEffect, RefObject } from "react";

const useClickOutsideEffect = (
  elements: Array<HTMLElement | RefObject<HTMLElement> | null>,
  handler: () => void
) => {
  useEffect(() => {
    if (!elements?.length) {
      return;
    }

    const listener = (e: MouseEvent | TouchEvent) => {

      for (const elOrRef of elements) {
        if (!elOrRef) {
          return;
        }

        const element = 'current' in elOrRef ? elOrRef.current : elOrRef;

        if (!element || element.contains(e.target as Node)) {
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
