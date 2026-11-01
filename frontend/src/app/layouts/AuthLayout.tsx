import { Outlet, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { Lock, User as UserIcon } from "lucide-react";

interface AuthLayoutProps {
  title: string;
  subtitle: string;
  action: string;
  actionHref: string;
  actionLabel: string;
}

export default function AuthLayout({
  title,
  subtitle,
  action,
  actionHref,
  actionLabel,
}: AuthLayoutProps) {
  const navigate = useNavigate();

  return (
    <div className="min-h-[calc(100vh-12rem)] flex items-center justify-center bg-indigo-900 py-8 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl">
          <div className="text-center mb-8">
            <div className="w-12 h-12 rounded-lg bg-amber-500 flex items-center justify-center mx-auto mb-4 text-indigo-900 font-bold">
              {action === "Sign in" ? <Lock className="w-6 h-6" /> : <UserIcon className="w-6 h-6" />}
            </div>
            <h1 className="text-2xl font-display font-bold text-white">{title}</h1>
            <p className="text-amber-200 mt-2">{subtitle}</p>
          </div>

          <Outlet context={navigate} />

          <div className="mt-8 text-center text-amber-200 text-sm">
            {actionLabel} <Link to={actionHref} className="text-white font-medium hover:underline">{action}</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
