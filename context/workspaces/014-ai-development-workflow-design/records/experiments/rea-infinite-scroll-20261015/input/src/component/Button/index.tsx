import Spinner from "../Spinner";
import styles from "./index.module.css";
import clsx from "clsx";

type ButtonVariant = "primary" | "secondary" | "outline" | "text";
type ButtonSize = "sm" | "md" | "lg";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  fullWidth?: boolean;
  isLoading?: boolean;
  children: React.ReactNode;
}

const Button = ({
  variant = "primary",
  size = "md",
  fullWidth = false,
  isLoading = false,
  children,
  disabled,
  className,
  ...restProps
}: ButtonProps) => {
  return (
    <button
      className={clsx(
        styles.button,
        styles[variant],
        styles[`size-${size}`],
        fullWidth && styles.fullWidth,
        isLoading && styles.loading,
        disabled && styles.disabled,
        className
      )}
      disabled={isLoading || disabled}
      {...restProps}
    >
      {isLoading ? (
        <div className={styles.loadingContainer}>
          <Spinner size={size} />
          {children}
        </div>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;
