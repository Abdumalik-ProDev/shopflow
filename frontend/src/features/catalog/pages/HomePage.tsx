import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Link } from "react-router-dom";
import { Star, Truck, Zap } from "lucide-react";
import { analyticsApi } from "@/features/analytics/api/analytics";

export default function HomePage() {
  const [summary, setSummary] = React.useState<any>(null);
  const [isPending, setIsPending] = React.useState(true);

  React.useEffect(() => {
    analyticsApi
      .getSummary()
      .then((data) => {
        setSummary(data);
        setIsPending(false);
      })
      .catch(() => setIsPending(false));
  }, []);

  return (
    <section className="space-y-16">
      <div className="text-center">
        <h1 className="text-5xl font-display font-bold text-charcoal-900 tracking-tight">
          Marketplace that learns your business
        </h1>
        <p className="mt-4 text-lg text-charcoal-600 max-w-2xl mx-auto">
          Discover products, personalized recommendations, and intelligent delivery — built with
          professional engineering and machine learning.
        </p>
        <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <Button asChild>
            <Link to="/catalog">Shop catalog</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link to="/">Learn more</Link>
          </Button>
        </div>
      </div>

      {!isPending && summary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <StatCard value={summary.kpis.find((k: any) => k.label === "Total Orders")?.value ?? 0} label="Total Orders" />
          <StatCard value={summary.kpis.find((k: any) => k.label === "GMV (Delivered)")?.value ?? 0} label="GMV" prefix="$" />
          <StatCard value={summary.kpis.find((k: any) => k.label === "Customers")?.value ?? 0} label="Customers" />
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <FeatureCard icon={<Star className="w-6 h-6 text-amber-500" />}>
          Personalized recommendations
          <p className="mt-2 text-sm text-charcoal-600">ML-powered product suggestions tailored to you.</p>
        </FeatureCard>
        <FeatureCard icon={<Truck className="w-6 h-6 text-indigo-600" />}>
          Delivery intelligence
          <p className="mt-2 text-sm text-charcoal-600">Accurate ETAs and late-delivery predictions.</p>
        </FeatureCard>
        <FeatureCard icon={<Zap className="w-6 h-6 text-emerald-500" />}>
          Demand forecasting
          <p className="mt-2 text-sm text-charcoal-600">Inventory planning with XGBoost & LightGBM models.</p>
        </FeatureCard>
      </div>
    </section>
  );
}

function StatCard({ value, label, prefix = "" }: { value: number; label: string; prefix?: string }) {
  return (
    <Card className="p-6 text-center">
      <div className="text-3xl font-bold text-charcoal-900">{prefix}{value}</div>
      <div className="text-sm text-charcoal-500 mt-2">{label}</div>
    </Card>
  );
}

function FeatureCard({ icon, children }: { icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <Card className="p-6">
      <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center mb-4 text-indigo-600">
        {icon}
      </div>
      <CardTitle className="text-lg">
        {typeof children === "string" ? <>{children.split("\n")[0]}</> : children}
      </CardTitle>
      <CardContent className="pt-0">
        {typeof children === "string" ? children.split("\n")[1] : null}
      </CardContent>
    </Card>
  );
}
