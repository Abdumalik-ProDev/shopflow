import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { useCart } from "@/stores/cart";
import { Link } from "react-router-dom";
import { Trash2, CreditCard } from "lucide-react";

export default function CartPage() {
  const { items, removeItem, updateQuantity, total, itemCount, clear } = useCart();

  if (itemCount === 0) {
    return (
      <div className="text-center py-20">
        <div className="w-16 h-16 rounded-full bg-charcoal-100 flex items-center justify-center mx-auto mb-4 text-charcoal-400">
          <CreditCard className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-semibold text-charcoal-900">Your cart is empty</h2>
        <p className="mt-2 text-charcoal-600">Looks like you haven't added anything yet.</p>
        <Button asChild>
          <Link to="/catalog">Start shopping</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-4">
        {items.map((item) => (
          <Card key={item.productId} className="flex flex-col sm:flex-row gap-4 items-center">
            <div className="w-16 h-16 rounded-lg bg-charcoal-100 flex items-center justify-center shrink-0">
              <span className="text-charcoal-400">📦</span>
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-charcoal-900">{item.name}</h3>
              <p className="text-sm text-charcoal-500">${item.price.toFixed(2)} each</p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => updateQuantity(item.productId, item.quantity - 1)}
                className="p-1 hover:bg-charcoal-100 rounded"
              >
                −
              </button>
              <span className="font-medium">{item.quantity}</span>
              <button
                onClick={() => updateQuantity(item.productId, item.quantity + 1)}
                className="p-1 hover:bg-charcoal-100 rounded"
              >
                +
              </button>
              <button
                onClick={() => removeItem(item.productId)}
                className="p-1 hover:bg-red-50 text-red-600 rounded"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </Card>
        ))}
      </div>

      <Card className="lg:col-span-1">
        <CardHeader>
          <CardTitle>Order summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between text-sm">
            <span>Items ({itemCount})</span>
            <span>{items.reduce((s, i) => s + i.quantity, 0)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span>Subtotal</span>
            <span>${total.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-sm text-charcoal-500">
            <span>Shipping</span>
            <span>Calculated at checkout</span>
          </div>
          <div className="h-px bg-charcoal-200" />
          <div className="flex justify-between font-semibold text-lg">
            <span>Total</span>
            <span>${total.toFixed(2)}</span>
          </div>
        </CardContent>
        <CardFooter>
          <Button className="w-full" onClick={clear} variant="outline">
            Clear cart
          </Button>
          <Button className="w-full" asChild>
            <Link to="/checkout">Proceed to checkout</Link>
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
