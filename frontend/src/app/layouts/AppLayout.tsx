import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "@/app/providers/AuthProvider";
import { Link } from "react-router-dom";
import { ShoppingCart, LogOut } from "lucide-react";

export default function AppLayout() {
  const { logout, isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen flex flex-col bg-cream-50">
      <header className="bg-indigo-900 text-white sticky top-0 z-50 border-b border-white/10">
        <div className="container flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex items-center gap-2 font-display text-xl font-bold tracking-tight">
            <div className="w-8 h-8 rounded bg-amber-500 flex items-center justify-center text-indigo-900 font-bold">
              S
            </div>
            <span>ShopFlow</span>
          </Link>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
            <Link to="/" className="hover:text-amber-400 transition">Home</Link>
            <Link to="/catalog" className="hover:text-amber-400 transition">Catalog</Link>
            <Link to="/cart" className="hover:text-amber-400 transition">
              Cart <span className="bg-amber-500 text-indigo-900 text-xs px-2 py-0.5 rounded-full">0</span>
            </Link>
          </nav>

          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 hover:text-amber-400 transition text-sm"
                >
                  <LogOut className="w-4 h-4" /> Sign out
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-sm hover:text-amber-400 transition">
                  Sign in
                </Link>
                <Link
                  to="/register"
                  className="text-sm px-4 py-2 rounded bg-amber-500 text-indigo-900 font-medium hover:bg-amber-400 transition"
                >
                  Get started
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      <main className="flex-1">{<Outlet />}</main>

      <footer className="bg-charcoal-900 text-charcoal-200 border-t border-white/10 py-12">
        <div className="container px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm">ShopFlow — E-Commerce Marketplace with Integrated ML</p>
        </div>
      </footer>
    </div>
  );
}
