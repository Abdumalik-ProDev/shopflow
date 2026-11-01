import { cn } from "@/lib/utils";

export interface ToasterProps {
  className?: string;
}
export function Toaster({ className }: ToasterProps) {
  return (
    <div
      className={cn(
        "fixed top-0 z-[100] flex max-w-[400px] flex-col-reverse gap-4 p-6 sm:top-6 sm:right-0",
        className
      )}
    />
  );
}
