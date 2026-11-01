import { createBrowserRouter, RouteObject } from "react-router-dom";
import AppLayout from "@/app/layouts/AppLayout";
import MainLayout from "@/app/layouts/MainLayout";
import AuthLayout from "@/app/layouts/AuthLayout";
import AdminLayout from "@/app/layouts/AdminLayout";
import HomePage from "@/features/catalog/pages/HomePage";
import CatalogPage from "@/features/catalog/pages/CatalogPage";
import ProductDetailPage from "@/features/catalog/pages/ProductDetailPage";
import CartPage from "@/features/cart/pages/CartPage";
import CheckoutPage from "@/features/checkout/pages/CheckoutPage";
import LoginPage from "@/features/auth/pages/LoginPage";
import RegisterPage from "@/features/auth/pages/RegisterPage";
import AccountPage from "@/features/customers/pages/AccountPage";
import SellerDashboardPage from "@/features/sellers/pages/SellerDashboardPage";
import AdminDashboardPage from "@/features/analytics/pages/AdminDashboardPage";
import OrdersPage from "@/features/orders/pages/OrdersPage";
import RecommendationsPage from "@/features/recommendations/pages/RecommendationsPage";


const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "catalog", element: <MainLayout><CatalogPage /></MainLayout> },
      { path: "product/:id", element: <MainLayout><ProductDetailPage /></MainLayout> },
      { path: "cart", element: <MainLayout><CartPage /></MainLayout> },
      { path: "checkout", element: <MainLayout><CheckoutPage /></MainLayout> },
      { path: "account", element: <MainLayout><AccountPage /></MainLayout> },
      { path: "orders", element: <MainLayout><OrdersPage /></MainLayout> },
      { path: "seller", element: <MainLayout><SellerDashboardPage /></MainLayout> },
      { path: "admin", element: <AdminLayout><AdminDashboardPage /></AdminLayout> },
      { path: "recommendations", element: <MainLayout><RecommendationsPage /></MainLayout> },
    ],
  },
  {
    path: "auth",
    element: <AuthLayout title="Welcome back" subtitle="Sign in to your ShopFlow account" action="Create an account" actionHref="/auth/register" actionLabel="Don't have an account? " />,
    children: [
      { path: "login", element: <LoginPage /> },
      { path: "register", element: <RegisterPage /> },
    ],
  },
] as unknown as RouteObject[]);

export default router;
