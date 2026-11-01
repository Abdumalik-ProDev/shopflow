import { RouterProvider } from "react-router-dom";
import { AuthProvider } from "@/app/providers/AuthProvider";
import { ThemeProvider } from "@/app/providers/ThemeProvider";
import { CartProvider } from "@/stores/cart";
import router from "./router";

export default function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <CartProvider>
          <RouterProvider router={router} />
        </CartProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}
