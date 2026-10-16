import {
  createContext,
  forwardRef,
  ReactNode,
  useContext,
  useMemo,
  useRef,
  useState,
  ButtonHTMLAttributes,
  HTMLAttributes,
  KeyboardEvent,
  Dispatch,
  SetStateAction,
  MouseEvent,
  CSSProperties,
  useCallback,
} from "react";
import clsx from "clsx";
import styles from "./index.module.css";
import useClickOutsideEffect from "../../hooks/useClickOutsideEffect";
import useFloatingPosition from "../../hooks/useFloatingPosition";
import Portal from "../Portal";

// --- Context Definition ---
interface DropdownContextType {
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
  selectedValue?: string | number;
  onChangeValue: (value: string | number) => void;
  setTriggerElement: Dispatch<SetStateAction<HTMLButtonElement | null>>;
  setMenuElement: Dispatch<SetStateAction<HTMLUListElement | null>>;
  positionStyles: CSSProperties;
}

const DropdownContext = createContext<DropdownContextType>(
  {} as DropdownContextType
);

// --- Root Component ---
export interface RootProps {
  children: ReactNode;
  value: string | number;
  onChange: (newValue: string | number) => void;
}

const Root = ({ children, value, onChange }: RootProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);

  const [triggerElement, setTriggerElement] =
    useState<HTMLButtonElement | null>(null);
  const [menuElement, setMenuElement] = useState<HTMLUListElement | null>(null);

  const positionStyles = useFloatingPosition(
    triggerElement,
    menuElement,
    isOpen
  );

  useClickOutsideEffect([menuElement, rootRef.current], () => setIsOpen(false));

  const onChangeValue = useCallback(
    (newValue: string | number) => {
      onChange?.(newValue);
      setIsOpen(false);
    },
    [onChange, setIsOpen]
  );

  const contextValue = useMemo(
    () => ({
      isOpen,
      setIsOpen,
      selectedValue: value,
      onChangeValue,
      setTriggerElement,
      setMenuElement,
      positionStyles,
      rootRef,
    }),
    [isOpen, value, onChange, positionStyles, rootRef, menuElement]
  );

  return (
    <DropdownContext.Provider value={contextValue}>
      <div ref={rootRef} className={styles.root}>
        {children}
      </div>
    </DropdownContext.Provider>
  );
};

Root.displayName = "Dropdown.Root";

// --- Trigger Component ---
export interface TriggerProps extends ButtonHTMLAttributes<HTMLButtonElement> {}

const Trigger = forwardRef<HTMLButtonElement, TriggerProps>(
  ({ children, className, ...restProps }, ref) => {
    const { isOpen, setIsOpen, setTriggerElement } =
      useContext(DropdownContext);

    const combinedRef = (element: HTMLButtonElement | null) => {
      setTriggerElement(element);

      if (typeof ref === "function") {
        ref(element);
      } else if (ref) {
        ref.current = element;
      }
    };

    return (
      <button
        ref={combinedRef}
        type="button"
        className={clsx(
          styles.trigger,
          "global-focus-visible-default",
          className
        )}
        onClick={() => setIsOpen((prev) => !prev)}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        {...restProps}
      >
        <span className={styles.triggerValue}>{children}</span>
        <span className={clsx(styles.arrow, isOpen && styles.arrowOpen)}>
          ▼
        </span>
      </button>
    );
  }
);

Trigger.displayName = "Dropdown.Trigger";

// --- Menu Component ---
export interface MenuProps {
  children: ReactNode;
  className?: string;
}

const Menu = ({ children, className }: MenuProps) => {
  const { isOpen, setMenuElement, positionStyles } =
    useContext(DropdownContext);

  return (
    <>
      {isOpen && (
        <Portal>
          <ul
            ref={setMenuElement}
            className={clsx(styles.menu, className)}
            role="listbox"
            style={positionStyles}
          >
            {children}
          </ul>
        </Portal>
      )}
    </>
  );
};

Menu.displayName = "Dropdown.Menu";

// --- Item Component ---
export interface ItemProps
  extends Omit<HTMLAttributes<HTMLLIElement>, "value"> {
  children: ReactNode;
  value: string | number;
}

const Item = ({ children, value, className, ...restProps }: ItemProps) => {
  const { selectedValue, onChangeValue } = useContext(DropdownContext);
  const isSelected = selectedValue === value;

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLLIElement>) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        e.stopPropagation();

        onChangeValue?.(value);
      }
    },
    [value, onChangeValue]
  );

  const handleChange = useCallback(
    (e: MouseEvent<HTMLLIElement>) => {
      e.stopPropagation();

      onChangeValue?.(value);
    },
    [value, onChangeValue]
  );

  return (
    <li
      role="option"
      aria-selected={isSelected}
      tabIndex={0}
      onClick={handleChange}
      onKeyDown={handleKeyDown}
      className={clsx(styles.item, isSelected && styles.selected, className)}
      {...restProps}
    >
      {children}
    </li>
  );
};

Item.displayName = "Dropdown.Item";

// --- Component Composition ---
const Dropdown = Object.assign(Root, {
  Trigger,
  Menu,
  Item,
});

export default Dropdown;
