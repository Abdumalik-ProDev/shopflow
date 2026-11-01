import { cn } from "@/lib/utils";

export interface AvatarProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  className?: string;
  src: string;
  alt?: string;
}

export function Avatar({ className, ...props }: AvatarProps) {
  return <img className={cn("rounded-full h-10 w-10 object-cover", className)} {...props} />;
}
