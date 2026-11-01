import React from "react";
import { Sparkles } from "lucide-react";
import { recommendationsApi } from "@/features/analytics/api/analytics";

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = React.useState<any[]>([]);
  const [isPending, setIsPending] = React.useState(true);

  React.useEffect(() => {
    recommendationsApi.getForCustomer("guest-customer", 8).then((data) => {
      setRecommendations(data.recommendations);
      setIsPending(false);
    });
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-amber-500" />
        <h1 className="text-2xl font-display font-bold text-charcoal-900">For you</h1>
      </div>
      <p className="text-charcoal-600">Personalized recommendations powered by our ML models.</p>

      {isPending ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1,2,3,4,5,6].map((i) => <SkeletonCard key={i} />)}
        </div>
      ) : recommendations.length === 0 ? (
        <div className="text-center py-20 text-charcoal-500">No recommendations available yet.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommendations.map((r) => (
            <Card key={r.product_id} className="p-4">
              <div className="aspect-square bg-charcoal-100 rounded-lg mb-3 flex items-center justify-center">
                <span className="text-charcoal-400">☕</span>
              </div>
              <h3 className="font-semibold text-charcoal-900 text-base">{r.product_id}</h3>
              <span className="text-amber-600 font-medium">${r.score.toFixed(2)}</span>
              <p className="mt-2 text-sm text-charcoal-500">{r.reason}</p>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`rounded-xl border border-charcoal-200 bg-white shadow-sm ${className ?? ""}`}>{children}</div>
  );
}

function SkeletonCard() {
  return (
    <div className="p-4">
      <div className="aspect-square bg-charcoal-100 rounded-lg mb-3" />
      <div className="h-4 bg-charcoal-200 rounded w-3/4 mb-2" />
      <div className="h-4 bg-charcoal-200 rounded w-1/2" />
    </div>
  );
}
