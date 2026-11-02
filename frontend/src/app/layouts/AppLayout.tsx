import { Outlet, Link } from "react-router-dom";
import { useAuth } from "@/app/providers/AuthProvider";
import { useCart } from "@/stores/cart";
import { ShoppingCart, LogOut, User, BarChart3, Package } from "lucide-react";

export default function AppLayout() {
  const { user, logout, isAuthenticated } = useAuth();
  const { itemCount } = useCart();

  return (
    <div className="min-h-screen flex flex-col bg-cream-50">
      <header className="bg-indigo-900 text-white sticky top-0 z-50 border-b border-white/10 shadow-sm">
        <div className="container flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex items-center gap-2 font-display text-xl font-bold tracking-tight">
            <div className="w-8 h-8 rounded bg-amber-500 flex items-center justify-center text-indigo-900 font-bold">
              S
            </div>
            <span>ShopFlow</span>
          </Link>

          <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
            <Link to="/" className="hover:text-amber-400 transition">Home</Link>
            <Link to="/catalog" className="hover:text-amber-400 transition">Catalog</Link>
            <Link to="/recommendations" className="hover:text-amber-400 transition flex items-center gap-1.5">
              <span>Recommendations</span>
              <span className="text-[10px] bg-amber-400 text-indigo-950 font-semibold px-1.5 py-0.5 rounded">ML</span>
            </Link>
            <Link to="/orders" className="hover:text-amber-400 transition">Orders</Link>
            <Link to="/admin" className="hover:text-amber-400 transition">Analytics</Link>
          </nav>

          <div className="flex items-center gap-4">
            <Link
              to="/cart"
              className="flex items-center gap-2 hover:text-amber-400 transition text-sm bg-white/10 px-3 py-1.5 rounded-lg border border-white/15"
            >
              <ShoppingCart className="w-4 h-4" />
              <span>Cart</span>
              <span className="bg-amber-500 text-indigo-900 font-bold text-xs px-2 py-0.2 rounded-full">
                {itemCount}
              </span>
            </Link>

            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <Link
                  to="/account"
                  className="flex items-center gap-1.5 text-sm hover:text-amber-400 transition"
                >
                  <User className="w-4 h-4" />
                  <span className="hidden sm:inline">{user?.username || "Account"}</span>
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center gap-1.5 hover:text-amber-400 transition text-sm text-charcoal-300"
                  title="Sign out"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="hidden sm:inline">Sign out</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link to="/login" className="text-sm hover:text-amber-400 transition">
                  Sign in
                </Link>
                <Link
                  to="/register"
                  className="text-sm px-3.5 py-1.5 rounded-lg bg-amber-500 text-indigo-900 font-medium hover:bg-amber-400 transition"
                >
                  Get started
                </Link>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <Outlet />
      </main>

      <footer className="bg-charcoal-900 text-charcoal-300 border-t border-white/10 py-10 mt-auto">
        <div className="container px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 rounded bg-amber-500 flex items-center justify-center text-indigo-900 font-bold text-xs">
              S
            </div>
            <span className="font-semibold text-white">ShopFlow</span>
            <span>— E-Commerce Marketplace with Embedded Machine Learning</span>
          </div>
          <div className="flex items-center gap-6 text-charcoal-400">
            <span>FastAPI Monolith</span>
            <span>·</span>
            <span>PostgreSQL & Redis</span>
            <span>·</span>
            <span>LightGBM & XGBoost</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
