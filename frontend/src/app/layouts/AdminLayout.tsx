import { Outlet } from "react-router-dom";
import type { PropsWithChildren } from "react";

export default function AdminLayout({ children }: PropsWithChildren) {
  return (
    <div className="container py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-display font-bold text-charcoal-900">Administration</h1>
      </div>
      {children}
    </div>
  );
}
