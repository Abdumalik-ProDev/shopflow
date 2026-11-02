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
import { Mail, MapPin, CreditCard, Phone, Truck, ShieldCheck, Sparkles } from "lucide-react";
import { ordersApi } from "@/features/orders/api/orders";
import { api } from "@/app/config/api";

const schema = z.object({
  full_name: z.string().min(1, "Full name is required"),
  email: z.string().email("Invalid email"),
  phone: z.string().min(1, "Phone is required"),
  address: z.string().min(1, "Address is required"),
  city: z.string().min(1, "City is required"),
  state: z.string().min(2, "State code required (e.g. SP, RJ)").default("SP"),
  zip: z.string().min(1, "ZIP is required"),
});

export default function CheckoutPage() {
  const { items, total, clear } = useCart();
  const navigate = useNavigate();
  const [orderPlaced, setOrderPlaced] = React.useState(false);
  const [placedOrderId, setPlacedOrderId] = React.useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [etaDays, setEtaDays] = React.useState<number | null>(4.5);
  const [etaModel, setEtaModel] = React.useState<string>("LightGBM-v1.0");

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: {
      full_name: "Jane Doe",
      email: "jane@example.com",
      phone: "+55 11 98765-4321",
      address: "Av. Paulista 1000",
      city: "São Paulo",
      state: "SP",
      zip: "01310-100",
    },
  });

  const selectedState = watch("state") || "SP";

  // ML Delivery ETA live query
  React.useEffect(() => {
    const itemCount = items.reduce((sum, item) => sum + item.quantity, 0);
    if (itemCount === 0) return;

    api
      .post("/analytics/predict-eta", {
        customer_state: selectedState,
        item_count: itemCount,
        freight_total: 15.0,
      })
      .then((res) => {
        if (res.data?.predicted_eta_days) {
          setEtaDays(res.data.predicted_eta_days);
          setEtaModel(res.data.model_version || "LightGBM-v1.0");
        }
      })
      .catch(() => {
        // Fallback default
        setEtaDays(4.5);
      });
  }, [selectedState, items]);

  const onSubmit = async (data: z.infer<typeof schema>) => {
    setIsSubmitting(true);
    const customerId = "guest-customer";
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
      alert("Failed to place order. Please check inputs and retry.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (items.length === 0 && !orderPlaced) {
    navigate("/cart");
    return null;
  }

  if (orderPlaced) {
    return (
      <div className="text-center py-20 max-w-lg mx-auto bg-white rounded-2xl p-8 border border-charcoal-200 shadow-sm">
        <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-4 text-emerald-600">
          <ShieldCheck className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-charcoal-900">Order Confirmed!</h2>
        <p className="mt-2 text-charcoal-600">
          Thank you for your purchase. We have received your order.
        </p>
        {placedOrderId && (
          <div className="mt-4 p-3 bg-cream-50 rounded-lg text-sm text-charcoal-700 font-mono">
            Order Reference: #{placedOrderId}
          </div>
        )}
        <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
          <Button asChild>
            <Link to="/orders">View my orders</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link to="/catalog">Continue shopping</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-display font-bold text-charcoal-900">Checkout</h1>
        <Link to="/cart" className="text-sm text-indigo-900 hover:underline">
          ← Edit cart
        </Link>
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
                <Input id="phone" placeholder="+55 11 98765-4321" {...register("phone")} />
                {errors.phone && <span className="text-xs text-red-600">{errors.phone.message}</span>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Address</Label>
                <Input id="address" placeholder="Av. Paulista 1000" {...register("address")} />
                {errors.address && <span className="text-xs text-red-600">{errors.address.message}</span>}
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div className="space-y-2 col-span-1">
                  <Label htmlFor="state">State</Label>
                  <Input id="state" placeholder="SP" maxLength={2} {...register("state")} />
                </div>
                <div className="space-y-2 col-span-2">
                  <Label htmlFor="city">City</Label>
                  <Input id="city" placeholder="São Paulo" {...register("city")} />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="zip">ZIP</Label>
                <Input id="zip" placeholder="01310-100" {...register("zip")} />
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

              {/* ML Delivery ETA Notice */}
              <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-3 text-xs text-indigo-950 flex items-start gap-2.5">
                <Truck className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold">Estimated Delivery:</span> ~{etaDays ?? 4.5} business days
                  <p className="text-indigo-600 mt-0.5 text-[11px]">
                    ML Prediction via {etaModel} (Olist Logistics)
                  </p>
                </div>
              </div>

              <div className="flex justify-between font-semibold pt-4 border-t border-charcoal-200 text-base">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </CardContent>
          </Card>

          <Button type="submit" className="w-full" size="lg" disabled={isSubmitting}>
            {isSubmitting ? "Processing order..." : "Place order"}
          </Button>
        </div>
      </form>
    </div>
  );
}
