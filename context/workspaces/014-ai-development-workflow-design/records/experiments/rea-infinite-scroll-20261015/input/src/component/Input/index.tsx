import {
  forwardRef,
  useEffect,
  useRef,
  useCallback,
  InputHTMLAttributes,
  FocusEvent,
  RefObject,
  useState,
  TouchEvent,
  MouseEvent,
} from "react";
import clsx from "clsx";
import styles from "./index.module.css";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  placeholder?: string;
  isTouched?: boolean;
  onChangeTouch?: (isTouched: boolean) => void;
  isFocused?: boolean;
  onChangeFocus?: (isFocused: boolean) => void;
  isError?: string;
  isDisabled?: boolean;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      placeholder,
      isFocused: controlledFocus,
      onFocus,
      onChangeFocus,
      onBlur,
      isTouched: controlledTouch,
      onTouchStart,
      onMouseDown,
      onChangeTouch,
      isError,
      disabled,
      isDisabled,
      className,
      ...restProps
    }: InputProps,
    ref: React.Ref<HTMLInputElement>
  ): React.ReactElement => {
    // ref 처리
    const internalInputRef = useRef<HTMLInputElement>(null);

    const assignRef = useCallback(
      (element: HTMLInputElement) => {
        if (element) {
          (internalInputRef as RefObject<HTMLInputElement>).current = element;
        }

        if (typeof ref === "function") {
          ref(element);
        } else if (ref) {
          (ref as RefObject<HTMLInputElement>).current = element;
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
      e: TouchEvent<HTMLInputElement> | MouseEvent<HTMLInputElement>
    ) => {
      e.stopPropagation();

      // 내부 unControlled 상태 이벤트
      setUnControlledTouch(true);

      // 단순 boolean 상태 이벤트
      onChangeTouch?.(true);

      // 상위 useForm과 같은 controlled 상태 이벤트
      onTouchStart?.(e as TouchEvent<HTMLInputElement>);
      onMouseDown?.(e as MouseEvent<HTMLInputElement>);
    };

    // focus 이벤트
    const [unControlledFocus, setUncontrolledFocus] = useState<boolean>(false);
    const isControlledFocus = controlledFocus !== undefined;

    const isFocused = isControlledFocus ? controlledFocus : unControlledFocus;

    const handleFocus = useCallback(
      (e: FocusEvent<HTMLInputElement>) => {
        e.stopPropagation();

        setUncontrolledFocus(true);

        onChangeFocus?.(true);

        onFocus?.(e);
      },
      [onChangeFocus, onFocus]
    );

    // blur 이벤트
    const handleBlur = useCallback(
      (e: FocusEvent<HTMLInputElement>) => {
        e.stopPropagation();

        setUncontrolledFocus(false);

        onChangeFocus?.(false);

        onBlur?.(e);
      },
      [onChangeFocus, onBlur, isControlledFocus]
    );

    return (
      <input
        ref={assignRef}
        placeholder={placeholder}
        disabled={disabled}
        className={clsx(
          styles.input,
          isTouched && styles.isTouched,
          isFocused && styles.isFocused,
          isError && styles.isError,
          isError
            ? "global-focus-visible-error"
            : "global-focus-visible-default",
          disabled && styles.isDisabled,
          className
        )}
        onMouseDown={handleTouch}
        onTouchStart={handleTouch}
        onFocus={handleFocus}
        onBlur={handleBlur}
        {...restProps}
      />
    );
  }
);

Input.displayName = "Input";

export default Input;
