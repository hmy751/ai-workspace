import { forwardRef, InputHTMLAttributes, ReactNode, ChangeEvent } from "react";
import clsx from "clsx";
import styles from "./index.module.css";

const CheckmarkIcon = () => (
  <svg
    className={styles.checkmarkIcon}
    viewBox="0 0 12 9"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M10.6667 1.16663L4.25002 7.24996L1.33335 4.33329"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export interface CheckboxProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  children?: ReactNode;
  value?: string | number;
  className?: string;
}

const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  (
    { id, onChange, children, disabled, className, value, ...restProps },
    ref
  ) => {
    return (
      <label
        htmlFor={id}
        className={clsx(styles.wrapper, className, disabled && styles.disabled)}
      >
        <input
          id={id}
          type="checkbox"
          ref={ref}
          className={clsx("visually-hidden")}
          onChange={onChange}
          disabled={disabled}
          value={value}
          {...restProps}
        />
        <span
          className={clsx(
            styles.customCheckbox,
            "global-focus-visible-default"
          )}
          aria-hidden="true"
        >
          <CheckmarkIcon />
        </span>
        <span className={styles.labelText}>{children}</span>
      </label>
    );
  }
);

Checkbox.displayName = "Checkbox";

export default Checkbox;
