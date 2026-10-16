import { ReactNode, useEffect } from "react";
import { createPortal } from "react-dom";
import styles from "./index.module.css";
import Text from "../Text";
import useToastStore, { ToastData } from "../../store/useToastStore";

export interface ToastProps {
  children?: ReactNode;
}

const Toast = ({ children }: ToastProps) => {
  const toasts = useToastStore((state) => state.toasts);

  return (
    <>
      {children}
      {createPortal(
        <div className={styles.viewport}>
          {toasts.map((toast) => (
            <ToastItem key={toast.id} {...toast} />
          ))}
        </div>,
        document.body
      )}
    </>
  );
};

const ToastItem = ({ id, title, description, duration = 5000 }: ToastData) => {
  const removeToast = useToastStore((state) => state.removeToast);

  useEffect(() => {
    const timer = setTimeout(() => removeToast(id), duration);
    return () => clearTimeout(timer);
  }, [duration, removeToast, id]);

  return (
    <div className={styles.root}>
      {title && (
        <Text size="md" weight="medium" className={styles.title}>
          {title}
        </Text>
      )}
      {description && (
        <Text size="sm" weight="normal">
          {description}
        </Text>
      )}
    </div>
  );
};

export default Toast;
