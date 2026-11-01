import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Package, Clock, CheckCircle } from "lucide-react";

const orders = [
  { id: "#SF-1001", status: "Delivered", total: "$89.50", badge: "default", icon: <CheckCircle className="w-4 h-4 text-emerald-600" /> },
  { id: "#SF-1002", status: "Shipping", total: "$142.00", badge: "secondary", icon: <Truck className="w-4 h-4 text-amber-600" /> },
  { id: "#SF-1003", status: "Pending", total: "$56.00", badge: "outline", icon: <Clock className="w-4 h-4 text-charcoal-500" /> },
];

export default function OrdersPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-display font-bold text-charcoal-900">My orders</h1>
      <div className="space-y-4">
        {orders.map((o) => (
          <Card key={o.id} className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold">{o.id}</p>
                <p className="text-sm text-charcoal-500">Order placed</p>
              </div>
              <div className="text-right">
                <p className="font-semibold">{o.total}</p>
                <Badge variant={(o.badge as any)}>{o.status}</Badge>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

function Truck({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2m4-2v2m-7-3H12a3 3 0 003 3v2a3 3 0 01-3 3H6a3 3 0 01-3-3V6a3 3 0 003-3h6a3 3 0 013 3z" />
    </svg>
  );
}
