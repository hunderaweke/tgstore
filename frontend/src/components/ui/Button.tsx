import React from "react";
import { cn } from "../../lib/cn";

type Variant = "primary" | "secondary" | "ghost" | "danger";
type Size = "sm" | "md";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
}

const variantStyles: Record<Variant, string> = {
  primary: "bg-gray-800 text-paper hover:bg-gray-600 active:bg-gray-900",
  secondary: "bg-forest text-paper hover:bg-forest/90 active:bg-forest/80",
  ghost: "bg-transparent text-gray-800 border border-gray-800 hover:bg-gray-300 active:bg-gray-400",
  danger: "bg-red-700 text-paper hover:bg-red-800 active:bg-red-900",
};

const sizeStyles: Record<Size, string> = {
  sm: "h-9 sm:h-10 px-3.5 sm:px-5 text-xs sm:text-sm md:text-base gap-1.5 shrink-0 ",
  md: "h-11 sm:h-12 px-5 sm:px-7 text-sm sm:text-base md:text-lg gap-2 ",
};

export function Button({
  variant = "primary",
  size = "md",
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center font-medium transition-all disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-none cursor-pointer select-none",
        variantStyles[variant],
        sizeStyles[size],
        className,
      )}
      {...props}
    />
  );
}
