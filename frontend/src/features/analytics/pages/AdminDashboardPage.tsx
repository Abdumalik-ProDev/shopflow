import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DollarSign, Users, ShoppingCart, Activity } from "lucide-react";
import { analyticsApi } from "@/features/analytics/api/analytics";

export default function AdminDashboardPage() {
  const [summary, setSummary] = React.useState<any>(null);
  const [isPending, setIsPending] = React.useState(true);

  React.useEffect(() => {
    analyticsApi.getSummary().then(setSummary).finally(() => setIsPending(false));
  }, []);

  if (isPending) {
    return (
      <div className="space-y-8">
        <h1 className="text-2xl font-display font-bold text-charcoal-900">Marketplace analytics</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1,2,3,4].map((i) => <SkeletonCard key={i} />)}
        </div>
      </div>
    );
  }

  const kpis = summary?.kpis ?? [];
  const get = (label: string) => kpis.find((k: any) => k.label === label)?.value ?? 0;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-bold text-charcoal-900">Marketplace analytics</h1>
        <Badge variant="outline">Admin</Badge>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard label="GMV" value={get("GMV (Delivered)")} prefix="$" icon={<DollarSign className="w-5 h-5 text-white" />} />
        <StatCard label="Orders" value={get("Total Orders")} icon={<ShoppingCart className="w-5 h-5 text-white" />} />
        <StatCard label="Customers" value={get("Customers")} icon={<Users className="w-5 h-5 text-white" />} />
        <StatCard label="Conversion" value={get("Conversion Rate")} suffix="%" icon={<Activity className="w-5 h-5 text-white" />} />
      </div>

      <div className="mt-8 bg-white p-6 rounded-2xl border border-charcoal-200 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-charcoal-900">Recent Marketplace Sales Trend</h2>
            <p className="text-xs text-charcoal-500">Aggregated daily revenue from live orders</p>
          </div>
          <Badge variant="secondary" className="text-xs">
            {summary?.sales_over_time?.length || 0} Total Reporting Days
          </Badge>
        </div>

        {summary?.sales_over_time?.length ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead>
                <tr className="border-b border-charcoal-100 text-xs font-semibold text-charcoal-500 uppercase tracking-wider">
                  <th className="py-2.5 px-3">Date</th>
                  <th className="py-2.5 px-3">Orders</th>
                  <th className="py-2.5 px-3 text-right">Daily Revenue</th>
                  <th className="py-2.5 px-3 text-right">Volume Activity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-charcoal-100">
                {summary.sales_over_time.slice(-10).reverse().map((point: any) => (
                  <tr key={point.date} className="hover:bg-cream-50 transition">
                    <td className="py-2.5 px-3 font-medium text-charcoal-900">{point.date}</td>
                    <td className="py-2.5 px-3 text-charcoal-700">{point.orders} orders</td>
                    <td className="py-2.5 px-3 text-right font-semibold text-charcoal-900">
                      ${Number(point.sales).toFixed(2)}
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <div className="inline-block w-24 bg-charcoal-100 rounded-full h-2 overflow-hidden">
                        <div
                          className="bg-indigo-600 h-full rounded-full"
                          style={{
                            width: `${Math.min(100, Math.max(15, (point.orders / 5) * 100))}%`,
                          }}
                        />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-sm text-charcoal-500 py-10 text-center">No sales data recorded yet.</div>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value, prefix, suffix, icon }: { label: string; value: number; prefix?: string; suffix?: string; icon: React.ReactNode }) {
  return (
    <Card className="p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-charcoal-500">{label}</p>
          <p className="text-2xl font-semibold">{prefix ?? ""}{value}{suffix ?? ""}</p>
        </div>
        <div className="w-10 h-10 rounded-lg bg-charcoal-800 flex items-center justify-center text-white">
          {icon}
        </div>
      </div>
    </Card>
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
