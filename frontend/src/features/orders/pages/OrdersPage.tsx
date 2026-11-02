import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Package, Clock, CheckCircle, Truck, AlertCircle } from "lucide-react";
import { ordersApi, OrderResponse } from "@/features/orders/api/orders";
import { Link } from "react-router-dom";

export default function OrdersPage() {
  const [orders, setOrders] = React.useState<OrderResponse[]>([]);
  const [isPending, setIsPending] = React.useState(true);

  React.useEffect(() => {
    ordersApi
      .list({ limit: 50 })
      .then((data) => {
        setOrders(data || []);
        setIsPending(false);
      })
      .catch(() => {
        setIsPending(false);
      });
  }, []);

  if (isPending) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-display font-bold text-charcoal-900">Orders History</h1>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-charcoal-100 rounded-xl animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (orders.length === 0) {
    return (
      <div className="text-center py-20 bg-white rounded-2xl p-8 border border-charcoal-200">
        <Package className="w-12 h-12 text-charcoal-400 mx-auto mb-3" />
        <h2 className="text-xl font-semibold text-charcoal-900">No orders found</h2>
        <p className="mt-1 text-charcoal-600 mb-6">You haven't placed any orders yet.</p>
        <Button asChild>
          <Link to="/catalog">Start shopping</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-charcoal-900">Orders History</h1>
          <p className="text-charcoal-600 mt-1">Track marketplace orders and delivery updates.</p>
        </div>
        <Badge variant="outline" className="text-charcoal-700">
          {orders.length} Total Orders
        </Badge>
      </div>

      <div className="space-y-4">
        {orders.map((o) => {
          const isDelivered = o.status === "delivered";
          const isPendingStatus = o.status === "pending";

          return (
            <Card key={o.id} className="p-5 hover:shadow-sm transition">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-start gap-4">
                  <div
                    className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                      isDelivered ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"
                    }`}
                  >
                    {isDelivered ? <CheckCircle className="w-5 h-5" /> : <Truck className="w-5 h-5" />}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-semibold text-charcoal-900 font-mono text-sm">
                        #{o.id.slice(0, 13)}
                      </p>
                      <Badge
                        variant={isDelivered ? "default" : isPendingStatus ? "secondary" : "outline"}
                        className="capitalize text-xs"
                      >
                        {o.status}
                      </Badge>
                    </div>
                    <p className="text-xs text-charcoal-500 mt-1">
                      Placed:{" "}
                      {o.purchase_timestamp
                        ? new Date(o.purchase_timestamp).toLocaleDateString()
                        : "Recent"}
                      {" · "}
                      {o.items?.length || 1} item{o.items?.length !== 1 ? "s" : ""}
                    </p>
                  </div>
                </div>

                <div className="text-right flex sm:flex-col justify-between items-center sm:items-end">
                  <span className="text-xs text-charcoal-500 hidden sm:inline">Order Total</span>
                  <p className="text-lg font-bold text-charcoal-900">${o.total.toFixed(2)}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
