import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DollarSign, ShoppingCart, Package, TrendingUp } from "lucide-react";
import { analyticsApi } from "@/features/analytics/api/analytics";

export default function SellerDashboardPage() {
  const [summary, setSummary] = React.useState<any>(null);
  const [isPending, setIsPending] = React.useState(true);

  React.useEffect(() => {
    analyticsApi.getSummary().then(setSummary).finally(() => setIsPending(false));
  }, []);

  const stats = [
    { label: "Total sales", value: summary?.kpis.find((k: any) => k.label === "GMV (Delivered)")?.value ?? 0, prefix: "$", icon: <DollarSign className="w-5 h-5" />, delta: "+12%" },
    { label: "Orders", value: summary?.kpis.find((k: any) => k.label === "Total Orders")?.value ?? 0, icon: <ShoppingCart className="w-5 h-5" />, delta: "+8" },
    { label: "Low stock", value: 3, icon: <Package className="w-5 h-5" />, delta: "-2" },
    { label: "Top product", value: "Ceramic Mug", icon: <TrendingUp className="w-5 h-5" />, delta: "+45%" },
  ];

  if (isPending) {
    return (
      <div className="space-y-8">
        <h1 className="text-2xl font-display font-bold text-charcoal-900">Seller dashboard</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1,2,3,4].map((i) => <SkeletonCard key={i} />)}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-bold text-charcoal-900">Seller dashboard</h1>
        <Badge variant="outline">Seller</Badge>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((s) => (
          <Card key={s.label} className="p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-charcoal-500">{s.label}</p>
                <p className="text-2xl font-semibold">{s.prefix ?? ""}{s.value}</p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600">
                {s.icon}
              </div>
            </div>
            <p className="mt-2 text-xs text-emerald-600 flex items-center gap-1">
              <span className="font-bold">{s.delta}</span> vs last month
            </p>
          </Card>
        ))}
      </div>
    </div>
  );
}

function SkeletonCard() {
  return (
    <Card className="p-5">
      <div className="h-4 bg-charcoal-200 rounded w-1/3 mb-2" />
      <div className="h-6 bg-charcoal-200 rounded w-full" />
    </Card>
  );
}
