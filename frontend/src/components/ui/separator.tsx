import { cn } from "@/lib/utils";

export interface SeparatorProps extends React.HTMLAttributes<HTMLHRElement> {}
export function Separator({ className, ...props }: SeparatorProps) {
  return (
    <hr
      className={cn("mx-auto border-charcoal-200", className)}
      {...props}
    />
  );
}
