import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCart } from "@/stores/cart";
import { Link, useNavigate } from "react-router-dom";
import { Mail, MapPin, CreditCard, Phone } from "lucide-react";
import { ordersApi } from "@/features/orders/api/orders";

const schema = z.object({
  full_name: z.string().min(1, "Full name is required"),
  email: z.string().email("Invalid email"),
  phone: z.string().min(1, "Phone is required"),
  address: z.string().min(1, "Address is required"),
  city: z.string().min(1, "City is required"),
  zip: z.string().min(1, "ZIP is required"),
});

export default function CheckoutPage() {
  const { items, total, clear } = useCart();
  const navigate = useNavigate();
  const [orderPlaced, setOrderPlaced] = React.useState(false);
  const [placedOrderId, setPlacedOrderId] = React.useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<z.infer<typeof schema>>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: z.infer<typeof schema>) => {
    // Build order from cart
    const customerId = "guest-customer"; // In production, from auth
    const payload = {
      customer_id: customerId,
      items: items.map((i) => ({
        product_id: i.productId,
        seller_id: "seller-1",
        price: i.price,
        freight_value: 0,
        quantity: i.quantity,
      })),
    };
    try {
      const order = await ordersApi.create(payload);
      setPlacedOrderId(order.id);
      setOrderPlaced(true);
      clear();
    } catch (e) {
      alert("Failed to place order");
    }
  };

  if (items.length === 0) {
    navigate("/cart");
    return null;
  }

  if (orderPlaced) {
    return (
      <div className="text-center py-20">
        <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-4 text-emerald-600">
          <CreditCard className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-charcoal-900">Order placed!</h2>
        <p className="mt-2 text-charcoal-600">Thank you for your purchase.</p>
        {placedOrderId && (
          <p className="mt-4 text-sm text-charcoal-500">Order #{placedOrderId}</p>
        )}
        <Button className="mt-8" asChild>
          <Link to="/catalog">Continue shopping</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-bold text-charcoal-900">Checkout</h1>
        <a href="/cart" className="text-sm text-indigo-900 hover:underline">
          Edit cart
        </a>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Shipping details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="full_name">Full name</Label>
                <Input id="full_name" placeholder="Jane Doe" {...register("full_name")} />
                {errors.full_name && <span className="text-xs text-red-600">{errors.full_name.message}</span>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" placeholder="jane@example.com" {...register("email")} />
                {errors.email && <span className="text-xs text-red-600">{errors.email.message}</span>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Phone</Label>
                <Input id="phone" placeholder="+1 555-0000" {...register("phone")} />
                {errors.phone && <span className="text-xs text-red-600">{errors.phone.message}</span>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Address</Label>
                <Input id="address" placeholder="123 Market St" {...register("address")} />
                {errors.address && <span className="text-xs text-red-600">{errors.address.message}</span>}
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="city">City</Label>
                  <Input id="city" placeholder="São Paulo" {...register("city")} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="zip">ZIP</Label>
                  <Input id="zip" placeholder="01000-000" {...register("zip")} />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Order summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {items.map((item) => (
                <div key={item.productId} className="flex justify-between items-center py-2 border-b border-charcoal-100 last:border-0">
                  <div>
                    <p className="text-sm font-medium">{item.name}</p>
                    <p className="text-xs text-charcoal-500">Qty {item.quantity}</p>
                  </div>
                  <span className="font-medium">${(item.price * item.quantity).toFixed(2)}</span>
                </div>
              ))}
              <div className="flex justify-between font-semibold pt-4 border-t border-charcoal-200">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </CardContent>
          </Card>

          <Button type="submit" className="w-full" size="lg">
            Place order
          </Button>
        </div>
      </form>
    </div>
  );
}
