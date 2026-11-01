import React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon";
  asChild?: boolean;
}

export function Button({ className, variant = "default", size = "default", asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? (React as any).Fragment : "button";
  const variants = {
    default: "bg-indigo-900 text-white hover:bg-indigo-800",
    destructive: "bg-red-600 text-white hover:bg-red-700",
    outline: "border border-charcoal-800 bg-white hover:bg-charcoal-50",
    secondary: "bg-charcoal-800 text-white hover:bg-charcoal-700",
    ghost: "hover:bg-charcoal-100",
    link: "text-indigo-900 underline-offset-4 hover:underline",
  };
  const sizes = {
    default: "h-10 px-4 py-2",
    sm: "h-9 rounded-md px-3",
    lg: "h-11 rounded-md px-8",
    icon: "h-10 w-10",
  };
  return (
    <Comp
      className={cn(
        "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-900 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    />
  );
}
