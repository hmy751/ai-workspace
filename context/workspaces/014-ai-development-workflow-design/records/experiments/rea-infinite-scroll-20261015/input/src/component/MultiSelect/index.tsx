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
  useEffect,
  Dispatch,
  SetStateAction,
  KeyboardEvent,
  CSSProperties,
  useCallback,
} from "react";
import clsx from "clsx";
import styles from "./index.module.css";
import useClickOutsideEffect from "../../hooks/useClickOutsideEffect";
import useFloatingPosition from "../../hooks/useFloatingPosition";
import Portal from "../Portal";

// --- Types and Context ---
export interface Option {
  value: string;
  label: ReactNode;
}

export interface MultiSelectContextType {
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
  selectedValues: string[];
  handleItemSelect: (value: string) => void;
  triggerElement: HTMLButtonElement | null;
  setTriggerElement: Dispatch<SetStateAction<HTMLButtonElement | null>>;
  menuElement: HTMLUListElement | null;
  setMenuElement: Dispatch<SetStateAction<HTMLUListElement | null>>;
  options: Option[];
  positionStyles: CSSProperties;
}

const MultiSelectContext = createContext<MultiSelectContextType>(
  {} as MultiSelectContextType
);

// --- Root ---
export interface RootProps {
  children: ReactNode;
  options: Option[];
  value: string[];
  onChange: (newValue: string[]) => void;
}

const Root = ({ children, options, value, onChange }: RootProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [triggerElement, setTriggerElement] =
    useState<HTMLButtonElement | null>(null);
  const [menuElement, setMenuElement] = useState<HTMLUListElement | null>(null);

  const handleItemSelect = useCallback(
    (itemValue: string) => {
      const newValues = value.includes(itemValue)
        ? value.filter((v) => v !== itemValue)
        : [...value, itemValue];

      onChange(newValues);
    },
    [value, onChange]
  );

  useClickOutsideEffect([triggerElement, menuElement], () => {
    setIsOpen(false);
  });

  const positionStyles = useFloatingPosition(
    triggerElement,
    menuElement,
    isOpen
  );

  const contextValue = useMemo(
    () => ({
      isOpen,
      setIsOpen,
      selectedValues: value,
      handleItemSelect,
      triggerElement,
      setTriggerElement,
      menuElement,
      setMenuElement,
      positionStyles,
      options,
    }),
    [
      isOpen,
      value,
      onChange,
      triggerElement,
      menuElement,
      positionStyles,
      options,
    ]
  );

  return (
    <MultiSelectContext.Provider value={contextValue}>
      <div className={styles.root}>{children}</div>
    </MultiSelectContext.Provider>
  );
};

Root.displayName = "MultiSelect.Root";

// --- Trigger ---
export interface TriggerProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "children"> {
  placeholder?: string;
  isError?: boolean;
}

const Trigger = forwardRef<HTMLButtonElement, TriggerProps>(
  ({ className, placeholder, disabled, isError, ...restProps }, ref) => {
    const {
      isOpen,
      setIsOpen,
      setTriggerElement,
      selectedValues,
      options,
      handleItemSelect,
    } = useContext(MultiSelectContext);

    const handleRef = (element: HTMLButtonElement | null) => {
      setTriggerElement(element);
      if (typeof ref === "function") ref(element);
      else if (ref) ref.current = element;
    };

    const optionsMap = useMemo(
      () => new Map(options.map((opt) => [opt.value, opt.label])),
      [options]
    );

    return (
      <button
        ref={handleRef}
        type="button"
        className={clsx(styles.trigger, isError && styles.isError, className)}
        onClick={() => setIsOpen((prev) => !prev)}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        disabled={disabled}
        {...restProps}
      >
        <div className={styles.triggerValueWrapper}>
          {selectedValues.length === 0 ? (
            <span className={styles.placeholder}>
              {placeholder || "선택..."}
            </span>
          ) : (
            selectedValues.map((value) => (
              <span
                key={value}
                className={styles.tag}
                onClick={(e) => e.stopPropagation()}
              >
                {optionsMap.get(value) || value}
                <span
                  className={styles.tagRemoveButton}
                  onClick={() => handleItemSelect(value)}
                  aria-label={`${optionsMap.get(value)} 제거`}
                >
                  &times;
                </span>
              </span>
            ))
          )}
        </div>
        <span className={clsx(styles.arrow, isOpen && styles.arrowOpen)}>
          ▼
        </span>
      </button>
    );
  }
);

Trigger.displayName = "MultiSelect.Trigger";

// --- Menu ---
export interface MenuProps {
  children: ReactNode;
  className?: string;
}

const Menu = ({ children, className }: MenuProps) => {
  const { isOpen, positionStyles, setMenuElement } =
    useContext(MultiSelectContext);

  return (
    <>
      {isOpen && (
        <Portal>
          <ul
            ref={setMenuElement}
            className={clsx(styles.dropdown, className)}
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

Menu.displayName = "MultiSelect.Menu";

// --- Item ---
export interface ItemProps
  extends Omit<HTMLAttributes<HTMLLIElement>, "value"> {
  children: ReactNode;
  value: string;
}

const Item = ({ children, value, className, ...restProps }: ItemProps) => {
  const { selectedValues, handleItemSelect } = useContext(MultiSelectContext);
  const isSelected = selectedValues.includes(value);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLLIElement>) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        e.stopPropagation();

        handleItemSelect(value);
      }
    },
    [handleItemSelect]
  );

  return (
    <li
      className={clsx(styles.item, isSelected && styles.selected, className)}
      onClick={() => handleItemSelect(value)}
      role="option"
      aria-selected={isSelected}
      tabIndex={0}
      onKeyDown={handleKeyDown}
      {...restProps}
    >
      <span className={styles.itemCheckbox}>
        {isSelected && <span className={styles.itemCheckmark}>✓</span>}
      </span>
      <span>{children}</span>
    </li>
  );
};

Item.displayName = "MultiSelect.Item";

// --- Component Composition ---
const MultiSelect = Object.assign(Root, {
  Trigger,
  Menu,
  Item,
});

export default MultiSelect;
