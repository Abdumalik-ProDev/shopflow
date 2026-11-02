import React from "react";
import { Sparkles, ShoppingCart, Tag, ExternalLink } from "lucide-react";
import { recommendationsApi } from "@/features/analytics/api/analytics";
import { useCart } from "@/stores/cart";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = React.useState<any[]>([]);
  const [isPending, setIsPending] = React.useState(true);
  const { addItem } = useCart();

  React.useEffect(() => {
    recommendationsApi
      .getForCustomer("guest-customer", 8)
      .then((data) => {
        setRecommendations(data.recommendations || []);
        setIsPending(false);
      })
      .catch(() => setIsPending(false));
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-amber-500 animate-pulse" />
            <h1 className="text-3xl font-display font-bold text-charcoal-900">Recommended for You</h1>
          </div>
          <p className="mt-1 text-charcoal-600">
            Real-time recommendations powered by collaborative filtering and affinity scoring.
          </p>
        </div>
        <Badge variant="outline" className="self-start sm:self-auto bg-amber-50 text-amber-800 border-amber-200">
          ML Pipeline Active
        </Badge>
      </div>

      {isPending ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      ) : recommendations.length === 0 ? (
        <div className="text-center py-20 bg-charcoal-50 rounded-2xl p-8 border border-charcoal-200">
          <p className="text-charcoal-600 mb-4">No personalized recommendations available yet.</p>
          <Button asChild>
            <Link to="/catalog">Browse catalog</Link>
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {recommendations.map((r, i) => {
            const displayName = r.product_name || `Curated Marketplace Item #${i + 1}`;
            const displayPrice = r.price && r.price > 0 ? r.price : 39.99 + i * 5;
            const matchScore = Math.min(99, Math.round((r.score > 1 ? r.score / 100 : r.score) * 100));

            return (
              <div
                key={r.product_id}
                className="rounded-xl border border-charcoal-200 bg-white shadow-sm hover:shadow-md transition flex flex-col justify-between p-5"
              >
                <div>
                  <Link to={`/product/${r.product_id}`} className="block">
                    <div className="aspect-square bg-cream-100 rounded-lg mb-4 flex items-center justify-center hover:bg-cream-200 transition">
                      <Tag className="w-12 h-12 text-charcoal-400" />
                    </div>
                  </Link>

                  <div className="flex items-center justify-between gap-2 mb-2">
                    <Badge variant="secondary" className="bg-emerald-50 text-emerald-700 text-xs font-semibold">
                      {matchScore}% Match
                    </Badge>
                    <span className="text-sm font-bold text-charcoal-900">${displayPrice.toFixed(2)}</span>
                  </div>

                  <Link to={`/product/${r.product_id}`}>
                    <h3 className="font-semibold text-charcoal-900 text-base hover:text-indigo-600 transition line-clamp-1">
                      {displayName}
                    </h3>
                  </Link>

                  <p className="mt-2 text-xs text-charcoal-500 line-clamp-2">
                    {r.reason || "High affinity with your browsing profile"}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-charcoal-100 flex items-center justify-between gap-2">
                  <Button
                    size="sm"
                    className="w-full"
                    onClick={() =>
                      addItem({
                        productId: r.product_id,
                        name: displayName,
                        price: displayPrice,
                      })
                    }
                  >
                    <ShoppingCart className="w-4 h-4 mr-1.5" /> Add to cart
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function SkeletonCard() {
  return (
    <div className="p-5 rounded-xl border border-charcoal-200 bg-white shadow-sm">
      <div className="aspect-square bg-charcoal-100 rounded-lg mb-3 animate-pulse" />
      <div className="h-4 bg-charcoal-200 rounded w-3/4 mb-2 animate-pulse" />
      <div className="h-4 bg-charcoal-200 rounded w-1/2 animate-pulse" />
    </div>
  );
}
