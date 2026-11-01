import { Outlet } from "react-router-dom";
import type { PropsWithChildren } from "react";

export default function MainLayout({ children }: PropsWithChildren) {
  return (
    <div className="container py-8">
      {children}
    </div>
  );
}
