import { HTMLAttributes, ReactNode } from "react";
import styles from "./index.module.css";
import Text, { TextProps } from "../../Text";
import clsx from "clsx";

export interface RootProps {
  children: ReactNode;
  ariaLabelledby: string;
}

const Root = ({ ariaLabelledby, children }: RootProps) => {
  return (
    <div className={styles.root} aria-labelledby={ariaLabelledby}>
      {children}
    </div>
  );
};

Root.displayName = "Field.Root";

export interface TitleProps extends Omit<TextProps, "id"> {
  id: string;
  hidden?: boolean;
}

const Title = ({ id, hidden = false, children }: TitleProps) => {
  return (
    <Text
      id={id}
      size="sm"
      weight="bold"
      className={clsx(hidden && "visually-hidden")}
    >
      {children}
    </Text>
  );
};

Title.displayName = "Field.Title";

export interface ElementsBoxProps {
  elementsHeight?: string;
  children: ReactNode;
}

const ElementsBox = ({
  elementsHeight = "var(--space-10)",
  children,
}: ElementsBoxProps) => {
  return (
    <div className={styles.elementsBox} style={{ height: elementsHeight }}>
      {children}
    </div>
  );
};

ElementsBox.displayName = "Field.ElementsBox";

export interface LabelProps extends HTMLAttributes<HTMLLabelElement> {
  maxWidth?: string;
  children: ReactNode;
}

const Label = ({ children, ...restProps }: LabelProps) => {
  return (
    <label className={styles.label} {...restProps}>
      {children}
    </label>
  );
};

Label.displayName = "Field.Label";

export interface DescriptionProps {
  children: ReactNode;
}

const Description = ({ children }: DescriptionProps) => {
  return (
    <Text size="sm" weight="light">
      {children}
    </Text>
  );
};

Description.displayName = "Field.Description";

export interface MessageProps {
  children: ReactNode;
}

const Message = ({ children }: MessageProps) => {
  return (
    <Text size="sm" color="error">
      {children}
    </Text>
  );
};

Message.displayName = "Field.Message";

const Field = Object.assign(Root, {
  Title,
  ElementsBox,
  Label,
  Description,
  Message,
});

export default Field;
