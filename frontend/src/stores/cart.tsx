import React, { useState } from "react";

export interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
  image?: string;
}

interface CartContextType {
  items: CartItem[];
  addItem: (item: Omit<CartItem, "quantity"> & { quantity?: number }) => void;
  removeItem: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  clear: () => void;
  total: number;
  itemCount: number;
}

const CartContext = React.createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);

  const total = items.reduce((sum: number, i: CartItem) => sum + i.price * i.quantity, 0);
  const itemCount = items.reduce((sum: number, i: CartItem) => sum + i.quantity, 0);

  const addItem = (item: Omit<CartItem, "quantity"> & { quantity?: number }) => {
    setItems((prev: CartItem[]) => {
      const existing = prev.find((i) => i.productId === item.productId);
      if (existing) {
        return prev.map((i) =>
          i.productId === item.productId
            ? { ...i, quantity: i.quantity + (item.quantity ?? 1) }
            : i
        );
      }
      return [...prev, { ...item, quantity: item.quantity ?? 1 }];
    });
  };

  const removeItem = (productId: string) => {
    setItems((prev: CartItem[]) => prev.filter((i) => i.productId !== productId));
  };

  const updateQuantity = (productId: string, quantity: number) => {
    if (quantity <= 0) {
      removeItem(productId);
      return;
    }
    setItems((prev: CartItem[]) => prev.map((i) => (i.productId === productId ? { ...i, quantity } : i)));
  };

  const clear = () => setItems([]);

  return (
    <CartContext.Provider value={{ items, addItem, removeItem, updateQuantity, clear, total, itemCount }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = React.useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used within CartProvider");
  return ctx;
}
