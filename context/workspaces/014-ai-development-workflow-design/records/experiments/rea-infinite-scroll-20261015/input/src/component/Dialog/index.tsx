import React, {
  ReactNode,
  ReactElement,
  useMemo,
  useEffect,
  useState,
  createContext,
  useContext,
  forwardRef,
  HTMLAttributes,
  MouseEvent,
  ButtonHTMLAttributes,
} from "react";
import { createPortal } from "react-dom";
import styles from "./index.module.css";
import Text from "../Text";
import Button from "../Button";

interface DialogContextType {
  open: boolean;
  setOpen: (open: boolean) => void;
  controlled?: boolean;
}

const DialogContext = createContext<DialogContextType>({} as DialogContextType);

export interface DialogRootProps {
  children: ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

const Root = ({
  children,
  open: controlledOpen,
  onOpenChange,
}: DialogRootProps): ReactElement => {
  const [uncontrolledOpen, setUncontrolledOpen] = useState(false);
  const isControlled = controlledOpen !== undefined;

  const open = isControlled ? controlledOpen! : uncontrolledOpen;
  const setOpen = useMemo(() => {
    if (isControlled) {
      return onOpenChange || (() => {});
    }
    return setUncontrolledOpen;
  }, [isControlled, onOpenChange]);

  const contextValue = useMemo(
    () => ({
      open,
      setOpen,
      controlled: isControlled,
    }),
    [open, setOpen, isControlled]
  );

  return (
    <DialogContext.Provider value={contextValue}>
      {children}
    </DialogContext.Provider>
  );
};

Root.displayName = "Dialog.Root";

export interface TriggerProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

const Trigger = forwardRef<HTMLDivElement, TriggerProps>(
  ({ children, onClick, ...restProps }, ref) => {
    const { setOpen } = useContext(DialogContext);
    const handleClick = (e: MouseEvent<HTMLDivElement>) => {
      setOpen(true);
      onClick?.(e);
    };
    return (
      <div ref={ref} onClick={handleClick} {...restProps}>
        {children}
      </div>
    );
  }
);

Trigger.displayName = "Dialog.Trigger";

export interface ContentProps {
  children: ReactNode;
}

const Content = ({ children }: ContentProps): ReactElement | null => {
  const { open, setOpen } = useContext(DialogContext);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };

    if (open) {
      document.addEventListener("keydown", handleEscape);
    }
    return () => document.removeEventListener("keydown", handleEscape);
  }, [open, setOpen]);

  if (!open) return null;

  return createPortal(
    <>
      <div className={styles.overlay} onClick={() => setOpen(false)} />
      <div className={styles.content}>{children}</div>
    </>,
    document.body
  );
};

Content.displayName = "Dialog.Content";

export interface TitleProps {
  children: ReactNode;
}

const Title = ({ children }: TitleProps): ReactElement => {
  return <Text as="h2">{children}</Text>;
};

Title.displayName = "Dialog.Title";

export interface DescriptionProps {
  children: ReactNode;
}

const Description = ({ children }: DescriptionProps): ReactElement => {
  return <Text as="p">{children}</Text>;
};

Description.displayName = "Dialog.Description";

export interface FooterProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

const Footer = forwardRef<HTMLDivElement, FooterProps>(
  ({ children, ...restProps }, ref) => {
    return (
      <div ref={ref} className={styles.footer} {...restProps}>
        {children}
      </div>
    );
  }
);

Footer.displayName = "Dialog.Footer";

export interface ConfirmProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  callback: () => void;
  children: ReactNode;
}

const Confirm = ({
  callback,
  children,
  onClick,
  ...restProps
}: ConfirmProps): ReactElement => {
  const { setOpen } = useContext(DialogContext);
  const handleConfirm = (e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    callback?.();
    setOpen(false);
    onClick?.(e);
  };

  return (
    <Button
      variant="primary"
      fullWidth={true}
      onClick={handleConfirm}
      {...restProps}
    >
      {children}
    </Button>
  );
};

Confirm.displayName = "Dialog.Confirm";

export interface CancelProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  callback?: () => void;
  children: ReactNode;
}

const Cancel = ({
  callback,
  children,
  onClick,
  ...restProps
}: CancelProps): ReactElement => {
  const { setOpen } = useContext(DialogContext);
  const handleCancel = (e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    callback?.();
    setOpen(false);
    onClick?.(e);
  };

  return (
    <Button
      variant="outline"
      fullWidth={true}
      onClick={handleCancel}
      {...restProps}
    >
      {children}
    </Button>
  );
};

Cancel.displayName = "Dialog.Cancel";

const Dialog = Object.assign(Root, {
  Trigger,
  Content,
  Title,
  Description,
  Footer,
  Confirm,
  Cancel,
});

Dialog.displayName = "Dialog";

export default Dialog;
