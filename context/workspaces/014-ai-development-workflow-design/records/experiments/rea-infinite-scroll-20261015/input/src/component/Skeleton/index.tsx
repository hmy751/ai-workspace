import React, { forwardRef } from "react";
import clsx from "clsx";
import styles from "./index.module.css";

export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  shape?: "rect" | "circle";
  width?: string | number;
  height?: string | number;
  aspectRatio?: string;
}

const Skeleton = forwardRef<HTMLDivElement, SkeletonProps>(
  (
    { shape = "rect", width, height, aspectRatio, className, ...restProps },
    ref
  ) => {
    const style = {
      width,
      height,
      aspectRatio,
    };

    return (
      <div
        ref={ref}
        className={clsx(styles.skeleton, styles[shape], className)}
        style={style}
        {...restProps}
      />
    );
  }
);

export default Skeleton;
