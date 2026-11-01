import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "secondary" | "destructive" | "outline";
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variants = {
    default: "bg-indigo-900 text-white",
    secondary: "bg-charcoal-800 text-white",
    destructive: "bg-red-600 text-white",
    outline: "border border-charcoal-300 text-charcoal-900",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold leading-none transition-colors",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}
