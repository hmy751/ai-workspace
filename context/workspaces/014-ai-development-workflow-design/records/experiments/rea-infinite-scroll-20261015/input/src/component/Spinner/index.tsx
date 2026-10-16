import styles from "./index.module.css";

export interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  color?: string;
  className?: string;
}

const Spinner = ({
  size = "md",
  color = "var(--color-primary)",
  className,
}: SpinnerProps) => {
  return (
    <div
      className={`
        ${styles.spinner}
        ${styles[size]}
        ${className || ""}
      `}
      style={{ borderTopColor: color }}
      role="status"
      aria-label="loading"
    />
  );
};

export default Spinner;
