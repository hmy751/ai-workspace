import {
  useState,
  useEffect,
  CSSProperties,
  ReactNode,
  forwardRef,
  useCallback,
  useRef,
  RefObject,
} from "react";
import clsx from "clsx";
import styles from "./index.module.css";
import Skeleton from "../Skeleton";

const DefaultFallbackIcon = () => (
  <svg className={styles.fallbackIcon} viewBox="0 0 24 24" fill="currentColor">
    <path d="M21.9,4.1c-0.4-0.4-1-0.4-1.4,0L12,12.6L3.5,4.1c-0.4-0.4-1-0.4-1.4,0s-0.4,1,0,1.4L10.6,14L2.1,22.5c-0.4,0.4-0.4,1,0,1.4 C2.3,24,2.6,24,2.8,24s0.5-0.1,0.7-0.3L12,15.4l8.5,8.5c0.2,0.2,0.5,0.3,0.7,0.3s0.5-0.1,0.7-0.3c0.4-0.4,0.4-1,0-1.4L13.4,14 l8.5-8.5C22.3,5.1,22.3,4.5,21.9,4.1z" />
  </svg>
);

// --- Prop Types ---
type ImageStatus = "loading" | "success" | "error";

interface BaseImageProps {
  src: string;
  alt: string;
  aspectRatio?: string;
  backgroundColor?: string;
  fallback?: ReactNode;
  children?: ReactNode;
  className?: string;
  style?: CSSProperties;
}

interface InternalImageProps extends BaseImageProps {
  sizing?: "ratio" | "natural";
  objectFit?: "cover" | "contain";
}

// --- Base Component ---
const Base = forwardRef<HTMLDivElement, InternalImageProps>(
  (
    {
      src,
      alt,
      aspectRatio = "1/1",
      backgroundColor = "transparent",
      fallback = <DefaultFallbackIcon />,
      children,
      className,
      style,
      sizing = "ratio",
      objectFit = "cover",
    },
    ref
  ) => {
    const [status, setStatus] = useState<ImageStatus>("loading");

    const isLoading = status === "loading";
    const isError = status === "error";

    useEffect(() => {
      if (!src) {
        setStatus("error");
        return;
      }

      setStatus("loading");
    }, [src]);

    const isMasonry = sizing === "natural";

    const handleLoad = useCallback(() => setStatus("success"), []);
    const handleError = useCallback(() => setStatus("error"), []);

    const containerStyle: CSSProperties = {
      ...style,
      aspectRatio: !isMasonry ? aspectRatio.replace("/", " / ") : undefined,
      backgroundColor,
    };

    return (
      <div
        ref={ref}
        className={clsx(
          styles.container,
          isMasonry && styles.masonryContainer,
          className
        )}
        style={containerStyle}
      >
        {isLoading && (
          <Skeleton className={styles.placeholder} aspectRatio={aspectRatio} />
        )}
        {isError && <div className={styles.fallbackWrapper}>{fallback}</div>}

        <img
          src={src}
          alt={alt}
          className={clsx(styles.image, isMasonry && styles.masonryImage)}
          style={{ objectFit }}
          onLoad={handleLoad}
          onError={handleError}
          data-status={status}
        />

        {!isLoading && !isError && children && (
          <div className={styles.overlay}>{children}</div>
        )}
      </div>
    );
  }
);
Base.displayName = "Image.Base";

// --- Standard Components ---
const Standard = forwardRef<HTMLDivElement, BaseImageProps>((props, ref) => (
  <Base ref={ref} {...props} sizing="ratio" objectFit="cover" />
));

Standard.displayName = "Image.Standard";

// --- Contained Components ---
const Contained = forwardRef<HTMLDivElement, BaseImageProps>((props, ref) => (
  <Base ref={ref} {...props} sizing="ratio" objectFit="contain" />
));

Contained.displayName = "Image.Contained";

// --- Masonry Components ---
const Masonry = forwardRef<HTMLDivElement, Omit<BaseImageProps, "aspectRatio">>(
  (props, ref) => <Base ref={ref} {...props} sizing="natural" />
);

Masonry.displayName = "Image.Masonry";

// --- Component Composition ---
const Image = Object.assign(Standard, {
  Standard,
  Contained,
  Masonry,
  Base,
});

export default Image;
