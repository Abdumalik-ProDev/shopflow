import { Outlet } from "react-router-dom";
import type { PropsWithChildren } from "react";

export default function MainLayout({ children }: PropsWithChildren) {
  return (
    <div className="w-full">
      {children || <Outlet />}
    </div>
  );
}
