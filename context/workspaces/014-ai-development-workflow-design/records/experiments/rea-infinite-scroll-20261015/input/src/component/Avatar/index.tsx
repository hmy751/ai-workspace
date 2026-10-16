import React from "react";
import styles from "./index.module.css";

type AvatarSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface AvatarProps {
  src?: string;
  size?: AvatarSize;
  alt?: string;
  className?: string;
}

const sizeMap = {
  xs: 24,
  sm: 32,
  md: 40,
  lg: 48,
  xl: 160,
};

const Avatar = ({
  src,
  size = "md",
  alt = "avatar",
  className,
  ...props
}: AvatarProps) => {
  const containerClasses = [
    styles.container,
    styles[`size-${size}`],
    className || "",
  ]
    .filter(Boolean)
    .join(" ");

  const imageSrc = src || "/assets/images/default-avatar.svg";

  return (
    <div className={containerClasses} {...props}>
      <img
        src={imageSrc}
        alt={alt}
        width={sizeMap[size]}
        height={sizeMap[size]}
        className={styles.image}
        loading="lazy"
      />
    </div>
  );
};

export default Avatar;
