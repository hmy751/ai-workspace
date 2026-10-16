import {
  createContext,
  forwardRef,
  SelectHTMLAttributes,
  useContext,
  ReactNode,
  OptionHTMLAttributes,
  useState,
  ChangeEvent,
  TouchEvent,
  MouseEvent,
  FocusEvent,
  useRef,
  useCallback,
  RefObject,
  useMemo,
} from "react";
import clsx from "clsx";
import styles from "./index.module.css";

interface SelectContextType {
  value?: string | number;
  onChangeValue?: (value: string) => void;
}

const SelectContext = createContext<SelectContextType>({} as SelectContextType);

export interface SelectRootProps
  extends Omit<SelectHTMLAttributes<HTMLSelectElement>, "size"> {
  value?: string | number;
  children: ReactNode;
  placeholder?: string;
  fullWidth?: boolean;
  size?: "sm" | "md" | "lg";
  isTouched?: boolean;
  onChangeTouch?: (isTouch: boolean) => void;
  isFocused?: boolean;
  onChangeFocus?: (isFocused: boolean) => void;
  onChangeValue?: (value: string) => void;
  isError?: string;
}

const Root = forwardRef<HTMLSelectElement, SelectRootProps>(
  (
    {
      value,
      children,
      placeholder,
      fullWidth,
      size,
      onChange,
      onChangeValue,
      isTouched: controlledTouch,
      onTouchStart,
      onMouseDown,
      onChangeTouch,
      isFocused: controlledFocus,
      onFocus,
      onChangeFocus,
      onBlur,
      isError,
      className,
      ...restProps
    }: SelectRootProps,
    ref
  ) => {
    // ref 처리
    const internalSelectRef = useRef<HTMLSelectElement>(null);

    const assignRef = useCallback(
      (element: HTMLSelectElement) => {
        if (element) {
          (internalSelectRef as RefObject<HTMLSelectElement>).current = element;
        }

        if (typeof ref === "function") {
          ref(element);
        } else if (ref) {
          (ref as RefObject<HTMLSelectElement>).current = element;
        }
      },
      [ref]
    );

    // isTouched와 같은 value는 control, unControl에 따라서 기준을 정하고,
    // 이벤트는 control, unControl 모두 실행하여 일관성을 유지한다.

    // touch 이벤트
    const [unControlledTouch, setUnControlledTouch] = useState<boolean>(false);
    const isControlledTouch = controlledTouch !== undefined;

    const isTouched = isControlledTouch ? controlledTouch : unControlledTouch;

    const handleTouch = (
      e: TouchEvent<HTMLSelectElement> | MouseEvent<HTMLSelectElement>
    ) => {
      e.stopPropagation();

      // 내부 unControlled 상태 이벤트
      setUnControlledTouch(true);

      // 단순 boolean 상태 이벤트
      onChangeTouch?.(true);

      // 상위 useForm과 같은 controlled 상태 이벤트
      onTouchStart?.(e as TouchEvent<HTMLSelectElement>);
      onMouseDown?.(e as MouseEvent<HTMLSelectElement>);
    };

    // focus 이벤트
    const [unControlledFocus, setUncontrolledFocus] = useState<boolean>(false);
    const isControlledFocus = controlledFocus !== undefined;

    const isFocused = isControlledFocus ? controlledFocus : unControlledFocus;

    const handleFocus = useCallback(
      (e: FocusEvent<HTMLSelectElement>) => {
        e.stopPropagation();

        onChangeFocus?.(true);

        setUncontrolledFocus(true);

        onFocus?.(e);
      },
      [onChangeFocus, onFocus]
    );

    // blur 이벤트
    const handleBlur = useCallback(
      (e: FocusEvent<HTMLSelectElement>) => {
        e.stopPropagation();

        setUncontrolledFocus(false);

        onChangeFocus?.(false);

        onBlur?.(e);
      },
      [onChangeFocus, onBlur, isControlledFocus]
    );

    // change 이벤트
    const handleChange = useCallback(
      (e: ChangeEvent<HTMLSelectElement>) => {
        e.stopPropagation();

        onChangeValue?.(e.target.value);

        onChange?.(e);
      },
      [onChange, onChangeValue]
    );

    const contextValue = useMemo(
      () => ({
        value,
        onChangeValue,
      }),
      [value, onChangeValue]
    );

    return (
      <SelectContext.Provider value={contextValue}>
        <select
          ref={assignRef}
          value={value}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onMouseDown={handleTouch}
          onTouchStart={handleTouch}
          className={clsx(
            styles.select,
            styles[`size-${size}`],
            fullWidth && styles.fullWidth,
            isTouched && styles.isTouched,
            isFocused && styles.isFocused,
            isError && styles.isError,
            isError
              ? "global-focus-visible-error"
              : "global-focus-visible-default",
            className
          )}
          {...restProps}
        >
          {placeholder && <option value="">{placeholder}</option>}
          {children}
        </select>
      </SelectContext.Provider>
    );
  }
);

Root.displayName = "Select.Root";

export interface SelectOptionProps
  extends OptionHTMLAttributes<HTMLOptionElement> {}

const Option = forwardRef<HTMLOptionElement, SelectOptionProps>(
  ({ children, ...restProps }: SelectOptionProps, ref) => {
    return (
      <option ref={ref} {...restProps}>
        {children}
      </option>
    );
  }
);

Option.displayName = "Select.Option";

const Select = Object.assign(Root, {
  Option,
});

Select.displayName = "Select";

export default Select;
